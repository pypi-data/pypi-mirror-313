"""
This function deletes a content from the service.

Functions:
    _delete_content: Deletes a content from the service.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_content(self, content_id: str, content_definition_id: str) -> dict | None:
    """
    Deletes a content from the service.

    Args:
        content_id (str): The ID of the content to delete.
        content_definition_id (str): The ID of the content definition to delete.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/content/{content_id}"
        f"?contentDefinitionId={content_definition_id}"
    )

    return _send_request(self, "Deleting content", api_url, "DELETE", None, None)
