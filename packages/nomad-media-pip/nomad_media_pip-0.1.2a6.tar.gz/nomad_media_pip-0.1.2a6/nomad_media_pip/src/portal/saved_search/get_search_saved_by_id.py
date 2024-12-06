"""
This module gets the saved search by ID from the service API.

Functions:
    _get_search_saved_by_id: Gets the saved search by ID.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_search_saved_by_id(self, saved_search_id: str) -> dict | None:
    """
    Gets the saved search by ID.

    Args:
        saved_search_id (str): The ID of the saved search to get.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/search-saved/{saved_search_id}"

    return _send_request(self, "Get saved search", api_url, "GET", None, None)
