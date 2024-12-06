"""
This module creates a schedule item live channel.

Functions:
    _create_schedule_item_live_channel: Creates a schedule item live channel.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_schedule_item_live_channel(
    self,
    scheudle_id: str,
    days: list[dict],
    duration_time_code: str,
    end_time_code: str,
    live_channel: dict,
    previous_item: str | None,
    time_code: str,
) -> dict | None:
    """
    Creates a schedule item live channel.

    Args:
        schedule_id (str): The id of the schedule the live channel item is to be added to.
        days (list[dict]): The days of the schedule item live channel.
            Format: {"id": "string", "description": "string"}
        duration_time_code (str): The duration time between time_code and end_time_code.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str): The end time code of the schedule item live channel.
            Please use the following format: hh:mm:ss;ff.
        live_channel (dict): The live channel of the schedule item live channel.
            Format: {"id": "string", "description": "string"}.
            Note: The live channel must be non-secure output.
        previous_item (str | None): The previous item of the schedule item live channel.
        time_code (str): The time code of the schedule item live channel.
            Please use the following format: hh:mm:ss;ff.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{scheudle_id}/item"

    body: dict = {
        "days": days,
        "durationTimeCode": duration_time_code,
        "endTimeCode": end_time_code,
        "liveChannel": live_channel,
        "previousItem": previous_item,
        "scheduleItemType": "1",
        "sourceType": "4",
        "timeCode": time_code
    }

    return _send_request(self, "Create Schedule Item Live Channel", api_url, "POST", None, body)
