"""
This module changes the email of the account in the service API.

Functions:
    _change_email: Changes the email of the account.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _change_email(self, new_email: str) -> dict | None:
    """
    Changes the email of the account.

    Args:
        new_email (str): The new email address for the account.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/change-email"

    body: dict = {
        "password": self.config["password"],
        "newEmail": new_email
    }

    return _send_request(self, "Change email", api_url, "POST", None, body)
