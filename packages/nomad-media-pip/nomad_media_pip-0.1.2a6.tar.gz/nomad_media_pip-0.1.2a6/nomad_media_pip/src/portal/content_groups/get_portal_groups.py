"""
This module is used to get all portal groups.

Functions:
    _get_portal_groups: Gets all portal groups.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _get_portal_groups(self, returned_group_names: list[str]) -> dict | None:
    """
    Gets all portal groups.

    Args:
        portal_groups (list[str]): The portal groups to get. The portal groups are
            contentGroups, shared_content_groups, and savedSearches. You can only see a content
            groups if it is shared with you, or if you are the owner of the content group.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/groups"

    body: dict = {
        "returnedGroupNames": returned_group_names
    }

    return _send_request(self, "Get poral groups", api_url, "POST", None, body)
