"""
This module contains the logic to updates an asset.

Functions:
    _update_share: updates an asset
"""

import logging

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.portal.share.get_share import _get_share


def _update_share(
    self,
    share_id: str,
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
    Updates an asset

    Args:
        share_id (str ): The share id of the updateShare.
        id (str | None): The id of the updateShare.
        name (str | None): The name of the updateShare.
        shared_contents (list[str] | None): The shared contents of the updateShare.
        shared_duration (dict | None): The shared duration of the updateShare.
        dict format: {"id": "string", "description": "string"}
        shared_permissions (list[dict] | None): The shared permissions of the updateShare.
        dict format: {"id": "string", "description": "string"}
        shared_type (dict | None): The shared type of the updateShare.
        dict format: {"id": "string", "description": "string"}
        shared_status (list[dict] | None): The shared status of the updateShare.
        dict format: {"id": "string", "description": "string"}
        shared_duration_in_hours (int | None): The shared duration in hours of the updateShare.
        shared_link (str | None): The shared link of the updateShare.
        owner_id (str | None): The owner id of the updateShare.
        expiration_date (str | None): The expiration date of the updateShare.

    Returns:
        dict: The JSON response form the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.

    Exceptions:
        InvalidAPITypeException: If the API type is not portal.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/share/{share_id}?"

    share_info: dict | None = _get_share(self, share_id)

    if not share_info:
        logging.error("Failed to get share info for share id: %s", share_id)
        return None

    body: dict = {
        "id": id,
        "name": name or share_info["name"],
        "sharedContents": shared_contents or share_info["sharedContents"],
        "sharedDuration": shared_duration or share_info["sharedDuration"],
        "sharedPermissions": shared_permissions or share_info["sharedPermissions"],
        "sharedType": shared_type or share_info["sharedType"],
        "sharedStatus": shared_status or share_info["sharedStatus"],
        "sharedDurationInHours": shared_duration_in_hours or share_info["sharedDurationInHours"],
        "sharedLink": shared_link or share_info["sharedLink"],
        "ownerId": owner_id or share_info["ownerId"],
        "expirationDate": expiration_date or share_info["expirationDate"]
    }

    return _send_request(self, "Update Share", api_url, "PUT", None, body)
