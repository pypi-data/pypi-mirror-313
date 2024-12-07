"""
This module is used to get completed segments for a live channel.

Functions:
    _get_completed_segments: Gets completed segments for a live channel.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_completed_segments(self, channel_id: str) -> dict | None:
    """
    Gets completed segments for a live channel.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator/{channel_id}/segments"

    return _send_request(self, f"Getting completed segments for Live Channel {channel_id}", api_url, "GET", None, None)
