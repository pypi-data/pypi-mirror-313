"""
This module is used to share content group with user.

Functions:
    _share_content_group_with_user: Shares content group with user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _share_content_group_with_user(self, content_group_id: str, user_ids: list[str]) -> dict | None:
    """
    Shares a content group with users. To share a content group with a user, the
    user must meet certain requirements. They must not be a guest user and their account must be
    in a normal state. Only the owner, the user who created the content group, can share the
    content group. The user the content group is being shared with cannot change the collection.

    Args:
        content_group_id (str): The ID of the content group to share.
        user_ids (list[str]): The IDs of the users to share the content group with.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup/share/{content_group_id}"

    body: list = user_ids

    return _send_request(self, "Share content group with user", api_url, "POST", None, body)
