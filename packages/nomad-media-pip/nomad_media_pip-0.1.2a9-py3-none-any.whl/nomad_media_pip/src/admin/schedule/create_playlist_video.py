"""
This module creates a playlist video in the service API.

Functions:
    _create_playlist_video: Creates a playlist video.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_playlist_video(self, playlist_id: str, asset: dict, previous_item: str | None) -> dict | None:
    """
    Creates a playlist video.

    Args:
        playlist_id (str): The ID of the playlist.
        video_asset (dict): The video asset of the playlist video.
            Format: {"id": "string", "description": "string"}
        previous_item (str | None): The previous item of the playlist video.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{playlist_id}/item"

    body: dict = {
        "asset": asset,
        "previousItem": previous_item
    }

    return _send_request(self, "Create Playlist Video", api_url, "POST", None, body)
