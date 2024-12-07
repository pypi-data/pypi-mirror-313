"""
This module gets the live output profile groups from the service API.

Functions:
	_get_live_output_profile_groups: Gets the live output profile groups.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_output_profile_groups(self) -> dict | None:
    """
    Gets the live output profile groups.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfileGroup"

    return _send_request(self, "Get Live Output Profile Groups", api_url, "GET", None, None)
