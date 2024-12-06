"""
This module is used to get asset child nodes.

Functions:
    _get_asset_child_nodes: Gets asset child nodes.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_asset_child_nodes(
    self,
    asset_id: str,
    folder_id: str,
    sort_column: str,
    is_desc: str,
    page_index: int,
    page_size: int
) -> dict | None:
    """
    Gets asset child nodes.

    Args:
        asset_id (str): The ID of the asset to get the child nodes for.
        folder_id (str): The ID of the folder to get the child nodes for.
        sort_column (str): The sort column.
        is_desc (str): The is descending flag.
        page_index (int): The page index.
        page_size (int): The page size.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/getAssetChildNodes"

    params: dict = {
        "folderId": folder_id,
        "sortColumn": sort_column,
        "isDesc": is_desc,
        "pageIndex": page_index,
        "pageSize": page_size
    }

    return _send_request(self, "Get asset child nodes", api_url, "GET", params, None)
