"""
This module contains the function to create a content group.

Functions:
    _create_content_group: Creates a content group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_content_group(self, content_group_name: str) -> dict | None:
    """
    Creates a content group.

    Args:
        content_group_name (str): The name of the content group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup"

    body: dict = {
        "name": content_group_name
    }

    return _send_request(self, "Create content groups", api_url, "POST", None, body)
