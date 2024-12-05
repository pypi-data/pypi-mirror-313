import logging
from pathlib import Path
from typing import Annotated, Any

import pandas as pd
import typer

import vcf_to_duckdb.convert_utils

pd.set_option("display.max_columns", 30)
pd.set_option("display.max_colwidth", 50)
pd.set_option("display.max_info_columns", 30)
pd.set_option("display.max_info_rows", 20)
pd.set_option("display.max_rows", 20)
pd.set_option("display.max_seq_items", None)
pd.set_option("display.width", 200)
pd.set_option("expand_frame_repr", True)
pd.set_option("mode.chained_assignment", "warn")

app = typer.Typer()

config: dict[str, Any] = {}


# noinspection PyUnusedLocal
def done(*args, **kwargs):
    logging.info("Done.")


@app.callback(result_callback=done)
def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )


@app.command()
def convert(
    vcf: Annotated[Path, typer.Option(exists=True)],
    db: Annotated[Path, typer.Option()],
    parquet_dir: Annotated[Path, typer.Option()],
    multiallelics: Annotated[bool, typer.Option()] = True,
    compound_info_field: Annotated[list[str] | None, typer.Option()] = None,
    url_encoded_col_name_regex: Annotated[list[str] | None, typer.Option()] = None,
    tab: Annotated[Path | None, typer.Option()] = None,
) -> None:
    if compound_info_field is None:
        compound_info_field = []

    if url_encoded_col_name_regex is None:
        url_encoded_col_name_regex = []

    vcf_to_duckdb.convert_utils.convert(
        vcf_path=vcf,
        db_path=db,
        parquet_dir_path=parquet_dir,
        multiallelics=multiallelics,
        compound_info_fields=set(compound_info_field),
        url_encoded_col_name_regexes=url_encoded_col_name_regex,
        tab_path=tab,
    )


if __name__ == "__main__":
    app()
