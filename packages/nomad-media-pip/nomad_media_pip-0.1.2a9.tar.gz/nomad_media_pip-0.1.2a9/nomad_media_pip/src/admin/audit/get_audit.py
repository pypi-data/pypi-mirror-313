"""
This module contains the _get_audit function that is used to get the audit for an asset.

Functions:
    _get_audit: Gets the audit for an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_audit(self, content_id: str) -> dict | None:
    """
    Gets the audit for an asset.

    Args:
        content_id (str): The ID of the asset.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/audit/{content_id}"

    return _send_request(self, "Get audit", api_url, "GET", None, None)
