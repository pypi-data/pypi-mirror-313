"""
This module is used to import annotations.

Functions:
    _import_annotations: Imports annotations.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _import_annotations(self, asset_id: str, annotations: list[dict]) -> None:
    """
    Imports annotations.

    Args:
        asset_id (str): The ID of the asset to import the annotations for.
        annotations (list[dict]): The annotations to import.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/annotation/import"

    return _send_request(self, "Import annotations", api_url, "POST", None, annotations)
