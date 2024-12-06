"""
This module contains the implementation of the multi-threaded upload function.

Functions:
    _multi_thread_upload: Uploads parts of a file in multiple threads.
"""

import logging
import threading
import time

from nomad_media_pip.src.admin.asset_upload.upload_thread import _upload_thread


def _multi_thread_upload(self, file: str, start_upload_info: dict) -> None:
    """
    Uploads parts of a file in multiple threads.

    Args:
        file (str): The full or relative path of the file.
        start_upload_info (dict): The response from the start upload method call.

    Returns:
        None: If the upload is successful.
    """

    parts: dict = start_upload_info["parts"]
    total_parts: int = len(parts)
    max_active_workers = 8
    max_workers: int = min(total_parts, max_active_workers)
    max_retries = 5

    idx = 0
    worker_count: dict[str, int] = {"value": 0}
    threads: list = []
    while idx < total_parts:
        # Loop while available workers
        while (worker_count["value"] < max_workers) and (idx < total_parts):
            for _ in range(max_retries):
                try:
                    thread = threading.Thread(
                        target=_upload_thread,
                        args=(self, file, parts[idx], worker_count)
                    )
                    threads.append(thread)
                    thread.start()

                    idx += 1
                    worker_count["value"] += 1

                    if idx >= total_parts:
                        break
                except (threading.ThreadError, RuntimeError) as e:
                    logging.error("Error: %s. Retrying...", e)
                else:
                    break

        while worker_count["value"] == max_workers:
            time.sleep(20)

    for thread in threads:
        thread.join()

    while True:
        if worker_count["value"] == 0:
            break
        time.sleep(20)
