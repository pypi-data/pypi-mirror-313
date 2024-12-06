"""
This module gets the video tracking from the service API.

Functions:
    _get_video_tracking: Gets the video tracking.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_video_tracking(self, asset_id: str, tracking_event: str, second: int | None) -> dict | None:
    """
    Gets the video tracking.

    Args:
        asset_id (str): The id of the asset.
        tracking_event (str): The tracking event of the asset. The value of tracking
            event's value can be 0-5 with 0 being no tracking event, 1-4 being the progress in quarters,
            i.e 3 meaning it is tracking 3 quarters of the video, and 5 meaning that the tracking is hidden.
        seconds (int | None): The seconds into the video being tracked.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/tracking?assetId={asset_id}"

    params: dict = {
        "event": tracking_event,
        "second": second
    }

    return _send_request(self, "Get video tracking service", api_url, "GET", params, None)
