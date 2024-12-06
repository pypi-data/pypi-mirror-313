"""
This module is used to get all user uploads.

Functions:
    _get_user_uploads: Gets all user uploads.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_user_uploads(self, include_completed_uploads: bool) -> dict | None:
    """
    Gets all user uploads.

    Args:
        include_completed_uploads (bool): The include completed uploads flag.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/asset/upload?"
        f"includeCompletedUploads={include_completed_uploads}"
    )

    return _send_request(self, "Get user uploads", api_url, "GET", None, None)
