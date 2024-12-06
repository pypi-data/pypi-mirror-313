"""
This module is used to delete an annotation.

Functions:
    _delete_annotation: Deletes an annotation.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_annotation(self, asset_id: str, annotation_id: str) -> dict | None:
    """
    Deletes an annotation.

    Args:
        asset_id (str): The ID of the asset to delete the annotation from.
        annotation_id (str): The ID of the annotation to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/annotation/{annotation_id}"

    return _send_request(self, "Delete annotation", api_url, "DELETE", None, None)
