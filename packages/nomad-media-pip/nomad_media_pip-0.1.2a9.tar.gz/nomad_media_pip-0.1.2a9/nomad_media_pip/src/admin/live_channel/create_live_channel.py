"""
This module contains the function to create a live channel.

Functions:
    _create_live_channel: Creates a live channel.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.helpers.slugify import _slugify
from nomad_media_pip.src.admin.live_channel.live_channel_types import _LIVE_CHANNEL_TYPES
from nomad_media_pip.src.admin.live_channel.get_security_groups import _get_security_groups


def _create_live_channel(
    self,
    name: str | None,
    thumbnail_image: str | None,
    archive_folder_asset: str | None,
    enable_high_availability: bool | None,
    enable_live_clipping: bool | None,
    is_secure_output: bool | None,
    output_screenshots: bool | None,
    channel_type: str,
    external_url: str | None,
    security_groups: str | None
) -> dict | None:
    """
    Creates a live channel.

    Args:
        name (str | None): The name of the live channel.
        thumbnail_image (str | None): The thumbnail image of the live channel.
        archive_folder_asset (str | None): The archive folder asset of the live channel.
        enable_high_availability (bool | None): The enable high availability flag of the live channel.
        enable_live_clipping (bool | None): The enable live clipping flag of the live channel.
        is_secure_output (bool | None): The is secure output flag of the live channel.
        output_screenshots (bool | None): The output screenshots flag of the live channel.
        channel_type (str): The type of the live channel.
        external_url (str | None): The external URL of the live channel.
        security_groups (str | None): The security groups of the live channel.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveChannel"

    body: dict = {
        "name": name,
        "routeName": _slugify(name),
        "enableHighAvailability": enable_high_availability,
        "enableLiveClipping": enable_live_clipping,
        "isSecureOutput": is_secure_output,
        "outputScreenshots": output_screenshots,
        "type": {"id": _LIVE_CHANNEL_TYPES[channel_type]}
    }

    if thumbnail_image:
        body["thumbnailImage"] = {"id": thumbnail_image}

    if archive_folder_asset:
        body["archiveFolderAsset"] = {"id": archive_folder_asset}

    # Set the appropriate fields based on the channel type
    if channel_type == _LIVE_CHANNEL_TYPES["External"]:
        body["externalUrl"] = external_url

    if security_groups:
        nomad_security_groups: dict | None = _get_security_groups(self)

        body['securityGroups'] = [
            {
                'description': group['description'],
                'id': group['id']
            }
            for group in nomad_security_groups
            if group['description'] in security_groups
        ]

    return _send_request(self, "Create Live Channel", api_url, "POST", None, body)
