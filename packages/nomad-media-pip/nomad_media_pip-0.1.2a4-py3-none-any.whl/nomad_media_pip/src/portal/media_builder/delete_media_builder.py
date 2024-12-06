"""
This module deletes a media builder from the service.

Functions:
    _delete_media_builder: Deletes a media builder.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_media_builder(self, media_builder_id: str) -> None:
    """
    Deletes a media builder.

    Args:
        media_builder_id (str): The ID of the media builder to delete.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}"

    _send_request(self, "Delete Media Builder", api_url, "DELETE", None, None)
