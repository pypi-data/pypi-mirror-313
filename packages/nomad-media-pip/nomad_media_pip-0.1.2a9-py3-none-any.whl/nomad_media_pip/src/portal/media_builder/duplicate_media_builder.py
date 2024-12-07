"""
This module contains the function to duplicate a media builder.

Functions:
    _duplicate_media_builder: Duplicates a media builder.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _duplicate_media_builder(
    self,
    media_builder_id: str,
    name: str,
    destination_folder_id: str | None,
    collections: list[str] | None,
    related_contents: list[str] | None,
    properties: dict | None
) -> dict | None:
    """
    Duplicates a media builder.

    Args:
        media_builder_id (str): The ID of the media builder to duplicate.
        name (str): The name of the new media builder.
        destination_folder_id (str | None): The ID of the folder to duplicate the media builder to.
        collections (list[str] | None): The collections to add the new media builder to.
        related_contents (list[str] | None): The related contents to add to the new media builder.
        properties (dict | None): The properties to update.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}/duplicate"

    body: dict = {
        "name": name,
        "destinationFolderId": destination_folder_id,
        "collections": collections,
        "relatedContent": related_contents,
        "properties": properties
    }

    return _send_request(self, "Duplicate Media Builder", api_url, "POST", None, body)
