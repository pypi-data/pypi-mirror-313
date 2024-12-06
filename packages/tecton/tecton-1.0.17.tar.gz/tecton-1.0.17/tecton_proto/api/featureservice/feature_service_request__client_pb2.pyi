from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetFeaturesBatchParameters(_message.Message):
    __slots__ = ["feature_service_id", "feature_service_name", "metadata_options", "request_data", "workspace_name"]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: ClassVar[int]
    METADATA_OPTIONS_FIELD_NUMBER: ClassVar[int]
    REQUEST_DATA_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    feature_service_id: str
    feature_service_name: str
    metadata_options: MetadataOptions
    request_data: _containers.RepeatedCompositeFieldContainer[GetFeaturesBatchRequestData]
    workspace_name: str
    def __init__(self, feature_service_id: Optional[str] = ..., feature_service_name: Optional[str] = ..., workspace_name: Optional[str] = ..., request_data: Optional[Iterable[Union[GetFeaturesBatchRequestData, Mapping]]] = ..., metadata_options: Optional[Union[MetadataOptions, Mapping]] = ...) -> None: ...

class GetFeaturesBatchRequest(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: ClassVar[int]
    params: GetFeaturesBatchParameters
    def __init__(self, params: Optional[Union[GetFeaturesBatchParameters, Mapping]] = ...) -> None: ...

class GetFeaturesBatchRequestData(_message.Message):
    __slots__ = ["join_key_map", "request_context_map"]
    class JoinKeyMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[_struct_pb2.Value, Mapping]] = ...) -> None: ...
    class RequestContextMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[_struct_pb2.Value, Mapping]] = ...) -> None: ...
    JOIN_KEY_MAP_FIELD_NUMBER: ClassVar[int]
    REQUEST_CONTEXT_MAP_FIELD_NUMBER: ClassVar[int]
    join_key_map: _containers.MessageMap[str, _struct_pb2.Value]
    request_context_map: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, join_key_map: Optional[Mapping[str, _struct_pb2.Value]] = ..., request_context_map: Optional[Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class GetFeaturesParameters(_message.Message):
    __slots__ = ["allow_partial_results", "feature_package_id", "feature_package_name", "feature_service_id", "feature_service_name", "feature_view_id", "feature_view_name", "isCallerBatch", "join_key_map", "metadata_options", "request_context_map", "request_options", "workspace_name"]
    class JoinKeyMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[_struct_pb2.Value, Mapping]] = ...) -> None: ...
    class RequestContextMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[_struct_pb2.Value, Mapping]] = ...) -> None: ...
    ALLOW_PARTIAL_RESULTS_FIELD_NUMBER: ClassVar[int]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_PACKAGE_NAME_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    ISCALLERBATCH_FIELD_NUMBER: ClassVar[int]
    JOIN_KEY_MAP_FIELD_NUMBER: ClassVar[int]
    METADATA_OPTIONS_FIELD_NUMBER: ClassVar[int]
    REQUEST_CONTEXT_MAP_FIELD_NUMBER: ClassVar[int]
    REQUEST_OPTIONS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    allow_partial_results: bool
    feature_package_id: str
    feature_package_name: str
    feature_service_id: str
    feature_service_name: str
    feature_view_id: str
    feature_view_name: str
    isCallerBatch: bool
    join_key_map: _containers.MessageMap[str, _struct_pb2.Value]
    metadata_options: MetadataOptions
    request_context_map: _containers.MessageMap[str, _struct_pb2.Value]
    request_options: RequestOptions
    workspace_name: str
    def __init__(self, feature_service_id: Optional[str] = ..., feature_service_name: Optional[str] = ..., feature_package_id: Optional[str] = ..., feature_package_name: Optional[str] = ..., feature_view_id: Optional[str] = ..., feature_view_name: Optional[str] = ..., workspace_name: Optional[str] = ..., join_key_map: Optional[Mapping[str, _struct_pb2.Value]] = ..., request_context_map: Optional[Mapping[str, _struct_pb2.Value]] = ..., metadata_options: Optional[Union[MetadataOptions, Mapping]] = ..., allow_partial_results: bool = ..., request_options: Optional[Union[RequestOptions, Mapping]] = ..., isCallerBatch: bool = ...) -> None: ...

class GetFeaturesRequest(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: ClassVar[int]
    params: GetFeaturesParameters
    def __init__(self, params: Optional[Union[GetFeaturesParameters, Mapping]] = ...) -> None: ...

class MetadataOptions(_message.Message):
    __slots__ = ["include_data_types", "include_effective_times", "include_feature_descriptions", "include_feature_tags", "include_names", "include_serving_status", "include_slo_info", "include_types"]
    INCLUDE_DATA_TYPES_FIELD_NUMBER: ClassVar[int]
    INCLUDE_EFFECTIVE_TIMES_FIELD_NUMBER: ClassVar[int]
    INCLUDE_FEATURE_DESCRIPTIONS_FIELD_NUMBER: ClassVar[int]
    INCLUDE_FEATURE_TAGS_FIELD_NUMBER: ClassVar[int]
    INCLUDE_NAMES_FIELD_NUMBER: ClassVar[int]
    INCLUDE_SERVING_STATUS_FIELD_NUMBER: ClassVar[int]
    INCLUDE_SLO_INFO_FIELD_NUMBER: ClassVar[int]
    INCLUDE_TYPES_FIELD_NUMBER: ClassVar[int]
    include_data_types: bool
    include_effective_times: bool
    include_feature_descriptions: bool
    include_feature_tags: bool
    include_names: bool
    include_serving_status: bool
    include_slo_info: bool
    include_types: bool
    def __init__(self, include_names: bool = ..., include_effective_times: bool = ..., include_types: bool = ..., include_data_types: bool = ..., include_slo_info: bool = ..., include_serving_status: bool = ..., include_feature_descriptions: bool = ..., include_feature_tags: bool = ...) -> None: ...

class RequestOptions(_message.Message):
    __slots__ = ["aggregation_leading_edge", "high_watermark_override", "read_from_cache", "write_to_cache"]
    AGGREGATION_LEADING_EDGE_FIELD_NUMBER: ClassVar[int]
    HIGH_WATERMARK_OVERRIDE_FIELD_NUMBER: ClassVar[int]
    READ_FROM_CACHE_FIELD_NUMBER: ClassVar[int]
    WRITE_TO_CACHE_FIELD_NUMBER: ClassVar[int]
    aggregation_leading_edge: _feature_view__client_pb2.AggregationLeadingEdge
    high_watermark_override: _timestamp_pb2.Timestamp
    read_from_cache: bool
    write_to_cache: bool
    def __init__(self, read_from_cache: bool = ..., write_to_cache: bool = ..., aggregation_leading_edge: Optional[Union[_feature_view__client_pb2.AggregationLeadingEdge, str]] = ..., high_watermark_override: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...
