"""
This module deletes a media builder item from the service API.

Functions:
    _delete_media_builder_item: Deletes a media builder item.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_media_builder_item(self, media_builder_id: str, item_id: str) -> None:
    """
    Deletes a media builder item.

    Args:
        media_builder_id (str): The ID of the media builder.
        item_id (str): The ID of the item to delete.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}/items/{item_id}"

    _send_request(self, "Delete Media Builder Item", api_url, "DELETE", None, None)
