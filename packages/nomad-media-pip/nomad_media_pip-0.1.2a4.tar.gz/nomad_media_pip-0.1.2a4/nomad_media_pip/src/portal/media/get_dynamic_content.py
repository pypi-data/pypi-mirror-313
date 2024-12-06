"""
This module gets the dynamic content from the service API.

Functions:
    _get_dynamic_content: Gets the dynamic content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_dynamic_content(self, dynamic_content_record_id: str) -> dict | None:
    """
    Gets the dynamic content.

    Args:
        dynamic_content_record_id (str): The ID of the dynamic content record.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/content/{dynamic_content_record_id}"

    return _send_request(self, "Get Dynamic Content", api_url, "GET", None, None)
