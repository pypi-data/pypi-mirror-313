"""
This module is used to get the content definition types from the service API.

Functions:
    _get_content_definition_types: Gets the content definition types.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_definition_types(self) -> dict | None:
    """
    Gets the content definition types.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/lookup/6"

    return _send_request(self, "Get content definition types", api_url, "GET", None, None)
