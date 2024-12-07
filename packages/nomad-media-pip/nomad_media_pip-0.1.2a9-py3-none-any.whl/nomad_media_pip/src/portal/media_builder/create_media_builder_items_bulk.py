"""
This module creates media builder items in bulk.

Functions:
    _create_media_builder_items_bulk: Creates media builder items in bulk.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_media_builder_items_bulk(self, media_builder_id: str, media_builder_items: list[dict]) -> dict | None:
    """
    Creates media builder items in bulk.

    Args:
        media_builder_id (str): The ID of the media builder to create the items for.
        media_builder_items (list[dict]): The items of media bulder items.
            dict format: [{"sourceAssetId": "string", "sourceAnnotationId": "string | null",
            "startTimeCode": "string | null", "endTimeCode": "string | null"}]

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}/items/bulk"

    body: list = media_builder_items

    return _send_request(self, "Create Media Builder Items Bulk", api_url, "POST", None, body)
