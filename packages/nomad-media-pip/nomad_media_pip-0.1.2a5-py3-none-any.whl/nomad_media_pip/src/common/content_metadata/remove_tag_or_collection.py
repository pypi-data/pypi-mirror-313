"""
This module contains the function to remove a tag or collection from a content.

Functions:
    _remove_tag_or_collection: Removes a tag or collection from a content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _remove_tag_or_collection(
    self,
    tag_type: str,
    content_id: str,
    content_definition: str,
    tag_id: str
) -> dict | None:
    """
    Removes a tag or collection from a content.

    Args:
        tag_type (str): Whether to remove a tag or collection from the content.
        content_id (str): The ID of the content.
        content_definition (str): The content definition.
        tag_id (str): The ID of the tag or collection.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/{tag_type}/content/delete"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/content/{tag_type}/delete"
    )

    body: dict = {
        "items": [
            {
                "contentDefinition": content_definition,
                "contentId": content_id,
                f"{tag_type}Id": tag_id
            }
        ]
    }

    return _send_request(self, "delete tag or colleciton", api_url, "POST", None, body)
