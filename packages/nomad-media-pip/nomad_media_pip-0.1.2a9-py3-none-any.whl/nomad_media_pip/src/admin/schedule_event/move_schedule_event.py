"""
This module moves a schedule event to a new position in the schedule.

Functions:
    _move_schedule_event: Moves a schedule event to a new position in the schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _move_schedule_event(
    self,
    channel_id: str,
    schedule_event_id: str,
    previous_schedule_event_id: str | None
) -> dict | None:
    """
    Moves a schedule event to a new position in the schedule.

    Args:
        channel_id (str): The ID of the channel to move the schedule event in.
        schedule_event_id (str): The ID of the schedule event to move.
        previous_schedule_event_id (str | None): The ID of the schedule event that the moved schedule event should be placed after.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/"
        f"liveScheduleEvent/{schedule_event_id}/move"
    )

    body: dict = {
        "previousScheduleEventId": previous_schedule_event_id
    }

    return _send_request(self, "Move Schedule Event", api_url, "PUT", None, body)
