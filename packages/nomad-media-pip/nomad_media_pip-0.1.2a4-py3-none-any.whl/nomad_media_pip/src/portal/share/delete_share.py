"""
This module contains the logic to deletes an asset.

Functions:
    _delete_share: deletes an asset
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_share(self, share_id: str) -> dict | None:
    """
    Deletes an asset

    Args:
        share_id (str): The share id of the deleteShare.

    Returns:
        dict: The JSON response form the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.

    Exceptions:
        InvalidAPITypeException: If the API type is not portal.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/share/{share_id}"

    return _send_request(self, "Delete Share", api_url, "DELETE", None, None)
