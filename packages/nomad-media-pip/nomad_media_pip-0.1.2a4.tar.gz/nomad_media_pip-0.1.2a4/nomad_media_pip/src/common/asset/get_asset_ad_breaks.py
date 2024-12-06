"""
This module is used to get all ad breaks for an asset.

Functions:
    _get_asset_ad_breaks: Gets all ad breaks for an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_ad_breaks(self, asset_id: str) -> dict | None:
    """
    Gets all ad breaks for an asset.

    Args:
        asset_id (str): The ID of the asset to get the ad breaks for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/adbreak"

    return _send_request(self, "Get asset ad breaks", api_url, "GET", None, None)
