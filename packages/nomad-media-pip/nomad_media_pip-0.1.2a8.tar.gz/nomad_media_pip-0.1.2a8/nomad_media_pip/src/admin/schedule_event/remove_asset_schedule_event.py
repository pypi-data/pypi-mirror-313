"""
This module removes an asset schedule event from the service.

Functions:
    _remove_asset_schedule_event: Removes an asset schedule event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _remove_asset_schedule_event(self, channel_id: str, schedule_event_id: str) -> dict | None:
    """
    Removes an asset schedule event.

    Args:
        channel_id (str): The ID of the channel to remove the schedule event from.
        schedule_event_id (str): The ID of the schedule event to remove.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent/{schedule_event_id}"

    return _send_request(self, "Remove Asset Schedule Event", api_url, "DELETE", None, None)
