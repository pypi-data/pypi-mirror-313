"""
This module contains the function to create a form in the Nomad Media Portal.

Functions:
    _create_form: Creates a form.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_form(self, content_definition_id: str, form_info: dict) -> dict | None:
    """
    Creates a form.

    Args:
        content_definition_id (str): The ID of the content definition to create the form for.
        form_info (dict): The form information to create the form with.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/media/form/{content_definition_id}"

    body: dict = form_info

    return _send_request(self, "Forms", api_url, "POST", None, body)
