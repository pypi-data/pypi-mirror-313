"""
This module creates a schedule item asset.

Functions:
    _create_schedule_item_asset: Creates a schedule item asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_schedule_item_asset(
    self,
    scheudle_id: str,
    asset: dict,
    days: list[dict],
    duration_time_code: str,
    end_time_code: str,
    previous_item: str | None,
    time_code: str
) -> dict | None:
    """
    Creates a schedule item asset.

    Args:
        schedule_id (str): The id of the schedule the asset item is to be added to.
        asset (dict): The asset of the schedule item asset. Format: {"id": "string"}
        days (list[dict]): The days of the schedule item asset. Format: {"id": "string"}
        duration_time_code (str): The duration time between time_code and end_time_code.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str): The end time code of the schedule item asset.
            Please use the following format: hh:mm:ss;ff.
        previous_item (str | None): The previous item of the schedule item asset.
        time_code (str): The time code of the schedule item asset.
            Please use the following format: hh:mm:ss;ff.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{scheudle_id}/item"

    body: dict = {
        "asset": asset,
        "days": days,
        "durationTimeCode": duration_time_code,
        "endTimeCode": end_time_code,
        "previousItem": previous_item,
        "scheduleItemType": "1",
        "sourceType": "3",
        "timeCode": time_code
    }

    return _send_request(self, "Create Schedule Item Asset", api_url, "POST", None, body)
