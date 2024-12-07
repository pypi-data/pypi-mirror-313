"""
This module contains the logic to create an annotation for an asset.

Functions:
    _create_annotation: Creates an annotation for an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_annotation(
    self,
    asset_id: str,
    start_time_code: str,
    end_time_code: str | None,
    title: str | None,
    summary: str | None,
    description: str | None
) -> dict | None:
    """
    Creates an annotation for an asset.

    Args:
        asset_id (str): The id of the asset.
        start_time_code (str): The start time code of the annotation.
            Please use the following format: hh:mm:ss;ff.
        end_time_code (str | None): The end time code of the annotation.
            Please use the following format: hh:mm:ss;ff.
        title (str | None): The title of the annotation.
        summary (str | None): The summary of the annotation.
        description (str | None): The description of the annotation.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/{asset_id}/annotation"

    body: dict = {
        "startTimecode": start_time_code,
        "endTimecode": end_time_code,
        "properties": {
            "title": title,
            "description": description,
            "summary": summary
        }
    }

    return _send_request(self, "Create annotation", api_url, "POST", None, body)
