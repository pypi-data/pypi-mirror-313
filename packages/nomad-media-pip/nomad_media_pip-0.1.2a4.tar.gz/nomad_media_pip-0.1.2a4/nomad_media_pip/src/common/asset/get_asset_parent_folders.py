"""
This module is used to get asset parent folders.

Functions:
    _get_asset_parent_folders: Gets asset parent folders.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_parent_folders(self, asset_id: str, page_size: int) -> dict | None:
    """
    Gets asset parent folders.

    Args:
        asset_id (str): The ID of the asset to get the parent folders for.
        page_size (int): The number of parent folders to return.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/parent-folders"

    params: dict = {
        "pageSize": page_size
    }

    return _send_request(self, "Get asset parent folders", api_url, "GET", params, None)
