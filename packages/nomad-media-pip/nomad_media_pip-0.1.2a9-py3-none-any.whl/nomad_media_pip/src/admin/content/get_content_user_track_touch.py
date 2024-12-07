"""
This module contains the _get_content_user_track_touch function, which gets the user track touch
for a content.

Functions:
    _get_content_user_track_touch: Gets the user track touch for a content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_user_track_touch(self, content_id, content_definition_id) -> dict | None:
    """
    Gets the user track touch for a content.

    Args:
        content_id (str): The ID of the content.
        content_definition_id (str): The ID of the content definition.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/content/{content_definition_id}/user-track/{content_id}/touch"

    return _send_request(self, "Get content user track touch", api_url, "GET", None, None)
