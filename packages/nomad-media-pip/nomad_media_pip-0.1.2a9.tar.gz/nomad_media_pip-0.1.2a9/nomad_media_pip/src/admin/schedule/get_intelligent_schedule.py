"""
This module gets the intelligent schedule from the service API.

Functions:
    _get_intelligent_schedule: Gets the intelligent schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_intelligent_schedule(self, schedule_id: str) -> dict | None:
    """
    Gets the intelligent schedule.

    Args:
        schedule_id (str): The ID of the schedule to get the intelligent schedule for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}"

    return _send_request(self, "Get Intelligent Schedule", api_url, "GET", None, None)
