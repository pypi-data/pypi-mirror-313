"""
Deactivate content user track

This module contains the _deactivate_content_user_track function,
which deactivates a content user track.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _deactivate_content_user_track(
    self,
    session_id: str,
    content_id: str,
    content_definition_id: str,
    deactivate: str
) -> None:
    """
    Deactivates a content user track.

    Args:
        session_id (str): The ID of the session.
        content_id (str): The ID of the content.
        content_definition_id (str): The ID of the content definition.
        deactivate (str): The deactivate flag.

    Returns:
        None: If the request succeeds
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/content/{content_definition_id}"
        f"/user-track/{content_id}/{session_id}/{deactivate}"
    )

    _send_request(self, "Deactivate content user track", api_url, "DELETE", None, None)
