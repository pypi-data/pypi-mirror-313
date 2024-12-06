from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

CLIENT_LOG_MESSAGE_TYPE_METHOD_ENTRY: LogMessageType
CLIENT_LOG_MESSAGE_TYPE_METHOD_RETURN: LogMessageType
CLIENT_LOG_MESSAGE_TYPE_UNKNOWN: LogMessageType
DESCRIPTOR: _descriptor.FileDescriptor

class ErrorLog(_message.Message):
    __slots__ = ["cause", "message", "stacktrace"]
    CAUSE_FIELD_NUMBER: ClassVar[int]
    MESSAGE_FIELD_NUMBER: ClassVar[int]
    STACKTRACE_FIELD_NUMBER: ClassVar[int]
    cause: ErrorLog
    message: str
    stacktrace: str
    def __init__(self, message: Optional[str] = ..., stacktrace: Optional[str] = ..., cause: Optional[Union[ErrorLog, Mapping]] = ...) -> None: ...

class LoggedValue(_message.Message):
    __slots__ = ["name", "value"]
    NAME_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    name: str
    value: str
    def __init__(self, name: Optional[str] = ..., value: Optional[str] = ...) -> None: ...

class SDKMethodInvocation(_message.Message):
    __slots__ = ["class_name", "error", "execution_time", "is_local_fco", "log_level", "method_name", "params_or_return_values", "python_version", "sdk_version", "time", "trace_id", "type", "user_id", "workspace"]
    CLASS_NAME_FIELD_NUMBER: ClassVar[int]
    ERROR_FIELD_NUMBER: ClassVar[int]
    EXECUTION_TIME_FIELD_NUMBER: ClassVar[int]
    IS_LOCAL_FCO_FIELD_NUMBER: ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: ClassVar[int]
    METHOD_NAME_FIELD_NUMBER: ClassVar[int]
    PARAMS_OR_RETURN_VALUES_FIELD_NUMBER: ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    TIME_FIELD_NUMBER: ClassVar[int]
    TRACE_ID_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    USER_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    class_name: str
    error: ErrorLog
    execution_time: _duration_pb2.Duration
    is_local_fco: bool
    log_level: str
    method_name: str
    params_or_return_values: _containers.RepeatedCompositeFieldContainer[LoggedValue]
    python_version: str
    sdk_version: str
    time: _timestamp_pb2.Timestamp
    trace_id: str
    type: LogMessageType
    user_id: str
    workspace: str
    def __init__(self, time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., user_id: Optional[str] = ..., trace_id: Optional[str] = ..., log_level: Optional[str] = ..., type: Optional[Union[LogMessageType, str]] = ..., class_name: Optional[str] = ..., method_name: Optional[str] = ..., execution_time: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., params_or_return_values: Optional[Iterable[Union[LoggedValue, Mapping]]] = ..., error: Optional[Union[ErrorLog, Mapping]] = ..., workspace: Optional[str] = ..., sdk_version: Optional[str] = ..., python_version: Optional[str] = ..., is_local_fco: bool = ...) -> None: ...

class LogMessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
