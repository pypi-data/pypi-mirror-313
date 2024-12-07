"""
This module is used to delete related content.

Functions:
    _delete_related_content: Deletes related content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_related_content(self, content_id: str, related_content_id: str, content_definition: str) -> dict | None:
    """
    Deletes related content.

    Args:
        content_id (str): The ID of the content.
        related_content_id (str): The ID of the related content.
        content_definition (str): The content definition of the content.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/related/delete"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/content/related/delete"
    )

    body: dict = {
        "items": [
            {
                "contentDefinition": content_definition,
                "contentId": content_id,
                "relatedContentId": related_content_id
            }
        ]
    }

    return _send_request(self, "delete related content", api_url, "POST", None, body)
