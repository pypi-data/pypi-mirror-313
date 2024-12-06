"""
This module is used to stop a broadcast.

Functions:
    _stop_broadcast: Stops a broadcast.
"""

from nomad_media_pip.src.admin.live_operator.wait_for_live_operator_status import _wait_for_live_operator_status
from nomad_media_pip.src.helpers.send_request import _send_request


def _stop_broadcast(self, channel_id: str) -> dict | None:
    """
    Stops a broadcast.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator/{channel_id}/stop"

    info: dict | None = _send_request(self, "Stop Boadcast", api_url, "POST", None, None)
    _wait_for_live_operator_status(self, channel_id, "Idle", 1200, 20)
    return info
