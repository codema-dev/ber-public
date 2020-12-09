import csv
import json

from os import path

import dask.dataframe as dd
import prefect

from prefect import task


HERE = Path(__name__)


@task
def convert(input_filepath: str, output_filepath: str) -> None:
    """Convert csv file to parquet.

    Args:
        input_filepath (str): Path to input data
        output_filepath (str): Path to output data
    """
    with open(HERE / "dtypes.json", "r") as json_file:
        dtypes = json.load(json_file)

    ber_raw = dd.read_csv(
        input_filepath,
        sep="\t",
        low_memory=False,
        dtype=dtypes,
        encoding="latin-1",
        lineterminator="\n",
        error_bad_lines=False,
        quoting=csv.QUOTE_NONE,
    )

    ber_raw.to_parquet(output_filepath, schema="infer")
