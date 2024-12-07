"""
This module contains the function to create and update an event.

Functions:
    _create_and_update_event: Creates and updates an event.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _create_and_update_event(
    self,
    content_id: str | None,
    content_definition_id: str,
    name: str | None,
    start_datetime: str,
    end_datetime: str,
    event_type: dict,
    series: dict | None,
    disabled: bool,
    overried_series_properties: bool,
    series_properties: dict | None
) -> dict | None:
    """
    Creates and updates an event.

    Args:
        content_id (str | None): The ID of the content to update.
        content_definition_id (str): The ID of the content definition.
        name (str | None): The name of the event.
        start_datetime (str): The start date and time of the event.
        end_datetime (str): The end date and time of the event.
        event_type (dict): The event type of the event.
        series (dict | None): The series of the event.
        disabled (bool): The disabled flag of the event.
        overried_series_properties (bool): The override series properties flag of the event.
        series_properties (dict | None): The series properties of the event.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    if content_id == "" or content_id is None:
        api_url: str = f"{self.config["serviceApiUrl"]}/api/content/new?contentDefinitionId={content_definition_id}"

        info: dict | None = _send_request(self, "Create Event", api_url, "GET", None, None)
        content_id: str = info["contentId"]

        api_url: str = f"{self.config["serviceApiUrl"]}/api/content/{content_id}"

        if not series_properties or not overried_series_properties:
            series_properties = {}

            series_properties["name"] = name if name else series["description"]
            series_properties["startDateTime"] = start_datetime
            series_properties["endDateTime"] = end_datetime
            series_properties["eventType"] = event_type
            if series:
                series_properties["series"] = series
            series_properties["disabled"] = disabled
            series_properties["overrideSeriesDetails"] = overried_series_properties

            body: dict = {
                "contentId": content_id,
                "contentDefinitionId": content_definition_id,
                "properties": series_properties
            }

        return _send_request(self, "Update Event", api_url, "PUT", None, body)
