"""
This module is used to move an asset to a different folder.

Functions:
    _move_asset: Moves an asset to a different folder.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _move_asset(
    self,
    asset_id,
    destination_folder_id,
    name,
    batch_action,
    content_definition_id,
    schema_name,
    resolver_excempt
) -> dict | None:
    """
    Moves an asset to a different folder.

    Args:
        asset_id: The ID of the asset to move.
        destination_folder_id: The ID of the folder to move the asset to.
        name: The name of the asset.
        batch_action: The batch action.
        content_definition_id: The content definition ID.
        schema_name: The schema name.
        resolver_excempt: The resolver excempt.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/{asset_id}/move"

    body: dict = {
        "actionArguments": {
            "destinationFolderAssetId": destination_folder_id
        },
        "targetIds": [asset_id],
        "batchAction": batch_action,
        "contentDefinitionId": content_definition_id,
        "schemaName": schema_name,
        "userId": self.id,
        "resolverExempt": resolver_excempt
    }

    if name is not None:
        body["actionArguments"]["name"] = name

    return _send_request(self, "Move asset", api_url, "POST", None, body)
