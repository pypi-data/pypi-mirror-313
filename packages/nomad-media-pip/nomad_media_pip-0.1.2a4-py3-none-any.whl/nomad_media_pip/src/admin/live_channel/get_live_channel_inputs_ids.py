"""
This module gets the live channel inputs IDs from the service API.

Functions:
    _get_live_channel_inputs_ids: Gets the live channel inputs IDs.
"""

from nomad_media_pip.src.admin.live_channel.get_live_channel_schedule_events import _get_live_channel_schedule_events


def _get_live_channel_inputs_ids(self, channel_id: str) -> list:
    """
    Gets the live channel inputs IDs.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        list: The array of input IDs
    """

    # Declare empty array for the IDs
    input_ids: list = []

    # Get all the schedule events for the channel
    channel_events: dict | None = _get_live_channel_schedule_events(self, channel_id)

    # If there are schedule events
    if channel_events and len(channel_events) > 0:
        # Loop schedule events
        for schedule_events in channel_events:
            # Check if schedule event is input type
            if schedule_events and "liveInput" in schedule_events:
                if schedule_events["liveInput"] is not None:
                    # If it has a valid lookupId add it to the array
                    if schedule_events["liveInput"]["id"]:
                        input_ids.append(schedule_events["liveInput"]["id"])

    # Return the array of inputs IDs
    return input_ids
