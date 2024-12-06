"""
This module contains the function to get content definitions.

Functions:
    _get_content_definitions: Gets content definitions.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content_definitions(
    self,
    content_management_type: int | None,
    sort_column: str | None,
    is_desc: bool | None,
    page_index: int | None,
    page_size: int | None
) -> dict | None:
    """
    Gets content definitions.

    Args:
        content_management_type (number | null): The type of content management to get.
            enum: 1; None, 2; DataSelector, 3; FormSelector
        sort_column (string | null): The column to sort by.
        is_desc (boolean | null): Whether to sort descending.
        page_index (number | null): The page index to get.
        page_size (number | null): The page size to get.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentDefinition"

    params: dict = {
        "contentManagementType": content_management_type,
        "sortColumn": sort_column,
        "isDesc": is_desc,
        "pageIndex": page_index,
        "pageSize": page_size
    }

    return _send_request(self, "Getting Content Definitions", api_url, "GET", params, None)
