"""
This module is used to refresh live channels.

Functions:
    _live_channel_refresh: Refreshes live channels.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _live_channel_refresh(self) -> dict | None:
    """
    Refreshes live channels.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/refresh"

    return _send_request(self, "Live Channel Refresh", api_url, "POST", None, None)
