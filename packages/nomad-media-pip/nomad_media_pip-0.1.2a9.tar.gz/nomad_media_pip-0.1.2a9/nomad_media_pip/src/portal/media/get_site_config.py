"""
This module gets the site config from the service API.

Functions:
    _get_site_config: Gets the site config.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_site_config(self, site_config_record_id: str) -> dict | None:
    """
    Gets the site config.

    Args:
        site_config_record_id (str): The ID of the site config record.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/config/{site_config_record_id}"

    return _send_request(self, "Get Site Config", api_url, "GET", None, None)
