"""
This module contains the _send_request function, which sends an HTTP request and
handles retries and token refresh.

Functions:
    _send_request: Sends an HTTP request and handles retries and token refresh.
"""

import time
import json
import logging
import requests

from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

MAX_RETRIES: int = 5
TIMEOUT: int = 30
SLEEP_TIME: float = 0.5


def _send_request(
    self,
    function_name: str,
    url: str,
    method_type: str,
    params: dict | None,
    body: dict | None
) -> dict | None:
    """
    Sends an HTTP request and handles retries and token refresh.

    Args:
        function_name (str): The name of the function making the request.
        url (str): The URL to which the request is sent.
        method_type (str): The HTTP method type (e.g., 'GET', 'POST').
        params (dict): The query parameters to be included in the request.
        body (dict): The JSON body to be included in the request.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.

    Raises:

    """

    headers: dict[str, str] = {
        "Content-Type": "application/json"
    }

    if self.token:
        headers["Authorization"] = f"Bearer {self.token}"

    if self.debug and function_name != "Login":
        logging.debug(
            f"URL: {url}\nMETHOD: {method_type}" +
            (f"\nparams: {json.dumps(params, indent=4)}" if params else "") +
            (f"\nBODY: {json.dumps(body, indent=4)}" if body else "")
        )

    retries = 0
    response = None
    refreshed_token = False
    while retries < MAX_RETRIES:
        try:
            response: requests.Response | None = (
                requests.request(
                    method_type,
                    url,
                    headers=headers,
                    params=params if params else None,
                    data=json.dumps(body) if body else None,
                    timeout=TIMEOUT
                )
            )

            if response.ok:
                try:
                    return response.json()
                except ValueError:
                    return None

            if response.status_code == 403 and function_name != "Refresh Token" and not refreshed_token:
                self.refresh_token()
                headers["Authorization"] = f"Bearer {self.token}"
                refreshed_token = True
            else:
                response.raise_for_status()

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if retries + 1 == MAX_RETRIES:
                return _api_exception_handler(response, f"{function_name} failed: {response.status_code}")

            time.sleep(SLEEP_TIME * 2 ** (retries + 1))

        except requests.exceptions.RequestException:
            return _api_exception_handler(response, f"{function_name} failed: {response.status_code}")

        finally:
            retries += 1

    return None
