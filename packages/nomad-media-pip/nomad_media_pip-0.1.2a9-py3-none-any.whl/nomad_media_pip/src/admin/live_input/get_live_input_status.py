"""
This module gets the live input status from the service API.

Functions:
    _get_live_input_status: Gets the live input status.
"""

from nomad_media_pip.src.admin.live_input.get_live_input import _get_live_input


def _get_live_input_status(self, input_id: str) -> str:
    """
    Gets the live input status.

    Args:
        input_id (str): The ID of the live input to get the status of.

    Returns:
        str: The status of the live input.
    """

    # Get the live INPUT
    input_info: dict | None = _get_live_input(self, input_id)

    # Check if INPUT was found
    if input_info:
        # Return the status of the INPUT
        return input_info["status"]["description"]

    # Input was not found
    return "Deleted"
