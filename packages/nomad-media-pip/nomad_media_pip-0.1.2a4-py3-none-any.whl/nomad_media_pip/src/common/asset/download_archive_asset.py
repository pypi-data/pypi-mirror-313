"""
This module is used to download archive asset.

Functions:
    _download_archive_asset: Downloads archive asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _download_archive_asset(
    self,
    asset_ids: list[str],
    file_name: str | None,
    download_proxy: bool | None
) -> dict | None:
    """
    Downloads archive asset.

    Args:
        asset_ids (list[str]): The ids of the assets.
        file_name (str | None): The file name of the archive asset. Only use if apiType is admin.
        download_proxy (boolean | None): The download proxy of the archive asset. Only use if apiType is admin.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/asset/download-archive"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/asset/download-archive"
    )

    body: dict = {
        "assetIds": asset_ids
    }

    if self.config["apiType"] == "admin":
        body["fileName"] = file_name
        body["downloadProxy"] = download_proxy

    return _send_request(self, "Download archive asset", api_url, "POST", None, body)
