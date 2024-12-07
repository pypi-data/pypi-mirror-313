"""
This module gets the live output profile group from the service API.

Functions:
	_get_live_output_profile_group: Gets the live output profile group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_output_profile_group(self, live_output_profile_group_id: str) -> dict | None:
    """
    Gets the live output profile group.

    Args:
        live_output_profile_group_id (str): The ID of the live output profile group to get.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfileGroup/{live_output_profile_group_id}"

    return _send_request(self, "Get Live Output Profile Group", api_url, "GET", None, None)
