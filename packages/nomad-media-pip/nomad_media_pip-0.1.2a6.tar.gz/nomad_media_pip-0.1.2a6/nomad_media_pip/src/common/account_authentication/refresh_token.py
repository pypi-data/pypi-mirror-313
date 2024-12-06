"""
This module is used to refresh the token. It is called when the token is expired.

Functions:
    _refresh_token: Refreshes the token.
"""

from datetime import datetime
import logging

from nomad_media_pip.src.helpers.send_request import _send_request


def _refresh_token(self) -> bool:
    """
    Refreshes the token.

    Args:
        refresh_token (str): The refresh token.

    Returns:
        bool: True if the token is refreshed successfully.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/refresh-token"

    body: dict[str, str] = {
        "refreshToken": self.refresh_token_val
    }

    logging.info("%s Refreshing Token", datetime.now().strftime('%H:%M:%S'))

    token_info: dict | None = _send_request(self, "Refresh Token", api_url, "POST", None, body)

    if token_info and "token" in token_info:
        self.token = token_info["token"]
        return True

    return False
