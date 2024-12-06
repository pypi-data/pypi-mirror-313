"""
This module is used to get all security groups.

Functions:
    _get_security_groups: Gets all security groups.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_security_groups(self) -> dict | None:
    """
    Gets all security groups.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/"
        f"lookup/22?lookupKey=99e8767a-00ba-4758-b9c2-e07b52c47016"
    )

    return _send_request(self, "Get Security Groups", api_url, "GET", None, None)
