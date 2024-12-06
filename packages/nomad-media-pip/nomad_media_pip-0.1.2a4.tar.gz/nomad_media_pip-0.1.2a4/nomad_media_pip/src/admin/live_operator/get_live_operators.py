"""
This module gets the live operators from the service API.

Functions:
    _get_live_operators: Gets the live operators.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_operators(self) -> dict | None:
    """
    Gets the live operators.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator"

    return _send_request(self, "Getting Live Operators", api_url, "GET", None, None)
