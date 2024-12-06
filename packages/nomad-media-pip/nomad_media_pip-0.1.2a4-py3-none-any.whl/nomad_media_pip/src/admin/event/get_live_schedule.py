"""
This module contains the logic for getting the live schedule for a specific event.

Functions:
    _get_live_schedule: Gets the live schedule for a specific event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_schedule(self, event_id: str) -> dict | None:
    """
    Gets the live schedule for a specific event.

    Args:
        event_id (str): The ID of the event to get the live schedule for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveSchedule/content/{event_id}"

    return _send_request(self, "Get Live Schedule", api_url, "GET", None, None)
