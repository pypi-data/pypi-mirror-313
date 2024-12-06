"""
This module is used to get the configuration from the service.

Functions:
    _get_config: Gets the configuration from the service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_config(self, config_type: int) -> dict | None:
    """
    Gets the configuration from the service.

    Args:
        config_type (int): The type of config to get. 1 - Admin, 2 - Lambda, 3 - Groundtruth

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/config?configType={config_type}"

    return _send_request(self, "Get Config", api_url, "GET", None, None)
