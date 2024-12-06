"""
This module contains the function to change the password of the user.

Functions:
    _change_password: Changes the password of the user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _change_password(self, new_password) -> dict | None:
    """
    Changes the password of the user.

    Args:
        new_password (str): The new password for the user.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/change-password"

    body: dict = {
        "password": self.config["password"],
        "newPassword": new_password
    }

    return _send_request(self, "Change password", api_url, "POST", None, body)
