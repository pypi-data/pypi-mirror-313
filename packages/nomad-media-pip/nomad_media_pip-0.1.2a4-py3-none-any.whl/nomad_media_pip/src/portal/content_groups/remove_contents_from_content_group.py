"""
This module contains the function to remove contents from content group.

Functions:
    _remove_contents_from_content_group: Removes contents from content group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _remove_contents_from_content_group(self, content_group_id: str, contents: dict) -> dict | None:
    """
    Removes contents from content group.

    Args:
        content_group_id (str): The ID of the content group to remove content from.
        contents (dict): The content to remove from the content group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup/remove/{content_group_id}"

    body: dict = contents

    return _send_request(self, "Remove content to content group", api_url, "POST", None, body)
