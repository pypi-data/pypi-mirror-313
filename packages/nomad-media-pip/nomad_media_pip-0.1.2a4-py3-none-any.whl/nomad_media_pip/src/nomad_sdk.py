"""
Nomad SDK

This SDK is used to interact with the Nomad API.
"""

import logging
import threading
import os
from typing import TypeVar

# account
from nomad_media_pip.src.common.account_authentication.login import _login
from nomad_media_pip.src.common.account_authentication.refresh_token import _refresh_token

# admin
from nomad_media_pip.src.admin.asset_upload.cancel_upload import _cancel_upload
from nomad_media_pip.src.admin.asset_upload.multi_thread_upload import _multi_thread_upload
from nomad_media_pip.src.admin.asset_upload.start_asset_upload import _start_upload
from nomad_media_pip.src.admin.asset_upload.start_related_asset_upload import _start_related_asset_upload
from nomad_media_pip.src.admin.asset_upload.upload_complete_asset import _upload_complete_asset

from nomad_media_pip.src.admin.audit.get_audit import _get_audit

from nomad_media_pip.src.admin.config.clear_server_cache import _clear_server_cache
from nomad_media_pip.src.admin.config.get_config import _get_config
from nomad_media_pip.src.admin.config.get_server_time import _get_server_time

from nomad_media_pip.src.admin.content.create_content import _create_content
from nomad_media_pip.src.admin.content.deactivate_content_user_track import _deactivate_content_user_track
from nomad_media_pip.src.admin.content.delete_content import _delete_content
from nomad_media_pip.src.admin.content.get_content import _get_content
from nomad_media_pip.src.admin.content.get_content_user_track import _get_content_user_track
from nomad_media_pip.src.admin.content.get_content_user_track_touch import _get_content_user_track_touch
from nomad_media_pip.src.admin.content.update_content import _update_content

from nomad_media_pip.src.admin.content_definition.create_content_definition import _create_content_definition
from nomad_media_pip.src.admin.content_definition.get_content_definition import _get_content_definition
from nomad_media_pip.src.admin.content_definition.get_content_definitions import _get_content_definitions
from nomad_media_pip.src.admin.content_definition.update_content_definition import _update_content_definition

from nomad_media_pip.src.admin.event.add_live_schedule_to_event import _add_live_schedule_to_event
from nomad_media_pip.src.admin.event.create_update_event import _create_and_update_event
from nomad_media_pip.src.admin.event.delete_event import _delete_event
from nomad_media_pip.src.admin.event.extend_live_schedule import _extend_live_schedule
from nomad_media_pip.src.admin.event.get_live_schedule import _get_live_schedule
from nomad_media_pip.src.admin.event.start_live_schedule import _start_live_schedule
from nomad_media_pip.src.admin.event.stop_live_schedule import _stop_live_schedule

from nomad_media_pip.src.admin.live_channel.clip_live_channel import _clip_live_channel
from nomad_media_pip.src.admin.live_channel.create_live_channel import _create_live_channel
from nomad_media_pip.src.admin.live_channel.delete_live_channel import _delete_live_channel
from nomad_media_pip.src.admin.live_channel.get_live_channel import _get_live_channel
from nomad_media_pip.src.admin.live_channel.get_live_channels import _get_live_channels
from nomad_media_pip.src.admin.live_channel.live_channel_refresh import _live_channel_refresh
from nomad_media_pip.src.admin.live_channel.next_event import _next_event
from nomad_media_pip.src.admin.live_channel.start_live_channel import _start_live_channel
from nomad_media_pip.src.admin.live_channel.start_output_tracking import _start_output_tracking
from nomad_media_pip.src.admin.live_channel.stop_live_channel import _stop_live_channel
from nomad_media_pip.src.admin.live_channel.update_live_channel import _update_live_channel

from nomad_media_pip.src.admin.live_input.create_live_input import _create_live_input
from nomad_media_pip.src.admin.live_input.delete_live_input import _delete_live_input
from nomad_media_pip.src.admin.live_input.get_live_input import _get_live_input
from nomad_media_pip.src.admin.live_input.get_live_inputs import _get_live_inputs
from nomad_media_pip.src.admin.live_input.update_live_input import _update_live_input

from nomad_media_pip.src.admin.live_operator.cancel_broadcast import _cancel_broadcast
from nomad_media_pip.src.admin.live_operator.cancel_segment import _cancel_segment
from nomad_media_pip.src.admin.live_operator.complete_segment import _complete_segment
from nomad_media_pip.src.admin.live_operator.get_completed_segments import _get_completed_segments
from nomad_media_pip.src.admin.live_operator.get_live_operator import _get_live_operator
from nomad_media_pip.src.admin.live_operator.get_live_operators import _get_live_operators
from nomad_media_pip.src.admin.live_operator.start_broadcast import _start_broadcast
from nomad_media_pip.src.admin.live_operator.start_segment import _start_segment
from nomad_media_pip.src.admin.live_operator.stop_broadcast import _stop_broadcast

from nomad_media_pip.src.admin.live_output_profile.create_live_output_profile import _create_live_output_profile
from nomad_media_pip.src.admin.live_output_profile.delete_live_output_profile import _delete_live_output_profile
from nomad_media_pip.src.admin.live_output_profile.get_live_output_profile import _get_live_output_profile
from nomad_media_pip.src.admin.live_output_profile.get_live_output_profiles import _get_live_output_profiles
from nomad_media_pip.src.admin.live_output_profile.get_live_output_types import _get_live_output_types
from nomad_media_pip.src.admin.live_output_profile.update_live_output_profile import _update_live_output_profile

from nomad_media_pip.src.admin.live_output_profile_group.create_live_output_profile_group import _create_live_output_profile_group
from nomad_media_pip.src.admin.live_output_profile_group.delete_live_output_profile_group import _delete_live_output_profile_group
from nomad_media_pip.src.admin.live_output_profile_group.get_live_output_profile_group import _get_live_output_profile_group
from nomad_media_pip.src.admin.live_output_profile_group.get_live_output_profile_groups import _get_live_output_profile_groups
from nomad_media_pip.src.admin.live_output_profile_group.update_live_output_profile_group import _update_live_output_profile_group

from nomad_media_pip.src.admin.schedule_event.add_asset_schedule_event import _add_asset_schedule_event
from nomad_media_pip.src.admin.schedule_event.add_input_schedule_event import _add_input_schedule_event
from nomad_media_pip.src.admin.schedule_event.get_asset_schedule_event import _get_asset_schedule_event
from nomad_media_pip.src.admin.schedule_event.get_input_schedule_event import _get_input_schedule_event
from nomad_media_pip.src.admin.schedule_event.move_schedule_event import _move_schedule_event
from nomad_media_pip.src.admin.schedule_event.remove_asset_schedule_event import _remove_asset_schedule_event
from nomad_media_pip.src.admin.schedule_event.remove_input_schedule_event import _remove_input_schedule_event
from nomad_media_pip.src.admin.schedule_event.update_asset_schedule_event import _update_asset_schedule_event
from nomad_media_pip.src.admin.schedule_event.update_input_schedule_event import _update_input_schedule_event

from nomad_media_pip.src.admin.schedule.create_intelligent_playlist import _create_intelligent_playlist
from nomad_media_pip.src.admin.schedule.create_intelligent_schedule import _create_intelligent_schedule
from nomad_media_pip.src.admin.schedule.create_playlist import _create_playlist
from nomad_media_pip.src.admin.schedule.create_playlist_video import _create_playlist_video
from nomad_media_pip.src.admin.schedule.create_schedule_items.create_schedule_item_asset import _create_schedule_item_asset
from nomad_media_pip.src.admin.schedule.create_schedule_items.create_schedule_item_live_channel import _create_schedule_item_live_channel
from nomad_media_pip.src.admin.schedule.create_schedule_items.create_schedule_item_playlist_schedule import _create_schedule_item_playlist_schedule
from nomad_media_pip.src.admin.schedule.create_schedule_items.create_schedule_item_search_filter import _create_schedule_item_search_filter
from nomad_media_pip.src.admin.schedule.delete_intelligent_playlist import _delete_intelligent_playlist
from nomad_media_pip.src.admin.schedule.delete_intelligent_schedule import _delete_intelligent_schedule
from nomad_media_pip.src.admin.schedule.delete_playlist import _delete_playlist
from nomad_media_pip.src.admin.schedule.delete_schedule_item import _delete_schedule_item
from nomad_media_pip.src.admin.schedule.get_intelligent_playlist import _get_intelligent_playlist
from nomad_media_pip.src.admin.schedule.get_intelligent_schedule import _get_intelligent_schedule
from nomad_media_pip.src.admin.schedule.get_playlist import _get_playlist
from nomad_media_pip.src.admin.schedule.get_schedule_item import _get_schedule_item
from nomad_media_pip.src.admin.schedule.get_schedule_items import _get_schedule_items
from nomad_media_pip.src.admin.schedule.get_schedule_preview import _get_schedule_preview
from nomad_media_pip.src.admin.schedule.move_schedule_item import _move_schedule_item
from nomad_media_pip.src.admin.schedule.publish_intelligent_schedule import _publish_intelligent_schedule
from nomad_media_pip.src.admin.schedule.start_schedule import _start_schedule
from nomad_media_pip.src.admin.schedule.stop_schedule import _stop_schedule
from nomad_media_pip.src.admin.schedule.update_intelligent_playlist import _update_intelligent_playlist
from nomad_media_pip.src.admin.schedule.update_intelligent_schedule import _update_intelligent_schedule
from nomad_media_pip.src.admin.schedule.update_playlist import _update_playlist
from nomad_media_pip.src.admin.schedule.update_playlist_video import _update_playlist_video
from nomad_media_pip.src.admin.schedule.update_schedule_items.update_schedule_item_asset import _update_schedule_item_asset
from nomad_media_pip.src.admin.schedule.update_schedule_items.update_schedule_item_live_channel import _update_schedule_item_live_channel
from nomad_media_pip.src.admin.schedule.update_schedule_items.update_schedule_item_playlist_schedule import _update_schedule_item_playlist_schedule
from nomad_media_pip.src.admin.schedule.update_schedule_items.update_schedule_item_search_filter import _update_schedule_item_search_filter

from nomad_media_pip.src.admin.user.delete_user import _delete_user
from nomad_media_pip.src.admin.user.delete_user_content_attribute_data import _delete_user_content_attribute_data
from nomad_media_pip.src.admin.user.delete_user_content_group_data import _delete_user_content_group_data
from nomad_media_pip.src.admin.user.delete_user_content_security_data import _delete_user_content_security_data
from nomad_media_pip.src.admin.user.delete_user_data import _delete_user_data
from nomad_media_pip.src.admin.user.delete_user_dislike_data import _delete_user_dislike_data
from nomad_media_pip.src.admin.user.delete_user_favorites_data import _delete_user_favorites_data
from nomad_media_pip.src.admin.user.delete_user_likes_data import _delete_user_likes_data
from nomad_media_pip.src.admin.user.delete_user_saved_search_data import _delete_user_saved_search_data
from nomad_media_pip.src.admin.user.delete_user_session_data import _delete_user_session_data
from nomad_media_pip.src.admin.user.delete_user_share_data import _delete_user_share_data
from nomad_media_pip.src.admin.user.delete_user_video_tracking_data import _delete_user_video_tracking_data

from nomad_media_pip.src.admin.user_session.change_session_status import _change_session_status
from nomad_media_pip.src.admin.user_session.get_user_session import _get_user_session

from nomad_media_pip.src.common.account_authentication.forgot_password import _forgot_password
from nomad_media_pip.src.common.account_authentication.reset_password import _reset_password
from nomad_media_pip.src.common.account_authentication.logout import _logout

from nomad_media_pip.src.common.account_registration.register import _register
from nomad_media_pip.src.common.account_registration.resend_code import _resend_code
from nomad_media_pip.src.common.account_registration.verify import _verify

from nomad_media_pip.src.common.asset.archive_asset import _archive_asset
from nomad_media_pip.src.common.asset.build_media import _build_media
from nomad_media_pip.src.common.asset.clip_asset import _clip_asset
from nomad_media_pip.src.common.asset.copy_asset import _copy_asset
from nomad_media_pip.src.common.asset.create_annotation import _create_annotation
from nomad_media_pip.src.common.asset.create_asset_ad_break import _create_asset_ad_break
from nomad_media_pip.src.common.asset.create_folder_asset import _create_folder_asset
from nomad_media_pip.src.common.asset.create_placeholder_asset import _create_placeholder_asset
from nomad_media_pip.src.common.asset.create_screenshot_at_timecode import _create_screenshot_at_timecode
from nomad_media_pip.src.common.asset.delete_annotation import _delete_annotation
from nomad_media_pip.src.common.asset.delete_asset import _delete_asset
from nomad_media_pip.src.common.asset.delete_asset_ad_break import _delete_asset_ad_break
from nomad_media_pip.src.common.asset.download_archive_asset import _download_archive_asset
from nomad_media_pip.src.common.asset.duplicate_asset import _duplicate_asset
from nomad_media_pip.src.common.asset.get_annotations import _get_annotations
from nomad_media_pip.src.common.asset.get_asset import _get_asset
from nomad_media_pip.src.common.asset.get_asset_ad_breaks import _get_asset_ad_breaks
from nomad_media_pip.src.common.asset.get_asset_child_nodes import _get_asset_child_nodes
from nomad_media_pip.src.common.asset.get_asset_details import _get_asset_details
from nomad_media_pip.src.common.asset.get_asset_manifest_with_cookies import _get_asset_manifest_with_cookies
from nomad_media_pip.src.common.asset.get_asset_metadata_summary import _get_asset_metadata_summary
from nomad_media_pip.src.common.asset.get_asset_parent_folders import _get_asset_parent_folders
from nomad_media_pip.src.common.asset.get_asset_screenshot_details import _get_asset_screenshot_details
from nomad_media_pip.src.common.asset.get_asset_segment_details import _get_asset_segment_details
from nomad_media_pip.src.common.asset.get_user_upload_parts import _get_user_upload_parts
from nomad_media_pip.src.common.asset.get_user_uploads import _get_user_uploads
from nomad_media_pip.src.common.asset.import_annotations import _import_annotations
from nomad_media_pip.src.common.asset.index_asset import _index_asset
from nomad_media_pip.src.common.asset.local_restore_asset import _local_restore_asset
from nomad_media_pip.src.common.asset.move_asset import _move_asset
from nomad_media_pip.src.common.asset.records_asset_tracking_beacon import _records_asset_tracking_beacon
from nomad_media_pip.src.common.asset.register_asset import _register_asset
from nomad_media_pip.src.common.asset.reprocess_asset import _reprocess_asset
from nomad_media_pip.src.common.asset.restore_asset import _restore_asset
from nomad_media_pip.src.common.asset.share_asset import _share_asset
from nomad_media_pip.src.common.asset.start_workflow import _start_workflow
from nomad_media_pip.src.common.asset.transcribe_asset import _transcribe_asset
from nomad_media_pip.src.common.asset.update_annotation import _update_annotation
from nomad_media_pip.src.common.asset.update_asset import _update_asset
from nomad_media_pip.src.common.asset.update_asset_ad_break import _update_asset_ad_break
from nomad_media_pip.src.common.asset.update_asset_language import _update_asset_language

from nomad_media_pip.src.common.content_metadata.add_custom_properties import _add_custom_properties
from nomad_media_pip.src.common.content_metadata.add_related_content import _add_related_content
from nomad_media_pip.src.common.content_metadata.add_tag_or_collection import _add_tag_or_collection
from nomad_media_pip.src.common.content_metadata.bulk_update_metadata import _bulk_update_metadata
from nomad_media_pip.src.common.content_metadata.create_tag_or_collection import _create_tag_or_collection
from nomad_media_pip.src.common.content_metadata.delete_related_content import _delete_related_content
from nomad_media_pip.src.common.content_metadata.delete_tag_or_collection import _delete_tag_or_collection
from nomad_media_pip.src.common.content_metadata.get_tag_or_collection import _get_tag_or_collection
from nomad_media_pip.src.common.content_metadata.remove_tag_or_collection import _remove_tag_or_collection

from nomad_media_pip.src.common.ping.ping import _ping
from nomad_media_pip.src.common.ping.ping_auth import _ping_auth

from nomad_media_pip.src.common.search.search import _search

from nomad_media_pip.src.portal.account_updates.change_email import _change_email
from nomad_media_pip.src.portal.account_updates.change_password import _change_password
from nomad_media_pip.src.portal.account_updates.get_user import _get_user
from nomad_media_pip.src.portal.account_updates.update_user import _update_user

from nomad_media_pip.src.portal.content_groups.add_contents_to_content_group import _add_contents_to_content_group
from nomad_media_pip.src.portal.content_groups.create_content_group import _create_content_group
from nomad_media_pip.src.portal.content_groups.delete_content_group import _delete_content_group
from nomad_media_pip.src.portal.content_groups.get_content_group import _get_content_group
from nomad_media_pip.src.portal.content_groups.get_content_groups import _get_content_groups
from nomad_media_pip.src.portal.content_groups.get_portal_groups import _get_portal_groups
from nomad_media_pip.src.portal.content_groups.remove_contents_from_content_group import _remove_contents_from_content_group
from nomad_media_pip.src.portal.content_groups.rename_content_group import _rename_content_group
from nomad_media_pip.src.portal.content_groups.share_content_group_with_user import _share_content_group_with_user
from nomad_media_pip.src.portal.content_groups.stop_sharing_content_group_with_user import _stop_sharing_content_group_with_user

from nomad_media_pip.src.portal.guest_registration.guest_invite import _guest_invite
from nomad_media_pip.src.portal.guest_registration.register_guest import _register_guest
from nomad_media_pip.src.portal.guest_registration.remove_guest import _remove_guest

from nomad_media_pip.src.portal.media.clear_continue_watching import _clear_continue_watching
from nomad_media_pip.src.portal.media.clear_watchlist import _clear_watchlist
from nomad_media_pip.src.portal.media.create_form import _create_form
from nomad_media_pip.src.portal.media.get_content_cookies import _get_content_cookies
from nomad_media_pip.src.portal.media.get_default_site_config import _get_default_site_config
from nomad_media_pip.src.portal.media.get_dynamic_content import _get_dynamic_content
from nomad_media_pip.src.portal.media.get_dynamic_contents import _get_dynamic_contents
from nomad_media_pip.src.portal.media.get_media_group import _get_media_group
from nomad_media_pip.src.portal.media.get_media_item import _get_media_item
from nomad_media_pip.src.portal.media.get_my_content import _get_my_content
from nomad_media_pip.src.portal.media.get_my_group import _get_my_group
from nomad_media_pip.src.portal.media.get_site_config import _get_site_config
from nomad_media_pip.src.portal.media.media_search import _media_search

from nomad_media_pip.src.portal.media_builder.create_media_builder import _create_media_builder
from nomad_media_pip.src.portal.media_builder.create_media_builder_item import _create_media_builder_item
from nomad_media_pip.src.portal.media_builder.create_media_builder_items_add_annotations import _create_media_builder_items_add_annotations
from nomad_media_pip.src.portal.media_builder.create_media_builder_items_bulk import _create_media_builder_items_bulk
from nomad_media_pip.src.portal.media_builder.delete_media_builder import _delete_media_builder
from nomad_media_pip.src.portal.media_builder.delete_media_builder_item import _delete_media_builder_item
from nomad_media_pip.src.portal.media_builder.duplicate_media_builder import _duplicate_media_builder
from nomad_media_pip.src.portal.media_builder.get_media_builder import _get_media_builder
from nomad_media_pip.src.portal.media_builder.get_media_builder_ids_from_asset import _get_media_builder_ids_from_asset
from nomad_media_pip.src.portal.media_builder.get_media_builders import _get_media_builders
from nomad_media_pip.src.portal.media_builder.get_media_builder_items import _get_media_builder_items
from nomad_media_pip.src.portal.media_builder.move_media_builder_item import _move_media_builder_item
from nomad_media_pip.src.portal.media_builder.render_media_builder import _render_media_builder
from nomad_media_pip.src.portal.media_builder.update_media_builder import _update_media_builder

from nomad_media_pip.src.portal.saved_search.add_saved_search import _add_saved_search
from nomad_media_pip.src.portal.saved_search.delete_saved_search import _delete_saved_search
from nomad_media_pip.src.portal.saved_search.get_saved_search import _get_saved_search
from nomad_media_pip.src.portal.saved_search.get_saved_searches import _get_saved_searches
from nomad_media_pip.src.portal.saved_search.get_search_saved import _get_search_saved
from nomad_media_pip.src.portal.saved_search.get_search_saved_by_id import _get_search_saved_by_id
from nomad_media_pip.src.portal.saved_search.patch_saved_search import _patch_saved_search
from nomad_media_pip.src.portal.saved_search.update_saved_search import _update_saved_search

from nomad_media_pip.src.portal.share.delete_share import _delete_share
from nomad_media_pip.src.portal.share.get_share import _get_share
from nomad_media_pip.src.portal.share.share import _share
from nomad_media_pip.src.portal.share.share_expire import _share_expire
from nomad_media_pip.src.portal.share.share_notification import _share_notification
from nomad_media_pip.src.portal.share.update_share import _update_share

from nomad_media_pip.src.portal.video_tracking.get_video_tracking import _get_video_tracking

from nomad_media_pip.src.helpers.send_request import _send_request

Self = TypeVar("Self", bound="Nomad_SDK")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')


class InvalidAPITypeException(Exception):
    """
    This class is used to throw an exception when the API type is invalid.
    """

    def __init__(self, message) -> None:
        self.message: str = message
        super().__init__(self.message)


class LoginError(Exception):
    """
    This class is used to throw an exception when the login info is incorrect.
    """

    def __init__(self, message="Login info incorrect") -> None:
        self.message: str = message
        super().__init__(self.message)


class Nomad_SDK:
    """
    Nomad SDK

    This SDK is used to interact with the Nomad API.
    """

    _instance = None
    _lock = threading.Lock()
    _stop_event = threading.Event()

    def __new__(cls, config) -> Self:

        if config.get("singleton", True) is True:
            if cls._instance is None:
                with cls._lock:
                    if cls._instance is None:
                        cls._instance: Self = super(Nomad_SDK, cls).__new__(cls)
                        cls._instance.__init__(config)
            return cls._instance

        instance: Self = super(Nomad_SDK, cls).__new__(cls)
        instance.__init__(config)
        return instance

    def __init__(self, config) -> None:
        if not hasattr(self, "initialized"):
            self.config: dict[str, any] = config
            self.token: str = None
            self.refresh_token_val: str = None
            self.expiration_seconds: str = None
            self.user_session_id: str = None
            self.id: str = None
            self.debug: bool = self.config.get("debugMode", False)

            if self.config.get("noLogging") is True:
                logging.getLogger().setLevel(logging.CRITICAL + 1)
            elif self.debug:
                logging.getLogger().setLevel(logging.DEBUG)
            else:
                logging.getLogger().setLevel(logging.INFO)

            if self.config["serviceApiUrl"][-1] == "/":
                self.config["serviceApiUrl"] = self.config["serviceApiUrl"][:-1]

            # User may not want to login initially
            if self.config.get("username") and self.config.get("password"):
                 self.login()
                
            self.initialized = True

    def login(self) -> None:
        """
        Logs in to the system.

        Raises:
            LoginError: If the login info is incorrect.
        """

        login_info: dict | None = _login(self)
        if login_info == "Login info incorrect":
            raise LoginError()
        self.token = login_info["token"]
        self.refresh_token_val = login_info["refreshToken"]
        self.expiration_seconds = login_info["expirationSeconds"]
        self.id = login_info["id"]

    def refresh_token(self) -> None:
        """
        Refreshes the token.
        """

        refreshed: bool = _refresh_token(self)

        if refreshed:
            logging.info("Token refreshed")

    # admin
    # asset upload
    def upload_asset(
        self,
        name: str | None,
        existing_asset_id: str | None,
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
            file (str): The full or relative path of the file.
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

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        start_upload_info = None
        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Uploading asset %s", name)

            logging.info("Start upload")
            start_upload_info: dict | None = _start_upload(
                self,
                name,
                existing_asset_id,
                related_content_id,
                upload_overwrite_option,
                file,
                parent_id,
                language_id
            )

            if start_upload_info is None:
                raise RuntimeError("Failed to start upload")

            _multi_thread_upload(self, file, start_upload_info)

            _upload_complete_asset(self, start_upload_info["id"])

            if start_upload_info:
                logging.info("Upload complete")

            return start_upload_info["assetId"]
        except RuntimeError as error:
            logging.error("Upload failed: %s", str(error))

            if start_upload_info:
                _cancel_upload(self, start_upload_info.get("id"))

            return None

    def upload_related_asset(
        self,
        existing_asset_id: str,
        related_asset_id: str | None,
        new_related_asset_metatype: str | None,
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

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        start_upload_info = None
        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Uploading related asset")

            logging.info("Start upload")
            start_upload_info: dict | None = _start_related_asset_upload(
                self,
                existing_asset_id,
                related_asset_id,
                new_related_asset_metatype,
                upload_overwrite_option,
                file,
                language_id)

            if start_upload_info is None:
                raise RuntimeError("Failed to start upload")

            _multi_thread_upload(self, file, start_upload_info)

            _upload_complete_asset(self, start_upload_info["id"])

            if start_upload_info:
                logging.info("Upload complete")

            details: dict | None = _get_asset_details(self, existing_asset_id)

            related_asset: dict | None = next(
                (
                    asset for asset in details['relatedAssets'] if os.path.basename(file) in asset['url']
                ), None
            )

            return related_asset["id"]

        except RuntimeError as error:
            logging.error("Upload failed: %s", str(error))

            if start_upload_info:
                _cancel_upload(self, start_upload_info.get("id"))

            return None

    # audit

    def get_audit(self, content_id: str) -> dict | None:
        """
        Gets the audit information for the specified content ID.

        Args:
            content_id (str): The ID of the content to get the audit information for.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting audit")

            audit: dict | None = _get_audit(self, content_id)

            if audit is not None:
                logging.info("Get audit complete")

            return audit
        except Exception as error:
            logging.error("Get audit failed")
            raise error

    # config
    def clear_server_cache(self) -> None:
        """
        Clears the server cache.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Clearing server cache")

            _clear_server_cache(self)

            logging.info("Clear server cache complete")
        except Exception as error:
            logging.error("Clear server cache failed")
            raise error

    def get_config(self, config_type: int) -> dict | None:
        """
        Gets the specified config.

        Args:
            config_type (int): The type of config to get. 1 - Admin, 2 - Lambda, 3 - Groundtruth

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting config")

            config: dict | None = _get_config(self, config_type)

            if config is not None:
                logging.info("Get config complete")

            return config
        except Exception as error:
            logging.error("Get config failed")
            raise error

    def get_server_time(self) -> dict | None:
        """
        Gets the server time.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting server time")

            server_time: dict | None = _get_server_time(self)

            if server_time is not None:
                logging.info("Get server time complete")

            return server_time
        except Exception as error:
            logging.error("Get server time failed")
            raise error

    # content
    def create_content(self, content_definition_id: str, language_id: str | None) -> dict | None:
        """
        Creates a content.

        Args:
            content_definition_id (str): The ID of the content definition to use.
            language_id (str | None): The ID of the language to use. If this is None then the default language is used.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating content")

            content_id: dict | None = _create_content(self, content_definition_id, language_id)

            if content_id is not None:
                logging.info("Create content complete")

            return content_id
        except Exception as error:
            logging.error("Create content failed")
            raise error

    def deactivate_content_user_track(
        self,
        session_id: str,
        content_id: str,
        content_definition_id: str,
        deactivate: bool
    ) -> None:
        """
        Deactivates the specified user track.

        Args:
            session_id (str): The session ID of the user track to deactivate.
            content_id (str): The content ID of the user track to deactivate.
            content_definition_id (str): The content definition ID of the user track to deactivate.
            deactivate (bool): Whether to deactivate the user track.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """
        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deactivating content user track")

            _deactivate_content_user_track(self, session_id, content_id, content_definition_id, deactivate)

            logging.info("Deactivate content user track complete")
        except Exception as error:
            logging.error("Deactivate content user track failed")
            raise error

    def delete_content(self, content_id: str, content_definition_id: str) -> None:
        """
        Deletes a content.

        Args:
            content_id (str): The ID of the content to delete.
            content_definition_id (str): The ID of the content definition the content belongs to.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting content")

            _delete_content(self, content_id, content_definition_id)

            logging.info("Delete content complete")
        except Exception as error:
            logging.error("Delete content failed")
            raise error

    def get_content(self, content_id: str, content_definition_id: str, is_revision: str | bool) -> dict | None:
        """
        Gets a content.

        Args:
            content_id (str): The ID of the content to get.
            content_definition_id: The ID of the content definition the content belongs to.
            is_revision (bool | None): Indicates if the content is a revision. Defaults to false.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Geting content")

            content: dict | None = _get_content(self, content_id, content_definition_id, is_revision)

            if content is not None:
                logging.info("Get content complete")

            return content
        except Exception as error:
            logging.error("Get content failed")
            raise error

    def get_content_user_track(
            self,
            content_id: str,
            content_definition_id: str,
            sort_column: str | None,
            is_desc: bool | None,
            page_index: int | None,
            page_size: int | None) -> dict | None:
        """
        Gets the specified content user track.

        Args:
            content_id (str): The ID of the content to get the user track for.
            content_definition_id (str): The ID of the content definition to use.
            sort_column (str | None): The column to sort by.
            is_desc (bool | None): Whether to sort descending.
            page_index (int | None): The page index to get.
            page_size (int | None): The page size to get.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting content user track")

            content: dict | None = _get_content_user_track(
                self, content_id, content_definition_id, sort_column, is_desc, page_index, page_size
            )

            if content is not None:
                logging.info("Get content user track complete")

            return content
        except Exception as error:
            logging.error("Get content user track failed")
            raise error

    def get_content_user_track_touch(self, content_id: str, content_definition_id: str) -> dict | None:
        """
        Gets the specified content user track touch.

        Args:
            content_id (str): The ID of the content to get the user track touch for.
            content_definition_id (str): The ID of the content definition to use.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting content user track touch")

            content: dict | None = _get_content_user_track_touch(self, content_id, content_definition_id)

            if content is not None:
                logging.info("Get content user track touch complete")

            return content
        except Exception as error:
            logging.error("Get content user track touch failed")
            raise error

    def update_content(
        self,
        content_id: str,
        content_definition_id: str,
        properties: dict,
        language_id: str | None
    ) -> dict | None:
        """
        Updates a content.

        Args:
            content_id (str): The ID of the content to update.
            content_definition_id: The ID of the content definition the content belongs to.
            properties (dict): The properties to update.
            language_id (str | None): The language id of the asset to upload.
            If this is left blank then the default system language is used.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating content")

            _update_content(self, content_id, content_definition_id, properties, language_id)

            logging.info("Update content complete")
        except Exception as error:
            logging.error("Update content failed")
            raise error

    # Content Definition
    def create_content_definition(self) -> dict | None:
        """
        Creates a new content definition.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating content definition")

            content: dict | None = _create_content_definition(self)

            if content is not None:
                logging.info("Create content definition complete")

            return content
        except Exception as error:
            logging.error("Create content definition failed")
            raise error

    def get_content_definition(self, content_definition_id: str) -> dict | None:
        """
        Gets the specified content definition.

        Args:
            content_definition_id (string): The ID of the content definition to get.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting content definition")

            content: dict | None = _get_content_definition(self, content_definition_id)

            if content is not None:
                logging.info("Get content definition complete")

            return content
        except Exception as error:
            logging.error("Get content definition failed")
            raise error

    def get_content_definitions(
        self,
        content_management_type: int | None,
        sort_column: str | None,
        is_desc: bool | None,
        page_index: int | None,
        page_size: int | None
    ) -> dict | None:
        """
        Gets the content definitions.

        Args:
            content_management_type (number | null): The type of content management to get.
                enum: 1; None, 2; DataSelector, 3; FormSelector
            sort_column (string | null): The column to sort by.
            is_desc (boolean | null): Whether to sort descending.
            page_index (number | null): The page index to get.
            page_size (number | null): The page size to get.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting content definitions")

            content: dict | None = _get_content_definitions(
                self, content_management_type, sort_column, is_desc, page_index, page_size
            )

            if content is not None:
                logging.info("Get content definitions complete")

            return content
        except Exception as error:
            logging.error("Get content definitions failed")
            raise error

    def update_content_definition(
        self,
        content_definition_id: str,
        name: str | None,
        content_fields: list[dict] | None,
        content_definition_group: str | None,
        content_definition_type: str | None,
        display_field: str | None,
        route_item_name_field: str | None,
        security_groups: list[str] | None,
        system_roles: list[str] | None,
        include_in_tags: bool | None,
        index_content: bool | None
    ) -> None:
        """
        Updates the specified content definition.

        Args:
            content_defnition_id (string): The ID of the content definition to update.
            name (str | None): The name of the content definition.
            content_fields (list[dict] | None): The content fields of the content definition.
            content_definition_group (str | None): The content definition group of the content definition.
                    enum: Custom Definitions, Forms, Layout, Navigation, Page Content, System Definitions
            content_definition_type (str | None): The content definition type of the content definition.
                enum: Asset List Content Type, Basic Content, Dynamic Module Content Type,
                Form Content Type, Navigation Content Type
            display_field (str | None): The display field of the content definition. This is the field that
                is used to display the content definition. Must be a field in the content definition or content fields.
            route_item_name_field (str | None): The name of the route item. This is used to create the route
                for the content definition. Must be a field in the content definition or content fields.
            security_groups (list[str] | None): The security groups of the content definition.
                enum: Content Manager, Developers, Everyone, Guest, Quality Assurance Specialists
            system_roles (list[str] | None): The system roles of the content definition.
                enum: Content Manager, Quality Assurance Specialist, System Administrator
            include_in_tags (boolean | None): Whether to include the content definition in tags.
            index_content (boolean | None): Whether to index the content.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating content definition")

            _update_content_definition(
                self, content_definition_id, name, content_fields, content_definition_group, content_definition_type,
                display_field, route_item_name_field, security_groups, system_roles, include_in_tags, index_content
            )

            logging.info("Update content definition complete")
        except Exception as error:
            logging.error("Update content definition failed")
            raise error

    # Event
    def add_live_schedule_to_event(
        self,
        event_id: str,
        slate_video: dict | None,
        preroll_video: dict | None,
        postroll_video: dict | None,
        is_secure_output: bool | None,
        archive_folder: dict | None,
        primary_live_input: dict | None,
        backup_live_input: dict | None,
        primary_livestream_input_url: dict | None,
        backup_livestream_input_url: dict | None,
        external_output_profiles: list[dict] | None,
        status: dict | None,
        status_message: str | None,
        live_channel: dict | None,
        override_settings: bool | None,
        output_profile_group: dict | None
    ) -> None:
        """
        Adds a live schedule to an event and updated live schedule attached to event.

        Args:
            event_id (str): The ID of the event to add the live schedule to.
            slate_video (dict | None): The slate video ID of the event. Format: {"id": string, "description": string }
            preroll_video (dict | None): The preroll video of the event. Format: {"id": string, "description": string }
            postroll_video (dict | None): The postroll video of the event. Format: {"id": string, "description": string }
            is_secure_output (bool | None): Whether the event is secure output.
            archive_folder (dict | None): The archive folder of the event. Format: { id: string, description: string }
            primary_live_input (dict | None): The live input A ID of the event. Format: { id: string, description: string }
            backup_live_input (dict | None): The live input B ID of the event. Format: { id: string, description: string }
            primary_livestream_input_url (str | None): The primary live stream URL of the event.
            backup_livestream_input_url (str | None): The backup live stream URL of the event.
            external_output_profiles (list[dict] | None): The external output profiles of the event. Format: [{ id: string, description: string }]
            status (dict | None): Current status of the Live Channel Settings configuration. Format: { id: string, description: string }
            status_message (str | None): The status message of the event.
            live_channel (dict | None): The live channel of the event. Format: { id: string, description: string }
            override_settings (bool | None): Whether to override the settings of the event.
            output_profile_group (dict | None): The output profile group of the event. Format: { id: string, description: string }

        Returns:
            None: A promise that resolves when the live event schedule is created.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Adding live schedule to event")

            _add_live_schedule_to_event(
                self, event_id, slate_video, preroll_video, postroll_video, is_secure_output, archive_folder,
                primary_live_input, backup_live_input, primary_livestream_input_url, backup_livestream_input_url,
                external_output_profiles, status, status_message, live_channel, override_settings, output_profile_group
            )

            logging.info("Add live schedule to event complete")
        except Exception as error:
            logging.error("Add live schedule to event failed")
            raise error

    def create_and_update_event(
        self,
        content_id: str | None,
        content_definition_id: str,
        name: str | None,
        start_datetime: str,
        end_datetime: str,
        event_type: dict,
        series: dict | None,
        is_disabled: bool | None,
        override_series_properties: bool,
        series_properties: dict | None
    ) -> str | None:
        """
        Creates and updates an event.

        Args:
            content_id (str | None): The content id of the event to update. None for create.
            content_definition_id (str): The content definition id of the event.
            name (str | None): The name of the event.
            start_datetime (str): The start date time of the event.
            end_datetime (str): The end date time of the event.
            event_type (dict): The event type of the event. Format: { id: string, description: string }
            series (dict | None): The series of the event. Format: { id: string, description: string }
            is_disaled (bool | None): Whether the event is disabled.
            override_series_properties (bool): Whether to override the series properties.
            series_properties (dict | None): The properties of the event.

        Returns:
            str: The ID of the event if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating and updating event")

            event: dict | None = _create_and_update_event(
                self, content_id, content_definition_id, name, start_datetime, end_datetime, event_type,
                series, is_disabled, override_series_properties, series_properties
            )

            if event is not None:
                logging.info("Create and update event complete")

            return event
        except Exception as error:
            logging.error("Create and update event failed")
            raise error

    def delete_event(self, content_id: str, content_definition_id: str) -> None:
        """
        Deletes an event.

        Args:
            content_id (str): The ID of the event to delete.
            content_definition_id (str): The content definition ID of the event to delete.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting event")

            _delete_event(self, content_id, content_definition_id)

            logging.info("Delete event complete")
        except Exception as error:
            logging.error("Delete event failed")
            raise error

    def extend_live_schedule(
        self,
        event_id: str,
        recurring_days: list[dict],
        recurring_weeks: int,
        end_date: str | None
    ) -> None:
        """
        Extends the live schedule of an event.

        Args:
            event_id (str): The ID of the event to extend the live schedule of.
            recurring_days (list[dict]): The days of the week to extend the live schedule of.
                dict format: { id: string, description: string }
            recurring_weeks (int): The number of weeks to extend the live schedule of.
            end_date (str | None): The end date to extend the live schedule of.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Extending live schedule")

            _extend_live_schedule(self, event_id, recurring_days, recurring_weeks, end_date)

            logging.info("Extend live schedule complete")
        except Exception as error:
            logging.error("Extend live schedule failed")
            raise error

    def get_live_schedule(self, event_id: str) -> dict | None:
        """
        Gets the live schedule of an event.

        Args:
            event_id (str): The ID of the event to get the live schedule of.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting live schedule")

            event: dict | None = _get_live_schedule(self, event_id)

            if event is not None:
                logging.info("Get live schedule complete")

            return event
        except Exception as error:
            logging.error("Get live schedule failed")
            raise error

    def start_live_schedule(self, event_id: str) -> None:
        """
        Starts the live schedule of an event.

        Args:
            event_id (str): The ID of the event to start the live schedule of.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Starting live schedule")

            _start_live_schedule(self, event_id)

            logging.info("Start live schedule complete")
        except Exception as error:
            logging.error("Start live schedule failed")
            raise error

    def stop_live_schedule(self, event_id: str) -> None:
        """
        Stops the live schedule of an event.

        Args:
            event_id (str): The ID of the event to stop the live schedule of.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Stopping live schedule")

            _stop_live_schedule(self, event_id)

            logging.info("Stop live schedule complete")
        except Exception as error:
            logging.error("Stop live schedule failed")
            raise error

    # Live Channel
    def clip_live_channel(
        self,
        live_channel_id: str,
        start_time_code: str | None,
        end_time_code: str | None,
        title: str | None,
        output_folder_id: str,
        tags: list[dict] | None,
        collections: list[dict] | None,
        related_contents: list[dict] | None,
        video_bitrate: int | None,
        audio_tracks: list[dict] | None
    ) -> dict | None:
        """
        Clips a live channel.

        Args:
            live_channel_id (str): The ID of the live channel to clip.
            start_time_code (str | None): The start time code of the live channel to clip.
            end_time_code (str | None): The end time code of the live channel to clip.
            title (str | None): The title of the live channel to clip.
            output_folder_id (str): The output folder ID of the live channel to clip.
            tags (list[dict] | None): The tags of the live channel to clip.
                dict format: { id: string, description: string }
            collections (list[dict] | None): The collections of the live channel to clip. Format:
                dict format: { id: string, description: string }
            related_contents (list[dict] | None): The related contents of the live channel to clip.
                dict format: { id: string, description: string }
            video_bitrate int | None: The video bitrate of the live channel to clip.
            audio_tracks (list[dict] | None): The audio tracks of the live channel to clip.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Clipping live channel")

            live_channel: dict | None = _clip_live_channel(
                self, live_channel_id, start_time_code, end_time_code, title, output_folder_id,
                tags, collections, related_contents, video_bitrate, audio_tracks
            )

            if live_channel is not None:
                logging.info("Clip live channel complete")

            return live_channel
        except Exception as error:
            logging.error("Clip live channel failed")
            raise error

    def create_live_channel(
        self,
        name: str | None,
        thumbnail_image_id: str | None,
        archive_folder_asset_id: str | None,
        enable_high_availability: bool | None,
        enable_live_clipping: bool | None,
        is_secure_output: bool,
        is_output_screenshot: bool,
        channel_type: str | None,
        external_service_api_url: str | None,
        security_groups: str | None
    ) -> dict | None:
        """
        Creates a live channel.

        Args:
            name (str | None): The name of the live channel.
            thumbnail_image_id (str | None): The thumbnail image ID of the live channel.
            archive_folder_asset_id (str | None): The archive folder asset ID of the live channel.
            enable_high_availability (bool | None): Indicates if the live channel is enabled for high availability.
            enable_live_clipping (bool | None): Indicates if the live channel is enabled for live clipping.
            is_secure_output (bool): Indicates if the live channel is secure output.
            is_output_screenshot (bool): Indicates if the live channel is output screenshot.
            type (str): The type of the live channel. The types are External, IVS, Normal, and Realtime.
            external_service_api_url (str | None): The external service API URL of the live channel.
                Only required if the type is External.
            security_groups (str | None): The security groups of the live channel.
                The security groups are: Content Manager, Everyone, and Guest.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start create live channel")

            live_channel_info: dict | None = _create_live_channel(
                self, name, thumbnail_image_id, archive_folder_asset_id, enable_high_availability, enable_live_clipping,
                is_secure_output, is_output_screenshot, channel_type, external_service_api_url, security_groups
            )

            if live_channel_info is not None:
                logging.info("Create live channel complete")

            return live_channel_info
        except Exception as error:
            logging.error("Create live channel failed")
            raise error

    def delete_live_channel(self, live_channel_id: str, delete_inputs: bool) -> None:
        """
        Deletes a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.
            delete_inputs (bool | None): Indicates if the live channel inputs should be deleted.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start delete live channel")

            _delete_live_channel(self, live_channel_id, delete_inputs)

            logging.info("Delete live channel complete")
        except Exception as error:
            logging.error("Delete live channel failed")
            raise error

    def get_live_channel(self, live_channel_id: str) -> dict | None:
        """
        Gets the live channel.

        Args:
            live_channel_id (str): The ID of the live channel.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live channel")

            live_channel_info: dict | None = _get_live_channel(self, live_channel_id)

            if live_channel_info is not None:
                logging.info("Get live channel complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get live channel failed")
            raise error

    def get_live_channels(self) -> dict | None:
        """
        Gets all the live channels.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live channels")

            live_channel_info: dict | None = _get_live_channels(self)

            if live_channel_info is not None:
                logging.info("Get live channels complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get live channels failed")
            raise error

    def live_channel_refresh(self) -> None:
        """
        Refreshes Live Channels

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start live channel refresh")

            _live_channel_refresh(self)

            logging.info("Live channel refresh complete")
        except Exception as error:
            raise error

    def next_event(self, live_channel_id: str) -> dict | None:
        """
        Gets the next live channel event

        Args:
            live_channel_id (str): The ID of the live channel.

        Returns:
            dict: The information of the next live channel event.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get next live channel event")

            live_channel_info: dict | None = _next_event(self, live_channel_id)

            if live_channel_info is not None:
                logging.info("Get next live channel event complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get next live channel event failed")
            raise error

    def start_live_channel(self, live_channel_id: str, wait_for_start: bool | None) -> None:
        """
        Starts a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.
            wait_for_start (bool | None): Indicates if the live channel should wait for start.

        Returns:
            None: If the request is successful.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start start live channel")

            _start_live_channel(self, live_channel_id, wait_for_start)

            logging.info("Start live channel complete")
        except Exception as error:
            logging.error("Start live channel failed")
            raise error

    def start_output_tracking(self, live_channel_id: str) -> None:
        """
        Starts output tracking for a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start start output tracking")

            _start_output_tracking(self, live_channel_id)

            logging.info("Start output tracking complete")
        except Exception as error:
            raise error

    def stop_live_channel(self, live_channel_id: str, wait_for_stop: bool | None) -> None:
        """
        Stops a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.
            wait_for_stop (bool | None): Indicates if the live channel should wait for stop.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start stop live channel")

            _stop_live_channel(self, live_channel_id, wait_for_stop)

            logging.info("Stop live channel complete")
        except Exception as error:
            logging.error("Stop live channel failed")
            raise error

    def update_live_channel(
        self,
        live_channel_id: str,
        name: str | None,
        thumbnail_image_id: str | None,
        archive_folder_asset_id: str | None,
        enable_high_availability: bool | None,
        enable_live_clipping: bool | None,
        is_secure_output: bool,
        is_output_screenshot: bool,
        channel_type: str | None,
        external_service_api_url: str | None,
        security_groups: str | None
    ) -> dict | None:
        """
        Updates a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.
            name (str | None): The name of the live channel.
            thumbnail_image_id (str | None): The thumbnail image ID of the live channel.
            archive_folder_asset_id (str | None): The archive folder asset ID of the live channel.
            enable_high_availability (bool | None): Indicates if the live channel is enabled for high availability.
            enable_live_clipping (bool | None): Indicates if the live channel is enabled for live clipping.
            is_secure_output (bool | None): Indicates if the live channel is secure output.
            is_output_screenshot (bool | None): Indicates if the live channel is output screenshot.
            channel_type (str | None): The type of the live channel. The types are External, IVS, Normal, and Realtime.
            external_service_api_url (str | None): The external service API URL of the live channel.
                Only required if the type is External.
            security_groups (str | None): The security groups of the live channel.
                The security groups are: Content Manager, Everyone, and Guest.

        Returns:
            dict: The information of the live channel.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start update live channel")

            live_channel_info: dict | None = _update_live_channel(
                self, live_channel_id, name, thumbnail_image_id, archive_folder_asset_id, enable_high_availability,
                enable_live_clipping, is_secure_output, is_output_screenshot, channel_type, external_service_api_url,
                security_groups
            )

            if live_channel_info is not None:
                logging.info("Update live channel complete")

            return live_channel_info
        except Exception as error:
            logging.error("Update live channel failed")
            raise error

    # Live Input
    def create_live_input(
        self,
        name: str | None,
        source: str | None,
        input_type: str | None,
        is_standard: bool | None,
        video_asset_id: str | None,
        destinations: list[dict],
        sources: list[dict] | None
    ) -> dict | None:
        """
        Creates a live input.

        Args:
            name (str | None): The name of the live input.
            source (str | None): The souce of the live input.
            input_type (str | None): The type of the live input. The types are RTMP_PULL, RTMP_PUSH,
                RTP_PUSH, UDP_PUSH and URL_PULL
            is_standard (bool | None): Indicates if the live input is standard.
            video_asset_id (str | None): The video asset ID of the live input.
            destinations (list[dict] | None): The destinations of the live input. Sources must be URLs and are
                only valid for input types: RTMP_PUSH, URL_PULL, and MP4_FILE.
                dict format: {"ip": "str | None", "port": "str | None", "url": "str | None"}
            sources (list[dict] | None): The sources of the live input. Sources must be URLs and are
                only valid for input types: RTMP_PULL.
                dict format: {"ip": "str | None", "port": "str | None", "url": "str | None"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start create live input")

            live_channel_info: dict | None = _create_live_input(
                self, name, source, input_type, is_standard, video_asset_id, destinations, sources
            )

            if live_channel_info is not None:
                logging.info("Create live input complete")

            return live_channel_info
        except Exception as error:
            logging.error("Create live input failed")
            raise error

    def delete_live_input(self, live_input_id: str) -> None:
        """
        Deletes a live input.

        Args:
            live_input_id (str): The ID of the live input.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start delete live input")

            _delete_live_input(self, live_input_id)

            logging.info("Delete live input complete")
        except Exception as error:
            logging.error("Delete live input failed")
            raise error

    def get_live_input(self, live_input_id: str) -> dict | None:
        """
        Gets a live input.

        Args:
            live_input_id (str): The ID of the live input.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live input")

            live_channel_info: dict | None = _get_live_input(self, live_input_id)

            if live_channel_info is not None:
                logging.info("Get live input complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get live input failed")
            raise error

    def get_live_inputs(self) -> dict | None:
        """
        Gets all the live inputs.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live inputs")

            live_channel_info: dict | None = _get_live_inputs(self)

            if live_channel_info is not None:
                logging.info("Get live inputs complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get live inputs failed")
            raise error

    def update_live_input(
        self,
        live_input_id: str,
        name: str | None,
        source: str | None,
        input_type: str | None,
        is_standard: bool | None,
        video_asset_id: str | None,
        destinations: list[dict] | None,
        sources: list[dict] | None
    ) -> dict | None:
        """
        Updates a live input.

        Args:
            live_input_id (str): The ID of the live input.
            name (str | None): The name of the live input.
            source (str | None): The souce of the live input.
            input_type (str | None): The type of the live input. The types are RTMP_PULL, RTMP_PUSH,
                RTP_PUSH, UDP_PUSH and URL_PULL
            is_standard (bool | None): Indicates if the live input is standard.
            video_asset_id (str | None): The video asset ID of the live input.
            destinations (list[dict] | None): The destinations of the live input. Sources must be URLs and are
                only valid for input types: RTMP_PUSH, URL_PULL, and MP4_FILE.
                dict format: {"ip": "str | None", "port": "str | None", "url": "str | None"}
            sources (list[dict] | None): The sources of the live input. Sources must be URLs and are
                only valid for input types: RTMP_PULL.
                dict format: {"ip": "str | None", "port": "str | None", "url": "str | None"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start update live input")

            live_channel_info: dict | None = _update_live_input(
                self, live_input_id, name, source, input_type, is_standard, video_asset_id, destinations, sources
            )

            if live_channel_info is not None:
                logging.info("Update live input complete")

            return live_channel_info
        except Exception as error:
            logging.error("Update live input failed")
            raise error

    # Live Operator
    def cancel_broadcast(self, live_operator_id: str) -> None:
        """
        Cancels a broadcast.

        Args:
            live_operator_id (str): The ID of the live operator.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start cancel broadcast")

            _cancel_broadcast(self, live_operator_id)

            logging.info("Cancel broadcast complete")
        except Exception as error:
            logging.error("Cancel broadcast failed")
            raise error

    def cancel_segment(self, live_operator_id: str) -> None:
        """
        Cancels a segment.

        Args:
            live_operator_id (str): The ID of the live operator.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start cancel segment")

            _cancel_segment(self, live_operator_id)

            logging.info("Cancel segment complete")
        except Exception as error:
            logging.error("Cancel segment failed")
            raise error

    def complete_segment(
        self,
        live_operator_id: str,
        related_content_ids: list[str] | None,
        tag_ids: list[str] | None
    ) -> None:
        """
        Completes a segment.

        Args:
            live_operator_id (str): The ID of the live operator.
            related_content_ids (list | None): The related content IDs of the live operator.
            tag_ids (list | None): The tag IDs of the live operator.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start complete segment")

            _complete_segment(self, live_operator_id, related_content_ids, tag_ids)

            logging.info("Complete segment complete")
        except Exception as error:
            logging.error("Complete segment failed")
            raise error

    def get_completed_segments(self, live_operator_id: str) -> dict | None:
        """
        Gets completed segments for given id.

        Args:
            live_operator_id (str): The ID of the live operator.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get completed segments")

            live_channel_info: dict | None = _get_completed_segments(self, live_operator_id)

            if live_channel_info is not None:
                logging.info("Get completed segments complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get completed segments failed")
            raise error

    def get_live_operator(self, live_operator_id: str) -> dict | None:
        """
        Gets the live operator.

        Args:
            live_operator_id (str): The ID of the live operator.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live operator")

            live_channel_info: dict | None = _get_live_operator(self, live_operator_id)

            if live_channel_info is not None:
                logging.info("Get live operator complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get live operator failed")
            raise error

    def get_live_operators(self) -> dict | None:
        """
        Gets all the live operators.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live operators")

            live_channel_info: dict | None = _get_live_operators(self)

            if live_channel_info is not None:
                logging.info("Get live operators complete")

            return live_channel_info
        except Exception as error:
            logging.error("Get live operators failed")
            raise error

    def start_broadcast(
        self,
        live_operator_id: str,
        preroll_asset_id: str | None,
        postroll_asset_id: str | None,
        live_input_id: str | None,
        related_content_ids: list[str] | None,
        tag_ids: list[str] | None
    ) -> None:
        """
        Starts a broadcast.

        Args:
            live_operator_id (str): The ID of the live operator.
            preroll_asset_id (str | None): The preroll asset ID of the live operator.
            postroll_asset_id (str | None): The postroll asset ID of the live operator.
            live_input_id (str | None): The live input ID of the live operator.
            related_content_ids (list | None): The related content IDs of the live operator.
            tag_ids (list | None): The tag IDs of the live operator.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start start broadcast")

            start_broadcast_info: dict | None = _start_broadcast(
                self, live_operator_id, preroll_asset_id, postroll_asset_id, live_input_id,
                related_content_ids, tag_ids
            )

            if start_broadcast_info is not None:
                logging.info("Start broadcast complete")

            return start_broadcast_info
        except Exception as error:
            logging.error("Start broadcast failed")
            raise error

    def start_segment(self, live_operator_id: str) -> None:
        """
        Starts a segment.

        Args:
            live_operator_id (str): The ID of the live operator.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start start segment")

            _start_segment(self, live_operator_id)

            logging.info("Start segment complete")
        except Exception as error:
            logging.error("Start segment failed")
            raise error

    def stop_broadcast(self, live_operator_id: str) -> None:
        """
        Stops Broadcast.

        Args:
            live_operator_id (str): The ID of the live operator.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start stop broadcast")

            _stop_broadcast(self, live_operator_id)

            logging.info("Stop broadcast complete")
        except Exception as error:
            logging.error("Stop broadcast failed")
            raise error

    # Live Output Profile
    def create_live_output_profile(
        self,
        name: str,
        output_type: str | None,
        enabled: bool | None,
        audio_bitrate: int | None,
        output_stream_key: str | None,
        output_url: str | None,
        secondary_output_stream_key: str | None,
        secondary_url: str | None,
        video_bitrate: int | None,
        video_bitrate_mode: str | None,
        video_codec: str | None,
        video_frames_per_second: int | None,
        video_height: int | None,
        video_width: int | None
    ) -> dict | None:
        """
        Creates a live output profile.

        Args:
        name (str): The name of the live output profile.
        output_type (list | None): The type of the live output profile. Default is MediaStore.
            "MediaStore":"ac5146ea-4c01-4278-8c7b-0117f70c0100", Archive":"ac5146ea-4c01-4278-8c7b-0117f70c0200",
            "MediaPackage":"ac5146ea-4c01-4278-8c7b-0117f70c0300", "Rtmp":"ac5146ea-4c01-4278-8c7b-0117f70c0400",
            "S3":"ac5146ea-4c01-4278-8c7b-0117f70c0500", "LiveVodHls":"ac5146ea-4c01-4278-8c7b-0117f70c0600",
            "Rtp":"ac5146ea-4c01-4278-8c7b-0117f70c0700", "RtpFec":"ac5146ea-4c01-4278-8c7b-0117f70c0800"*
            dict format: {"name": "string", "id": "string"}
        enabled (bool | None): Indicates if the live output profile is enabled.
        audio_bitrate (int | None): The audio bitrate of the live output profile.
            The audio bitrate in bytes. For example, 128KB = 128000.
        output_stream_key (str | None): The output stream key of the live output profile.
        output_url (str | None): The output URL of the live output profile.
        secondary_output_stream_key (str | None): The secondary output stream key of the live output profile.
        secondary_url (str | None): The secondary URL of the live output profile.
        video_bitrate (int | None): The video bitrate of the live output profile.
            The video bitrate in bytes. For example, 2mbps = 2048000, validate > 0.
        video_bitrate_mode (str | None): The video bitrate mode of the live output profile. The modes are CBR and VBR.
        video_codec (str | None): The video codec of the live output profile. The codecs are H264 and H265.
        video_frames_per_second (int | None): The video frames per second of the live output profile.
        video_height (int | None): The video height of the live output profile.
        video_width (int | None): The video width of the live output profile.

        Returns:
            dict: The information of the live output profile.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start create live output profile")

            live_output_info: dict | None = _create_live_output_profile(
                self, name, output_type, enabled, audio_bitrate, output_stream_key, output_url,
                secondary_output_stream_key, secondary_url, video_bitrate, video_bitrate_mode,
                video_codec, video_frames_per_second, video_height, video_width
            )

            if live_output_info is not None:
                logging.info("Create live output profile complete")

            return live_output_info
        except Exception as error:
            logging.error("Create live output profile failed")
            raise error

    def delete_live_output_profile(self, live_output_id: str) -> None:
        """
        Deletes a live output profile.

        Args:
            live_output_id (str): The ID of the live output profile.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start delete live output profile")

            _delete_live_output_profile(self, live_output_id)

            logging.info("Delete live output profile complete")
        except Exception as error:
            logging.error("Delete live output profile failed")
            raise error

    def get_live_output_profile(self, live_output_id: str) -> dict | None:
        """
        Gets a live output profile.

        Args:
            live_output_id (str): The ID of the live output profile.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live output profile")

            live_output_info: dict | None = _get_live_output_profile(self, live_output_id)

            if live_output_info is not None:
                logging.info("Get live output profile complete")

            return live_output_info
        except Exception as error:
            logging.error("Get live output profile failed")
            raise error

    def get_live_output_profiles(self) -> list[dict] | None:
        """
        Gets all the live output profiles

        Returns:
            list[dict]: The information of the live output profiles.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live outputs")

            live_output_info: dict | None = _get_live_output_profiles(self)

            if live_output_info is not None:
                logging.info("Get live outputs complete")

            return live_output_info
        except Exception as error:
            logging.error("Get live outputs failed")
            raise error

    def get_live_output_types(self) -> dict | None:
        """
        Gets live output types

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live output types")

            live_output_info: dict | None = _get_live_output_types(self)

            if live_output_info is not None:
                logging.info("Get live output types complete")

            return live_output_info
        except Exception as error:
            logging.error("Get live output types failed")
            raise error

    def update_live_output_profile(
        self,
        live_output_id: str,
        name: str | None,
        output_type: str | None,
        enabled: bool | None,
        audio_bitrate: int | None,
        output_stream_key: str | None,
        output_url: str | None,
        secondary_output_stream_key: str | None,
        secondary_url: str | None,
        video_bitrate: int | None,
        video_bitrate_mode: str | None,
        video_codec: str | None,
        video_frames_per_second: int | None,
        video_height: int | None,
        video_width: int | None
    ) -> dict | None:
        """
        Updates a live output profile.

        Args:
            live_output_id (str): The ID of the live output profile.
            name (str | None): The name of the live output profile.
            output_type (list | None): The type of the live output profile. Default is MediaStore.
                "MediaStore":"ac5146ea-4c01-4278-8c7b-0117f70c0100", Archive":"ac5146ea-4c01-4278-8c7b-0117f70c0200",
                "MediaPackage":"ac5146ea-4c01-4278-8c7b-0117f70c0300", "Rtmp":"ac5146ea-4c01-4278-8c7b-0117f70c0400",
                "S3":"ac5146ea-4c01-4278-8c7b-0117f70c0500", "LiveVodHls":"ac5146ea-4c01-4278-8c7b-0117f70c0600",
                "Rtp":"ac5146ea-4c01-4278-8c7b-0117f70c0700", "RtpFec":"ac5146ea-4c01-4278-8c7b-0117f70c0800"*
                dict format: {"name": "string", "id": "string"}
            ENABLED (bool | None): Indicates if the live output profile is enabled.
            AUDIO_BITRATE (int | None): The audio bitrate of the live output profile.
            OUTPUT_STREAM_KEY (str | None): The output stream key of the live output profile.
            OUTPUT_URL (str | None): The output URL of the live output profile.
            SECONDARY_OUTPUT_STREAM_KEY (str | None): The secondary output stream key of the live output profile.
            SECONDARY_URL (str | None): The secondary URL of the live output profile.
            VIDEO_BITRATE (int | None): The video bitrate of the live output profile.
            VIDEO_BITRATE_MODE (str | None): The video bitrate mode of the live output profile. The modes are CBR and VBR.
            VIDEO_CODEC (str | None): The video codec of the live output profile. The codecs are H264 and H265.
            VIDEO_FRAMES_PER_SECOND (int | None): The video frames per second of the live output profile.
            VIDEO_HEIGHT (int | None): The video height of the live output profile.
            VIDEO_WIDTH (int | None): The video width of the live output profile.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start update live output profile")

            live_output_info: dict | None = _update_live_output_profile(
                self, live_output_id, name, output_type, enabled, audio_bitrate, output_stream_key,
                output_url, secondary_output_stream_key, secondary_url, video_bitrate, video_bitrate_mode,
                video_codec, video_frames_per_second, video_height, video_width
            )

            if live_output_info is not None:
                logging.info("Update live output profile complete")

            return live_output_info
        except Exception as error:
            logging.error("Update live output profile failed")
            raise error

    # Live Output Profile Group
    def create_live_output_profile_group(
        self,
        name: str,
        is_enabled: bool,
        manifest_type: str,
        is_default_group: bool,
        live_output_type: list,
        archive_live_output_profile: list | None,
        live_output_profiles: list
    ) -> dict | None:
        """
        Creates a live output profile group.

        Args:
            name (str): The name of the live output profile group.
            is_enabled (bool): Indicates if the live output profile group is enabled.
            manifest_type (str): The manifest type of the live output profile group. The types are HLS, DASH, and BOTH.
            is_default_group (bool): Indicates if the live output profile group is the default group.
            live_output_type (list | None): The type of the live output profile. Default is MediaStore.
                "MediaStore":"ac5146ea-4c01-4278-8c7b-0117f70c0100", Archive":"ac5146ea-4c01-4278-8c7b-0117f70c0200",
                "MediaPackage":"ac5146ea-4c01-4278-8c7b-0117f70c0300", "Rtmp":"ac5146ea-4c01-4278-8c7b-0117f70c0400",
                "S3":"ac5146ea-4c01-4278-8c7b-0117f70c0500", "LiveVodHls":"ac5146ea-4c01-4278-8c7b-0117f70c0600",
                "Rtp":"ac5146ea-4c01-4278-8c7b-0117f70c0700", "RtpFec":"ac5146ea-4c01-4278-8c7b-0117f70c0800"*
                dict format: {"name": "string", "id": "string"}
            live_output_type (list): The type of the live output profile group.
                dict format: {"description": "string", "id": "string"}
            archive_live_output_profile (list | None): The archive live output profile of the live output profile group.
                dict format: {"description": "string", "id": "string"}
            live_output_profiles (list): The live output profile of the live output profile group.

        Returns:
            dict: The JSON response from the server if the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start create live output profile group")

            live_output_profile_group_info: dict | None = _create_live_output_profile_group(
                self, name, is_enabled, manifest_type, is_default_group, live_output_type,
                archive_live_output_profile, live_output_profiles
            )

            if live_output_profile_group_info is not None:
                logging.info("Create live output profile group complete")

            return live_output_profile_group_info
        except Exception as error:
            logging.error("Create live output profile group failed")
            raise error

    def delete_live_output_profile_group(self, live_output_profile_group_id: str) -> None:
        """
        Deletes a live output profile group.

        Args:
            live_output_profile_group_id (str): The ID of the live output profile group.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start delete live output profile group")

            _delete_live_output_profile_group(self, live_output_profile_group_id)

            logging.info("Delete live output profile group complete")
        except Exception as error:
            logging.error("Delete live output profile group failed")
            raise error

    def get_live_output_profile_group(self, live_output_profile_group_id: str) -> dict | None:
        """
        Gets a live output profile group.

        Args:
            live_output_profile_group_id (str): The ID of the live output profile group.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live output profile group")

            live_output_profile_group_info: dict | None = _get_live_output_profile_group(
                self, live_output_profile_group_id
            )

            if live_output_profile_group_info is not None:
                logging.info("Get live output profile group complete")

            return live_output_profile_group_info
        except Exception as error:
            logging.error("Get live output profile group failed")
            raise error

    def get_live_output_profile_groups(self) -> dict | None:
        """
        Gets all the live output profile groups.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start get live output profile groups")

            live_output_profile_group_info: dict | None = _get_live_output_profile_groups(self)

            if live_output_profile_group_info is not None:
                logging.info("Get live output profile groups complete")

            return live_output_profile_group_info
        except Exception as error:
            logging.error("Get live output profile groups failed")
            raise error

    def update_live_output_profile_group(
        self,
        live_output_profile_group_id: str,
        name: str | None,
        is_enabled: bool | None,
        manifest_type: str | None,
        is_default_group: bool | None,
        live_output_type: list | None,
        archive_live_output_profile: list | None,
        live_output_profile: list | None
    ) -> dict | None:
        """
        Updates a live output profile group.

        Args:
            live_output_profile_group_id (str): The ID of the live output profile group.
            name (str | None): The name of the live output profile group.
            is_enabled (bool | None): Indicates if the live output profile group is enabled.
            manifest_type (str | None): The manifest type of the live output profile group.
            is_default_group (bool | None): Indicates if the live output profile group is the default group.
            live_output_type (list | None): The type of the live output profile. Default is MediaStore.
                "MediaStore":"ac5146ea-4c01-4278-8c7b-0117f70c0100", Archive":"ac5146ea-4c01-4278-8c7b-0117f70c0200",
                "MediaPackage":"ac5146ea-4c01-4278-8c7b-0117f70c0300", "Rtmp":"ac5146ea-4c01-4278-8c7b-0117f70c0400",
                "S3":"ac5146ea-4c01-4278-8c7b-0117f70c0500", "LiveVodHls":"ac5146ea-4c01-4278-8c7b-0117f70c0600",
                "Rtp":"ac5146ea-4c01-4278-8c7b-0117f70c0700", "RtpFec":"ac5146ea-4c01-4278-8c7b-0117f70c0800"*
                dict format: {"name": "string", "id": "string"}
            archive_live_output_profile (list | None): The archive live output profile of the live output profile group.
                dict format: {"description": "string", "id": "string"}
            live_output_profile (list | None): The live output profile of the live output profile group.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Start update live output profile group")

            live_output_profile_group_info: dict | None = _update_live_output_profile_group(
                self, live_output_profile_group_id, name, is_enabled, manifest_type, is_default_group,
                live_output_type, archive_live_output_profile, live_output_profile
            )

            if live_output_profile_group_info is not None:
                logging.info("Update live output profile group complete")

            return live_output_profile_group_info
        except Exception as error:
            logging.error("Update live output profile group failed")
            raise error

    # Schedule
    def create_intelligent_playlist(
        self,
        collections: list[dict] | None,
        end_search_date: str | None,
        end_search_duration_in_minutes: int,
        name: str,
        related_contents: list[dict] | None,
        search_date: str | None,
        search_duration_in_minutes: int,
        search_filter_type: int,
        tags: list[dict],
        thumbnail_asset: dict | None
    ) -> dict | None:
        """
        Creates an intelligent playlist.

        Args:
            collections (list[dict] | None): The collections of the intelligent playlist.
                Format: {"id": "string", "description": "string"}
            end_search_date (str | None): The end search date of the intelligent playlist.
                Only use when search_filter_type = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
            end_search_duration_in_minutes (int): The end search duration in minutes of the intelligent playlist.
            name (str): The name of the intelligent playlist.
            related_contents (list[dict] | None): The related content of the intelligent playlist.
                Format: {"id": "string", "description": "string"}
            search_date (str | None): The search date of the intelligent playlist. Only use when SEARCH_FILTER_TYPE = 2.
                Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
            search_duration_in_minutes (int): The search duration in minutes of the intelligent playlist.
            search_filter_type (int): The search filter type of the intelligent playlist.
                Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
            tags (list[dict]): The tags of the intelligent playlist. Format: {"id": "string", "description": "string"}
            thumbnail_asset (dict | None): The thumbnail asset of the intelligent playlist.
                Format: {"id": "string", "description": "string"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating intelligent playlist")

            intelligent_playlist_info: dict | None = _create_intelligent_playlist(
                self, collections, end_search_date, end_search_duration_in_minutes, name, related_contents,
                search_date, search_duration_in_minutes, search_filter_type, tags, thumbnail_asset
            )

            if intelligent_playlist_info is not None:
                logging.info("Intelligent playlist created")

            return intelligent_playlist_info
        except Exception as error:
            logging.error("Create intelligent playlist failed")
            raise error

    def create_intelligent_schedule(
        self,
        default_video_asset: dict,
        name: str,
        thumbnail_asset: dict | None,
        time_zone_id: str | None
    ) -> dict | None:
        """
        Creates an intelligent schedule.

        Args:
            default_video_asset (dict): The default video asset of the intelligent schedule. Format: {"id": "string", "description": "string"}
            name (str): The name of the intelligent schedule.
            thumbnail_asset (dict | None): The thumbnail asset of the intelligent schedule. Format: {"id": "string", "description": "string"}
            time_zone_id (str | None): The time zone ID of the intelligent schedule.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating intelligent schedule")

            intelligent_schedule_info: dict | None = _create_intelligent_schedule(
                self, default_video_asset, name, thumbnail_asset, time_zone_id
            )

            if intelligent_schedule_info is not None:
                logging.info("Intelligent schedule created")

            return intelligent_schedule_info
        except Exception as error:
            logging.error("Create intelligent schedule failed")
            raise error

    def create_playlist(
        self,
        name: str,
        thumbnail_asset: dict | None,
        loop_playlist: bool,
        default_video_asset: dict
    ) -> dict | None:
        """
        Creates a playlist.

        Args:
            name (str): The name of the playlist.
            thumbnail_asset (dict | None): The thumbnail asset of the playlist.
                Format: {"id": "string", "description": "string"}
            loop_playlist (bool): Whether the playlist is looped.
            default_video_asset (dict): The default video asset of the playlist.
                Format: {"id": "string"}. Only needed if loop_playlist is false.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating playlist")

            playlist_info: dict | None = _create_playlist(
                self, name, thumbnail_asset, loop_playlist, default_video_asset)

            if playlist_info is not None:
                logging.info("Playlist created")

            return playlist_info
        except Exception as error:
            logging.error("Create playlist failed")
            raise error

    def create_playlist_video(self, playlist_id: str, video_asset: dict, previous_item: str | None) -> dict | None:
        """
        Creates a playlist video.

        Args:
            playlist_id (str): The ID of the playlist.
            video_asset (dict): The video asset of the playlist video.
                Format: {"id": "string", "description": "string"}
            previous_item (str | None): The previous item of the playlist video.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating playlist video")

            playlist_video_info: dict | None = _create_playlist_video(
                self, playlist_id, video_asset, previous_item
            )

            if playlist_video_info is not None:
                logging.info("Playlist video created")

            return playlist_video_info
        except Exception as error:
            logging.error("Create playlist video failed")
            raise error

    def create_schedule_item_asset(
        self,
        schedule_id: str,
        asset: dict,
        days: list[dict],
        duration_time_code: str,
        end_time_code: str,
        previous_item: str | None,
        time_code: str
    ) -> dict | None:
        """
        Creates a schedule item asset.

        Args:
            schedule_id (str): The id of the schedule the asset item is to be added to.
            asset (dict): The asset of the schedule item asset. Format: {"id": "string"}
            days (list[dict]): The days of the schedule item asset. Format: {"id": "string"}
            duration_time_code (str): The duration time between time_code and end_time_code.
                Please use the following format: The content security attribute can be "Undefined", "Guest", or "Demo".hh:mm:ss;ff.
            end_time_code (str): The end time code of the schedule item asset.
                Please use the following format: hh:mm:ss;ff.
            previous_item (str | None): The previous item of the schedule item asset.
            time_code (str): The time code of the schedule item asset.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating schedule item asset")

            schedule_item_asset_info: dict | None = _create_schedule_item_asset(
                self, schedule_id, asset, days, duration_time_code, end_time_code, previous_item, time_code
            )

            if schedule_item_asset_info is not None:
                logging.info("Schedule item asset created")

            return schedule_item_asset_info
        except Exception as error:
            logging.error("Create schedule item asset failed")
            raise error

    def create_schedule_item_live_channel(
        self,
        schedule_id: str,
        days: list[dict],
        duration_time_code: str,
        end_time_code: str,
        live_channel: dict,
        previous_item: str | None,
        time_code: str
    ) -> dict | None:
        """
        Creates a schedule item live channel.

        Args:
            schedule_id (str): The id of the schedule the live channel item is to be added to.
            days (list[dict]): The days of the schedule item live channel.
                Format: {"id": "string", "description": "string"}
            duration_time_code (str): The duration time between time_code and end_time_code.
                Please use the following format: hh:mm:ss;ff.
            end_time_code (str): The end time code of the schedule item live channel.
                Please use the following format: hh:mm:ss;ff.
            live_channel (dict): The live channel of the schedule item live channel.
                Format: {"id": "string", "description": "string"}.
                Note: The live channel must be non-secure output.
            previous_item (str | None): The previous item of the schedule item live channel.
            time_code (str): The time code of the schedule item live channel.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating schedule item live channel")

            schedule_item_live_channel_info: dict | None = _create_schedule_item_live_channel(
                self, schedule_id, days, duration_time_code, end_time_code, live_channel,
                previous_item, time_code
            )

            if schedule_item_live_channel_info is not None:
                logging.info("Schedule item live channel created")

            return schedule_item_live_channel_info
        except Exception as error:
            logging.error("Create schedule item live channel failed")
            raise error

    def create_schedule_item_playlist_schedule(
        self,
        schedule_id: str,
        days: list[dict],
        duration_time_code: str,
        end_time_code: str,
        playlist_schedule: dict,
        previous_item: str | None,
        time_code: str
    ) -> dict | None:
        """
        Creates a schedule item playlist schedule.

        Args:
            schedule_id (str): The id of the schedule the playlist schedule item is to be added to.
            days (list[dict]): The days of the schedule item playlist schedule.
                Format: {"id": "string", "description": "string"}
            duration_time_code (str): The duration time between time_code and end_time_code.
                Please use the following format: hh:mm:ss;ff.
            end_time_code (str): The end time code of the schedule item playlist schedule.
                Please use the following format: hh:mm:ss;ff.
            playlist_schedule (dict): The playlist schedule of the schedule item playlist schedule.
                Format: {"id": "string", "description": "string"}
            previous_item (str | None): The previous item of the schedule item playlist schedule.
            time_code (str): The time code of the schedule item playlist schedule.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: This JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating schedule item playlist schedule")

            schedule_item_playlist_schedule_info: dict | None = _create_schedule_item_playlist_schedule(
                self, schedule_id, days, duration_time_code, end_time_code, playlist_schedule,
                previous_item, time_code)

            if schedule_item_playlist_schedule_info is not None:
                logging.info("Schedule item playlist schedule created")

            return schedule_item_playlist_schedule_info
        except Exception as error:
            logging.error("Create schedule item playlist schedule failed")
            raise error

    def create_schedule_item_search_filter(
        self,
        schedule_id: str,
        collections: list[dict] | None,
        days: list[dict],
        duration_time_code: str,
        end_search_date: str | None,
        end_search_duration_in_minutes: int,
        end_time_code: str,
        previous_item: str | None,
        related_contents: list[dict] | None,
        search_date: str | None,
        search_duration_in_minutes: int,
        search_filter_type: int,
        tags: list[dict],
        time_code: str
    ) -> dict | None:
        """
        Creates a schedule item search filter.

        Args:
            schedule_id (str): The id of the schedule the search filter item is to be added to.
            collections (list[dict] | None): The collections of the schedule item search filter.
                Format: {"id": "string", "description": "string"}
            days (list[dict]): The days of the schedule item search filter.
                Format: {"id": "string", "description": "string"}
            duration_time_code (str): The duration time between time_code and end_time_code.
                Please use the following format: hh:mm:ss;ff.
            end_search_date (str | None): The end search date of the schedule item search filter.
                Only use when SEARCH_FILTER_TYPE = 2. yyyy-MM-dd.THH:MM:SS.FFFZ.
            end_search_duration_in_minutes (int): The end search duration in minutes of the schedule
                item search filter.
            end_time_code (str): The end time code of the schedule item search filter.
                Please use the following format: hh:mm:ss;ff.
            previous_item (str | None): The previous item of the schedule item search filter.
            related_contents (list[dict] | None): The related contents of the schedule item search filter.
            search_date (str | None): The search date of the schedule item search filter.
                Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
            search_duration_in_minutes (str): The search duration in minutes of the schedule
                item search filter.
            search_filter_type (str): The search filter type of the schedule item search filter.
                Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
            tags (list[dict]): The tags of the schedule item search filter.
                Format: {"id": "string", "description": "string"}
            time_code (str): The time code of the schedule item search filter.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating schedule item search filter")

            schedule_item_search_filter_info: dict | None = _create_schedule_item_search_filter(
                self, schedule_id, collections, days, duration_time_code, end_search_date,
                end_search_duration_in_minutes, end_time_code, previous_item, related_contents,
                search_date, search_duration_in_minutes, search_filter_type, tags, time_code
            )

            if schedule_item_search_filter_info is not None:
                logging.info("Schedule item search filter created")

            return schedule_item_search_filter_info
        except Exception as error:
            logging.error("Create schedule item search filter failed")
            raise error

    def delete_intelligent_playlist(self, schedule_id: str) -> None:
        """
        Deletes an intelligent playlist.

        Args:
            schedule_id (str): The id of the intelligent playlist to be deleted.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting intelligent playlist")

            _delete_intelligent_playlist(self, schedule_id)

            logging.info("Intelligent playlist deleted")
        except Exception as error:
            logging.error("Delete intelligent playlist failed")
            raise error

    def delete_intelligent_schedule(self, schedule_id: str) -> None:
        """
        Deletes a schedule.

        Args:
            schedule_id (str): The id of the intelligent schedule to be deleted.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting intelligent schedule")

            _delete_intelligent_schedule(self, schedule_id)

            logging.info("Intelligent schedule deleted")
        except Exception as error:
            logging.error("Delete intelligent schedule failed")
            raise error

    def delete_playlist(self, schedule_id: str) -> None:
        """
        Deletes a playlist.

        Args:
            schedule_id (str): The id of the playlist to be deleted.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting playlist")

            _delete_playlist(self, schedule_id)

            logging.info("Playlist deleted")
        except Exception as error:
            logging.error("Delete playlist failed")
            raise error

    def delete_schedule_item(self, schedule_id: str, item_id: str) -> None:
        """
        Deletes a schedule item.

        Args:
            schedule_id (str): The id of the schedule the schedule item is to be deleted from.
            item_id (str): The id of the item to be deleted.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting schedule item")

            _delete_schedule_item(self, schedule_id, item_id)

            logging.info("Schedule item deleted")
        except Exception as error:
            logging.error("Delete schedule item failed")
            raise error

    def get_intelligent_playlist(self, schedule_id: str) -> dict | None:
        """
        Gets an intelligent playlist.

        Args:
            schedule_id (str): The id of the intelligent playlist to be gotten.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting intelligent playlist")

            intelligent_playlist_info: dict | None = _get_intelligent_playlist(self, schedule_id)

            if intelligent_playlist_info is not None:
                logging.info("Intelligent playlist gotten")

            return intelligent_playlist_info
        except Exception as error:
            logging.error("Get intelligent playlist failed")
            raise error

    def get_intelligent_schedule(self, schedule_id: str) -> dict | None:
        """
        Gets an intelligent schedule.

        Args:
            schedule_id (str): The id of the intelligent schedule to be gotten.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting intelligent schedule")

            intelligent_schedule_info: dict | None = _get_intelligent_schedule(self, schedule_id)

            if intelligent_schedule_info is not None:
                logging.info("Intelligent schedule gotten")

            return intelligent_schedule_info
        except Exception as error:
            logging.error("Get intelligent schedule failed")
            raise error

    def get_playlist(self, schedule_id: str) -> dict | None:
        """
        Gets a playlist.

        Args:
            schedule_id (str): The id of the playlist to be gotten.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting playlist")

            playlist_info: dict | None = _get_playlist(self, schedule_id)

            if playlist_info is not None:
                logging.info("Playlist gotten")

            return playlist_info
        except Exception as error:
            logging.error("Get playlist failed")
            raise error

    def get_schedule_item(self, schedule_id: str, item_id: str) -> dict | None:
        """
        Gets a schedule item.

        Args:
            schedule_id (str): The id of the schedule the schedule item is to be gotten from.
            item_id (str): The id of the item to be gotten.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting schedule item")

            schedule_item_info: dict | None = _get_schedule_item(self, schedule_id, item_id)

            if schedule_item_info is not None:
                logging.info("Schedule item gotten")

            return schedule_item_info
        except Exception as error:
            logging.error("Get schedule item failed")
            raise error

    def get_schedule_items(self, schedule_id: str) -> list[dict] | None:
        """
        Gets the schedule items of a schedule.

        Args:
            schedule_id (str): The id of the schedule the schedule items are to be gotten from.

        Returns:
            list[dict]: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting schedule items")

            schedule_items_info: dict | None = _get_schedule_items(self, schedule_id)

            if schedule_items_info is not None:
                logging.info("Schedule items gotten")

            return schedule_items_info
        except Exception as error:
            logging.error("Get schedule items failed")
            raise error

    def get_schedule_preview(self, schedule_id: str) -> dict | None:
        """
        Gets a schedule preview.

        Args:
            schedule_id (str): The id of the schedule the schedule preview is to be gotten from.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting schedule preview")

            schedule_preview_info: dict | None = _get_schedule_preview(self, schedule_id)

            if schedule_preview_info is not None:
                logging.info("Schedule preview gotten")

            return schedule_preview_info
        except Exception as error:
            logging.error("Get schedule preview failed")
            raise error

    def move_schedule_item(self, schedule_id: str, item_id: str, previous_item: str | None) -> dict | None:
        """
        Moves a schedule item.

        Args:
            schedule_id (str): The id of the schedule the schedule item is to be moved from.
            item_id (str): The id of the item to be moved.
            previous_item (str | None): The previous item of the schedule item.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Moving schedule item")

            schedule_item_info: dict | None = _move_schedule_item(self, schedule_id, item_id, previous_item)

            if schedule_item_info is not None:
                logging.info("Schedule item moved")

            return schedule_item_info
        except Exception as error:
            logging.error("Move schedule item failed")
            raise error

    def publish_intelligent_schedule(self, schedule_id: str, number_of_locked_days: int) -> dict | None:
        """
        Publishes an intelligent schedule.

        Args:
            schedule_id (str): The id of the schedule to be published.
            number_of_locked_days (int): The number of locked days of the intelligent schedule.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Publishing intelligent schedule")

            info: dict | None = _publish_intelligent_schedule(self, schedule_id, number_of_locked_days)

            if info is not None:
                logging.info("Intelligent schedule published")

            return info
        except Exception as error:
            logging.error("Publish intelligent schedule failed")
            raise error

    def start_schedule(self, schedule_id: str, skip_cleanup_on_failure: bool | None) -> dict | None:
        """
        Starts a schedule.

        Args:
            schedule_id (str): The id of the schedule to be started.
            skip_cleanup_on_failure (bool | None): Whether or not to skip cleanup on failure.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Starting schedule")

            schedule_info: dict | None = _start_schedule(self, schedule_id, skip_cleanup_on_failure)

            if schedule_info is not None:
                logging.info("Schedule started")

            return schedule_info
        except Exception as error:
            logging.error("Start schedule failed")
            raise error

    def stop_schedule(self, schedule_id: str, force_stop: bool | None) -> dict | None:
        """
        Stops a schedule.

        Args:
            schedule_id (str): The id of the schedule to be stopped.
            force_stop (bool | None): Whether or not to force a stop.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Stopping schedule")

            schedule_info: dict | None = _stop_schedule(self, schedule_id, force_stop)

            if schedule_info is not None:
                logging.info("Schedule stopped")

            return schedule_info
        except Exception as error:
            logging.error("Stop schedule failed")
            raise error

    def update_intelligent_playlist(
            self,
            schedule_id: str,
            collections: list[dict] | None,
            end_search_date: str | None,
            end_search_duration_in_minutes: int | None,
            name: str | None,
            related_contents: list[dict] | None,
            search_date: str | None,
            search_duration_in_minutes: int | None,
            search_filter_type: int | None,
            tags: list[dict] | None,
            thumbnail_asset: dict | None) -> dict | None:
        """
        Updates an intelligent playlist.

        Args:
            schedule_id (str): The id of the schedule the intelligent playlist is to be updated.
            collections (list[dict] | None): The collections of the intelligent playlist.
                dict format: {"id": "string", "description": "string"}
            end_search_date (str | None): The end search date of the intelligent playlist.
                Only use when search_filter_type = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
            end_search_duration_in_minutes int | None: The end search duration in minutes of the intelligent playlist.
            name (str | None): The name of the intelligent playlist.
            related_contents (list[dict] | None): The related content of the intelligent playlist.
            search_date (str | None): The search date of the intelligent playlist.
                Only use when search_filter_type = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
            search_duration_in_minutes int | None: The search duration in minutes of the intelligent playlist.
            search_filter_type (str | None): The search filter type of the intelligent playlist.
                Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
            tags (list[dict] | None): The tags of the intelligent playlist.
            thumbnail_asset (dict | None): The thumbnail asset of the intelligent playlist.
                dict format: {"id": "string", "description": "string"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating intelligent playlist")

            intelligent_playlist_info: dict | None = _update_intelligent_playlist(
                self, schedule_id, collections, end_search_date, end_search_duration_in_minutes, name,
                related_contents, search_date, search_duration_in_minutes, search_filter_type, tags, thumbnail_asset
            )

            if intelligent_playlist_info is not None:
                logging.info("Intelligent playlist updated")

            return intelligent_playlist_info
        except Exception as error:
            logging.error("Update intelligent playlist failed")
            raise error

    def update_intelligent_schedule(
        self,
        schedule_id: str,
        default_video_asset: dict,
        name: str | None,
        thumbnail_asset: dict | None,
        time_zone_id: str | None
    ) -> dict | None:
        """
        Updates an intelligent schedule.

        Args:
            schedule_id (str): The id of the schedule the intelligent schedule is to be updated.
            default_video_asset (dict): The default video asset of the intelligent schedule.
                dict format: {"id": "string", "description": "string"}
            name (str | None): The name of the intelligent schedule.
            thumbnail_asset (dict | None): The thumbnail asset of the intelligent schedule.
                dict format: {"id": "string", "description": "string"}
            time_zone_id (str | None): The time zone id of the intelligent schedule.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating intelligent schedule")

            intelligent_schedule_info: dict | None = _update_intelligent_schedule(
                self, schedule_id, default_video_asset, name, thumbnail_asset, time_zone_id
            )

            if intelligent_schedule_info is not None:
                logging.info("Intelligent schedule updated")

            return intelligent_schedule_info
        except Exception as error:
            logging.error("Update intelligent schedule failed")
            raise error

    def update_playlist(
        self,
        schedule_id: str,
        default_video_asset: dict | None,
        loop_playlist: bool | None,
        name: str | None,
        thumbnail_asset: dict | None
    ) -> dict | None:
        """
        Updates a playlist.

        Args:
            schedule_id (str): The id of the schedule the playlist is to be updated from.
            default_video_asset (list[dict] | None): The default video asset of the playlist.
                dict format: {"id": "string", "description": "string"}
            loop_playlist (bool | None): Whether or not to loop the playlist.
            name (str | None): The name of the playlist.
            thumbnail_asset (dict | None): The thumbnail asset of the playlist.
                dict format: {"id": "string", "description": "string"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating playlist")

            playlist_info: dict | None = _update_playlist(
                self, schedule_id, default_video_asset, loop_playlist, name, thumbnail_asset
            )

            if playlist_info is not None:
                logging.info("Playlist updated")

            return playlist_info
        except Exception as error:
            logging.error("Update playlist failed")
            raise error

    def update_playlist_video(self, playlist_id: str, item_id: str, asset: dict | None) -> dict | None:
        """
        Updates a playlist video.

        Args:
            playlist_id (str): The id of the schedule the playlist video is to be updated from.
            item_id (str): The id of the item to be updated.
            asset (dict | None): The asset of the playlist video.
                dict format: {"id": "string", "description": "string"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating playlist video")

            playlist_video_info: dict | None = _update_playlist_video(self, playlist_id, item_id, asset)

            if playlist_video_info is not None:
                logging.info("Playlist video updated")

            return playlist_video_info
        except Exception as error:
            logging.error("Update playlist video failed")
            raise error

    def update_schedule_item_asset(
        self,
        schedule_id: str,
        item_id: str,
        asset: dict | None,
        days: list[dict] | None,
        duration_time_code: str | None,
        end_time_code: str | None,
        time_code: str | None
    ) -> dict | None:
        """
        Updates a schedule item asset.

        Args:
            schedule_id (str): The id of the schedule the schedule item asset is to be updated from.
            item_id (str): The id of the item to be updated.
            asset (dict | None): The asset of the schedule item asset.
                dict format: {"id": "string", "description": "string"}
            days (list[dict] | None): The days of the schedule item asset.
                dict format: {"id": "string", "description": "string"}
            duration_time_code (str | None): The duration time between time_code and end_time_code.
                Please use the following format: hh:mm:ss;ff.
            end_time_code (str | None): The end time code of the schedule item asset.
                Please use the following format: hh:mm:ss;ff.
            time_code (str | None): The time code of the schedule item asset.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating schedule item asset")

            schedule_item_asset_info: dict | None = _update_schedule_item_asset(
                self, schedule_id, item_id, asset, days, duration_time_code, end_time_code, time_code)

            if schedule_item_asset_info is not None:
                logging.info("Schedule item asset updated")

            return schedule_item_asset_info
        except Exception as error:
            logging.error("Update schedule item asset failed")
            raise error

    def update_schedule_item_live_channel(
        self,
        schedule_id: str,
        item_id: str,
        days: list[dict] | None,
        duration_time_code: str | None,
        end_time_code: str | None,
        live_channel: dict | None,
        time_code: str | None
    ) -> dict | None:
        """
        Updates a schedule item live channel.

        Args:
            schedule_id (str): The id of the schedule the schedule item live channel is to be updated from.
            item_id (str): The id of the item to be updated.
            days (list[dict] | None): The days of the schedule item live channel.
                dict format: {"id": "string", "description": "string"}
            duration_time_code (str | None): The duration time between time_code and end_time_code.
                Please use the following format: hh:mm:ss;ff.
            end_time_code (str | None): The end time code of the schedule item live channel.
                Please use the following format: hh:mm:ss;ff.
            live_channel (dict | None): The live channel of the schedule item live channel.
                dict format: {"id": "string", "description": "string"}
            time_code (str | None): The time code of the schedule item live channel.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating schedule item live channel")

            schedule_item_live_channel_info: dict | None = _update_schedule_item_live_channel(
                self, schedule_id, item_id, days, duration_time_code, end_time_code, live_channel, time_code
            )

            if schedule_item_live_channel_info is not None:
                logging.info("Schedule item live channel updated")

            return schedule_item_live_channel_info
        except Exception as error:
            logging.error("Update schedule item live channel failed")
            raise error

    def update_schedule_item_playlist_schedule(
        self,
        schedule_id: str,
        item_id: str,
        days: list[dict] | None,
        duration_time_code: str | None,
        end_time_code: str | None,
        playlist_schedule: dict | None,
        time_code: str | None
    ) -> dict | None:
        """
        Updates a schedule item playlist schedule.

        Args:
            schedule_id (str): The id of the schedule the schedule item playlist schedule is to be updated from.
            item_id (str): The id of the item to be updated.
            days (list[dict] | None): The days of the schedule item playlist schedule.
                dict format: {"id": "string", "description": "string"}
            duration_time_code (str | None): The duration time between time_code and end_time_code.
                Please use the following format: hh:mm:ss;ff.
            end_time_code (str | None): The end time code of the schedule item playlist schedule.
                Please use the following format: hh:mm:ss;ff.
            playlist_schedule (dict | None): The playlist schedule of the schedule item playlist schedule.
                dict format: {"id": "string", "description": "string"}
            time_code (str | None): The time code of the schedule item playlist schedule.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating schedule item playlist schedule")

            schedule_item_playlist_schedule_info: dict | None = _update_schedule_item_playlist_schedule(
                self, schedule_id, item_id, days, duration_time_code, end_time_code, playlist_schedule, time_code
            )

            if schedule_item_playlist_schedule_info is not None:
                logging.info("Schedule item playlist schedule updated")

            return schedule_item_playlist_schedule_info
        except Exception as error:
            logging.error("Update schedule item playlist schedule failed")
            raise error

    def update_schedule_item_search_filter(
        self,
        schedule_id: str,
        item_id: str,
        collections: list[dict] | None,
        days: list[dict] | None,
        duration_time_code: str | None,
        end_search_date: str | None,
        end_search_duration_in_minutes: int | None,
        end_time_code: str | None,
        related_contents: list[dict] | None,
        search_date: str | None,
        search_duration_in_minutes: int | None,
        search_filter_type: int | None,
        tags: list[dict] | None,
        time_code: str | None
    ) -> dict | None:
        """
        Updates a schedule item search filter.

        Args:
            schedule_id (str): The id of the schedule the schedule item search filter is to be updated from.
            item_id (str): The id of the item to be updated.
            collections (list[dict] | None): The collections of the schedule item search filter.
                dict format: {"id": "string", "description": "string"}
            days (list[dict] | None): The days of the schedule item search filter.
                dict format: {"id": "string", "description": "string"}
            duration_time_code (str | None): The duration time between time_code and end_time_code.
                Please use the following format: hh:mm:ss;ff.
            end_search_date (str | None): The end search date of the schedule item search filter.
                Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
            end_search_duration_in_minutes int | None: The end search duration in minutes of the
                schedule item search filter.
            end_time_code (str | None): The end time code of the schedule item search filter.
                Please use the following format: hh:mm:ss;ff.
            related_contents (list[dict] | None): The related content of the schedule item search filter.
                dict format: {"id": "string", "description": "string"}
            search_date (str | None): The search date of the schedule item search filter.
                Only use when SEARCH_FILTER_TYPE = 2. Please use the following format: yyyy-MM-dd.THH:MM:SS.FFFZ.
            search_duration_in_minutes int | None: The search duration in minutes of the
                schedule item search filter.
            search_filter_type (str | None): The search filter type of the schedule item search filter.
                Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
            tags (list[dict] | None): The tags of the schedule item search filter.
                dict format: {"id": "string", "description": "string"}
            time_code (str | None): The time code of the schedule item search filter.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating schedule item search filter")

            schedule_item_search_filter_info: dict | None = _update_schedule_item_search_filter(
                self, schedule_id, item_id, collections, days, duration_time_code, end_search_date,
                end_search_duration_in_minutes, end_time_code, related_contents, search_date,
                search_duration_in_minutes, search_filter_type, tags, time_code
            )

            if schedule_item_search_filter_info is not None:
                logging.info("Schedule item search filter updated")

            return schedule_item_search_filter_info
        except Exception as error:
            logging.error("Update schedule item search filter failed")
            raise error

    # Schedule Event
    def add_asset_schedule_event(
        self,
        live_channel_id: str,
        asset: dict,
        is_loop: bool,
        duration_time_code: str | None,
        previous_id: str | None
    ) -> dict | None:
        """
        Adds an asset schedule event to a live channel.

        Paremeters:
            live_channel_id (str): The ID of the live channel.
            asset (dict): The asset of the asset schedule event.
            is_loop (bool): Indicates if the asset schedule event should loop.
            duration_time_code (str | None): The duration time code of the asset schedule event.
                Please use the following format: hh:mm:ss;ff.
            previous_id (str | None): The ID of the previous asset schedule event.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Add asset schedule event")

            asset_info: dict | None = _add_asset_schedule_event(
                self, live_channel_id, asset, is_loop, duration_time_code, previous_id
            )

            if asset_info is not None:
                logging.info("Add asset schedule event complete")

            return asset_info
        except Exception as error:
            logging.error("Add asset schedule event failed")
            raise error

    def add_input_schedule_event(
        self,
        live_channel_id: str,
        live_input: dict,
        backup_live_input: dict | None,
        fixed_on_air_time_utc: str | None,
        previous_id: str | None
    ) -> dict | None:
        """
        Adds a live input schedule event to a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.
            live_input (dict): The live input of the live input schedule event.
            backup_live_input (dict | None): The backup live input of the live input schedule event.
            fixed_on_air_time_utc (str | None): The fixed on air time UTC of the live input schedule event.
                Please use the following format: hh:mm:ss;ff.
            previous_id (str | None): The ID of the previous live input schedule event.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Add live input schedule event")

            live_input_info: dict | None = _add_input_schedule_event(
                self, live_channel_id, live_input, backup_live_input, fixed_on_air_time_utc, previous_id
            )

            if live_input_info is not None:
                logging.info("Add live input schedule event complete")

            return live_input_info
        except Exception as error:
            logging.error("Add live input schedule event failed")
            raise error

    def get_asset_schedule_event(self, live_channel_id: str, schedule_event_id: str) -> dict | None:
        """
        Gets an asset schedule event.

        Args:
            channel_id (str): The channel ID of the schedule event.
            schedule_event_id (str): The schedule event ID of the schedule event.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Get asset schedule event")

            asset_info: dict | None = _get_asset_schedule_event(self, live_channel_id, schedule_event_id)

            if asset_info is not None:
                logging.info("Get asset schedule event complete")

            return asset_info
        except Exception as error:
            logging.error("Get asset schedule event failed")
            raise error

    def get_input_schedule_event(self, live_channel_id: str, schedule_event_id: str) -> dict | None:
        """
        Gets an input schedule event.

        Args:
            channel_id (str): The channel ID of the schedule event.
            schedule_event_id (str): The schedule event ID of the schedule event.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Get input schedule event")

            input_info: dict | None = _get_input_schedule_event(self, live_channel_id, schedule_event_id)

            if input_info is not None:
                logging.info("Get input schedule event complete")

            return input_info
        except Exception as error:
            logging.error("Get input schedule event failed")
            raise error

    def move_schedule_event(
        self,
        live_channel_id: str,
        schedule_event_id: str,
        previous_schedule_event_id: str | None
    ) -> dict | None:
        """
        Moves a schedule event.

        Args:
            channel_id (str): The channel ID of the schedule event.
            schedule_event_id (str): The schedule event ID of the schedule event.
            previous_schedule_event_id (str | None): The previous schedule event ID of the schedule event.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Move schedule event")

            move_info: dict | None = _move_schedule_event(
                self, live_channel_id, schedule_event_id, previous_schedule_event_id
            )

            if move_info is not None:
                logging.info("Move schedule event complete")

            return move_info
        except Exception as error:
            logging.error("Move schedule event failed")
            raise error

    def remove_asset_schedule_event(self, live_channel_id: str, schedule_event_id: str) -> None:
        """
        Removes a live asset schedule event from a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.
            schedule_event_id (str): The ID of the schedule event.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Remove asset schedule event")

            _remove_asset_schedule_event(self, live_channel_id, schedule_event_id)

            logging.info("Remove asset schedule event complete")
        except Exception as error:
            logging.error("Add live operator schedule event failed")
            raise error

    def remove_input_schedule_event(self, live_channel_id: str, input_id: str) -> None:
        """
        Removes a live input schedule event from a live channel.

        Args:
            live_channel_id (str): The ID of the live channel.
            input_id (str): The ID of the schedule event.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Remove input schedule event")

            _remove_input_schedule_event(self, live_channel_id, input_id)

            logging.info("Remove input schedule event complete")
        except Exception as error:
            logging.error("Add live operator schedule event failed")
            raise error

    def update_asset_schedule_event(
        self,
        event_id: str,
        channel_id: str,
        asset: dict | None,
        is_loop: bool | None,
        duration_time_code: str | None
    ) -> dict | None:
        """
        Updates an asset schedule event.

        Args:
            event_id (str): The ID of the schedule event.
            channel_id (str): The channel ID of the schedule event.
            asset (dict | None): The asset of the schedule event.
                Format: {"id": "string", "name": "string"}
            is_loop (bool | None): Whether the schedule event is loop.
            duration_time_code (str | None): The duration time code of the schedule event.
                Please use the following format: hh:mm:ss;ff. Set to null if IS_LOOP is true.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Update asset schedule event")

            asset_info: dict | None = _update_asset_schedule_event(
                self, event_id, channel_id, asset, is_loop, duration_time_code
            )

            if asset_info is not None:
                logging.info("Update asset schedule event complete")

            return asset_info
        except Exception as error:
            logging.error("Update asset schedule event failed")
            raise error

    def update_input_schedule_event(
        self,
        event_id: str,
        channel_id: str,
        live_input: dict,
        backup_input: dict | None,
        fixed_on_air_time_utc: str | None
    ) -> dict | None:
        """
        Updates an input schedule event.

        Args:
            event_id (str): The ID of the Input schedule event.
            channel_id (str): The channel ID of the schedule event.
            input (dict | None): The input of the schedule event.
                Format: {"id": "string", "name": "string"}
            backup_input (dict | None): The backup input of the schedule event.
                Format: {"id": "string", "name": "string"}
            fixed_on_air_time_utc (str | None): The fixed on air time UTC of the schedule event.
                Please use the following format: hh:mm:ss.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Update input schedule event")

            input_info: dict | None = _update_input_schedule_event(
                self, event_id, channel_id, live_input, backup_input, fixed_on_air_time_utc
            )

            if input_info is not None:
                logging.info("Update input schedule event complete")

            return input_info
        except Exception as error:
            logging.error("Update input schedule event failed")
            raise error

    # User
    def delete_user(self, user_id: str) -> None:
        """
        Deletes a user.

        Args:
            user_id (str): The user ID of the user to be deleted.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting User")
            _delete_user(self, user_id)
            logging.info("User Deleted")
        except Exception as error:
            logging.error("User Failed to Delete")
            raise error

    def delete_user_content_attribute_data(self, user_id: str | None) -> None:
        """
        Deletes a user content attribute data.

        Args:
            user_id (str | None): The user ID of the user's content attribute data.
                If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Content Attribute Data")
            _delete_user_content_attribute_data(self, user_id)
            logging.info("User Content Attribute Data Deleted")
        except Exception as error:
            logging.error("User Content Attribute Data Failed to Delete")
            raise error

    def delete_user_content_group_data(self, user_id: str | None) -> None:
        """
        Deletes a user content group data.

        Args:
            user_id (str | None): The user ID of the user's content group data.
                If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Content Group Data")
            _delete_user_content_group_data(self, user_id)
            logging.info("User Content Group Data Deleted")
        except Exception as error:
            logging.error("User Content Group Data Failed to Delete")
            raise error

    def delete_user_content_security_data(
        self,
        content_id: str | None,
        content_definition_id: str | None,
        user_id: str | None,
        email: str | None,
        uid: str | None,
        key_name: str | None,
        expiration_date: str | None
    ) -> None:
        """
        Deletes a user content security data.

        Args:
            content_id (str | None): The content ID of the user content security data.
            content_definition_id (str | None): The content definition ID of the user content security data.
            user_id (str | None): The user ID of the user's content security data.
                If set to None, the user ID of the current user is used.
            email (str | None): The email of the user content security data.
            uid (str | None): The ID of the user content security data.
            key_name (str | None): The key name of the user content security data.
            expiration_date (str | None): The expiration date of the user content security data.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Content Security Data")
            _delete_user_content_security_data(
                self, content_id, content_definition_id, user_id, email, uid, key_name, expiration_date
            )
            logging.info("User Content Security Data Deleted")
        except Exception as error:
            logging.error("User Content Security Data Failed to Delete")
            raise error

    def delete_user_data(self, user_id: str | None) -> None:
        """
        Deletes a user's data.

        Args:
            user_id (str | None): The user ID of the user's data. If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Data")
            _delete_user_data(self, user_id)
            logging.info("User Data Deleted")
        except Exception as error:
            logging.error("User Data Failed to Delete")
            raise error

    def delete_user_dislikes_data(self, user_id: str | None) -> None:
        """
        Deletes a user dislikes data.

        Args:
            user_id (str | None): The user ID of the user's dislike data.
                If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Dislikes Data")
            _delete_user_dislike_data(self, user_id)
            logging.info("User Dislikes Data Deleted")
        except Exception as error:
            logging.error("User Dislikes Data Failed to Delete")
            raise error

    def delete_user_favorites_data(self, user_id: str | None) -> None:
        """
        Deletes a user favorites data.

        Args:
            user_id (str | None): The user ID of the user's favorites data. If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Favorites Data")
            _delete_user_favorites_data(self, user_id)
            logging.info("User Favorites Data Deleted")
        except Exception as error:
            logging.error("User Favorites Data Failed to Delete")
            raise error

    def delete_user_likes_data(self, user_id: str | None) -> None:
        """
        Deletes a user likes data.

        Args:
            user_id (str | None): The user ID of the user's likes data. If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Likes Data")
            _delete_user_likes_data(self, user_id)
            logging.info("User Likes Data Deleted")
        except Exception as error:
            logging.error("User Likes Data Failed to Delete")
            raise error

    def delete_user_saved_search_data(self, user_id: str | None) -> None:
        """
        Deletes a user saved search data.

        Args:
            user_id (str | None): The user ID of the user's saved search data.
                If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Saved Search Data")
            _delete_user_saved_search_data(self, user_id)
            logging.info("User Saved Search Data Deleted")
        except Exception as error:
            logging.error("User Saved Search Data Failed to Delete")
            raise error

    def delete_user_session_data(self, user_id: str | None) -> None:
        """
        Deletes a user session data.

        Args:
            user_id (str | None): The user ID of the user's session data.
                If set to None, the user ID of the current user is used.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Session Data")
            _delete_user_session_data(self, user_id)
            logging.info("User Session Data Deleted")
        except Exception as error:
            logging.error("User Session Data Failed to Delete")
            raise error

    def delete_user_share_data(self, user_id: str) -> None:
        """
        Deletes a user's shared data.

        Args:
            user_id (str): The user ID of the user's share data.
            If set to null, the user ID of the current user is used

        Returns:
            Unknown Type: If the request succeeds.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin type.")

            logging.info("Calling delete user share data")

            response: dict | None = _delete_user_share_data(self, user_id)

            if response is not None:
                logging.info("Delete user share data called successfully.")

            return response
        except Exception as error:
            logging.error("Calling delete user share data failed")
            raise error

    def delete_user_video_tracking_data(
        self,
        asset_id: str | None,
        content_id: str | None,
        video_tracking_attribute_id: str | None,
        user_id: str | None,
        uid: str | None,
        is_first_quartile: bool | None,
        is_midpoint: bool | None,
        is_third_quartile: bool | None,
        is_complete: bool | None,
        is_hidden: bool | None,
        is_live_stream: bool | None,
        max_second: float | None,
        last_second: float | None,
        total_seconds: float | None,
        last_beacon_date: str | None,
        key_name: str | None
    ) -> None:
        """
        Deletes a user video tracking data.

        Args:
            asset_id (str | None) The asset ID of the user video tracking data.
            content_id (str | None) The content ID of the user video tracking data.
            video_tracking_attribute_id (str | None) The video tracking attribute ID of the user video tracking data.
            Possible values: "Undefined", "Watchlist", "LiveStream".
            user_id (str | None) The user ID of the user video tracking data.
            If set to None, the user ID of the current user is used.
            uid (str | None) The ID of the user video tracking data.
            is_first_quartile (bool | None): The first quartile of the user video tracking data.
            is_midpoint (bool | None): The midpoint of the user video tracking data.
            is_third_quartile (bool | None): The third quartile of the user video tracking data.
            is_complete (bool | None): The complete of the user video tracking data.
            is_hidden (bool | None): The hidden of the user video tracking data.
            is_live_stream (bool | None): The live stream of the user video tracking data.
            max_second float | None: The max second of the user video tracking data.
            last_second float | None: The last second of the user video tracking data.
            total_seconds float | None: The total seconds of the user video tracking data.
            last_beacon_date (str | None) The last beacon date of the user video tracking data.
            key_name (str | None) The key name of the user video tracking data.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.id

            logging.info("Deleting User Video Tracking Data")
            _delete_user_video_tracking_data(
                self, asset_id, content_id, video_tracking_attribute_id, user_id, uid, is_first_quartile, is_midpoint,
                is_third_quartile, is_complete, is_hidden, is_live_stream, max_second, last_second, total_seconds,
                last_beacon_date, key_name
            )
            logging.info("User Video Tracking Data Deleted")
        except Exception as error:
            logging.error("User Video Tracking Data Failed to Delete")
            raise error

    # User Session
    def change_session_status(
        self,
        user_id: str | None,
        user_session_status: str,
        application_id: str | None
    ) -> dict | None:
        """
        Changes the status of a user session.

        Args:
            user_id (str | None) The ID of the user. If set to None, the user ID of the current user is used.
            user_session_status (str): The status of the user session.
            application_id (str | None) The application ID of the user session.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            if user_id is None:
                user_id = self.user_session_id

            logging.info("Changing Session Status")
            status_info: dict | None = _change_session_status(self, user_id, user_session_status, application_id)

            if status_info is not None:
                logging.info("Session Status Changed")

            return status_info
        except Exception as error:
            raise error

    def get_user_session(self, user_id: str | None) -> dict | None:
        """
        Gets a user session.

        Args:
            user_id (str | None) The ID of the user session. If set to None, the user ID of the current user is used.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if user_id is None:
                user_id = self.id

            logging.info("Getting User Session")
            user_session_info: dict | None = _get_user_session(self, user_id)
            if user_session_info is not None:
                logging.info("User Session Got")

            return user_session_info
        except Exception as error:
            raise error

    # Common
    def forgot_password(self) -> None:
        """
        Sends password to the user's email containing code used to reset password.

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            logging.info("Start forgot password")

            _forgot_password(self)

            logging.info("Forgot password complete")
        except Exception as error:
            logging.error("Forgot password failed")
            raise error

    def reset_password(self, code: str, new_password: str) -> None:
        """
        Resets the user's password.

        Args:
            code (str): The code of the user.
            new_password (str): The new password of the user.

        Returns:
            None: If the request is successful.
        """

        try:
            logging.info("Start reset password")

            _reset_password(self, code, new_password)

            logging.info("Reset password complete")
        except Exception as error:
            logging.error("Reset password failed")
            raise error

    def logout(self) -> None:
        """
        Logs the user out.

        Returns:
            None: If the request is successful.
        """

        try:
            logging.info("Start logout")

            _logout(self)

            logging.info("Logout complete")

            self.token = None
            self.refresh_token_val = None
            self.expiration_seconds = None
            self.user_session_id = None
            self.id = None

        except Exception as error:
            logging.error("Logout failed")
            raise error

    def register(self, email: str, first_name: str | None, last_name: str | None, password: str) -> dict | None:
        """
        Sends a code to the user's email to verify the account.

        Args:
            email (str): The email of the user.
            first_name (str | None): The first name of the user.
            last_name (str | None): The last name of the user.
            password (str): The password of the user.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Start register")

            register_info: dict | None = _register(self, email, first_name, last_name, password)

            if register_info is not None:
                logging.info("Register complete")

            return register_info
        except Exception as error:
            logging.error("Register failed")
            raise error

    def resend_code(self, email: str) -> None:
        """
        Resends the verification email.

        Args:
            email (str): The email of the user.

        Returns:
            None: If the request is successful.
        """

        try:
            logging.info("Start resend code")

            _resend_code(self, email)

            logging.info("Resend code complete")
        except Exception as error:
            logging.error("Resend code failed")
            raise error

    def verify(self, email: str, code: str) -> dict | None:
        """
        Verifies the user's account.

        Args:
            email (str): The email of the user.
            code (str): The code of the user.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Start verify")

            verification_info: dict | None = _verify(self, email, code)

            if verification_info is not None:
                logging.info("Verify complete")

            return verification_info
        except Exception as error:
            logging.error("Verify failed")
            raise error

    # Asset
    def archive_asset(self, asset_id: str) -> dict | None:
        """
        Archives an asset.

        Args:
            asset_id (str): The id of the asset.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the asset fails to archive.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Archiving asset")

            archived_asset_info: dict | None = _archive_asset(self, asset_id)

            if archived_asset_info is not None:
                logging.info("Asset archived")

            return archived_asset_info
        except Exception as error:
            raise error

    def build_media(
        self,
        sources: list[dict],
        title: str | None,
        tags: list[dict] | None,
        collections: list[dict] | None,
        related_contents: list[dict] | None,
        destination_folder_id: str,
        video_bitrate: int | None,
        audio_tracks: list[dict] | None
    ) -> None:
        """
        Builds a media.

        Args:
            sources (list[dict]): The sources of the media.
                dict format: {"sourceAssetId": "string", "startTimeCode": "string", "endTimeCode": "string"}
            title (str | None): The title of the media.
            tags (list[dict] | None): The tags of the media.
                dict format: {"id": "string", "description": "string"}
            collections (list[dict] | None): The collections of the media.
                dict format: {"id": "string", "description": "string"}
            related_contents (list[dict] | None): The related contents of the media.
                dict format: {"id": "string", "description": "string"}
            destination_folder_id (str): The destination folder ID of the media.
            video_bitrate (int | None): The video bitrate of the media.
            audio_tracks (list[dict] | None): The audio tracks of the media.
                dict format: { "id": "string", "bitRate": "int", "sampleRate": "int", "numChannels": "int",
                "format": "string", "frameRate": "int", "bitDepth": "int", "bitRateMode": "string",
                "durationSeconds": "int"}

        Returns:
            None: If the request is successful.

        Exceptions:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Building media")

            _build_media(
                self, sources, title, tags, collections, related_contents, destination_folder_id,
                video_bitrate, audio_tracks
            )

            logging.info("Media built")
        except Exception as error:
            raise error

    def clip_asset(
        self,
        asset_id: str,
        start_time_code: str,
        end_time_code: str,
        title: str,
        output_folder_id: str,
        tags: list[dict] | None,
        collections: list[dict] | None,
        related_contents: list[dict] | None,
        video_bitrate: int | None,
        audio_tracks: list[dict] | None
    ) -> dict | None:
        """
        Clips an asset.

        Args:
            asset_id (str): The id of the asset.
            start_time_code (str): The start time code of the asset.
                Please use the following format: hh:mm:ss;ff.
            end_time_code (str): The end time code of the asset.
                Please use the following format: hh:mm:ss;ff.
            title (str): The title of the asset.
            output_folder_id (str): The output folder ID of the asset.
            tags (list[dict] | None): The tags of the asset.
                dict format: {"id": "string", "description": "string"}
            collections (list[dict] | None): The collections of the asset.
                dict format: {"id": "string", "description": "string"}
            related_contents (list[dict] | None): The related contents of the asset.
                dict format: {"id": "string", "description": "string"}
            video_bitrate (int | None): The video bitrate of the asset.
            audio_tracks (list[dict] | None): The audio tracks of the asset.
                dict format: {"id": "string", "description": "string"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Clipping asset")

            clipped_asset_info: dict | None = _clip_asset(
                self, asset_id, start_time_code, end_time_code, title, output_folder_id, tags, collections,
                related_contents, video_bitrate, audio_tracks
            )

            if clipped_asset_info is not None:
                logging.info("Asset clipped")

            return clipped_asset_info
        except Exception as error:
            raise error

    def copy_asset(
        self,
        asset_ids: list[str],
        destination_folder_id: str,
        batch_action: dict | None,
        content_definition_id: str | None,
        schema_name: str | None,
        resolver_excempt: bool | None
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

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Copying asset")

            copied_asset_info: dict | None = _copy_asset(
                self, asset_ids, destination_folder_id, batch_action, content_definition_id,
                schema_name, resolver_excempt
            )

            if copied_asset_info is not None:
                logging.info("Asset copied")

            return copied_asset_info
        except Exception as error:
            raise error

    def create_annotation(
        self,
        asset_id: str,
        start_time_code: str,
        end_time_code: str,
        title: str | None,
        summary: str | None,
        description: str | None
    ) -> dict | None:
        """
        Creates an annotation.

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

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Creating annotation")

            annotation_info: dict | None = _create_annotation(
                self, asset_id, start_time_code, end_time_code, title, summary, description
            )

            if annotation_info is not None:
                logging.info("Annotation created")

            return annotation_info
        except Exception as error:
            raise error

    def create_asset_ad_break(
        self,
        asset_id: str,
        time_code: str | None,
        tags: list[dict] | None,
        labels: list[dict] | None
    ) -> dict | None:
        """
        Creates an asset ad break.

        Args:
            asset_id (str): The id of the asset.
            time_code (str | None): The time code of the asset ad break.
                Please use the following format: hh:mm:ss;ff.
            tags (list[dict] | None): The tags of the asset ad break.
                dict format: {"id": "string", "description": "string"}
            labels (list[dict] | None): The labels of the asset ad break.
                dict format: {"id": "string", "description": "string"}

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating asset ad break")

            asset_ad_break_info: dict | None = _create_asset_ad_break(
                self, asset_id, time_code, tags, labels
            )

            if asset_ad_break_info is not None:
                logging.info("Asset ad break created")

            return asset_ad_break_info
        except Exception as error:
            raise error

    def create_folder_asset(self, parent_id: str, display_name: str) -> dict | None:
        """
        Creates a folder asset.

        Args:
            PARENT_ID (str): The parent asset id for the parent folder.
            DISPLAY_NAME (str): The visual name of the new folder. It can contain spaces and other characters.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating folder asset")

            folder_asset_info: dict | None = _create_folder_asset(self, parent_id, display_name)

            if folder_asset_info is not None:
                logging.info("Folder asset created")

            return folder_asset_info
        except Exception as error:
            raise error

    def create_placeholder_asset(self, parent_id: str, asset_name: str) -> dict | None:
        """
        Creates a placeholder asset.

        Args:
            parent_id (str): The parent asset id for the placeholder asset.
            asset_name (str): The visual name of the new placeholder.
                It can contain spaces and other characters, must contain file extension.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating placeholder asset")

            placeholder_asset_info: dict | None = _create_placeholder_asset(self, parent_id, asset_name)

            if placeholder_asset_info is not None:
                logging.info("Placeholder asset created")

            return placeholder_asset_info
        except Exception as error:
            raise error

    def create_screenshot_at_timecode(self, asset_id: str, time_code: str | None) -> dict | None:
        """
        Creates a screenshot at a timecode.

        Args:
            asset_id (str): The id of the asset.
            time_code (str | None): The time code of the screenshot.
                Please use the following format: hh:mm:ss;ff.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating screenshot at timecode")

            screenshot_info: dict | None = _create_screenshot_at_timecode(self, asset_id, time_code)

            if screenshot_info is not None:
                logging.info("Screenshot created at timecode")

            return screenshot_info
        except Exception as error:
            raise error

    def delete_annotation(self, asset_id: str, annotation_id: str) -> dict | None:
        """
        Deletes an annotation.

        Args:
            asset_id (str): The id of the asset of the annotation.
            annotation_id (str): The id of the annotation.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Deleting annotation")

            deleted_annotation_info: dict | None = _delete_annotation(self, asset_id, annotation_id)

            if deleted_annotation_info is not None:
                logging.info("Annotation deleted")

            return deleted_annotation_info
        except Exception as error:
            raise error

    def delete_asset(self, asset_id: str) -> dict | None:
        """
        Deletes an asset.

        Args:
            asset_id (str): The id of the asset.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting asset")

            deleted_asset_info: dict | None = _delete_asset(self, asset_id)

            if deleted_asset_info is not None:
                logging.info("Asset deleted")

            return deleted_asset_info
        except Exception as error:
            raise error

    def delete_asset_ad_break(self, asset_id: str, ad_break_id: str) -> dict | None:
        """
        Deletes an asset ad break.

        Args:
            asset_id (str): The id of the asset.
            ad_break_id (str): The id of the ad break.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting asset ad break")

            deleted_asset_ad_break_info: dict | None = _delete_asset_ad_break(self, asset_id, ad_break_id)

            if deleted_asset_ad_break_info is not None:
                logging.info("Asset ad break deleted")

            return deleted_asset_ad_break_info
        except Exception as error:
            raise error

    def download_archive_asset(
        self,
        asset_ids: list[str],
        file_name: str | None,
        download_proxy: bool | None
    ) -> dict | None:
        """
        Downloads an archive asset.

        Args:
            asset_ids (list[str]): The ids of the assets.
            file_name (str | None): The file name of the archive asset. Only use if apiType is admin.
            download_proxy (boolean | None): The download proxy of the archive asset. Only use if apiType is admin.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            logging.info("Downloading archive asset")

            downloaded_archive_asset_info: dict | None = _download_archive_asset(
                self, asset_ids, file_name, download_proxy
            )

            if downloaded_archive_asset_info is not None:
                logging.info("Archive asset downloaded")

            return downloaded_archive_asset_info
        except Exception as error:
            raise error

    def duplicate_asset(self, asset_id: str) -> dict | None:
        """
        Duplicates an asset.

        Args:
            asset_id (str): The id of the asset.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Duplicating asset")

            duplicated_asset_info: dict | None = _duplicate_asset(self, asset_id)

            if duplicated_asset_info is not None:
                logging.info("Asset duplicated")

            return duplicated_asset_info
        except Exception as error:
            raise error

    def get_annotations(self, asset_id: str) -> dict | None:
        """
        Gets the annotations for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the annotations for.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Getting annotations")

            annotations: dict | None = _get_annotations(self, asset_id)

            if annotations is not None:
                logging.info("Annotations got")

            return annotations
        except Exception as error:
            raise error

    def get_asset(self, asset_id: str) -> dict | None:
        """
        Gets the asset for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the asset for.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting asset")

            asset: dict | None = _get_asset(self, asset_id)

            if asset is not None:
                logging.info("Asset got")

            return asset
        except Exception as error:
            raise error

    def get_asset_ad_breaks(self, asset_id: str) -> dict | None:
        """
        Gets the asset ad breaks for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the asset ad breaks for.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting asset ad breaks")

            asset_ad_breaks: dict | None = _get_asset_ad_breaks(self, asset_id)

            if asset_ad_breaks is not None:
                logging.info("Asset ad breaks got")

            return asset_ad_breaks
        except Exception as error:
            raise error

    def get_asset_child_nodes(
        self,
        asset_id: str,
        folder_id: str,
        sort_column: str,
        is_desc: bool,
        page_index: int,
        page_size: int
    ) -> dict | None:
        """
        Gets the asset child nodes for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the asset child nodes for.
            folder_id (str): The ID of the folder the asset is in.
            sort_column (str): The column to sort by.
            is_desc (bool): Whether the sort is descending or not.
            page_index (int): The page index of the asset child nodes.
            page_size (int): The page size of the asset child nodes.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting asset child nodes")

            asset_child_nodes: dict | None = _get_asset_child_nodes(
                self, asset_id, folder_id, sort_column, is_desc, page_index, page_size
            )

            if asset_child_nodes is not None:
                logging.info("Asset child nodes got")

            return asset_child_nodes
        except Exception as error:
            raise error

    def get_asset_details(self, asset_id: str) -> dict | None:
        """
        Gets the asset details for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the details for.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            logging.info("Getting asset details")

            asset_details: dict | None = _get_asset_details(self, asset_id)

            if asset_details is not None:
                logging.info("Asset details got")

            return asset_details
        except Exception as error:
            raise error

    def get_asset_manifest_with_cookies(self, asset_id: str, cookie_id: str) -> dict | None:
        """
        Gets the asset manifest with cookies for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the manifest with cookies for.
            cookie_id (str): The ID of the cookie.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            logging.info("Getting asset manifest with cookies")

            asset_manifest_with_cookies: dict | None = _get_asset_manifest_with_cookies(
                self, asset_id, cookie_id
            )

            if asset_manifest_with_cookies is not None:
                logging.info("Asset manifest with cookies got")

            return asset_manifest_with_cookies
        except Exception as error:
            raise error

    def get_asset_metadata_summary(self, asset_id: str) -> dict | None:
        """
        Gets the asset metadata summary for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the metadata summary for.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting asset metadata summary")

            asset_metadata_summary: dict | None = _get_asset_metadata_summary(self, asset_id)

            if asset_metadata_summary is not None:
                logging.info("Asset metadata summary got")

            return asset_metadata_summary
        except Exception as error:
            raise error

    def get_asset_parent_folders(self, asset_id: str, page_size: int) -> dict | None:
        """
        Gets the list of all parent folders for this item. It does not include the item itself or
        any files in any folder. The folders will be returned in hierarchical sequence, starting
        from the top node and each identifiers object will have a new children attribute that is
        the next sub-folder in the hierarchy.

        Args:
            asset_id (str): The assetId of the current item to get the parents for. This can be either a folder or a file.
            page_size (int): The size of the page of folders to retrieve. Note this is for each level of the tree.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting asset parent folders")

            asset_parent_folders: dict | None = _get_asset_parent_folders(self, asset_id, page_size)

            if asset_parent_folders is not None:
                logging.info("Asset parent folders got")

            return asset_parent_folders
        except Exception as error:
            raise error

    def get_asset_screenshot_details(self, asset_id: str, segment_id: str, screenshot_id: str) -> dict | None:
        """
        Gets the asset screenshot details for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the screenshot details for.
            segment_id (str): The ID of the segment.
            screenshot_id (str): The ID of the screenshot.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting asset screenshot details")

            asset_screenshot_details: dict | None = _get_asset_screenshot_details(
                self, asset_id, segment_id, screenshot_id
            )

            if asset_screenshot_details is not None:
                logging.info("Asset screenshot details got")

            return asset_screenshot_details
        except Exception as error:
            raise error

    def get_asset_segment_details(self, asset_id: str, segment_id: str) -> dict | None:
        """
        Gets the asset segment details for the specified asset ID.

        Args:
            asset_id (str): The ID of the asset to get the segment details for.
            segment_id (str): The ID of the segment.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting asset segment details")

            asset_segment_details: dict | None = _get_asset_segment_details(self, asset_id, segment_id)

            if asset_segment_details is not None:
                logging.info("Asset segment details got")

            return asset_segment_details
        except Exception as error:
            raise error

    def get_user_upload_parts(self, upload_id: str) -> dict | None:
        """
        Gets the user upload parts for the specified asset ID.

        Args:
            upload_id (str): The ID of the upload to get the user upload parts for.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting user upload parts")

            user_upload_parts: dict | None = _get_user_upload_parts(self, upload_id)

            if user_upload_parts is not None:
                logging.info("User upload parts got")

            return user_upload_parts
        except Exception as error:
            raise error

    def get_user_uploads(self, include_completed_uploads: bool) -> dict | None:
        """
        Gets the user uploads for the specified asset ID.

        Args:
            include_completed_uploads (boolean): Whether to include completed uploads or not.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting user uploads")

            upload_uploads: dict | None = _get_user_uploads(self, include_completed_uploads)

            if upload_uploads is not None:
                logging.info("User uploads got")

            return upload_uploads
        except Exception as error:
            raise error

    def import_annotations(self, asset_id: str, annotations: list[dict]) -> None:
        """
        Imports annotations.

        Args:
            asset_id (str): The ID of the asset to import the annotations for.
            annotations (list[dict]): The annotations to import. dict format: {"startTimeCode": "string", "endTimeCode": "string"}

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Importing annotations")

            _import_annotations(self, asset_id, annotations)

            logging.info("Annotations imported")

        except Exception as error:
            raise error

    def index_asset(self, asset_id: str) -> dict | None:
        """
        Indexes an asset.

        Args:
            asset_id (str): The ID of the asset to index.

        Returns:
            dict: The JSON response from the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Indexing asset")

            indexed_asset_info: dict | None = _index_asset(self, asset_id)

            if indexed_asset_info is not None:
                logging.info("Asset indexed")

            return indexed_asset_info
        except Exception as error:
            raise error

    def local_restore_asset(self, asset_id: str, profile: str | None) -> dict | None:
        """
        Local restores an asset.

        Args:
            asset_id (str): The ID of the asset to local restore.
            profile (str | None): The profile of the local restore.

        Returns:
            dict: The JSON response from the server if the asset is local restored.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Local restoring asset")

            local_restored_asset_info: dict | None = _local_restore_asset(self, asset_id, profile)

            if local_restored_asset_info is not None:
                logging.info("Asset local restored")

            return local_restored_asset_info
        except Exception as error:
            raise error

    def move_asset(
        self,
        asset_id: str,
        destination_folder_id: str,
        name: str | None,
        batch_action: dict | None,
        content_definition_id: str,
        schema_name: str | None,
        resolver_excempt: bool | None
    ) -> dict | None:
        """
        Moves an asset.

        Args:
            asset_id (str): The ID of the asset to move.
            destination_folder_id (str): The destination folder ID of the move.
            name (str | None): The name of the asset when moved.
            batch_action (dict | None): The batch action of the move.
            content_definition_id (str | None): The content definition ID of the move.
            schema_name (str | None): The schema name of the move.
            resolver_excempt (boolean | None): The resolver exempt of the move.

        Returns:
            dict: The JSON response from the server if the asset is moved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Moving asset")

            moved_asset_info: dict | None = _move_asset(
                self, asset_id, destination_folder_id, name, batch_action, content_definition_id,
                schema_name, resolver_excempt)

            if moved_asset_info is not None:
                logging.info("Asset moved")

            return moved_asset_info
        except Exception as error:
            raise error

    def records_asset_tracking_beacon(
        self,
        asset_id: str,
        tracking_event: str,
        live_channel_id: str,
        content_id: str | None,
        second: int
    ) -> None:
        """
        Records an asset tracking beacon for the asset (either an ad or a normal asset).

        Args:
            asset_id (str): The ID of the asset to record the asset tracking beacon for.
            tracking_event (str): The tracking event of the asset tracking beacon.
                Enum: "Progress", "FirstQuartile", "Midpoint", "ThirdQuartile", "Complete", "Hide", "LiveStream"
            live_channel_id (str): The live channel ID of the asset tracking beacon.
            content_id (str | None): Optional content Id to track along with required asset id.
            second (int): Second mark into the video/ad.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Recording asset tracking beacon")

            _records_asset_tracking_beacon(
                self, asset_id, tracking_event, live_channel_id, content_id, second
            )

            logging.info("Asset tracking beacon recorded")
        except Exception as error:
            raise error

    def register_asset(
        self,
        asset_id: str | None,
        parent_id: str | None,
        display_object_key: str | None,
        bucket_name: str,
        object_key: str,
        e_tag: str | None,
        tag_ids: list[str] | None,
        collection_ids: list[str] | None,
        related_content_ids: list[str] | None,
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
            asset_id (str | null): The ID of the asset to register.
            parent_id (str | null): The ID of the parent.
            display_object_key (str | None): The display object key of the register.
            bucket_name (str): The bucket name of the register.
            object_key (str): The object key of the register.
            e_tag (str | None): The eTag of the register.
            tag_ids (list[str] | None): The tags of the register.
            collection_ids (list[str] | None): The collections of the register.
            related_content_ids (list[str] | None): The related contents of the register.
            sequencer (str | None): The sequencer of the register.
            asset_status (str | None): The asset status of the register.
                Enum: "Available", "Renaming", "Copying", "Restoring", "Registering",
                "Uploading", "Archiving", "Archived", "PendingArchive", "PendingRestore",
                "Restored", "Deleting", "Moving", "SlugReplaced", "Updating", "Error",
                "Assembling", "Clipping", "Placeholder", "Creating"
            storage_class (str | None): The storage class of the register.
                Enum: "Standard", "ReducedRedundancy", "Glacier", "StandardInfrequentAccess",
                "OneZoneInfrequentAccess", "IntelligentTiering", "DeepArchive", "GlacierInstanctRetrival",
                "Outposts"
            asset_type (str | None): The asset type of the register.
                Enum: "Folder", "File", "Bucket"
            content_length (int | None): The content length of the register.
            storage_event_name (str | None): The storage event name of the register.
            created_date (str | None): The created date of the register.
            storage_source_ip_address (str | None): The storage source IP address of the register.
            start_media_processor (boolean | null): The start media processor of the register.
            delete_missing_asset (boolean | null): The delete missing asset of the register.

        Returns:
            dict: The JSON response from the server if the asset is registered.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            If the asset fails to register.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Registering asset")

            registered_asset_info: dict | None = _register_asset(
                self, asset_id, parent_id, display_object_key, bucket_name, object_key, e_tag, tag_ids,
                collection_ids, related_content_ids, sequencer, asset_status, storage_class, asset_type,
                content_length, storage_event_name, created_date, storage_source_ip_address,
                start_media_processor, delete_missing_asset
            )

            if registered_asset_info is not None:
                logging.info("Asset registered")

            return registered_asset_info
        except Exception as error:
            raise error

    def reprocess_asset(self, target_ids: list[str]) -> dict | None:
        """
        Reprocesses an asset.

        Args:
            target_ids (list[str]): The target IDs of the reprocess.

        Returns:
            dict: The JSON response from the server if the asset is reprocessed.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Reprocessing asset")

            reprocessed_asset_info: dict | None = _reprocess_asset(self, target_ids)

            if reprocessed_asset_info is not None:
                logging.info("Asset reprocessed")

            return reprocessed_asset_info
        except Exception as error:
            raise error

    def restore_asset(self, asset_id: str) -> dict | None:
        """
        Restores an asset.

        Args:
            asset_id (str): The ID of the asset to restore.

        Returns:
            dict: The JSON response from the server if the asset is restored.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Restoring asset")

            restored_asset_info: dict | None = _restore_asset(self, asset_id)

            if restored_asset_info is not None:
                logging.info("Asset restored")

            return restored_asset_info
        except Exception as error:
            raise error

    def share_asset(
            self,
            asset_id: str,
            nomad_users: list[dict] | None,
            external_users: list[dict] | None,
            shared_duration_in_hours: int | None) -> dict | None:
        """
        Shares an asset.

        Args:
            asset_id (str): The ID of the asset to share.
            nomad_users (list[dict] | None): The nomad users of the share. dict format: { id: string }
            external_users (list[dict] | None): The external users of the share. dict format: { id: string }
            shared_duration_in_hours (int | None): The share duration in hours of the share.

        Returns:
            dict: The JSON response from the server if the asset is shared.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Sharing asset")

            shared_asset_info: dict | None = _share_asset(
                self, asset_id, nomad_users, external_users, shared_duration_in_hours
            )

            if shared_asset_info is not None:
                logging.info("Asset shared")

            return shared_asset_info
        except Exception as error:
            raise error

    def start_workflow(self, action_arguments: dict, target_ids: list[str]) -> dict | None:
        """
        Starts a workflow.

        Args:
            action_arguments (dict): The action arguments of the start. dict format: { "workflowName": string }
            target_ids (list[str]): The target IDs of the start.

        Returns:
            dict: The JSON response from the server if the workflow is started.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Starting workflow")

            started_workflow_info: dict | None = _start_workflow(self, action_arguments, target_ids)

            if started_workflow_info is not None:
                logging.info("Workflow started")

            return started_workflow_info
        except Exception as error:
            raise error

    def transcribe_asset(self, asset_id: str, transcript_id: str, transcript: list[dict] | None) -> dict | None:
        """
        Transcribes an asset.

        Args:
            asset_id (str): The ID of the asset to transcribe.
            transcript_id (str): The ID of the transcript.
            transcript (list[dict] | None): The transcript of the transcribe.
                dict format: { "startTimeCode": string, "content": string }

        Returns:
            dict: The JSON response from the server if the asset is transcribed.
            None: If return fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Transcribing asset")

            _transcribe_asset(self, asset_id, transcript_id, transcript)

            logging.info("Asset transcribed")
        except Exception as error:
            raise error

    def update_annotation(
        self,
        asset_id: str,
        annotation_id: str,
        start_time_code: str,
        end_time_code: str,
        title: str | None,
        summary: str | None,
        description: str
    ) -> dict | None:
        """
        Updates an annotation.

        Args:
            asset_id (str): The ID of the asset to update the annotation for.
            annotation_id (str): The ID of the annotation.
            start_time_code (str | None): The start time code of the annotation.
            please use the following format: hh:mm:ss;ff.
            end_time_code (str | None): The end time code of the annotation.
            please use the following format: hh:mm:ss;ff.
            title (str | None): The title of the annotation.
            summary (str | None): The summary of the annotation.
            description (str | None): The description of the annotation.

        Returns:
            dict: The JSON response from the server if the annotation is updated.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Updating annotation")

            updated_annotation_info: dict | None = _update_annotation(
                self, asset_id, annotation_id, start_time_code, end_time_code,
                title, summary, description
            )

            if updated_annotation_info is not None:
                logging.info("Annotation updated")

            return updated_annotation_info
        except Exception as error:
            raise error

    def update_asset(
        self,
        asset_id: str,
        display_name: str | None,
        display_date: str | None,
        available_start_date: str | None,
        available_end_date: str | None,
        custom_properties: dict | None
    ) -> dict | None:
        """
        Updates specific properties of the asset.
        Other API calls can be used to alter other more involved properties.

        Args:
            asset_id (str): The ID of the asset to update.
            display_name (str | None): The display name of the asset.
            display_date (str | None): The display date of the asset.
            available_start_date (str | None): The available start date of the asset.
            available_end_date (str | None): The available end date of the asset.
            custom_properties (dict | None): The custom properties of the asset.
                dict format: {"key": "string", "value": "string"}

        Returns:
            dict: The JSON response from the server if the asset is updated.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating asset")

            updated_asset_info: dict | None = _update_asset(
                self, asset_id, display_name, display_date, available_start_date,
                available_end_date, custom_properties
            )

            if updated_asset_info is not None:
                logging.info("Asset updated")

            return updated_asset_info
        except Exception as error:
            raise error

    def update_asset_ad_break(
        self,
        asset_id: str,
        ad_break_id: str,
        time_code: str | None,
        tags: list[dict] | None,
        labels: list[dict] | None
    ) -> dict | None:
        """
        Updates an asset ad break.

        Args:
            asset_id (str): The ID of the asset to update the ad break for.
            ad_break_id (str): The ID of the ad break.
            time_code (str | None): The time code of the asset ad break.
                Please use the following format: hh:mm:ss;ff.
            tags (list[dict] | None): The tags of the asset ad break.
                dict format: {"id": "string", "description": "string"}
            labels (list[dict] | None): The labels of the asset ad break.
                dict format: {"id": "string", "description": "string"}

        Returns:
            dict: The JSON response from the server if the asset ad break is updated.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating asset ad break")

            updated_asset_ad_break_info: dict | None = _update_asset_ad_break(
                self, asset_id, ad_break_id, time_code, tags, labels
            )

            if updated_asset_ad_break_info is not None:
                logging.info("Asset ad break updated")

            return updated_asset_ad_break_info
        except Exception as error:
            raise error

    def update_asset_language(self, asset_id: str, language_id: str) -> dict | None:
        """
        Updates language of the asset. This will cause a re-process of the AI data.

        Args:
            asset_id (str): The ID of the asset to update the language for.
            language_id (str): The ID of the language.

        Returns:
            dict: The JSON response from the server if the asset language is updated.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Updating asset language")

            updated_asset_language_info: dict | None = _update_asset_language(self, asset_id, language_id)

            if updated_asset_language_info is not None:
                logging.info("Asset language updated")

            return updated_asset_language_info
        except Exception as error:
            raise error

    # content metadata
    def add_custom_properties(
        self,
        content_id: str,
        name: str | None,
        date: str | None,
        custom_properties: dict
    ) -> dict | None:
        """
        Adds a custom properties to the specified content.

        Args:
            content_id (str): The ID of the content to add the custom property to.
            name (str | None): The name of the custom property.
            date (str | None): The date of the custom property.
            custom_properties (dict):  A list of custom properties that should be saved for the
            asset. To remove a property value, set the value to None

        Returns:
            dict: The JSON response from the server if the custom properties are added.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Adding custom properties")

            content: dict | None = _add_custom_properties(self, content_id, name, date, custom_properties)

            if content is not None:
                logging.info("Add custom properties complete")

            return content
        except Exception as error:
            logging.error("Add custom properties failed")
            raise error

    def add_related_content(self, content_id: str, related_content_id: str, content_definition: str) -> dict | None:
        """
        Adds a related content to the specified content.

        Args:
            content_id (str): The ID of the content to add the related content to.
            related_content_id (str): The ID of the related content.
            content_definition (str): The content definition of the related content.

        Returns:
            dict: The JSON response from the server if the related content is added.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Adding related content")

            content: dict | None = _add_related_content(
                self, content_id, related_content_id, content_definition
            )

            if content is not None:
                logging.info("Add related content complete")

            return content
        except Exception as error:
            logging.error("Add related content failed")
            raise error

    def add_tag_or_collection(
            self,
            tag_type: str,
            content_id: str,
            content_definition: str,
            tag_name: str,
            tag_id: str | None,
            create_new: bool | None) -> dict | None:
        """
        Adds a tag or collection to the specified content.

        Args:
            TAG_TYPE (str): The type of the tag or collection. The options are tag and collection.
            CONTENT_ID (str): The ID of the content to add the tag or collection to.
            CONTENT_DEFINITION (str): The content definition of the tag or collection.
            TAG_NAME (str): The name of the tag or collection.
            TAG_ID (str | None): The ID of the tag or collection.
            CREATE_NEW (bool | None): Indicates if a new tag or collection should be created.

        Returns:
            dict: The JSON response from the server if the tag or collection is added.

        """

        try:
            logging.info("Adding %s to content %s", tag_type, content_id)

            content: dict | None = _add_tag_or_collection(
                self, tag_type, content_id, content_definition, tag_name, tag_id, create_new
            )

            if content is not None:
                logging.info("Added %s to content %s", tag_type, content_id)

            return content
        except Exception as error:
            logging.error("Adding %s to content %s failed", tag_type, content_id)
            raise error

    def bulk_update_metadata(
        self,
        content_ids: list[str] | None,
        collection_ids: list[str] | None,
        related_content_ids: list[str] | None,
        tag_ids: list[str] | None,
        schema_name: str | None
    ) -> None:
        """
        Updates the metadata for the specified content.

        Args:
            content_ids (list[str]): The IDs of the content to update the metadata for.
            collection_ids (list[str] | None): The IDs of the collections to update the metadata for.
            related_content_ids (list[str] | None): The IDs of the related content to update.
            tag_ids (list[str] | None): The IDs of the tags to update the metadata for.
            schema_name (str | None): The name of the schema to use.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Performing Bulk Update")

            _bulk_update_metadata(self, content_ids, collection_ids, related_content_ids, tag_ids, schema_name)

            logging.info("Bulk Update complete")
        except Exception as error:
            logging.error("Bulk Update failed")
            raise error

    def create_tag_or_collection(self, tag_type: str, tag_name: str) -> dict | None:
        """
        Creates a tag or collection.

        Args:
            tag_type (str): Specify if the content being managed is a tag or a collection.
            tag_name (str): The name of the tag or collection to create.

        Returns:
            dict: The JSON response from the server if the tag or collection is created.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Creating %s", tag_type)

            content: dict | None = _create_tag_or_collection(self, tag_type, tag_name)

            if content is not None:
                logging.info("Create %s complete", tag_type)

            return content
        except Exception as error:
            logging.error("Create %s failed", tag_type)
            raise error

    def delete_related_content(self, content_id: str, related_content_id: str, content_definition: str) -> dict | None:
        """
        Deletes a related content from the specified content.

        Args:
            content_id (str): The ID of the content to delete the related content from.
            related_content_id (str): The ID of the related content.
            content_definition (str): The content definition of the related content.

        Returns:
            dict: The JSON response from the server if the related content is deleted.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Deleting related content")

            content: dict | None = _delete_related_content(self, content_id, related_content_id, content_definition)

            if content is not None:
                logging.info("Delete related content complete")

            return content
        except Exception as error:
            logging.error("Delete related content failed")
            raise error

    def delete_tag_or_collection(self, tag_type: str, tag_id: str) -> dict | None:
        """
        Deletes a tag or collection from the specified content.

        Args:
            tag_type (str): The type of the tag or collection. The options are tag and collection.
            tag_id (str): The ID of the tag or collection.

        Returns:
            dict: The JSON response from the server if the tag or collection is deleted.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Deleting %s", tag_type)

            content: dict | None = _delete_tag_or_collection(self, tag_type, tag_id)

            if content is not None:
                logging.info("Delete %s complete", tag_type)

            return content
        except Exception as error:
            logging.error("Delete %s failed", tag_type)
            raise error

    def get_tag_or_collection(self, tag_type: str, tag_id: str) -> dict | None:
        """
        Gets a tag or collection from the specified content.

        Args:
            tag_type (str): The type of the tag or collection. The options are tag and collection.
            tag_id (str): The ID of the tag or collection.

        Returns:
            dict: The information of the tag or collection.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not admin.
        """

        try:
            if self.config["apiType"] != "admin":
                raise InvalidAPITypeException("This function is only available for admin API type.")

            logging.info("Getting %s", tag_type)

            content: dict | None = _get_tag_or_collection(self, tag_type, tag_id)

            if content is not None:
                logging.info("Get %s complete", tag_type)

            return content
        except Exception as error:
            logging.error("Get %s failed", tag_type)
            raise error

    def remove_tag_or_collection(
        self,
        tag_type: str,
        content_id: str,
        content_definition_id: str,
        tag_id: str
    ) -> dict | None:
        """
        Removes a tag or collection from the specified content.

        Args:
            tag_type (str): The type of the tag or collection. The options are tag and collection.
            content_id (str): The ID of the content to remove the tag or collection from.
            content_definition_id (str): The content definition of the tag or collection.
            tag_id (str): The ID of the tag or collection.

        Returns:
            dict: The JSON response from the server if the tag or collection is removed.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Start remove tag or collection")

            content: dict | None = _remove_tag_or_collection(
                self, tag_type, content_id, content_definition_id, tag_id
            )

            if content is not None:
                logging.info("Remove tag or collection complete")

            return content
        except Exception as error:
            logging.error("Remove tag or collection failed")
            raise error

    # Ping
    def ping(self, application_id: str | None, user_session_id: str | None) -> dict | None:
        """
        Pings the user

        Args:
            application_id (str | None): The application ID of the user.
            user_session_id (str | None): The user session ID of the user.

        Returns:
            dict: The JSON response from the server if the user is pinged.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Pinging user")

            ping_info: dict | None = _ping(self, application_id, user_session_id)

            if ping_info is not None:
                logging.info("User pinged")

            return ping_info
        except Exception as error:
            logging.error("User failed to ping")
            raise error

    def ping_auth(self, application_id: str | None, user_session_id: str) -> dict | None:
        """
        Pings the user

        Args:
            application_id (str | None): The application ID of the user.
            user_session_id (str): The user session ID of the user.

        Returns:
            dict: The JSON response from the server if the user is pinged.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Pinging user")

            ping_info: dict | None = _ping_auth(self, application_id, user_session_id)

            if ping_info is not None:
                logging.info("User pinged")

            return ping_info
        except Exception as error:
            logging.error("User failed to ping")
            raise error

    # Search
    def search(
        self,
        query: str | None,
        offset: int | None,
        size: int | None,
        filters: list[dict] | None,
        sort_fields: list[dict] | None,
        search_result_fields: list[dict] | None,
        similar_asset_id: str | None,
        min_score: int | None,
        exclude_total_record_count: bool | None,
        filter_binder: int | None,
        full_url_field_names: list[str] | None,
        distinct_on_field_name: str | None,
        include_video_clips: bool | None,
        use_llm_search: bool | None,
        include_internal_fields_in_results: bool | None
    ) -> dict | None:
        """
        Search

        Args:
            query (str | None): The query is used for free text searching within all of the text of the records.
                This is typically associated to the values entered into a search bar on a website.
            OFFSET (int | None): The pageOffset is a zero based number offset used for paging purposes.
                If this value is omitted then the marker based paging is used and the return nextPageOffset
                value will specify a string - rather than a number. You can only use either the zero based page
                numbers OR the string based page markers, but not both in a single search query and paging.
            SIZE (int | None): The size is a zero based number that represents how many items
                in the selected page to return
            FILTERS (list[dict] | None): Filters are the primary mechanism for filtering the returned
                records. There is often more than 1 filter. When 2 or more filters are supplied then there is an
                implied "**AND**" between each filter.  The name of each filter must match exactly to the name in
                the output including the appropriate camel-casing.  The operator choices are: (Equals, NotEqual,
                Contains, NotContains, LessThan, GreaterThan, LessThanEquals, snf GreaterThanEquals).
                The value can be either a single value or an array of values. If an array of values is supplied
                then there is an implied "**OR**" between each value in the array. NOTE: When filtering by dates,
                format matters. The appropriate format to use is UTC format such as YYYY-MM-DDTHH:MM:SS.SSSZ.
                dict format: {"fieldName": "string", "operator": "string", "values" : "list | string"}
            SORT_FIELDS (list[dict] | None): The sortFields allows the top level results to be sorted
                by one or more of the output result fields. The name represents one of the fields in the output
                and must match exactly including the camel-casing.
                dict format: {"fieldName": "string", "sortType": ("Ascending" | "Descending")}
            SEARCH_RESULT_FIELDS (list[dict] | None): The searchResultFields allows you to specify specific
                fields that should be returned in the output as well as any children (or related) records that should
                be also returned. Note that any given searchResultField can contain children also and those fields can
                contain children. There is no limit to the level of related children to return
                dict format: {"name": "string"}
            SIMILAR_ASSET_ID (str | None): When SimilarAssetId has a value, then the search
                results are a special type of results and bring back the items that are the most similar to
                the item represented here. This search is only enabled when Vector searching has been enabled.
                When this has a value, the SearchQuery value and PageOffset values are ignored.
            MIN_SCORE (int | None): Specifies the minimum score to match when returning results.
                If omitted, the system default will be used - which is usually .65
            EXCLUDE_TOTAL_RECORD_COUNT (bool | None): Normally, the total record count is
                returned but the query can be made faster if this value is excluded.
            FILTER_BINDER (int | None): The filter binder of the search. 0 = AND, 1 = OR.
            FULL_URL_FIELD_NAMES (list[str] | None): Gets or sets the list of fields that should have the FullURL
                calculated. The calculations are expensive and greatly slow down the query.
                Use this field to only return the ones that are actually needed.
            DISTINCT_ON_FIELD_NAME (str | None): Gets or sets optional property that will be used to aggregate
                results records to distinct occurances of this field's values.
            INCLUDE_VIDEO_CLIPS (bool | None): Gets or sets a value indicating whether specify if the video
                search results are grouped by include clips of the videos also.
            USE_LLM_SEARCH (bool | None): Gets or sets a value indicating whether gets or Sets a value representing
                if the search engine should try and use the LLM search instead of the standard search.
            INCLUDE_INTERNAL_FIELDS_IN_RESULTS (bool | None): Gets or sets a value indicating whether
                specify if the internal fields are included in the results.

        Returns:
            dict: The JSON response from the server if the search is successful.
            None: If the request fails or the response cannot be parsed as JSON.
        """

        try:
            logging.info("Start search")

            search_info: dict | None = _search(
                self, query, offset, size, filters, sort_fields, search_result_fields, similar_asset_id,
                min_score, exclude_total_record_count, filter_binder, full_url_field_names, distinct_on_field_name,
                include_video_clips, use_llm_search, include_internal_fields_in_results
            )

            if search_info is not None:
                logging.info("Search complete")

            return search_info
        except Exception as error:
            logging.error("Search failed")
            raise error

    # Portal
    def change_email(self, new_email: str) -> None:
        """
        Changes the email of the user.

        Args:
            new_email (str): The new email of the user.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start change email")

            _change_email(self, new_email)

            logging.info("Change email complete")
        except Exception as error:
            logging.error("Change email failed")
            raise error

    def change_password(self, new_password: str) -> None:
        """
        Changes the password of the user.

        Args:
            new_password (str): The new password of the user.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start change password")

            _change_password(self, new_password)

            logging.info("Change password complete")
        except Exception as error:
            logging.error("Change password failed")
            raise error

    def get_user(self) -> dict | None:
        """
        Gets user.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get user")

            user_info: dict | None = _get_user(self)

            if user_info is not None:
                logging.info("Get user complete")

            return user_info
        except Exception as error:
            logging.error("Get user failed")
            raise error

    def update_user(
        self,
        address: str | None,
        address2: str | None,
        city: str | None,
        first_name: str | None,
        last_name: str | None,
        phone_number: str | None,
        phone_extention: str | None,
        postal_code: str | None,
        organization: str | None,
        country: str | None,
        state: str | None
    ) -> dict | None:
        """
        Updated user.

        Args:
            address (str | None): The address of the user.
            address2 (str | None): The address2 of the user.
            city (str | None): The city of the user.
            first_name (str | None): The first name of the user.
            last_name (str | None): The last name of the user.
            phone_number (str | None): The phone number of the user.
            phone_extention (str | None): The phone extention of the user.
            postal_code (str | None): The postal code of the user.
            organization (str | None): The organization of the user.
            country (str | None): The country of the user.
            state (str | None): The state of the user.

        Returns:
            dict: The JSON response from the server if the user is updated.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start update user")

            user_info: dict | None = _update_user(
                self, address, address2, city, first_name, last_name, phone_number, phone_extention,
                postal_code, organization, country, state
            )

            if user_info is not None:
                logging.info("Update user complete")

            return user_info
        except Exception as error:
            logging.error("Update user failed")
            raise error

    def add_contents_to_content_group(self, content_group_id: str, content_ids: list[str]) -> None:
        """
        Add contents to content group.

        Args:
            content_group_id (str): The ID of the content group.
            content_ids (list[str]): The IDs of the content.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start add contents to content group")

            info: dict | None = _add_contents_to_content_group(self, content_group_id, content_ids)

            if info is not None:
                logging.info("Add contents to content group complete")

            return info
        except Exception as error:
            logging.error("Add contents to content group failed")
            raise error

    def create_content_group(self, name: str) -> dict | None:
        """
        Creates a content group.

        Args:
            name (str): The name of the content group.

        Returns:
            dict: The JSON response from the server if the content group is created.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start create content group")

            content_group_info: dict | None = _create_content_group(self, name)

            if content_group_info is not None:
                logging.info("Create content group complete")

            return content_group_info
        except Exception as error:
            logging.error("Create content group failed")
            raise error

    def delete_content_group(self, content_group_id: str) -> None:
        """
        Deletes a content group.

        Args:
            content_group_id (str): The ID of the content group.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start delete content group")

            info: dict | None = _delete_content_group(self, content_group_id)

            if info is not None:
                logging.info("Delete content group complete")

            return info
        except Exception as error:
            logging.error("Delete content group failed")
            raise error

    def get_content_group(self, content_group_id: str) -> dict | None:
        """
        Gets a content group.

        Args:
            content_group_id (str): The ID of the content group.

        Returns:
            dict: The JSON response from the server if the content group is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get content group")

            content_group_info: dict | None = _get_content_group(self, content_group_id)

            if content_group_info is not None:
                logging.info("Get content group complete")

            return content_group_info
        except Exception as error:
            logging.error("Get content group failed")
            raise error

    def get_content_groups(self) -> dict | None:
        """
        Gets all content groups.

        Returns:
            dict: The JSON response from the server if the content groups are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get content groups")

            content_group_info: dict | None = _get_content_groups(self)

            if content_group_info is not None:
                logging.info("Get content groups complete")

            return content_group_info
        except Exception as error:
            logging.error("Get content groups failed")
            raise error

    def get_portal_groups(self, portal_groups: list[str]) -> dict | None:
        """
        Gets portal groups.

        Args:
            portal_groups (list[str]): The portal groups to get. The portal groups are
                contentGroups, sharedContentGroups, and savedSearches. You can only see a content
                groups if it is shared with you, or if you are the owner of the content group.

        Returns:
            dict: The JSON response from the server if the portal groups are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get portal groups")

            portal_groups_info: dict | None = _get_portal_groups(self, portal_groups)

            if portal_groups_info is not None:
                logging.info("Get portal groups complete")

            return portal_groups_info
        except Exception as error:
            logging.error("Get portal groups failed")
            raise error

    def remove_contents_from_content_group(self, content_group_id: str, content_ids: list[str]) -> None:
        """
        Removes contents from content group.

        Args:
            CONTENT_GROUP_ID (str): The ID of the content group.
            CONTENT_IDS (list[str]): The IDs of the content.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start remove contents from content group")

            info: dict | None = _remove_contents_from_content_group(self, content_group_id, content_ids)

            if info is not None:
                logging.info("Remove contents from content group complete")

            return info
        except Exception as error:
            logging.error("Remove contents from content group failed")
            raise error

    def rename_content_group(self, content_group_id: str, name: str) -> None:
        """
        Renames a content group.

        Args:
            content_group_id (str): The ID of the content group.
            name (str): The name of the content group.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start rename content group")

            info: dict | None = _rename_content_group(self, content_group_id, name)

            if info is not None:
                logging.info("Rename content group complete")

            return info
        except Exception as error:
            logging.error("Rename content group failed")
            raise error

    def share_content_group_with_user(self, content_group_id: str, user_ids: list[str]) -> None:
        """
        Shares a content group with users. To share a content group with a user, the
        user must meet certain requirements. They must not be a guest user and their account must be
        in a normal state. Only the owner, the user who created the content group, can share the
        content group. The user the content group is being shared with cannot change the collection.

        Args:
            content_group_id (str): The ID of the content group.
            user_ids (list[str]): The IDs of the users.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start share content group")

            info: dict | None = _share_content_group_with_user(self, content_group_id, user_ids)

            if info is not None:
                logging.info("Share content group complete")

            return info
        except Exception as error:
            logging.error("Share content group failed")
            raise error

    def stop_sharing_content_group_with_user(self, content_group_id: str, user_ids: list[str]) -> None:
        """
        Unshares a content group with users.

        Args:
            content_group_id (str): The ID of the content group.
            user_ids (list): The IDs of the users.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start unshare content group")

            info: dict | None = _stop_sharing_content_group_with_user(self, content_group_id, user_ids)

            if info is not None:
                logging.info("Unshare content group complete")

            return info
        except Exception as error:
            logging.error("Unshare content group failed")
            raise error

    def guest_invite(
            self,
            content_id: str | None,
            content_definition_id: str | None,
            emails: list[str],
            content_security_attribute: str) -> None:
        """
        Invites a guest.

        Args:
            content_id (str | None): The ID of the content to be shared to the user.
            content_definition_id (str | None): The ID of the content definition to be shared to the user.
            emails (list[str]): The email(s) of the guest(s).
            content_security_attribute (str): The content security attribute of the guest.
                The content security attribute can be "Undefined", "Guest", or "Demo".

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start invite guest")

            _guest_invite(self, content_id, content_definition_id, emails, content_security_attribute)

            logging.info("Invite guest complete")
        except Exception as error:
            logging.error("Invite guest failed")
            raise error

    def register_guest(self, email: str, first_name: str | None, last_name: str | None, password: str) -> dict | None:
        """
        Register a guest.

        Args:
            email (str): The email of the guest.
            first_name (str | None): The first name of the guest.
            last_name (str | None): The last name of the guest.
            password (str): The password of the guest.

        Returns:
            dict: The JSON response from the server if the guest is registered.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start register guest")

            guest_info: dict | None = _register_guest(self, email, first_name, last_name, password)

            if guest_info is not None:
                logging.info("Register guest complete")

            return guest_info
        except Exception as error:
            logging.error("Register guest failed")
            raise error

    def remove_guest(
            self,
            content_id: str | None,
            content_definition_id: str | None,
            emails: list[str],
            content_security_attribute: str) -> None:
        """
        Removes a guest.

        Args:
            content_id (str | None): The ID of the content to be unshared to the user.
            content_definition_id (str | None): The ID of the content definition to be unshared to the user.
            emails (list[str]): The email(s) of the guest(s).
            content_security_attribute (str): The content security attribute of the guest.
                The content security attribute can be "Undefined", "Guest", or "Demo".

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start remove guest")

            _remove_guest(self, content_id, content_definition_id, emails, content_security_attribute)

            logging.info("Remove guest complete")
        except Exception as error:
            logging.error("Remove guest failed")
            raise error

    # Media
    def clear_continue_watching(self, user_id: str | None, asset_id: str | None) -> None:
        """
        Delete continue watching markers.

        Args:
            user_id (str | None): The user ID of the user to clear the continue watching list.
                If no user Id is passed it clears the markers of the logged in user.
            asset_id (str | None): The asset ID of the asset to clear the continue watching list.
                If no asset Id is passed it clears the markers of all assets.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Clear continue watching")

            user_id = user_id if user_id else self.id

            _clear_continue_watching(self, user_id, asset_id)

            logging.info("Clear continue watching complete")
        except Exception as error:
            raise error

    def clear_watchlist(self, user_id: str | None) -> None:
        """
        Clears the watchlist.

        Args:
            user_id (str | None): The user ID of the user to clear the watchlist.
                If no user Id is passed it clears the watchlist of the logged in user.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Clear watchlist")

            user_id = user_id if user_id else self.id

            _clear_watchlist(self, user_id)

            logging.info("Clear watchlist complete")
        except Exception as error:
            raise error

    def create_form(self, content_definition_id: str, form_info: dict) -> dict | None:
        """
        Creates a form.

        Args:
            content_definition_id (str): The id of the content definition the form is going in.
            form_info (dict): The information of the form.

        Returns:
            dict: The JSON response from the server if the form is created.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start create form")

            form_id: dict | None = _create_form(self, content_definition_id, form_info)

            if form_id is not None:
                logging.info("Create form complete")

            return form_id
        except Exception as error:
            logging.error("Create form failed")
            raise error

    def get_content_cookies(self, content_id: str) -> dict | None:
        """
        Gets content cookies.

        Args:
            content_id (str): The Id of the content to retrieve the cookies for.
                This can be the ID for the content definition of the LiveChannel, or a folder asset ID or a specific Asset ID.

        Returns:
            dict: The JSON response from the server if the content cookies are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get content cookies")

            content_cookies_info: dict | None = _get_content_cookies(self, content_id)

            if content_cookies_info is not None:
                logging.info("Get content cookies complete")

            return content_cookies_info
        except Exception as error:
            logging.error("Get content cookies failed")
            raise error

    def get_default_site_config(self) -> list[dict] | None:
        """
        Gets default site config.

        Returns:
            list[dict]: The JSON response from the server if the default site config is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get default site config")

            default_site_config_info: dict | None = _get_default_site_config(self)

            if default_site_config_info is not None:
                logging.info("Get default site config complete")

            return default_site_config_info
        except Exception as error:
            logging.error("Get default site config failed")
            raise error

    def get_dynamic_content(self, dynamic_content_record_id: str) -> dict | None:
        """
        Gets dynamic content.

        Args:
            dynamic_content_record_id (str): The dynamic content record ID.

        Returns:
            dict: The JSON response from the server if the dynamic content is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get dynamic content")

            dynamic_content_info: dict | None = _get_dynamic_content(self, dynamic_content_record_id)

            if dynamic_content_info is not None:
                logging.info("Get dynamic content complete")

            return dynamic_content_info
        except Exception as error:
            logging.error("Get dynamic content failed")
            raise error

    def get_dynamic_contents(self) -> list[dict] | None:
        """
        Gets dynamic contents.

        Returns:
            list[dict]: The JSON response from the server if the dynamic contents are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get dynamic contents")

            dynamic_contents_info: dict | None = _get_dynamic_contents(self)

            if dynamic_contents_info is not None:
                logging.info("Get dynamic contents complete")

            return dynamic_contents_info
        except Exception as error:
            logging.error("Get dynamic contents failed")
            raise error

    def get_media_group(self, media_group_id: str) -> dict | None:
        """
        Gets media group.

        Args:
            media_group_id (str): The ID of the media group.

        Returns:
            dict: Returns the information of the gotten media group.

        Exception:
            If the media group fails to get.
            If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get media")

            media_info: dict | None = _get_media_group(self, media_group_id)

            if media_info is not None:
                logging.info("Get media complete")

            return media_info
        except Exception as error:
            logging.error("Get media failed")
            raise error

    def get_media_item(self, media_item_id: str) -> dict | None:
        """
        Gets media item.

        Args:
            media_item_id (str): The ID of the media item.

        Returns:
            dict: Returns the information of the gotten media item.

        Exception:
            If the media item fails to get.
            If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get media")

            media_info: dict | None = _get_media_item(self, media_item_id)

            if media_info is not None:
                logging.info("Get media complete")

            return media_info
        except Exception as error:
            logging.error("Get media failed")
            raise error

    def get_my_content(self) -> dict | None:
        """
        Gets favorites and continue watching lists of IDs for the logged in user.

        Returns:
            dict: The JSON response from the server if the my media IDs are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            my_media_ids_info: dict | None = _get_my_content(self)

            if my_media_ids_info is not None:
                logging.info("Get my media IDs complete")

            return my_media_ids_info
        except Exception as error:
            logging.error("Get my media IDs failed")
            raise error

    def get_my_group(self, group_id: str) -> dict | None:
        """
        Gets user's group.

        Args:
            group_id (str): The ID of the group.

        Returns:
            dict: The JSON response from the server if the user group is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get user group")

            user_group_info: dict | None = _get_my_group(self, group_id)

            if user_group_info is not None:
                logging.info("Get user group complete")

            return user_group_info
        except Exception as error:
            logging.error("Get user group failed")
            raise error

    def get_site_config(self, site_config_record_id: str) -> dict | None:
        """
        Gets site config.

        Args:
            site_config_record_id (str): The site config record ID.

        Returns:
            dict: The JSON response from the server if the site config is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get site config")

            site_config_info: dict | None = _get_site_config(self, site_config_record_id)

            if site_config_info is not None:
                logging.info("Get site config complete")

            return site_config_info
        except Exception as error:
            logging.error("Get site config failed")
            raise error

    def media_search(
        self,
        query: str | None,
        ids: list[str] | None,
        sort_fields: list[dict],
        offset: int | None,
        size: int | None
    ) -> dict | None:
        """
        Searches for media.

        Args:
            query (str | None): The query of the search.
            ids (list[str] | None): The ids of the media to be searched.
            sort_fields (list[dict] | None): The sort fields of the search.
                dict format: {"fieldName": "string", "sortType": ("Ascending" | "Descending")}
            offset (int | None): The offset of the search.
            size (int | None): The size of the search.

        Returns:
            dict: The JSON response from the server if the media is searched.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start search media")

            search_info: dict | None = _media_search(self, query, ids, sort_fields, offset, size)

            if search_info is not None:
                logging.info("Search media complete")

            return search_info
        except Exception as error:
            logging.error("Search media failed")
            raise error

    # Media Builder
    def create_media_builder(
        self,
        name: str,
        destination_folder_id: str | None,
        collections: list[str] | None,
        related_contents: list[str] | None,
        tags: list[str] | None,
        properties: dict | None
    ) -> dict | None:
        """
        Creates a media builder.

        Args:
            name (str): The name of the media builder.
            destination_folder_id (str | None): The ID of the destination folder.
            collections (list[str] | None): The collections of the media builder.
            related_contents (list[str] | None): The related contents of the media builder.
            tags: (list[str] | None): The tags of the media builder.
            properties (dict | None): The properties of the media builder.

        Returns
            dict: The JSON response from the server if the media builder is created.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start create media builder")

            media_builder_info: dict | None = _create_media_builder(
                self, name, destination_folder_id, collections, related_contents, tags, properties
            )

            if media_builder_info is not None:
                logging.info("Create media builder complete")

            return media_builder_info
        except Exception as error:
            logging.error("Create media builder failed")
            raise error

    def create_media_builder_item(
        self,
        media_builder_id: str,
        source_asset_id: str | None,
        start_time_code: str | None,
        end_time_code: str | None,
        source_annotation_id: str | None,
        related_contents: list[str] | None
    ) -> dict | None:
        """
        Creates a media builder item.

        Args:
            media_builder_id (str): The ID of the media builder.
            source_asset_id (str | None): The ID of the source asset.
            start_time_code (str | None): The start time code of the media builder item. Only use if using source asset.
                Please use the following format: hh:mm:ss;ff.
            end_time_code (str | None): The end time code of the media builder item. Only use if using source asset.
                Please use the following format: hh:mm:ss;ff.
            source_annotation_id (str | None): The ID of the source annotation. Only use if using source annotation.
            related_contents (list[str] | None): The related contents of the media builder item.

        Returns:
            dict: The JSON response from the server if the media builder item is created.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start create media builder item")

            media_builder_item_info: dict | None = _create_media_builder_item(
                self, media_builder_id, source_asset_id, start_time_code, end_time_code,
                source_annotation_id, related_contents
            )

            if media_builder_item_info is not None:
                logging.info("Create media builder item complete")

            return media_builder_item_info
        except Exception as error:
            logging.error("Create media builder item failed")
            raise error

    def create_media_builder_items_add_annotations(
        self,
        media_builder_id: str,
        source_asset_id: str
    ) -> list[dict] | None:
        """
        Creates media builder items from annotations

        Args:
            media_builder_id (str): The ID of the media builder.
            source_asset_id (str): The ID of the source asset.

        Returns:
            list[dict]: The JSON response from the server if the media builder items are created.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start create media builder items from annotations")

            media_builder_items_info: dict | None = _create_media_builder_items_add_annotations(
                self, media_builder_id, source_asset_id
            )

            if media_builder_items_info is not None:
                logging.info("Create media builder items from annotations complete")

            return media_builder_items_info
        except Exception as error:
            logging.error("Create media builder items from annotations failed")
            raise error

    def create_media_builder_items_bulk(self, media_builder_id: str, media_builder_items: list[dict]) -> None:
        """
        Creates media builder items in bulk

        Args:
            media_builder_id (str): The ID of the media builder.
            media_builder_items (list[dict]): The list of media builder items.
                dict format: {"sourceAssetId": "string", "sourceAnnotationId": "string | null",
                "startTimeCode": "string | null", "endTimeCode": "string | null"}

        Returns:
            dict: The JSON response from the server if the media builder items are created.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            logging.info("Start create media builder items in bulk")

            media_builder_items_info: dict | None = _create_media_builder_items_bulk(
                self, media_builder_id, media_builder_items
            )

            if media_builder_items_info is not None:
                logging.info("Create media builder items in bulk complete")

            return media_builder_items_info
        except Exception as error:
            logging.error("Create media builder items in bulk failed")
            raise error

    def delete_media_builder(self, media_builder_id: str) -> None:
        """
        Deletes a media builder.

        Args:
            media_builder_id (str): The ID of the media builder.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start delete media builder")

            _delete_media_builder(self, media_builder_id)

            logging.info("Delete media builder complete")
        except Exception as error:
            logging.error("Delete media builder failed")
            raise error

    def delete_media_builder_item(self, media_builder_id: str, media_builder_item_id: str) -> None:
        """
        Deletes a media builder item.

        Args:
            media_builder_id (str): The ID of the media builder.
            media_builder_item_id (str): The ID of the media builder item.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start delete media builder item")

            _delete_media_builder_item(self, media_builder_id, media_builder_item_id)

            logging.info("Delete media builder item complete")
        except Exception as error:
            logging.error("Delete media builder item failed")
            raise error

    def duplicate_media_builder(
            self,
            media_builder_id: str,
            name: str,
            destination_folder_id: str | None,
            collections: list[str] | None,
            related_contents: list[str] | None,
            properties: dict | None) -> dict | None:
        """
        Duplicates a media builder.

        Args:
            media_builder_id (str): The ID of the media builder.
            name (str): The name of the media builder.
            destination_folder_id (str | None): The ID of the destination folder.
            collections (list[str] | None): The collections of the media builder.
            related_contents (list[str] | None): The related contents of the media builder.
            properties (dict | None): The properties of the media builder.

        Returns:
            dict: The JSON response from the server if the media builder is duplicated.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start duplicate media builder")

            duplicated_media_builder_info: dict | None = _duplicate_media_builder(
                self, media_builder_id, name, destination_folder_id, collections,
                related_contents, properties
            )

            if duplicated_media_builder_info is not None:
                logging.info("Duplicate media builder complete")

            return duplicated_media_builder_info
        except Exception as error:
            logging.error("Duplicate media builder failed")
            raise error

    def get_media_builder(self, media_builder_id: str) -> dict | None:
        """
        Gets a media builder.

        Args:
            media_builder_id (str): The ID of the media builder.

        Returns:
            dict: The JSON response from the server if the media builder is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start get media builder")

            media_builder_info: dict | None = _get_media_builder(self, media_builder_id)

            if media_builder_info is not None:
                logging.info("Get media builder complete")

            return media_builder_info
        except Exception as error:
            logging.error("Get media builder failed")
            raise error

    def get_media_builder_ids_from_asset(self, source_asset_id: str) -> list[str] | None:
        """
        Gets media builder ids from a given asset.

        Args:
            source_asset_id (str): The ID of the source asset.

        Returns:
            list[str]: The string response from the server if the media builder ids are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start get media builder item ids from asset")

            media_builder_item_ids_info: dict | None = _get_media_builder_ids_from_asset(self, source_asset_id)

            if media_builder_item_ids_info is not None:
                logging.info("Get media builder item ids from asset complete")

            return media_builder_item_ids_info
        except Exception as error:
            logging.error("Get media builder item ids from asset failed")
            raise error

    def get_media_builders(self) -> list[dict] | None:
        """
        Gets media builders

        Returns:
            list[dict]: The JSON response from the server if the media builders are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get media builders")

            media_builders_info: dict | None = _get_media_builders(self)

            if media_builders_info is not None:
                logging.info("Get media builders complete")

            return media_builders_info
        except Exception as error:
            logging.error("Get media builders failed")
            raise error

    def get_media_builder_items(self, media_builder_id) -> list[dict] | None:
        """
        Gets media builder items.

        Args:
            media_builder_id (str): The ID of the media builder.

        Returns:
            list[dict]: The JSON response from the server if the media builder items are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start get media builder items")

            media_builder_items_info: dict | None = _get_media_builder_items(self, media_builder_id)

            if media_builder_items_info is not None:
                logging.info("Get media builder items complete")

            return media_builder_items_info
        except Exception as error:
            logging.error("Get media builder items failed")
            raise error

    def move_media_builder_item(
        self,
        media_builder_id: str,
        media_builder_item_id: str,
        media_builder_previous_item_id: str | None
    ) -> None:
        """
        Moves a media builder item.

        Args:
            media_builder_id (str): The ID of the media builder.
            media_builder_item_id (str): The ID of the media builder item.
            media_builder_previous_item_id (str | None): The ID of the media builder previous item.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            _move_media_builder_item(self, media_builder_id, media_builder_item_id, media_builder_previous_item_id)
            logging.info("Move media builder item complete")
        except Exception as error:
            logging.error("Move media builder item failed")
            raise error

    def render_media_builder(self, media_builder_id: str) -> dict | None:
        """
        Renders a media builder.

        Args:
            media_builder_id (str): The ID of the media builder.

        Returns:
            dict: The JSON response from the server if the media builder is rendered.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")
            logging.info("Start render media builder")

            render_info: dict | None = _render_media_builder(self, media_builder_id)

            if render_info is not None:
                logging.info("Render media builder complete")

            return render_info
        except Exception as error:
            logging.error("Render media builder failed")
            raise error

    def update_media_builder(
        self,
        media_builder_id: str,
        name: str | None,
        destination_folder_id: str | None,
        collections: list[str] | None,
        related_contents: list[str] | None,
        tags: list[str] | None,
        properties: dict | None
    ) -> dict | None:
        """
        Updates a media builder.

        Args:
            media_builder_id (str): The ID of the media builder.
            name (str | None): The name of the media builder.
            destination_folder_id (str | None): The ID of the destination folder.
            collections (list[str] | None): The collections of the media builder.
            related_contents (list[str] | None): The related contents of the media builder.
            tags (list[str] | None): The tags of the media builder.
            properties (dict | None): The properties of the media builder.

        Returns:
            dict: The JSON response from the server if the media builder is updated.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start update media builder")

            builder_info: dict | None = _update_media_builder(
                self, media_builder_id, name, destination_folder_id, collections, related_contents,
                tags, properties
            )

            if builder_info is not None:
                logging.info("Update media builder complete")

            return builder_info
        except Exception as error:
            logging.error("Update media builder failed")
            raise error

    # Saved Search
    def add_saved_search(
        self,
        name: str,
        featured: bool,
        bookmarked: bool,
        public: bool | None,
        sequence: int | None,
        saved_search_type: int | None,
        query: str | None,
        offset: int | None,
        size: int | None,
        filters: list[dict] | None,
        sort_fields: list[dict] | None,
        search_result_fields: list[dict] | None,
        similar_asset_id: str | None,
        min_score: float | None,
        exclude_total_record_count: bool | None,
        filter_binder: str | None
    ) -> dict | None:
        """
        Adds a saved search.

        Args:
            name (str): The name of the saved search.
            featured (bool | None): If the saved search is featured.
            bookmarked (bool | None): If the saved search is bookmarked.
            public (bool | None): If the saved search is public.
            sequence (int | None): The sequence of the saved search.
            saved_search_type (int | None): The type of the saved search. 0 = List, 1 = Preview Image, 2 = Header.
            query (str | None): The query of the search.
            offset (int | None): The offset of the search.
            size (int | None): The size of the search.
            filters (list[dict] | None): The filters of the search.
                dict format: {"fieldName": "string", "operator": "string", "values" : "list of strings"}
            sort_fields (list[dict] | None): The sort fields of the search.
                dict format: {"fieldName": "string", "sortType": ("Ascending" | "Descending")}
            search_result_fields (list[dict] | None): The property fields you want to show in the result.
                dict format: {"name": "string"}
            similar_asset_id (str | None): When SimilarAssetId has a value, then the search results are a special
                type of results and bring back the items that are the most similar to the item represented here.
                This search is only enabled when Vector searching has been enabled.
                When this has a value, the SearchQuery value and PageOffset values are ignored.
            min_score (float | None): Specifies the minimum score to match when returning results.
                If omitted, the system default will be used - which is usually .65
            exclude_total_record_count (bool | None): Normally, the total record count is returned but the query
                can be made faster if this value is excluded.
            filter_binder (str | None): The filter binder of the search. 0 = AND, 1 = OR.

        Returns:
            dict: The JSON response from the server if the saved search is added.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start add saved search")

            saved_search_info: dict | None = _add_saved_search(
                self, name, featured, bookmarked, public, sequence, saved_search_type, query, offset, size,
                filters, sort_fields, search_result_fields, similar_asset_id, min_score,
                exclude_total_record_count, filter_binder
            )

            if saved_search_info is not None:
                logging.info("Add saved search complete")

            return saved_search_info
        except Exception as error:
            logging.error("Add saved search failed")
            raise error

    def delete_saved_search(self, saved_search_id: str) -> None:
        """
        Deletes a saved search.

        Args:
            id (str): The ID of the saved search.

        Returns:
            None: If the request succeeds.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start delete saved search")

            _delete_saved_search(self, saved_search_id)

            logging.info("Delete saved search complete")
        except Exception as error:
            logging.error("Delete saved search failed")
            raise error

    def get_saved_search(self, saved_search_id: str) -> dict | None:
        """
        Gets a saved search.

        Args:
            id (str): The ID of the saved search.

        Returns:
            dict: The JSON response from the server if the saved search is retrieved.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get saved search")

            saved_search_info: dict | None = _get_saved_search(self, saved_search_id)

            if saved_search_info is not None:
                logging.info("Get saved search complete")

            return saved_search_info
        except Exception as error:
            logging.error("Get saved search failed")
            raise error

    def get_saved_searches(self) -> list[dict] | None:
        """
        Gets saved searches.

        Returns:
            list[dict]: The JSON response from the server if the saved searches are retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get saved searches")

            saved_searches_info: dict | None = _get_saved_searches(self)

            if saved_searches_info is not None:
                logging.info("Get saved searches complete")

            return saved_searches_info
        except Exception as error:
            logging.error("Get saved searches failed")
            raise error

    def get_search_saved(
        self,
        query: str | None,
        offset: int | None,
        size: int | None,
        filters: list[dict] | None,
        sort_fields: list[dict] | None,
        search_result_fields: list[dict] | None,
        similar_asset_id: str | None,
        min_score: float | None,
        exclude_total_record_count: bool | None,
        filter_binder: str | None
    ) -> dict | None:
        """
        Gets search saved based on params.

        Args:
            query (str | None): The query of the search.
            offset (int | None): The offset of the search.
            size (int | None): The size of the search.
            filters (list[dict] | None): The filters of the search.
                dict format: {"fieldName": "string", "operator": "string", "values" : "array<string>" | "string"}
            sort_fields (list[dict] | None): The sort fields of the search.
                dict format: {"fieldName": "string", "sortType": ("Ascending" | "Descending")}
            search_result_fields (list[dict] | None): The property fields you want to show in the result.
                dict format: {"name": "string"}
            similar_asset_id (str | None): When SimilarAssetId has a value, then the search results are a special
                type of results and bring back the items that are the most similar to the item represented here.
                This search is only enabled when Vector searching has been enabled. When this has a value,
                the SearchQuery value and PageOffset values are ignored.
            min_score (float | None): Specifies the minimum score to match when returning results.
                If omitted, the system default will be used - which is usually .65
            exclude_total_record_count (bool | None): Normally, the total record count is returned but the
                query can be made faster if this value is excluded.
            filter_binder (str | None): The filter binder of the search. 0 = AND, 1 = OR.

        Returns:
            dict: The JSON response from the server if the search saved is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get search saved")

            search_saved_info: dict | None = _get_search_saved(
                self, query, offset, size, filters, sort_fields, search_result_fields, similar_asset_id,
                min_score, exclude_total_record_count, filter_binder
            )

            if search_saved_info is not None:
                logging.info("Get search saved complete")

            return search_saved_info
        except Exception as error:
            logging.error("Get search saved failed")
            raise error

    def get_search_saved_by_id(self, saved_search_id: str) -> dict | None:
        """
        Gets search saved by id

        Args:
            id (str): The ID of the search saved.

        Returns:
            dict: The JSON response from the server if the search saved is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get search saved")

            search_saved_info: dict | None = _get_search_saved_by_id(self, saved_search_id)

            if search_saved_info is not None:
                logging.info("Get search saved complete")

            return search_saved_info
        except Exception as error:
            logging.error("Get search saved failed")
            raise error

    def patch_saved_search(
        self,
        saved_search_id: str,
        name: str | None,
        featured: bool | None,
        bookmarked: bool | None,
        public: bool | None,
        sequence: int | None
    ) -> dict | None:
        """
        Patches a saved search.

        Args:
            saved_search_id (str): The ID of the saved search.
            name (str | None): The name of the saved search.
            featured (bool | None): If the saved search is featured.
            bookmarked (bool | None): If the saved search is bookmarked.
            public (bool | None): If the saved search is public.
            sequence (int | None): The sequence of the saved search.

        Returns:
            dict: The JSON response from the server if the saved search is patched.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start patch saved search")

            saved_search_info: dict | None = _patch_saved_search(
                self, saved_search_id, name, featured, bookmarked, public, sequence
            )

            if saved_search_info is not None:
                logging.info("Patch saved search complete")

            return saved_search_info
        except Exception as error:
            logging.error("Patch saved search failed")
            raise error

    def update_saved_search(
        self,
        saved_search_id: str,
        name: str | None,
        featured: bool | None,
        bookmarked: bool | None,
        public: bool | None,
        sequence: int | None,
        saved_search_type: int | None,
        query: str | None,
        offset: int | None,
        size: int | None,
        filters: list[dict] | None,
        sort_fields: list[dict] | None,
        search_result_fields: list[dict] | None,
        similar_asset_id: str | None,
        min_score: float | None,
        exclude_total_record_count: bool | None,
        filter_binder: str | None
    ) -> dict | None:
        """
        Updates a saved search.

        Args:
            saved_search_id (str): The ID of the saved search.
            name (str | None): The name of the saved search.
            featured (bool | None): If the saved search is featured.
            bookmarked (bool | None): If the saved search is bookmarked.
            public (bool | None): If the saved search is public.
            sequence (int | None): The sequence of the saved search.
            saved_search_type (int | None): The type of the saved search. 0 = List, 1 = Preview Image, 2 = Header.
            query (str | None): The query of the search.
            offset (int | None): The offset of the search.
            size (int | None): The size of the search.
            filters (list[dict] | None): The filters of the search.
                dict format: {"fieldName": "string", "operator": "string", "values" : "array<string>" | "string"}
            sort_fields (list[dict] | None): The sort fields of the search.
                dict format: {"fieldName": "string", "sortType": ("Ascending" | "Descending")}
            search_result_fields (list[dict] | None): The property fields you want to show in the result.
                dict format: {"name": "string"}
            similar_asset_id (str | None): When SimilarAssetId has a value, then the search results are a special type
                of results and bring back the items that are the most similar to the item represented here.
                This search is only enabled when Vector searching has been enabled.
                When this has a value, the SearchQuery value and PageOffset values are ignored.
            min_score (float | None): Specifies the minimum score to match when returning results.
                If omitted, the system default will be used - which is usually .65
            exclude_total_record_count (bool | None): Normally, the total record count is returned but the query
                can be made faster if this value is excluded.
            filter_binder (str | None): The filter binder of the search. 0 = AND, 1 = OR.

        Returns:
            dict: The JSON response from the server if the saved search is updated.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start update saved search")

            saved_search_info: dict | None = _update_saved_search(
                self, saved_search_id, name, featured, bookmarked, public, sequence, saved_search_type,
                query, offset, size, filters, sort_fields, search_result_fields, similar_asset_id,
                min_score, exclude_total_record_count, filter_binder
            )

            if saved_search_info is not None:
                logging.info("Update saved search complete")

            return saved_search_info
        except Exception as error:
            logging.error("Update saved search failed")
            raise error

    # Share
    def delete_share(self, share_id: str) -> dict | None:
        """
        Deletes an asset

        Args:
            share_id (str): The share id of the deleteShare.

        Returns:
            dict: The JSON response form the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal type.")

            logging.info("Calling delete share")

            response: dict | None = _delete_share(self, share_id)

            if response is not None:
                logging.info("Delete share called successfully.")

            return response
        except Exception as error:
            logging.error("Calling delete share failed")
            raise error

    def get_share(self, share_id: str) -> dict | None:
        """
        Gets an asset

        Args:
            share_id (str): The share id of the getShare.

        Returns:
            dict: The JSON response form the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal type.")

            logging.info("Calling get share")

            response: dict | None = _get_share(self, share_id)

            if response is not None:
                logging.info("Get share called successfully.")

            return response
        except Exception as error:
            logging.error("Calling get share failed")
            raise error

    def share(
        self,
        id: str | None,
        name: str | None,
        shared_contents: list[str] | None,
        shared_duration: dict | None,
        shared_permissions: list[dict] | None,
        shared_type: dict | None,
        shared_status: list[dict] | None,
        shared_duration_in_hours: int | None,
        shared_link: str | None,
        owner_id: str | None,
        expiration_date: str | None
    ) -> dict | None:
        """
        Share an asset

        Args:
            id (str | None): The id of the share.
            name (str | None): The name of the share.
            shared_contents (list[str] | None): The shared contents of the share.
            shared_duration (dict | None): The shared duration of the share.
            dict format: {"id": "string", "description": "string"}
            shared_permissions (list[dict] | None): The shared permissions of the share.
            dict format: {"id": "string", "description": "string"}
            shared_type (dict | None): The shared type of the share.
            dict format: {"id": "string", "description": "string"}
            shared_status (list[dict] | None): The shared status of the share.
            dict format: {"id": "string", "description": "string"}
            shared_duration_in_hours (int | None): The shared duration in hours of the share.
            shared_link (str | None): The shared link of the share.
            owner_id (str | None): The owner id of the share.
            expiration_date (str | None): The expiration date of the share.

        Returns:
            dict: The JSON response form the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal type.")

            logging.info("Calling share")

            response: dict | None = _share(
                self, id, name, shared_contents, shared_duration, shared_permissions, shared_type,
                shared_status, shared_duration_in_hours, shared_link, owner_id, expiration_date
            )

            if response is not None:
                logging.info("share called successfully.")

            return response
        except Exception as error:
            logging.error("Calling share failed")
            raise error

    def share_expire(self, share_id: str) -> None:
        """
        Expire a share

        Args:
            share_id (str): The share id of the shareExpire.

        Returns:
            Unknown Type: If the request succeeds.

        Exceptions:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal type.")

            logging.info("Calling Share expire")

            response: dict | None = _share_expire(self, share_id)

            if response is not None:
                logging.info("Share expire called successfully.")

            return response
        except Exception as error:
            logging.error("Calling Share expire failed")
            raise error

    def share_notification(
        self,
        share_id: str,
        nomad_users: list[dict] | None,
        external_users: list[dict] | None
    ) -> None:
        """
        Get an notification when asset is shared

        Args:
            share_id (str): The share id of the shareNotification.
            nomad_users (list[dict] | None): The nomad users of the shareNotification.
            dict format: {"id": "string", "description": "string"}
            external_users (list[dict] | None): The external users of the shareNotification.
            dict format: {"id": "string", "description": "string"}

        Returns:
            Unknown Type: If the request succeeds.
        Exceptions:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal type.")

            logging.info("Calling shareNotification")

            response: dict | None = _share_notification(
                self, share_id, nomad_users, external_users
            )

            if response is not None:
                logging.info("shareNotification called successfully.")

            return response
        except Exception as error:
            logging.error("Calling shareNotification failed")
            raise error

    def update_share(
        self,
        share_id: str,
        id: str | None,
        name: str | None,
        shared_contents: list[str] | None,
        shared_duration: dict | None,
        shared_permissions: list[dict] | None,
        shared_type: dict | None,
        shared_status: list[dict] | None,
        shared_duration_in_hours: int | None,
        shared_link: str | None,
        owner_id: str | None,
        expiration_date: str | None
    ) -> dict | None:
        """
        Updates an asset

        Args:
            share_id (str ): The share id of the updateShare.
            id (str | None): The id of the updateShare.
            name (str | None): The name of the updateShare.
            shared_contents (list[str] | None): The shared contents of the updateShare.
            shared_duration (dict | None): The shared duration of the updateShare.
            dict format: {"id": "string", "description": "string"}
            shared_permissions (list[dict] | None): The shared permissions of the updateShare.
            dict format: {"id": "string", "description": "string"}
            shared_type (dict | None): The shared type of the updateShare.
            dict format: {"id": "string", "description": "string"}
            shared_status (list[dict] | None): The shared status of the updateShare.
            dict format: {"id": "string", "description": "string"}
            shared_duration_in_hours (int | None): The shared duration in hours of the updateShare.
            shared_link (str | None): The shared link of the updateShare.
            owner_id (str | None): The owner id of the updateShare.
            expiration_date (str | None): The expiration date of the updateShare.

        Returns:
            dict: The JSON response form the server if the request is successful.
            None: If the request fails or the response cannot be parsed as JSON.

        Exceptions:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal type.")

            logging.info("Calling updateShare")

            response: dict | None = _update_share(
                self, share_id, id, name, shared_contents, shared_duration, shared_permissions,
                shared_type, shared_status, shared_duration_in_hours, shared_link, owner_id, expiration_date
            )

            if response is not None:
                logging.info("updateShare called successfully.")

            return response
        except Exception as error:
            logging.error("Calling updateShare failed")
            raise error

    # Video Tracking

    def get_video_tracking(self, asset_id: str, tracking_event: str, seconds: int | None) -> dict | None:
        """
        Gets video tracking.

        Args:
            asset_id (str): The id of the asset.
            tracking_event (str): The tracking event of the asset. The value of tracking
            event's value can be 0-5 with 0 being no tracking event, 1-4 being the progress in quarters,
            i.e 3 meaning it is tracking 3 quarters of the video, and 5 meaning that the tracking is
                hidden.
            seconds (int | None): The seconds into the video being tracked.

        Returns:
            dict: The JSON response from the server if the video tracking is retrieved.
            None: If the request fails or the response cannot be parsed as JSON.

        Exception:
            InvalidAPITypeException: If the API type is not portal.
        """

        try:
            if self.config["apiType"] != "portal":
                raise InvalidAPITypeException("This function is only available for portal API type.")

            logging.info("Start get video tracking")

            video_tracking_info: dict | None = _get_video_tracking(self, asset_id, tracking_event, seconds)

            if video_tracking_info is not None:
                logging.info("Get video tracking complete")

            return video_tracking_info
        except Exception as error:
            logging.error("Get video tracking failed")
            raise error

    def misc_function(self, url_path: str, method: str, body: dict, not_api_path: bool) -> dict | None:
        """
        Calls any nomad function given URL, method, and body.

        Args:
            url_path (str): The URL of the nomad function.
            method (str): The method of the nomad function.
            body (dict): The body of the nomad function.
            not_api_path (bool): If the path has /api in it.

        Returns:
            dict: The information of the nomad function.

        """

        try:
            logging.info("Calling function %s", url_path)

            api_url: str = f'{self.config["serviceApiUrl"]}/{url_path}'
            if not_api_path:
                api_url = api_url.replace('/api', '')
                api_url = api_url.replace('app-api.', '')
                api_url = api_url.replace('admin-app.', '')

            info: dict | None = _send_request(self, url_path, api_url, method, None, body)

            if info is not None:
                logging.info("Function %s complete", url_path)

            return info

        except Exception as error:
            logging.error("Misc function failed")
            raise error
