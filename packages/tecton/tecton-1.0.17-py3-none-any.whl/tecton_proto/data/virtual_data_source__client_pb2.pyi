from tecton_proto.common import data_source_type__client_pb2 as _data_source_type__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema_container__client_pb2 as _schema_container__client_pb2
from tecton_proto.data import batch_data_source__client_pb2 as _batch_data_source__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.data import stream_data_source__client_pb2 as _stream_data_source__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class VirtualDataSource(_message.Message):
    __slots__ = ["batch_data_source", "data_source_type", "fco_metadata", "options", "schema", "stream_data_source", "validation_args", "virtual_data_source_id"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BATCH_DATA_SOURCE_FIELD_NUMBER: ClassVar[int]
    DATA_SOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    FCO_METADATA_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    STREAM_DATA_SOURCE_FIELD_NUMBER: ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCE_ID_FIELD_NUMBER: ClassVar[int]
    batch_data_source: _batch_data_source__client_pb2.BatchDataSource
    data_source_type: _data_source_type__client_pb2.DataSourceType
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    options: _containers.ScalarMap[str, str]
    schema: _schema_container__client_pb2.SchemaContainer
    stream_data_source: _stream_data_source__client_pb2.StreamDataSource
    validation_args: _validator__client_pb2.VirtualDataSourceValidationArgs
    virtual_data_source_id: _id__client_pb2.Id
    def __init__(self, virtual_data_source_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., batch_data_source: Optional[Union[_batch_data_source__client_pb2.BatchDataSource, Mapping]] = ..., stream_data_source: Optional[Union[_stream_data_source__client_pb2.StreamDataSource, Mapping]] = ..., data_source_type: Optional[Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., fco_metadata: Optional[Union[_fco_metadata__client_pb2.FcoMetadata, Mapping]] = ..., schema: Optional[Union[_schema_container__client_pb2.SchemaContainer, Mapping]] = ..., validation_args: Optional[Union[_validator__client_pb2.VirtualDataSourceValidationArgs, Mapping]] = ..., options: Optional[Mapping[str, str]] = ...) -> None: ...
