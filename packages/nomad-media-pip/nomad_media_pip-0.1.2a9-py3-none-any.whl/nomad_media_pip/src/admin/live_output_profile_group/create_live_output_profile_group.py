"""
This module creates a live output profile group.

Functions:
	_create_live_output_profile_group: Creates a live output profile group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_live_output_profile_group(
    self,
    name: str,
    is_enabled: bool,
    manifest_type: str,
    is_default_group: bool,
    live_output_type: list,
    archive_live_output_profile: list | None,
    live_output_profiles: list | None
) -> dict | None:
    """
    Creates a live output profile group.

    Args:
        name (str): The name of the live output profile group.
        is_enabled (bool): Indicates if the live output profile group is enabled.
        manifest_type (str): The manifest type of the live output profile group. The types are HLS, DASH, and BOTH.
        is_default_group (bool): Indicates if the live output profile group is the default group.
        live_output_type (list | None): The type of the live output profile. Default is MediaStore.
            "MediaStore":"ac5146ea-4c01-4278-8c7b-0117f70c0100", Archive":"ac5146ea-4c01-4278-8c7b-0117f70c0200",
            "MediaPackage":"ac5146ea-4c01-4278-8c7b-0117f70c0300", "Rtmp":"ac5146ea-4c01-4278-8c7b-0117f70c0400",
            "S3":"ac5146ea-4c01-4278-8c7b-0117f70c0500", "LiveVodHls":"ac5146ea-4c01-4278-8c7b-0117f70c0600",
            "Rtp":"ac5146ea-4c01-4278-8c7b-0117f70c0700", "RtpFec":"ac5146ea-4c01-4278-8c7b-0117f70c0800"*
            Dict format: {"name": "string", "id": "string"}
        live_output_type (list): The type of the live output profile group.
            dict format: {"description": "string", "id": "string"}
        archive_live_output_profile (list | None): The archive live output profile of the live output profile group.
            dict format: {"description": "string", "id": "string"}
        live_output_profiles (list): The live output profile of the live output profile group.

    Returns:
        dict: The JSON response from the server if the request is successful.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfileGroup"

    body: dict = {
        "name": name,
        "enabled": is_enabled,
        "manifestType": manifest_type,
        "isDefaultGroup": is_default_group,
        "outputType": live_output_type,
        "archiveOutputProfile": archive_live_output_profile,
        "outputProfiles": live_output_profiles
    }

    return _send_request(self, "Create live output profile group", api_url, "POST", None, body)
