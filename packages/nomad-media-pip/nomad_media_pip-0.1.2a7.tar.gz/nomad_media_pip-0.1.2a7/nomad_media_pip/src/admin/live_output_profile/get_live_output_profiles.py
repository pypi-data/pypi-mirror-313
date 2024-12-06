"""
This module is used to get all live output profiles.

Functions:
    _get_live_output_profiles: Gets all live output profiles.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_output_profiles(self) -> dict | None:
    """
    Gets all live output profiles.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfile"

    return _send_request(self, "Get Live Output Profiles", api_url, "GET", None, None)
