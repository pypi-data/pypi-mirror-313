"""
This module stops a schedule from the service API.

Functions:
    _stop_schedule: Stops a schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _stop_schedule(self, schedule_id, force_stop) -> dict | None:
    """
    Stops a schedule.

    Args:
        schedule_id (str): The ID of the schedule to stop.
        force_stop (bool): Whether to force stop the schedule.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    if force_stop is None:
        force_stop = False

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/stop?force={force_stop}"

    return _send_request(self, "Stop Schedule", api_url, "POST", None, None)
