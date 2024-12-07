"""
This module deletes the user content attribute data from the service API.

Functions:
    _delete_user_content_attribute_data: Deletes the user content attribute data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_content_attribute_data(self, user_id: str | None) -> None:
    """
    Deletes the user content attribute data.

    Args:
        user_id (str | None): The user ID of the user's content attribute data.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/userContentAttribute/{user_id}"

    _send_request(self, "Delete User Content Attribute Data", api_url, "DELETE", None, None)
