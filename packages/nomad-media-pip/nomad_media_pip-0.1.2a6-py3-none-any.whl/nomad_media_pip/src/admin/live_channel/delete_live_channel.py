"""
This module to delete a Live Channel

Functions:
    _delete_live_channel
"""

import logging

from nomad_media_pip.src.admin.live_channel.get_live_channel_inputs_ids import _get_live_channel_inputs_ids
from nomad_media_pip.src.admin.live_input.delete_live_input import _delete_live_input
from nomad_media_pip.src.helpers.send_request import _send_request

MAX_RETRIES = 2


def _delete_live_channel(self, channel_id: str, delete_inputs: bool | None) -> dict | None:
    """
    Deletes a Live Channel

    Args:
        channel_id (str): The ID of the Live Channel to delete.
        delete_inputs (bool | None): Flag to delete Live Channel Inputs.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel/{channel_id}"

    # If delete Live Inputs then get their IDs
    input_ids = None
    if delete_inputs:
        input_ids: list = _get_live_channel_inputs_ids(self, channel_id)

    if delete_inputs and input_ids and len(input_ids) > 0:
        logging.info("Deleting Channel Inputs...")
        # Loop deleted Live Channel Live Inputs
        for input_id in input_ids:
            # Delete Live Input
            _delete_live_input(self, input_id)

    _send_request(self, "Delete Live Channel", api_url, "DELETE", None, None)
