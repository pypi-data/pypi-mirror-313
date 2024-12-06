"""
This module contains the function to get asset manifest with cookies.

Functions:
    _get_asset_manifest_with_cookies: Gets the asset manifest with cookies.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_manifest_with_cookies(self, asset_id: str, cookie_id: str) -> dict | None:
    """
    Gets the asset manifest with cookies.

    Args:
        asset_id (str): The ID of the asset to get the manifest for.
        cookie_id (str): The ID of the cookie to get the manifest for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/set-cookies/{cookie_id}"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/set-cookies/{cookie_id}"
    )

    return _send_request(self, "Get asset manifest with cookies", api_url, "GET", None, None)
