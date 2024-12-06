"""
This module updates a playlist in the service.

Functions:
    _update_playlist: Updates a playlist.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_playlist import _get_playlist


def _update_playlist(
    self,
    schedule_id: str,
    default_video_asset: dict | None,
    loop_playlist: bool | None,
    name: str | None,
    thumbnail_asset: dict | None
) -> dict | None:
    """
    Updates a playlist.

    Args:
        schedule_id (str): The id of the schedule the playlist is to be updated from.
        default_video_asset (list[dict] | None): The default video asset of the playlist.
            dict format: {"id": "string", "description": "string"}
        loop_playlist (bool | None): Whether or not to loop the playlist.
        name (str | None): The name of the playlist.
        thumbnail_asset (dict | None): The thumbnail asset of the playlist.
            dict format: {"id": "string", "description": "string"}

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}"

    playlist: dict | None = _get_playlist(self, schedule_id)

    body: dict = {
        "defaultVideoAsset": default_video_asset or playlist.get("defaultVideoAsset"),
        "id": schedule_id,
        "loopPlaylist": loop_playlist or playlist.get("loopPlaylist"),
        "name": name or playlist.get("name"),
        "scheduleType": "1",
        "thumbnailAsset": thumbnail_asset or playlist.get("thumbnailAsset")
    }

    return _send_request(self, "Update Playlist", api_url, "PUT", None, body)
