"""
This module gets the live inputs from the service API.

Functions:
    _get_live_inputs: Gets the live inputs.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_inputs(self) -> dict | None:
    """
    Gets the live inputs.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveInput"

    return _send_request(self, "Get Live Inputs", api_url, "GET", None, None)
