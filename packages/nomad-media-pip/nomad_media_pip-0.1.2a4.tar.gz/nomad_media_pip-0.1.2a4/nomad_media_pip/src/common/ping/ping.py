"""
This module is used to ping the service.

Functions:
    _ping: Pings the service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _ping(self, application_id: str | None, user_session_id: str | None) -> dict | None:
    """
    Pings the service.

    Args:
        application_id (str | None): The ID of the application to ping.
        user_session_id (str | None): The ID of the user session to ping.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/ping"

    body: dict = {
        "userSessionId": user_session_id
    }

    if application_id:
        body["applicationId"] = application_id

    return _send_request(self, "Ping", api_url, "POST", None, body)
