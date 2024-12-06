"""
This module is used to get asset details.

Functions:
    _get_asset_details: Gets the asset details.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_details(self, asset_id: str) -> dict | None:
    """
    Gets the asset details.

    Args:
        asset_id (str): The ID of the asset to get the details for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/detail"
        if self.config["apiType"] == "admin"
        else f"{self.config["apiType"]}/api/asset/{asset_id}/detail"
    )

    return _send_request(self, "Get asset details", api_url, "GET", None, None)
