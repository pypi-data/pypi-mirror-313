"""
This module contains the logic to share an asset.

Functions:
    _share: share an asset
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _share(
    self,
    id: str | None,
    name: str | None,
    shared_contents: list[str] | None,
    shared_duration: dict | None,
    shared_permissions: list[dict] | None,
    shared_type: dict | None,
    shared_status: list[dict] | None,
    shared_duration_in_hours: int | None,
    shared_link: str | None,
    owner_id: str | None,
    expiration_date: str | None
) -> dict | None:
    """
    Share an asset

    Args:
        id (str | None): The id of the share.
        name (str | None): The name of the share.
        shared_contents (list[str] | None): The shared contents of the share.
        shared_duration (dict | None): The shared duration of the share.
        dict format: {"id": "string", "description": "string"}
        shared_permissions (list[dict] | None): The shared permissions of the share.
        dict format: {"id": "string", "description": "string"}
        shared_type (dict | None): The shared type of the share.
        dict format: {"id": "string", "description": "string"}
        shared_status (list[dict] | None): The shared status of the share.
        dict format: {"id": "string", "description": "string"}
        shared_duration_in_hours (int | None): The shared duration in hours of the share.
        shared_link (str | None): The shared link of the share.
        owner_id (str | None): The owner id of the share.
        expiration_date (str | None): The expiration date of the share.

    Returns:
        dict: The JSON response form the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.

    Exceptions:
        InvalidAPITypeException: If the API type is not portal.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/share"

    body: dict = {
        "id": id,
        "name": name,
        "sharedContents": shared_contents,
        "sharedDuration": shared_duration,
        "sharedPermissions": shared_permissions,
        "sharedType": shared_type,
        "sharedStatus": shared_status,
        "sharedDurationInHours": shared_duration_in_hours,
        "sharedLink": shared_link,
        "ownerId": owner_id,
        "expirationDate": expiration_date
    }

    return _send_request(self, "Share", api_url, "POST", None, body)
