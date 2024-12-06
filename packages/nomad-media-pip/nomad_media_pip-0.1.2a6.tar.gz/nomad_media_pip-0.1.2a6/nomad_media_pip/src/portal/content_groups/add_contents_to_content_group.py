"""
This module contains the function to add contents to content group.

Functions:
    _add_contents_to_content_group: Adds contents to content group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _add_contents_to_content_group(self, content_group_id: str, contents: dict) -> dict | None:
    """
    Adds contents to content group.

    Args:
        content_group_id (str): The ID of the content group to add contents to.
        contents (dict): The contents to add to the content group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup/add/{content_group_id}"

    body: dict = contents

    return _send_request(self, "Add content to content group", api_url, "POST", None, body)
