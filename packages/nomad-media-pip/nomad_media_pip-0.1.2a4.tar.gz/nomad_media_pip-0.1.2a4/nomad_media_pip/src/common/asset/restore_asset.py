"""
This module contains the logic to restore an asset.

Functions:
    _restore_asset: Restores an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _restore_asset(self, asset_id: str) -> dict | None:
    """
    Restores an asset.

    Args:
        asset_id (str): The ID of the asset to restore.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/restore"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/restore"
    )

    return _send_request(self, "Restore asset", api_url, "POST", None, None)
