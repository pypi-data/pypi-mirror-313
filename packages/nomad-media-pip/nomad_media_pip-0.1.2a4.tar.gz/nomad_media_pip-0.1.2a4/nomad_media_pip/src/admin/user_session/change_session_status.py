"""
This module is used to change the session status of a user.

Functions:
    _change_session_status: Changes the session status of a user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _change_session_status(
    self,
    user_id: str | None,
    user_session_status: str,
    application_id: str | None
) -> dict | None:
    """
    Changes the session status of a user.

    Args:
        user_id (str | None): The ID of the user to change the session status for.
        user_session_status (str): The new session status of the user.
        application_id (str | None): The ID of the application to change the session status for.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user-session"

    body: dict = {
        "id": user_id,
        "userSessionStatus": user_session_status,
        "applicationId": application_id
    }

    return _send_request(self, "Change Session Status", api_url, "POST", None, body)
