"""
This module is used to get all live channels.

Functions:
    _get_live_channels: Gets all live channels.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_channels(self) -> dict | None:
    """
    Gets all live channels.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel"
    return _send_request(self, "Get Live Channels", api_url, "GET", None, None)
