"""
Method to clip a live channel.

Functions:
    _clip_live_channel
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _clip_live_channel(
    self,
    channel_id: str,
    start_time_code: str | None,
    end_time_code: str | None,
    title: str | None,
    output_folder_id: str,
    tags: list[dict],
    collections: list[dict],
    related_contents: list[dict],
    video_bitrate: int | None,
    audio_tracks: list[dict] | None
) -> dict | None:
    """
    Clips a live channel.

    Args:
        channel_id (str): The ID of the live channel to clip.
        start_time_code (str | None): The start time code of the clip.
        end_time_code (str | None): The end time code of the clip.
        title (str | None): The title of the clip.
        output_folder_id (str): The ID of the output folder.
        tags (list[dict]): The tags of the clip.
        collections (list[dict]): The collections of the clip.
        related_contents (list[dict]): The related contents of the clip.
        video_bitrate (int | None): The video bitrate of the clip.
        audio_tracks (list[dict] | None): The audio tracks of the clip.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config['serviceApiUrl']}/api/liveChannel/{channel_id}/clip"

    body: dict = {
        "startTimeCode": start_time_code,
        "endTimeCode": end_time_code,
        "title": title,
        "outputFolderId": output_folder_id,
        "tags": tags,
        "collections": collections,
        "relatedContent": related_contents,
        "videoBitrate": video_bitrate,
        "audioTracks": audio_tracks
    }

    return _send_request(self, "Clip Live Channel", api_url, "POST", None, body)
