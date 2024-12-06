"""
This module gets the live channel schedule events from the service API.

Functions:
    _get_live_channel_schedule_events: Gets the live channel schedule events.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_channel_schedule_events(self, channel_id: str) -> dict | None:
    """
    Gets the live channel schedule events.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent"

    return _send_request(self, "Get Live Channel Schedule Events", api_url, "GET", None, None)
