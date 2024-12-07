"""
This module updates the asset schedule event.

Functions:
    _update_asset_schedule_event: Updates the asset schedule event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES
from nomad_media_pip.src.admin.schedule_event.get_asset_schedule_event import _get_asset_schedule_event


def _update_asset_schedule_event(
    self,
    event_id: str,
    channel_id: str,
    asset: dict | None,
    is_loop: bool | None,
    duration_time_code: str | None
) -> dict | None:
    """
    Updates an asset schedule event.

    Args:
        event_id (str): The ID of the schedule event.
        channel_id (str): The channel ID of the schedule event.
        asset (dict | None): The asset of the schedule event.
            Format: {"id": "string", "name": "string"}
        is_loop (bool | None): Whether the schedule event is loop.
        duration_time_code (str | None): The duration time code of the schedule event.
            Please use the following format: hh:mm:ss;ff. Set to null if IS_LOOP is true.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent"

    schedule_event_info: dict | None = _get_asset_schedule_event(self, channel_id, event_id)

    body: dict = {
        "id": event_id,
        "type": {
            "id": _EVENT_TYPES["videoAsset"],
            "description": "Video Asset"
        }
    }

    body['isLoop'] = (
        is_loop
        if is_loop and is_loop != schedule_event_info['isLoop']
        else schedule_event_info['isLoop']
    )
    body['channelId'] = (
        channel_id
        if channel_id and channel_id != schedule_event_info['channelId']
        else schedule_event_info['channelId']
    )
    body['durationTimeCode'] = (
        duration_time_code
        if duration_time_code and duration_time_code != schedule_event_info['durationTimeCode']
        else schedule_event_info['durationTimeCode']
    )
    body['asset'] = (
        asset
        if asset and asset != schedule_event_info['asset']
        else schedule_event_info['asset']
    )

    return _send_request(self, "Update Asset Schedule Event", api_url, "PUT", None, body)
