from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Secret(_message.Message):
    __slots__ = ["encrypted_value", "redacted_value", "value"]
    ENCRYPTED_VALUE_FIELD_NUMBER: ClassVar[int]
    REDACTED_VALUE_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    encrypted_value: str
    redacted_value: str
    value: str
    def __init__(self, value: Optional[str] = ..., redacted_value: Optional[str] = ..., encrypted_value: Optional[str] = ...) -> None: ...

class SecretReference(_message.Message):
    __slots__ = ["is_local", "key", "scope"]
    IS_LOCAL_FIELD_NUMBER: ClassVar[int]
    KEY_FIELD_NUMBER: ClassVar[int]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    is_local: bool
    key: str
    scope: str
    def __init__(self, scope: Optional[str] = ..., key: Optional[str] = ..., is_local: bool = ...) -> None: ...
