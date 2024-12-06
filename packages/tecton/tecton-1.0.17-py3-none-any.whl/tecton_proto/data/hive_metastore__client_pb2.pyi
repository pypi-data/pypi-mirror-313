from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HiveTableDataSource(_message.Message):
    __slots__ = ["database", "table"]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    database: str
    table: str
    def __init__(self, table: Optional[str] = ..., database: Optional[str] = ...) -> None: ...

class ListHiveResult(_message.Message):
    __slots__ = ["names"]
    NAMES_FIELD_NUMBER: ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: Optional[Iterable[str]] = ...) -> None: ...
