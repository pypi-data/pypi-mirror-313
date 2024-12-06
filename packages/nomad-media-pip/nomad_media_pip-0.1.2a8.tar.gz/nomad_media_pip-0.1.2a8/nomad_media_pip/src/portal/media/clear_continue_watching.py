"""
This module clears the continue watching for a user.

Functions:
    _clear_continue_watching: Clears the continue watching for a user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _clear_continue_watching(self, user_id: str, asset_id: str | None) -> dict | None:
    """
    Clears the continue watching for a user.

    Args:
        user_id (str): The ID of the user to clear the continue watching for.
        asset_id (str): The ID of the asset to clear the continue watching for.
            If no asset id is passed, it clears the markers of all assets.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/clear-watching"

    params: dict = {
        "userId": user_id,
        "assetId": asset_id
    }

    return _send_request(self, "Clear Continue Watching", api_url, "POST", params, None)
