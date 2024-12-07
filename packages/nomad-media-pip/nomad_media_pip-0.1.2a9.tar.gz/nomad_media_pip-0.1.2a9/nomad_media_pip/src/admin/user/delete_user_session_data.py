"""
This module deletes the user session data from the service.

Functions:
    _delete_user_session_data: Deletes the user session data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_session_data(self, user_id: str | None) -> None:
    """
    Deletes the user session data.

    Args:
        user_id (str | None): The ID of the user to delete the session data for.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/userSession/{user_id}"

    _send_request(self, "Delete User Session Data", api_url, "DELETE", None, None)
