"""
This module contains the function to get user.

Functions:
    _get_user: Gets user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_user(self) -> dict | None:
    """
    Gets user.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/user"

    return _send_request(self, "Get user", api_url, "GET", None, None)
