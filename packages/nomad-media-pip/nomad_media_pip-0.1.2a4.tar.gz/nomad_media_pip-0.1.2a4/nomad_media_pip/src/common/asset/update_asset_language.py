"""
This module contains the logic to update the language of an asset.

Functions:
    _update_asset_language: Updates the language of an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _update_asset_language(self, asset_id: str, language_id: str) -> dict | None:
    """
    Updates the language of an asset.

    Args:
        asset_id (str): The ID of the asset to update.
        language_id (str): The ID of the language to update the asset to.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/language"

    body: dict = {
        "languageId": language_id
    }

    return _send_request(self, "Update asset language", api_url, "POST", None, body)
