"""
This module is used to delete an asset ad break.

Functions:
    _delete_asset_ad_break: Deletes an asset ad break.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_asset_ad_break(self, asset_id: str, ad_break_id: str) -> dict | None:
    """
    Deletes an asset ad break.

    Args:
        asset_id (str): The ID of the asset to delete the ad break from.
        ad_break_id (str): The ID of the ad break to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/adbreak/{ad_break_id}"

    return _send_request(self, "Delete asset ad break", api_url, "DELETE", None, None)
