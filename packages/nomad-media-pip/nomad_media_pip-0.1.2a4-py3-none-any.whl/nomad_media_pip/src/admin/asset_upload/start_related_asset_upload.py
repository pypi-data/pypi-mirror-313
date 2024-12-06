"""
This module contains the function to start a related asset upload.

Functions:
    _start_related_asset_upload: Starts a related asset upload.
"""

import os

from nomad_media_pip.src.helpers.send_request import _send_request


def _start_related_asset_upload(
    self,
    existing_content_id: str,
    related_content_id: str | None,
    new_related_asset_metadata_type: str | None,
    upload_overwrite_option: str,
    file: str,
    language_id: str | None
) -> dict | None:
    """
    Uploads a related asset to the specified existing asset ID.

    Args:
        existing_asset_id (str): Gets or sets the Existing AssetId (file) that should be
            overwritten with this upload. Note that by specifying this attribute then the parentId,
            relativePath and displayName are all ignored.
        related_asset_id (str | None): Gets or sets the related asset ID of the existingAsset that
            we're replacing. If this is used, most of the other properties are not needed.
            new_related_asset_metatype (str | None): Gets or sets the type of the related asset metadata to
            be created for a given ExistingAssetId. If specified, ExistingAssetId has to have a value defined.
        upload_overwrite_option (str): The overwrite option for the upload.
            The option you want to use when uploading the asset. The options are continue, replace, and cancel.
            Continue continues the upload from where it left off. Replace replaces an existing asset.
            Replace is the one you want to use if you are starting a new upload. Cancel cancels an uploading asset.
        file (str): The filename to upload - or the full or relative path of the file.
            This is ignored if the ExistingAssetId or if the RelatedContentId has a value.
        language_id (str | None): The language of the asset to upload.
            If this is left blank then the default system language is used.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/upload/start-related-asset"

    file_stats: os.stat_result = os.stat(file)

    file_name: str = os.path.basename(file)

    aws_min_limit = 5242880
    chunk_size: float = file_stats.st_size / 10000

    if chunk_size < (aws_min_limit * 4):
        chunk_size = 20971520

    body: dict = {
        "contentLength": file_stats.st_size,
        "chunkSize": chunk_size,
        "existingAssetId": existing_content_id,
        "languageId": language_id,
        "newRelatedAssetMetadataType": new_related_asset_metadata_type,
        "relatedAssetId": related_content_id,
        "relativePath": file_name,
        "uploadOverwriteOption": upload_overwrite_option
    }

    return _send_request(self, "Start Related Asset Upload", api_url, "POST", None, body)
