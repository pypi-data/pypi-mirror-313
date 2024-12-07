"""
This module contains the logic to deletes a user's shared data..

Functions:
    _delete_user_share_data: deletes a user's shared data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_share_data(self, user_id: str) -> None:
    """
    Deletes a user's shared data.

    Args:
        user_id (str | None): The user ID of the user's share data.
        If set to null, the user ID of the current user is used

    Returns:
        Unknown Type: If the request succeeds.

    Exceptions:
        InvalidAPITypeException: If the API type is not admin.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/shares/${user_id}"

    return _send_request(self, "Delete User Share Data", api_url, "DELETE", None, None)
