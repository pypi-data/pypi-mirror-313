"""
This module gets all lookups from the service API.

Functions:
    _get_lookups: Gets all lookups.
"""

import re

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_lookups(self) -> dict | None:
    """
    Gets all lookups.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = re.sub(r"https:\/\/(.+?)\.", "https://", self.config["serviceApiUrl"])
    api_url: str = f"{api_url}/config/ea1d7060-6291-46b8-9468-135e7b94021b/lookups.json"

    return _send_request(self, "Get lookups", api_url, "GET", None, None)
