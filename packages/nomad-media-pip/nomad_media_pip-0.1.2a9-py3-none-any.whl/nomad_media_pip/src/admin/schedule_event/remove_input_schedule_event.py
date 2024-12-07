"""
This module removes an input schedule event from a channel.

Functions:
    _remove_input_schedule_event: Removes an input schedule event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _remove_input_schedule_event(self, channel_id: str, input_id: str) -> dict | None:
    """
    Removes an input schedule event.

    Args:
        channel_id (str): The ID of the channel to remove the input schedule event from.
        input_id (str): The ID of the input schedule event to remove.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/liveScheduleEvent/{input_id}"

    return _send_request(self, "Remove Input Schedule Event", api_url, "DELETE", None, None)
