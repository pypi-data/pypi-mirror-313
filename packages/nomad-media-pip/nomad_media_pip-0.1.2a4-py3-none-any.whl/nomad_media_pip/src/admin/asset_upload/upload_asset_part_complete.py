"""
This module is used to complete the upload of a part of an asset.

Functions:
    _upload_asset_part_complete: Completes the upload of a part of an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request

MAX_RETRIES = 2


def _upload_asset_part_complete(self, part_id: str, etag: str) -> dict | None:
    """
    Completes the upload of a part of an asset.

    Args:
        part_id (str): The ID of the part.
        etag (str): The ETag of the part.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/upload/part/{part_id}/complete"

    # Build the payload BODY
    body: dict[str, str] = {
        "etag": etag
    }

    return _send_request(self, "Upload Asset Part Complete", api_url, "POST", None, body)
