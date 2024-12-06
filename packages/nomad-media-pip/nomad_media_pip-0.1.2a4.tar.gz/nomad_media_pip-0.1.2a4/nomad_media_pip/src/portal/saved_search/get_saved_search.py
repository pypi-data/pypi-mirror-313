"""
This module gets the saved search from the service API.

Functions:
    _get_saved_search: Gets the saved search.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_saved_search(self, saved_search_id: str) -> dict | None:
    """
    Gets the saved search.

    Args:
        saved_search_id (str): The ID of the saved search.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/savedsearch/{saved_search_id}"

    return _send_request(self, "Get saved search", api_url, "GET", None, None)
