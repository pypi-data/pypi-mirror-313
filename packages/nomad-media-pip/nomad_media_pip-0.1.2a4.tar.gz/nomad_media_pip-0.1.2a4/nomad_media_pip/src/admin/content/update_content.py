"""
This module contains the function to update content.

Functions:
    _update_content: Updates content.
"""

from deepdiff import DeepDiff

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.content.get_content import _get_content


def _update_content(
    self,
    content_id: str,
    content_definition_id: str,
    properties: dict,
    language_id: str | None
) -> dict | None:
    """
    Updates content.

    Args:
        content_id (str): The ID of the content to update.
        content_definition_id (str): The ID of the content definition.
        properties (dict): The properties to update.
        language_id (str | None): The ID of the language to update the content in.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/content/{content_id}"

    body: dict | None = _get_content(self, content_id, content_definition_id, None)

    if body is not None:
        if body["contentDefinitionId"] != content_definition_id:
            body["contentDefinitionId"] = content_definition_id
        if body.get("languageId") != language_id:
            body["languageId"] = language_id
        if body["contentId"] != content_id:
            body["contentId"] = content_id

        _update_properties(body, properties)

    else:
        body: dict = {
            "contentDefinitionId": content_definition_id,
            "contentId": content_id,
            "languageId": language_id,
            "properties": properties
        }

    return _send_request(self, "Update content", api_url, "PUT", None, body)


def _update_properties(body, properties) -> None:
    for key, value in properties.items():
        if isinstance(value, list):
            for i, _ in enumerate(value):
                if DeepDiff(body['properties'][key][i], value[i]):
                    body['properties'][key][i] = value[i]
        elif isinstance(value, dict):
            if DeepDiff(body['properties'][key], value):
                body['properties'][key] = value
        elif body['properties'].get(key) != value:
            body['properties'][key] = value
