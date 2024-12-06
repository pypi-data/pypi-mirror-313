from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.common import compute_mode__client_pb2 as _compute_mode__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.materialization import spark_cluster__client_pb2 as _spark_cluster__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor
TEST_ONLY_MATERIALIZATION_JOB_TYPE_BATCH: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_DATASET_GENERATION: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_INGEST: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_MAINTENANCE: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_STREAM: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_UNSPECIFIED: TestOnlyMaterializationJobType

class CancelDatasetJobRequest(_message.Message):
    __slots__ = ["job_id", "saved_feature_data_frame", "workspace"]
    JOB_ID_FIELD_NUMBER: ClassVar[int]
    SAVED_FEATURE_DATA_FRAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    job_id: str
    saved_feature_data_frame: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., saved_feature_data_frame: Optional[str] = ..., job_id: Optional[str] = ...) -> None: ...

class CancelDatasetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: Optional[Union[MaterializationJob, Mapping]] = ...) -> None: ...

class CancelJobRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "job_id", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    JOB_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service: str
    feature_view: str
    job_id: str
    workspace: str
    def __init__(self, job_id: Optional[str] = ..., workspace: Optional[str] = ..., feature_view: Optional[str] = ..., feature_service: Optional[str] = ...) -> None: ...

class CancelJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: Optional[Union[MaterializationJob, Mapping]] = ...) -> None: ...

class CompleteDataframeUploadRequest(_message.Message):
    __slots__ = ["key", "part_etags", "upload_id", "workspace"]
    class PartEtagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: int
        value: str
        def __init__(self, key: Optional[int] = ..., value: Optional[str] = ...) -> None: ...
    KEY_FIELD_NUMBER: ClassVar[int]
    PART_ETAGS_FIELD_NUMBER: ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    key: str
    part_etags: _containers.ScalarMap[int, str]
    upload_id: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., key: Optional[str] = ..., upload_id: Optional[str] = ..., part_etags: Optional[Mapping[int, str]] = ...) -> None: ...

class CompleteDataframeUploadResponse(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: ClassVar[int]
    key: str
    def __init__(self, key: Optional[str] = ...) -> None: ...

class GetDataframeInfoRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "task_type", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service: str
    feature_view: str
    task_type: _spark_cluster__client_pb2.TaskType
    workspace: str
    def __init__(self, feature_view: Optional[str] = ..., feature_service: Optional[str] = ..., workspace: Optional[str] = ..., task_type: Optional[Union[_spark_cluster__client_pb2.TaskType, str]] = ...) -> None: ...

class GetDataframeInfoResponse(_message.Message):
    __slots__ = ["df_path", "signed_url_for_df_upload"]
    DF_PATH_FIELD_NUMBER: ClassVar[int]
    SIGNED_URL_FOR_DF_UPLOAD_FIELD_NUMBER: ClassVar[int]
    df_path: str
    signed_url_for_df_upload: str
    def __init__(self, df_path: Optional[str] = ..., signed_url_for_df_upload: Optional[str] = ...) -> None: ...

class GetDataframeUploadUrlRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "task_type", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service: str
    feature_view: str
    task_type: _spark_cluster__client_pb2.TaskType
    workspace: str
    def __init__(self, feature_view: Optional[str] = ..., feature_service: Optional[str] = ..., workspace: Optional[str] = ..., task_type: Optional[Union[_spark_cluster__client_pb2.TaskType, str]] = ...) -> None: ...

class GetDataframeUploadUrlResponse(_message.Message):
    __slots__ = ["key", "upload_id"]
    KEY_FIELD_NUMBER: ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: ClassVar[int]
    key: str
    upload_id: str
    def __init__(self, key: Optional[str] = ..., upload_id: Optional[str] = ...) -> None: ...

class GetDatasetJobRequest(_message.Message):
    __slots__ = ["job_id", "saved_feature_data_frame", "workspace"]
    JOB_ID_FIELD_NUMBER: ClassVar[int]
    SAVED_FEATURE_DATA_FRAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    job_id: str
    saved_feature_data_frame: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., saved_feature_data_frame: Optional[str] = ..., job_id: Optional[str] = ...) -> None: ...

class GetDatasetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: Optional[Union[MaterializationJob, Mapping]] = ...) -> None: ...

class GetJobRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "job_id", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    JOB_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service: str
    feature_view: str
    job_id: str
    workspace: str
    def __init__(self, job_id: Optional[str] = ..., workspace: Optional[str] = ..., feature_view: Optional[str] = ..., feature_service: Optional[str] = ...) -> None: ...

class GetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: Optional[Union[MaterializationJob, Mapping]] = ...) -> None: ...

class GetLatestReadyTimeRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service: str
    feature_view: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view: Optional[str] = ..., feature_service: Optional[str] = ...) -> None: ...

class GetLatestReadyTimeResponse(_message.Message):
    __slots__ = ["offline_latest_ready_time", "online_latest_ready_time"]
    OFFLINE_LATEST_READY_TIME_FIELD_NUMBER: ClassVar[int]
    ONLINE_LATEST_READY_TIME_FIELD_NUMBER: ClassVar[int]
    offline_latest_ready_time: _timestamp_pb2.Timestamp
    online_latest_ready_time: _timestamp_pb2.Timestamp
    def __init__(self, online_latest_ready_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., offline_latest_ready_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class IngestDataframeFromS3Request(_message.Message):
    __slots__ = ["df_path", "feature_view", "use_tecton_managed_retries", "workspace"]
    DF_PATH_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    USE_TECTON_MANAGED_RETRIES_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    df_path: str
    feature_view: str
    use_tecton_managed_retries: bool
    workspace: str
    def __init__(self, feature_view: Optional[str] = ..., df_path: Optional[str] = ..., workspace: Optional[str] = ..., use_tecton_managed_retries: bool = ...) -> None: ...

class IngestDataframeFromS3Response(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: Optional[Union[MaterializationJob, Mapping]] = ...) -> None: ...

class JobAttempt(_message.Message):
    __slots__ = ["created_at", "id", "run_url", "state", "updated_at"]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    RUN_URL_FIELD_NUMBER: ClassVar[int]
    STATE_FIELD_NUMBER: ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    id: str
    run_url: str
    state: str
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: Optional[str] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., updated_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., state: Optional[str] = ..., run_url: Optional[str] = ...) -> None: ...

class ListJobsRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service: str
    feature_view: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view: Optional[str] = ..., feature_service: Optional[str] = ...) -> None: ...

class ListJobsResponse(_message.Message):
    __slots__ = ["jobs"]
    JOBS_FIELD_NUMBER: ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[MaterializationJob]
    def __init__(self, jobs: Optional[Iterable[Union[MaterializationJob, Mapping]]] = ...) -> None: ...

class MaterializationJob(_message.Message):
    __slots__ = ["attempts", "created_at", "end_time", "feature_service", "feature_view", "id", "ingest_path", "job_type", "next_attempt_at", "offline", "online", "saved_feature_data_frame", "start_time", "state", "updated_at", "workspace"]
    ATTEMPTS_FIELD_NUMBER: ClassVar[int]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    INGEST_PATH_FIELD_NUMBER: ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: ClassVar[int]
    NEXT_ATTEMPT_AT_FIELD_NUMBER: ClassVar[int]
    OFFLINE_FIELD_NUMBER: ClassVar[int]
    ONLINE_FIELD_NUMBER: ClassVar[int]
    SAVED_FEATURE_DATA_FRAME_FIELD_NUMBER: ClassVar[int]
    START_TIME_FIELD_NUMBER: ClassVar[int]
    STATE_FIELD_NUMBER: ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    attempts: _containers.RepeatedCompositeFieldContainer[JobAttempt]
    created_at: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    feature_service: str
    feature_view: str
    id: str
    ingest_path: str
    job_type: str
    next_attempt_at: _timestamp_pb2.Timestamp
    offline: bool
    online: bool
    saved_feature_data_frame: str
    start_time: _timestamp_pb2.Timestamp
    state: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, id: Optional[str] = ..., workspace: Optional[str] = ..., feature_view: Optional[str] = ..., feature_service: Optional[str] = ..., saved_feature_data_frame: Optional[str] = ..., start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., updated_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., state: Optional[str] = ..., attempts: Optional[Iterable[Union[JobAttempt, Mapping]]] = ..., next_attempt_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., online: bool = ..., offline: bool = ..., job_type: Optional[str] = ..., ingest_path: Optional[str] = ...) -> None: ...

class MaterializationJobRequest(_message.Message):
    __slots__ = ["end_time", "feature_view", "offline", "online", "overwrite", "start_time", "use_tecton_managed_retries", "workspace"]
    END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    OFFLINE_FIELD_NUMBER: ClassVar[int]
    ONLINE_FIELD_NUMBER: ClassVar[int]
    OVERWRITE_FIELD_NUMBER: ClassVar[int]
    START_TIME_FIELD_NUMBER: ClassVar[int]
    USE_TECTON_MANAGED_RETRIES_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    end_time: _timestamp_pb2.Timestamp
    feature_view: str
    offline: bool
    online: bool
    overwrite: bool
    start_time: _timestamp_pb2.Timestamp
    use_tecton_managed_retries: bool
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view: Optional[str] = ..., start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., online: bool = ..., offline: bool = ..., use_tecton_managed_retries: bool = ..., overwrite: bool = ...) -> None: ...

class MaterializationJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: Optional[Union[MaterializationJob, Mapping]] = ...) -> None: ...

class StartDatasetJobRequest(_message.Message):
    __slots__ = ["cluster_config", "compute_mode", "dataset_name", "datetime_range", "environment", "expected_schema", "extra_config", "feature_service_id", "feature_view_id", "from_source", "spine", "tecton_runtime", "workspace"]
    class DateTimeRangeInput(_message.Message):
        __slots__ = ["end", "entities_path", "max_lookback", "start"]
        END_FIELD_NUMBER: ClassVar[int]
        ENTITIES_PATH_FIELD_NUMBER: ClassVar[int]
        MAX_LOOKBACK_FIELD_NUMBER: ClassVar[int]
        START_FIELD_NUMBER: ClassVar[int]
        end: _timestamp_pb2.Timestamp
        entities_path: str
        max_lookback: _timestamp_pb2.Timestamp
        start: _timestamp_pb2.Timestamp
        def __init__(self, start: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., end: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., max_lookback: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., entities_path: Optional[str] = ...) -> None: ...
    class ExtraConfigEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    class SpineInput(_message.Message):
        __slots__ = ["column_names", "path", "timestamp_key"]
        COLUMN_NAMES_FIELD_NUMBER: ClassVar[int]
        PATH_FIELD_NUMBER: ClassVar[int]
        TIMESTAMP_KEY_FIELD_NUMBER: ClassVar[int]
        column_names: _containers.RepeatedScalarFieldContainer[str]
        path: str
        timestamp_key: str
        def __init__(self, path: Optional[str] = ..., timestamp_key: Optional[str] = ..., column_names: Optional[Iterable[str]] = ...) -> None: ...
    CLUSTER_CONFIG_FIELD_NUMBER: ClassVar[int]
    COMPUTE_MODE_FIELD_NUMBER: ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: ClassVar[int]
    DATETIME_RANGE_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    EXPECTED_SCHEMA_FIELD_NUMBER: ClassVar[int]
    EXTRA_CONFIG_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FROM_SOURCE_FIELD_NUMBER: ClassVar[int]
    SPINE_FIELD_NUMBER: ClassVar[int]
    TECTON_RUNTIME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    cluster_config: _feature_view__client_pb2.ClusterConfig
    compute_mode: _compute_mode__client_pb2.BatchComputeMode
    dataset_name: str
    datetime_range: StartDatasetJobRequest.DateTimeRangeInput
    environment: str
    expected_schema: _schema__client_pb2.Schema
    extra_config: _containers.ScalarMap[str, str]
    feature_service_id: _id__client_pb2.Id
    feature_view_id: _id__client_pb2.Id
    from_source: bool
    spine: StartDatasetJobRequest.SpineInput
    tecton_runtime: str
    workspace: str
    def __init__(self, compute_mode: Optional[Union[_compute_mode__client_pb2.BatchComputeMode, str]] = ..., from_source: bool = ..., workspace: Optional[str] = ..., feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., spine: Optional[Union[StartDatasetJobRequest.SpineInput, Mapping]] = ..., datetime_range: Optional[Union[StartDatasetJobRequest.DateTimeRangeInput, Mapping]] = ..., dataset_name: Optional[str] = ..., cluster_config: Optional[Union[_feature_view__client_pb2.ClusterConfig, Mapping]] = ..., tecton_runtime: Optional[str] = ..., environment: Optional[str] = ..., extra_config: Optional[Mapping[str, str]] = ..., expected_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ...) -> None: ...

class StartDatasetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: Optional[Union[MaterializationJob, Mapping]] = ...) -> None: ...

class TestOnlyCompleteOnlineTableRequest(_message.Message):
    __slots__ = ["feature_view_name", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class TestOnlyCompleteOnlineTableResponse(_message.Message):
    __slots__ = ["table_name"]
    TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    table_name: str
    def __init__(self, table_name: Optional[str] = ...) -> None: ...

class TestOnlyGetDatasetGenerationTaskParamsRequest(_message.Message):
    __slots__ = ["start_dataset_job_request"]
    START_DATASET_JOB_REQUEST_FIELD_NUMBER: ClassVar[int]
    start_dataset_job_request: StartDatasetJobRequest
    def __init__(self, start_dataset_job_request: Optional[Union[StartDatasetJobRequest, Mapping]] = ...) -> None: ...

class TestOnlyGetMaterializationTaskParamsRequest(_message.Message):
    __slots__ = ["df_path", "disable_offline", "disable_online", "feature_view_name", "job_end_time", "job_start_time", "job_type", "workspace"]
    DF_PATH_FIELD_NUMBER: ClassVar[int]
    DISABLE_OFFLINE_FIELD_NUMBER: ClassVar[int]
    DISABLE_ONLINE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    JOB_END_TIME_FIELD_NUMBER: ClassVar[int]
    JOB_START_TIME_FIELD_NUMBER: ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    df_path: str
    disable_offline: bool
    disable_online: bool
    feature_view_name: str
    job_end_time: _timestamp_pb2.Timestamp
    job_start_time: _timestamp_pb2.Timestamp
    job_type: TestOnlyMaterializationJobType
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., job_type: Optional[Union[TestOnlyMaterializationJobType, str]] = ..., disable_offline: bool = ..., disable_online: bool = ..., job_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., job_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., df_path: Optional[str] = ...) -> None: ...

class TestOnlyGetMaterializationTaskParamsResponse(_message.Message):
    __slots__ = ["encoded_materialization_params"]
    ENCODED_MATERIALIZATION_PARAMS_FIELD_NUMBER: ClassVar[int]
    encoded_materialization_params: str
    def __init__(self, encoded_materialization_params: Optional[str] = ...) -> None: ...

class TestOnlyOnlineTableNameRequest(_message.Message):
    __slots__ = ["feature_view_name", "watermark", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    WATERMARK_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    watermark: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., watermark: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class TestOnlyOnlineTableNameResponse(_message.Message):
    __slots__ = ["table_name"]
    TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    table_name: str
    def __init__(self, table_name: Optional[str] = ...) -> None: ...

class TestOnlyWriteFeatureServerConfigRequest(_message.Message):
    __slots__ = ["absolute_filepath"]
    ABSOLUTE_FILEPATH_FIELD_NUMBER: ClassVar[int]
    absolute_filepath: str
    def __init__(self, absolute_filepath: Optional[str] = ...) -> None: ...

class TestOnlyWriteFeatureServerConfigResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UploadDataframePartRequest(_message.Message):
    __slots__ = ["key", "parent_upload_id", "part_number", "workspace"]
    KEY_FIELD_NUMBER: ClassVar[int]
    PARENT_UPLOAD_ID_FIELD_NUMBER: ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    key: str
    parent_upload_id: str
    part_number: int
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., key: Optional[str] = ..., parent_upload_id: Optional[str] = ..., part_number: Optional[int] = ...) -> None: ...

class UploadDataframePartResponse(_message.Message):
    __slots__ = ["upload_url"]
    UPLOAD_URL_FIELD_NUMBER: ClassVar[int]
    upload_url: str
    def __init__(self, upload_url: Optional[str] = ...) -> None: ...

class TestOnlyMaterializationJobType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
