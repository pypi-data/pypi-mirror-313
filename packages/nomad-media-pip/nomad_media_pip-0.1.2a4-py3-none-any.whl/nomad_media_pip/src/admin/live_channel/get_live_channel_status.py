"""
This module gets the status of a live channel from the service API.

Functions:
    _get_live_channel_status: Gets the status of a live channel.
"""

from nomad_media_pip.src.admin.live_channel.get_live_channel import _get_live_channel


def _get_live_channel_status(self, channel_id: str) -> str:
    """
    Gets the status of a live channel.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        str: The status of the live channel.
    """

    # Get the live channel
    channel: dict | None = _get_live_channel(self, channel_id)

    # Check if live channel was found
    if channel:
        # Return the status of the live channel
        return channel["status"]["description"]

    # Live channel was not found
    return "Deleted"
