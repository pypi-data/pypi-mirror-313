"""
This module stops a live channel.

Functions:
    _stop_live_channel: Stops a live channel.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_channel.live_channel_statuses import _LIVE_CHANNEL_STATUSES
from nomad_media_pip.src.admin.live_channel.wait_for_live_channel_status import _wait_for_live_channel_status

MAX_RETRIES = 2


def _stop_live_channel(self, channel_id: str, wait_for_stop: bool | None) -> None:
    """
    Stops a live channel.

    Args:
        CHANNEL_ID (str): The ID of the live channel to stop.
        WAIT_FOR_STOP (bool | None): Whether to wait for the live channel to stop.

    Returns:
        None
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/stop"

    _send_request(self, "Stop Live Channel", api_url, "POST", None, None)
    if wait_for_stop:
        _wait_for_live_channel_status(self, channel_id, _LIVE_CHANNEL_STATUSES["Idle"], 720, 2)
