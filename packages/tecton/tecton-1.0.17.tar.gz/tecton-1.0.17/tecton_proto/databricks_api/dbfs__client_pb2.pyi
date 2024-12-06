from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DbfsDeleteRequest(_message.Message):
    __slots__ = ["path", "recursive"]
    PATH_FIELD_NUMBER: ClassVar[int]
    RECURSIVE_FIELD_NUMBER: ClassVar[int]
    path: str
    recursive: bool
    def __init__(self, path: Optional[str] = ..., recursive: bool = ...) -> None: ...

class DbfsGetStatusRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class DbfsReadRequest(_message.Message):
    __slots__ = ["length", "offset", "path"]
    LENGTH_FIELD_NUMBER: ClassVar[int]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    PATH_FIELD_NUMBER: ClassVar[int]
    length: int
    offset: int
    path: str
    def __init__(self, path: Optional[str] = ..., offset: Optional[int] = ..., length: Optional[int] = ...) -> None: ...

class DbfsReadResponse(_message.Message):
    __slots__ = ["bytes_read", "data"]
    BYTES_READ_FIELD_NUMBER: ClassVar[int]
    DATA_FIELD_NUMBER: ClassVar[int]
    bytes_read: int
    data: bytes
    def __init__(self, bytes_read: Optional[int] = ..., data: Optional[bytes] = ...) -> None: ...
