"""
This module gets the media builder ids from the asset id.

Functions:
	_get_media_builder_ids_from_asset: Gets the media builder ids from the asset id.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_media_builder_ids_from_asset(self, source_asset_id: str) -> dict | None:
    """
    Gets the media builder ids from the asset id.

    Args:
        source_asset_id (str): The ID of the source asset.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/idsbysource/{source_asset_id}"

    return _send_request(self, "Get Media Builder Ids From Asset", api_url, "GET", None, None)
