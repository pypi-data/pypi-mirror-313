from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class LifetimeWindow(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RelativeTimeWindow(_message.Message):
    __slots__ = ["window_end", "window_start"]
    WINDOW_END_FIELD_NUMBER: ClassVar[int]
    WINDOW_START_FIELD_NUMBER: ClassVar[int]
    window_end: _duration_pb2.Duration
    window_start: _duration_pb2.Duration
    def __init__(self, window_start: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., window_end: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class TimeWindow(_message.Message):
    __slots__ = ["lifetime_window", "relative_time_window", "time_window_series"]
    LIFETIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    RELATIVE_TIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_SERIES_FIELD_NUMBER: ClassVar[int]
    lifetime_window: LifetimeWindow
    relative_time_window: RelativeTimeWindow
    time_window_series: TimeWindowSeries
    def __init__(self, relative_time_window: Optional[Union[RelativeTimeWindow, Mapping]] = ..., lifetime_window: Optional[Union[LifetimeWindow, Mapping]] = ..., time_window_series: Optional[Union[TimeWindowSeries, Mapping]] = ...) -> None: ...

class TimeWindowSeries(_message.Message):
    __slots__ = ["time_windows"]
    TIME_WINDOWS_FIELD_NUMBER: ClassVar[int]
    time_windows: _containers.RepeatedCompositeFieldContainer[RelativeTimeWindow]
    def __init__(self, time_windows: Optional[Iterable[Union[RelativeTimeWindow, Mapping]]] = ...) -> None: ...
