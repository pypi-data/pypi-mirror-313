from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorResponse(_message.Message):
    __slots__ = ["error", "error_code", "message"]
    ERROR_CODE_FIELD_NUMBER: ClassVar[int]
    ERROR_FIELD_NUMBER: ClassVar[int]
    MESSAGE_FIELD_NUMBER: ClassVar[int]
    error: str
    error_code: str
    message: str
    def __init__(self, error_code: Optional[str] = ..., message: Optional[str] = ..., error: Optional[str] = ...) -> None: ...
