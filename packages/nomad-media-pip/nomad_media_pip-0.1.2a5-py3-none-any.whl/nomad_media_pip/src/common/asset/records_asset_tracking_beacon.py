"""
This module is used to record asset tracking beacon.

Functions:
    _records_asset_tracking_beacon: Records asset tracking beacon.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _records_asset_tracking_beacon(
    self,
    asset_id: str,
    tracking_event: str,
    live_channel_id: str,
    content_id: str | None,
    second: int
) -> None:
    """
    Records asset tracking beacon.

    Args:
        asset_id (str): The ID of the asset to record the tracking beacon for.
        tracking_event (str): The tracking event to record.
            Enum: "Progress", "FirstQuartile", "Midpoint", "ThirdQuartile", "Complete", "Hide", "LiveStream"
        live_channel_id (str): The ID of the live channel.
        content_id (str | None): The ID of the content.
        second (int): The second to record the tracking beacon at.

    Returns:
        None: If the request succeedes
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/tracking"

    params: dict = {
        "trackingEvent": tracking_event,
        "assetId": asset_id,
        "liveChannelId": live_channel_id,
        "contentId": content_id,
        "second": second
    }

    return _send_request(self, "Record asset tracking beacon", api_url, "GET", params, None)
