"""
This module deletes an intelligent schedule from the service.

Functions:
    _delete_intelligent_schedule: Deletes an intelligent schedule from the service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_intelligent_schedule(self, schedule_id: str) -> None:
    """
    Deletes an intelligent schedule from the service.

    Args:
        schedule_id (str): The ID of the intelligent schedule to delete.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}"

    _send_request(self, "Delete Intelligent Schedule", api_url, "DELETE", None, None)
