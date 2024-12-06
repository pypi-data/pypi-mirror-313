"""
This module is responsible for uploading a part of an asset to the Nomad API.

Functions:
    _upload_asset_part: Uploads a part of an asset to the Nomad API.
"""

import logging
import time
from io import BufferedReader
import requests

from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

MAX_RETRIES = 5
TIMEOUT = 30
TIME_SLEEP = 60


def _upload_asset_part(file: str, part: dict, debug: bool) -> str | None:
    """
    Uploads a part of an asset to the Nomad API.

    Args:
        file (str): The file to upload.
        part (dict): The part to upload.
        debug (bool): Whether to log debug messages.

    Returns:
        str: The ETag of the part if the request is successful.
        None: If the request fails.
    """

    try:
        open_file: BufferedReader = open(file, "rb")
        open_file.seek(part["startingPosition"])
        body: bytes = open_file.read(
            part["endingPosition"] + 1 - part["startingPosition"])
        open_file.close()

    except OSError as error:
        logging.error("Error reading file: %s", error)

    retries = 0
    response = None
    while retries < MAX_RETRIES:
        try:
            header: dict[str, str] = {
                "Accept": "application/json, text/plain, */*"
            }

            if debug:
                logging.debug("URL: %s,\nMETHOD: PUT,\n", part["url"])

            response: requests.Response = requests.put(
                part["url"], headers=header, data=body, timeout=TIMEOUT
            )

            if response.ok:
                break

            response.raise_for_status()

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if retries < MAX_RETRIES:
                retries += 1
                time.sleep(TIME_SLEEP)
            else:
                _api_exception_handler(response, "Upload part failed")

        except requests.exceptions.RequestException:
            return _api_exception_handler(response, f"Upload part failed: {response.status_code}")

    return response.headers.get("ETag")
