from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.spark_common import clusters__client_pb2 as _clusters__client_pb2
from tecton_proto.spark_common import libraries__client_pb2 as _libraries__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
INSTANCE_ALLOCATION_FAILURE: RunTerminationReason
JOB_FINISHED: RunTerminationReason
MANUAL_CANCELATION: RunTerminationReason
NON_CLOUD_FAILURE: RunTerminationReason
RUN_STATUS_CANCELED: RunStatus
RUN_STATUS_ERROR: RunStatus
RUN_STATUS_PENDING: RunStatus
RUN_STATUS_RUNNING: RunStatus
RUN_STATUS_SUBMISSION_ERROR: RunStatus
RUN_STATUS_SUCCESS: RunStatus
RUN_STATUS_TERMINATING: RunStatus
RUN_STATUS_UNKNOWN: RunStatus
SUBMISSION_ERROR: RunTerminationReason
UNKNOWN_TERMINATION_REASON: RunTerminationReason

class GetJobRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    run_id: str
    def __init__(self, run_id: Optional[str] = ...) -> None: ...

class GetJobResponse(_message.Message):
    __slots__ = ["additional_metadata", "details", "job_id", "run_id", "run_page_url", "spark_cluster_id"]
    class AdditionalMetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ADDITIONAL_METADATA_FIELD_NUMBER: ClassVar[int]
    DETAILS_FIELD_NUMBER: ClassVar[int]
    JOB_ID_FIELD_NUMBER: ClassVar[int]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    RUN_PAGE_URL_FIELD_NUMBER: ClassVar[int]
    SPARK_CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    additional_metadata: _containers.ScalarMap[str, str]
    details: RunDetails
    job_id: str
    run_id: str
    run_page_url: str
    spark_cluster_id: str
    def __init__(self, run_id: Optional[str] = ..., job_id: Optional[str] = ..., run_page_url: Optional[str] = ..., spark_cluster_id: Optional[str] = ..., details: Optional[Union[RunDetails, Mapping]] = ..., additional_metadata: Optional[Mapping[str, str]] = ...) -> None: ...

class ListJobRequest(_message.Message):
    __slots__ = ["marker", "offset"]
    MARKER_FIELD_NUMBER: ClassVar[int]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    marker: str
    offset: int
    def __init__(self, offset: Optional[int] = ..., marker: Optional[str] = ...) -> None: ...

class ListJobResponse(_message.Message):
    __slots__ = ["has_more", "marker", "runs"]
    HAS_MORE_FIELD_NUMBER: ClassVar[int]
    MARKER_FIELD_NUMBER: ClassVar[int]
    RUNS_FIELD_NUMBER: ClassVar[int]
    has_more: bool
    marker: str
    runs: _containers.RepeatedCompositeFieldContainer[RunSummary]
    def __init__(self, runs: Optional[Iterable[Union[RunSummary, Mapping]]] = ..., has_more: bool = ..., marker: Optional[str] = ...) -> None: ...

class PythonMaterializationTask(_message.Message):
    __slots__ = ["base_parameters", "materialization_path_uri", "taskType"]
    class TaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class BaseParametersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BASE_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    BATCH: PythonMaterializationTask.TaskType
    DATASET_GENERATION: PythonMaterializationTask.TaskType
    DELETION: PythonMaterializationTask.TaskType
    DELTA_MAINTENANCE: PythonMaterializationTask.TaskType
    FEATURE_EXPORT: PythonMaterializationTask.TaskType
    INGEST: PythonMaterializationTask.TaskType
    MATERIALIZATION_PATH_URI_FIELD_NUMBER: ClassVar[int]
    PLAN_INTEGRATION_TEST_BATCH: PythonMaterializationTask.TaskType
    PLAN_INTEGRATION_TEST_STREAM: PythonMaterializationTask.TaskType
    STREAMING: PythonMaterializationTask.TaskType
    TASKTYPE_FIELD_NUMBER: ClassVar[int]
    base_parameters: _containers.ScalarMap[str, str]
    materialization_path_uri: str
    taskType: PythonMaterializationTask.TaskType
    def __init__(self, materialization_path_uri: Optional[str] = ..., base_parameters: Optional[Mapping[str, str]] = ..., taskType: Optional[Union[PythonMaterializationTask.TaskType, str]] = ...) -> None: ...

class RunDetails(_message.Message):
    __slots__ = ["end_time", "run_status", "start_time", "state_message", "termination_reason", "vendor_termination_reason"]
    END_TIME_FIELD_NUMBER: ClassVar[int]
    RUN_STATUS_FIELD_NUMBER: ClassVar[int]
    START_TIME_FIELD_NUMBER: ClassVar[int]
    STATE_MESSAGE_FIELD_NUMBER: ClassVar[int]
    TERMINATION_REASON_FIELD_NUMBER: ClassVar[int]
    VENDOR_TERMINATION_REASON_FIELD_NUMBER: ClassVar[int]
    end_time: _timestamp_pb2.Timestamp
    run_status: RunStatus
    start_time: _timestamp_pb2.Timestamp
    state_message: str
    termination_reason: RunTerminationReason
    vendor_termination_reason: str
    def __init__(self, run_status: Optional[Union[RunStatus, str]] = ..., termination_reason: Optional[Union[RunTerminationReason, str]] = ..., state_message: Optional[str] = ..., vendor_termination_reason: Optional[str] = ..., start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class RunSummary(_message.Message):
    __slots__ = ["additional_metadata", "resource_locator", "run_id", "run_state"]
    class AdditionalMetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ADDITIONAL_METADATA_FIELD_NUMBER: ClassVar[int]
    RESOURCE_LOCATOR_FIELD_NUMBER: ClassVar[int]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    RUN_STATE_FIELD_NUMBER: ClassVar[int]
    additional_metadata: _containers.ScalarMap[str, str]
    resource_locator: str
    run_id: str
    run_state: str
    def __init__(self, run_id: Optional[str] = ..., run_state: Optional[str] = ..., resource_locator: Optional[str] = ..., additional_metadata: Optional[Mapping[str, str]] = ...) -> None: ...

class StartJobRequest(_message.Message):
    __slots__ = ["existing_cluster", "is_notebook", "libraries", "materialization_task", "new_cluster", "run_name", "timeout_seconds", "use_stepped_materialization"]
    EXISTING_CLUSTER_FIELD_NUMBER: ClassVar[int]
    IS_NOTEBOOK_FIELD_NUMBER: ClassVar[int]
    LIBRARIES_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_TASK_FIELD_NUMBER: ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: ClassVar[int]
    RUN_NAME_FIELD_NUMBER: ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: ClassVar[int]
    USE_STEPPED_MATERIALIZATION_FIELD_NUMBER: ClassVar[int]
    existing_cluster: _clusters__client_pb2.ExistingCluster
    is_notebook: bool
    libraries: _containers.RepeatedCompositeFieldContainer[_libraries__client_pb2.Library]
    materialization_task: PythonMaterializationTask
    new_cluster: _clusters__client_pb2.NewCluster
    run_name: str
    timeout_seconds: int
    use_stepped_materialization: bool
    def __init__(self, new_cluster: Optional[Union[_clusters__client_pb2.NewCluster, Mapping]] = ..., existing_cluster: Optional[Union[_clusters__client_pb2.ExistingCluster, Mapping]] = ..., materialization_task: Optional[Union[PythonMaterializationTask, Mapping]] = ..., run_name: Optional[str] = ..., libraries: Optional[Iterable[Union[_libraries__client_pb2.Library, Mapping]]] = ..., timeout_seconds: Optional[int] = ..., is_notebook: bool = ..., use_stepped_materialization: bool = ...) -> None: ...

class StartJobResponse(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    run_id: str
    def __init__(self, run_id: Optional[str] = ...) -> None: ...

class StopJobRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    run_id: str
    def __init__(self, run_id: Optional[str] = ...) -> None: ...

class RunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RunTerminationReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
