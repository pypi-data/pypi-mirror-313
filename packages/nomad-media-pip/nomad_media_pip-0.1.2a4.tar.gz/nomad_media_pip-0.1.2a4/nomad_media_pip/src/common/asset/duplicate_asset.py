"""
This module is used to duplicate an asset.

Functions:
    _duplicate_asset: Duplicates an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _duplicate_asset(self, asset_id: str) -> dict | None:
    """
    Duplicates an asset.

    Args:
        asset_id (str): The ID of the asset to duplicate.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/duplicate"

    return _send_request(self, "Duplicate asset", api_url, "POST", None, None)
