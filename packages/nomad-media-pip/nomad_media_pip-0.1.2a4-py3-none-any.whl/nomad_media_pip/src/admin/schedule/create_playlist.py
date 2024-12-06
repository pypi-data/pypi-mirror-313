"""
Create a new playlist.

Functions:
    _create_playlist: Creates a playlist.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_playlist(
    self,
    name: str,
    thumbnail_asset: dict | None,
    loop_playlist: bool,
    default_video_asset: dict
) -> dict | None:
    """
    Creates a playlist.

    Args:
        name (str): The name of the playlist.
        thumbnail_asset (dict | None): The thumbnail asset of the playlist.
            Format: {"id": "string", "description": "string"}
        loop_playlist (bool): Whether the playlist is looped.
        default_video_asset (dict): The default video asset of the playlist.
            Format: {"id": "string"}. Only needed if loop_playlist is false.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.one: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule"

    body: dict = {
        "name": name,
        "scheduleType": "1",
        "thumbnailAsset": thumbnail_asset,
        "loopPlaylist": loop_playlist,
        "defaultVideoAsset": default_video_asset
    }

    return _send_request(self, "Create Playlist", api_url, "POST", None, body)
