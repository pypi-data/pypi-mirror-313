"""
This module creates a schedule item search filter.

Functions:
    _create_schedule_item_search_filter: Creates a schedule item search filter.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_schedule_item_search_filter(
    self,
    schedule_id: str,
    collections: list[dict] | None,
    days: list[dict],
    duration_time_code: str,
    end_search_date: str | None,
    end_search_duration_in_minutes: int,
    end_time_code: str,
    previous_item: str | None,
    related_contents: list[dict] | None,
    search_date: str | None,
    search_duration_in_minutes: int,
    search_filter_type: int,
    tags: list[dict],
    time_code: str
) -> dict | None:
    """
    Creates a schedule item search filter.

    Args:
        schedule_id (str): The id of the schedule the search filter item is to be added to.
        collections (list[dict] | None): The collections of the schedule item search filter.
            Format: {"id": "string", "description": "string"}
        days (list[dict]): The days of the schedule item search filter.
            Format: {"id": "string", "description": "string"}
        duration_time_code (str): The duration time between time_code and end_time_code.
            Please use the following format: hh:mm:ss;ff.
        end_search_date (str | None): The end search date of the schedule item search filter.
            Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        end_search_duration_in_minutes (int): The end search duration in minutes of the schedule
            item search filter.
        end_time_code (str): The end time code of the schedule item search filter.
            Please use the following format: hh:mm:ss;ff.
        previous_item (str | None): The previous item of the schedule item search filter.
        related_contents (list[dict] | None): The related contents of the schedule item search filter.
        search_date (str | None): The search date of the schedule item search filter.
            Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
        search_duration_in_minutes (str): The search duration in minutes of the schedule
            item search filter.
        search_filter_type (str): The search filter type of the schedule item search filter.
            Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
        tags (list[dict]): The tags of the schedule item search filter.
            Format: {"id": "string", "description": "string"}
        time_code (str): The time code of the schedule item search filter.
            Please use the following format: hh:mm:ss;ff.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item"

    body: dict = {
        "collections": collections,
        "days": days,
        "durationTimeCode": duration_time_code,
        "endSearchDate": end_search_date,
        "endSearchDurationInMinutes": end_search_duration_in_minutes,
        "endTimeCode": end_time_code,
        "previousItem": previous_item,
        "relatedContent": related_contents,
        "scheduleItemType": "1",
        "searchDate": search_date,
        "searchDurationInMinutes": search_duration_in_minutes,
        "searchFilterType": search_filter_type,
        "sourceType": "2",
        "tags": tags,
        "timeCode": time_code
    }

    return _send_request(self, "Create Schedule Item Search Filter", api_url, "POST", None, body)
