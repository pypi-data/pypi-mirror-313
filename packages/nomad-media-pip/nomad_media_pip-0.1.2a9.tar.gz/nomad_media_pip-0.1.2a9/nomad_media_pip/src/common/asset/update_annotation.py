"""
This module contains the logic to update an annotation.

Functions:
    _update_annotation: Updates an annotation.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.common.asset.get_annotations import _get_annotations


def _update_annotation(
    self,
    asset_id: str,
    annotation_id: str,
    start_time_code: str | None,
    end_time_code: str | None,
    title: str | None,
    summary: str | None,
    description: str | None
) -> dict | None:
    """
    Updates an annotation.

    Args:
        asset_id (str): The ID of the asset containing the annotation.
        annotation_id (str): The ID of the annotation to update.
        start_time_code (str | None): The start time code of the annotation.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str | None): The end time code of the annotation.
            Please use the following format: hh:mm:ss;ff
        title (str | None): The title of the annotation.
        summary (str | None): The summary of the annotation.
        description (str | None): The description of the annotation.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/annotation/{annotation_id}"

    asset_annotations: dict | None = _get_annotations(self, asset_id)
    annotation: dict | None = next(
        (
            annotation for annotation in asset_annotations if annotation["id"] == annotation_id
        ), None
    )

    body: dict = {
        "id": annotation_id,
        "startTimeCode": start_time_code or annotation.get("startTimeCode"),
        "endTimeCode": end_time_code or annotation.get("endTimeCode"),
        "properties": {
            "title": title or annotation.get("properties").get("title"),
            "summary": summary or annotation.get("properties").get("summary"),
            "description": description or annotation.get("properties").get("description"),
        }
    }

    return _send_request(self, "Update annotation", api_url, "PUT", None, body)
