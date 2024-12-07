
"""
This module is responsible for resending the code to the user's email.

Functions:
    _resend_code: Resends the code to the user's email.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _resend_code(self, email: str) -> None:
    """
    Resends the verification email.

    Args:
        email (str): The email of the user to resend the code.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/resend-code"

    body: dict = {
        "userName": email
    }

    _send_request(self, "Resend code", api_url, "POST", None, body)
