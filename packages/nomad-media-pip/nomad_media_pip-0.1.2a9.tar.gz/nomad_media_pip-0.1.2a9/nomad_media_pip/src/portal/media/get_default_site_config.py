from nomad_media_pip.src.helpers.send_request import _send_request


def _get_default_site_config(self) -> dict | None:
    """
    Gets the default site config.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/config"

    return _send_request(self, "Get Default Site Config", api_url, "GET", None, None)
