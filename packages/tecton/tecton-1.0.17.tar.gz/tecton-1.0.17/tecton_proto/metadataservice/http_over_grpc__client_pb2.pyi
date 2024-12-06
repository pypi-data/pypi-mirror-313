from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor

class HttpRequest(_message.Message):
    __slots__ = ["body", "contentLength", "contentType", "method", "url"]
    BODY_FIELD_NUMBER: ClassVar[int]
    CONTENTLENGTH_FIELD_NUMBER: ClassVar[int]
    CONTENTTYPE_FIELD_NUMBER: ClassVar[int]
    METHOD_FIELD_NUMBER: ClassVar[int]
    URL_FIELD_NUMBER: ClassVar[int]
    body: bytes
    contentLength: int
    contentType: str
    method: str
    url: str
    def __init__(self, method: Optional[str] = ..., url: Optional[str] = ..., body: Optional[bytes] = ..., contentType: Optional[str] = ..., contentLength: Optional[int] = ...) -> None: ...

class HttpResponseHeaders(_message.Message):
    __slots__ = ["contentLength", "contentType", "status"]
    CONTENTLENGTH_FIELD_NUMBER: ClassVar[int]
    CONTENTTYPE_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    contentLength: int
    contentType: str
    status: int
    def __init__(self, status: Optional[int] = ..., contentType: Optional[str] = ..., contentLength: Optional[int] = ...) -> None: ...

class HttpResponsePiece(_message.Message):
    __slots__ = ["body_piece", "headers"]
    BODY_PIECE_FIELD_NUMBER: ClassVar[int]
    HEADERS_FIELD_NUMBER: ClassVar[int]
    body_piece: bytes
    headers: HttpResponseHeaders
    def __init__(self, headers: Optional[Union[HttpResponseHeaders, Mapping]] = ..., body_piece: Optional[bytes] = ...) -> None: ...
