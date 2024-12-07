"""
This module creates a media builder.

Functions:
    _create_media_builder: Creates a media builder.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_media_builder(
    self,
    name: str,
    destination_folder_id: str | None,
    collections: list[str] | None,
    related_content: list[str] | None,
    tags: list[str] | None,
    properties: dict | None
) -> dict | None:
    """
    Creates a media builder.

    Args:
        name (str): The name of the media builder.
        destination_folder_id (str): The ID of the destination folder.
        collections (list[str]): The collections of the media builder.
        related_content (list[str]): The related content of the media builder.
        tags (list[str]): The tags of the media builder.
        properties (dict): The properties of the media builder.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder"

    body: dict = {
        "name": name,
        "destinationFolderId": destination_folder_id,
        "collections": collections,
        "relatedContent": related_content,
        "tags": tags,
        "properties": properties
    }

    return _send_request(self, "Create Media Builder", api_url, "POST", None, body)
