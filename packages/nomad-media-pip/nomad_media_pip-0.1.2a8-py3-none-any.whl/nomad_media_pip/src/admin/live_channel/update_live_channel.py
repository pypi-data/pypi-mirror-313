"""
This module contains the function to update live channel.

Functions:
    _update_live_channel: Updates a live channel.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.helpers.slugify import _slugify
from nomad_media_pip.src.admin.live_channel.live_channel_statuses import _LIVE_CHANNEL_STATUSES
from nomad_media_pip.src.admin.live_channel.get_security_groups import _get_security_groups
from nomad_media_pip.src.admin.live_channel.wait_for_live_channel_status import _wait_for_live_channel_status
from nomad_media_pip.src.admin.live_channel.live_channel_types import _LIVE_CHANNEL_TYPES
from nomad_media_pip.src.admin.live_channel.get_live_channel import _get_live_channel


def _update_live_channel(
    self,
    channel_id: str,
    name: str | None,
    thumbnail_image_id: str | None,
    archive_folder_asset_id: str | None,
    enable_high_availability: bool | None,
    enable_live_clipping: bool | None,
    is_secure_output: bool | None,
    output_screenshots: bool | None,
    channel_type: str | None,
    external_url: str | None,
    security_groups: str | None
) -> dict | None:
    """
    Updates a live channel.

    Args:
        live_channel_id (str): The ID of the live channel.
        name (str | None): The name of the live channel.
        thumbnail_image_id (str | None): The thumbnail image ID of the live channel.
        archive_folder_asset_id (str | None): The archive folder asset ID of the live channel.
        enable_high_availability (bool | None): Indicates if the live channel is enabled for high availability.
        enable_live_clipping (bool | None): Indicates if the live channel is enabled for live clipping.
        is_secure_output (bool | None): Indicates if the live channel is secure output.
        is_output_screenshot (bool | None): Indicates if the live channel is output screenshot.
        channel_type (str | None): The type of the live channel. The types are External, IVS, Normal, and Realtime.
        external_service_api_url (str | None): The external service API URL of the live channel.
            Only required if the type is External.
        security_groups (str | None): The security groups of the live channel.
            The security groups are: Content Manager, Everyone, and Guest.

    Returns:
        dict: The information of the live channel.
    """

    live_channel_info: dict | None = _get_live_channel(self, channel_id)

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel"

    # Build the payload BODY
    body: dict | None = live_channel_info

    # Build the payload bodygg
    body: dict | None = live_channel_info

    if name and name != body.get('name'):
        body['name'] = name
        body['routeName'] = _slugify(name)

    if thumbnail_image_id and thumbnail_image_id != body.get('thumbnailImage'):
        body['thumbnailImage'] = {'id': thumbnail_image_id}

    if archive_folder_asset_id and archive_folder_asset_id != body.get('archiveFolderAsset', {}).get('id'):
        body['archiveFolderAsset'] = {'id': archive_folder_asset_id}

    if enable_high_availability is not None and enable_high_availability != body.get('enableHighAvailability'):
        body['enableHighAvailability'] = enable_high_availability

    if enable_live_clipping is not None and enable_live_clipping != body.get('enableLiveClipping'):
        body['enableLiveClipping'] = enable_live_clipping

    if is_secure_output is not None and is_secure_output != body.get('isSecureOutput'):
        body['isSecureOutput'] = is_secure_output

    if output_screenshots is not None and output_screenshots != body.get('outputScreenshots'):
        body['outputScreenshots'] = output_screenshots

    if channel_type and _LIVE_CHANNEL_STATUSES.get(channel_type) != body.get('channel_type', {}).get('id'):
        body['channel_type'] = {'id': _LIVE_CHANNEL_TYPES.get(channel_type)}

    # Set the appropriate fields based on the channel type
    if channel_type == "External":
        if external_url and external_url != body.get('externalUrl'):
            body['externalUrl'] = external_url
    else:
        if external_url and body.get('externalUrl'):
            del body['externalUrl']

    if security_groups:
        nomad_security_groups: dict | None = _get_security_groups(self)

        filtered_security_groups: list[dict[str, str]] = [
            {'description': group['description'], 'id': group['id']}
            for group in nomad_security_groups
            if group['description'] in security_groups
        ]

        if filtered_security_groups != body.get('securityGroups'):
            body['securityGroups'] = filtered_security_groups

    info: dict | None = _send_request(self, "Update Live Channel", api_url, "PUT", None, body)
    _wait_for_live_channel_status(self, info["id"], _LIVE_CHANNEL_STATUSES["Idle"], 120, 2)
    return info
