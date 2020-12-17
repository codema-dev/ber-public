import json

from os import path
from pathlib import Path
from typing import Any

import requests

from tqdm import tqdm


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


def download_berpublicsearch(email_address: str, filepath: str) -> None:
    """Login & Download BER data.

    Warning:
        Email address must first be registered with SEAI at
            https://ndber.seai.ie/BERResearchTool/Register/Register.aspx

    Args:
        email_address (str): Registered Email address with SEAI
        filepath (str): Save path for data
    """
    with open(HERE / "request.json", "r") as json_file:
        ber_form_data = json.load(json_file)

    # Register login email address
    ber_form_data["login"][
        "ctl00$DefaultContent$Register$dfRegister$Name"
    ] = email_address

    with requests.Session() as session:

        # Login to BER Research Tool using email address
        session.post(
            url="https://ndber.seai.ie/BERResearchTool/Register/Register.aspx",
            headers=ber_form_data["headers"],
            data=ber_form_data["login"],
        )

        # Download Ber data via a post request
        with session.post(
            url="https://ndber.seai.ie/BERResearchTool/ber/search.aspx",
            headers=ber_form_data["headers"],
            data=ber_form_data["download_all_data"],
            stream=True,
        ) as response:

            response.raise_for_status()
            download_file_from_response(response, filepath)
