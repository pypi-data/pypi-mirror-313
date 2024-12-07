"""
This module is used to get asset screenshot details.

Functions:
    _get_asset_screenshot_details: Gets asset screenshot details.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_screenshot_details(self, asset_id: str, segment_id: str, screenshot_id: str) -> dict | None:
    """
    Gets asset screenshot details.

    Args:
        asset_id (str): The ID of the asset to get the screenshot details for.
        segment_id (str): The ID of the segment to get the screenshot details for.
        screenshot_id (str): The ID of the screenshot to get the details for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/{segment_id}/{screenshot_id}/detail"

    return _send_request(self, "Get asset screenshot details", api_url, "GET", None, None)
