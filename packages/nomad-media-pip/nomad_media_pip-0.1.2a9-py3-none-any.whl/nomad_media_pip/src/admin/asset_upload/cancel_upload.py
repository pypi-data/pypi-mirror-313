"""
This module contains the _cancel_upload function, which cancels an asset upload.

Functions:
    _cancel_upload: Cancels an asset upload.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _cancel_upload(self, content_id: str) -> dict | None:
    """
    Cancels an asset upload.

    Args:
        content_id (str): The ID of the asset upload to cancel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/upload/{content_id}/cancel"

    return _send_request(self, "Cancel Upload", api_url, "POST", None, None)
