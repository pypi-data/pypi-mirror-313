"""
This module is used to get a content group.

Functions:
    _get_content_group: Gets a content group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_group(self, content_group_id: str) -> dict | None:
    """
    Gets a content group.

    Args:
        content_group_id (str): The ID of the content group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup/{content_group_id}"

    return _send_request(self, "Get content group", api_url, "GET", None, None)
