"""
This module creates media builder items add annotations.

Functions:
	_create_media_builder_items_add_annotations: Creates media builder items add annotations.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_media_builder_items_add_annotations(self, media_builder_id: str, source_asset_id: str) -> dict | None:
    """
    Creates media builder items add annotations.

    Args:
            media_builder_id (str): The ID of the media builder to create the items add annotations for.
            source_asset_id (str): The ID of the source asset.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}"
        f"/items/{source_asset_id}/add-annotations"
    )

    return _send_request(self, "Create Media Builder Items Add Annotations", api_url, "POST", None, None)
