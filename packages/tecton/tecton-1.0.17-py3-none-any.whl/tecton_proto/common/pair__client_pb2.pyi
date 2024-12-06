from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Pair(_message.Message):
    __slots__ = ["first", "second"]
    FIRST_FIELD_NUMBER: ClassVar[int]
    SECOND_FIELD_NUMBER: ClassVar[int]
    first: str
    second: str
    def __init__(self, first: Optional[str] = ..., second: Optional[str] = ...) -> None: ...
