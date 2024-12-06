"""
This module is used to ping the auth service.

Functions:
    _ping_auth: Pings the auth service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _ping_auth(self, application_id: str | None, user_session_id: str) -> dict | None:
    """
    Pings the auth service.

    Args:
        application_id (str | None): The ID of the application to ping.
        user_session_id (str): The ID of the user session to ping.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/ping/auth"

    body: dict = {
        "userSessionId": user_session_id
    }

    if application_id:
        body["applicationId"] = application_id

    return _send_request(self, "Ping Auth", api_url, "POST", None, body)
