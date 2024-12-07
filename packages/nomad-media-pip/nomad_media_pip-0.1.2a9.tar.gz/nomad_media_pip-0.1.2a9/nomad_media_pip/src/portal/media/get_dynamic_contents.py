"""
This module gets the dynamic contents from the service API.

Functions:
    _get_dynamic_contents: Gets the dynamic contents.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_dynamic_contents(self) -> dict | None:
    """
    Gets the dynamic contents.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/content"

    return _send_request(self, "Get Dynamic Contents", api_url, "GET", None, None)
