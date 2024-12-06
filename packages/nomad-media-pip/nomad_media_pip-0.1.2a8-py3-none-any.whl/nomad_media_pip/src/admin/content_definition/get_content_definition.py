"""
This module is used to get the content definition of a specific asset.

Functions:
    _get_content_definition: Gets the content definition of a specific asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_definition(self, content_definition_id: str) -> dict | None:
    """
    Gets the content definition of a specific asset.

    Args:
        content_definition_id (str): The ID of the asset to get the content definition for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentDefinition/{content_definition_id}"

    return _send_request(self, "Get content definitions", api_url, "GET", None, None)
