"""
This module contains the function to get a live channel by its ID.

Functions:
    _get_live_channel: Gets a live channel by its ID.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_channel(self, channel_id: str) -> dict | None:
    """
    Gets a live channel by its ID.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}"

    return _send_request(self, "Get Live Channel", api_url, "GET", None, None)
