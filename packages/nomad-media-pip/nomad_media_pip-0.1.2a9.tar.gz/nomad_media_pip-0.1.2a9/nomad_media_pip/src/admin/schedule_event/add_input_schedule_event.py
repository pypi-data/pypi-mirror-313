"""
This module adds an input schedule event.

Functions:
    _add_input_schedule_event: Adds an input schedule event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES


def _add_input_schedule_event(
    self,
    channel_id: str,
    live_input: dict,
    backup_input: dict | None,
    fixed_on_air_time_utc: str | None,
    previous_id: str | None
) -> dict | None:
    """
    Adds an input schedule event.

    Args:
        channel_id (str): The ID of the channel to add the event to.
        live_input (dict): The live input to add to the event.
        backup_input (dict | None): The backup input to add to the event.
        fixed_on_air_time_utc (str | None): The on air time of the event.
        previous_id (str | None): The ID of the previous event.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent"

    # Build the payload BODY
    body: dict = {
        "channelId": channel_id,
        "fixedOnAirTimeUtc": fixed_on_air_time_utc,
        "type": {
            "id": _EVENT_TYPES["liveInput"],
            "description": "Live Input"
        },
        "liveInput": live_input,
        "liveInput2": backup_input,
        "previousId": previous_id
    }

    return _send_request(self, "Add Input Schedule Event", api_url, "POST", None, body)
