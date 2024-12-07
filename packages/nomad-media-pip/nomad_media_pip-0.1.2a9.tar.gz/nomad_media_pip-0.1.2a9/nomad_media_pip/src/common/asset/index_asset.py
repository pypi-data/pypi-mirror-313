"""
This module is used to index an asset.

Functions:
    _index_asset: Indexes an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _index_asset(self, asset_id: str) -> dict | None:
    """
    Indexes an asset.

    Args:
        asset_id (str): The ID of the asset to index.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/index"

    return _send_request(self, "Index asset", api_url, "POST", None, None)
