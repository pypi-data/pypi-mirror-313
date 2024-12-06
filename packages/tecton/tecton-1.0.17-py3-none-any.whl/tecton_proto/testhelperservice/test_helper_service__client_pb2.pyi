from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional, Text

DESCRIPTOR: _descriptor.FileDescriptor

class IngestionServerConfigRequest(_message.Message):
    __slots__ = ["absolute_filepath"]
    ABSOLUTE_FILEPATH_FIELD_NUMBER: ClassVar[int]
    absolute_filepath: str
    def __init__(self, absolute_filepath: Optional[str] = ...) -> None: ...

class IngestionServerConfigResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class InitializeStoreRequest(_message.Message):
    __slots__ = ["feature_view_name", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class InitializeStoreResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
