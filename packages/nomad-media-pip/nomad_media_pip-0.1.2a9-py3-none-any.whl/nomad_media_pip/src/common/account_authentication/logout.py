"""
This module contains the function to logout a user from the Nomad Media service.

Functions:
    _logout: Logs out a user from the Nomad Media service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _logout(self) -> None:
    """
    Logs out a user from the Nomad Media service.

    Args:
        USER_SESSION_ID (str): The ID of the user session to log out.

    Returns:
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/logout"

    body: dict = {
        "userSessionId": self.user_session_id,
    }

    return _send_request(self, "Logout", api_url, "POST", None, body)
