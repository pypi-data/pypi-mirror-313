"""
This module contains the function to register a guest.

Functions:
    _register_guest: Registers a guest.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _register_guest(self, email: str, first_name: str | None, last_name: str | None, password: str) -> dict | None:
    """
    Registers a guest.

    Args:
        email (str): The email of the guest to register.
        first_name (str | None): The first name of the guest to register.
        last_name (str | None): The last name of the guest to register.
        password (str): The password of the guest to register.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/register-guest"

    body: dict = {
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "password": password
    }

    return _send_request(self, "Registering guest", api_url, "POST", None, body)
