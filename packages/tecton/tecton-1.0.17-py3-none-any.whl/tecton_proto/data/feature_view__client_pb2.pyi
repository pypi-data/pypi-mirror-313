from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import pipeline__client_pb2 as _pipeline__client_pb2
from tecton_proto.common import aggregation_function__client_pb2 as _aggregation_function__client_pb2
from tecton_proto.common import compute_mode__client_pb2 as _compute_mode__client_pb2
from tecton_proto.common import data_source_type__client_pb2 as _data_source_type__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import time_window__client_pb2 as _time_window__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.data import fv_materialization__client_pb2 as _fv_materialization__client_pb2
from tecton_proto.data import realtime_compute__client_pb2 as _realtime_compute__client_pb2
from tecton_proto.modelartifactservice import model_artifact_service__client_pb2 as _model_artifact_service__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DELTA_OFFLINE_STORE_VERSION_1: DeltaOfflineStoreVersion
DELTA_OFFLINE_STORE_VERSION_2: DeltaOfflineStoreVersion
DELTA_OFFLINE_STORE_VERSION_UNSPECIFIED: DeltaOfflineStoreVersion
DESCRIPTOR: _descriptor.FileDescriptor
MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE: MaterializationTimeRangePolicy
MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE: MaterializationTimeRangePolicy
MATERIALIZATION_TIME_RANGE_POLICY_UNSPECIFIED: MaterializationTimeRangePolicy
PARQUET_OFFLINE_STORE_VERSION_1: ParquetOfflineStoreVersion
PARQUET_OFFLINE_STORE_VERSION_2: ParquetOfflineStoreVersion
PARQUET_OFFLINE_STORE_VERSION_UNSPECIFIED: ParquetOfflineStoreVersion

class Aggregate(_message.Message):
    __slots__ = ["batch_sawtooth_tile_size", "description", "function", "function_params", "input_feature_name", "output_feature_name", "tags", "time_window", "window"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BATCH_SAWTOOTH_TILE_SIZE_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    FUNCTION_FIELD_NUMBER: ClassVar[int]
    FUNCTION_PARAMS_FIELD_NUMBER: ClassVar[int]
    INPUT_FEATURE_NAME_FIELD_NUMBER: ClassVar[int]
    OUTPUT_FEATURE_NAME_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    WINDOW_FIELD_NUMBER: ClassVar[int]
    batch_sawtooth_tile_size: _duration_pb2.Duration
    description: str
    function: _aggregation_function__client_pb2.AggregationFunction
    function_params: _aggregation_function__client_pb2.AggregationFunctionParams
    input_feature_name: str
    output_feature_name: str
    tags: _containers.ScalarMap[str, str]
    time_window: _time_window__client_pb2.TimeWindow
    window: _duration_pb2.Duration
    def __init__(self, input_feature_name: Optional[str] = ..., output_feature_name: Optional[str] = ..., function: Optional[Union[_aggregation_function__client_pb2.AggregationFunction, str]] = ..., function_params: Optional[Union[_aggregation_function__client_pb2.AggregationFunctionParams, Mapping]] = ..., window: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., time_window: Optional[Union[_time_window__client_pb2.TimeWindow, Mapping]] = ..., batch_sawtooth_tile_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class Attribute(_message.Message):
    __slots__ = ["column", "description", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COLUMN_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    column: _schema__client_pb2.Field
    description: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, column: Optional[Union[_schema__client_pb2.Field, Mapping]] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class BigtableOnlineStore(_message.Message):
    __slots__ = ["enabled", "instance_id", "project_id"]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: ClassVar[int]
    enabled: bool
    instance_id: str
    project_id: str
    def __init__(self, enabled: bool = ..., project_id: Optional[str] = ..., instance_id: Optional[str] = ...) -> None: ...

class DataQualityConfig(_message.Message):
    __slots__ = ["data_quality_enabled", "skip_default_expectations"]
    DATA_QUALITY_ENABLED_FIELD_NUMBER: ClassVar[int]
    SKIP_DEFAULT_EXPECTATIONS_FIELD_NUMBER: ClassVar[int]
    data_quality_enabled: bool
    skip_default_expectations: bool
    def __init__(self, data_quality_enabled: bool = ..., skip_default_expectations: bool = ...) -> None: ...

class DeltaOfflineStoreParams(_message.Message):
    __slots__ = ["time_partition_size", "version"]
    TIME_PARTITION_SIZE_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    time_partition_size: _duration_pb2.Duration
    version: DeltaOfflineStoreVersion
    def __init__(self, time_partition_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., version: Optional[Union[DeltaOfflineStoreVersion, str]] = ...) -> None: ...

class DynamoDbOnlineStore(_message.Message):
    __slots__ = ["cross_account_external_id", "cross_account_intermediate_role_arn", "cross_account_role_arn", "dbfs_credentials_path", "enabled"]
    CROSS_ACCOUNT_EXTERNAL_ID_FIELD_NUMBER: ClassVar[int]
    CROSS_ACCOUNT_INTERMEDIATE_ROLE_ARN_FIELD_NUMBER: ClassVar[int]
    CROSS_ACCOUNT_ROLE_ARN_FIELD_NUMBER: ClassVar[int]
    DBFS_CREDENTIALS_PATH_FIELD_NUMBER: ClassVar[int]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    cross_account_external_id: str
    cross_account_intermediate_role_arn: str
    cross_account_role_arn: str
    dbfs_credentials_path: str
    enabled: bool
    def __init__(self, cross_account_role_arn: Optional[str] = ..., cross_account_external_id: Optional[str] = ..., cross_account_intermediate_role_arn: Optional[str] = ..., enabled: bool = ..., dbfs_credentials_path: Optional[str] = ...) -> None: ...

class Embedding(_message.Message):
    __slots__ = ["description", "input_column_name", "model", "output_column_name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    INPUT_COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    MODEL_FIELD_NUMBER: ClassVar[int]
    OUTPUT_COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    description: str
    input_column_name: str
    model: str
    output_column_name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, input_column_name: Optional[str] = ..., output_column_name: Optional[str] = ..., model: Optional[str] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class FeaturePublishOfflineStoreConfig(_message.Message):
    __slots__ = ["publish_full_features", "publish_start_time"]
    PUBLISH_FULL_FEATURES_FIELD_NUMBER: ClassVar[int]
    PUBLISH_START_TIME_FIELD_NUMBER: ClassVar[int]
    publish_full_features: bool
    publish_start_time: _timestamp_pb2.Timestamp
    def __init__(self, publish_full_features: bool = ..., publish_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class FeatureTable(_message.Message):
    __slots__ = ["attributes", "offline_enabled", "online_enabled", "serving_ttl"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    OFFLINE_ENABLED_FIELD_NUMBER: ClassVar[int]
    ONLINE_ENABLED_FIELD_NUMBER: ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    offline_enabled: bool
    online_enabled: bool
    serving_ttl: _duration_pb2.Duration
    def __init__(self, online_enabled: bool = ..., offline_enabled: bool = ..., serving_ttl: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ...) -> None: ...

class FeatureView(_message.Message):
    __slots__ = ["batch_compute_mode", "batch_trigger", "cache_config", "context_parameter_name", "data_quality_config", "enrichments", "entity_ids", "fco_metadata", "feature_store_format_version", "feature_table", "feature_view_id", "framework_version", "fw_version", "join_keys", "materialization_enabled", "materialization_params", "materialization_state_transitions", "monitoring_params", "online_serving_index", "options", "pipeline", "prompt", "realtime_feature_view", "schemas", "snowflake_data", "temporal", "temporal_aggregate", "timestamp_key", "validation_args", "web_url"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BATCH_COMPUTE_MODE_FIELD_NUMBER: ClassVar[int]
    BATCH_TRIGGER_FIELD_NUMBER: ClassVar[int]
    CACHE_CONFIG_FIELD_NUMBER: ClassVar[int]
    CONTEXT_PARAMETER_NAME_FIELD_NUMBER: ClassVar[int]
    DATA_QUALITY_CONFIG_FIELD_NUMBER: ClassVar[int]
    ENRICHMENTS_FIELD_NUMBER: ClassVar[int]
    ENTITY_IDS_FIELD_NUMBER: ClassVar[int]
    FCO_METADATA_FIELD_NUMBER: ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: ClassVar[int]
    FEATURE_TABLE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FRAMEWORK_VERSION_FIELD_NUMBER: ClassVar[int]
    FW_VERSION_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_ENABLED_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_PARAMS_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_STATE_TRANSITIONS_FIELD_NUMBER: ClassVar[int]
    MONITORING_PARAMS_FIELD_NUMBER: ClassVar[int]
    ONLINE_SERVING_INDEX_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    PIPELINE_FIELD_NUMBER: ClassVar[int]
    PROMPT_FIELD_NUMBER: ClassVar[int]
    REALTIME_FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    SCHEMAS_FIELD_NUMBER: ClassVar[int]
    SNOWFLAKE_DATA_FIELD_NUMBER: ClassVar[int]
    TEMPORAL_AGGREGATE_FIELD_NUMBER: ClassVar[int]
    TEMPORAL_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_KEY_FIELD_NUMBER: ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: ClassVar[int]
    WEB_URL_FIELD_NUMBER: ClassVar[int]
    batch_compute_mode: _compute_mode__client_pb2.BatchComputeMode
    batch_trigger: _feature_view__client_pb2.BatchTriggerType
    cache_config: FeatureViewCacheConfig
    context_parameter_name: str
    data_quality_config: DataQualityConfig
    enrichments: FeatureViewEnrichments
    entity_ids: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    feature_store_format_version: int
    feature_table: FeatureTable
    feature_view_id: _id__client_pb2.Id
    framework_version: int
    fw_version: _framework_version__client_pb2.FrameworkVersion
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    materialization_enabled: bool
    materialization_params: NewMaterializationParams
    materialization_state_transitions: _containers.RepeatedCompositeFieldContainer[MaterializationStateTransition]
    monitoring_params: MonitoringParams
    online_serving_index: OnlineServingIndex
    options: _containers.ScalarMap[str, str]
    pipeline: _pipeline__client_pb2.Pipeline
    prompt: Prompt
    realtime_feature_view: RealtimeFeatureView
    schemas: FeatureViewSchemas
    snowflake_data: SnowflakeData
    temporal: Temporal
    temporal_aggregate: TemporalAggregate
    timestamp_key: str
    validation_args: _validator__client_pb2.FeatureViewValidationArgs
    web_url: str
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., fco_metadata: Optional[Union[_fco_metadata__client_pb2.FcoMetadata, Mapping]] = ..., entity_ids: Optional[Iterable[Union[_id__client_pb2.Id, Mapping]]] = ..., join_keys: Optional[Iterable[str]] = ..., schemas: Optional[Union[FeatureViewSchemas, Mapping]] = ..., enrichments: Optional[Union[FeatureViewEnrichments, Mapping]] = ..., temporal_aggregate: Optional[Union[TemporalAggregate, Mapping]] = ..., temporal: Optional[Union[Temporal, Mapping]] = ..., realtime_feature_view: Optional[Union[RealtimeFeatureView, Mapping]] = ..., feature_table: Optional[Union[FeatureTable, Mapping]] = ..., prompt: Optional[Union[Prompt, Mapping]] = ..., timestamp_key: Optional[str] = ..., online_serving_index: Optional[Union[OnlineServingIndex, Mapping]] = ..., pipeline: Optional[Union[_pipeline__client_pb2.Pipeline, Mapping]] = ..., materialization_params: Optional[Union[NewMaterializationParams, Mapping]] = ..., materialization_enabled: bool = ..., materialization_state_transitions: Optional[Iterable[Union[MaterializationStateTransition, Mapping]]] = ..., monitoring_params: Optional[Union[MonitoringParams, Mapping]] = ..., feature_store_format_version: Optional[int] = ..., snowflake_data: Optional[Union[SnowflakeData, Mapping]] = ..., framework_version: Optional[int] = ..., fw_version: Optional[Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., web_url: Optional[str] = ..., batch_trigger: Optional[Union[_feature_view__client_pb2.BatchTriggerType, str]] = ..., validation_args: Optional[Union[_validator__client_pb2.FeatureViewValidationArgs, Mapping]] = ..., data_quality_config: Optional[Union[DataQualityConfig, Mapping]] = ..., options: Optional[Mapping[str, str]] = ..., batch_compute_mode: Optional[Union[_compute_mode__client_pb2.BatchComputeMode, str]] = ..., cache_config: Optional[Union[FeatureViewCacheConfig, Mapping]] = ..., context_parameter_name: Optional[str] = ...) -> None: ...

class FeatureViewCacheConfig(_message.Message):
    __slots__ = ["cache_group_name", "max_age_jitter", "max_age_seconds", "namespace", "remapped_join_keys"]
    CACHE_GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    MAX_AGE_JITTER_FIELD_NUMBER: ClassVar[int]
    MAX_AGE_SECONDS_FIELD_NUMBER: ClassVar[int]
    NAMESPACE_FIELD_NUMBER: ClassVar[int]
    REMAPPED_JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    cache_group_name: str
    max_age_jitter: _duration_pb2.Duration
    max_age_seconds: _duration_pb2.Duration
    namespace: str
    remapped_join_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: Optional[str] = ..., cache_group_name: Optional[str] = ..., max_age_seconds: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., max_age_jitter: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., remapped_join_keys: Optional[Iterable[str]] = ...) -> None: ...

class FeatureViewEnrichments(_message.Message):
    __slots__ = ["fp_materialization"]
    FP_MATERIALIZATION_FIELD_NUMBER: ClassVar[int]
    fp_materialization: _fv_materialization__client_pb2.FvMaterialization
    def __init__(self, fp_materialization: Optional[Union[_fv_materialization__client_pb2.FvMaterialization, Mapping]] = ...) -> None: ...

class FeatureViewSchemas(_message.Message):
    __slots__ = ["is_explicit_view_schema", "materialization_schema", "online_batch_table_format", "view_schema"]
    IS_EXPLICIT_VIEW_SCHEMA_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_SCHEMA_FIELD_NUMBER: ClassVar[int]
    ONLINE_BATCH_TABLE_FORMAT_FIELD_NUMBER: ClassVar[int]
    VIEW_SCHEMA_FIELD_NUMBER: ClassVar[int]
    is_explicit_view_schema: bool
    materialization_schema: _schema__client_pb2.Schema
    online_batch_table_format: _schema__client_pb2.OnlineBatchTableFormat
    view_schema: _schema__client_pb2.Schema
    def __init__(self, view_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., is_explicit_view_schema: bool = ..., materialization_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., online_batch_table_format: Optional[Union[_schema__client_pb2.OnlineBatchTableFormat, Mapping]] = ...) -> None: ...

class Inference(_message.Message):
    __slots__ = ["description", "input_columns", "model_artifact", "output_column", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    INPUT_COLUMNS_FIELD_NUMBER: ClassVar[int]
    MODEL_ARTIFACT_FIELD_NUMBER: ClassVar[int]
    OUTPUT_COLUMN_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    description: str
    input_columns: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.Column]
    model_artifact: _model_artifact_service__client_pb2.ModelArtifactInfo
    output_column: _schema__client_pb2.Column
    tags: _containers.ScalarMap[str, str]
    def __init__(self, input_columns: Optional[Iterable[Union[_schema__client_pb2.Column, Mapping]]] = ..., output_column: Optional[Union[_schema__client_pb2.Column, Mapping]] = ..., model_artifact: Optional[Union[_model_artifact_service__client_pb2.ModelArtifactInfo, Mapping]] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class MaterializationStateTransition(_message.Message):
    __slots__ = ["feature_start_timestamp", "force_stream_job_restart", "materialization_serial_version", "offline_enabled", "online_enabled", "tecton_runtime_version", "timestamp"]
    FEATURE_START_TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    FORCE_STREAM_JOB_RESTART_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_SERIAL_VERSION_FIELD_NUMBER: ClassVar[int]
    OFFLINE_ENABLED_FIELD_NUMBER: ClassVar[int]
    ONLINE_ENABLED_FIELD_NUMBER: ClassVar[int]
    TECTON_RUNTIME_VERSION_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    feature_start_timestamp: _timestamp_pb2.Timestamp
    force_stream_job_restart: bool
    materialization_serial_version: int
    offline_enabled: bool
    online_enabled: bool
    tecton_runtime_version: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., online_enabled: bool = ..., offline_enabled: bool = ..., feature_start_timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., materialization_serial_version: Optional[int] = ..., force_stream_job_restart: bool = ..., tecton_runtime_version: Optional[str] = ...) -> None: ...

class MonitoringParams(_message.Message):
    __slots__ = ["alert_email", "expected_feature_freshness", "grace_period_seconds", "monitor_freshness", "user_specified"]
    ALERT_EMAIL_FIELD_NUMBER: ClassVar[int]
    EXPECTED_FEATURE_FRESHNESS_FIELD_NUMBER: ClassVar[int]
    GRACE_PERIOD_SECONDS_FIELD_NUMBER: ClassVar[int]
    MONITOR_FRESHNESS_FIELD_NUMBER: ClassVar[int]
    USER_SPECIFIED_FIELD_NUMBER: ClassVar[int]
    alert_email: str
    expected_feature_freshness: _duration_pb2.Duration
    grace_period_seconds: int
    monitor_freshness: bool
    user_specified: bool
    def __init__(self, user_specified: bool = ..., monitor_freshness: bool = ..., expected_feature_freshness: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., alert_email: Optional[str] = ..., grace_period_seconds: Optional[int] = ...) -> None: ...

class NewMaterializationParams(_message.Message):
    __slots__ = ["aggregation_leading_edge", "batch_materialization", "compaction_enabled", "environment", "feature_publish_offline_store_config", "feature_start_timestamp", "manual_trigger_backfill_end_timestamp", "materialization_start_timestamp", "max_backfill_interval", "max_source_data_delay", "offline_store_config", "offline_store_params", "online_backfill_load_type", "online_store_params", "output_stream", "schedule_interval", "stream_materialization", "stream_tile_size", "stream_tiling_enabled", "tecton_materialization_runtime", "time_range_policy", "writes_to_offline_store", "writes_to_online_store"]
    AGGREGATION_LEADING_EDGE_FIELD_NUMBER: ClassVar[int]
    BATCH_MATERIALIZATION_FIELD_NUMBER: ClassVar[int]
    COMPACTION_ENABLED_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    FEATURE_PUBLISH_OFFLINE_STORE_CONFIG_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    MANUAL_TRIGGER_BACKFILL_END_TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_START_TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    MAX_BACKFILL_INTERVAL_FIELD_NUMBER: ClassVar[int]
    MAX_SOURCE_DATA_DELAY_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_CONFIG_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_PARAMS_FIELD_NUMBER: ClassVar[int]
    ONLINE_BACKFILL_LOAD_TYPE_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_PARAMS_FIELD_NUMBER: ClassVar[int]
    OUTPUT_STREAM_FIELD_NUMBER: ClassVar[int]
    SCHEDULE_INTERVAL_FIELD_NUMBER: ClassVar[int]
    STREAM_MATERIALIZATION_FIELD_NUMBER: ClassVar[int]
    STREAM_TILE_SIZE_FIELD_NUMBER: ClassVar[int]
    STREAM_TILING_ENABLED_FIELD_NUMBER: ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_FIELD_NUMBER: ClassVar[int]
    TIME_RANGE_POLICY_FIELD_NUMBER: ClassVar[int]
    WRITES_TO_OFFLINE_STORE_FIELD_NUMBER: ClassVar[int]
    WRITES_TO_ONLINE_STORE_FIELD_NUMBER: ClassVar[int]
    aggregation_leading_edge: _feature_view__client_pb2.AggregationLeadingEdge
    batch_materialization: _feature_view__client_pb2.ClusterConfig
    compaction_enabled: bool
    environment: str
    feature_publish_offline_store_config: FeaturePublishOfflineStoreConfig
    feature_start_timestamp: _timestamp_pb2.Timestamp
    manual_trigger_backfill_end_timestamp: _timestamp_pb2.Timestamp
    materialization_start_timestamp: _timestamp_pb2.Timestamp
    max_backfill_interval: _duration_pb2.Duration
    max_source_data_delay: _duration_pb2.Duration
    offline_store_config: _feature_view__client_pb2.OfflineFeatureStoreConfig
    offline_store_params: OfflineStoreParams
    online_backfill_load_type: _fv_materialization__client_pb2.OnlineBackfillLoadType
    online_store_params: OnlineStoreParams
    output_stream: _feature_view__client_pb2.OutputStream
    schedule_interval: _duration_pb2.Duration
    stream_materialization: _feature_view__client_pb2.ClusterConfig
    stream_tile_size: _duration_pb2.Duration
    stream_tiling_enabled: bool
    tecton_materialization_runtime: str
    time_range_policy: MaterializationTimeRangePolicy
    writes_to_offline_store: bool
    writes_to_online_store: bool
    def __init__(self, schedule_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., materialization_start_timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_start_timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., manual_trigger_backfill_end_timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., max_backfill_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., writes_to_online_store: bool = ..., writes_to_offline_store: bool = ..., offline_store_config: Optional[Union[_feature_view__client_pb2.OfflineFeatureStoreConfig, Mapping]] = ..., offline_store_params: Optional[Union[OfflineStoreParams, Mapping]] = ..., batch_materialization: Optional[Union[_feature_view__client_pb2.ClusterConfig, Mapping]] = ..., stream_materialization: Optional[Union[_feature_view__client_pb2.ClusterConfig, Mapping]] = ..., max_source_data_delay: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., online_store_params: Optional[Union[OnlineStoreParams, Mapping]] = ..., output_stream: Optional[Union[_feature_view__client_pb2.OutputStream, Mapping]] = ..., time_range_policy: Optional[Union[MaterializationTimeRangePolicy, str]] = ..., online_backfill_load_type: Optional[Union[_fv_materialization__client_pb2.OnlineBackfillLoadType, str]] = ..., tecton_materialization_runtime: Optional[str] = ..., feature_publish_offline_store_config: Optional[Union[FeaturePublishOfflineStoreConfig, Mapping]] = ..., compaction_enabled: bool = ..., stream_tiling_enabled: bool = ..., environment: Optional[str] = ..., stream_tile_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., aggregation_leading_edge: Optional[Union[_feature_view__client_pb2.AggregationLeadingEdge, str]] = ...) -> None: ...

class OfflineStoreParams(_message.Message):
    __slots__ = ["delta", "parquet"]
    DELTA_FIELD_NUMBER: ClassVar[int]
    PARQUET_FIELD_NUMBER: ClassVar[int]
    delta: DeltaOfflineStoreParams
    parquet: ParquetOfflineStoreParams
    def __init__(self, parquet: Optional[Union[ParquetOfflineStoreParams, Mapping]] = ..., delta: Optional[Union[DeltaOfflineStoreParams, Mapping]] = ...) -> None: ...

class OnlineServingIndex(_message.Message):
    __slots__ = ["join_keys"]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, join_keys: Optional[Iterable[str]] = ...) -> None: ...

class OnlineStoreParams(_message.Message):
    __slots__ = ["bigtable", "dynamo", "redis"]
    BIGTABLE_FIELD_NUMBER: ClassVar[int]
    DYNAMO_FIELD_NUMBER: ClassVar[int]
    REDIS_FIELD_NUMBER: ClassVar[int]
    bigtable: BigtableOnlineStore
    dynamo: DynamoDbOnlineStore
    redis: RedisOnlineStore
    def __init__(self, dynamo: Optional[Union[DynamoDbOnlineStore, Mapping]] = ..., redis: Optional[Union[RedisOnlineStore, Mapping]] = ..., bigtable: Optional[Union[BigtableOnlineStore, Mapping]] = ...) -> None: ...

class ParquetOfflineStoreParams(_message.Message):
    __slots__ = ["time_partition_size", "version"]
    TIME_PARTITION_SIZE_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    time_partition_size: _duration_pb2.Duration
    version: ParquetOfflineStoreVersion
    def __init__(self, time_partition_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., version: Optional[Union[ParquetOfflineStoreVersion, str]] = ...) -> None: ...

class Prompt(_message.Message):
    __slots__ = ["attributes", "environment"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    environment: _realtime_compute__client_pb2.RemoteFunctionComputeConfig
    def __init__(self, environment: Optional[Union[_realtime_compute__client_pb2.RemoteFunctionComputeConfig, Mapping]] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ...) -> None: ...

class RealtimeFeatureView(_message.Message):
    __slots__ = ["attributes", "no_op", "supported_environments"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    NO_OP_FIELD_NUMBER: ClassVar[int]
    SUPPORTED_ENVIRONMENTS_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    no_op: bool
    supported_environments: _containers.RepeatedCompositeFieldContainer[_realtime_compute__client_pb2.RemoteFunctionComputeConfig]
    def __init__(self, no_op: bool = ..., supported_environments: Optional[Iterable[Union[_realtime_compute__client_pb2.RemoteFunctionComputeConfig, Mapping]]] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ...) -> None: ...

class RedisOnlineStore(_message.Message):
    __slots__ = ["authentication_token", "enabled", "inject_host_sni", "primary_endpoint", "tls_enabled"]
    AUTHENTICATION_TOKEN_FIELD_NUMBER: ClassVar[int]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    INJECT_HOST_SNI_FIELD_NUMBER: ClassVar[int]
    PRIMARY_ENDPOINT_FIELD_NUMBER: ClassVar[int]
    TLS_ENABLED_FIELD_NUMBER: ClassVar[int]
    authentication_token: str
    enabled: bool
    inject_host_sni: bool
    primary_endpoint: str
    tls_enabled: bool
    def __init__(self, primary_endpoint: Optional[str] = ..., authentication_token: Optional[str] = ..., tls_enabled: bool = ..., enabled: bool = ..., inject_host_sni: bool = ...) -> None: ...

class SecondaryKeyOutputColumn(_message.Message):
    __slots__ = ["name", "time_window"]
    NAME_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    name: str
    time_window: _time_window__client_pb2.TimeWindow
    def __init__(self, time_window: Optional[Union[_time_window__client_pb2.TimeWindow, Mapping]] = ..., name: Optional[str] = ...) -> None: ...

class SnowflakeData(_message.Message):
    __slots__ = ["snowflake_view_name"]
    SNOWFLAKE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    snowflake_view_name: str
    def __init__(self, snowflake_view_name: Optional[str] = ...) -> None: ...

class Temporal(_message.Message):
    __slots__ = ["attributes", "backfill_config", "data_source_type", "embeddings", "incremental_backfills", "inferences", "is_continuous", "serving_ttl"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    BACKFILL_CONFIG_FIELD_NUMBER: ClassVar[int]
    DATA_SOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    EMBEDDINGS_FIELD_NUMBER: ClassVar[int]
    INCREMENTAL_BACKFILLS_FIELD_NUMBER: ClassVar[int]
    INFERENCES_FIELD_NUMBER: ClassVar[int]
    IS_CONTINUOUS_FIELD_NUMBER: ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    backfill_config: _feature_view__client_pb2.BackfillConfig
    data_source_type: _data_source_type__client_pb2.DataSourceType
    embeddings: _containers.RepeatedCompositeFieldContainer[Embedding]
    incremental_backfills: bool
    inferences: _containers.RepeatedCompositeFieldContainer[Inference]
    is_continuous: bool
    serving_ttl: _duration_pb2.Duration
    def __init__(self, serving_ttl: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., data_source_type: Optional[Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., backfill_config: Optional[Union[_feature_view__client_pb2.BackfillConfig, Mapping]] = ..., incremental_backfills: bool = ..., is_continuous: bool = ..., embeddings: Optional[Iterable[Union[Embedding, Mapping]]] = ..., inferences: Optional[Iterable[Union[Inference, Mapping]]] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ...) -> None: ...

class TemporalAggregate(_message.Message):
    __slots__ = ["aggregation_secondary_key", "data_source_type", "features", "is_continuous", "secondary_key_output_columns", "slide_interval", "slide_interval_string"]
    AGGREGATION_SECONDARY_KEY_FIELD_NUMBER: ClassVar[int]
    DATA_SOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    FEATURES_FIELD_NUMBER: ClassVar[int]
    IS_CONTINUOUS_FIELD_NUMBER: ClassVar[int]
    SECONDARY_KEY_OUTPUT_COLUMNS_FIELD_NUMBER: ClassVar[int]
    SLIDE_INTERVAL_FIELD_NUMBER: ClassVar[int]
    SLIDE_INTERVAL_STRING_FIELD_NUMBER: ClassVar[int]
    aggregation_secondary_key: str
    data_source_type: _data_source_type__client_pb2.DataSourceType
    features: _containers.RepeatedCompositeFieldContainer[Aggregate]
    is_continuous: bool
    secondary_key_output_columns: _containers.RepeatedCompositeFieldContainer[SecondaryKeyOutputColumn]
    slide_interval: _duration_pb2.Duration
    slide_interval_string: str
    def __init__(self, slide_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., slide_interval_string: Optional[str] = ..., features: Optional[Iterable[Union[Aggregate, Mapping]]] = ..., is_continuous: bool = ..., data_source_type: Optional[Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., aggregation_secondary_key: Optional[str] = ..., secondary_key_output_columns: Optional[Iterable[Union[SecondaryKeyOutputColumn, Mapping]]] = ...) -> None: ...

class TrailingTimeWindowAggregation(_message.Message):
    __slots__ = ["aggregation_slide_period", "features", "is_continuous", "time_key"]
    AGGREGATION_SLIDE_PERIOD_FIELD_NUMBER: ClassVar[int]
    FEATURES_FIELD_NUMBER: ClassVar[int]
    IS_CONTINUOUS_FIELD_NUMBER: ClassVar[int]
    TIME_KEY_FIELD_NUMBER: ClassVar[int]
    aggregation_slide_period: _duration_pb2.Duration
    features: _containers.RepeatedCompositeFieldContainer[Aggregate]
    is_continuous: bool
    time_key: str
    def __init__(self, time_key: Optional[str] = ..., aggregation_slide_period: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., features: Optional[Iterable[Union[Aggregate, Mapping]]] = ..., is_continuous: bool = ...) -> None: ...

class ParquetOfflineStoreVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DeltaOfflineStoreVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MaterializationTimeRangePolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
