"""
This module contains the _upload_complete_asset function, which completes an asset upload.

Functions:
    _upload_complete_asset: Completes an asset upload.
"""


from nomad_media_pip.src.helpers.send_request import _send_request


def _upload_complete_asset(self, content_id: str) -> dict | None:
    """
    Completes an asset upload.

    Args:
        content_id (str): The ID of the asset to complete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/upload/{content_id}/complete"

    return _send_request(self, "Upload Complete Asset", api_url, "POST", None, None)
