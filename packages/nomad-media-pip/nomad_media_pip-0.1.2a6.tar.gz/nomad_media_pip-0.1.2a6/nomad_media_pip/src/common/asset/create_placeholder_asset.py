"""
This module contains the function to create placeholder asset.

Functions:
    _create_placeholder_asset: Creates placeholder asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_placeholder_asset(self, parent_id: str, asset_name: str) -> dict | None:
    """
    Creates placeholder asset.

    Args:
        parent_id (str): The parent asset id for the placeholder asset.
        asset_name (str): The visual name of the new placeholder.
            It can contain spaces and other characters, must contain file extension.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{parent_id}/create-placeholder"

    body: dict = {
        "assetName": asset_name
    }

    return _send_request(self, "Create placeholder asset", api_url, "POST", None, body)
