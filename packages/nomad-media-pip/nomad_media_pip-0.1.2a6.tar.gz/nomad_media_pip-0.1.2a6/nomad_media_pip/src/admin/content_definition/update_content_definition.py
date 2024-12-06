"""
This module updates a content definition in the service.

Functions:
    _update_content_definition: Updates a content definition in the service.
"""


from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.content_definition.get_content_definition import _get_content_definition
from nomad_media_pip.src.admin.content_definition.get_content_definition_groups import _get_content_definition_groups
from nomad_media_pip.src.admin.content_definition.get_content_definition_types import _get_content_definition_types
from nomad_media_pip.src.admin.live_channel.get_security_groups import _get_security_groups
from nomad_media_pip.src.admin.content_definition.get_system_roles import _get_system_roles


def _update_content_definition(
    self,
    content_definition_id: str,
    name: str | None,
    content_fields: list[dict],
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
    Updates a content definition in the service.

    Args:
        content_definition_id (string): The ID of the content definition to update.
        name (str | None): The name of the content definition.
        content_fields (list of dict | None): The content fields of the content definition.
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
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/contentDefinition/{content_definition_id}"

    if content_definition_group:
        content_definiiton_groups: dict | None = _get_content_definition_groups(
            self)
        content_definition_group_info: dict | None = (
            next(
                (
                    group for group in content_definiiton_groups["items"]
                    if group["title"] == content_definition_group
                ),
                None
            )
        )
    else:
        content_definition_group_info = None

    if content_definition_type:
        content_definition_types: dict | None = _get_content_definition_types(
            self)
        content_definition_type_info: dict | None = (
            next(
                (
                    def_type for def_type in content_definition_types["items"]
                    if def_type["description"] == content_definition_type
                ),
                None
            )
        )
    else:
        content_definition_type_info = None

    content_definition_info: dict | None = _get_content_definition(self, content_definition_id)

    if content_definition_info is not None:
        if display_field:
            display_field_info: dict | None = (
                next(
                    (
                        field for field in content_definition_info["contentFields"]
                        if field["properties"]["title"] == display_field
                    ),
                    None
                )
            )
        if route_item_name_field:
            route_item_name_field_info: dict | None = (
                next(
                    (
                        field for field in content_definition_info["contentFields"]
                        if field["properties"]["title"] == route_item_name_field
                    ),
                    None
                )
            )
    else:
        content_definition_info = None
        display_field_info = (
            next(
                (
                    field for field in content_fields
                    if field["properties"]["title"] == display_field
                ),
                None
            )
            if display_field else None
        )

        route_item_name_field_info = (
            next(
                (
                    field for field in content_fields
                    if field["properties"]["title"] == route_item_name_field
                ),
                None
            )
            if route_item_name_field else None
        )

    if security_groups:
        security_groups_info: dict | None = _get_security_groups(self)
        security_groups_selected_info: list = [
            group for group in security_groups_info["items"]
            if group["description"] in security_groups
        ]
    else:
        security_groups_selected_info = None

    if system_roles:
        system_roles_info: dict | None = _get_system_roles(self)
        system_roles_selected_info: list = [
            role for role in system_roles_info["items"]
            if role["description"] in system_roles
        ]
    else:
        system_roles_selected_info = None

    body: dict = {
        "contentDefinitionId": content_definition_id,
        "contentFields": content_fields or content_definition_info.get("contentFields"),
        "properties": {
            "assignedSecurityGroups": (
                security_groups_selected_info
                if security_groups_selected_info is not None
                else content_definition_info.get("assignedSecurityGroups")
                if content_definition_info is not None
                else []
            ),
            "assignedSystemRoles": (
                system_roles_selected_info
                if system_roles_selected_info is not None
                else content_definition_info.get("assignedSystemRoles")
                if content_definition_info is not None
                else []
            ),
            "includeInTags": (
                include_in_tags
                if include_in_tags is not None
                else content_definition_info.get("includeTags")
                if content_definition_info is not None
                else None
            ),
            "indexContent": (
                index_content
                if index_content is not None
                else content_definition_info.get("indexContent")
                if content_definition_info is not None
                else None
            ),
            "title": (
                name
                if name is not None
                else content_definition_info.get("title")
                if content_definition_info is not None
                else None
            )
        }
    }

    body["properties"]["contentDefinitionGroupId"] = (
        {
            "description": content_definition_group_info["title"],
            "id": content_definition_group_info["contentDefinitionGroupId"]
        }
        if content_definition_group_info is not None
        else content_definition_info.get("contentDefinitionGroupId")
        if content_definition_info is not None
        else None
    )

    body["properties"]["contentTypeId"] = (
        {
            "description": content_definition_type_info["description"],
            "id": content_definition_type_info["id"]
        }
        if content_definition_type_info is not None
        else content_definition_info.get("contentDefinitionTypeId")
        if content_definition_info is not None
        else None
    )

    body["properties"]["displayField"] = (
        {
            "description": display_field_info["properties"]["title"],
            "id": display_field_info["contentFieldId"]
        }
        if display_field_info is not None
        else content_definition_info.get("displayField")
        if content_definition_info is not None
        else None
    )

    body["properties"]["routeItemNameField"] = (
        {
            "description": route_item_name_field_info["properties"]["title"],
            "id": route_item_name_field_info["id"]
        }
        if route_item_name_field_info is not None
        else content_definition_info.get("routeItemNameField")
        if content_definition_info is not None
        else None
    )

    _send_request(self, "Update content definition", api_url, "PUT", None, body)
