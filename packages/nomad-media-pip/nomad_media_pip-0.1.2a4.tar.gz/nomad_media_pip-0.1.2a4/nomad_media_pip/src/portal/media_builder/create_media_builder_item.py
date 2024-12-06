"""
This module creates a media builder item.

Functions:
    _create_media_builder_item: Creates a media builder item.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_media_builder_item(
    self,
    media_builder_id: str,
    source_asset_id: str | None,
    start_time_code: str | None,
    end_time_code: str | None,
    source_annotation_id: str | None,
    related_contents: list[str] | None
) -> dict | None:
    """
    Creates a media builder item.

    Args:
        media_builder_id (str): The ID of the media builder to create the item for.
        source_asset_id (str | None): The ID of the source asset.
        start_time_code (str | None): The start time code of the media builder item. Only use if using source asset.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str | None): The end time code of the item. Only use if using source asset.
            Please use the following format: hh:mm:ss;ff.
        source_annotation_id (str): The ID of the source annotation. Only use if using source annotation.
        related_contents (list[str] | None): The related contents of the item.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}/items"

    body: dict = {
        "sourceAssetId": source_asset_id,
        "startTimeCode": start_time_code,
        "endTimeCode": end_time_code,
        "sourceAnnotationId": source_annotation_id,
        "relatedContent": related_contents
    }

    return _send_request(self, "Create Media Builder Item", api_url, "POST", None, body)
