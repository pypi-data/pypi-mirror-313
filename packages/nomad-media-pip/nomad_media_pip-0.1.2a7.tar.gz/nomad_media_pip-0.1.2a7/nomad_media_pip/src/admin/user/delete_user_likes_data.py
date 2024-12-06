"""
This module deletes the user likes data from the service.

Functions:
    _delete_user_likes_data: Deletes the user likes data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_likes_data(self, user_id: str | None) -> None:
    """
    Deletes the user likes data.

    Args:
        user_id (str | None): The ID of the user to delete the likes data for.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/like/{user_id}"

    _send_request(self, "Delete User Likes Data", api_url, "DELETE", None, None)
