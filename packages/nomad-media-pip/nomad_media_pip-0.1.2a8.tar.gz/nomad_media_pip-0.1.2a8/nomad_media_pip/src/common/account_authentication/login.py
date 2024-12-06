"""
This module contains the _login function, which logs in to the Nomad service.

Functions:
    _login: Logs in to the Nomad service.

Returns:
    dict: The JSON response from the server if the request is successful.
    None: If the request fails or the response cannot be parsed as JSON.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _login(self) -> dict | None:
    """
    Logs in to the Nomad service.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/login"

    body: dict[str, str] = {
        "username": self.config["username"],
        "password": self.config["password"]
    }

    return _send_request(self, "Login", api_url, "POST", None, body)
