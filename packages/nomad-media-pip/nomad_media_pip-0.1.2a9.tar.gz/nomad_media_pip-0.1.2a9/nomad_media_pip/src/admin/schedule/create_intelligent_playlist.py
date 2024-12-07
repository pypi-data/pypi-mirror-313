"""
This module creates an intelligent playlist.

Functions:
    _create_intelligent_playlist: Creates an intelligent playlist.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_intelligent_playlist(
    self,
    collections: list[dict] | None,
    end_search_date: str | None,
    end_search_duration_in_minutes: int,
    name: str,
    related_contents: list[dict] | None,
    search_date: str | None,
    search_duration_in_minutes: int,
    search_filter_type: int,
    tags: list[dict],
    thumbnail_asset: dict | None
) -> dict | None:
    """
    Creates an intelligent playlist.

    Args:
        collections (list[dict] | None): The collections of the intelligent playlist.
            Format: {"id": "string", "description": "string"}
        end_search_date (str | None): The end search date of the intelligent playlist.
            Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        end_search_duration_in_minutes (int): The end search duration in minutes of the intelligent playlist.
        name (str): The name of the intelligent playlist.
        related_contents (list[dict] | None): The related content of the intelligent playlist.
            Format: {"id": "string", "description": "string"}
        search_date (str | None): The search date of the intelligent playlist. Only use when SEARCH_FILTER_TYPE = 2.
            Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        search_duration_in_minutes (int): The search duration in minutes of the intelligent playlist.
        search_filter_type (int): The search filter type of the intelligent playlist.
            Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
        tags (list[dict]): The tags of the intelligent playlist. Format: {"id": "string", "description": "string"}
        thumbnail_asset (dict | None): The thumbnail asset of the intelligent playlist.
            Format: {"id": "string", "description": "string"}

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    schedule_api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule"

    schedule_body: dict = {
        "name": name,
        "scheduleType": "4",
        "thumbnailAsset": thumbnail_asset
    }

    schedule_info: dict | None = _send_request(
        self, "Create Intelligent Playlist", schedule_api_url, "POST", None, schedule_body
    )

    item_api_url: str = f"{schedule_api_url}/{schedule_info['id']}/item"

    item_body: dict = {
        "collections": collections,
        "endSearchDate": end_search_date,
        "endSearchDurationInMinutes": end_search_duration_in_minutes,
        "name": name,
        "relatedContent": related_contents,
        "searchDate": search_date,
        "searchDurationInMinutes": search_duration_in_minutes,
        "searchFilterType": search_filter_type,
        "tags": tags,
        "thumbnailAsset": thumbnail_asset
    }

    item_info: dict | None = _send_request(self, "Creating Intelligent Playlist", item_api_url, "POST", None, item_body)

    for param in schedule_info:
        item_info[param] = schedule_info[param]

    return item_info
