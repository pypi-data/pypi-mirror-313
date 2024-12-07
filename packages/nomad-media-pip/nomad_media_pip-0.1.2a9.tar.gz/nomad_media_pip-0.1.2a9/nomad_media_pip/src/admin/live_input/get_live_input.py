"""
Get a live input by ID

Functions:
    _get_live_input: Gets a live input by ID.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_live_input(self, input_id: str) -> dict | None:
    """
    Gets a live input by ID.

    Args:
        input_id (str): The ID of the live input.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveInput/{input_id}"

    return _send_request(self, "Get Live Input", api_url, "GET", None, None)
