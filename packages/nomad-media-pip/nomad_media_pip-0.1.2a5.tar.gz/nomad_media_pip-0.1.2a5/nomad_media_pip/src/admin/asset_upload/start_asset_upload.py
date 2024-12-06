"""
This module contains the _start_upload function, which starts an asset upload.

Functions:
    _start_upload: Starts an asset upload.
"""

import os

from nomad_media_pip.src.helpers.send_request import _send_request


def _start_upload(
    self,
    name: str | None,
    existing_content_id: str | None,
    related_content_id: str | None,
    upload_overwrite_option: str,
    file: str,
    parent_id: str | None,
    language_id: str | None
) -> dict | None:
    """
    Uploads a file to the system.

    Args:
        name (str | None): The name of the file being uploaded.
        existing_asset_id (str | None): The Existing AssetId (file) that should be
            overwritten with this upload. Note that by specifying this attribute then the parentId,
            relativePath and displayName are all ignored.
        related_content_id (str | None): The Content ID of the related content record
            to associate this asset to. Note that by specifying this attribute then the parentId and
            relativePath attributes are both ignored.
        upload_overwrite_option (str): The overwrite option for the upload.
            The option you want to use when uploading the asset. The options are continue, replace,
            and cancel. Continue continues the upload from where it left off. Replace replaces an
            existing asset. Replace is the one you want to use if you are starting a new upload.
            Cancel cancels an uploading asset.
        file (str): The filename to upload - or the full or relative path of the file.
            This is ignored if the ExistingAssetId or if the RelatedContentId has a value.
        parent_id (str | None): The Parent AssetId (folder) to add the upload to.
            Note that if there is a full relativePath, then it is appended to this parent path.
            If this value is omitted then the file will be added to the predefined incoming folder.
            This is ignored if the ExistingAssetId or if the RelatedContentId has a value.
        language_id (str | None): The language of the asset to upload.
            If this is left blank then the default system language is used.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/asset/upload/start"

    file_stats: os.stat_result = os.stat(file)

    file_name: str = os.path.basename(file)

    chunk_size = 8388608

    # Build the payload BODY
    body: dict = {
        "displayName": name or file_name,
        "contentLength": file_stats.st_size,
        "uploadOverwriteOption": upload_overwrite_option,
        "chunkSize": chunk_size,
        "relativePath": file_name,
        "parentId": parent_id,
        "existingAssetId": existing_content_id,
        "relatedContentId": related_content_id,
        "languageId": language_id
    }

    return _send_request(self, "Start Upload", api_url, "POST", None, body)
