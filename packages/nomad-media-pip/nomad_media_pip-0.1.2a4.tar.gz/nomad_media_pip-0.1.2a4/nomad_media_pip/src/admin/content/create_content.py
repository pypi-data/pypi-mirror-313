"""
This module contains the function to create a new content.

Functions:
    _create_content: Creates a new content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_content(self, content_definition_id: str, language_id: str | None) -> dict | None:
    """
    Creates a new content.

    Args:
        content_definition_id (str): The ID of the content definition to create.
        language_id (str): The ID of the language to create the content in.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/content/new?contentDefinitionId={content_definition_id}"

    params: dict[str, str | None] = {
        "languageId": language_id
    }

    return _send_request(self, "Create content", api_url, "GET", params, None)
