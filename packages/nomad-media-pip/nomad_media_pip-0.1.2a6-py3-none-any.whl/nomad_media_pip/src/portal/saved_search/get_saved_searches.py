"""
This module gets the saved searches from the service API.

Functions:
    _get_saved_searches: Gets the saved searches.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_saved_searches(self) -> dict | None:
    """
    Gets the saved searches.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/savedsearch"

    return _send_request(self, "Get saved searches", api_url, "GET", None, None)
