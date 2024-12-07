"""
This module deletes the user video tracking data from the service.

Functions:
    _delete_user_video_tracking_data: Deletes the user video tracking data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_video_tracking_data(
    self,
    asset_id: str | None,
    content_id: str | None,
    video_tracking_attribute: str | None,
    user_id: str | None,
    uid: str | None,
    is_first_quartile: bool | None,
    is_midpoint: bool | None,
    is_third_quartile: bool | None,
    is_complete: bool | None,
    is_hidden: bool | None,
    is_live_stream: bool | None,
    max_seconds: float | None,
    last_second: float | None,
    total_seconds: float | None,
    last_beacon_date: str | None,
    key_name: str | None
) -> None:
    """
    Deletes the user video tracking data.

    Args:
        asset_id (str | None): The ID of the asset to delete the video tracking data for.
        content_id (str | None): The ID of the content to delete the video tracking data for.
        video_tracking_attribute (str | None): The video tracking attribute to delete.
        user_id (str | None): The ID of the user to delete the video tracking data for.
        uid (str | None): The ID of the video tracking data to delete.
        is_first_quartile (bool | None): Whether the video tracking data is first quartile.
        is_midpoint (bool | None): Whether the video tracking data is midpoint.
        is_third_quartile (bool | None): Whether the video tracking data is third quartile.
        is_complete (bool | None): Whether the video tracking data is complete.
        is_hidden (bool | None): Whether the video tracking data is hidden.
        is_live_stream (bool | None): Whether the video tracking data is live stream.
        max_seconds (float | None): The maximum seconds of the video tracking data.
        last_second (float | None): The last second of the video tracking data.
        total_seconds (float | None): The total seconds of the video tracking data.
        last_beacon_date (str | None): The last beacon date of the video tracking data.
        key_name (str | None): The key name of the video tracking data.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/userVideoTracking/delete"

    body: dict = {
        "assetId": asset_id,
        "contentId": content_id,
        "videoTrackingAttribute": video_tracking_attribute,
        "userId": user_id,
        "id": uid,
        "isFirstQuartile": is_first_quartile,
        "isMidpoint": is_midpoint,
        "isThirdQuartile": is_third_quartile,
        "isComplete": is_complete,
        "isHidden": is_hidden,
        "isLiveStream": is_live_stream,
        "maxSeconds": max_seconds,
        "lastSecond": last_second,
        "totalSeconds": total_seconds,
        "lastBeaconDate": last_beacon_date,
        "keyName": key_name
    }

    _send_request(self, "Delete User Video Tracking Data", api_url, "POST", None, body)
