"""
This module creates a live input.

Functions:
    _create_live_input: Creates a live input.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.helpers.slugify import _slugify
from nomad_media_pip.src.admin.live_input.live_input_types import _LIVE_INPUT_TYPES
from nomad_media_pip.src.admin.live_input.live_input_statuses import _LIVE_INPUT_STATUSES
from nomad_media_pip.src.admin.live_input.wait_for_live_input_status import _wait_for_live_input_status


def _create_live_input(
    self,
    name: str | None,
    source: str | None,
    input_type: str | None,
    is_standard: bool | None,
    video_asset_id: str | None,
    destinations: list[dict[str, str]] | None,
    sources: list[dict[str, str]] | None
) -> dict | None:
    """
    Creates a live input.

    Args:
        name (str | None): The name of the live input.
        source (str | None): The souce of the live input.
        input_type (str | None): The type of the live input. The types are RTMP_PULL, RTMP_PUSH,
            RTP_PUSH, UDP_PUSH and URL_PULL
        is_standard (bool | None): Indicates if the live input is standard.
        video_asset_id (str | None): The video asset ID of the live input.
        destinations (list[dict] | None): The destinations of the live input. Sources must be URLs and are
            only valid for input types: RTMP_PUSH, URL_PULL, and MP4_FILE.
            dict format: {"ip": "str | None", "port": "str | None", "url": "str | None"}
        sources (list[dict] | None): The sources of the live input. Sources must be URLs and are
            only valid for input types: RTMP_PULL.
            dict format: {"ip": "str | None", "port": "str | None", "url": "str | None"}

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveInput"

    body: dict = {
        "name": name,
        "internalName": _slugify(name),
        "type": {
            "id": _LIVE_INPUT_TYPES[input_type],
            "description": input_type
        }
    }

    # Set the appropriate fields based on the type
    if input_type == "RTMP_PUSH":
        if source:
            body["sourceCidr"] = source
    elif input_type == "RTMP_PULL" or input_type == "RTP_PUSH" or input_type == "URL_PULL":
        if source:
            body["sources"] = [{"url": source}]

    if is_standard:
        body["isStandard"] = is_standard
    if video_asset_id:
        body["videoAsset"] = {"id": video_asset_id}
    if destinations:
        body["destinations"] = destinations
    if sources:
        body["sources"] = sources

    info: dict | None = _send_request(self, "Create Live Input", api_url, "POST", None, body)
    _wait_for_live_input_status(self, info["id"], _LIVE_INPUT_STATUSES["Detached"], 15, 1)
    return info
