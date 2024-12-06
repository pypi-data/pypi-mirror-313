"""
This module contains the function to create content definition.

Functions:
    _create_content_definition: Creates content definition.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_content_definition(self) -> dict | None:
    """
    Creates content definition.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentDefinition/New"

    return _send_request(self, "Create content definition", api_url, "GET", None, None)
