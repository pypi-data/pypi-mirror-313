"""
This module contains the function to create folder asset.

Functions:
    _create_folder_asset: Creates folder asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_folder_asset(self, parent_id: str, display_name: str) -> dict | None:
    """
    Creates folder asset.

    Args:
        parent_id (str): The ID of the parent asset.
        display_name (str): The display name of the folder asset.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{parent_id}/create-folder"

    body: dict = {
        "displayName": display_name
    }

    return _send_request(self, "Create folder asset", api_url, "POST", None, body)
