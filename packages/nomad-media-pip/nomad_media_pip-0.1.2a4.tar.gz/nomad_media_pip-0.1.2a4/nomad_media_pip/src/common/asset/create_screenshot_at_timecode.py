"""
This module is used to create a screenshot at a specific timecode for an asset.

Functions:
    _create_screenshot_at_timecode: Creates a screenshot at a specific timecode for an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_screenshot_at_timecode(self, asset_id: str, time_code: str | None) -> dict | None:
    """
    Creates a screenshot at a specific timecode for an asset.

    Args:
        asset_id (str): The ID of the asset to create a screenshot for.
        time_code (str): The timecode to create the screenshot at.
            Please use the following format: hh:mm:ss;ff.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/screenshot"

    body: dict = {
        "timecode": time_code
    }

    return _send_request(self, "Create screenshot at timecode", api_url, "POST", None, body)
