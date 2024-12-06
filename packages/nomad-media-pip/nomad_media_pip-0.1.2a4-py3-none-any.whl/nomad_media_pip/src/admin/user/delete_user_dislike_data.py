"""
This module deletes the user dislike data from the service API.

Functions:
    _delete_user_dislike_data: Deletes the user dislike data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_dislike_data(self, user_id: str | None) -> None:
    """
    Deletes the user dislike data.

    Args:
        user_id (str | None): The ID of the user to delete the dislike data for.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/dislike/{user_id}"

    _send_request(self, "Delete User Dislike Data", api_url, "DELETE", None, None)
