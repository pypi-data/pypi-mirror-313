"""
This module is used to delete live output profile.

Functions:
    _delete_live_output_profile: Deletes live output profile.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_live_output_profile(self, output_id: str) -> dict | None:
    """
    Deletes live output profile.

    Args:
        output_id (str): The ID of the live output profile to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfile/{output_id}"

    return _send_request(self, "Delete Live Output Profile", api_url, "DELETE", None, None)
