"""
This module contains the function to send a request to the service to reset the user's password.

Functions:
    _forgot_password: Sends a request to the service to reset the user's password.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _forgot_password(self) -> None:
    """
    Sends a request to the service to reset the user's password.

    Returns:
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/forgot-password"

    body: dict = {
        "username": self.config["username"]
    }

    _send_request(self, "Forgot Password", api_url, "POST", None, body)
