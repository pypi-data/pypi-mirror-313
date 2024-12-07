"""
This module clears the watchlist of a user.

Functions:
    _clear_watchlist: Clears the watchlist of a user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _clear_watchlist(self, user_id: str) -> dict | None:
    """
    Clears the watchlist of a user.

    Args:
        user_id (str): The ID of the user to clear the watchlist for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/clear-watching?userId={user_id}"

    return _send_request(self, "Clear Watchlist", api_url, "POST", None, None)
