"""
This module is used to create a live output profile.

Functions:
    _create_live_output_profile: Creates a live output profile.
"""

from nomad_media_pip.src.helpers.send_request import _send_request

MAX_RETRIES = 2


def _create_live_output_profile(
    self,
    name: str,
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
    video_width: int | None
) -> dict | None:
    """
    Creates a live output profile.

    Args:
    name (str): The name of the live output profile.
    output_type (list | None): The type of the live output profile. Default is MediaStore.
        "MediaStore":"ac5146ea-4c01-4278-8c7b-0117f70c0100", Archive":"ac5146ea-4c01-4278-8c7b-0117f70c0200",
        "MediaPackage":"ac5146ea-4c01-4278-8c7b-0117f70c0300", "Rtmp":"ac5146ea-4c01-4278-8c7b-0117f70c0400",
        "S3":"ac5146ea-4c01-4278-8c7b-0117f70c0500", "LiveVodHls":"ac5146ea-4c01-4278-8c7b-0117f70c0600",
        "Rtp":"ac5146ea-4c01-4278-8c7b-0117f70c0700", "RtpFec":"ac5146ea-4c01-4278-8c7b-0117f70c0800"*
        Dict format: {"name": "string", "id": "string"}
    enabled (bool | None): Indicates if the live output profile is enabled.
    audio_bitrate (int | None): The audio bitrate of the live output profile.
        The audio bitrate in bytes. For example, 128KB = 128000.
    output_stream_key (str | None): The output stream key of the live output profile.
    output_url (str | None): The output URL of the live output profile.
    secondary_output_stream_key (str | None): The secondary output stream key of the live output profile.
    secondary_url (str | None): The secondary URL of the live output profile.
    video_bitrate (int | None): The video bitrate of the live output profile.
        The video bitrate in bytes. For example, 2mbps = 2048000, validate > 0.
    video_bitrate_mode (str | None): The video bitrate mode of the live output profile. The modes are CBR and VBR.
    video_codec (str | None): The video codec of the live output profile. The codecs are H264 and H265.
    video_frames_per_second (int | None): The video frames per second of the live output profile.
    video_height (int | None): The video height of the live output profile.
    video_width (int | None): The video width of the live output profile.

    Returns:
        dict: The information of the live output profile.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/liveOutputProfile"

    body: dict = {
        "name": name,
        "outputType": output_type,
        "enabled": enabled,
        "audioBitrate": audio_bitrate,
        "outputStreamKey": output_stream_key,
        "outputUrl": output_url,
        "secondaryOutputStreamKey": secondary_output_stream_key,
        "secondaryOutputUrl": secondary_output_url,
        "videoBitrate": video_bitrate,
        "videoBitrateMode": video_bitrate_mode,
        "videoCodec": video_codec,
        "videoFramesPerSecond": video_frames_per_second,
        "videoHeight": video_height,
        "videoWidth": video_width
    }

    return _send_request(self, "Create live output profile", api_url, "POST", None, body)
