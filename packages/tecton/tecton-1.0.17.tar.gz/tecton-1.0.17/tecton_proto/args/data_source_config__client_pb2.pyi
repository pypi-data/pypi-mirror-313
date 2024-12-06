from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
INITIAL_STREAM_POSITION_LATEST: InitialStreamPosition
INITIAL_STREAM_POSITION_TRIM_HORIZON: InitialStreamPosition
INITIAL_STREAM_POSITION_UNSPECIFIED: InitialStreamPosition

class BatchConfig(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class StreamConfig(_message.Message):
    __slots__ = ["initial_stream_position", "watermark_delay_threshold"]
    INITIAL_STREAM_POSITION_FIELD_NUMBER: ClassVar[int]
    WATERMARK_DELAY_THRESHOLD_FIELD_NUMBER: ClassVar[int]
    initial_stream_position: InitialStreamPosition
    watermark_delay_threshold: _duration_pb2.Duration
    def __init__(self, initial_stream_position: Optional[Union[InitialStreamPosition, str]] = ..., watermark_delay_threshold: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class InitialStreamPosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
