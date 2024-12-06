from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityArgs(_message.Message):
    __slots__ = ["entity_id", "info", "join_keys", "join_keys_legacy", "options", "prevent_destroy", "version"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ENTITY_ID_FIELD_NUMBER: ClassVar[int]
    INFO_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_LEGACY_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    entity_id: _id__client_pb2.Id
    info: _basic_info__client_pb2.BasicInfo
    join_keys: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.Column]
    join_keys_legacy: _containers.RepeatedScalarFieldContainer[str]
    options: _containers.ScalarMap[str, str]
    prevent_destroy: bool
    version: _framework_version__client_pb2.FrameworkVersion
    def __init__(self, entity_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., info: Optional[Union[_basic_info__client_pb2.BasicInfo, Mapping]] = ..., version: Optional[Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., prevent_destroy: bool = ..., options: Optional[Mapping[str, str]] = ..., join_keys_legacy: Optional[Iterable[str]] = ..., join_keys: Optional[Iterable[Union[_schema__client_pb2.Column, Mapping]]] = ...) -> None: ...
