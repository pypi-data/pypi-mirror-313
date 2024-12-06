"""
This module deletes a live input.

Functions:
    _delete_live_input: Deletes a live input.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_live_input(self, input_id: str) -> dict | None:
    """
    Deletes a live input.

    Args:
        input_id (str): The ID of the live input to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveInput/{input_id}"

    return _send_request(self, "Delete Live Input", api_url, "DELETE", None, None)
