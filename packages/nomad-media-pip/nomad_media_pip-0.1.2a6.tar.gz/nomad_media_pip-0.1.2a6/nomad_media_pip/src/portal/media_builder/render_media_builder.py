"""
This module renders the media builder.

Functions:
    _render_media_builder: Renders the media builder.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _render_media_builder(self, media_builder_id: str) -> dict | None:
    """
    Renders the media builder.

    Args:
        media_builder_id (str): The ID of the media builder to render.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/mediaBuilder/{media_builder_id}/render"

    return _send_request(self, "Render Media Builder", api_url, "POST", None, None)
