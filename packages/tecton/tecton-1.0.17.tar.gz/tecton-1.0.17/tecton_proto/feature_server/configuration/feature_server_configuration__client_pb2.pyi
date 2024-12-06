from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import pipeline__client_pb2 as _pipeline__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.auth import acl__client_pb2 as _acl__client_pb2
from tecton_proto.common import aggregation_function__client_pb2 as _aggregation_function__client_pb2
from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import time_window__client_pb2 as _time_window__client_pb2
from tecton_proto.data import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.data import realtime_compute__client_pb2 as _realtime_compute__client_pb2
from tecton_proto.data import tecton_api_key__client_pb2 as _tecton_api_key__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DATA_TABLE_TIMESTAMP_TYPE_ATTRIBUTE: DataTableTimestampType
DATA_TABLE_TIMESTAMP_TYPE_SORT_KEY: DataTableTimestampType
DATA_TABLE_TIMESTAMP_TYPE_UNKNOWN: DataTableTimestampType
DESCRIPTOR: _descriptor.FileDescriptor
STATUS_TABLE_TIMESTAMP_CONTINUOUS_AGGREGATE: StatusTableTimestampType
STATUS_TABLE_TIMESTAMP_TYPE_ATTRIBUTE: StatusTableTimestampType
STATUS_TABLE_TIMESTAMP_TYPE_SORT_KEY: StatusTableTimestampType
STATUS_TABLE_TIMESTAMP_TYPE_UNKNOWN: StatusTableTimestampType

class CacheGroup(_message.Message):
    __slots__ = ["feature_view_ids", "join_keys", "key_jitter", "key_ttl", "name"]
    FEATURE_VIEW_IDS_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    KEY_JITTER_FIELD_NUMBER: ClassVar[int]
    KEY_TTL_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    feature_view_ids: _containers.RepeatedScalarFieldContainer[str]
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    key_jitter: _duration_pb2.Duration
    key_ttl: _duration_pb2.Duration
    name: str
    def __init__(self, name: Optional[str] = ..., join_keys: Optional[Iterable[str]] = ..., key_ttl: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., key_jitter: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., feature_view_ids: Optional[Iterable[str]] = ...) -> None: ...

class CacheParams(_message.Message):
    __slots__ = ["redis"]
    REDIS_FIELD_NUMBER: ClassVar[int]
    redis: _feature_view__client_pb2.RedisOnlineStore
    def __init__(self, redis: Optional[Union[_feature_view__client_pb2.RedisOnlineStore, Mapping]] = ...) -> None: ...

class CanaryConfig(_message.Message):
    __slots__ = ["feature_server_canary_follower_endpoint", "feature_server_canary_id", "feature_server_canary_pod_name"]
    FEATURE_SERVER_CANARY_FOLLOWER_ENDPOINT_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_CANARY_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_CANARY_POD_NAME_FIELD_NUMBER: ClassVar[int]
    feature_server_canary_follower_endpoint: str
    feature_server_canary_id: str
    feature_server_canary_pod_name: str
    def __init__(self, feature_server_canary_id: Optional[str] = ..., feature_server_canary_pod_name: Optional[str] = ..., feature_server_canary_follower_endpoint: Optional[str] = ...) -> None: ...

class Column(_message.Message):
    __slots__ = ["batch_table_feature_view_index", "data_type", "description", "feature_service_space_name", "feature_view_index", "feature_view_space_name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BATCH_TABLE_FEATURE_VIEW_INDEX_FIELD_NUMBER: ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_SPACE_NAME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_INDEX_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_SPACE_NAME_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    batch_table_feature_view_index: int
    data_type: _data_type__client_pb2.DataType
    description: str
    feature_service_space_name: str
    feature_view_index: int
    feature_view_space_name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, data_type: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ..., feature_view_space_name: Optional[str] = ..., feature_service_space_name: Optional[str] = ..., feature_view_index: Optional[int] = ..., batch_table_feature_view_index: Optional[int] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class CompactTransformation(_message.Message):
    __slots__ = ["transformation_id", "transformation_mode", "user_defined_function_id"]
    TRANSFORMATION_ID_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_MODE_FIELD_NUMBER: ClassVar[int]
    USER_DEFINED_FUNCTION_ID_FIELD_NUMBER: ClassVar[int]
    transformation_id: _id__client_pb2.Id
    transformation_mode: _transformation__client_pb2.TransformationMode
    user_defined_function_id: str
    def __init__(self, transformation_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., transformation_mode: Optional[Union[_transformation__client_pb2.TransformationMode, str]] = ..., user_defined_function_id: Optional[str] = ...) -> None: ...

class FeaturePlan(_message.Message):
    __slots__ = ["aggregation_function", "aggregation_function_params", "aggregation_leading_edge_mode", "aggregation_secondary_key", "aggregation_window", "batch_table_name", "batch_table_window_index", "cache_index", "data_table_timestamp_type", "deletionTimeWindow", "feature_set_column_hash", "feature_store_format_version", "feature_view_cache_config", "feature_view_id", "feature_view_name", "input_columns", "is_compacted_feature_view", "is_secondary_key_output", "join_keys", "online_store_params", "output_column", "refresh_status_table", "serving_ttl", "slide_period", "status_table_timestamp_type", "stream_table_name", "table_format_version", "table_name", "tiles", "time_window", "timestamp_key", "wildcard_join_keys"]
    AGGREGATION_FUNCTION_FIELD_NUMBER: ClassVar[int]
    AGGREGATION_FUNCTION_PARAMS_FIELD_NUMBER: ClassVar[int]
    AGGREGATION_LEADING_EDGE_MODE_FIELD_NUMBER: ClassVar[int]
    AGGREGATION_SECONDARY_KEY_FIELD_NUMBER: ClassVar[int]
    AGGREGATION_WINDOW_FIELD_NUMBER: ClassVar[int]
    BATCH_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    BATCH_TABLE_WINDOW_INDEX_FIELD_NUMBER: ClassVar[int]
    CACHE_INDEX_FIELD_NUMBER: ClassVar[int]
    DATA_TABLE_TIMESTAMP_TYPE_FIELD_NUMBER: ClassVar[int]
    DELETIONTIMEWINDOW_FIELD_NUMBER: ClassVar[int]
    FEATURE_SET_COLUMN_HASH_FIELD_NUMBER: ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_CACHE_CONFIG_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    INPUT_COLUMNS_FIELD_NUMBER: ClassVar[int]
    IS_COMPACTED_FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    IS_SECONDARY_KEY_OUTPUT_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_PARAMS_FIELD_NUMBER: ClassVar[int]
    OUTPUT_COLUMN_FIELD_NUMBER: ClassVar[int]
    REFRESH_STATUS_TABLE_FIELD_NUMBER: ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: ClassVar[int]
    SLIDE_PERIOD_FIELD_NUMBER: ClassVar[int]
    STATUS_TABLE_TIMESTAMP_TYPE_FIELD_NUMBER: ClassVar[int]
    STREAM_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    TABLE_FORMAT_VERSION_FIELD_NUMBER: ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    TILES_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_KEY_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    WILDCARD_JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    aggregation_function: _aggregation_function__client_pb2.AggregationFunction
    aggregation_function_params: _aggregation_function__client_pb2.AggregationFunctionParams
    aggregation_leading_edge_mode: _feature_view__client_pb2.AggregationLeadingEdge
    aggregation_secondary_key: Column
    aggregation_window: _duration_pb2.Duration
    batch_table_name: str
    batch_table_window_index: int
    cache_index: int
    data_table_timestamp_type: DataTableTimestampType
    deletionTimeWindow: int
    feature_set_column_hash: str
    feature_store_format_version: int
    feature_view_cache_config: _feature_view__client_pb2.FeatureViewCacheConfig
    feature_view_id: str
    feature_view_name: str
    input_columns: _containers.RepeatedCompositeFieldContainer[Column]
    is_compacted_feature_view: bool
    is_secondary_key_output: bool
    join_keys: _containers.RepeatedCompositeFieldContainer[Column]
    online_store_params: _feature_view__client_pb2.OnlineStoreParams
    output_column: Column
    refresh_status_table: bool
    serving_ttl: _duration_pb2.Duration
    slide_period: _duration_pb2.Duration
    status_table_timestamp_type: StatusTableTimestampType
    stream_table_name: str
    table_format_version: int
    table_name: str
    tiles: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.OnlineBatchTablePartTile]
    time_window: _time_window__client_pb2.TimeWindow
    timestamp_key: str
    wildcard_join_keys: _containers.RepeatedCompositeFieldContainer[Column]
    def __init__(self, output_column: Optional[Union[Column, Mapping]] = ..., input_columns: Optional[Iterable[Union[Column, Mapping]]] = ..., aggregation_function: Optional[Union[_aggregation_function__client_pb2.AggregationFunction, str]] = ..., aggregation_function_params: Optional[Union[_aggregation_function__client_pb2.AggregationFunctionParams, Mapping]] = ..., aggregation_window: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., join_keys: Optional[Iterable[Union[Column, Mapping]]] = ..., wildcard_join_keys: Optional[Iterable[Union[Column, Mapping]]] = ..., aggregation_secondary_key: Optional[Union[Column, Mapping]] = ..., is_secondary_key_output: bool = ..., table_name: Optional[str] = ..., data_table_timestamp_type: Optional[Union[DataTableTimestampType, str]] = ..., status_table_timestamp_type: Optional[Union[StatusTableTimestampType, str]] = ..., timestamp_key: Optional[str] = ..., slide_period: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., serving_ttl: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., refresh_status_table: bool = ..., feature_view_name: Optional[str] = ..., feature_view_id: Optional[str] = ..., feature_store_format_version: Optional[int] = ..., online_store_params: Optional[Union[_feature_view__client_pb2.OnlineStoreParams, Mapping]] = ..., deletionTimeWindow: Optional[int] = ..., time_window: Optional[Union[_time_window__client_pb2.TimeWindow, Mapping]] = ..., feature_view_cache_config: Optional[Union[_feature_view__client_pb2.FeatureViewCacheConfig, Mapping]] = ..., cache_index: Optional[int] = ..., table_format_version: Optional[int] = ..., batch_table_name: Optional[str] = ..., batch_table_window_index: Optional[int] = ..., stream_table_name: Optional[str] = ..., tiles: Optional[Iterable[Union[_schema__client_pb2.OnlineBatchTablePartTile, Mapping]]] = ..., is_compacted_feature_view: bool = ..., feature_set_column_hash: Optional[str] = ..., aggregation_leading_edge_mode: Optional[Union[_feature_view__client_pb2.AggregationLeadingEdge, str]] = ...) -> None: ...

class FeatureServerConfiguration(_message.Message):
    __slots__ = ["all_online_compute_configs", "all_online_store_params", "authorized_api_keys", "cache_groups", "computed_time", "feature_server_canary_config", "feature_service_acls", "feature_services", "global_table_config_by_name", "jwks", "remote_compute_configs", "user_defined_function_map", "workspace_acls"]
    class CacheGroupsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: CacheGroup
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[CacheGroup, Mapping]] = ...) -> None: ...
    class GlobalTableConfigByNameEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: GlobalTableConfig
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[GlobalTableConfig, Mapping]] = ...) -> None: ...
    class JwksEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: Jwk
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[Jwk, Mapping]] = ...) -> None: ...
    class UserDefinedFunctionMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: _user_defined_function__client_pb2.UserDefinedFunction
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ...) -> None: ...
    ALL_ONLINE_COMPUTE_CONFIGS_FIELD_NUMBER: ClassVar[int]
    ALL_ONLINE_STORE_PARAMS_FIELD_NUMBER: ClassVar[int]
    AUTHORIZED_API_KEYS_FIELD_NUMBER: ClassVar[int]
    CACHE_GROUPS_FIELD_NUMBER: ClassVar[int]
    COMPUTED_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_CANARY_CONFIG_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICES_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ACLS_FIELD_NUMBER: ClassVar[int]
    GLOBAL_TABLE_CONFIG_BY_NAME_FIELD_NUMBER: ClassVar[int]
    JWKS_FIELD_NUMBER: ClassVar[int]
    REMOTE_COMPUTE_CONFIGS_FIELD_NUMBER: ClassVar[int]
    USER_DEFINED_FUNCTION_MAP_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_ACLS_FIELD_NUMBER: ClassVar[int]
    all_online_compute_configs: _containers.RepeatedCompositeFieldContainer[_realtime_compute__client_pb2.OnlineComputeConfig]
    all_online_store_params: _containers.RepeatedCompositeFieldContainer[_feature_view__client_pb2.OnlineStoreParams]
    authorized_api_keys: _containers.RepeatedCompositeFieldContainer[_tecton_api_key__client_pb2.TectonApiKey]
    cache_groups: _containers.MessageMap[str, CacheGroup]
    computed_time: _timestamp_pb2.Timestamp
    feature_server_canary_config: CanaryConfig
    feature_service_acls: _containers.RepeatedCompositeFieldContainer[FeatureServiceAcls]
    feature_services: _containers.RepeatedCompositeFieldContainer[FeatureServicePlan]
    global_table_config_by_name: _containers.MessageMap[str, GlobalTableConfig]
    jwks: _containers.MessageMap[str, Jwk]
    remote_compute_configs: _containers.RepeatedCompositeFieldContainer[_realtime_compute__client_pb2.RemoteFunctionComputeConfig]
    user_defined_function_map: _containers.MessageMap[str, _user_defined_function__client_pb2.UserDefinedFunction]
    workspace_acls: _containers.RepeatedCompositeFieldContainer[WorkspaceAcls]
    def __init__(self, computed_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_services: Optional[Iterable[Union[FeatureServicePlan, Mapping]]] = ..., global_table_config_by_name: Optional[Mapping[str, GlobalTableConfig]] = ..., authorized_api_keys: Optional[Iterable[Union[_tecton_api_key__client_pb2.TectonApiKey, Mapping]]] = ..., feature_service_acls: Optional[Iterable[Union[FeatureServiceAcls, Mapping]]] = ..., workspace_acls: Optional[Iterable[Union[WorkspaceAcls, Mapping]]] = ..., all_online_store_params: Optional[Iterable[Union[_feature_view__client_pb2.OnlineStoreParams, Mapping]]] = ..., feature_server_canary_config: Optional[Union[CanaryConfig, Mapping]] = ..., remote_compute_configs: Optional[Iterable[Union[_realtime_compute__client_pb2.RemoteFunctionComputeConfig, Mapping]]] = ..., all_online_compute_configs: Optional[Iterable[Union[_realtime_compute__client_pb2.OnlineComputeConfig, Mapping]]] = ..., cache_groups: Optional[Mapping[str, CacheGroup]] = ..., user_defined_function_map: Optional[Mapping[str, _user_defined_function__client_pb2.UserDefinedFunction]] = ..., jwks: Optional[Mapping[str, Jwk]] = ...) -> None: ...

class FeatureServiceAcls(_message.Message):
    __slots__ = ["acls", "feature_service_id"]
    ACLS_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    acls: _containers.RepeatedCompositeFieldContainer[_acl__client_pb2.Acl]
    feature_service_id: _id__client_pb2.Id
    def __init__(self, feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., acls: Optional[Iterable[Union[_acl__client_pb2.Acl, Mapping]]] = ...) -> None: ...

class FeatureServiceCachePlan(_message.Message):
    __slots__ = ["cache_group_name", "feature_set_column_hashes", "feature_view_ids", "remapped_join_key_lists"]
    CACHE_GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    FEATURE_SET_COLUMN_HASHES_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_IDS_FIELD_NUMBER: ClassVar[int]
    REMAPPED_JOIN_KEY_LISTS_FIELD_NUMBER: ClassVar[int]
    cache_group_name: str
    feature_set_column_hashes: _containers.RepeatedScalarFieldContainer[str]
    feature_view_ids: _containers.RepeatedScalarFieldContainer[str]
    remapped_join_key_lists: _containers.RepeatedCompositeFieldContainer[RemappedJoinKeys]
    def __init__(self, feature_view_ids: Optional[Iterable[str]] = ..., cache_group_name: Optional[str] = ..., remapped_join_key_lists: Optional[Iterable[Union[RemappedJoinKeys, Mapping]]] = ..., feature_set_column_hashes: Optional[Iterable[str]] = ...) -> None: ...

class FeatureServicePlan(_message.Message):
    __slots__ = ["cache_plans", "feature_service_id", "feature_service_name", "feature_view_id", "feature_view_name", "features_plans", "join_key_template", "logging_config", "realtime_environment", "workspace_name", "workspace_state_id"]
    CACHE_PLANS_FIELD_NUMBER: ClassVar[int]
    FEATURES_PLANS_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    JOIN_KEY_TEMPLATE_FIELD_NUMBER: ClassVar[int]
    LOGGING_CONFIG_FIELD_NUMBER: ClassVar[int]
    REALTIME_ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    cache_plans: _containers.RepeatedCompositeFieldContainer[FeatureServiceCachePlan]
    feature_service_id: _id__client_pb2.Id
    feature_service_name: str
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    features_plans: _containers.RepeatedCompositeFieldContainer[FeaturesPlan]
    join_key_template: _feature_service__client_pb2.JoinKeyTemplate
    logging_config: LoggingConfig
    realtime_environment: _realtime_compute__client_pb2.OnlineComputeConfig
    workspace_name: str
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_service_name: Optional[str] = ..., feature_view_name: Optional[str] = ..., workspace_name: Optional[str] = ..., workspace_state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., features_plans: Optional[Iterable[Union[FeaturesPlan, Mapping]]] = ..., join_key_template: Optional[Union[_feature_service__client_pb2.JoinKeyTemplate, Mapping]] = ..., logging_config: Optional[Union[LoggingConfig, Mapping]] = ..., realtime_environment: Optional[Union[_realtime_compute__client_pb2.OnlineComputeConfig, Mapping]] = ..., cache_plans: Optional[Iterable[Union[FeatureServiceCachePlan, Mapping]]] = ...) -> None: ...

class FeatureVectorPlan(_message.Message):
    __slots__ = ["features"]
    FEATURES_FIELD_NUMBER: ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeaturePlan]
    def __init__(self, features: Optional[Iterable[Union[FeaturePlan, Mapping]]] = ...) -> None: ...

class FeaturesPlan(_message.Message):
    __slots__ = ["feature_plan", "realtime_features_plan"]
    FEATURE_PLAN_FIELD_NUMBER: ClassVar[int]
    REALTIME_FEATURES_PLAN_FIELD_NUMBER: ClassVar[int]
    feature_plan: FeaturePlan
    realtime_features_plan: RealtimeFeaturesPlan
    def __init__(self, feature_plan: Optional[Union[FeaturePlan, Mapping]] = ..., realtime_features_plan: Optional[Union[RealtimeFeaturesPlan, Mapping]] = ...) -> None: ...

class GlobalTableConfig(_message.Message):
    __slots__ = ["feature_data_water_mark", "feature_store_format_version", "feature_view_id", "feature_view_name", "online_store_params", "refresh_status_table", "slide_period", "status_table_timestamp_type", "table_format_version", "workspace_name"]
    FEATURE_DATA_WATER_MARK_FIELD_NUMBER: ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_PARAMS_FIELD_NUMBER: ClassVar[int]
    REFRESH_STATUS_TABLE_FIELD_NUMBER: ClassVar[int]
    SLIDE_PERIOD_FIELD_NUMBER: ClassVar[int]
    STATUS_TABLE_TIMESTAMP_TYPE_FIELD_NUMBER: ClassVar[int]
    TABLE_FORMAT_VERSION_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    feature_data_water_mark: _timestamp_pb2.Timestamp
    feature_store_format_version: int
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    online_store_params: _feature_view__client_pb2.OnlineStoreParams
    refresh_status_table: bool
    slide_period: _duration_pb2.Duration
    status_table_timestamp_type: StatusTableTimestampType
    table_format_version: int
    workspace_name: str
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_view_name: Optional[str] = ..., workspace_name: Optional[str] = ..., slide_period: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., status_table_timestamp_type: Optional[Union[StatusTableTimestampType, str]] = ..., refresh_status_table: bool = ..., feature_store_format_version: Optional[int] = ..., online_store_params: Optional[Union[_feature_view__client_pb2.OnlineStoreParams, Mapping]] = ..., table_format_version: Optional[int] = ..., feature_data_water_mark: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class Jwk(_message.Message):
    __slots__ = ["alg", "n", "use"]
    ALG_FIELD_NUMBER: ClassVar[int]
    N_FIELD_NUMBER: ClassVar[int]
    USE_FIELD_NUMBER: ClassVar[int]
    alg: str
    n: str
    use: str
    def __init__(self, n: Optional[str] = ..., alg: Optional[str] = ..., use: Optional[str] = ...) -> None: ...

class LoggingConfig(_message.Message):
    __slots__ = ["avro_schema", "log_effective_times", "sample_rate"]
    AVRO_SCHEMA_FIELD_NUMBER: ClassVar[int]
    LOG_EFFECTIVE_TIMES_FIELD_NUMBER: ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: ClassVar[int]
    avro_schema: str
    log_effective_times: bool
    sample_rate: float
    def __init__(self, sample_rate: Optional[float] = ..., log_effective_times: bool = ..., avro_schema: Optional[str] = ...) -> None: ...

class RealtimeFeaturesPlan(_message.Message):
    __slots__ = ["args_from_request_context", "compact_transformations", "description", "feature_set_inputs", "feature_view_id", "feature_view_name", "outputs", "pipeline", "tags", "transformations"]
    class FeatureSetInputsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: FeatureVectorPlan
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[FeatureVectorPlan, Mapping]] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ARGS_FROM_REQUEST_CONTEXT_FIELD_NUMBER: ClassVar[int]
    COMPACT_TRANSFORMATIONS_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    FEATURE_SET_INPUTS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    OUTPUTS_FIELD_NUMBER: ClassVar[int]
    PIPELINE_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: ClassVar[int]
    args_from_request_context: _containers.RepeatedCompositeFieldContainer[Column]
    compact_transformations: _containers.RepeatedCompositeFieldContainer[CompactTransformation]
    description: str
    feature_set_inputs: _containers.MessageMap[str, FeatureVectorPlan]
    feature_view_id: str
    feature_view_name: str
    outputs: _containers.RepeatedCompositeFieldContainer[Column]
    pipeline: _pipeline__client_pb2.Pipeline
    tags: _containers.ScalarMap[str, str]
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    def __init__(self, args_from_request_context: Optional[Iterable[Union[Column, Mapping]]] = ..., outputs: Optional[Iterable[Union[Column, Mapping]]] = ..., feature_set_inputs: Optional[Mapping[str, FeatureVectorPlan]] = ..., pipeline: Optional[Union[_pipeline__client_pb2.Pipeline, Mapping]] = ..., transformations: Optional[Iterable[Union[_transformation__client_pb2.Transformation, Mapping]]] = ..., feature_view_name: Optional[str] = ..., feature_view_id: Optional[str] = ..., compact_transformations: Optional[Iterable[Union[CompactTransformation, Mapping]]] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class RemappedJoinKeys(_message.Message):
    __slots__ = ["join_keys"]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, join_keys: Optional[Iterable[str]] = ...) -> None: ...

class WorkspaceAcls(_message.Message):
    __slots__ = ["acls", "workspace_name"]
    ACLS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    acls: _containers.RepeatedCompositeFieldContainer[_acl__client_pb2.Acl]
    workspace_name: str
    def __init__(self, workspace_name: Optional[str] = ..., acls: Optional[Iterable[Union[_acl__client_pb2.Acl, Mapping]]] = ...) -> None: ...

class DataTableTimestampType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class StatusTableTimestampType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
