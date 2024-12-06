from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.auth import resource__client_pb2 as _resource__client_pb2
from tecton_proto.auth import resource_role_assignments__client_pb2 as _resource_role_assignments__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AssignRolesPutRequest(_message.Message):
    __slots__ = ["principal_id", "principal_type", "resource_id", "resource_type", "roles"]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLES_FIELD_NUMBER: ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: Optional[str] = ..., principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ..., roles: Optional[Iterable[str]] = ...) -> None: ...

class AssignRolesPutResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class AssignRolesRequest(_message.Message):
    __slots__ = ["assignments"]
    ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[Assignment]
    def __init__(self, assignments: Optional[Iterable[Union[Assignment, Mapping]]] = ...) -> None: ...

class AssignRolesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Assignment(_message.Message):
    __slots__ = ["principal_id", "principal_type", "resource_id", "resource_type", "role"]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLE_FIELD_NUMBER: ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    role: str
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: Optional[str] = ..., role: Optional[str] = ..., principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ...) -> None: ...

class AssignmentBasic(_message.Message):
    __slots__ = ["principal", "role_assignments", "roles"]
    PRINCIPAL_FIELD_NUMBER: ClassVar[int]
    ROLES_FIELD_NUMBER: ClassVar[int]
    ROLE_ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    principal: _principal__client_pb2.PrincipalBasic
    role_assignments: _containers.RepeatedCompositeFieldContainer[_resource_role_assignments__client_pb2.ResourceAndRoleAssignments]
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, principal: Optional[Union[_principal__client_pb2.PrincipalBasic, Mapping]] = ..., roles: Optional[Iterable[str]] = ..., role_assignments: Optional[Iterable[Union[_resource_role_assignments__client_pb2.ResourceAndRoleAssignments, Mapping]]] = ...) -> None: ...

class AssignmentBasicV2(_message.Message):
    __slots__ = ["principal", "role_assignments"]
    PRINCIPAL_FIELD_NUMBER: ClassVar[int]
    ROLE_ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    principal: _principal__client_pb2.PrincipalBasic
    role_assignments: _containers.RepeatedCompositeFieldContainer[_resource_role_assignments__client_pb2.ResourceAndRoleAssignmentsV2]
    def __init__(self, principal: Optional[Union[_principal__client_pb2.PrincipalBasic, Mapping]] = ..., role_assignments: Optional[Iterable[Union[_resource_role_assignments__client_pb2.ResourceAndRoleAssignmentsV2, Mapping]]] = ...) -> None: ...

class AuthorizedResources(_message.Message):
    __slots__ = ["actions", "resource_id"]
    ACTIONS_FIELD_NUMBER: ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    actions: _containers.RepeatedScalarFieldContainer[str]
    resource_id: str
    def __init__(self, resource_id: Optional[str] = ..., actions: Optional[Iterable[str]] = ...) -> None: ...

class GetAppPermissionsRequest(_message.Message):
    __slots__ = ["principal_id", "principal_type", "resource_type_permissions"]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_PERMISSIONS_FIELD_NUMBER: ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    resource_type_permissions: _containers.RepeatedCompositeFieldContainer[ResourceTypePermissions]
    def __init__(self, principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ..., resource_type_permissions: Optional[Iterable[Union[ResourceTypePermissions, Mapping]]] = ...) -> None: ...

class GetAppPermissionsResponse(_message.Message):
    __slots__ = ["resource_type_permission_values"]
    RESOURCE_TYPE_PERMISSION_VALUES_FIELD_NUMBER: ClassVar[int]
    resource_type_permission_values: _containers.RepeatedCompositeFieldContainer[ResourceTypePermissionValues]
    def __init__(self, resource_type_permission_values: Optional[Iterable[Union[ResourceTypePermissionValues, Mapping]]] = ...) -> None: ...

class GetAssignedPrincipalsRequest(_message.Message):
    __slots__ = ["principal_types", "resource_id", "resource_type", "roles"]
    PRINCIPAL_TYPES_FIELD_NUMBER: ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLES_FIELD_NUMBER: ClassVar[int]
    principal_types: _containers.RepeatedScalarFieldContainer[_principal__client_pb2.PrincipalType]
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: Optional[str] = ..., roles: Optional[Iterable[str]] = ..., principal_types: Optional[Iterable[Union[_principal__client_pb2.PrincipalType, str]]] = ...) -> None: ...

class GetAssignedPrincipalsResponse(_message.Message):
    __slots__ = ["assignments"]
    ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[AssignmentBasic]
    def __init__(self, assignments: Optional[Iterable[Union[AssignmentBasic, Mapping]]] = ...) -> None: ...

class GetAssignedRolesRequest(_message.Message):
    __slots__ = ["principal_id", "principal_type", "resource_ids", "resource_type", "roles"]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    RESOURCE_IDS_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLES_FIELD_NUMBER: ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    resource_ids: _containers.RepeatedScalarFieldContainer[str]
    resource_type: _resource__client_pb2.ResourceType
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ..., resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_ids: Optional[Iterable[str]] = ..., roles: Optional[Iterable[str]] = ...) -> None: ...

class GetAssignedRolesResponse(_message.Message):
    __slots__ = ["assignments"]
    ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[_resource_role_assignments__client_pb2.ResourceAndRoleAssignments]
    def __init__(self, assignments: Optional[Iterable[Union[_resource_role_assignments__client_pb2.ResourceAndRoleAssignments, Mapping]]] = ...) -> None: ...

class GetAuthorizedResourcesRequest(_message.Message):
    __slots__ = ["action", "principal_id", "principal_type", "resource_type"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    action: str
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    resource_type: _resource__client_pb2.ResourceType
    def __init__(self, principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ..., resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., action: Optional[str] = ...) -> None: ...

class GetAuthorizedResourcesResponse(_message.Message):
    __slots__ = ["authorized_resources"]
    AUTHORIZED_RESOURCES_FIELD_NUMBER: ClassVar[int]
    authorized_resources: _containers.RepeatedCompositeFieldContainer[AuthorizedResources]
    def __init__(self, authorized_resources: Optional[Iterable[Union[AuthorizedResources, Mapping]]] = ...) -> None: ...

class GetIsAuthorizedRequest(_message.Message):
    __slots__ = ["permissions", "principal_id", "principal_type"]
    PERMISSIONS_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    def __init__(self, principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ..., permissions: Optional[Iterable[Union[Permission, Mapping]]] = ...) -> None: ...

class GetIsAuthorizedResponse(_message.Message):
    __slots__ = ["permissions"]
    PERMISSIONS_FIELD_NUMBER: ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: Optional[Iterable[Union[Permission, Mapping]]] = ...) -> None: ...

class GetRolesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetRolesResponse(_message.Message):
    __slots__ = ["roles"]
    ROLES_FIELD_NUMBER: ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[RoleDefinition]
    def __init__(self, roles: Optional[Iterable[Union[RoleDefinition, Mapping]]] = ...) -> None: ...

class GetWorkspacePermissionsRequest(_message.Message):
    __slots__ = ["principal_id", "principal_type", "resource_type_permissions", "workspace_id"]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_PERMISSIONS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    resource_type_permissions: _containers.RepeatedCompositeFieldContainer[ResourceTypePermissions]
    workspace_id: str
    def __init__(self, principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ..., workspace_id: Optional[str] = ..., resource_type_permissions: Optional[Iterable[Union[ResourceTypePermissions, Mapping]]] = ...) -> None: ...

class GetWorkspacePermissionsResponse(_message.Message):
    __slots__ = ["resource_type_permission_values"]
    RESOURCE_TYPE_PERMISSION_VALUES_FIELD_NUMBER: ClassVar[int]
    resource_type_permission_values: _containers.RepeatedCompositeFieldContainer[ResourceTypePermissionValues]
    def __init__(self, resource_type_permission_values: Optional[Iterable[Union[ResourceTypePermissionValues, Mapping]]] = ...) -> None: ...

class ListAssignedPrincipalsRequest(_message.Message):
    __slots__ = ["principal_types", "resource_id", "resource_type", "roles"]
    PRINCIPAL_TYPES_FIELD_NUMBER: ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLES_FIELD_NUMBER: ClassVar[int]
    principal_types: _containers.RepeatedScalarFieldContainer[_principal__client_pb2.PrincipalType]
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: Optional[str] = ..., roles: Optional[Iterable[str]] = ..., principal_types: Optional[Iterable[Union[_principal__client_pb2.PrincipalType, str]]] = ...) -> None: ...

class ListAssignedPrincipalsResponse(_message.Message):
    __slots__ = ["assignments"]
    ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[AssignmentBasicV2]
    def __init__(self, assignments: Optional[Iterable[Union[AssignmentBasicV2, Mapping]]] = ...) -> None: ...

class ListAssignedRolesRequest(_message.Message):
    __slots__ = ["principal_id", "principal_type", "resource_ids", "resource_type", "roles"]
    PRINCIPAL_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    RESOURCE_IDS_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLES_FIELD_NUMBER: ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    resource_ids: _containers.RepeatedScalarFieldContainer[str]
    resource_type: _resource__client_pb2.ResourceType
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, principal_type: Optional[Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: Optional[str] = ..., resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_ids: Optional[Iterable[str]] = ..., roles: Optional[Iterable[str]] = ...) -> None: ...

class ListAssignedRolesResponse(_message.Message):
    __slots__ = ["assignments"]
    ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[_resource_role_assignments__client_pb2.ResourceAndRoleAssignmentsV2]
    def __init__(self, assignments: Optional[Iterable[Union[_resource_role_assignments__client_pb2.ResourceAndRoleAssignmentsV2, Mapping]]] = ...) -> None: ...

class Permission(_message.Message):
    __slots__ = ["action", "resource_id", "resource_type"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    action: str
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: Optional[str] = ..., action: Optional[str] = ...) -> None: ...

class PermissionDefinition(_message.Message):
    __slots__ = ["description", "id", "is_authorized"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IS_AUTHORIZED_FIELD_NUMBER: ClassVar[int]
    description: str
    id: str
    is_authorized: bool
    def __init__(self, id: Optional[str] = ..., description: Optional[str] = ..., is_authorized: bool = ...) -> None: ...

class PermissionValue(_message.Message):
    __slots__ = ["action", "is_authorized"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    IS_AUTHORIZED_FIELD_NUMBER: ClassVar[int]
    action: str
    is_authorized: bool
    def __init__(self, action: Optional[str] = ..., is_authorized: bool = ...) -> None: ...

class ResourceTypePermissionValues(_message.Message):
    __slots__ = ["permission_values", "resource_type"]
    PERMISSION_VALUES_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    permission_values: _containers.RepeatedCompositeFieldContainer[PermissionValue]
    resource_type: _resource__client_pb2.ResourceType
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., permission_values: Optional[Iterable[Union[PermissionValue, Mapping]]] = ...) -> None: ...

class ResourceTypePermissions(_message.Message):
    __slots__ = ["actions", "resource_type"]
    ACTIONS_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    actions: _containers.RepeatedScalarFieldContainer[str]
    resource_type: _resource__client_pb2.ResourceType
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., actions: Optional[Iterable[str]] = ...) -> None: ...

class RoleDefinition(_message.Message):
    __slots__ = ["assignable_on_resource_types", "assignable_to_principal_types", "description", "id", "legacy_id", "name", "permissions"]
    ASSIGNABLE_ON_RESOURCE_TYPES_FIELD_NUMBER: ClassVar[int]
    ASSIGNABLE_TO_PRINCIPAL_TYPES_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    LEGACY_ID_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: ClassVar[int]
    assignable_on_resource_types: _containers.RepeatedScalarFieldContainer[_resource__client_pb2.ResourceType]
    assignable_to_principal_types: _containers.RepeatedScalarFieldContainer[_principal__client_pb2.PrincipalType]
    description: str
    id: str
    legacy_id: str
    name: str
    permissions: _containers.RepeatedCompositeFieldContainer[PermissionDefinition]
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., description: Optional[str] = ..., assignable_on_resource_types: Optional[Iterable[Union[_resource__client_pb2.ResourceType, str]]] = ..., assignable_to_principal_types: Optional[Iterable[Union[_principal__client_pb2.PrincipalType, str]]] = ..., permissions: Optional[Iterable[Union[PermissionDefinition, Mapping]]] = ..., legacy_id: Optional[str] = ...) -> None: ...

class UnassignRolesRequest(_message.Message):
    __slots__ = ["assignments"]
    ASSIGNMENTS_FIELD_NUMBER: ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[Assignment]
    def __init__(self, assignments: Optional[Iterable[Union[Assignment, Mapping]]] = ...) -> None: ...

class UnassignRolesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
