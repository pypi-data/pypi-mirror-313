"""
This module gets the media group from the service API.

Functions:
    _get_media_group: Gets the media group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_media_group(self, media_group_id: str) -> dict | None:
    """
    Gets the media group.

    Args:
        media_group_id (str): The ID of the media group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/group/{media_group_id}"

    return _send_request(self, "Get Media Group", api_url, "GET", None, None)
