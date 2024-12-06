from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
PRINCIPAL_TYPE_GROUP: PrincipalType
PRINCIPAL_TYPE_SERVICE_ACCOUNT: PrincipalType
PRINCIPAL_TYPE_UNSPECIFIED: PrincipalType
PRINCIPAL_TYPE_USER: PrincipalType
PRINCIPAL_TYPE_WORKSPACE: PrincipalType

class GroupBasic(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    id: str
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ...) -> None: ...

class Principal(_message.Message):
    __slots__ = ["id", "principal_type"]
    ID_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: ClassVar[int]
    id: str
    principal_type: PrincipalType
    def __init__(self, principal_type: Optional[Union[PrincipalType, str]] = ..., id: Optional[str] = ...) -> None: ...

class PrincipalBasic(_message.Message):
    __slots__ = ["group", "service_account", "user", "workspace"]
    GROUP_FIELD_NUMBER: ClassVar[int]
    SERVICE_ACCOUNT_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    group: GroupBasic
    service_account: ServiceAccountBasic
    user: UserBasic
    workspace: WorkspaceBasic
    def __init__(self, user: Optional[Union[UserBasic, Mapping]] = ..., service_account: Optional[Union[ServiceAccountBasic, Mapping]] = ..., group: Optional[Union[GroupBasic, Mapping]] = ..., workspace: Optional[Union[WorkspaceBasic, Mapping]] = ...) -> None: ...

class ServiceAccountBasic(_message.Message):
    __slots__ = ["creator", "description", "id", "is_active", "name", "owner"]
    CREATOR_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    OWNER_FIELD_NUMBER: ClassVar[int]
    creator: Principal
    description: str
    id: str
    is_active: bool
    name: str
    owner: PrincipalBasic
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., description: Optional[str] = ..., is_active: bool = ..., creator: Optional[Union[Principal, Mapping]] = ..., owner: Optional[Union[PrincipalBasic, Mapping]] = ...) -> None: ...

class UserBasic(_message.Message):
    __slots__ = ["first_name", "last_name", "login_email", "okta_id"]
    FIRST_NAME_FIELD_NUMBER: ClassVar[int]
    LAST_NAME_FIELD_NUMBER: ClassVar[int]
    LOGIN_EMAIL_FIELD_NUMBER: ClassVar[int]
    OKTA_ID_FIELD_NUMBER: ClassVar[int]
    first_name: str
    last_name: str
    login_email: str
    okta_id: str
    def __init__(self, okta_id: Optional[str] = ..., first_name: Optional[str] = ..., last_name: Optional[str] = ..., login_email: Optional[str] = ...) -> None: ...

class WorkspaceBasic(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: ClassVar[int]
    name: str
    def __init__(self, name: Optional[str] = ...) -> None: ...

class PrincipalType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
