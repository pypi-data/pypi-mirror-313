from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSecretScopeRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    scope: str
    def __init__(self, scope: Optional[str] = ...) -> None: ...

class CreateSecretScopeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteSecretRequest(_message.Message):
    __slots__ = ["key", "scope"]
    KEY_FIELD_NUMBER: ClassVar[int]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    key: str
    scope: str
    def __init__(self, scope: Optional[str] = ..., key: Optional[str] = ...) -> None: ...

class DeleteSecretResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteSecretScopeRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    scope: str
    def __init__(self, scope: Optional[str] = ...) -> None: ...

class DeleteSecretScopeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSecretValueRequest(_message.Message):
    __slots__ = ["key", "scope"]
    KEY_FIELD_NUMBER: ClassVar[int]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    key: str
    scope: str
    def __init__(self, scope: Optional[str] = ..., key: Optional[str] = ...) -> None: ...

class GetSecretValueResponse(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: str
    def __init__(self, value: Optional[str] = ...) -> None: ...

class ListSecretScopesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListSecretScopesResponse(_message.Message):
    __slots__ = ["scopes"]
    SCOPES_FIELD_NUMBER: ClassVar[int]
    scopes: _containers.RepeatedCompositeFieldContainer[SecretScope]
    def __init__(self, scopes: Optional[Iterable[Union[SecretScope, Mapping]]] = ...) -> None: ...

class ListSecretsRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    scope: str
    def __init__(self, scope: Optional[str] = ...) -> None: ...

class ListSecretsResponse(_message.Message):
    __slots__ = ["keys"]
    KEYS_FIELD_NUMBER: ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[SecretKey]
    def __init__(self, keys: Optional[Iterable[Union[SecretKey, Mapping]]] = ...) -> None: ...

class PutSecretValueRequest(_message.Message):
    __slots__ = ["key", "scope", "value"]
    KEY_FIELD_NUMBER: ClassVar[int]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    key: str
    scope: str
    value: str
    def __init__(self, scope: Optional[str] = ..., key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...

class PutSecretValueResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SecretKey(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: ClassVar[int]
    name: str
    def __init__(self, name: Optional[str] = ...) -> None: ...

class SecretScope(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: ClassVar[int]
    name: str
    def __init__(self, name: Optional[str] = ...) -> None: ...
