from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class TectonDeltaMetadata(_message.Message):
    __slots__ = ["deletion_path", "feature_start_time", "ingest_path"]
    DELETION_PATH_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    INGEST_PATH_FIELD_NUMBER: ClassVar[int]
    deletion_path: str
    feature_start_time: _timestamp_pb2.Timestamp
    ingest_path: str
    def __init__(self, deletion_path: Optional[str] = ..., ingest_path: Optional[str] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...
