"""
This module is used to create a tag or collection.

Functions:
    _create_tag_or_collection: Creates a tag or collection.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_tag_or_collection(self, tag_type: str, tag_name: str) -> dict | None:
    """
    Creates a tag or collection.

    Args:
        tag_type (str): Whether to create a tag or collection.
        tag_name (str): The name of the tag or collection.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/{tag_type}"

    body: dict = {
        "name": tag_name
    }

    return _send_request(self, "Create Tag or Collection", api_url, "POST", None, body)
