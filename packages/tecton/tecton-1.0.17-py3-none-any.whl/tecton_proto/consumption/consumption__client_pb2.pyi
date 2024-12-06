from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

BATCH_MATERIALIZATION: JobType
BILLABLE_USAGE_OPTIONS_FIELD_NUMBER: ClassVar[int]
COMPUTE_TYPE_UNSPECIFIED: ComputeType
CONSUMPTION_TYPE_UNSPECIFIED: ConsumptionType
CONSUMPTION_UNITS_UNSPECIFIED: ConsumptionUnit
DATABRICKS: ComputeType
DATASET_GENERATION: JobType
DESCRIPTOR: _descriptor.FileDescriptor
EMR: ComputeType
ENTITY_DELETION: JobType
FEATURE_PUBLISH: JobType
FEATURE_SERVER_NODE_DURATION: ConsumptionType
FEATURE_SERVER_NODE_HOURS: ConsumptionUnit
FEATURE_SERVER_READS: ConsumptionType
FEATURE_SERVICE_ONLINE_REQUESTS: ConsumptionUnit
FEATURE_SERVICE_ONLINE_VECTORS_SERVED: ConsumptionUnit
FEATURE_SERVICE_VECTORS_SERVED: ConsumptionUnit
FEATURE_TABLE_INGEST: JobType
FEATURE_VIEW_ONLINE_READS: ConsumptionUnit
INGEST_API_COMPUTE: ConsumptionType
JOB_TYPE_UNSPECIFIED: JobType
MATERIALIZATION_JOB_WRITES: ConsumptionType
OFFLINE_WRITE_ROWS: ConsumptionUnit
OFFLINE_WRITE_VALUES: ConsumptionUnit
ONLINE_WRITE_ROWS: ConsumptionUnit
REAL_TIME_COMPUTE_DURATION_HOURS: ConsumptionUnit
REAL_TIME_JOB_COMPUTE: ConsumptionType
REQUIREMENT_NOT_REQUIRED: Requirement
REQUIREMENT_REQUIRED: Requirement
REQUIREMENT_UNSPECIFIED: Requirement
RIFT: ComputeType
RIFT_MATERIALIZATION_JOB_COMPUTE: ConsumptionType
SPARK_MATERIALIZATION_JOB_COMPUTE: ConsumptionType
STREAM_MATERIALIZATION: JobType
TECTON_JOB_COMPUTE_HOURS: ConsumptionUnit
VISIBILITY_UNSPECIFIED: Visibility
VISIBILITY_VISIBLE: Visibility
billable_usage_options: _descriptor.FieldDescriptor

class BillableUsageOptions(_message.Message):
    __slots__ = ["required", "visibility"]
    REQUIRED_FIELD_NUMBER: ClassVar[int]
    VISIBILITY_FIELD_NUMBER: ClassVar[int]
    required: Requirement
    visibility: Visibility
    def __init__(self, visibility: Optional[Union[Visibility, str]] = ..., required: Optional[Union[Requirement, str]] = ...) -> None: ...

class ConsumptionInfo(_message.Message):
    __slots__ = ["details", "feature_view_id", "feature_view_name", "metric", "online_read_aws_region", "source_id", "time_bucket_start", "units_consumed", "workspace"]
    class DetailsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    DETAILS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    METRIC_FIELD_NUMBER: ClassVar[int]
    ONLINE_READ_AWS_REGION_FIELD_NUMBER: ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: ClassVar[int]
    TIME_BUCKET_START_FIELD_NUMBER: ClassVar[int]
    UNITS_CONSUMED_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    details: _containers.ScalarMap[str, str]
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    metric: str
    online_read_aws_region: str
    source_id: str
    time_bucket_start: _timestamp_pb2.Timestamp
    units_consumed: int
    workspace: str
    def __init__(self, time_bucket_start: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., units_consumed: Optional[int] = ..., metric: Optional[str] = ..., details: Optional[Mapping[str, str]] = ..., source_id: Optional[str] = ..., feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_view_name: Optional[str] = ..., workspace: Optional[str] = ..., online_read_aws_region: Optional[str] = ...) -> None: ...

class ConsumptionRecord(_message.Message):
    __slots__ = ["account_name", "collection_timestamp", "duration", "feature_server_node_hours_metadata", "feature_server_reads_metadata", "ingest_api_compute_hours_metadata", "materialization_job_offline_writes_metadata", "materialization_job_online_writes_metadata", "quantity", "real_time_compute_metadata", "tecton_job_compute_hours_metadata", "timestamp", "unit"]
    ACCOUNT_NAME_FIELD_NUMBER: ClassVar[int]
    COLLECTION_TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    DURATION_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_NODE_HOURS_METADATA_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_READS_METADATA_FIELD_NUMBER: ClassVar[int]
    INGEST_API_COMPUTE_HOURS_METADATA_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_JOB_OFFLINE_WRITES_METADATA_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_JOB_ONLINE_WRITES_METADATA_FIELD_NUMBER: ClassVar[int]
    QUANTITY_FIELD_NUMBER: ClassVar[int]
    REAL_TIME_COMPUTE_METADATA_FIELD_NUMBER: ClassVar[int]
    TECTON_JOB_COMPUTE_HOURS_METADATA_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    UNIT_FIELD_NUMBER: ClassVar[int]
    account_name: str
    collection_timestamp: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    feature_server_node_hours_metadata: FeatureServerNodeHoursMetadata
    feature_server_reads_metadata: FeatureServerReadsMetadata
    ingest_api_compute_hours_metadata: IngestApiComputeHoursMetadata
    materialization_job_offline_writes_metadata: MaterializationJobOfflineWritesMetadata
    materialization_job_online_writes_metadata: MaterializationJobOnlineWritesMetadata
    quantity: float
    real_time_compute_metadata: RealTimeComputeMetadata
    tecton_job_compute_hours_metadata: TectonJobComputeHoursMetadata
    timestamp: _timestamp_pb2.Timestamp
    unit: ConsumptionUnit
    def __init__(self, timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., collection_timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., duration: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., account_name: Optional[str] = ..., materialization_job_online_writes_metadata: Optional[Union[MaterializationJobOnlineWritesMetadata, Mapping]] = ..., materialization_job_offline_writes_metadata: Optional[Union[MaterializationJobOfflineWritesMetadata, Mapping]] = ..., feature_server_node_hours_metadata: Optional[Union[FeatureServerNodeHoursMetadata, Mapping]] = ..., feature_server_reads_metadata: Optional[Union[FeatureServerReadsMetadata, Mapping]] = ..., real_time_compute_metadata: Optional[Union[RealTimeComputeMetadata, Mapping]] = ..., tecton_job_compute_hours_metadata: Optional[Union[TectonJobComputeHoursMetadata, Mapping]] = ..., ingest_api_compute_hours_metadata: Optional[Union[IngestApiComputeHoursMetadata, Mapping]] = ..., quantity: Optional[float] = ..., unit: Optional[Union[ConsumptionUnit, str]] = ...) -> None: ...

class EnrichedConsumptionInfo(_message.Message):
    __slots__ = ["consumption_info", "feature_view_id", "feature_view_name", "feature_view_workspace"]
    CONSUMPTION_INFO_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_WORKSPACE_FIELD_NUMBER: ClassVar[int]
    consumption_info: ConsumptionInfo
    feature_view_id: str
    feature_view_name: str
    feature_view_workspace: str
    def __init__(self, consumption_info: Optional[Union[ConsumptionInfo, Mapping]] = ..., feature_view_workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., feature_view_id: Optional[str] = ...) -> None: ...

class FeatureServerNodeHoursMetadata(_message.Message):
    __slots__ = ["pod_count", "pod_cpu", "pod_memory_mib", "region"]
    POD_COUNT_FIELD_NUMBER: ClassVar[int]
    POD_CPU_FIELD_NUMBER: ClassVar[int]
    POD_MEMORY_MIB_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    pod_count: int
    pod_cpu: float
    pod_memory_mib: int
    region: str
    def __init__(self, region: Optional[str] = ..., pod_cpu: Optional[float] = ..., pod_memory_mib: Optional[int] = ..., pod_count: Optional[int] = ...) -> None: ...

class FeatureServerReadsMetadata(_message.Message):
    __slots__ = ["tecton_object_id", "tecton_object_name", "workspace"]
    TECTON_OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., tecton_object_name: Optional[str] = ..., tecton_object_id: Optional[str] = ...) -> None: ...

class IngestApiComputeHoursMetadata(_message.Message):
    __slots__ = ["compute_type", "job_type", "memory_mib", "operation", "tags", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COMPUTE_TYPE_FIELD_NUMBER: ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: ClassVar[int]
    MEMORY_MIB_FIELD_NUMBER: ClassVar[int]
    OPERATION_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    compute_type: ComputeType
    job_type: JobType
    memory_mib: int
    operation: str
    tags: _containers.ScalarMap[str, str]
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, compute_type: Optional[Union[ComputeType, str]] = ..., job_type: Optional[Union[JobType, str]] = ..., operation: Optional[str] = ..., memory_mib: Optional[int] = ..., workspace: Optional[str] = ..., workspace_state_id: Optional[str] = ..., tecton_object_name: Optional[str] = ..., tecton_object_id: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class MaterializationJobOfflineWritesMetadata(_message.Message):
    __slots__ = ["tags", "tecton_job_id", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    TAGS_FIELD_NUMBER: ClassVar[int]
    TECTON_JOB_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    tags: _containers.ScalarMap[str, str]
    tecton_job_id: str
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, tecton_job_id: Optional[str] = ..., workspace: Optional[str] = ..., workspace_state_id: Optional[str] = ..., tecton_object_name: Optional[str] = ..., tecton_object_id: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class MaterializationJobOnlineWritesMetadata(_message.Message):
    __slots__ = ["online_store_type", "tags", "tecton_job_id", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ONLINE_STORE_TYPE_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TECTON_JOB_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    online_store_type: str
    tags: _containers.ScalarMap[str, str]
    tecton_job_id: str
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, online_store_type: Optional[str] = ..., tecton_job_id: Optional[str] = ..., workspace: Optional[str] = ..., workspace_state_id: Optional[str] = ..., tecton_object_name: Optional[str] = ..., tecton_object_id: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class RealTimeComputeMetadata(_message.Message):
    __slots__ = ["memory_allocated_mib", "tags", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    MEMORY_ALLOCATED_MIB_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    memory_allocated_mib: int
    tags: _containers.ScalarMap[str, str]
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, memory_allocated_mib: Optional[int] = ..., workspace: Optional[str] = ..., workspace_state_id: Optional[str] = ..., tecton_object_name: Optional[str] = ..., tecton_object_id: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class TectonJobComputeHoursMetadata(_message.Message):
    __slots__ = ["compute_type", "instance_type", "job_type", "num_workers", "region", "tags", "tecton_job_id", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COMPUTE_TYPE_FIELD_NUMBER: ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: ClassVar[int]
    NUM_WORKERS_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TECTON_JOB_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    compute_type: ComputeType
    instance_type: str
    job_type: JobType
    num_workers: int
    region: str
    tags: _containers.ScalarMap[str, str]
    tecton_job_id: str
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, tecton_job_id: Optional[str] = ..., instance_type: Optional[str] = ..., region: Optional[str] = ..., num_workers: Optional[int] = ..., compute_type: Optional[Union[ComputeType, str]] = ..., job_type: Optional[Union[JobType, str]] = ..., workspace: Optional[str] = ..., workspace_state_id: Optional[str] = ..., tecton_object_name: Optional[str] = ..., tecton_object_id: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class JobType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ComputeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ConsumptionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ConsumptionUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Visibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Requirement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
