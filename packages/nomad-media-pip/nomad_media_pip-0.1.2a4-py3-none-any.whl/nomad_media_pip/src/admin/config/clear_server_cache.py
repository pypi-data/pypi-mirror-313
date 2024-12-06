"""
Clear server cache

Functions:
    _clear_server_cache: Clears the server cache.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _clear_server_cache(self) -> None:
    """
    Clears the server cache.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/config/clearServerCache"

    _send_request(self, "Clear server cache", api_url, "POST", None, None)
