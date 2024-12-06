"""
This module deletes user content security data from the service API.

Functions:
    _delete_user_content_security_data: Deletes the user content security data.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_user_content_security_data(
    self,
    content_id: str | None,
    content_definition_id: str | None,
    user_id: str | None,
    email: str | None,
    uid: str | None,
    key_name: str | None,
    expiraton_date: str | None
) -> None:
    """
    Deletes the user content security data.

    Args:
        content_id (str | None): The ID of the content to delete the security data for.
        content_definition_id (str | None): The ID of the content definition to delete the security data for.
        user_id (str | None): The ID of the user to delete the security data for.
        email (str | None): The email of the user to delete the security data for.
        uid (str | None): The ID of the security data to delete.
        key_name (str | None): The key name of the security data to delete.
        expiraton_date (str | None): The expiration date of the security data to delete.

    Returns:
        None: If the request succeeds.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/user/userContentSecurity/delete"

    body: dict = {
        "contentId": content_id,
        "contentDefinitionId": content_definition_id,
        "userId": user_id,
        "email": email,
        "id": uid,
        "keyName": key_name,
        "expirationDate": expiraton_date
    }

    _send_request(self, "Delete User Content Security Data", api_url, "POST", None, body)
