"""
This module is used to get live operator.

Functions:
    _get_live_operator: Gets live operator.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_operator(self, channel_id: str) -> dict | None:
    """
    Gets live operator.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator/{channel_id}"

    return _send_request(self, "Get Live Operator", api_url, "GET", None, None)
