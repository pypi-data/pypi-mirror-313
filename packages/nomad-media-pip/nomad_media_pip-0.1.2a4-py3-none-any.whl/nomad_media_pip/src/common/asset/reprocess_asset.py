"""
This module is used to reprocess asset.

Functions:
    _reprocess_asset: Reprocess asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _reprocess_asset(self, target_ids: list[str]) -> dict | None:
    """
    Reprocess asset.

    Args:
        target_ids (list[str]): The IDs of the assets to reprocess.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/reprocess"

    body: dict = {
        "target_ids": target_ids
    }

    return _send_request(self, "Reprocess asset", api_url, "POST", None, body)
