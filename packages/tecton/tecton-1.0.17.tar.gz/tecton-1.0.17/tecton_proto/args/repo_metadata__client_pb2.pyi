from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureRepoSourceInfo(_message.Message):
    __slots__ = ["source_info"]
    SOURCE_INFO_FIELD_NUMBER: ClassVar[int]
    source_info: _containers.RepeatedCompositeFieldContainer[SourceInfo]
    def __init__(self, source_info: Optional[Iterable[Union[SourceInfo, Mapping]]] = ...) -> None: ...

class SourceInfo(_message.Message):
    __slots__ = ["fco_id", "scope", "source_filename", "source_lineno"]
    FCO_ID_FIELD_NUMBER: ClassVar[int]
    SCOPE_FIELD_NUMBER: ClassVar[int]
    SOURCE_FILENAME_FIELD_NUMBER: ClassVar[int]
    SOURCE_LINENO_FIELD_NUMBER: ClassVar[int]
    fco_id: _id__client_pb2.Id
    scope: str
    source_filename: str
    source_lineno: str
    def __init__(self, fco_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., scope: Optional[str] = ..., source_lineno: Optional[str] = ..., source_filename: Optional[str] = ...) -> None: ...
