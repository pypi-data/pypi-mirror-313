"""
This module starts a schedule.

Functions:
    _start_schedule: Starts a schedule.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _start_schedule(self, schedule_id: str, skip_cleanup_on_failure: bool | None) -> dict | None:
    """
    Starts a schedule.

    Args:
        schedule_id (str): The ID of the schedule to start.
        skip_cleanup_on_failure (bool | None): The skip cleanup on failure flag.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    if skip_cleanup_on_failure is None:
        skip_cleanup_on_failure = False

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/schedule/{schedule_id}/"
        f"start?skipCleanupOnFailure={skip_cleanup_on_failure}"
    )

    return _send_request(self, "Start Schedule", api_url, "POST", None, None)
