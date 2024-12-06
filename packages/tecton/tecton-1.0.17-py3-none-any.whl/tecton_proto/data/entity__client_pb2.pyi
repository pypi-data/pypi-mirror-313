from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Entity(_message.Message):
    __slots__ = ["entity_id", "fco_metadata", "join_keys", "join_keys_legacy", "options", "validation_args"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ENTITY_ID_FIELD_NUMBER: ClassVar[int]
    FCO_METADATA_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_LEGACY_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: ClassVar[int]
    entity_id: _id__client_pb2.Id
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    join_keys: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.Column]
    join_keys_legacy: _containers.RepeatedScalarFieldContainer[str]
    options: _containers.ScalarMap[str, str]
    validation_args: _validator__client_pb2.EntityValidationArgs
    def __init__(self, entity_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., join_keys_legacy: Optional[Iterable[str]] = ..., fco_metadata: Optional[Union[_fco_metadata__client_pb2.FcoMetadata, Mapping]] = ..., validation_args: Optional[Union[_validator__client_pb2.EntityValidationArgs, Mapping]] = ..., options: Optional[Mapping[str, str]] = ..., join_keys: Optional[Iterable[Union[_schema__client_pb2.Column, Mapping]]] = ...) -> None: ...
