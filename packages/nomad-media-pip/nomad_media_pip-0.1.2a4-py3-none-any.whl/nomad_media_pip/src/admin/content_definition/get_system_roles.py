"""
This module gets the system roles from the service API.

Functions:
    _get_system_roles: Gets the system roles.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_system_roles(self) -> dict | None:
    """
    Gets the system roles.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/lookup/45"

    return _send_request(self, "Get system roles", api_url, "GET", None, None)
