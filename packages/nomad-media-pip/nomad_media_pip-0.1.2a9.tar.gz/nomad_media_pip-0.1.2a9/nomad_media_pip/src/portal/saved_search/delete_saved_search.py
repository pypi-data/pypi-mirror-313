"""
This module deletes a saved search from the service.

Functions:
    _delete_saved_search: Deletes a saved search from the service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_saved_search(self, saved_search_id: str) -> None:
    """
    Deletes a saved search from the service.

    Args:
        saved_search_id (str): The ID of the saved search to delete.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/savedsearch/{saved_search_id}"

    return _send_request(self, "Delete saved search", api_url, "DELETE", None, None)
