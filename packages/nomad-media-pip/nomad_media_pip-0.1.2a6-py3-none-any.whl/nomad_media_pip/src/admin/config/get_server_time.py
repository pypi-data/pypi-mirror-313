"""
Get the server time from the service API.

Functions:
    _get_server_time: Gets the server time from the service API.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_server_time(self) -> dict | None:
    """
    Gets the server time from the service API.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/config/serverTime"

    return _send_request(self, "Get server time", api_url, "GET", None, None)
