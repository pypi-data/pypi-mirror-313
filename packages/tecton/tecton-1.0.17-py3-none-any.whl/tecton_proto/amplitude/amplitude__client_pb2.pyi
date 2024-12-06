from google.protobuf import duration_pb2 as _duration_pb2
from tecton_proto.amplitude import client_logging__client_pb2 as _client_logging__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AmplitudeEvent(_message.Message):
    __slots__ = ["device_id", "event_properties", "event_type", "os_name", "os_version", "platform", "session_id", "timestamp", "user_id"]
    DEVICE_ID_FIELD_NUMBER: ClassVar[int]
    EVENT_PROPERTIES_FIELD_NUMBER: ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: ClassVar[int]
    OS_NAME_FIELD_NUMBER: ClassVar[int]
    OS_VERSION_FIELD_NUMBER: ClassVar[int]
    PLATFORM_FIELD_NUMBER: ClassVar[int]
    SESSION_ID_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    USER_ID_FIELD_NUMBER: ClassVar[int]
    device_id: str
    event_properties: AmplitudeEventProperties
    event_type: str
    os_name: str
    os_version: str
    platform: str
    session_id: int
    timestamp: int
    user_id: str
    def __init__(self, user_id: Optional[str] = ..., device_id: Optional[str] = ..., event_type: Optional[str] = ..., platform: Optional[str] = ..., session_id: Optional[int] = ..., timestamp: Optional[int] = ..., os_name: Optional[str] = ..., os_version: Optional[str] = ..., event_properties: Optional[Union[AmplitudeEventProperties, Mapping]] = ...) -> None: ...

class AmplitudeEventProperties(_message.Message):
    __slots__ = ["caller_identity", "cluster_name", "error_message", "execution_time", "json_out", "num_fcos_changed", "num_total_fcos", "num_v3_fcos", "num_v5_fcos", "num_warnings", "params", "python_version", "sdk_method_invocation", "sdk_version", "status", "success", "suppress_recreates", "workspace"]
    class ParamsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    CALLER_IDENTITY_FIELD_NUMBER: ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: ClassVar[int]
    EXECUTION_TIME_FIELD_NUMBER: ClassVar[int]
    JSON_OUT_FIELD_NUMBER: ClassVar[int]
    NUM_FCOS_CHANGED_FIELD_NUMBER: ClassVar[int]
    NUM_TOTAL_FCOS_FIELD_NUMBER: ClassVar[int]
    NUM_V3_FCOS_FIELD_NUMBER: ClassVar[int]
    NUM_V5_FCOS_FIELD_NUMBER: ClassVar[int]
    NUM_WARNINGS_FIELD_NUMBER: ClassVar[int]
    PARAMS_FIELD_NUMBER: ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: ClassVar[int]
    SDK_METHOD_INVOCATION_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    SUCCESS_FIELD_NUMBER: ClassVar[int]
    SUPPRESS_RECREATES_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    caller_identity: CallerIdentity
    cluster_name: str
    error_message: str
    execution_time: _duration_pb2.Duration
    json_out: bool
    num_fcos_changed: int
    num_total_fcos: int
    num_v3_fcos: int
    num_v5_fcos: int
    num_warnings: int
    params: _containers.ScalarMap[str, str]
    python_version: str
    sdk_method_invocation: _client_logging__client_pb2.SDKMethodInvocation
    sdk_version: str
    status: str
    success: bool
    suppress_recreates: bool
    workspace: str
    def __init__(self, cluster_name: Optional[str] = ..., workspace: Optional[str] = ..., sdk_version: Optional[str] = ..., python_version: Optional[str] = ..., execution_time: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., num_total_fcos: Optional[int] = ..., num_fcos_changed: Optional[int] = ..., num_v3_fcos: Optional[int] = ..., num_v5_fcos: Optional[int] = ..., suppress_recreates: bool = ..., json_out: bool = ..., success: bool = ..., error_message: Optional[str] = ..., num_warnings: Optional[int] = ..., params: Optional[Mapping[str, str]] = ..., sdk_method_invocation: Optional[Union[_client_logging__client_pb2.SDKMethodInvocation, Mapping]] = ..., status: Optional[str] = ..., caller_identity: Optional[Union[CallerIdentity, Mapping]] = ...) -> None: ...

class CallerIdentity(_message.Message):
    __slots__ = ["id", "identity_type", "name"]
    IDENTITY_TYPE_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    id: str
    identity_type: str
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., identity_type: Optional[str] = ...) -> None: ...

class UploadRequest(_message.Message):
    __slots__ = ["api_key", "events"]
    API_KEY_FIELD_NUMBER: ClassVar[int]
    EVENTS_FIELD_NUMBER: ClassVar[int]
    api_key: str
    events: _containers.RepeatedCompositeFieldContainer[AmplitudeEvent]
    def __init__(self, api_key: Optional[str] = ..., events: Optional[Iterable[Union[AmplitudeEvent, Mapping]]] = ...) -> None: ...

class UploadResponse(_message.Message):
    __slots__ = ["code", "error", "events_ingested", "missing_field", "payload_size_bytes", "server_upload_time"]
    CODE_FIELD_NUMBER: ClassVar[int]
    ERROR_FIELD_NUMBER: ClassVar[int]
    EVENTS_INGESTED_FIELD_NUMBER: ClassVar[int]
    MISSING_FIELD_FIELD_NUMBER: ClassVar[int]
    PAYLOAD_SIZE_BYTES_FIELD_NUMBER: ClassVar[int]
    SERVER_UPLOAD_TIME_FIELD_NUMBER: ClassVar[int]
    code: int
    error: str
    events_ingested: int
    missing_field: str
    payload_size_bytes: int
    server_upload_time: int
    def __init__(self, code: Optional[int] = ..., events_ingested: Optional[int] = ..., payload_size_bytes: Optional[int] = ..., server_upload_time: Optional[int] = ..., error: Optional[str] = ..., missing_field: Optional[str] = ...) -> None: ...
