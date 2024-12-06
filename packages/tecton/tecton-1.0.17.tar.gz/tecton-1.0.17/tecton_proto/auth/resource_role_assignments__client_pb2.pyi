from tecton_proto.auth import resource__client_pb2 as _resource__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
ROLE_ASSIGNMENT_TYPE_DIRECT: RoleAssignmentType
ROLE_ASSIGNMENT_TYPE_FROM_PRINCIPAL_GROUP: RoleAssignmentType
ROLE_ASSIGNMENT_TYPE_UNSPECIFIED: RoleAssignmentType

class ResourceAndRoleAssignments(_message.Message):
    __slots__ = ["resource_id", "resource_type", "roles", "roles_granted"]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLES_FIELD_NUMBER: ClassVar[int]
    ROLES_GRANTED_FIELD_NUMBER: ClassVar[int]
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    roles: _containers.RepeatedScalarFieldContainer[str]
    roles_granted: _containers.RepeatedCompositeFieldContainer[RoleAssignmentSummary]
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: Optional[str] = ..., roles: Optional[Iterable[str]] = ..., roles_granted: Optional[Iterable[Union[RoleAssignmentSummary, Mapping]]] = ...) -> None: ...

class ResourceAndRoleAssignmentsV2(_message.Message):
    __slots__ = ["resource_id", "resource_type", "roles_granted"]
    RESOURCE_ID_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ROLES_GRANTED_FIELD_NUMBER: ClassVar[int]
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    roles_granted: _containers.RepeatedCompositeFieldContainer[RoleAssignmentSummary]
    def __init__(self, resource_type: Optional[Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: Optional[str] = ..., roles_granted: Optional[Iterable[Union[RoleAssignmentSummary, Mapping]]] = ...) -> None: ...

class RoleAssignmentSource(_message.Message):
    __slots__ = ["assignment_type", "principal_group_id", "principal_group_name"]
    ASSIGNMENT_TYPE_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_GROUP_ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    assignment_type: RoleAssignmentType
    principal_group_id: str
    principal_group_name: str
    def __init__(self, assignment_type: Optional[Union[RoleAssignmentType, str]] = ..., principal_group_name: Optional[str] = ..., principal_group_id: Optional[str] = ...) -> None: ...

class RoleAssignmentSummary(_message.Message):
    __slots__ = ["role", "role_assignment_sources"]
    ROLE_ASSIGNMENT_SOURCES_FIELD_NUMBER: ClassVar[int]
    ROLE_FIELD_NUMBER: ClassVar[int]
    role: str
    role_assignment_sources: _containers.RepeatedCompositeFieldContainer[RoleAssignmentSource]
    def __init__(self, role: Optional[str] = ..., role_assignment_sources: Optional[Iterable[Union[RoleAssignmentSource, Mapping]]] = ...) -> None: ...

class RoleAssignmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
