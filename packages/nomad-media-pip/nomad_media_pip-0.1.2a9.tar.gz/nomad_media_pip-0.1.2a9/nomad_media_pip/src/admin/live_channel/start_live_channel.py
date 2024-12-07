"""
This module contains the function to start a live channel.

Functions:
    _start_live_channel: Starts a live channel.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_channel.live_channel_statuses import _LIVE_CHANNEL_STATUSES
from nomad_media_pip.src.admin.live_channel.get_live_channel_status import _get_live_channel_status
from nomad_media_pip.src.admin.live_channel.wait_for_live_channel_status import _wait_for_live_channel_status


def _start_live_channel(self, channel_id: str, wait_for_start: bool | None) -> None:
    """
    Starts a live channel.

    Args:
        channel_id (str): The ID of the live channel to start.
        wait_for_start (bool | None): Whether to wait for the live channel to start.

    Returns:
        None
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}/start"

    _send_request(self, "Start Live Channel", api_url, "POST", None, None)

    if wait_for_start:
        live_channel_info: str = _get_live_channel_status(self, channel_id)
        if live_channel_info == _LIVE_CHANNEL_STATUSES["Idle"]:
            return None

        _wait_for_live_channel_status(self, channel_id, _LIVE_CHANNEL_STATUSES["Running"], 1200, 20)
