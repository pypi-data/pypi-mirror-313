"""
This module deletes a playlist from the service.

Functions:
    _delete_playlist: Deletes a playlist from the service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_playlist(self, schedule_id: str) -> None:
    """
    Deletes a playlist from the service.

    Args:
        schedule_id (str): The ID of the playlist to delete.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}"

    _send_request(self, "Delete Playlist", api_url, "DELETE", None, None)
