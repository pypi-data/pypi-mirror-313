"""
This module contains the logic to share an asset.

Functions:
    _share_asset: Shares an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _share_asset(
    self,
    asset_id: str,
    nomad_users: list[dict] | None,
    external_users: list[dict] | None,
    shared_duration_in_hours: list[dict] | None
) -> dict | None:
    """
    Shares an asset.

    Args:
        asset_id (str): The ID of the asset to share.
        nomad_users (list[dict] | None): The nomad users of the share. dict format: { id: string }
        external_users (list[dict] | None): The external users of the share. dict format: { id: string }
        shared_duration_in_hours (int | None): The share duration in hours of the share.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/share"

    body: dict = {
        "assetId": asset_id,
        "nomadUsers": nomad_users,
        "externalUsers": external_users,
        "sharedDurationInHours": shared_duration_in_hours
    }

    return _send_request(self, "Share asset", api_url, "POST", None, body)
