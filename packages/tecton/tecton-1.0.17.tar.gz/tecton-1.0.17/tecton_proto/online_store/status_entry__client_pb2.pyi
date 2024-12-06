from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StatusEntry(_message.Message):
    __slots__ = ["anchor_time", "raw_data_end_time", "source_type"]
    ANCHOR_TIME_FIELD_NUMBER: ClassVar[int]
    RAW_DATA_END_TIME_FIELD_NUMBER: ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    anchor_time: int
    raw_data_end_time: int
    source_type: str
    def __init__(self, source_type: Optional[str] = ..., raw_data_end_time: Optional[int] = ..., anchor_time: Optional[int] = ...) -> None: ...
