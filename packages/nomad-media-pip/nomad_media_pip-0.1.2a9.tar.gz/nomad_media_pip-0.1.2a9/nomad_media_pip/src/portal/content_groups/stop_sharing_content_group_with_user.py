"""
This module is used to stop sharing a content group with a user.

Functions:
    _stop_sharing_content_group_with_user: Stops sharing a content group with a user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _stop_sharing_content_group_with_user(self, content_group_id: str, user_ids: list[str]) -> dict | None:
    """
    Stops sharing a content group with a user.

    Args:
        content_group_id (str): The ID of the content group to stop sharing.
        user_ids (list[str]): The IDs of the users to stop sharing the content group with.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup/stopshare/{content_group_id}"

    body: list = user_ids

    return _send_request(self, "Share collection to user", api_url, "POST", None, body)
