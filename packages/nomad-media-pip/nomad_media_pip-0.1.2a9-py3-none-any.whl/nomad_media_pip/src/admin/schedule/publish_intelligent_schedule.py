"""
This module is used to publish intelligent schedule.

Functions:
    _publish_intelligent_schedule: Publishes intelligent schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _publish_intelligent_schedule(self, schedule_id: str, number_or_locked_days: int) -> dict | None:
    """
    Publishes intelligent schedule.

    Args:
        schedule_id (str): The ID of the schedule.
        number_or_locked_days (int): The number of locked days.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/publish"

    body: dict = {
        "number_of_days": number_or_locked_days
    }

    return _send_request(self, "Publish Intelligent Schedule", api_url, "POST", None, body)
