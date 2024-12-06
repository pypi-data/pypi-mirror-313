"""
This module is used to delete a tag or collection.

Functions:
    _delete_tag_or_collection: Deletes a tag or collection.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_tag_or_collection(self, tag_type: str, tag_id: str) -> dict | None:
    """
    Deletes a tag or collection.

    Args:
        tag_type (str): The type of the tag.
        tag_id (str): The ID of the tag.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/{tag_type}/{tag_id}"

    return _send_request(self, "delete tag or colleciton", api_url, "DELETE", None, None)
