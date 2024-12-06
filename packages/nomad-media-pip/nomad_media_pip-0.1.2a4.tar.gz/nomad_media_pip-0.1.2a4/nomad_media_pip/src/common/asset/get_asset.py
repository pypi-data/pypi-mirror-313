"""
This module is used to get an asset.

Functions:
    _get_asset: Gets an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset(self, asset_id):
    """
    Gets an asset.

    Args:
        asset_id (str): The ID of the asset to get.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}"

    return _send_request(self, "Get asset", api_url, "GET", None, None)
