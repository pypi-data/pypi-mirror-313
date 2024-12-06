"""
This module contains the function to update a media builder in the service.

Functions:
    _update_media_builder: Updates a media builder.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.portal.media_builder.get_media_builder import _get_media_builder


def _update_media_builder(
    self,
    media_builder_id: str,
    name: str | None,
    destination_folder_id: str | None,
    collections: list[str] | None,
    related_content: list[str] | None,
    tags: list[str] | None,
    properties: dict | None
) -> dict | None:
    """
    Updates a media builder in the service.

    Args:
        media_builder_id (str): The ID of the media builder to update.
        name (str | None): The name of the media builder.
        destination_folder_id (str | None): The ID of the destination folder.
        collections (list[str] | None): The collections of the media builder.
        related_content (list[str] | None): The related content of the media builder.
        tags (list[str] | None): The tags of the media builder.
        properties (dict | None): The properties of the media builder.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}"

    info: dict | None = _get_media_builder(self, media_builder_id)

    body: dict = {
        "name": name or info.get("name"),
        "destinationFolderId": destination_folder_id or info.get("destinationFolderId"),
        "collections": collections or info.get("collections"),
        "relatedContent": related_content or info.get("relatedContent"),
        "tags": tags or info.get("tags"),
        "properties": properties or info.get("properties")
    }

    return _send_request(self, "Update Media Builder", api_url, "PUT", None, body)
