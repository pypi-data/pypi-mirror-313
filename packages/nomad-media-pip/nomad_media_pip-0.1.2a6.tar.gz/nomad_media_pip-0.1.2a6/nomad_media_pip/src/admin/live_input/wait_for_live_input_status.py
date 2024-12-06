"""
This module waits for the live input to transition to a specific status.

Functions:
    _wait_for_live_input_status: Waits for the live input to transition to a specific status.
"""

import logging
import time

from nomad_media_pip.src.admin.live_input.get_live_input_status import _get_live_input_status
from nomad_media_pip.src.admin.live_input.get_live_input_status_message import _get_live_input_status_message


def _wait_for_live_input_status(
    self,
    input_id: str,
    status_to_wait_for: str,
    timeout: int = 30,
    poll_interval: int = 2
) -> None:
    """
    Waits for the live input to transition to a specific status.

    Args:
        input_id (str): The ID of the live input.
        status_to_wait_for (str): The status to wait for.
        timeout (int): The maximum time to wait in seconds.
        poll_interval (int): The time to wait between polls in seconds.

    Returns:
        None
    """

    # Set the starting time
    starting_time: float = time.time()

    # Elapsed time in seconds
    elapsed_time: int = 0

    while elapsed_time < timeout:
        # Get the Live Input status
        input_status: str = _get_live_input_status(self, input_id)

        # If Live Input is in STATUS_TO_WAIT_FOR return
        if input_status == status_to_wait_for:
            # Give feedback to the console
            logging.info("Live Input %s transitioned to status %s", str(input_id), status_to_wait_for)
            return

        # Give feedback to the console
        logging.info("Live Input [%s] is in status [%s]", input_id, input_status)

        # Check for Error status
        if input_status == "Error":
            # Get the error message
            input_status_message: str = _get_live_input_status_message(self, input_id)

            # Can't continue if Live Input is in error status
            logging.error("Live Input %s is in Error status: %s", input_id, input_status_message)

        # Calculate elapsed time in seconds
        elapsed_time: float = time.time() - starting_time

        # Give feedback to the console
        logging.info(
            "Waiting for Live Input [%s] to transition to status [%s]... [%s] timeout: [%s]",
            input_id, status_to_wait_for, round(elapsed_time), timeout
        )

        # Check for timeout
        if elapsed_time > timeout:
            break

        # Wait poll interval
        time.sleep(poll_interval)

    logging.error("Waiting for Live Input [%s] to transition to status [%s] timed out", input_id, status_to_wait_for)
