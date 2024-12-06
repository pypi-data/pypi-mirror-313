"""
This module gets the content of the current user from the service API.

Functions:
    _get_my_content: Gets the content of the current user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_my_content(self) -> dict | None:
    """
    Gets the content of the current user.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/my-content"

    return _send_request(self, "Get My Content", api_url, "GET", None, None)
