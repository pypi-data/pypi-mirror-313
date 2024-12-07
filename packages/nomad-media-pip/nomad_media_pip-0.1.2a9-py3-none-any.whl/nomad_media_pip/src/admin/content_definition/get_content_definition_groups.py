"""
This module is used to get all content definition groups.

Functions:
    _get_content_definition_groups: Gets all content definition groups.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_definition_groups(self) -> dict | None:
    """
    Gets all content definition groups.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentDefinitionGroup"

    return _send_request(self, "Get content definition group", api_url, "GET", None, None)
