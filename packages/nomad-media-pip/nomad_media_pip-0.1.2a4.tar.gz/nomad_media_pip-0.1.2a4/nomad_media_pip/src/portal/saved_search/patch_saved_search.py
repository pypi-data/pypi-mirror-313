"""
This module patches a saved search in the service.

Functions:
    _patch_saved_search: Patches a saved search.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _patch_saved_search(
    self,
    saved_search_id: str,
    name: str | None,
    featured: bool | None,
    bookmarked: bool | None,
    public: bool | None,
    sequence: int | None
) -> dict | None:
    """
    Patches a saved search.

    Args:
        saved_search_id (str): The ID of the saved search to patch.
        name (str | None): The name of the saved search.
        featured (bool | None): The featured flag.
        bookmarked (bool | None): The bookmarked flag.
        public (bool | None): The public flag.
        sequence (int | None): The sequence of the saved search.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/savedsearch/{saved_search_id}"

    body: dict = {
        key: value for key, value in {
            "name": name,
            "featured": featured,
            "bookmarked": bookmarked,
            "public": public,
            "sequence": sequence
        }.items() if value is not None
    }

    return _send_request(self, "Patch saved search", api_url, "PATCH", None, body)
