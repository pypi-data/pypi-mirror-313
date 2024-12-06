"""
This module adds an asset schedule event to the service.

Functions:
    _add_asset_schedule_event: Adds an asset schedule event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES


def _add_asset_schedule_event(
    self,
    channel_id: str,
    asset: dict,
    is_loop: bool,
    duration_time_code: str | None,
    previous_id: str | None
) -> dict | None:
    """
    Adds an asset schedule event.

    Args:
        channel_id (str): The ID of the channel to add the event to.
        asset (dict): The asset to add to the event.
        is_loop (bool): The loop flag of the event.
        duration_time_code (str | None): The duration time code of the event.
            Please use the following format: hh:mm:ss;ff.
        previous_id (str | None): The ID of the previous event.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent"

    # Build the payload BODY
    body: dict = {
        "isLoop": is_loop,
        "channelId": channel_id,
        "durationTimeCode": duration_time_code,
        "previousId": previous_id,
        "type": {
            "id": _EVENT_TYPES["videoAsset"],
            "description": "Video-Asset"
        },
        "asset": asset,
    }

    return _send_request(self, "Add Asset Schedule Event", api_url, "POST", None, body)
