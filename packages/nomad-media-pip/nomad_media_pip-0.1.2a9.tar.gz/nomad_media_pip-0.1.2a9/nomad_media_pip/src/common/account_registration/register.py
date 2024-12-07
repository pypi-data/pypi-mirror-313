"""
This module contains the logic to register a user.

Functions:
    _register: Registers a user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _register(self, email: str, first_name: str, last_name: str, password: str) -> dict | None:
    """
    Registers a user.

    Args:
        email (str): The email of the user to register.
        first_name (str): The first name of the user to register.
        last_name (str): The last name of the user to register.
        password (str): The password of the user to register.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/register"

    body: dict = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password
    }

    return _send_request(self, "Register user", api_url, "POST", None, body)
