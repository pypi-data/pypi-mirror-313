"""
Get content user track

This module contains the _get_content_user_track function, which gets the user track for a content.

Functions:
    _get_content_user_track: Gets the user track for a content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_user_track(
    self,
    content_id: str,
    content_definition_id: str,
    sort_column: str | None,
    is_desc: bool | None,
    page_index: int | None,
    size_index: int | None
) -> dict | None:
    """
    Gets the user track for a content.

    Args:
        content_id (str): The ID of the content.
        content_definition_id (str): The ID of the content definition.
        sort_column (str | None): The sort column.
        is_desc (bool | None): The is descending flag.
        page_index (int | None): The page index.
        size_index (int | None): The size index.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/content/{content_definition_id}/user-track/{content_id}"

    params: dict = {
        "sortColumn": sort_column,
        "isDesc": is_desc,
        "pageIndex": page_index,
        "sizeIndex": size_index
    }

    return _send_request(self, "Get content user track", api_url, "GET", params, None)
