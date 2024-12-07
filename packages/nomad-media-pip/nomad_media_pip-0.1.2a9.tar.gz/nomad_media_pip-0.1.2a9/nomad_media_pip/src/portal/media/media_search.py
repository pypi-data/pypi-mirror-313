"""
This module contains the logic to search for media.

Functions:
    _media_search: Searches for media.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _media_search(
    self,
    search_query: str | None,
    ids: list[str],
    sort_fields: list[dict],
    offset: int | None,
    size: int | None
) -> dict | None:
    """
    Searches for media.

    Args:
        search_query (str | None): The search query.
        ids (list[str]): The IDs to search for.
        sort_fields (list[dict]): The sort fields.
        offset (int | None): The offset.
        size (int | None): The size.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/search"

    body: dict = {
        key: value for key, value in {
            "searchQuery": search_query,
            "ids": ids,
            "sortFields": sort_fields,
            "offset": offset,
            "size": size
        }.items() if value is not None
    }

    return _send_request(self, "Media search", api_url, "POST", None, body)
