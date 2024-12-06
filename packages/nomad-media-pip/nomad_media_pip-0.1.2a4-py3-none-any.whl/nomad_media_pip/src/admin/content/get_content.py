"""
This module is used to get content by content id and content definition id.

Functions:
    _get_content: Gets content by content id and content definition id.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_content(
    self,
    content_id: str,
    content_definition_id: str,
    is_revision: bool | None
) -> dict | None:
    """
    Gets content by content id and content definition id.

    Args:
        content_id (str): The ID of the content.
        content_definition_id (str): The ID of the content definition.
        is_revision (bool | None): The is revision flag.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/content/{content_id}"
        f"?contentDefinitionId={content_definition_id}"
    )

    params: dict[str: bool] = {
        "isRevision": is_revision
    }

    return _send_request(self, "Get content", api_url, "GET", params, None)
