"""
This module deletes a live output profile group from the service.

Functions:
	_delete_live_output_profile_group: Deletes a live output profile group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_live_output_profile_group(self, live_output_profile_group_id: str) -> dict | None:
    """
    Deletes a live output profile group.

    Args:
        live_output_profile_group_id (str): The ID of the live output profile group to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfileGroup/{live_output_profile_group_id}"

    return _send_request(self, "Delete Live Output Profile Group", api_url, "DELETE", None, None)
