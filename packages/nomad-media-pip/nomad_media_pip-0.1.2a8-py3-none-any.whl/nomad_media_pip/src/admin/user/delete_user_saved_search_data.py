"""
This module deletes the user saved search data from the service API.

Functions:
    _delete_user_saved_search_data: Deletes the user saved search data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_saved_search_data(self, user_id: str | None) -> None:
    """
    Deletes the user saved search data.

    Args:
        user_id (str | None): The ID of the user to delete the saved search data for.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/savedSearch/{user_id}"

    _send_request(self, "Delete User Saved Search Data", api_url, "DELETE", None, None)
