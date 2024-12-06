"""
This module is used to wait for a Live Channel to transition to a specific status.

Functions:
    _wait_for_live_channel_status: Waits for a Live Channel to transition to a specific status.
"""

import logging
import time

from nomad_media_pip.src.admin.live_channel.get_live_channel_status import _get_live_channel_status
from nomad_media_pip.src.admin.live_channel.get_live_channel_status_message import _get_live_channel_status_message


def _wait_for_live_channel_status(
    self,
    channel_id: str,
    status_to_wait_for: str,
    timeout: int = 30,
    poll_interval: int = 2
) -> None:
    """
    Waits for a Live Channel to transition to a specific status.

    Args:
        channel_id (str): The ID of the Live Channel to wait for.
        status_to_wait_for (str): The status to wait for.
        timeout (int): The maximum time to wait in seconds.
        poll_interval (int): The time to wait between checks in seconds.

    Returns:
        None
    """

    # Set the starting time
    starting_time: float = time.time()

    # Elapsed time in seconds
    elapsed_time: int = 0

    while elapsed_time < timeout:
        # Get the Live Channel status
        channel_status: str = _get_live_channel_status(self, channel_id)

        # If channel is in STATUS_TO_WAIT_FOR return
        if channel_status == status_to_wait_for:
            # Give feedback to the console
            logging.info("Live Channel [%s] transitioned to status %s", channel_id, status_to_wait_for)
            return

        # Give feedback to the console
        logging.info("Live Channel [%s] current status is %s", channel_id, channel_status)

        # Check for Error status
        if channel_status == "Error":
            # Get the error message
            channel_status_message: str = _get_live_channel_status_message(self, channel_id)

            # Can't continue if Live Channel is in error status
            logging.error("Live Channel [%s] is in [Error] status: %s", channel_id, channel_status_message)
            return

        # Calculate elapsed time in seconds
        elapsed_time: float = time.time() - starting_time

        # Give feedback to the console
        logging.info(
            "Waiting for Live Channel [%s] to transition to status %s ... %s %s",
            channel_id, status_to_wait_for, str(round(elapsed_time)), str(timeout)
        )

        # Check for timeout
        if elapsed_time > timeout:
            break

        # Wait poll interval
        time.sleep(poll_interval)

    logging.error("Waiting for Live Channel [%s] to transition to status %s timed out", channel_id, status_to_wait_for)
