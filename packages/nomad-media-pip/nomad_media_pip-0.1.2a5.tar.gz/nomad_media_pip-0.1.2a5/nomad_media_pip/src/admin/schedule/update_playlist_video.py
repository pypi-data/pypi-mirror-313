"""
This module updates a playlist video.

Functions:
    _update_playlist_video: Updates a playlist video.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _update_playlist_video(self, schedule_id: str, item_id: str, asset: dict | None) -> dict | None:
    """
    Updates a playlist video.

    Args:
        schedule_id (str): The ID of the schedule.
        item_id (str): The ID of the playlist item.
        asset (dict | None): The asset to update.
            dict format: {"id": "string", "description": "string"}

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item/{item_id}"

    body: dict = {
        "asset": asset
    }

    return _send_request(self, "Update Playlist Video", api_url, "PUT", None, body)
