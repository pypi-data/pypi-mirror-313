from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

AUTH_METADATA_FIELD_NUMBER: ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
RESOURCE_REF_TYPE_PRINCIPAL_GROUP_ID: ResourceRefTypeEnum
RESOURCE_REF_TYPE_SECRET_SCOPE: ResourceRefTypeEnum
RESOURCE_REF_TYPE_SERVICE_ACCOUNT_ID: ResourceRefTypeEnum
RESOURCE_REF_TYPE_UNSPECIFIED: ResourceRefTypeEnum
RESOURCE_REF_TYPE_WORKSPACE_NAME: ResourceRefTypeEnum
auth_metadata: _descriptor.FieldDescriptor

class AuthMetadata(_message.Message):
    __slots__ = ["advanced_permission_overrides", "defer_authorization_to_service", "permission", "resource_reference", "skip_authentication", "skip_authorization"]
    ADVANCED_PERMISSION_OVERRIDES_FIELD_NUMBER: ClassVar[int]
    DEFER_AUTHORIZATION_TO_SERVICE_FIELD_NUMBER: ClassVar[int]
    PERMISSION_FIELD_NUMBER: ClassVar[int]
    RESOURCE_REFERENCE_FIELD_NUMBER: ClassVar[int]
    SKIP_AUTHENTICATION_FIELD_NUMBER: ClassVar[int]
    SKIP_AUTHORIZATION_FIELD_NUMBER: ClassVar[int]
    advanced_permission_overrides: _containers.RepeatedCompositeFieldContainer[PermissionOverride]
    defer_authorization_to_service: bool
    permission: str
    resource_reference: ResourceReference
    skip_authentication: bool
    skip_authorization: bool
    def __init__(self, skip_authentication: bool = ..., skip_authorization: bool = ..., permission: Optional[str] = ..., advanced_permission_overrides: Optional[Iterable[Union[PermissionOverride, Mapping]]] = ..., resource_reference: Optional[Union[ResourceReference, Mapping]] = ..., defer_authorization_to_service: bool = ...) -> None: ...

class PermissionOverride(_message.Message):
    __slots__ = ["condition_field_path", "condition_value", "permission_override"]
    CONDITION_FIELD_PATH_FIELD_NUMBER: ClassVar[int]
    CONDITION_VALUE_FIELD_NUMBER: ClassVar[int]
    PERMISSION_OVERRIDE_FIELD_NUMBER: ClassVar[int]
    condition_field_path: str
    condition_value: str
    permission_override: str
    def __init__(self, condition_field_path: Optional[str] = ..., condition_value: Optional[str] = ..., permission_override: Optional[str] = ...) -> None: ...

class ResourceReference(_message.Message):
    __slots__ = ["path", "type"]
    PATH_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    path: str
    type: ResourceRefTypeEnum
    def __init__(self, type: Optional[Union[ResourceRefTypeEnum, str]] = ..., path: Optional[str] = ...) -> None: ...

class ResourceRefTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
