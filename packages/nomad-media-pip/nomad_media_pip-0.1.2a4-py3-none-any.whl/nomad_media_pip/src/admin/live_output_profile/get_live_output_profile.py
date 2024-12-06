"""
This module gets the live output profile from the service API.

Functions:
    _get_live_output_profile: Gets the live output profile.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_output_profile(self, output_id: str) -> dict | None:
    """
    Gets the live output profile.

    Args:
        output_id (str): The ID of the live output profile to get.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfile/{output_id}"

    return _send_request(self, "Get Live Output Profile", api_url, "GET", None, None)
