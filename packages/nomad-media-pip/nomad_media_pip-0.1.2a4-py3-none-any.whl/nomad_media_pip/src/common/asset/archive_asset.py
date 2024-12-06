"""
This module contains the function to archive asset.

Functions:
    _archive_asset: Archives asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _archive_asset(self, asset_id: str) -> dict | None:
    """
    Archives asset.

    Args:
        asset_id (str): The ID of the asset to archive.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/archive"

    return _send_request(self, "Archive asset", api_url, "POST", None, None)
