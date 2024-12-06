"""
This module is used to get a tag or collection.

Functions:
    _get_tag_or_collection: Gets a tag or collection.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_tag_or_collection(self, tag_type, tag_id) -> dict | None:
    """
    Gets a tag or collection.

    Args:
        tag_type (str): The type of the tag.
        tag_id (str): The ID of the tag.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/{tag_type}/{tag_id}"

    return _send_request(self, "Get Tag or Collection", api_url, "GET", None, None)
