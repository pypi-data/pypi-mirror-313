"""
This module starts a broadcast.

Functions:
    _start_broadcast: Starts a broadcast.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_operator.wait_for_live_operator_status import _wait_for_live_operator_status


def _start_broadcast(
    self,
    channel_id: str,
    preroll_asset_id: str | None,
    postroll_asset_id: str | None,
    live_input_id: str | None,
    related_content_ids: list[str] | None,
    tag_ids: list[str] | None
) -> dict | None:
    """
    Starts a broadcast.

    Args:
        channel_id (str): The ID of the channel to start the broadcast.
        preroll_asset_id (str): The ID of the preroll asset.
        postroll_asset_id (str): The ID of the postroll asset.
        live_input_id (str): The ID of the live input.
        related_content_ids (list[str]): The IDs of the related content.
        tag_ids (list[str]): The IDs of the tags.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator/start"

    body: dict[str, str] = {
        "id": channel_id
    }

    if live_input_id:
        body["liveInput"] = {"id": live_input_id}
    if preroll_asset_id:
        body["prerollAsset"] = {"id": preroll_asset_id}
    if postroll_asset_id:
        body["postrollAsset"] = {"id": postroll_asset_id}

    if related_content_ids and isinstance(related_content_ids, list) and len(related_content_ids) > 0:
        body["relatedContent"] = [{"id": id} for id in related_content_ids]

    if tag_ids and isinstance(tag_ids, list) and len(tag_ids) > 0:
        body["tags"] = [{"id": id} for id in tag_ids]

    info: dict | None = _send_request(self, "Start Broadcast", api_url, "POST", body, None)
    _wait_for_live_operator_status(self, channel_id, "Running", 1200, 20)
    return info
