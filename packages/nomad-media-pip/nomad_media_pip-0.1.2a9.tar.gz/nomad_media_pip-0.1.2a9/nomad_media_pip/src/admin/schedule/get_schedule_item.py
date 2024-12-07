"""
This module gets the schedule item from the service API.

Functions:
    _get_schedule_item: Gets the schedule item.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_schedule_item(self, schedule_id: str, item_id: str) -> dict | None:
    """
    Gets the schedule item.

    Args:
        schedule_id (str): The ID of the schedule to get the item for.
        item_id (str): The ID of the item to get.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item/{item_id}"

    return _send_request(self, "Get Schedule Item", api_url, "GET", None, None)
