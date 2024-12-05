import logging
import os
import re
import subprocess
from math import ceil
from pathlib import Path

import bgzip
import duckdb
import pandas as pd
from caseconverter import snakecase
from duckdb import DuckDBPyConnection


def convert(
    vcf_path: Path,
    db_path: Path,
    parquet_dir_path: Path,
    multiallelics: bool,
    compound_info_fields: set[str],
    url_encoded_col_name_regexes: list[str],
    tab_path: Path | None = None,
) -> None:
    val_info_types = get_vcf_val_info_types(
        vcf_path, multiallelics, compound_info_fields
    )

    if tab_path is None:
        tab_path = vcf_path.with_suffix("").with_suffix(".tsv")

    try:
        os.remove(db_path)
    except OSError:
        pass

    with duckdb.connect(db_path) as db:
        set_up_db(db, val_info_types)

        write_tab_vcf(vcf_gz_path=vcf_path, tab_path=tab_path)

        logging.info(f"Reading {vcf_path} into {db_path}")
        populate_db(db, tab_path, val_info_types, url_encoded_col_name_regexes)

        logging.info(f"Exporting schema and Parquet files to {parquet_dir_path}")
        db.sql(f"EXPORT DATABASE '{parquet_dir_path}' (FORMAT PARQUET)")


def set_up_db(db: DuckDBPyConnection, val_info_types: pd.DataFrame) -> None:
    db.sql("""
        SET preserve_insertion_order = false;
        SET enable_progress_bar = false;
    """)

    val_info_types_tbl = val_info_types.copy()
    val_info_types_tbl["id_snake"] = val_info_types_tbl["id"]

    db.register("val_info_types_view", val_info_types_tbl)

    db.sql("""
        CREATE TABLE IF NOT EXISTS
            val_info_types
        AS
            SELECT * from val_info_types_view
    """)

    db.unregister("val_info_types_view")

    snake_case_col(db, tbl="val_info_types", col="id_snake")

    db.sql("""
        CREATE TABLE IF NOT EXISTS vcf_lines (
            chrom VARCHAR NOT NULL,
            pos UINTEGER NOT NULL,
            id VARCHAR,
            ref VARCHAR,
            alt VARCHAR,
            qual VARCHAR,
            filters VARCHAR,
            info VARCHAR,
            format VARCHAR,
            values VARCHAR
        );
    """)

    db.sql("""
        CREATE TABLE IF NOT EXISTS variants (
            vid UINTEGER PRIMARY KEY,
            chrom VARCHAR NOT NULL,
            pos UINTEGER NOT NULL,
            id VARCHAR,
            ref VARCHAR,
            alt VARCHAR,
            qual VARCHAR,
            filters VARCHAR[]
        );
    """)

    db.sql("""
        CREATE TABLE IF NOT EXISTS kv (
            vid UINTEGER,
            k VARCHAR,
            v VARCHAR
        );
    """)

    db.sql("""
        CREATE TABLE IF NOT EXISTS kv_compound_info (
            vid UINTEGER,
            k VARCHAR,
            k_sub VARCHAR,
            ix INTEGER,
            v VARCHAR
        );
    """)

    kind_map = [{"kind": "value", "tbl": "vals"}, {"kind": "info", "tbl": "info"}]

    for x in kind_map:
        types = val_info_types.loc[val_info_types["kind"].eq(x["kind"])].copy()
        req_col_types = types[["v_col_name", "col_def"]].drop_duplicates()
        cols = req_col_types["v_col_name"] + " " + req_col_types["col_def"]

        db.sql(f"""
            CREATE TABLE IF NOT EXISTS {x['tbl']}_tmp (
                vid UINTEGER,
                k VARCHAR,
                {', '.join(cols)}
            );
        """)

        db.sql(f"""
            CREATE TABLE IF NOT EXISTS {x['tbl']} (
                vid UINTEGER REFERENCES variants (vid),
                k VARCHAR NOT NULL,
                {', '.join(cols)}
            );
        """)

        if x["kind"] == "info":
            sub_fields = val_info_types.loc[
                val_info_types["parent_id"].isin(types["id"]),
                ["ix", "parent_id", "id"],
            ].rename(columns={"parent_id": "k", "id": "k_sub"})

            db.register("sub_fields", sub_fields)


def get_vcf_val_info_types(
    vcf_path: Path, multiallelics: bool, compound_info_fields: set[str]
) -> pd.DataFrame:
    header_lines = get_header_lines(vcf_path)
    header_lines = [
        x for x in header_lines if x.startswith("##FORMAT") or x.startswith("##INFO")
    ]

    type_map = {
        "Integer": "INTEGER",
        "Float": "FLOAT",
        "String": "VARCHAR",
        "Character": "VARCHAR",
        "Flag": "BOOLEAN",
    }

    arr = []
    sub_arr = []

    for x in header_lines:
        kind = re.search(r"^##(\w+)", x).group(1).lower()
        interior = re.search(r"<(.+)>$", x).group(1)
        parts = re.findall(r'([A-Za-z0-9_]+)=(".*?"|[^,]+)', interior)

        d = {k.lower(): v.strip('"') for k, v in parts}
        d["kind"] = kind if kind == "info" else "value"

        if d["id"] in compound_info_fields:
            d["has_children"] = True
            d["type"] = "JSON"

            desc = re.search(r"^.+:['\s]*([^']+)['\s]*$", d["description"]).group(1)
            subfields = re.split(r"\s*\|\s*", desc)

            for ix, s in enumerate(subfields):
                dsub = {
                    "id": s,
                    "has_children": False,
                    "number": "1",
                    "type": "VARCHAR",
                    "kind": "sub_info",
                    "parent_id": d["id"],
                    "ix": ix + 1,
                }

                sub_arr.append(dsub)

        else:
            d["has_children"] = False
            d["type"] = type_map[d["type"]]

        arr.append(d)

    df = pd.DataFrame(arr + sub_arr).astype(
        {
            "id": "string",
            "number": "string",
            "type": "string",
            "description": "string",
            "kind": "string",
            "has_children": "boolean",
            "parent_id": "string",
            "ix": "UInt64",
        }
    )

    if not multiallelics:
        # force single value if we're assuming multiallelics have already been split to
        # separate rows
        df.loc[df["number"].eq("A"), "number"] = "1"

    df["col_def"] = df["type"]
    df["is_list"] = ~df["number"].isin({"0", "1"})
    df.loc[df["is_list"], "col_def"] += "[]"

    df["v_col_name"] = "v_" + df["type"].str.lower()
    df.loc[df["is_list"], "v_col_name"] += "_arr"

    return df


def get_header_lines(vcf_path: Path) -> list[str]:
    """
    Read all of the header lines in a list of VCF files and return their union,
    retaining their order.

    :param vcf_path: a path to a VCF file
    :return: a list of the distinct header lines in their original order
    """

    header_lines = []
    col_header_line = None

    # don't read more lines than necessary to get the entire header
    break_next_time = False

    with open(vcf_path, "rb") as raw:
        logging.info(f"Reading {os.path.basename(vcf_path)} header")
        this_header_texts = ""  # start collecting header text

        # assume file is bgzipped
        with bgzip.BGZipReader(raw) as f:
            while True:
                # read a small block of bytes at a time
                if not (d := f.read(10 * 1024)):
                    break

                # concat the latest chunk of text
                text = d.tobytes().decode()
                d.release()
                this_header_texts += text

                # check if we've reached the end of the header section and get one
                # more chunk
                if break_next_time:
                    break
                elif "\n#CHROM" in this_header_texts:
                    break_next_time = True

        # extract the header lines and the column headers
        this_header_lines = this_header_texts.split("\n")

        if col_header_line is None:
            # extract the line with column names
            col_header_line = [x for x in this_header_lines if x.startswith("#CHROM")][
                0
            ]

        this_header_lines = [x for x in this_header_lines if x.startswith("##")]

        # add to the collected header lines
        header_lines.extend(this_header_lines)

    # de-dup but keep original order of lines
    return (
        pd.Series([*header_lines, col_header_line])
        .astype("string")
        .drop_duplicates()
        .tolist()
    )


def write_tab_vcf(vcf_gz_path: Path, tab_path: Path) -> None:
    logging.info(f"Converting {vcf_gz_path} to TSV")
    subprocess.run(["bcftools", "view", vcf_gz_path, "--no-header", "-o", tab_path])


def populate_db(
    db: DuckDBPyConnection,
    tab_path: Path,
    val_info_types: pd.DataFrame,
    url_encoded_col_name_regexes: list[str],
) -> None:
    db.sql(f"""
        COPY
            vcf_lines
        FROM
            '{tab_path}' (DELIMITER '\\t', AUTO_DETECT false);
    """)

    db.sql("""
        UPDATE vcf_lines SET id = NULL where id = '.';
        UPDATE vcf_lines SET ref = NULL where ref = '.';
        UPDATE vcf_lines SET alt = NULL where alt = '.';
        UPDATE vcf_lines SET qual = NULL where qual = '.';
        UPDATE vcf_lines SET filters = NULL where filters = '.';
        UPDATE vcf_lines SET info = NULL where info = '.';
        UPDATE vcf_lines SET format = NULL where format = '.';
        UPDATE vcf_lines SET values = NULL where values = '.';
    """)

    db.sql("""
        BEGIN;
    
        CREATE SEQUENCE vid_sequence;
        
        ALTER TABLE
            vcf_lines
        ADD COLUMN
            vid UINTEGER
        DEFAULT
            nextval('vid_sequence');
        
        DROP SEQUENCE vid_sequence;
        
        COMMIT;
    """)

    db.sql("""
        INSERT INTO
            variants (
                vid,
                chrom,
                pos,
                id,
                ref,
                alt,
                qual,
                filters
            )
        SELECT
            vid,
            chrom,
            pos,
            id,
            ref,
            alt,
            qual,
            str_split(filters, ';')
        FROM
            vcf_lines;
    """)

    n_variants = db.table("vcf_lines").shape[0]
    max_batch_size = 100000
    n_batches = 1 + n_variants // max_batch_size
    batch_size = ceil(n_variants / n_batches)

    for i in range(n_batches):
        logging.info(f"Loading batch {i+1} of {n_batches}")
        offset = i * batch_size

        populate_vals(db, val_info_types, limit=batch_size, offset=offset)
        populate_info(db, val_info_types, limit=batch_size, offset=offset)

    db.sql("DROP TABLE IF EXISTS kv;")
    db.sql("DROP TABLE IF EXISTS kv_compound_info;")
    db.sql("DROP TABLE IF EXISTS vcf_lines;")
    db.unregister("sub_fields")

    for tbl in ["vals", "info"]:
        make_constraints(db, tbl)
        snake_case_col(db, tbl, "k")

    urldecode_cols(db, url_encoded_col_name_regexes)


def make_constraints(db: DuckDBPyConnection, tbl: str) -> None:
    logging.info(f"Applying constraints to {tbl}")

    db.sql(f"""
        INSERT INTO
            {tbl}
        BY NAME
        SELECT
            *
        FROM
            {tbl}_tmp;
    """)

    db.sql(f"DROP TABLE {tbl}_tmp;")


def snake_case_col(db: DuckDBPyConnection, tbl: str, col: str) -> None:
    snake_map = db.table(tbl)[col].distinct().df()
    snake_map[f"{col}_snake"] = snake_map[col].apply(snakecase)

    db.register("snake_map", snake_map)

    db.sql(f"""
        UPDATE
            {tbl}
        SET
            {col} = snake_map.{col}_snake
        FROM
            snake_map
        WHERE
            {tbl}.{col} = snake_map.{col};
    """)

    db.unregister("snake_map")


def populate_vals(
    db: DuckDBPyConnection,
    val_info_types: pd.DataFrame,
    limit: int = 0,
    offset: int = 0,
) -> None:
    db.sql("TRUNCATE kv;")

    db.sql(f"""
        INSERT INTO
            kv (
                vid,
                k,
                v
            )
        SELECT
            vid,
            unnest(str_split(format, ':')) as k,
            unnest(str_split(values, ':')) as v
        FROM (
            SELECT
                vid,
                format,
                values
            FROM
                vcf_lines
            ORDER BY
                chrom,
                pos,
                ref,
                alt
            LIMIT
                {limit}
            OFFSET
                {offset}
        );
    """)

    val_types = val_info_types.loc[
        val_info_types["kind"].eq("value")
        & val_info_types["id"].isin(db.table("kv")["k"].distinct().df()["k"])
    ].copy()

    cast_and_insert_v(
        db=db, src_table_name="kv", dest_table_name="vals_tmp", types_df=val_types
    )


def populate_info(
    db: DuckDBPyConnection,
    val_info_types: pd.DataFrame,
    limit: int = 0,
    offset: int = 0,
) -> None:
    db.sql("TRUNCATE kv;")
    db.sql("TRUNCATE kv_compound_info;")

    info_types = val_info_types.loc[val_info_types["kind"].eq("info")].copy()
    info_types_expr = ", ".join(["'" + x + "'" for x in info_types["id"]])

    db.sql(f"""
        INSERT INTO
            kv (
                vid,
                k,
                v
            )
        SELECT
            vid,
            annot[1] as k,
            annot[2] as v
        FROM (
            SELECT
                vid,
                str_split(unnest(str_split(info, ';')), '=') AS annot
            FROM (
                SELECT
                    vid,
                    info
                FROM
                    vcf_lines
                ORDER BY
                    chrom,
                    pos,
                    ref,
                    alt
                LIMIT
                    {limit}
                OFFSET
                    {offset}
            )
        )
        WHERE
            k IN ({info_types_expr});
    """)

    info_types = info_types.loc[
        info_types["id"].isin(db.table("kv")["k"].distinct().df()["k"])
    ].copy()

    flag_fields = info_types["id"].loc[
        info_types["kind"].eq("info") & info_types["number"].eq("0")
    ]

    db.sql(f"""
        UPDATE
            kv
        SET
            v = 'true'
        WHERE
            k in ({', '.join(["'" + x + "'" for x in flag_fields])})
    """)

    simple_info_types = info_types.loc[~info_types["has_children"]].copy()
    compound_info_types = info_types.loc[info_types["has_children"]].copy()

    cast_and_insert_v(
        db=db,
        src_table_name="kv",
        dest_table_name="info_tmp",
        types_df=simple_info_types,
    )

    compound_types_expr = ", ".join(["'" + x + "'" for x in compound_info_types["id"]])

    db.sql(f"""
        DELETE FROM
            kv
        WHERE
            k NOT IN ({compound_types_expr});
    """)

    db.sql(f"""
        INSERT INTO
            kv_compound_info (
                vid,
                k,
                k_sub,
                ix,
                v
            )
        SELECT
           vid,
           k,
           k_sub,
           ix,
           v
        FROM (
            WITH compound_info_split AS (
                SELECT
                    vid,
                    k,
                    str_split_regex(trim(v, '()'), '\\s*\\|\\s*') AS v
                FROM
                    kv
            ),
            compound_info_exploded AS (
                SELECT
                    vid,
                    k,
                    unnest(v) AS v,
                    generate_subscripts(v, 1) AS ix
                FROM
                    compound_info_split
            )
            SELECT
                vid,
                compound_info_exploded.k,
                sub_fields.k_sub,
                sub_fields.ix,
                CASE
                    WHEN v IN ('', '.')
                THEN
                    NULL
                ELSE
                    v
                END AS v
            FROM
                compound_info_exploded
            INNER JOIN
                sub_fields
            ON
                compound_info_exploded.k = sub_fields.k
                AND
                compound_info_exploded.ix = sub_fields.ix
        );
    """)

    snake_case_col(db, tbl="kv_compound_info", col="k_sub")

    db.sql("TRUNCATE kv;")

    db.sql(f"""
        INSERT INTO
            kv (
                vid,
                k,
                v
            )
        SELECT
            vid,
            k,
            v
        FROM (
            WITH compound_info_maps AS (
                SELECT
                    vid,
                    k,
                    MAP(
                        list(k_sub ORDER BY ix),
                        list(v ORDER BY ix)
                    )::JSON::VARCHAR AS v
                FROM
                    kv_compound_info
                GROUP BY
                    vid,
                    k
            )
            SELECT
                vid,
                k,
                '[' || string_agg(v, ',') || ']' AS v
            FROM
                compound_info_maps
            GROUP BY
                vid,
                k
        )
    """)

    compound_info_types["is_list"] = False

    cast_and_insert_v(
        db=db,
        src_table_name="kv",
        dest_table_name="info_tmp",
        types_df=compound_info_types,
    )


def cast_and_insert_v(
    db: DuckDBPyConnection,
    src_table_name: str,
    dest_table_name: str,
    types_df: pd.DataFrame,
) -> None:
    for (v_col_name, is_list), g in types_df.groupby(["v_col_name", "is_list"]):
        k_ids_expr = ", ".join(["'" + x + "'" for x in g["id"]])

        if is_list:
            db.sql(f"""
                INSERT INTO
                    {dest_table_name} (
                        vid,
                        k,
                        {v_col_name}
                    )
                SELECT
                    vid,
                    k,
                    str_split(v, ',') as {v_col_name}
                FROM
                    {src_table_name}
                WHERE
                    k IN ({k_ids_expr});
            """)
        else:
            db.sql(f"""
                INSERT INTO
                    {dest_table_name} (
                        vid,
                        k,
                        {v_col_name}
                    )
                SELECT
                    vid,
                    k,
                    v
                FROM
                    {src_table_name}
                WHERE
                    k IN ({k_ids_expr});
            """)


def urldecode_cols(
    db: DuckDBPyConnection, url_encoded_col_name_regexes: list[str]
) -> None:
    if len(url_encoded_col_name_regexes) == 0:
        return

    logging.info("URL-decoding info fields")

    url_encoded_col_name_regex = "|".join(url_encoded_col_name_regexes)

    db.sql(f"""
        UPDATE
            info
        SET
            v_varchar = url_decode(v_varchar)
        WHERE
            regexp_matches(k, '{url_encoded_col_name_regex}')
            AND
            contains(v_varchar, '%')
    """)

    db.sql(f"""
        UPDATE
            info
        SET
            v_varchar_arr = list_transform(v_varchar_arr, x -> url_decode(x))
        WHERE
            regexp_matches(k, '{url_encoded_col_name_regex}')
            AND
            contains(v_varchar_arr::text, '%')
    """)

    still_encoded = db.sql(f"""
        SELECT
            vid,
            k,
            v_varchar,
            v_varchar_arr
        FROM
            info
        WHERE
            NOT regexp_matches(k, '{url_encoded_col_name_regex}')
            AND (
                contains(v_varchar, '%')
                OR
                contains(v_varchar_arr::varchar, '%')
            )
        ORDER BY
            random()
    """)

    if still_encoded.shape[0] > 0:
        still_encoded_k = ", ".join(
            [x[0] for x in still_encoded["k"].distinct().fetchall()]
        )

        logging.warning(
            f"{still_encoded.shape[0]} values for annotations [{still_encoded_k}] "
            f"might need to be URL_decoded:\n{still_encoded}"
        )
