"""
This module is used to add a tag or collection to a content.

Functions:
    _add_tag_or_collection: Adds a tag or collection to a content.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _add_tag_or_collection(
    self,
    tag_type: str,
    content_id: str,
    content_definition: str,
    tag_name: str,
    tag_id: str | None,
    create_new: bool
) -> dict | None:
    """
    Adds a tag or collection to a content.

    Args:
        tag_type (str): Whether to add a tag or collection to the content.
        content_id (str): The ID of the content.
        content_definition (str): The content definition.
        tag_name (str): The name of the tag or collection.
        tag_id (str | None): The ID of the tag or collection.
        create_new (bool): The create new flag.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/{tag_type}/content"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/content/{tag_type}"
    )

    body: dict = {
        "items": [
            {
                "contentDefinition": content_definition,
                "contentId": content_id,
                "name": tag_name,
                "createNew": create_new,
                f"{tag_type}Id": tag_id
            }
        ]
    }

    return _send_request(self, f"Add {tag_type}", api_url, "POST", None, body)
