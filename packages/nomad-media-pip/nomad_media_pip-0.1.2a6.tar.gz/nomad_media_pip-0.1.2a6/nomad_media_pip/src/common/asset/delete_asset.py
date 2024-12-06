"""
This module is used to delete an asset.

Functions:
    _delete_asset: Deletes an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_asset(self, asset_id: str) -> dict | None:
    """
    Deletes an asset.

    Args:
        asset_id (str): The ID of the asset to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}"

    return _send_request(self, "Delete asset", api_url, "DELETE", None, None)
