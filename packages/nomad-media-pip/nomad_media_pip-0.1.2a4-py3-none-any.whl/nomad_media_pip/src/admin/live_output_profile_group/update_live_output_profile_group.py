"""
This module updates the live output profile group.

Functions:
	_update_live_output_profile_group: Updates the live output profile group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_output_profile_group.get_live_output_profile_group import _get_live_output_profile_group


def _update_live_output_profile_group(
    self,
    live_output_profile_group_id: str,
    name: str | None,
    is_enabled: bool | None,
    manifest_type: str | None,
    is_default_group: bool | None,
    live_output_type: list | None,
    archive_live_output_profile: list | None,
    live_output_profiles: list | None
) -> dict | None:
    """
    Updates the live output profile group.

    Args:
        live_output_profile_group_id (str): The ID of the live output profile group to update.
        name (str | None): The name of the live output profile group.
        is_enabled (bool | None): The enabled flag.
        manifest_type (str | None): The manifest type.
        is_default_group (bool | None): The default group flag.
        live_output_type (list | None): The live output type.
        archive_live_output_profile (list | None): The archive live output profile.
        live_output_profiles (list | None): The live output profiles.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfileGroup"

    profile_group_info: dict | None = _get_live_output_profile_group(self, live_output_profile_group_id)

    body: dict = {
        "id": live_output_profile_group_id or profile_group_info.get("id"),
        "name": name or profile_group_info.get("name"),
        "isEnabled": is_enabled or profile_group_info.get("isEnabled"),
        "manifestType": manifest_type or profile_group_info.get("manifestType"),
        "isDefaultGroup": is_default_group or profile_group_info.get("isDefaultGroup"),
        "outputType": live_output_type or profile_group_info.get("outputType"),
        "archiveOutputProfile": archive_live_output_profile or profile_group_info.get("archiveOutputProfile"),
        "outputProfiles": live_output_profiles or profile_group_info.get("outputProfiles")
    }

    return _send_request(self, "Update live output profile group", api_url, "PUT", None, body)
