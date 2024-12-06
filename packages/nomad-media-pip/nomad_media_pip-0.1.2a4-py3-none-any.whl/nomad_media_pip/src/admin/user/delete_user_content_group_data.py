"""
This module deletes the user content group data from the service API.

Functions:
    _delete_user_content_group_data: Deletes the user content group data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_content_group_data(self, user_id: str | None) -> None:
    """
    Deletes the user content group data.

    Args:
        user_id (str | None): The user ID of the user's content group data.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/contentGroup/{user_id}"

    _send_request(self, "Delete User Content Group Data", api_url, "DELETE", None, None)
