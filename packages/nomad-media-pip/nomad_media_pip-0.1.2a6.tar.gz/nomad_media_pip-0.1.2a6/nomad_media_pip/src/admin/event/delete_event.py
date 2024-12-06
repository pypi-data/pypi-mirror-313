"""
This module contains the function to delete an event.

Functions:
    _delete_event: Deletes an event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _delete_event(self, content_id: str, content_definition_id: str) -> None:
    """
    Deletes an event.

    Args:
        content_id (str): The ID of the event to delete.
        content_definition_id (str): The ID of the content definition.

    Returns:
        None: If the request succeeds
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/content/{content_id}"
        f"?contentDefinitionId={content_definition_id}"
    )

    _send_request(self, "Delete Event", api_url, "DELETE", None, None)
