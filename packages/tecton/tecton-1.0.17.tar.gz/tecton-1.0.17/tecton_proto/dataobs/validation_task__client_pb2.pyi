from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import fco_locator__client_pb2 as _fco_locator__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.dataobs import expectation__client_pb2 as _expectation__client_pb2
from tecton_proto.dataobs import validation__client_pb2 as _validation__client_pb2
from tecton_proto.dataobs import validation_task_params__client_pb2 as _validation_task_params__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
VALIDATION_TASK_TYPE_BATCH_METRICS: ValidationTaskType
VALIDATION_TASK_TYPE_UNKNOWN: ValidationTaskType

class ValidationTask(_message.Message):
    __slots__ = ["dynamo_data_source", "feature_end_time", "feature_start_time", "feature_view_locator", "metric_expectations", "s3_data_source", "task_type", "timeout", "validation_job_id"]
    DYNAMO_DATA_SOURCE_FIELD_NUMBER: ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_LOCATOR_FIELD_NUMBER: ClassVar[int]
    METRIC_EXPECTATIONS_FIELD_NUMBER: ClassVar[int]
    S3_DATA_SOURCE_FIELD_NUMBER: ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: ClassVar[int]
    TIMEOUT_FIELD_NUMBER: ClassVar[int]
    VALIDATION_JOB_ID_FIELD_NUMBER: ClassVar[int]
    dynamo_data_source: _validation_task_params__client_pb2.DynamoDataSource
    feature_end_time: _timestamp_pb2.Timestamp
    feature_start_time: _timestamp_pb2.Timestamp
    feature_view_locator: _fco_locator__client_pb2.IdFcoLocator
    metric_expectations: _containers.RepeatedCompositeFieldContainer[_expectation__client_pb2.MetricExpectation]
    s3_data_source: _validation_task_params__client_pb2.S3DataSource
    task_type: ValidationTaskType
    timeout: _duration_pb2.Duration
    validation_job_id: _id__client_pb2.Id
    def __init__(self, validation_job_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_view_locator: Optional[Union[_fco_locator__client_pb2.IdFcoLocator, Mapping]] = ..., metric_expectations: Optional[Iterable[Union[_expectation__client_pb2.MetricExpectation, Mapping]]] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., task_type: Optional[Union[ValidationTaskType, str]] = ..., timeout: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., dynamo_data_source: Optional[Union[_validation_task_params__client_pb2.DynamoDataSource, Mapping]] = ..., s3_data_source: Optional[Union[_validation_task_params__client_pb2.S3DataSource, Mapping]] = ...) -> None: ...

class ValidationTaskMetrics(_message.Message):
    __slots__ = ["feature_rows_read", "metric_rows_read", "query_execution_times"]
    FEATURE_ROWS_READ_FIELD_NUMBER: ClassVar[int]
    METRIC_ROWS_READ_FIELD_NUMBER: ClassVar[int]
    QUERY_EXECUTION_TIMES_FIELD_NUMBER: ClassVar[int]
    feature_rows_read: int
    metric_rows_read: int
    query_execution_times: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    def __init__(self, metric_rows_read: Optional[int] = ..., feature_rows_read: Optional[int] = ..., query_execution_times: Optional[Iterable[Union[_duration_pb2.Duration, Mapping]]] = ...) -> None: ...

class ValidationTaskResult(_message.Message):
    __slots__ = ["feature_end_time", "feature_package_id", "feature_start_time", "metrics", "results", "validation_job_id", "validation_time", "workspace"]
    FEATURE_END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    METRICS_FIELD_NUMBER: ClassVar[int]
    RESULTS_FIELD_NUMBER: ClassVar[int]
    VALIDATION_JOB_ID_FIELD_NUMBER: ClassVar[int]
    VALIDATION_TIME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_end_time: _timestamp_pb2.Timestamp
    feature_package_id: _id__client_pb2.Id
    feature_start_time: _timestamp_pb2.Timestamp
    metrics: ValidationTaskMetrics
    results: _containers.RepeatedCompositeFieldContainer[_validation__client_pb2.ExpectationResult]
    validation_job_id: _id__client_pb2.Id
    validation_time: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_package_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., validation_job_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., results: Optional[Iterable[Union[_validation__client_pb2.ExpectationResult, Mapping]]] = ..., metrics: Optional[Union[ValidationTaskMetrics, Mapping]] = ..., validation_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class ValidationTaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
