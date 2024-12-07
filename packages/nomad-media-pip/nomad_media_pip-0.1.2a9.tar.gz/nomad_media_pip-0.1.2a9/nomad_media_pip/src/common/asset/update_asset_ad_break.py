"""
This module contains the function to update an ad break for an asset.

Functions:
    _update_asset_ad_break: Updates an ad break for an asset.
"""
from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.common.asset.get_asset_ad_breaks import _get_asset_ad_breaks


def _update_asset_ad_break(
    self,
    asset_id: str,
    ad_break_id: str,
    time_code: str | None,
    tags: list[dict] | None,
    labels: list[dict] | None
) -> dict | None:
    """
    Updates an ad break for an asset.

    Args:
        asset_id (str): The ID of the asset containing the ad break.
        ad_break_id (str): The ID of the ad break to update.
        time_code (str | None): The time code of the ad break.
        tags (list[dict] | None): The tags of the ad break.
        labels (list[dict] | None): The labels of the ad break.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/adbreak/{ad_break_id}"

    asset_ad_breaks: dict | None = _get_asset_ad_breaks(self, asset_id)
    ad_break: dict | None = next(
        (
            ad_break for ad_break in asset_ad_breaks if ad_break["id"] == ad_break_id
        ), None
    )

    body: dict = {
        "id": ad_break_id,
        "timecode": time_code or ad_break.get("timecode"),
        "tags": tags or ad_break.get("tags"),
        "labels": labels or ad_break.get("labels")
    }

    return _send_request(self, "Update ad break", api_url, "PUT", None, body)
