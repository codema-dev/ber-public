import json
from os import path
from os import mkdir
from pathlib import Path
from shutil import unpack_archive
from typing import Any

import requests
from requests import HTTPError
from tqdm import tqdm

from berpublicsearch.convert import convert_to_parquet


HERE = Path(__file__).parent


def download_file_from_response(response: requests.Response, filepath: str) -> None:
    """Download file to filepath via a HTTP response from a POST or GET request.

    Args:
        response (requests.Response): A HTTP response from a POST or GET request
        filepath (str): Save path destination for downloaded file
    """
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kilobyte
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    with open(filepath, "wb") as save_destination:

        for stream_data in response.iter_content(block_size):
            progress_bar.update(len(stream_data))
            save_destination.write(stream_data)

    progress_bar.close()


def download_berpublicsearch(email_address: str, savedir: str = Path.cwd()) -> None:
    """Login & Download BER data.

    Args:
        email_address (str): Registered Email address with SEAI
        savedir (str): Save directory for data
    """
    savepath = path.join(savedir, "BERPublicsearch.zip")

    with open(HERE / "request.json", "r") as json_file:
        ber_form_data = json.load(json_file)

    # Register login email address
    ber_form_data["login"][
        "ctl00$DefaultContent$Register$dfRegister$Name"
    ] = email_address

    with requests.Session() as session:

        # Login to BER Research Tool using email address
        response = session.post(
            url="https://ndber.seai.ie/BERResearchTool/Register/Register.aspx",
            headers=ber_form_data["headers"],
            data=ber_form_data["login"],
        )

        response.raise_for_status()
        if "not registered" in str(response.content):
            raise ValueError(
                f"{email_address} does not have access to the BER Public"
                f" search database, please login to {email_address} and"
                " respond to your registration email and try again."
            )

        # Download Ber data via a post request
        with session.post(
            url="https://ndber.seai.ie/BERResearchTool/ber/search.aspx",
            headers=ber_form_data["headers"],
            data=ber_form_data["download_all_data"],
            stream=True,
        ) as response:

            response.raise_for_status()
            download_file_from_response(response, savepath)


def download_berpublicsearch_parquet(
    email_address: str,
    savedir: str = Path.cwd(),
) -> None:
    """Login, download, unzip & convert BER data to parquet.

    Args:
        email_address (str): Registered Email address with SEAI
        savedir (str): Save directory for data
    """
    print("Download BERPublicsearch.zip...")
    download_berpublicsearch(email_address, savedir)

    path_to_zipped = path.join(savedir, "BERPublicsearch.zip")
    print(f"Unzipping {path_to_zipped}...")
    path_to_unzipped = path.join(savedir, "BERPublicsearch")
    unpack_archive(path_to_zipped, path_to_unzipped)

    print("Converting BERPublicsearch to BERPublicsearch_parquet...")
    path_to_parquet = path.join(savedir, "BERPublicsearch_parquet")
    convert_to_parquet(path_to_unzipped, path_to_parquet)