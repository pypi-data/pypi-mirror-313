"""
This module contains the function to start output tracking.

Functions:
    _start_output_tracking: Starts output tracking.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _start_output_tracking(self, live_channel_id: str) -> dict | None:
    """
    Starts output tracking.

    Args:
        live_channel_id (str): The ID of the live channel to start output tracking.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{live_channel_id}/startOutputTracking"

    return _send_request(self, "Start Output Tracking", api_url, "POST", None, None)
