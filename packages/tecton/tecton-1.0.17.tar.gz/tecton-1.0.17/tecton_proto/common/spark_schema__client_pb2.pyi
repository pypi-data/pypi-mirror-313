from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class SparkField(_message.Message):
    __slots__ = ["name", "structfield_json"]
    NAME_FIELD_NUMBER: ClassVar[int]
    STRUCTFIELD_JSON_FIELD_NUMBER: ClassVar[int]
    name: str
    structfield_json: str
    def __init__(self, name: Optional[str] = ..., structfield_json: Optional[str] = ...) -> None: ...

class SparkSchema(_message.Message):
    __slots__ = ["fields"]
    FIELDS_FIELD_NUMBER: ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[SparkField]
    def __init__(self, fields: Optional[Iterable[Union[SparkField, Mapping]]] = ...) -> None: ...
