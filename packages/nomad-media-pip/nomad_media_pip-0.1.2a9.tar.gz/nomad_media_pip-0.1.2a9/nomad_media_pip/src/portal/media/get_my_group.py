"""
This module gets the group of the user from the service API.

Functions:
    _get_my_group: Gets the group of the user.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_my_group(self, group_id: str) -> dict | None:
    """
    Gets the group of the user.

    Args:
        group_id (str): The ID of the group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/my-group/{group_id}"

    return _send_request(self, "Get My Group", api_url, "GET", None, None)
