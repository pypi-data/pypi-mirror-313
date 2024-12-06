"""
This module contains the logic to get an notification when asset is shared.

Functions:
    _share_notification: get an notification when asset is shared
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _share_notification(self, share_id: str, nomad_users: list | None, external_users: list | None) -> None:
    """
    Get an notification when asset is shared

    Args:
        share_id (str): The share id of the shareNotification.
        nomad_users (list | None): The nomad users of the shareNotification.
        external_users (list | None): The external users of the shareNotification.

    Returns:
        Unknown Type: If the request succeeds.
    Exceptions:
        InvalidAPITypeException: If the API type is not portal.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/share/{share_id}/notification"

    body: dict = {
        "shareId": share_id,
        "nomadUsers": nomad_users,
        "externalUsers": external_users
    }

    return _send_request(self, "Share Notification", api_url, "POST", None, body)
