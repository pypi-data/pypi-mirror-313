from tecton_proto.common import aws_credentials__client_pb2 as _aws_credentials__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import entity__client_pb2 as _entity__client_pb2
from tecton_proto.data import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.data import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from tecton_proto.dataobs import config__client_pb2 as _config__client_pb2
from tecton_proto.materialization import job_metadata__client_pb2 as _job_metadata__client_pb2
from tecton_proto.materialization import materialization_task__client_pb2 as _materialization_task__client_pb2
from tecton_proto.online_store_writer import config__client_pb2 as _config__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatchTaskInfo(_message.Message):
    __slots__ = ["batch_parameters", "dynamodb_json_output_path", "should_avoid_coalesce", "should_dedupe_online_store_writes"]
    BATCH_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    DYNAMODB_JSON_OUTPUT_PATH_FIELD_NUMBER: ClassVar[int]
    SHOULD_AVOID_COALESCE_FIELD_NUMBER: ClassVar[int]
    SHOULD_DEDUPE_ONLINE_STORE_WRITES_FIELD_NUMBER: ClassVar[int]
    batch_parameters: _materialization_task__client_pb2.BatchMaterializationParameters
    dynamodb_json_output_path: str
    should_avoid_coalesce: bool
    should_dedupe_online_store_writes: bool
    def __init__(self, batch_parameters: Optional[Union[_materialization_task__client_pb2.BatchMaterializationParameters, Mapping]] = ..., dynamodb_json_output_path: Optional[str] = ..., should_dedupe_online_store_writes: bool = ..., should_avoid_coalesce: bool = ...) -> None: ...

class DatasetGenerationTaskInfo(_message.Message):
    __slots__ = ["dataset_generation_parameters"]
    DATASET_GENERATION_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    dataset_generation_parameters: _materialization_task__client_pb2.DatasetGenerationParameters
    def __init__(self, dataset_generation_parameters: Optional[Union[_materialization_task__client_pb2.DatasetGenerationParameters, Mapping]] = ...) -> None: ...

class DeletionTaskInfo(_message.Message):
    __slots__ = ["deletion_parameters"]
    DELETION_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    deletion_parameters: _materialization_task__client_pb2.DeletionParameters
    def __init__(self, deletion_parameters: Optional[Union[_materialization_task__client_pb2.DeletionParameters, Mapping]] = ...) -> None: ...

class DeltaMaintenanceTaskInfo(_message.Message):
    __slots__ = ["delta_maintenance_parameters"]
    DELTA_MAINTENANCE_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    delta_maintenance_parameters: _materialization_task__client_pb2.DeltaMaintenanceParameters
    def __init__(self, delta_maintenance_parameters: Optional[Union[_materialization_task__client_pb2.DeltaMaintenanceParameters, Mapping]] = ...) -> None: ...

class FeatureExportInfo(_message.Message):
    __slots__ = ["feature_export_parameters"]
    FEATURE_EXPORT_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    feature_export_parameters: _materialization_task__client_pb2.FeatureExportParameters
    def __init__(self, feature_export_parameters: Optional[Union[_materialization_task__client_pb2.FeatureExportParameters, Mapping]] = ...) -> None: ...

class IngestTaskInfo(_message.Message):
    __slots__ = ["ingest_parameters"]
    INGEST_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    ingest_parameters: _materialization_task__client_pb2.IngestMaterializationParameters
    def __init__(self, ingest_parameters: Optional[Union[_materialization_task__client_pb2.IngestMaterializationParameters, Mapping]] = ...) -> None: ...

class MaterializationTaskParams(_message.Message):
    __slots__ = ["attempt_id", "batch_task_info", "canary_id", "data_observability_config", "dataset_generation_task_info", "dbfs_credentials_path", "deletion_task_info", "delta_log_table", "delta_maintenance_task_info", "dynamodb_cross_account_external_id", "dynamodb_cross_account_role", "dynamodb_cross_account_role_arn", "dynamodb_table_region", "entities", "feature_export_info", "feature_service", "feature_services", "feature_view", "feature_views", "idempotence_key", "ingest_task_info", "job_metadata_table", "job_metadata_table_type", "kms_key_arn", "materialization_task_id", "offline_store_path", "online_store_writer_config", "plan_id", "secret_access_api_key", "secrets_api_service_url", "spark_job_execution_table", "stream_task_info", "transformations", "use_new_consumption_metrics", "virtual_data_sources"]
    ATTEMPT_ID_FIELD_NUMBER: ClassVar[int]
    BATCH_TASK_INFO_FIELD_NUMBER: ClassVar[int]
    CANARY_ID_FIELD_NUMBER: ClassVar[int]
    DATASET_GENERATION_TASK_INFO_FIELD_NUMBER: ClassVar[int]
    DATA_OBSERVABILITY_CONFIG_FIELD_NUMBER: ClassVar[int]
    DBFS_CREDENTIALS_PATH_FIELD_NUMBER: ClassVar[int]
    DELETION_TASK_INFO_FIELD_NUMBER: ClassVar[int]
    DELTA_LOG_TABLE_FIELD_NUMBER: ClassVar[int]
    DELTA_MAINTENANCE_TASK_INFO_FIELD_NUMBER: ClassVar[int]
    DYNAMODB_CROSS_ACCOUNT_EXTERNAL_ID_FIELD_NUMBER: ClassVar[int]
    DYNAMODB_CROSS_ACCOUNT_ROLE_ARN_FIELD_NUMBER: ClassVar[int]
    DYNAMODB_CROSS_ACCOUNT_ROLE_FIELD_NUMBER: ClassVar[int]
    DYNAMODB_TABLE_REGION_FIELD_NUMBER: ClassVar[int]
    ENTITIES_FIELD_NUMBER: ClassVar[int]
    FEATURE_EXPORT_INFO_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICES_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEWS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    IDEMPOTENCE_KEY_FIELD_NUMBER: ClassVar[int]
    INGEST_TASK_INFO_FIELD_NUMBER: ClassVar[int]
    JOB_METADATA_TABLE_FIELD_NUMBER: ClassVar[int]
    JOB_METADATA_TABLE_TYPE_FIELD_NUMBER: ClassVar[int]
    KMS_KEY_ARN_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_TASK_ID_FIELD_NUMBER: ClassVar[int]
    OFFLINE_STORE_PATH_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_WRITER_CONFIG_FIELD_NUMBER: ClassVar[int]
    PLAN_ID_FIELD_NUMBER: ClassVar[int]
    SECRETS_API_SERVICE_URL_FIELD_NUMBER: ClassVar[int]
    SECRET_ACCESS_API_KEY_FIELD_NUMBER: ClassVar[int]
    SPARK_JOB_EXECUTION_TABLE_FIELD_NUMBER: ClassVar[int]
    STREAM_TASK_INFO_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: ClassVar[int]
    USE_NEW_CONSUMPTION_METRICS_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: ClassVar[int]
    attempt_id: _id__client_pb2.Id
    batch_task_info: BatchTaskInfo
    canary_id: str
    data_observability_config: _config__client_pb2.DataObservabilityMaterializationConfig
    dataset_generation_task_info: DatasetGenerationTaskInfo
    dbfs_credentials_path: str
    deletion_task_info: DeletionTaskInfo
    delta_log_table: str
    delta_maintenance_task_info: DeltaMaintenanceTaskInfo
    dynamodb_cross_account_external_id: str
    dynamodb_cross_account_role: _aws_credentials__client_pb2.AwsIamRole
    dynamodb_cross_account_role_arn: str
    dynamodb_table_region: str
    entities: _containers.RepeatedCompositeFieldContainer[_entity__client_pb2.Entity]
    feature_export_info: FeatureExportInfo
    feature_service: _feature_service__client_pb2.FeatureService
    feature_services: _containers.RepeatedScalarFieldContainer[str]
    feature_view: _feature_view__client_pb2.FeatureView
    feature_views: _containers.RepeatedCompositeFieldContainer[_feature_view__client_pb2.FeatureView]
    idempotence_key: str
    ingest_task_info: IngestTaskInfo
    job_metadata_table: str
    job_metadata_table_type: _job_metadata__client_pb2.JobMetadataTableType
    kms_key_arn: str
    materialization_task_id: str
    offline_store_path: str
    online_store_writer_config: _config__client_pb2.OnlineStoreWriterConfiguration
    plan_id: _id__client_pb2.Id
    secret_access_api_key: str
    secrets_api_service_url: str
    spark_job_execution_table: str
    stream_task_info: StreamTaskInfo
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    use_new_consumption_metrics: bool
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSource]
    def __init__(self, feature_view: Optional[Union[_feature_view__client_pb2.FeatureView, Mapping]] = ..., virtual_data_sources: Optional[Iterable[Union[_virtual_data_source__client_pb2.VirtualDataSource, Mapping]]] = ..., transformations: Optional[Iterable[Union[_transformation__client_pb2.Transformation, Mapping]]] = ..., entities: Optional[Iterable[Union[_entity__client_pb2.Entity, Mapping]]] = ..., feature_services: Optional[Iterable[str]] = ..., feature_views: Optional[Iterable[Union[_feature_view__client_pb2.FeatureView, Mapping]]] = ..., feature_service: Optional[Union[_feature_service__client_pb2.FeatureService, Mapping]] = ..., materialization_task_id: Optional[str] = ..., idempotence_key: Optional[str] = ..., attempt_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., spark_job_execution_table: Optional[str] = ..., job_metadata_table: Optional[str] = ..., delta_log_table: Optional[str] = ..., job_metadata_table_type: Optional[Union[_job_metadata__client_pb2.JobMetadataTableType, str]] = ..., dynamodb_table_region: Optional[str] = ..., online_store_writer_config: Optional[Union[_config__client_pb2.OnlineStoreWriterConfiguration, Mapping]] = ..., dynamodb_cross_account_role: Optional[Union[_aws_credentials__client_pb2.AwsIamRole, Mapping]] = ..., dynamodb_cross_account_role_arn: Optional[str] = ..., dynamodb_cross_account_external_id: Optional[str] = ..., dbfs_credentials_path: Optional[str] = ..., offline_store_path: Optional[str] = ..., use_new_consumption_metrics: bool = ..., canary_id: Optional[str] = ..., data_observability_config: Optional[Union[_config__client_pb2.DataObservabilityMaterializationConfig, Mapping]] = ..., batch_task_info: Optional[Union[BatchTaskInfo, Mapping]] = ..., stream_task_info: Optional[Union[StreamTaskInfo, Mapping]] = ..., ingest_task_info: Optional[Union[IngestTaskInfo, Mapping]] = ..., deletion_task_info: Optional[Union[DeletionTaskInfo, Mapping]] = ..., delta_maintenance_task_info: Optional[Union[DeltaMaintenanceTaskInfo, Mapping]] = ..., feature_export_info: Optional[Union[FeatureExportInfo, Mapping]] = ..., dataset_generation_task_info: Optional[Union[DatasetGenerationTaskInfo, Mapping]] = ..., secrets_api_service_url: Optional[str] = ..., secret_access_api_key: Optional[str] = ..., plan_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., kms_key_arn: Optional[str] = ...) -> None: ...

class SecretMaterializationTaskParams(_message.Message):
    __slots__ = ["secret_service_params"]
    SECRET_SERVICE_PARAMS_FIELD_NUMBER: ClassVar[int]
    secret_service_params: SecretServiceParams
    def __init__(self, secret_service_params: Optional[Union[SecretServiceParams, Mapping]] = ...) -> None: ...

class SecretServiceParams(_message.Message):
    __slots__ = ["secret_access_api_key", "secrets_api_service_url"]
    SECRETS_API_SERVICE_URL_FIELD_NUMBER: ClassVar[int]
    SECRET_ACCESS_API_KEY_FIELD_NUMBER: ClassVar[int]
    secret_access_api_key: str
    secrets_api_service_url: str
    def __init__(self, secrets_api_service_url: Optional[str] = ..., secret_access_api_key: Optional[str] = ...) -> None: ...

class StreamTaskInfo(_message.Message):
    __slots__ = ["stream_parameters", "streaming_checkpoint_path", "streaming_trigger_interval_override"]
    STREAMING_CHECKPOINT_PATH_FIELD_NUMBER: ClassVar[int]
    STREAMING_TRIGGER_INTERVAL_OVERRIDE_FIELD_NUMBER: ClassVar[int]
    STREAM_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    stream_parameters: _materialization_task__client_pb2.StreamMaterializationParameters
    streaming_checkpoint_path: str
    streaming_trigger_interval_override: str
    def __init__(self, stream_parameters: Optional[Union[_materialization_task__client_pb2.StreamMaterializationParameters, Mapping]] = ..., streaming_checkpoint_path: Optional[str] = ..., streaming_trigger_interval_override: Optional[str] = ...) -> None: ...
