"""
This module starts a live schedule for a specific event.

Functions:
    _start_live_schedule: Starts a live schedule for a specific event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _start_live_schedule(self, event_id: str) -> None:
    """
    Starts a live schedule for a specific event.

    Args:
        event_id (str): The ID of the event to start the live schedule for.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveSchedule/content/{event_id}/start"

    _send_request(self, "Start Live Schedule", api_url, "POST", None, None)
