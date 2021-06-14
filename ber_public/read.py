import csv
import json

from os import path
from pathlib import Path

import dask.dataframe as dd


HERE = Path(__file__).parent


def read_berpublicsearch_txt(input_dirpath: str) -> dd.DataFrame:
    """Read raw BERPublicsearch txt file.

    Args:
        input_dirpath (str): Path to unzipped BERPublicsearch folder

    Returns:
        dd.DataFrame: BERPublicsearch dataframe
    """
    with open(HERE / "dtypes.json", "r") as json_file:
        dtypes = json.load(json_file)

    return dd.read_csv(
        path.join(input_dirpath, "BERPublicsearch.txt"),
        sep="\t",
        low_memory=False,
        dtype=dtypes,
        encoding="latin-1",
        quoting=csv.QUOTE_NONE,
    )