"""
This module updates a schedule item playlist schedule.

Functions:
    _update_schedule_item_playlist_schedule: Updates a schedule item playlist schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_schedule_item import _get_schedule_item


def _update_schedule_item_playlist_schedule(
    self,
    schedule_id: int,
    item_id: int,
    days: list[dict] | None,
    duration_time_code: str | None,
    end_time_code: str | None,
    playlist_schedule: dict | None,
    time_code: str | None
) -> dict | None:
    """
    Updates a schedule item playlist schedule.

    Args:
        schedule_id (str): The id of the schedule the schedule item playlist schedule is to be updated from.
        item_id (str): The id of the item to be updated.
        days (list[dict] | None): The days of the schedule item playlist schedule.
            dict format: {"id": "string", "description": "string"}
        duration_time_code (str | None): The duration time between time_code and end_time_code.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str | None): The end time code of the schedule item playlist schedule.
            Please use the following format: hh:mm:ss;ff.
        playlist_schedule (dict | None): The playlist schedule of the schedule item playlist schedule.
            dict format: {"id": "string", "description": "string"}
        time_code (str | None): The time code of the schedule item playlist schedule.
            Please use the following format: hh:mm:ss;ff.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    schedule_item: dict | None = _get_schedule_item(self, schedule_id, item_id)

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item/{item_id}"

    body: dict = {
        "days": days or schedule_item.get("days"),
        "durationTimeCode": duration_time_code or schedule_item.get("durationTimeCode"),
        "endTimeCode": end_time_code or schedule_item.get("endTimeCode"),
        "playlistSchedule": playlist_schedule or schedule_item.get("playlistSchedule"),
        "scheduleItemType": "2",
        "sourceType": "1",
        "timeCode": time_code or schedule_item.get("timeCode")
    }

    return _send_request(self, "Update Schedule Item Playlist Schedule", api_url, "PUT", None, body)
