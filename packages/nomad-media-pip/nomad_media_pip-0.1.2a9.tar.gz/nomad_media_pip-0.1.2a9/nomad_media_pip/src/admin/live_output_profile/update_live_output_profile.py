"""
This module updates a live output profile.

Functions:
    _update_live_output_profile: Updates a live output profile.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_output_profile.get_live_output_profile import _get_live_output_profile


def _update_live_output_profile(
    self,
    output_id: str,
    name: str | None,
    output_type: str | None,
    enabled: bool | None,
    audio_bitrate: int | None,
    output_stream_key: str | None,
    output_url: str | None,
    secondary_output_stream_key: str | None,
    secondary_output_url: str | None,
    video_bitrate: int | None,
    video_bitrate_mode: str | None,
    video_codec: str | None,
    video_frames_per_second: int | None,
    video_height: int | None,
    video_width: int | None,
) -> dict | None:
    """
    Updates a live output profile.

    Args:
        live_output_id (str): The ID of the live output profile.
        name (str | None): The name of the live output profile.
        output_type (list | None): The type of the live output profile. Default is MediaStore.
            "MediaStore":"ac5146ea-4c01-4278-8c7b-0117f70c0100", Archive":"ac5146ea-4c01-4278-8c7b-0117f70c0200",
            "MediaPackage":"ac5146ea-4c01-4278-8c7b-0117f70c0300", "Rtmp":"ac5146ea-4c01-4278-8c7b-0117f70c0400",
            "S3":"ac5146ea-4c01-4278-8c7b-0117f70c0500", "LiveVodHls":"ac5146ea-4c01-4278-8c7b-0117f70c0600",
            "Rtp":"ac5146ea-4c01-4278-8c7b-0117f70c0700", "RtpFec":"ac5146ea-4c01-4278-8c7b-0117f70c0800"*
            Dict format: {"name": "string", "id": "string"}
        ENABLED (bool | None): Indicates if the live output profile is enabled.
        AUDIO_BITRATE (int | None): The audio bitrate of the live output profile.
        OUTPUT_STREAM_KEY (str | None): The output stream key of the live output profile.
        OUTPUT_URL (str | None): The output URL of the live output profile.
        SECONDARY_OUTPUT_STREAM_KEY (str | None): The secondary output stream key of the live output profile.
        SECONDARY_URL (str | None): The secondary URL of the live output profile.
        VIDEO_BITRATE (int | None): The video bitrate of the live output profile.
        VIDEO_BITRATE_MODE (str | None): The video bitrate mode of the live output profile. The modes are CBR and VBR.
        VIDEO_CODEC (str | None): The video codec of the live output profile. The codecs are H264 and H265.
        VIDEO_FRAMES_PER_SECOND (int | None): The video frames per second of the live output profile.
        VIDEO_HEIGHT (int | None): The video height of the live output profile.
        VIDEO_WIDTH (int | None): The video width of the live output profile.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfile"

    profile_info: dict | None = _get_live_output_profile(self, output_id)

    body: dict = {
        "id": output_id,
        "name": name or profile_info.get("name"),
        "outputType": output_type or profile_info.get("outputType"),
        "enabled": enabled or profile_info.get("enabled"),
        "audioBitrate": audio_bitrate or profile_info.get("audioBitrate"),
        "outputStreamKey": output_stream_key or profile_info.get("outputStreamKey"),
        "outputUrl": output_url or profile_info.get("outputUrl"),
        "secondaryOutputStreamKey": secondary_output_stream_key or profile_info.get("secondaryOutputStreamKey"),
        "secondaryOutputUrl": secondary_output_url or profile_info.get("secondaryOutputUrl"),
        "videoBitrate": video_bitrate or profile_info.get("videoBitrate"),
        "videoBitrateMode": video_bitrate_mode or profile_info.get("videoBitrateMode"),
        "videoCodec": video_codec or profile_info.get("videoCodec"),
        "videoFramesPerSecond": video_frames_per_second or profile_info.get("videoFramesPerSecond"),
        "videoHeight": video_height or profile_info.get("videoHeight"),
        "videoWidth": video_width or profile_info.get("videoWidth")
    }

    return _send_request(self, "Update live output profile", api_url, "PUT", None, body)
