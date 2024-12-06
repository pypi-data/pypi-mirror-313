"""
This module gets the content cookies from the service API.

Functions:
    _get_content_cookies: Gets the content cookies.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_cookies(self, content_id: str) -> dict | None:
    """
    Gets the content cookies.

    Args:
        content_id (str): The ID of the content.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/set-cookies/{content_id}"

    return _send_request(self, "Get Content Cookies", api_url, "GET", None, None)
