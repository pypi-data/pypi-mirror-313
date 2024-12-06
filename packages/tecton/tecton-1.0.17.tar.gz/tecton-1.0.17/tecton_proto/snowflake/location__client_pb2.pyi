from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StageLocation(_message.Message):
    __slots__ = ["namespace", "path", "stage_name"]
    NAMESPACE_FIELD_NUMBER: ClassVar[int]
    PATH_FIELD_NUMBER: ClassVar[int]
    STAGE_NAME_FIELD_NUMBER: ClassVar[int]
    namespace: str
    path: str
    stage_name: str
    def __init__(self, namespace: Optional[str] = ..., stage_name: Optional[str] = ..., path: Optional[str] = ...) -> None: ...
