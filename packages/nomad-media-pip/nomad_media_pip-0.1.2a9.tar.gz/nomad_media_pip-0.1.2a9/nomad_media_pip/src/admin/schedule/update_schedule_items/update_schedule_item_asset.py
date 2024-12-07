"""
This module updates a schedule item asset.

Functions:
    _update_schedule_item_asset: Updates a schedule item asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_schedule_item import _get_schedule_item


def _update_schedule_item_asset(
    self,
    schedule_id: int,
    item_id: int,
    asset: dict | None,
    days: list[dict] | None,
    duration_time_code: str | None,
    end_time_code: str | None,
    time_code: str | None
) -> dict | None:
    """
    Updates a schedule item asset.

    Args:
        schedule_id (str): The id of the schedule the schedule item asset is to be updated from.
        item_id (str): The id of the item to be updated.
        asset (dict | None): The asset of the schedule item asset.
            dict format: {"id": "string", "description": "string"}
        days (list[dict] | None): The days of the schedule item asset.
            dict format: {"id": "string", "description": "string"}
        duration_time_code (str | None): The duration time between time_code and end_time_code.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str | None): The end time code of the schedule item asset.
            Please use the following format: hh:mm:ss;ff.
        time_code (str | None): The time code of the schedule item asset.
            Please use the following format: hh:mm:ss;ff.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    schedule_item: dict | None = _get_schedule_item(self, schedule_id, item_id)

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item/{item_id}"

    body: dict = {
        "asset": asset or schedule_item.get("asset"),
        "days": days or schedule_item.get("days"),
        "durationTimeCode": duration_time_code or schedule_item.get("durationTimeCode"),
        "endTimeCode": end_time_code or schedule_item.get("endTimeCode"),
        "scheduleItemType": "1",
        "sourceType": "3",
        "timeCode": time_code or schedule_item.get("timeCode")
    }

    return _send_request(self, "Update Schedule Item Asset", api_url, "PUT", None, body)
