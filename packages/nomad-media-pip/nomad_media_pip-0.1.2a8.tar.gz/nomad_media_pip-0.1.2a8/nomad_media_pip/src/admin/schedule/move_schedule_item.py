"""
This module moves a schedule item in the service API.

Functions:
    _move_schedule_item: Moves a schedule item.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _move_schedule_item(self, schedule_id: str, item_id: str, previous_item: str | None) -> dict | None:
    """
    Moves a schedule item.

    Args:
        schedule_id (str): The ID of the schedule to move the item in.
        item_id (str): The ID of the item to move.
        previous_item (str | None): The ID of the item to move the item after. If None, the item will be moved to the beginning of the schedule.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item/{item_id}/move"

    body: dict = {
        "previous_item": previous_item
    }

    return _send_request(self, "Move Schedule Item", api_url, "POST", None, body)
