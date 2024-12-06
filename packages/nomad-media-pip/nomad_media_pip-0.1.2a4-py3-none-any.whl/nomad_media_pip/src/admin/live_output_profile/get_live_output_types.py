"""
This module is used to get all live output types.

Functions:
    _get_live_output_types: Gets all live output types.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_output_types(self) -> dict | None:
    """
    Gets all live output types.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/lookup/117"

    return _send_request(self, "Get Output Types", api_url, "GET", None, None)
