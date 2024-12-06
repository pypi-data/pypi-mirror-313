"""
This module is responsible for verifying the user's email address.

Functions:
    _verify: Verifies the user's email address.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _verify(self, email: str, code: str) -> dict | None:
    """
    Verifies the user's email address.

    Args:
        email (str): The email of the user to verify.
        code (str): The code to verify the email.

    Returns:
        dict | None: The response from the service if the request succeeds, None otherwise.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/verify"

    body: dict = {
        "userName": email,
        "token": code
    }

    return _send_request(self, "Verification", api_url, "POST", None, body)
