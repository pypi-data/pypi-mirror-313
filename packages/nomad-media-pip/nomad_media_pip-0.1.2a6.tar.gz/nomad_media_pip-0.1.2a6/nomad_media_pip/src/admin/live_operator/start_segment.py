"""
This module starts a segment for a live operator.

Functions:
    _start_segment: Starts a segment for a live operator.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _start_segment(self, channel_id) -> dict | None:
    """
    Starts a segment for a live operator.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator/{channel_id}/startSegment"

    return _send_request(self, "Start Segment", api_url, "POST", None, None)
