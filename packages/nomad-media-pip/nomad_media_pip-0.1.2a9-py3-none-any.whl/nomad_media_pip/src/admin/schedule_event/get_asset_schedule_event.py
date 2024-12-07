"""
This module gets the asset schedule event from the service API.

Functions:
    _get_asset_schedule_event: Gets the asset schedule event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_schedule_event(self, channel_id: str, schedule_event_id: str) -> dict | None:
    """
    Gets the asset schedule event.

    Args:
        channel_id (str): The ID of the channel to get the asset schedule event for.
        schedule_event_id (str): The ID of the asset schedule event to get.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent/{schedule_event_id}"

    return _send_request(self, "Get Asset Schedule Event", api_url, "GET", None, None)
