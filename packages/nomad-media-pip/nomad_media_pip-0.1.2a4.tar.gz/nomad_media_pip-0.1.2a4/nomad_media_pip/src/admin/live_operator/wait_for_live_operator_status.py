"""
This module is used to wait for a Live Operator to transition to a specific status.

Functions:
    _wait_for_live_operator_status: Waits for a Live Operator to transition to a specific status.
"""

import logging
import time

from nomad_media_pip.src.admin.live_operator.get_live_operator import _get_live_operator


def _wait_for_live_operator_status(
    self,
    channel_id: str,
    status_to_wait_for: str,
    timeout: int = 30,
    poll_interval: int = 2
) -> None:
    """
    Waits for a Live Operator to transition to a specific status.

    Args:
        channel_id (str): The ID of the Live Operator.
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
        # Get the Live Operator status
        operator_status: str = _get_live_operator(self, channel_id)["status"]

        # If Live Operator is in STATUS_TO_WAIT_FOR return
        if operator_status == status_to_wait_for:
            # Give feedback to the console
            logging.info("Live Operator [%s] transitioned to status [%s]", channel_id, status_to_wait_for)
            return

        # Give feedback to the console
        logging.info("Live Operator [%s] is in status [%s]", channel_id, operator_status)

        # Calculate elapsed time in seconds
        elapsed_time = time.time() - starting_time

        # Give feedback to the console
        logging.info(
            "Waiting for Live Operator [%s] to transition to status [%s]... [%d] timeout: [%d]",
            channel_id,
            status_to_wait_for,
            round(elapsed_time),
            timeout
        )

        # Check for TIMEOUT
        if elapsed_time > timeout:
            break

        # Wait poll interval
        time.sleep(poll_interval)

    logging.error(
        "Waiting for Live Operator [%s] to transition to status [%s] timed out",
        channel_id,
        status_to_wait_for
    )
