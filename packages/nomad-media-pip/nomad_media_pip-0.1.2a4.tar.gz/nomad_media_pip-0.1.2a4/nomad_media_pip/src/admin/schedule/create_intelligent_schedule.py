"""
This module creates an intelligent schedule.

Functions:
    _create_intelligent_schedule: Creates an intelligent schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_intelligent_schedule(
    self,
    default_video_asset: dict,
    name: str,
    thumbnail_asset: dict | None,
    time_zone_id: str | None
) -> dict | None:
    """
    Creates an intelligent schedule.

    Args:
        default_video_asset (dict): The default video asset of the schedule.
        name (str): The name of the schedule.
        thumbnail_asset (dict | None): The thumbnail asset of the schedule.
        time_zone_id (str | None): The time zone ID of the schedule.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule"

    body: dict = {
        "defaultVideoAsset": default_video_asset,
        "name": name,
        "scheduleType": "3",
        "thumbnailAsset": thumbnail_asset,
        "timeZoneId": time_zone_id
    }

    return _send_request(self, "Create Intelligent Schedule", api_url, "POST", None, body)
