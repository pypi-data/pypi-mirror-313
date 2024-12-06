"""
This module gets the user session from the service API.

Functions:
    _get_user_session: Gets the user session.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_user_session(self, user_id: str | None) -> dict | None:
    """
    Gets the user session.

    Args:
        user_id (str | None): The ID of the user to get the session for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/user-session/{user_id}"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/user-session/{user_id}"
    )

    return _send_request(self, "Get User Session", api_url, "GET", None, None)
