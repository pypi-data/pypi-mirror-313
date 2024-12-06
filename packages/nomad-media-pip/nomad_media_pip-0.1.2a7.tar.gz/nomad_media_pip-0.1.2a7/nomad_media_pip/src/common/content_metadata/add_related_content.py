"""
This module is used to add related content.

Functions:
    _add_related_content: Adds related content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _add_related_content(self, content_id: str, related_content_id: str, content_definition: str) -> dict | None:
    """
    Adds related content.

    Args:
        content_id (str): The ID of the content.
        related_content_id (str): The ID of the related content.
        content_definition (str): The content definition.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/related"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/content/related"
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

    return _send_request(self, "add related content", api_url, "POST", None, body)
