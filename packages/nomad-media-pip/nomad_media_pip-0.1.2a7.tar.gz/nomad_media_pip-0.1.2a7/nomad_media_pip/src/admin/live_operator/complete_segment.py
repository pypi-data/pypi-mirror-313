"""
This module contains the function to complete segment.

Functions:
    _complete_segment: Completes segment.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _complete_segment(
    self,
    channel_id: str,
    related_content_ids: list[str] | None,
    tag_ids: list[str] | None
) -> dict | None:
    """
    Completes segment.

    Args:
        channel_id (str): The ID of the channel to complete the segment.
        related_content_ids (list[str]): The IDs of the related content.
        tag_ids (list[str]): The IDs of the tags.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/liveOperator/{channel_id}/completeSegment"

    body: dict[str, str] = {
        "liveOperatorId": channel_id,
    }

    if related_content_ids and isinstance(related_content_ids, list) and len(related_content_ids) > 0:
        body["relatedContent"] = [{"id": id} for id in related_content_ids]

    if tag_ids and isinstance(tag_ids, list) and len(tag_ids) > 0:
        body["tags"] = [{"id": id} for id in related_content_ids]

    return _send_request(self, "Complete Segment", api_url, "POST", body, None)
