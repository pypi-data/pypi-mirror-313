"""
This module gets the media item from the service API.

Functions:
    _get_media_item: Gets the media item.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_media_item(self, media_item_id: str) -> dict | None:
    """
    Gets the media item.

    Args:
        media_item_id (str): The ID of the media item.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/item/{media_item_id}"

    return _send_request(self, "Get Media Item", api_url, "GET", None, None)
