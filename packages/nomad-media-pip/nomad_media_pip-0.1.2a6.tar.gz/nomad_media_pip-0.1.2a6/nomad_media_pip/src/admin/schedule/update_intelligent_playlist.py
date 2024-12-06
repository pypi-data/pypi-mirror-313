"""
This module updates an intelligent playlist in the service API.

Functions:
    _update_intelligent_playlist: Updates an intelligent playlist.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_intelligent_playlist import _get_intelligent_playlist
from nomad_media_pip.src.admin.schedule.get_schedule_items import _get_schedule_items


def _update_intelligent_playlist(
    self,
    schedule_id: str,
    collections: list[dict] | None,
    end_search_date: str | None,
    end_search_duration_in_minutes: int | None,
    name: str | None,
    related_content: list[dict] | None,
    search_date: str | None,
    search_duration_in_minutes: int | None,
    search_filter_type: str | None,
    tags: list[dict] | None,
    thumbnail_asset: dict | None
) -> dict | None:
    """
    Updates an intelligent playlist.

    Args:
        schedule_id (str): The id of the schedule the intelligent playlist is to be updated.
        collections (list[dict] | None): The collections of the intelligent playlist.
            dict format: {"id": "string", "description": "string"}
        end_search_date (str | None): The end search date of the intelligent playlist.
            Only use when search_filter_type = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        end_search_duration_in_minutes int | None: The end search duration in minutes of the intelligent playlist.
        name (str | None): The name of the intelligent playlist.
        related_contents (list[dict] | None): The related content of the intelligent playlist.
        search_date (str | None): The search date of the intelligent playlist.
            Only use when search_filter_type = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        search_duration_in_minutes int | None: The search duration in minutes of the intelligent playlist.
        search_filter_type (str | None): The search filter type of the intelligent playlist.
            Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
        tags (list[dict] | None): The tags of the intelligent playlist.
        thumbnail_asset (dict | None): The thumbnail asset of the intelligent playlist.
            dict format: {"id": "string", "description": "string"}

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """
    schedule_api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}"

    playlist_info: dict | None = _get_intelligent_playlist(self, schedule_id)
    if playlist_info is None:
        return

    schedule_body: dict = {
        "name": name or playlist_info.get("name"),
        "scheduleType": "4",
        "thumbnailAsset": thumbnail_asset or playlist_info.get("thumbnailAsset"),
        "scheduleStatus": playlist_info.get("scheduleStatus"),
        "status": playlist_info.get("status")
    }

    schedule_info: dict | None = _send_request(
        self, "Update Intelligent Playlist", schedule_api_url, "PUT", schedule_body, None
    )
    if schedule_info is None:
        return

    item_info: dict | None = _get_schedule_items(self, schedule_id)
    item: dict = item_info[0]

    item_api_url: str = f"{schedule_api_url}/item/{item['id']}"

    item_body: dict = {
        'id': item['id'],
        'collections': collections if collections != [] else item.get("collections"),
        'endSearchDate': end_search_date if end_search_date else item.get("endSearchDate"),
        'endSearchDurationInMinutes': end_search_duration_in_minutes if end_search_duration_in_minutes else item.get("endSearchDurationInMinutes"),
        'relatedContent': related_content if related_content != [] else item.get("relatedContent"),
        'scheduleItemType': "2",
        'searchDate': search_date if search_date else item.get("searchDate"),
        'searchDurationInMinutes': search_duration_in_minutes if search_duration_in_minutes else item.get("searchDurationInMinutes"),
        'searchFilterType': search_filter_type if search_filter_type else item.get("searchFilterType"),
        'sourceType': "2",
        'tags': tags if tags != [] else item.get("tags")}

    item_info: dict | None = _send_request(self, "Update Intelligent Playlist", item_api_url, "PUT", item_body, None)

    for key in schedule_info:
        item_info[key] = schedule_info[key]

    return item_info
