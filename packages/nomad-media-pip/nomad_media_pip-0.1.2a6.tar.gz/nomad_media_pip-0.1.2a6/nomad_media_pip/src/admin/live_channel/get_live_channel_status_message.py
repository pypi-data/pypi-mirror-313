"""
This module gets the status message for a live channel from the service API.

Functions:
    _get_live_channel_status_message: Gets the status message for a live channel.
"""

from nomad_media_pip.src.admin.live_channel.get_live_channel import _get_live_channel


def _get_live_channel_status_message(self, channel_id: str) -> str:
    """
    Gets the status message for a live channel.

    Args:
        channel_id (str): The ID of the live channel.

    Returns:
        str: The status message for the live channel.
    """

    # Get the live channel
    channel = _get_live_channel(self, channel_id)

    # Check if channel was found
    if channel:
        # Check if there are status messages
        if channel["statusMessages"]:
            # Return the first status message
            return channel["statusMessage"]

    # There are no status messages
    return ""
