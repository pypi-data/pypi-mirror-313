"""
This module updates the intelligent schedule in the service API.

Functions:
    _update_intelligent_schedule: Updates the intelligent schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_intelligent_schedule import _get_intelligent_schedule


def _update_intelligent_schedule(
    self,
    schedule_id: str,
    default_video_asset: dict,
    name: str | None,
    thumbnail_asset: dict | None,
    time_zone_id: str | None
) -> dict | None:
    """
    Updates an intelligent schedule.

    Args:
        schedule_id (str): The id of the schedule the intelligent schedule is to be updated.
        default_video_asset (dict): The default video asset of the intelligent schedule.
            dict format: {"id": "string", "description": "string"}
        name (str | None): The name of the intelligent schedule.
        thumbnail_asset (dict | None): The thumbnail asset of the intelligent schedule.
            dict format: {"id": "string", "description": "string"}
        time_zone_id (str | None): The time zone id of the intelligent schedule.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}"

    schedule: dict | None = _get_intelligent_schedule(self, schedule_id)

    body: dict = {
        "defaultVideoAsset": default_video_asset or schedule.get("defaultVideoAsset"),
        "name": name or schedule.get("name"),
        "scheduleType": "3",
        "thumbnailAsset": thumbnail_asset or schedule.get("thumbnailAsset"),
        "timeZoneId": time_zone_id or schedule.get("timeZoneId"),
        "id": schedule_id
    }

    return _send_request(self, "Update Intelligent Schedule", api_url, "PUT", None, body)
