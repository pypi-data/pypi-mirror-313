"""
This module is used to delete a content group.

Functions:
    _delete_content_group: Deletes a content group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_content_group(self, content_group_id: str) -> dict | None:
    """
    Deletes a content group.

    Args:
        content_group_id (str): The ID of the content group to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup/{content_group_id}"

    return _send_request(self, "Delete content group", api_url, "DELETE", None, None)
