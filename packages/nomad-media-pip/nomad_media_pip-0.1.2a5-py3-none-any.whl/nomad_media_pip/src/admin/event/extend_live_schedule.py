"""
This module is used to extend the live schedule of an event.

Functions:
    _extend_live_schedule: Extends the live schedule of an event.
"""

from datetime import datetime, timedelta

from nomad_media_pip.src.helpers.send_request import _send_request


def _extend_live_schedule(
    self,
    event_id: str,
    recurring_days: list[str],
    recurring_weeks: int,
    end_date: str | None
) -> None:
    """
    Extends the live schedule of an event.

    Args:
        event_id (str): The ID of the event to extend the live schedule for.
        recurring_days (list[str]): The days of the week the event should recur on.
        recurring_weeks (int): The number of weeks the event should recur for.
        end_date (str): The end date of the recurring event.

    Returns:
        None: If the request succeeds
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveSchedule/content/{event_id}/copy"

    if end_date is None:
        # Calculate the end date based on the recurring weeks
        end_date = (datetime.now() + timedelta(weeks=recurring_weeks)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    body: dict = {
        "recurringDays": recurring_days,
        "recurringWeeks": recurring_weeks,
        "recurringEndDate": end_date,
        "timeZoneOffsetSeconds": int((datetime.now() - datetime.utcnow()).total_seconds())
    }

    _send_request(self, "Extend Live Schedule", api_url, "POST", None, body)
