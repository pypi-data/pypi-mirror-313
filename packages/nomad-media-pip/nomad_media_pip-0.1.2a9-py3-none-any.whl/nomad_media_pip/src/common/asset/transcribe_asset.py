"""
This module contains the logic to transcribe an asset.

Functions:
    _transcribe_asset: Transcribes an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _transcribe_asset(self, asset_id, transcript_id, transcript) -> dict | None:
    """
    Transcribes an asset.

    Args:
        asset_id (str): The ID of the asset to transcribe.
        transcript_id (str): The ID of the transcript to transcribe.
            dict format: { "startTimeCode": string, "content": string }

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/transcribe/{transcript_id}"

    return _send_request(self, "Transcribe asset", api_url, "POST", None, transcript)
