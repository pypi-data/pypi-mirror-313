"""
This module deletes the user favorites data from the service API.

Functions:
    _delete_user_favorites_data: Deletes the user favorites data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_favorites_data(self, user_id: str | None) -> None:
    """
    Deletes the user favorites data.

    Args:
        user_id (str | None): The ID of the user to delete the favorites data for.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/favorite/{user_id}"

    _send_request(self, "Delete User Favorites Data", api_url, "DELETE", None, None)
