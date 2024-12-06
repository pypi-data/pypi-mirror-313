"""
This module gets the next event of a live channel from the service API.

Functions:
    _next_event: Gets the next event of a live channel.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _next_event(self, channel_id: str) -> dict | None:
    """
    Gets the next event of a live channel.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/nextEvent"

    return _send_request(self, "Get Next Event", api_url, "GET", None, None)
