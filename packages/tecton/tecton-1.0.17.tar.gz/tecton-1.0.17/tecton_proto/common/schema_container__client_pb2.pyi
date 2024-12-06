from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchemaContainer(_message.Message):
    __slots__ = ["tecton_schema"]
    TECTON_SCHEMA_FIELD_NUMBER: ClassVar[int]
    tecton_schema: _schema__client_pb2.Schema
    def __init__(self, tecton_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ...) -> None: ...
