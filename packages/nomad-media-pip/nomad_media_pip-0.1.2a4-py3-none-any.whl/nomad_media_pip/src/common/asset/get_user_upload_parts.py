"""
This module is used to get user upload parts.

Functions:
    _get_user_upload_parts: Gets the user upload parts.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_user_upload_parts(self, upload_id: str) -> dict | None:
    """
    Gets the user upload parts.

    Args:
        upload_id (str): The ID of the user upload to get the parts for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/upload/{upload_id}"

    return _send_request(self, "Get user upload parts", api_url, "GET", None, None)
