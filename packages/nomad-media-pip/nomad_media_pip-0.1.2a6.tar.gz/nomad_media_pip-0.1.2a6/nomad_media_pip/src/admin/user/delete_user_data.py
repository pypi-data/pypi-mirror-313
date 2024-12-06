"""
This module deletes the user data from the service API.

Functions:
    _delete_user_data: Deletes the user data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_data(self, user_id: str | None) -> None:
    """
    Deletes the user data.

    Args:
        user_id (str): The ID of the user to delete the data for.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/userData/{user_id}"

    _send_request(self, "Delete User Data", api_url, "DELETE", None, None)
