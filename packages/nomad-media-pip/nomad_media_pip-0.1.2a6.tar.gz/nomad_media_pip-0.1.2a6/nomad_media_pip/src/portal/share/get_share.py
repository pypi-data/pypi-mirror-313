"""
This module contains the logic to gets an asset.

Functions:
    _get_share: gets an asset
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_share(self, share_id: str) -> dict | None:
    """
    Gets an asset

    Args:
        share_id (str): The share id of the getShare.

    Returns:
        dict: The JSON response form the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.

    Exceptions:
        InvalidAPITypeException: If the API type is not portal.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/share/{share_id}"

    return _send_request(self, "Get Share", api_url, "GET", None, None)
