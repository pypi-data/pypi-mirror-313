"""
This module gets the schedule preview from the service API.

Functions:
    _get_schedule_preview: Gets the schedule preview.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_schedule_preview(self, schedule_id: str) -> dict | None:
    """
    Gets the schedule preview.

    Args:
        schedule_id (str): The ID of the schedule to get the preview for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/preview"

    return _send_request(self, "Get Schedule Preview", api_url, "GET", None, None)
