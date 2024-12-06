"""
This module contains the function to create asset ad break.

Functions:
    _create_asset_ad_break: Creates asset ad break.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_asset_ad_break(
    self,
    asset_id: str,
    time_code: str | None,
    tags: list[dict] | None,
    labels: list[dict] | None
) -> dict | None:
    """
    Creates asset ad break.

    Args:
        asset_id (str): The id of the asset.
        time_code (str | None): The time code of the asset ad break.
            Please use the following format: hh:mm:ss;ff.
        tags (list[dict] | None): The tags of the asset ad break.
            dict format: {"id": "string", "description": "string"}
        labels (list[dict] | None): The labels of the asset ad break.
            dict format: {"id": "string", "description": "string"}

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/adbreak"

    body: dict = {
        "id": asset_id,
        "timecode": time_code
    }

    if tags:
        body["tags"] = tags

    if labels:
        body["labels"] = labels

    return _send_request(self, "Create ad break", api_url, "POST", None, body)
