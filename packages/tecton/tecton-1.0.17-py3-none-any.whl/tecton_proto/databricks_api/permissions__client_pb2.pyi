from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccessControlListResponse(_message.Message):
    __slots__ = ["all_permissions", "display_name", "group_name", "service_principal_name", "user_name"]
    ALL_PERMISSIONS_FIELD_NUMBER: ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    SERVICE_PRINCIPAL_NAME_FIELD_NUMBER: ClassVar[int]
    USER_NAME_FIELD_NUMBER: ClassVar[int]
    all_permissions: _containers.RepeatedCompositeFieldContainer[PermissionObject]
    display_name: str
    group_name: str
    service_principal_name: str
    user_name: str
    def __init__(self, user_name: Optional[str] = ..., group_name: Optional[str] = ..., service_principal_name: Optional[str] = ..., display_name: Optional[str] = ..., all_permissions: Optional[Iterable[Union[PermissionObject, Mapping]]] = ...) -> None: ...

class GroupPermissionsObject(_message.Message):
    __slots__ = ["group_name", "permission_level", "service_principal_name", "user_name"]
    GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    PERMISSION_LEVEL_FIELD_NUMBER: ClassVar[int]
    SERVICE_PRINCIPAL_NAME_FIELD_NUMBER: ClassVar[int]
    USER_NAME_FIELD_NUMBER: ClassVar[int]
    group_name: str
    permission_level: str
    service_principal_name: str
    user_name: str
    def __init__(self, group_name: Optional[str] = ..., permission_level: Optional[str] = ..., user_name: Optional[str] = ..., service_principal_name: Optional[str] = ...) -> None: ...

class PermissionObject(_message.Message):
    __slots__ = ["inherited", "inherited_from_object", "permission_level"]
    INHERITED_FIELD_NUMBER: ClassVar[int]
    INHERITED_FROM_OBJECT_FIELD_NUMBER: ClassVar[int]
    PERMISSION_LEVEL_FIELD_NUMBER: ClassVar[int]
    inherited: bool
    inherited_from_object: _containers.RepeatedScalarFieldContainer[str]
    permission_level: str
    def __init__(self, permission_level: Optional[str] = ..., inherited: bool = ..., inherited_from_object: Optional[Iterable[str]] = ...) -> None: ...

class PermissionsRequest(_message.Message):
    __slots__ = ["access_control_list"]
    ACCESS_CONTROL_LIST_FIELD_NUMBER: ClassVar[int]
    access_control_list: _containers.RepeatedCompositeFieldContainer[GroupPermissionsObject]
    def __init__(self, access_control_list: Optional[Iterable[Union[GroupPermissionsObject, Mapping]]] = ...) -> None: ...

class PermissionsResponse(_message.Message):
    __slots__ = ["access_control_list", "object_id", "object_type"]
    ACCESS_CONTROL_LIST_FIELD_NUMBER: ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: ClassVar[int]
    access_control_list: _containers.RepeatedCompositeFieldContainer[AccessControlListResponse]
    object_id: str
    object_type: str
    def __init__(self, object_id: Optional[str] = ..., object_type: Optional[str] = ..., access_control_list: Optional[Iterable[Union[AccessControlListResponse, Mapping]]] = ...) -> None: ...
