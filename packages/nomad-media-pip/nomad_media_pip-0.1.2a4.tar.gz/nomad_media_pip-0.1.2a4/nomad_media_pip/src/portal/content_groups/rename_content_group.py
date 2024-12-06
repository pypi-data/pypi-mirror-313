"""
This module is used to rename a content group.

Functions:
    _rename_content_group: Renames a content group.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _rename_content_group(self, content_id: str, name: str) -> dict | None:
    """
    Renames a content group.

    Args:
        content_id (str): The ID of the content group to rename.
        name (str): The new name of the content group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentGroup/{content_id}"

    body: dict = {
        "name": name
    }

    return _send_request(self, "Rename content group", api_url, "PATCH", None, body)
