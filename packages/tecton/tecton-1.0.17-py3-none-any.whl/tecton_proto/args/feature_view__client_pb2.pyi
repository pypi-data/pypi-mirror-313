from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import data_source__client_pb2 as _data_source__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import pipeline__client_pb2 as _pipeline__client_pb2
from tecton_proto.common import analytics_options__client_pb2 as _analytics_options__client_pb2
from tecton_proto.common import compute_mode__client_pb2 as _compute_mode__client_pb2
from tecton_proto.common import data_source_type__client_pb2 as _data_source_type__client_pb2
from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.common import time_window__client_pb2 as _time_window__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

AGGREGATION_MODE_LATEST_EVENT_TIME: AggregationLeadingEdge
AGGREGATION_MODE_UNSPECIFIED: AggregationLeadingEdge
AGGREGATION_MODE_WALL_CLOCK_TIME: AggregationLeadingEdge
BACKFILL_CONFIG_MODE_MULTIPLE_BATCH_SCHEDULE_INTERVALS_PER_JOB: BackfillConfigMode
BACKFILL_CONFIG_MODE_SINGLE_BATCH_SCHEDULE_INTERVAL_PER_JOB: BackfillConfigMode
BACKFILL_CONFIG_MODE_UNSPECIFIED: BackfillConfigMode
BATCH_TRIGGER_TYPE_MANUAL: BatchTriggerType
BATCH_TRIGGER_TYPE_NO_BATCH_MATERIALIZATION: BatchTriggerType
BATCH_TRIGGER_TYPE_SCHEDULED: BatchTriggerType
BATCH_TRIGGER_TYPE_UNSPECIFIED: BatchTriggerType
DESCRIPTOR: _descriptor.FileDescriptor
FEATURE_STORE_FORMAT_VERSION_DEFAULT: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_MAX: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_ONLINE_STORE_TTL_DELETION_ENABLED: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_TTL_FIELD: FeatureStoreFormatVersion
FEATURE_VIEW_TYPE_FEATURE_TABLE: FeatureViewType
FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW: FeatureViewType
FEATURE_VIEW_TYPE_PROMPT: FeatureViewType
FEATURE_VIEW_TYPE_REALTIME: FeatureViewType
FEATURE_VIEW_TYPE_UNSPECIFIED: FeatureViewType
STREAM_PROCESSING_MODE_CONTINUOUS: StreamProcessingMode
STREAM_PROCESSING_MODE_TIME_INTERVAL: StreamProcessingMode
STREAM_PROCESSING_MODE_UNSPECIFIED: StreamProcessingMode

class Attribute(_message.Message):
    __slots__ = ["column_dtype", "description", "name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COLUMN_DTYPE_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    column_dtype: _data_type__client_pb2.DataType
    description: str
    name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: Optional[str] = ..., column_dtype: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class BackfillConfig(_message.Message):
    __slots__ = ["mode"]
    MODE_FIELD_NUMBER: ClassVar[int]
    mode: BackfillConfigMode
    def __init__(self, mode: Optional[Union[BackfillConfigMode, str]] = ...) -> None: ...

class BigtableOnlineStore(_message.Message):
    __slots__ = ["enabled", "instance_id", "project_id"]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: ClassVar[int]
    enabled: bool
    instance_id: str
    project_id: str
    def __init__(self, enabled: bool = ..., project_id: Optional[str] = ..., instance_id: Optional[str] = ...) -> None: ...

class CacheConfig(_message.Message):
    __slots__ = ["max_age_seconds"]
    MAX_AGE_SECONDS_FIELD_NUMBER: ClassVar[int]
    max_age_seconds: int
    def __init__(self, max_age_seconds: Optional[int] = ...) -> None: ...

class ClusterConfig(_message.Message):
    __slots__ = ["existing_cluster", "implicit_config", "json_databricks", "json_dataproc", "json_emr", "new_databricks", "new_emr", "rift"]
    EXISTING_CLUSTER_FIELD_NUMBER: ClassVar[int]
    IMPLICIT_CONFIG_FIELD_NUMBER: ClassVar[int]
    JSON_DATABRICKS_FIELD_NUMBER: ClassVar[int]
    JSON_DATAPROC_FIELD_NUMBER: ClassVar[int]
    JSON_EMR_FIELD_NUMBER: ClassVar[int]
    NEW_DATABRICKS_FIELD_NUMBER: ClassVar[int]
    NEW_EMR_FIELD_NUMBER: ClassVar[int]
    RIFT_FIELD_NUMBER: ClassVar[int]
    existing_cluster: ExistingClusterConfig
    implicit_config: DefaultClusterConfig
    json_databricks: JsonClusterConfig
    json_dataproc: JsonClusterConfig
    json_emr: JsonClusterConfig
    new_databricks: NewClusterConfig
    new_emr: NewClusterConfig
    rift: RiftClusterConfig
    def __init__(self, existing_cluster: Optional[Union[ExistingClusterConfig, Mapping]] = ..., new_databricks: Optional[Union[NewClusterConfig, Mapping]] = ..., new_emr: Optional[Union[NewClusterConfig, Mapping]] = ..., implicit_config: Optional[Union[DefaultClusterConfig, Mapping]] = ..., json_databricks: Optional[Union[JsonClusterConfig, Mapping]] = ..., json_emr: Optional[Union[JsonClusterConfig, Mapping]] = ..., json_dataproc: Optional[Union[JsonClusterConfig, Mapping]] = ..., rift: Optional[Union[RiftClusterConfig, Mapping]] = ...) -> None: ...

class DataQualityConfig(_message.Message):
    __slots__ = ["data_quality_enabled", "skip_default_expectations"]
    DATA_QUALITY_ENABLED_FIELD_NUMBER: ClassVar[int]
    SKIP_DEFAULT_EXPECTATIONS_FIELD_NUMBER: ClassVar[int]
    data_quality_enabled: bool
    skip_default_expectations: bool
    def __init__(self, data_quality_enabled: bool = ..., skip_default_expectations: bool = ...) -> None: ...

class DefaultClusterConfig(_message.Message):
    __slots__ = ["databricks_spark_version", "emr_spark_version", "tecton_compute_instance_type"]
    DATABRICKS_SPARK_VERSION_FIELD_NUMBER: ClassVar[int]
    EMR_SPARK_VERSION_FIELD_NUMBER: ClassVar[int]
    TECTON_COMPUTE_INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    databricks_spark_version: str
    emr_spark_version: str
    tecton_compute_instance_type: str
    def __init__(self, databricks_spark_version: Optional[str] = ..., emr_spark_version: Optional[str] = ..., tecton_compute_instance_type: Optional[str] = ...) -> None: ...

class DeltaConfig(_message.Message):
    __slots__ = ["time_partition_size"]
    TIME_PARTITION_SIZE_FIELD_NUMBER: ClassVar[int]
    time_partition_size: _duration_pb2.Duration
    def __init__(self, time_partition_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class DynamoDbOnlineStore(_message.Message):
    __slots__ = ["enabled"]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class Embedding(_message.Message):
    __slots__ = ["column", "column_dtype", "description", "model", "name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COLUMN_DTYPE_FIELD_NUMBER: ClassVar[int]
    COLUMN_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    MODEL_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    column: str
    column_dtype: _data_type__client_pb2.DataType
    description: str
    model: str
    name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: Optional[str] = ..., column: Optional[str] = ..., column_dtype: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ..., model: Optional[str] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class EntityKeyOverride(_message.Message):
    __slots__ = ["entity_id", "join_keys"]
    ENTITY_ID_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    entity_id: _id__client_pb2.Id
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entity_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., join_keys: Optional[Iterable[str]] = ...) -> None: ...

class ExistingClusterConfig(_message.Message):
    __slots__ = ["existing_cluster_id"]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    existing_cluster_id: str
    def __init__(self, existing_cluster_id: Optional[str] = ...) -> None: ...

class FeatureAggregation(_message.Message):
    __slots__ = ["batch_sawtooth_tile_size", "column", "column_dtype", "description", "function", "function_params", "lifetime_window", "name", "tags", "time_window", "time_window_legacy", "time_window_series"]
    class FunctionParamsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: ParamValue
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[ParamValue, Mapping]] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BATCH_SAWTOOTH_TILE_SIZE_FIELD_NUMBER: ClassVar[int]
    COLUMN_DTYPE_FIELD_NUMBER: ClassVar[int]
    COLUMN_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    FUNCTION_FIELD_NUMBER: ClassVar[int]
    FUNCTION_PARAMS_FIELD_NUMBER: ClassVar[int]
    LIFETIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_LEGACY_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_SERIES_FIELD_NUMBER: ClassVar[int]
    batch_sawtooth_tile_size: _duration_pb2.Duration
    column: str
    column_dtype: _data_type__client_pb2.DataType
    description: str
    function: str
    function_params: _containers.MessageMap[str, ParamValue]
    lifetime_window: _time_window__client_pb2.LifetimeWindow
    name: str
    tags: _containers.ScalarMap[str, str]
    time_window: TimeWindow
    time_window_legacy: _duration_pb2.Duration
    time_window_series: TimeWindowSeries
    def __init__(self, column: Optional[str] = ..., function: Optional[str] = ..., function_params: Optional[Mapping[str, ParamValue]] = ..., time_window_legacy: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., name: Optional[str] = ..., time_window: Optional[Union[TimeWindow, Mapping]] = ..., lifetime_window: Optional[Union[_time_window__client_pb2.LifetimeWindow, Mapping]] = ..., time_window_series: Optional[Union[TimeWindowSeries, Mapping]] = ..., column_dtype: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ..., batch_sawtooth_tile_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class FeatureTableArgs(_message.Message):
    __slots__ = ["attributes", "batch_compute", "monitoring", "offline_store", "offline_store_legacy", "online_store", "schema", "serving_ttl", "tecton_materialization_runtime", "timestamp_field"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    BATCH_COMPUTE_FIELD_NUMBER: ClassVar[int]
    MONITORING_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_LEGACY_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    batch_compute: ClusterConfig
    monitoring: MonitoringConfig
    offline_store: OfflineStoreConfig
    offline_store_legacy: OfflineFeatureStoreConfig
    online_store: OnlineStoreConfig
    schema: _spark_schema__client_pb2.SparkSchema
    serving_ttl: _duration_pb2.Duration
    tecton_materialization_runtime: str
    timestamp_field: str
    def __init__(self, schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., serving_ttl: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., offline_store_legacy: Optional[Union[OfflineFeatureStoreConfig, Mapping]] = ..., offline_store: Optional[Union[OfflineStoreConfig, Mapping]] = ..., online_store: Optional[Union[OnlineStoreConfig, Mapping]] = ..., batch_compute: Optional[Union[ClusterConfig, Mapping]] = ..., monitoring: Optional[Union[MonitoringConfig, Mapping]] = ..., tecton_materialization_runtime: Optional[str] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ..., timestamp_field: Optional[str] = ...) -> None: ...

class FeatureViewArgs(_message.Message):
    __slots__ = ["batch_compute_mode", "cache_config", "context_parameter_name", "data_quality_config", "entities", "feature_table_args", "feature_view_id", "feature_view_type", "forced_materialized_schema", "forced_view_schema", "info", "materialized_feature_view_args", "offline_enabled", "online_enabled", "online_serving_index", "options", "pipeline", "prevent_destroy", "prompt_args", "realtime_args", "version"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BATCH_COMPUTE_MODE_FIELD_NUMBER: ClassVar[int]
    CACHE_CONFIG_FIELD_NUMBER: ClassVar[int]
    CONTEXT_PARAMETER_NAME_FIELD_NUMBER: ClassVar[int]
    DATA_QUALITY_CONFIG_FIELD_NUMBER: ClassVar[int]
    ENTITIES_FIELD_NUMBER: ClassVar[int]
    FEATURE_TABLE_ARGS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_TYPE_FIELD_NUMBER: ClassVar[int]
    FORCED_MATERIALIZED_SCHEMA_FIELD_NUMBER: ClassVar[int]
    FORCED_VIEW_SCHEMA_FIELD_NUMBER: ClassVar[int]
    INFO_FIELD_NUMBER: ClassVar[int]
    MATERIALIZED_FEATURE_VIEW_ARGS_FIELD_NUMBER: ClassVar[int]
    OFFLINE_ENABLED_FIELD_NUMBER: ClassVar[int]
    ONLINE_ENABLED_FIELD_NUMBER: ClassVar[int]
    ONLINE_SERVING_INDEX_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    PIPELINE_FIELD_NUMBER: ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: ClassVar[int]
    PROMPT_ARGS_FIELD_NUMBER: ClassVar[int]
    REALTIME_ARGS_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    batch_compute_mode: _compute_mode__client_pb2.BatchComputeMode
    cache_config: CacheConfig
    context_parameter_name: str
    data_quality_config: DataQualityConfig
    entities: _containers.RepeatedCompositeFieldContainer[EntityKeyOverride]
    feature_table_args: FeatureTableArgs
    feature_view_id: _id__client_pb2.Id
    feature_view_type: FeatureViewType
    forced_materialized_schema: _spark_schema__client_pb2.SparkSchema
    forced_view_schema: _spark_schema__client_pb2.SparkSchema
    info: _basic_info__client_pb2.BasicInfo
    materialized_feature_view_args: MaterializedFeatureViewArgs
    offline_enabled: bool
    online_enabled: bool
    online_serving_index: _containers.RepeatedScalarFieldContainer[str]
    options: _containers.ScalarMap[str, str]
    pipeline: _pipeline__client_pb2.Pipeline
    prevent_destroy: bool
    prompt_args: PromptArgs
    realtime_args: RealtimeArgs
    version: _framework_version__client_pb2.FrameworkVersion
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_view_type: Optional[Union[FeatureViewType, str]] = ..., info: Optional[Union[_basic_info__client_pb2.BasicInfo, Mapping]] = ..., version: Optional[Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., prevent_destroy: bool = ..., options: Optional[Mapping[str, str]] = ..., cache_config: Optional[Union[CacheConfig, Mapping]] = ..., entities: Optional[Iterable[Union[EntityKeyOverride, Mapping]]] = ..., materialized_feature_view_args: Optional[Union[MaterializedFeatureViewArgs, Mapping]] = ..., realtime_args: Optional[Union[RealtimeArgs, Mapping]] = ..., feature_table_args: Optional[Union[FeatureTableArgs, Mapping]] = ..., prompt_args: Optional[Union[PromptArgs, Mapping]] = ..., context_parameter_name: Optional[str] = ..., online_serving_index: Optional[Iterable[str]] = ..., online_enabled: bool = ..., offline_enabled: bool = ..., batch_compute_mode: Optional[Union[_compute_mode__client_pb2.BatchComputeMode, str]] = ..., pipeline: Optional[Union[_pipeline__client_pb2.Pipeline, Mapping]] = ..., data_quality_config: Optional[Union[DataQualityConfig, Mapping]] = ..., forced_view_schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., forced_materialized_schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...

class Inference(_message.Message):
    __slots__ = ["description", "input_columns", "model", "name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    INPUT_COLUMNS_FIELD_NUMBER: ClassVar[int]
    MODEL_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    description: str
    input_columns: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.Field]
    model: str
    name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, input_columns: Optional[Iterable[Union[_schema__client_pb2.Field, Mapping]]] = ..., name: Optional[str] = ..., model: Optional[str] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class JsonClusterConfig(_message.Message):
    __slots__ = ["json"]
    JSON_FIELD_NUMBER: ClassVar[int]
    json: _struct_pb2.Struct
    def __init__(self, json: Optional[Union[_struct_pb2.Struct, Mapping]] = ...) -> None: ...

class MaterializedFeatureViewArgs(_message.Message):
    __slots__ = ["aggregation_interval", "aggregation_leading_edge", "aggregation_secondary_key", "aggregations", "attributes", "batch_compute", "batch_schedule", "batch_trigger", "compaction_enabled", "data_source_type", "embeddings", "environment", "feature_start_time", "feature_store_format_version", "incremental_backfills", "inferences", "lifetime_start_time", "manual_trigger_backfill_end_time", "max_backfill_interval", "monitoring", "offline_store", "offline_store_legacy", "online_store", "output_stream", "run_transformation_validation", "schema", "secondary_key_output_columns", "serving_ttl", "stream_compute", "stream_processing_mode", "stream_tile_size", "stream_tiling_enabled", "tecton_materialization_runtime", "timestamp_field"]
    AGGREGATIONS_FIELD_NUMBER: ClassVar[int]
    AGGREGATION_INTERVAL_FIELD_NUMBER: ClassVar[int]
    AGGREGATION_LEADING_EDGE_FIELD_NUMBER: ClassVar[int]
    AGGREGATION_SECONDARY_KEY_FIELD_NUMBER: ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    BATCH_COMPUTE_FIELD_NUMBER: ClassVar[int]
    BATCH_SCHEDULE_FIELD_NUMBER: ClassVar[int]
    BATCH_TRIGGER_FIELD_NUMBER: ClassVar[int]
    COMPACTION_ENABLED_FIELD_NUMBER: ClassVar[int]
    DATA_SOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    EMBEDDINGS_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: ClassVar[int]
    INCREMENTAL_BACKFILLS_FIELD_NUMBER: ClassVar[int]
    INFERENCES_FIELD_NUMBER: ClassVar[int]
    LIFETIME_START_TIME_FIELD_NUMBER: ClassVar[int]
    MANUAL_TRIGGER_BACKFILL_END_TIME_FIELD_NUMBER: ClassVar[int]
    MAX_BACKFILL_INTERVAL_FIELD_NUMBER: ClassVar[int]
    MONITORING_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_LEGACY_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_FIELD_NUMBER: ClassVar[int]
    OUTPUT_STREAM_FIELD_NUMBER: ClassVar[int]
    RUN_TRANSFORMATION_VALIDATION_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    SECONDARY_KEY_OUTPUT_COLUMNS_FIELD_NUMBER: ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: ClassVar[int]
    STREAM_COMPUTE_FIELD_NUMBER: ClassVar[int]
    STREAM_PROCESSING_MODE_FIELD_NUMBER: ClassVar[int]
    STREAM_TILE_SIZE_FIELD_NUMBER: ClassVar[int]
    STREAM_TILING_ENABLED_FIELD_NUMBER: ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: ClassVar[int]
    aggregation_interval: _duration_pb2.Duration
    aggregation_leading_edge: AggregationLeadingEdge
    aggregation_secondary_key: str
    aggregations: _containers.RepeatedCompositeFieldContainer[FeatureAggregation]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    batch_compute: ClusterConfig
    batch_schedule: _duration_pb2.Duration
    batch_trigger: BatchTriggerType
    compaction_enabled: bool
    data_source_type: _data_source_type__client_pb2.DataSourceType
    embeddings: _containers.RepeatedCompositeFieldContainer[Embedding]
    environment: str
    feature_start_time: _timestamp_pb2.Timestamp
    feature_store_format_version: FeatureStoreFormatVersion
    incremental_backfills: bool
    inferences: _containers.RepeatedCompositeFieldContainer[Inference]
    lifetime_start_time: _timestamp_pb2.Timestamp
    manual_trigger_backfill_end_time: _timestamp_pb2.Timestamp
    max_backfill_interval: _duration_pb2.Duration
    monitoring: MonitoringConfig
    offline_store: OfflineStoreConfig
    offline_store_legacy: OfflineFeatureStoreConfig
    online_store: OnlineStoreConfig
    output_stream: OutputStream
    run_transformation_validation: bool
    schema: _schema__client_pb2.Schema
    secondary_key_output_columns: _containers.RepeatedCompositeFieldContainer[SecondaryKeyOutputColumn]
    serving_ttl: _duration_pb2.Duration
    stream_compute: ClusterConfig
    stream_processing_mode: StreamProcessingMode
    stream_tile_size: _duration_pb2.Duration
    stream_tiling_enabled: bool
    tecton_materialization_runtime: str
    timestamp_field: str
    def __init__(self, timestamp_field: Optional[str] = ..., batch_schedule: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., manual_trigger_backfill_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., max_backfill_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., serving_ttl: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., offline_store_legacy: Optional[Union[OfflineFeatureStoreConfig, Mapping]] = ..., offline_store: Optional[Union[OfflineStoreConfig, Mapping]] = ..., batch_compute: Optional[Union[ClusterConfig, Mapping]] = ..., stream_compute: Optional[Union[ClusterConfig, Mapping]] = ..., monitoring: Optional[Union[MonitoringConfig, Mapping]] = ..., data_source_type: Optional[Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., online_store: Optional[Union[OnlineStoreConfig, Mapping]] = ..., incremental_backfills: bool = ..., aggregation_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., stream_processing_mode: Optional[Union[StreamProcessingMode, str]] = ..., aggregations: Optional[Iterable[Union[FeatureAggregation, Mapping]]] = ..., output_stream: Optional[Union[OutputStream, Mapping]] = ..., batch_trigger: Optional[Union[BatchTriggerType, str]] = ..., schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., aggregation_secondary_key: Optional[str] = ..., secondary_key_output_columns: Optional[Iterable[Union[SecondaryKeyOutputColumn, Mapping]]] = ..., run_transformation_validation: bool = ..., tecton_materialization_runtime: Optional[str] = ..., lifetime_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., compaction_enabled: bool = ..., stream_tiling_enabled: bool = ..., stream_tile_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., environment: Optional[str] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ..., embeddings: Optional[Iterable[Union[Embedding, Mapping]]] = ..., inferences: Optional[Iterable[Union[Inference, Mapping]]] = ..., aggregation_leading_edge: Optional[Union[AggregationLeadingEdge, str]] = ..., feature_store_format_version: Optional[Union[FeatureStoreFormatVersion, str]] = ...) -> None: ...

class MonitoringConfig(_message.Message):
    __slots__ = ["alert_email", "expected_freshness", "monitor_freshness"]
    ALERT_EMAIL_FIELD_NUMBER: ClassVar[int]
    EXPECTED_FRESHNESS_FIELD_NUMBER: ClassVar[int]
    MONITOR_FRESHNESS_FIELD_NUMBER: ClassVar[int]
    alert_email: str
    expected_freshness: _duration_pb2.Duration
    monitor_freshness: bool
    def __init__(self, monitor_freshness: bool = ..., expected_freshness: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., alert_email: Optional[str] = ...) -> None: ...

class NewClusterConfig(_message.Message):
    __slots__ = ["extra_pip_dependencies", "first_on_demand", "instance_availability", "instance_type", "number_of_workers", "pinned_spark_version", "root_volume_size_in_gb", "spark_config"]
    EXTRA_PIP_DEPENDENCIES_FIELD_NUMBER: ClassVar[int]
    FIRST_ON_DEMAND_FIELD_NUMBER: ClassVar[int]
    INSTANCE_AVAILABILITY_FIELD_NUMBER: ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    NUMBER_OF_WORKERS_FIELD_NUMBER: ClassVar[int]
    PINNED_SPARK_VERSION_FIELD_NUMBER: ClassVar[int]
    ROOT_VOLUME_SIZE_IN_GB_FIELD_NUMBER: ClassVar[int]
    SPARK_CONFIG_FIELD_NUMBER: ClassVar[int]
    extra_pip_dependencies: _containers.RepeatedScalarFieldContainer[str]
    first_on_demand: int
    instance_availability: str
    instance_type: str
    number_of_workers: int
    pinned_spark_version: str
    root_volume_size_in_gb: int
    spark_config: SparkConfig
    def __init__(self, instance_type: Optional[str] = ..., instance_availability: Optional[str] = ..., number_of_workers: Optional[int] = ..., root_volume_size_in_gb: Optional[int] = ..., extra_pip_dependencies: Optional[Iterable[str]] = ..., spark_config: Optional[Union[SparkConfig, Mapping]] = ..., first_on_demand: Optional[int] = ..., pinned_spark_version: Optional[str] = ...) -> None: ...

class OfflineFeatureStoreConfig(_message.Message):
    __slots__ = ["delta", "parquet", "subdirectory_override"]
    DELTA_FIELD_NUMBER: ClassVar[int]
    PARQUET_FIELD_NUMBER: ClassVar[int]
    SUBDIRECTORY_OVERRIDE_FIELD_NUMBER: ClassVar[int]
    delta: DeltaConfig
    parquet: ParquetConfig
    subdirectory_override: str
    def __init__(self, parquet: Optional[Union[ParquetConfig, Mapping]] = ..., delta: Optional[Union[DeltaConfig, Mapping]] = ..., subdirectory_override: Optional[str] = ...) -> None: ...

class OfflineStoreConfig(_message.Message):
    __slots__ = ["publish_full_features", "publish_start_time", "staging_table_format"]
    PUBLISH_FULL_FEATURES_FIELD_NUMBER: ClassVar[int]
    PUBLISH_START_TIME_FIELD_NUMBER: ClassVar[int]
    STAGING_TABLE_FORMAT_FIELD_NUMBER: ClassVar[int]
    publish_full_features: bool
    publish_start_time: _timestamp_pb2.Timestamp
    staging_table_format: OfflineFeatureStoreConfig
    def __init__(self, staging_table_format: Optional[Union[OfflineFeatureStoreConfig, Mapping]] = ..., publish_full_features: bool = ..., publish_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class OnlineStoreConfig(_message.Message):
    __slots__ = ["bigtable", "dynamo", "redis"]
    BIGTABLE_FIELD_NUMBER: ClassVar[int]
    DYNAMO_FIELD_NUMBER: ClassVar[int]
    REDIS_FIELD_NUMBER: ClassVar[int]
    bigtable: BigtableOnlineStore
    dynamo: DynamoDbOnlineStore
    redis: RedisOnlineStore
    def __init__(self, dynamo: Optional[Union[DynamoDbOnlineStore, Mapping]] = ..., redis: Optional[Union[RedisOnlineStore, Mapping]] = ..., bigtable: Optional[Union[BigtableOnlineStore, Mapping]] = ...) -> None: ...

class OutputStream(_message.Message):
    __slots__ = ["include_features", "kafka", "kinesis"]
    INCLUDE_FEATURES_FIELD_NUMBER: ClassVar[int]
    KAFKA_FIELD_NUMBER: ClassVar[int]
    KINESIS_FIELD_NUMBER: ClassVar[int]
    include_features: bool
    kafka: _data_source__client_pb2.KafkaDataSourceArgs
    kinesis: _data_source__client_pb2.KinesisDataSourceArgs
    def __init__(self, include_features: bool = ..., kinesis: Optional[Union[_data_source__client_pb2.KinesisDataSourceArgs, Mapping]] = ..., kafka: Optional[Union[_data_source__client_pb2.KafkaDataSourceArgs, Mapping]] = ...) -> None: ...

class ParamValue(_message.Message):
    __slots__ = ["double_value", "int64_value"]
    DOUBLE_VALUE_FIELD_NUMBER: ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: ClassVar[int]
    double_value: float
    int64_value: int
    def __init__(self, int64_value: Optional[int] = ..., double_value: Optional[float] = ...) -> None: ...

class ParquetConfig(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PromptArgs(_message.Message):
    __slots__ = ["attributes", "environment"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    environment: str
    def __init__(self, environment: Optional[str] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ...) -> None: ...

class RealtimeArgs(_message.Message):
    __slots__ = ["attributes", "environments", "schema"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    environments: _containers.RepeatedScalarFieldContainer[str]
    schema: _spark_schema__client_pb2.SparkSchema
    def __init__(self, schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., environments: Optional[Iterable[str]] = ..., attributes: Optional[Iterable[Union[Attribute, Mapping]]] = ...) -> None: ...

class RedisOnlineStore(_message.Message):
    __slots__ = ["authentication_token", "enabled", "primary_endpoint"]
    AUTHENTICATION_TOKEN_FIELD_NUMBER: ClassVar[int]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    PRIMARY_ENDPOINT_FIELD_NUMBER: ClassVar[int]
    authentication_token: str
    enabled: bool
    primary_endpoint: str
    def __init__(self, primary_endpoint: Optional[str] = ..., authentication_token: Optional[str] = ..., enabled: bool = ...) -> None: ...

class RiftClusterConfig(_message.Message):
    __slots__ = ["instance_type"]
    INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    instance_type: str
    def __init__(self, instance_type: Optional[str] = ...) -> None: ...

class SecondaryKeyOutputColumn(_message.Message):
    __slots__ = ["lifetime_window", "name", "time_window", "time_window_series"]
    LIFETIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_SERIES_FIELD_NUMBER: ClassVar[int]
    lifetime_window: _time_window__client_pb2.LifetimeWindow
    name: str
    time_window: TimeWindow
    time_window_series: TimeWindowSeries
    def __init__(self, time_window: Optional[Union[TimeWindow, Mapping]] = ..., lifetime_window: Optional[Union[_time_window__client_pb2.LifetimeWindow, Mapping]] = ..., time_window_series: Optional[Union[TimeWindowSeries, Mapping]] = ..., name: Optional[str] = ...) -> None: ...

class SparkConfig(_message.Message):
    __slots__ = ["spark_conf", "spark_driver_memory", "spark_driver_memory_overhead", "spark_executor_memory", "spark_executor_memory_overhead"]
    class SparkConfEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    SPARK_CONF_FIELD_NUMBER: ClassVar[int]
    SPARK_DRIVER_MEMORY_FIELD_NUMBER: ClassVar[int]
    SPARK_DRIVER_MEMORY_OVERHEAD_FIELD_NUMBER: ClassVar[int]
    SPARK_EXECUTOR_MEMORY_FIELD_NUMBER: ClassVar[int]
    SPARK_EXECUTOR_MEMORY_OVERHEAD_FIELD_NUMBER: ClassVar[int]
    spark_conf: _containers.ScalarMap[str, str]
    spark_driver_memory: str
    spark_driver_memory_overhead: str
    spark_executor_memory: str
    spark_executor_memory_overhead: str
    def __init__(self, spark_driver_memory: Optional[str] = ..., spark_executor_memory: Optional[str] = ..., spark_driver_memory_overhead: Optional[str] = ..., spark_executor_memory_overhead: Optional[str] = ..., spark_conf: Optional[Mapping[str, str]] = ...) -> None: ...

class TimeWindow(_message.Message):
    __slots__ = ["offset", "window_duration"]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    WINDOW_DURATION_FIELD_NUMBER: ClassVar[int]
    offset: _duration_pb2.Duration
    window_duration: _duration_pb2.Duration
    def __init__(self, window_duration: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., offset: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class TimeWindowSeries(_message.Message):
    __slots__ = ["series_end", "series_start", "step_size", "window_duration"]
    SERIES_END_FIELD_NUMBER: ClassVar[int]
    SERIES_START_FIELD_NUMBER: ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: ClassVar[int]
    WINDOW_DURATION_FIELD_NUMBER: ClassVar[int]
    series_end: _duration_pb2.Duration
    series_start: _duration_pb2.Duration
    step_size: _duration_pb2.Duration
    window_duration: _duration_pb2.Duration
    def __init__(self, series_start: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., series_end: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., step_size: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., window_duration: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class FeatureViewType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class BackfillConfigMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class AggregationLeadingEdge(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class StreamProcessingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class BatchTriggerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FeatureStoreFormatVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
