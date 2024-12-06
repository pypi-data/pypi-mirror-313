"""
This module gets the schedule items from the service API.

Functions:
    _get_schedule_items: Gets the schedule items.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_schedule_items(self, schedule_id: str) -> dict | None:
    """
    Gets the schedule items.

    Args:
        schedule_id (str): The ID of the schedule to get the items for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/items"

    return _send_request(self, "Get Schedule Items", api_url, "GET", None, None)
