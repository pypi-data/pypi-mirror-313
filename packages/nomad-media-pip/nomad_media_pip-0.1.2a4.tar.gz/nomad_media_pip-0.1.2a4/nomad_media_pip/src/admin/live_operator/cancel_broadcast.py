"""
This module cancels the broadcast on the service API.

Functions:
    _cancel_broadcast: Cancels the broadcast.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _cancel_broadcast(self, channel_id: str) -> dict | None:
    """
    Cancels the broadcast.

    Args:
        channel_id (str): The ID of the channel to cancel the broadcast.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator/{channel_id}/cancel"

    return _send_request(self, "Cancel Broadcast", api_url, "POST", None, None)
