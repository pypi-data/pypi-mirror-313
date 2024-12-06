"""
This module contains the function to get asset metadata summary.

Functions:
    _get_asset_metadata_summary: Gets the asset metadata summary.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_metadata_summary(self, asset_id: str) -> dict | None:
    """
    Gets the asset metadata summary.

    Args:
        asset_id (str): The ID of the asset to get the metadata summary for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/metadata-summary"

    return _send_request(self, "Get asset metadata summary", api_url, "GET", None, None)
