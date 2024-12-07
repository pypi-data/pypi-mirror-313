"""
This module contains the function to move a media builder item to a new position in the media builder.

Functions:
    _move_media_builder_item: Moves a media builder item to a new position in the media builder.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _move_media_builder_item(self, media_builder_id: str, item_id: str, previous_item_id: str | None) -> None:
    """
    Moves a media builder item to a new position in the media builder.

    Args:
        media_builder_id (str): The ID of the media builder.
        item_id (str): The ID of the item to move.
        previous_item_id (str | None): The ID of the item that the item should be moved after.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}/items/{item_id}/move"

    body: dict = {
        "previousItemId": previous_item_id
    }

    return _send_request(self, "Move Media Builder Item", api_url, "POST", None, body)
