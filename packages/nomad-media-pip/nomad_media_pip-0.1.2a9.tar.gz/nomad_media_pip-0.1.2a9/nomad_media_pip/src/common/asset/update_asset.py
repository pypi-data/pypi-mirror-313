"""
This module contains the logic to update an asset.

Functions:
    _update_asset: Updates an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _update_asset(
    self,
    asset_id: str,
    display_name: str | None,
    display_date: str | None,
    available_start_date: str | None,
    available_end_date: str | None,
    custom_properties: dict | None,
) -> dict | None:
    """
    Updates an asset.

    Args:
        asset_id (str): The ID of the asset to update.
        display_name (str | None): The display name of the asset.
        display_date (str | None): The display date of the asset.
        available_start_date (str | None): The available start date of the asset.
        available_end_date (str | None): The available end date of the asset.
        custom_properties (dict | None): The custom properties of the asset.
            dict format: { "key": "string", "value": "string" }

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}"

    body: dict = {
        "displayName": display_name,
        "displayDate": display_date,
        "availableStartDate": available_start_date,
        "availableEndDate": available_end_date,
        "customProperties": custom_properties
    }

    return _send_request(self, "Update asset", api_url, "PATCH", None, body)
