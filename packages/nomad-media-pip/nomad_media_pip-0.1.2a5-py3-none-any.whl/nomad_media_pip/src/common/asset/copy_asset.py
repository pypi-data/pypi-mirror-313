"""
This module contains the logic to copy an asset.

Functions:
    _copy_asset: Copies an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _copy_asset(
    self,
    asset_ids: list,
    destination_folder_id: str,
    batch_action: dict | None,
    content_definition_id: str | None,
    schema_name: str | None,
    resolver_excempt: bool | None,
) -> dict | None:
    """
    Copys an asset.

    Args:
        asset_ids (list): The ids of the asset.
        destination_folder_id (str): The destination folder ID of the asset.
        batch_action (dict | None): The actions to be performed.
            dict format: {"id": "string", "description": "string"}
        content_definition_id (str | None): The content definition ID of the asset.
        schema_name (str | None): The schema name of the asset.
            Note that we convert all incoming keys to lower first char to help with serialization for dict later.
            dict format: {"key": "string", "value": "string"}
        resolver_excempt (boolean | None): The resolver excempt of the asset.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset//copy"

    body: dict = {
        "batchAction": batch_action,
        "contentDefinitionId": content_definition_id,
        "schemaName": schema_name,
        "targetIds": asset_ids,
        "actionArguments": {
            "destinationFolderAssetId": destination_folder_id
        },
        "resolverExempt": resolver_excempt
    }

    return _send_request(self, "Copy asset", api_url, "POST", None, body)
