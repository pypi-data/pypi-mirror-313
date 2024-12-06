from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListSecretScopesResponse(_message.Message):
    __slots__ = ["scopes"]
    SCOPES_FIELD_NUMBER: ClassVar[int]
    scopes: _containers.RepeatedCompositeFieldContainer[SecretScopeInfo]
    def __init__(self, scopes: Optional[Iterable[Union[SecretScopeInfo, Mapping]]] = ...) -> None: ...

class PutRequest(_message.Message):
    __slots__ = ["contents", "overwrite", "path"]
    CONTENTS_FIELD_NUMBER: ClassVar[int]
    OVERWRITE_FIELD_NUMBER: ClassVar[int]
    PATH_FIELD_NUMBER: ClassVar[int]
    contents: bytes
    overwrite: bool
    path: str
    def __init__(self, path: Optional[str] = ..., contents: Optional[bytes] = ..., overwrite: bool = ...) -> None: ...

class ScopeCreateRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    scope: str
    def __init__(self, scope: Optional[str] = ...) -> None: ...

class SecretAclPutRequest(_message.Message):
    __slots__ = ["permission", "principal", "scope"]
    PERMISSION_FIELD_NUMBER: ClassVar[int]
    PRINCIPAL_FIELD_NUMBER: ClassVar[int]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    permission: str
    principal: str
    scope: str
    def __init__(self, scope: Optional[str] = ..., principal: Optional[str] = ..., permission: Optional[str] = ...) -> None: ...

class SecretPutRequest(_message.Message):
    __slots__ = ["key", "scope", "string_value"]
    KEY_FIELD_NUMBER: ClassVar[int]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: ClassVar[int]
    key: str
    scope: str
    string_value: str
    def __init__(self, scope: Optional[str] = ..., key: Optional[str] = ..., string_value: Optional[str] = ...) -> None: ...

class SecretScopeInfo(_message.Message):
    __slots__ = ["backend_type", "name"]
    BACKEND_TYPE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    backend_type: str
    name: str
    def __init__(self, name: Optional[str] = ..., backend_type: Optional[str] = ...) -> None: ...
