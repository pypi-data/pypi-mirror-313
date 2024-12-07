"""
This module is used to get all annotations for an asset.

Functions:
    _get_annotations: Gets all annotations for an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_annotations(self, asset_id: str) -> dict | None:
    """
    Gets all annotations for an asset.

    Args:
        asset_id (str): The ID of the asset to get the annotations for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/annotation"

    return _send_request(self, "Get asset annotations", api_url, "GET", None, None)
