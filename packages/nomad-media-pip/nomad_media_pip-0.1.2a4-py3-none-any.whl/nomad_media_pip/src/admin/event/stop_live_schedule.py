"""
This module contains the function to stop a live schedule.

Functions:
    _stop_live_schedule: Stops a live schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _stop_live_schedule(self, event_id: str) -> None:
    """
    Stops a live schedule.

    Args:
        event_id (str): The ID of the event to stop the live schedule for.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveSchedule/content/{event_id}/stop"

    _send_request(self, "Stop Live Schedule", api_url, "POST", None, None)
