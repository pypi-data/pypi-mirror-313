"""
This module gets the media builder items from the service API.

Functions:
    _get_media_builder_items: Gets the media builder items.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_media_builder_items(self, media_builder_id: str) -> dict | None:
    """
    Gets the media builder items.

    Args:
        media_builder_id (str): The ID of the media builder.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}/items"

    return _send_request(self, "Get Media Builder Items", api_url, "GET", None, None)
