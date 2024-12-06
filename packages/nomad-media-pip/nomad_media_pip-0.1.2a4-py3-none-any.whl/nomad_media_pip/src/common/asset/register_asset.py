"""
This module contains the logic to register an asset in the Nomad Media Service.

Functions:
    _register_asset: Registers an asset.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _register_asset(
    self,
    asset_id: str | None,
    parent_id: str | None,
    display_object_key: str | None,
    bucket_name: str,
    object_key: str,
    etag: str,
    tags: list[str] | None,
    collections: list[str] | None,
    related_contents: list[str] | None,
    sequencer: str | None,
    asset_status: str | None,
    storage_class: str | None,
    asset_type: str | None,
    content_length: int | None,
    storage_event_name: str | None,
    created_date: str | None,
    storage_source_ip_address: str | None,
    start_media_processor: bool | None,
    delete_missing_asset: bool | None
) -> dict | None:
    """
    Registers an asset.

    Args:
        asset_id (str | None): The ID of the asset to register.
        parent_id (str | None): The parent ID of the asset.
        display_object_key (str | None): The display object key of the asset.
        bucket_name (str): The bucket name of the asset.
        object_key (str): The object key of the asset.
        etag (str): The etag of the asset.
        tags (list[str] | None): The tags of the asset.
        collections (list[str] | None): The collections of the asset.
        related_contents (list[str] | None): The related contents of the asset.
        sequencer (str | None): The sequencer of the asset.
        asset_status (str | None): The asset status of the register.
            Enum: "Available", "Renaming", "Copying", "Restoring", "Registering", "Uploading",
            "Archiving", "Archived", "PendingArchive", "PendingRestore", "Restored", "Deleting",
            "Moving", "SlugReplaced", "Updating", "Error", "Assembling", "Clipping", "Placeholder",
            "Creating"
        storage_class (str | None): The storage class of the register.
            Enum: "Standard", "ReducedRedundancy", "Glacier", "StandardInfrequentAccess",
            "OneZoneInfrequentAccess", "IntelligentTiering", "DeepArchive", "GlacierInstanctRetrival",
            "Outposts"
        asset_type (str | None): The asset type of the register.
            Enum: "Folder", "File", "Bucket"
        content_length (int | None): The content length of the asset.
        storage_event_name (str | None): The storage event name of the asset.
        created_date (str | None): The created date of the asset.
        storage_source_ip_address (str | None): The storage source IP address of the asset.
        start_media_processor (bool | None): The start media processor flag of the asset.
        delete_missing_asset (bool | None): The delete missing asset flag of the asset.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/admin/asset/register"

    body: dict = {
        "id": asset_id,
        "parentId": parent_id,
        "displayObjectKey": display_object_key,
        "bucketName": bucket_name,
        "objectKey": object_key,
        "eTag": etag,
        "tags": tags,
        "collections": collections,
        "relatedContents": related_contents,
        "sequencer": sequencer,
        "assetStatus": asset_status,
        "storageClass": storage_class,
        "assetType": asset_type,
        "contentLength": content_length,
        "storageEventName": storage_event_name,
        "createdDate": created_date,
        "storageSourceIpAddress": storage_source_ip_address,
        "startMediaProcessor": start_media_processor,
        "deleteMissingAsset": delete_missing_asset
    }

    return _send_request(self, "Register asset", api_url, "POST", None, body)
