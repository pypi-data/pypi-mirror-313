"""
This module gets the live input status message from the service API.

Functions:
    _get_live_input_status_message: Gets the live input status message.
"""

from nomad_media_pip.src.admin.live_input.get_live_input import _get_live_input


def _get_live_input_status_message(self, input_id: str) -> str:
    # Get the live input
    input_info: dict | None = _get_live_input(self, input_id)

    # Check if input was found
    if input_info:
        # Check if there is status message
        if input_info["statusMessage"] and input_info["statusMessage"]:
            # Return input status message
            return input_info["statusMessage"]

    # There is no status message
    return ""
