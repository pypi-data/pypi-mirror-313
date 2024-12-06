"""
This module deletes the user from the service.

Functions:
    _delete_user: Deletes the user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user(self, user_id: str) -> None:
    """
    Deletes the user.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/{user_id}"

    _send_request(self, "Delete User", api_url, "DELETE", None, None)
