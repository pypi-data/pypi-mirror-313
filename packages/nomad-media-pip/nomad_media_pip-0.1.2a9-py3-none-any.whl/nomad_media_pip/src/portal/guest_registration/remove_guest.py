"""
This module contains the function to remove a guest from a content.

Functions:
    _remove_guest: Removes a guest from a content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _remove_guest(
    self,
    content_id: str | None,
    content_definition_id: str | None,
    emails: list[str],
    content_security_attribute: str
) -> dict | None:
    """
    Removes a guest from a content.

    Args:
        content_id (str | None): The ID of the content to remove the user from.
        content_definition_id (str | None): The ID of the content definition.
        emails (list[str]): The emails of the users to remove.
        content_security_attribute (str): The content security attribute.
            The content security attribute can be "Undefined", "Guest", or "Demo".

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/remove-user"

    body: dict = {
        "contentId": content_id,
        "contentDefinitionId": content_definition_id,
        "userId": self.id,
        "emails": emails,
        "contentSecurityAttribute": content_security_attribute
    }

    return _send_request(self, "Removing Guest", api_url, "POST", None, body)
