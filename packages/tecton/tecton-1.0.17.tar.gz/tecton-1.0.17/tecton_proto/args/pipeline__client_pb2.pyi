from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

CONTEXT_TYPE_MATERIALIZATION: ContextType
CONTEXT_TYPE_REALTIME: ContextType
CONTEXT_TYPE_UNSPECIFIED: ContextType
DESCRIPTOR: _descriptor.FileDescriptor
TIME_REFERENCE_MATERIALIZATION_END_TIME: TimeReference
TIME_REFERENCE_MATERIALIZATION_START_TIME: TimeReference
TIME_REFERENCE_UNBOUNDED_FUTURE: TimeReference
TIME_REFERENCE_UNBOUNDED_PAST: TimeReference
TIME_REFERENCE_UNSPECIFIED: TimeReference

class ConstantNode(_message.Message):
    __slots__ = ["bool_const", "float_const", "int_const", "null_const", "string_const"]
    BOOL_CONST_FIELD_NUMBER: ClassVar[int]
    FLOAT_CONST_FIELD_NUMBER: ClassVar[int]
    INT_CONST_FIELD_NUMBER: ClassVar[int]
    NULL_CONST_FIELD_NUMBER: ClassVar[int]
    STRING_CONST_FIELD_NUMBER: ClassVar[int]
    bool_const: bool
    float_const: str
    int_const: str
    null_const: _empty_pb2.Empty
    string_const: str
    def __init__(self, string_const: Optional[str] = ..., int_const: Optional[str] = ..., float_const: Optional[str] = ..., bool_const: bool = ..., null_const: Optional[Union[_empty_pb2.Empty, Mapping]] = ...) -> None: ...

class ContextNode(_message.Message):
    __slots__ = ["context_type", "input_name"]
    CONTEXT_TYPE_FIELD_NUMBER: ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: ClassVar[int]
    context_type: ContextType
    input_name: str
    def __init__(self, context_type: Optional[Union[ContextType, str]] = ..., input_name: Optional[str] = ...) -> None: ...

class DataSourceNode(_message.Message):
    __slots__ = ["filter_end_time", "filter_start_time", "input_name", "schedule_offset", "start_time_offset", "virtual_data_source_id", "window", "window_unbounded", "window_unbounded_preceding"]
    FILTER_END_TIME_FIELD_NUMBER: ClassVar[int]
    FILTER_START_TIME_FIELD_NUMBER: ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: ClassVar[int]
    SCHEDULE_OFFSET_FIELD_NUMBER: ClassVar[int]
    START_TIME_OFFSET_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCE_ID_FIELD_NUMBER: ClassVar[int]
    WINDOW_FIELD_NUMBER: ClassVar[int]
    WINDOW_UNBOUNDED_FIELD_NUMBER: ClassVar[int]
    WINDOW_UNBOUNDED_PRECEDING_FIELD_NUMBER: ClassVar[int]
    filter_end_time: FilterDateTime
    filter_start_time: FilterDateTime
    input_name: str
    schedule_offset: _duration_pb2.Duration
    start_time_offset: _duration_pb2.Duration
    virtual_data_source_id: _id__client_pb2.Id
    window: _duration_pb2.Duration
    window_unbounded: bool
    window_unbounded_preceding: bool
    def __init__(self, virtual_data_source_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., window: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., window_unbounded_preceding: bool = ..., window_unbounded: bool = ..., start_time_offset: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., schedule_offset: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., input_name: Optional[str] = ..., filter_start_time: Optional[Union[FilterDateTime, Mapping]] = ..., filter_end_time: Optional[Union[FilterDateTime, Mapping]] = ...) -> None: ...

class FeatureViewNode(_message.Message):
    __slots__ = ["feature_reference", "feature_view_id", "input_name"]
    FEATURE_REFERENCE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: ClassVar[int]
    feature_reference: _feature_service__client_pb2.FeatureReference
    feature_view_id: _id__client_pb2.Id
    input_name: str
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_reference: Optional[Union[_feature_service__client_pb2.FeatureReference, Mapping]] = ..., input_name: Optional[str] = ...) -> None: ...

class FilterDateTime(_message.Message):
    __slots__ = ["relative_time", "timestamp"]
    RELATIVE_TIME_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    relative_time: RelativeTime
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., relative_time: Optional[Union[RelativeTime, Mapping]] = ...) -> None: ...

class Input(_message.Message):
    __slots__ = ["arg_index", "arg_name", "node"]
    ARG_INDEX_FIELD_NUMBER: ClassVar[int]
    ARG_NAME_FIELD_NUMBER: ClassVar[int]
    NODE_FIELD_NUMBER: ClassVar[int]
    arg_index: int
    arg_name: str
    node: PipelineNode
    def __init__(self, arg_index: Optional[int] = ..., arg_name: Optional[str] = ..., node: Optional[Union[PipelineNode, Mapping]] = ...) -> None: ...

class MaterializationContextNode(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Pipeline(_message.Message):
    __slots__ = ["root"]
    ROOT_FIELD_NUMBER: ClassVar[int]
    root: PipelineNode
    def __init__(self, root: Optional[Union[PipelineNode, Mapping]] = ...) -> None: ...

class PipelineNode(_message.Message):
    __slots__ = ["constant_node", "context_node", "data_source_node", "feature_view_node", "materialization_context_node", "request_data_source_node", "transformation_node"]
    CONSTANT_NODE_FIELD_NUMBER: ClassVar[int]
    CONTEXT_NODE_FIELD_NUMBER: ClassVar[int]
    DATA_SOURCE_NODE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NODE_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_CONTEXT_NODE_FIELD_NUMBER: ClassVar[int]
    REQUEST_DATA_SOURCE_NODE_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_NODE_FIELD_NUMBER: ClassVar[int]
    constant_node: ConstantNode
    context_node: ContextNode
    data_source_node: DataSourceNode
    feature_view_node: FeatureViewNode
    materialization_context_node: MaterializationContextNode
    request_data_source_node: RequestDataSourceNode
    transformation_node: TransformationNode
    def __init__(self, transformation_node: Optional[Union[TransformationNode, Mapping]] = ..., data_source_node: Optional[Union[DataSourceNode, Mapping]] = ..., constant_node: Optional[Union[ConstantNode, Mapping]] = ..., request_data_source_node: Optional[Union[RequestDataSourceNode, Mapping]] = ..., feature_view_node: Optional[Union[FeatureViewNode, Mapping]] = ..., materialization_context_node: Optional[Union[MaterializationContextNode, Mapping]] = ..., context_node: Optional[Union[ContextNode, Mapping]] = ...) -> None: ...

class RelativeTime(_message.Message):
    __slots__ = ["offset", "time_reference"]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    TIME_REFERENCE_FIELD_NUMBER: ClassVar[int]
    offset: _duration_pb2.Duration
    time_reference: TimeReference
    def __init__(self, time_reference: Optional[Union[TimeReference, str]] = ..., offset: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class RequestContext(_message.Message):
    __slots__ = ["schema", "tecton_schema"]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TECTON_SCHEMA_FIELD_NUMBER: ClassVar[int]
    schema: _spark_schema__client_pb2.SparkSchema
    tecton_schema: _schema__client_pb2.Schema
    def __init__(self, tecton_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...

class RequestDataSourceNode(_message.Message):
    __slots__ = ["input_name", "request_context"]
    INPUT_NAME_FIELD_NUMBER: ClassVar[int]
    REQUEST_CONTEXT_FIELD_NUMBER: ClassVar[int]
    input_name: str
    request_context: RequestContext
    def __init__(self, request_context: Optional[Union[RequestContext, Mapping]] = ..., input_name: Optional[str] = ...) -> None: ...

class TransformationNode(_message.Message):
    __slots__ = ["inputs", "transformation_id"]
    INPUTS_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_ID_FIELD_NUMBER: ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[Input]
    transformation_id: _id__client_pb2.Id
    def __init__(self, transformation_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., inputs: Optional[Iterable[Union[Input, Mapping]]] = ...) -> None: ...

class TimeReference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ContextType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
