"""
This module contains the function to start workflow.

Functions:
    _start_workflow: Starts workflow.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _start_workflow(self, action_arguments: dict, target_ids: list[str]) -> dict | None:
    """
    Starts workflow.

    Args:
        action_arguments (dict): The action arguments of the start. dict format: { "workflowName": string }.
        target_ids (list[str]): The IDs of the assets to start the workflow for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/startWorkflow"

    body: dict = {
        "actionArguments": action_arguments,
        "targetIds": target_ids
    }

    return _send_request(self, "Start workflow", api_url, "POST", None, body)
