"""
This module is used to bulk update metadata for content.

Functions:
    _bulk_update_metadata: Bulk updates metadata for content.
"""

import logging

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.common.asset.get_asset_details import _get_asset_details


def _bulk_update_metadata(
    self,
    content_ids: list[str],
    collection_ids: list[str] | None,
    related_content_ids: list[str] | None,
    tag_ids: list[str] | None,
    schema_name: str | None
) -> dict | None:
    """
    Bulk updates metadata for content.

    Args:
        content_ids (list[str]): The IDs of the content to update.
        collection_ids (list[str] | None): The IDs of the collections to update.
        related_content_ids (list[str] | None): The IDs of the related content to update.
        tag_ids (list[str] | None): The IDs of the tags to update.
        schema_name (str | None): The name of the schema to update.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/content/bulk-metadata-update"

    asset_details: dict | None = _get_asset_details(self, content_ids[0])
    if not asset_details:
        logging.error("Failed to get asset details for bulk update metadata.")
        return None

    body: dict = {
        'collections': (
            (collection_ids if collection_ids else []) +
            ([item['id'] for item in asset_details['collections']]
             if 'collections' in asset_details and asset_details['collections']
             else [])
        ),
        'contents': content_ids,
        'relatedContents': (
            (related_content_ids if related_content_ids else []) +
            ([item['id'] for item in asset_details['relatedContents']]
             if 'relatedContents' in asset_details and asset_details['relatedContents']
             else [])
        ),
        'tags': (
            (tag_ids if tag_ids else []) +
            ([item['id'] for item in asset_details['tags']]
             if 'tags' in asset_details and asset_details['tags']
             else [])
        ),
        'schemaName': schema_name
    }

    return _send_request(self, "Bulk update metadata", api_url, "POST", None, body)
