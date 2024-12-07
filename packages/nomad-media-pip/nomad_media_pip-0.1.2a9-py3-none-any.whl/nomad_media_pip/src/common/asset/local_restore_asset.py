"""
This module is used to restore an asset to a local path.

Functions:
    _local_restore_asset: Restores an asset to a local path.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _local_restore_asset(self, asset_id: str, profile: str | None) -> dict | None:
    """
    Restores an asset to a local path.

    Args:
        asset_id (str): The ID of the asset to restore.
        profile (str | None): The profile to restore the asset with.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/localRestore"

    body: dict = {
        "profile": profile
    }

    return _send_request(self, "Local restore asset", api_url, "POST", None, body)
