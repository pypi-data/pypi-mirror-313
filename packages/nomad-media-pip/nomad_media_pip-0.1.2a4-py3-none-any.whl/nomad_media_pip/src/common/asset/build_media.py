"""
This module contains the logic to build media.

Functions:
    _build_media: Builds media.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _build_media(
    self,
    source: list[dict],
    title: str | None,
    tags: list[dict] | None,
    collections: list[dict] | None,
    related_content: list[dict] | None,
    destination_folder_id: str,
    video_bitrate: int | None,
    audio_tracks: list[dict] | None
) -> dict | None:
    """
    Builds a media.

    Args:
        sources (list[dict]): The sources of the media.
            dict format: {"sourceAssetId": "string", "startTimeCode": "string", "endTimeCode": "string"}
        title (str | None): The title of the media.
        tags (list[dict] | None): The tags of the media.
            dict format: {"id": "string", "description": "string"}
        collections (list[dict] | None): The collections of the media.
            dict format: {"id": "string", "description": "string"}
        related_contents (list[dict] | None): The related contents of the media.
            dict format: {"id": "string", "description": "string"}
        destination_folder_id (str): The destination folder ID of the media.
        video_bitrate (int | None): The video bitrate of the media.
        audio_tracks (list[dict] | None): The audio tracks of the media.
            dict format: { "id": "string", "bitRate": "int", "sampleRate": "int", "numChannels": "int",
            "format": "string", "frameRate": "int", "bitDepth": "int", "bitRateMode": "string",
            "durationSeconds": "int"}

    Returns:
        None: If the request is successful.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/build-media"

    body: dict = {
        "source": source,
        "title": title,
        "destinationFolderId": destination_folder_id,
        "tags": tags,
        "collections": collections,
        "relatedContent": related_content,
        "videoBitrate": video_bitrate,
        "audioTracks": audio_tracks
    }

    return _send_request(self, "Build media", api_url, "POST", None, body)
