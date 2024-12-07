"""
This module deletes a schedule item from the service.

Functions:
    _delete_schedule_item: Deletes a schedule item from the service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_schedule_item(self, schedule_id: str, item_id: str) -> None:
    """
    Deletes a schedule item from the service.

    Args:
        schedule_id (str): The ID of the schedule to delete the item from.
        item_id (str): The ID of the item to delete from the schedule.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/item/{item_id}"

    _send_request(self, "Delete Schedule Item", api_url, "DELETE", None, None)
