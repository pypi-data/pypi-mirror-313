"""
This module is used to add live schedule to an event.

Functions:
    _add_live_schedule_to_event: Adds live schedule to an event.
"""


from nomad_media_pip.src.helpers.send_request import _send_request


def _add_live_schedule_to_event(
    self,
    event_id: str,
    slate_video: dict | None,
    preroll_video: dict | None,
    postroll_video: dict | None,
    is_secure_output: bool | None,
    archive_folder_asset: dict | None,
    primary_live_input: dict | None,
    backup_live_input: dict | None,
    primary_livestream_input_url: dict | None,
    backup_livestream_input_url: dict | None,
    external_output_profiles: list[dict] | None,
    status: dict | None,
    status_message: str | None,
    live_channel: dict | None,
    override_settings: dict | None,
    output_profile
) -> None:
    """
    Adds live schedule to an event.

    Args:
        event_id (str): The ID of the event to add the live schedule to.
        slate_video (dict | None): The slate video ID of the event. Format: {"id": string, "description": string }
        preroll_video (dict | None): The preroll video of the event. Format: {"id": string, "description": string }
        postroll_video (dict | None): The postroll video of the event. Format: {"id": string, "description": string }
        is_secure_output (bool | None): Whether the event is secure output.
        archive_folder (dict | None): The archive folder of the event. Format: { id: string, description: string }
        primary_live_input (dict | None): The live input A ID of the event. Format: { id: string, description: string }
        backup_live_input (dict | None): The live input B ID of the event. Format: { id: string, description: string }
        primary_livestream_input_url (str | None): The primary live stream URL of the event.
        backup_livestream_input_url (str | None): The backup live stream URL of the event.
        external_output_profiles (list[dict] | None): The external output profiles of the event.
        status (dict | None): The status of the event.
        status_message (str | None): The status message of the event.
        live_channel (dict | None): The live channel of the event.
        override_settings (dict | None): The override settings of the event.
        output_profile (dict | None): The output profile of the event.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveSchedule"

    body: dict = {
        "contentId": event_id,
        "slateVideo": slate_video,
        "prerollVideo": preroll_video,
        "postrollVideo": postroll_video,
        "isSecureOutput": is_secure_output,
        "archiveFolderAsset": archive_folder_asset,
        "primaryLiveInput": primary_live_input,
        "backupLiveInput": backup_live_input,
        "primaryLivestreamInputUrl": primary_livestream_input_url,
        "backupLivestreamInputUrl": backup_livestream_input_url,
        "externalOutputProfiles": external_output_profiles,
        "status": status,
        "statusMessage": status_message,
        "liveChannel": live_channel,
        "overrideSettings": override_settings,
        "outputProfile": output_profile
    }

    _send_request(self, "Add Live Schedule To Event", api_url, "POST", None, body)
