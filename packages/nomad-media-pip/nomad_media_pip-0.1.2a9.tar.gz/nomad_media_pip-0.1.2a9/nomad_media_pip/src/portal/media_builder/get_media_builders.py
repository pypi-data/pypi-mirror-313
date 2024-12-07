"""
This module gets the media builders from the service API.

Functions:
    _get_media_builders: Gets the media builders.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_media_builders(self) -> dict | None:
    """
    Gets the media builders.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder"

    return _send_request(self, "Get Media Builders", api_url, "GET", None, None)
