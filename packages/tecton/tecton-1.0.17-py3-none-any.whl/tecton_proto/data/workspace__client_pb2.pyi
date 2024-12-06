from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Workspace(_message.Message):
    __slots__ = ["capabilities", "created_at", "name"]
    CAPABILITIES_FIELD_NUMBER: ClassVar[int]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    capabilities: WorkspaceCapabilities
    created_at: _timestamp_pb2.Timestamp
    name: str
    def __init__(self, name: Optional[str] = ..., capabilities: Optional[Union[WorkspaceCapabilities, Mapping]] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class WorkspaceCapabilities(_message.Message):
    __slots__ = ["materializable", "offline_store_subdirectory_enabled"]
    MATERIALIZABLE_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_SUBDIRECTORY_ENABLED_FIELD_NUMBER: ClassVar[int]
    materializable: bool
    offline_store_subdirectory_enabled: bool
    def __init__(self, materializable: bool = ..., offline_store_subdirectory_enabled: bool = ...) -> None: ...
