"""
This module contains the logic to clip an asset.

Functions:
    _clip_asset: Clips an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _clip_asset(
    self,
    asset_id: str,
    start_time_code: str,
    end_time_code: str,
    title: str,
    output_folder_id: str,
    tags: list[dict] | None,
    collections: list[dict] | None,
    related_contents: list[dict] | None,
    video_bitrate: int | None,
    audio_tracks
) -> dict | None:
    """
    Clips an asset.

    Args:
        asset_id (str): The id of the asset.
        start_time_code (str): The start time code of the asset.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str): The end time code of the asset.
            Please use the following format: hh:mm:ss;ff.
        title (str): The title of the asset.
        output_folder_id (str): The output folder ID of the asset.
        tags (list[dict] | None): The tags of the asset.
            dict format: {"id": "string", "description": "string"}
        collections (list[dict] | None): The collections of the asset.
            dict format: {"id": "string", "description": "string"}
        related_contents (list[dict] | None): The related contents of the asset.
            dict format: {"id": "string", "description": "string"}
        video_bitrate (int | None): The video bitrate of the asset.
        audio_tracks (list[dict] | None): The audio tracks of the asset.
            dict format: {"id": "string", "description": "string"}

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/clip"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/clip"
    )

    body: dict = {
        "startTimecode": start_time_code,
        "title": title,
        "outputFolderId": output_folder_id,
        "tags": tags,
        "collections": collections,
        "relatedContent": related_contents,
        "videoBitrate": video_bitrate,
        "audioTracks": audio_tracks
    }

    if end_time_code:
        body["endTimecode"] = end_time_code

    return _send_request(self, "Clip asset", api_url, "POST", None, body)
