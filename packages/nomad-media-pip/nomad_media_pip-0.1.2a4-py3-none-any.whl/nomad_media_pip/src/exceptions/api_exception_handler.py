"""
This module contains the _api_exception_handler function, which handles exceptions

Functions:
    _api_exception_handler: Handles exceptions

Returns:
    None: If the request fails or the response cannot be parsed as JSON.
"""

import json
import logging
import requests


def _api_exception_handler(response: requests.Response | None, message: str) -> None:
    """
    Handles exceptions

    Args:
        response (requests.Response): The response object from the server.
        message (str): The error message to be displayed.

    Returns:
        None: If the request fails or the response cannot be parsed as JSON.
    """
    # Set a async default error message
    error: str = "Unknown error occurred"

    # Check if we have a response object and error message
    if response is None:
        # If not response then throw async default error or message
        if message is None or len(message.strip()) == 0:
            logging.error(json.dumps({"error": error}))
        else:
            logging.error(json.dumps({"error": message}))
        return None

    if response.text != "":
        # Response BODY is text
        error: str = response.text.strip()

        # Throw error if valid
        if error and len(error.strip()) > 0:
            try:
                response_val: dict | str = response.json()
                if isinstance(response_val, str):
                    logging.error(json.dumps({"error": f"{response.status_code} - {response_val}"}))
                else:
                    message: str = response_val.get("message", "")
                    error: list = response_val.get("errors", [])

                    log_message: str = [str(response.status_code)]
                    if error:
                        log_message.append(str(error))
                    if message:
                        log_message.append(str(message))
                    log_message = " - ".join(log_message)
                    logging.error(json.dumps({"error": log_message}, indent=4, ensure_ascii=False))
            except json.JSONDecodeError:
                logging.error({"error": f" {response.status_code} - {response.text}"})

    else:
        # Throw message and response status
        logging.error({"error": f"{response.status_code}"})

    return None
