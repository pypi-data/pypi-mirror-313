"""
This module is used to invite a guest user to a content.

Functions:
    _guest_invite: Invites a guest user to a content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _guest_invite(
    self,
    content_id: str | None,
    content_definition_id: str | None,
    emails: list[str],
    content_security_attribute: str
) -> dict | None:
    """
    Invites a guest user to a content.

    Args:
        content_id (str | None): The ID of the content to invite the user to.
        content_definition_id (str | None): The ID of the content definition.
        emails (list[str]): The emails of the users to invite.
        content_security_attribute (str): The content security attribute.
            The content security attribute can be "Undefined", "Guest", or "Demo".

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/invite-user"

    body: dict = {
        "contentId": content_id,
        "contentDefinitionId": content_definition_id,
        "userId": self.id,
        "emails": emails,
        "contentSecurityAttribute": content_security_attribute
    }

    return _send_request(self, "Guest invite", api_url, "POST", None, body)
