"""
Update a schedule item search filter.

Functions:
    _update_schedule_item_search_filter: Updates a schedule item search filter.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_schedule_item import _get_schedule_item


def _update_schedule_item_search_filter(
    self,
    schedule_id: int,
    item_id: int,
    collections: list[dict] | None,
    days: list[dict] | None,
    duration_time_code: str | None,
    end_search_date: str | None,
    end_search_duration_in_minutes: int | None,
    end_time_code: str | None,
    related_content: list[dict] | None,
    search_date: str | None,
    search_duration_in_minutes: int | None,
    search_filter_type: int | None,
    tags: list[dict] | None,
    time_code: str | None
) -> dict | None:
    """
    Updates a schedule item search filter.

    Args:
        schedule_id (str): The id of the schedule the schedule item search filter is to be updated from.
        item_id (str): The id of the item to be updated.
        collections (list[dict] | None): The collections of the schedule item search filter.
            dict format: {"id": "string", "description": "string"}
        days (list[dict] | None): The days of the schedule item search filter.
            dict format: {"id": "string", "description": "string"}
        duration_time_code (str | None): The duration time between time_code and end_time_code.
            Please use the following format: hh:mm:ss;ff.
        end_search_date (str | None): The end search date of the schedule item search filter.
            Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        end_search_duration_in_minutes int | None: The end search duration in minutes of the
            schedule item search filter.
        end_time_code (str | None): The end time code of the schedule item search filter.
            Please use the following format: hh:mm:ss;ff.
        related_contents (list[dict] | None): The related content of the schedule item search filter.
            dict format: {"id": "string", "description": "string"}
        search_date (str | None): The search date of the schedule item search filter.
            Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        search_duration_in_minutes int | None: The search duration in minutes of the
            schedule item search filter.
        search_filter_type (str | None): The search filter type of the schedule item search filter.
            Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
        tags (list[dict] | None): The tags of the schedule item search filter.
            dict format: {"id": "string", "description": "string"}
        time_code (str | None): The time code of the schedule item search filter.
            Please use the following format: hh:mm:ss;ff.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item/{item_id}"

    schedule_item: dict | None = _get_schedule_item(self, schedule_id, item_id)

    body: dict = {
        "collections": collections or schedule_item.get("collections"),
        "days": days or schedule_item.get("days"),
        "durationTimeCode": duration_time_code or schedule_item.get("durationTimeCode"),
        "endSearchDate": end_search_date or schedule_item.get("endSearchDate"),
        "endSearchDurationInMinutes": end_search_duration_in_minutes or schedule_item.get("endSearchDurationInMinutes"),
        "endTimeCode": end_time_code or schedule_item.get("endTimeCode"),
        "relatedContent": related_content or schedule_item.get("relatedContent"),
        "scheduleItemType": "1",
        "searchDate": search_date or schedule_item.get("searchDate"),
        "searchDurationInMinutes": search_duration_in_minutes or schedule_item.get("searchDurationInMinutes"),
        "searchFilterType": search_filter_type or schedule_item.get("searchFilterType"),
        "sourceType": "2",
        "tags": tags or schedule_item.get("tags"),
        "timeCode": time_code or schedule_item.get("timeCode")
    }

    return _send_request(self, "Update Schedule Item Search Filter", api_url, "PUT", None, body)
