"""
This module contains the function to reset password.

Functions:
    _reset_password: Resets password.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _reset_password(self, code: str, new_password: str) -> None:
    """
    Resets password.

    Args:
        code (str): The code to reset the password.
        new_password (str): The new password.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/reset-password"

    body: dict = {
        "username": self.config["username"],
        "token": code,
        "newPassword": new_password
    }

    _send_request(self, "Reset Password", api_url, "POST", None, body)
