"""
This module updates the input schedule event.

Functions:
    _update_input_schedule_event: Updates the input schedule event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.get_input_schedule_event import _get_input_schedule_event
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES


def _update_input_schedule_event(
    self,
    event_id: str,
    channel_id: str,
    live_input: dict | None,
    backup_input: dict | None,
    fixed_on_air_time_utc: str | None
) -> dict | None:
    """
    Updates an input schedule event.

    Args:
        event_id (str): The ID of the Input schedule event.
        channel_id (str): The channel ID of the schedule event.
        input (dict | None): The input of the schedule event.
            Format: {"id": "string", "name": "string"}
        backup_input (dict | None): The backup input of the schedule event.
            Format: {"id": "string", "name": "string"}
        fixed_on_air_time_utc (str | None): The fixed on air time UTC of the schedule event.
            Please use the following format: hh:mm:ss.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent"

    schedule_event_info: dict = _get_input_schedule_event(self, channel_id, event_id)

    body: dict = {
        "id": event_id,
        "channelId": channel_id,
        "liveInput": live_input or schedule_event_info.get('input'),
        "liveInput2": backup_input or schedule_event_info.get('backupInput'),
        "fixedOnAirTimeUTC": fixed_on_air_time_utc or schedule_event_info.get('fixedOnAirTimeUTC'),
        "type": {
            "id": _EVENT_TYPES["liveInput"],
            "description": "Live Input"
        }
    }

    return _send_request(self, "Update Input Schedule Event", api_url, "PUT", None, body)
