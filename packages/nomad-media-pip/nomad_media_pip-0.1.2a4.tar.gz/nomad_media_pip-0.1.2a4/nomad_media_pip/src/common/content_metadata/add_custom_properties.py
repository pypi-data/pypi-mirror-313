"""
This module is used to add custom properties to an asset.

Functions:
    _add_custom_properties: Adds custom properties to an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _add_custom_properties(
    self,
    content_id: str,
    name: str | None,
    date: str | None,
    custom_properties: dict
) -> dict | None:
    """
    Adds custom properties to an asset.

    Args:
        content_id (str): The ID of the asset to add custom properties to.
        name (str | None): The display name of the asset.
        date (str | None): The display date of the asset.
        custom_properties (dict): The custom properties of the asset.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{content_id}"

    body: dict = {}

    if name:
        body["displayName"] = name
    if date:
        body["displayDate"] = date
    if custom_properties:
        body["customProperties"] = custom_properties

    return _send_request(self, "Add Custom Properties", api_url, "PATCH", None, body)
