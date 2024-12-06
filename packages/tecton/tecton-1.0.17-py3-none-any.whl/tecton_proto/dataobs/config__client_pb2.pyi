from google.protobuf import duration_pb2 as _duration_pb2
from tecton_proto.dataobs import expectation__client_pb2 as _expectation__client_pb2
from tecton_proto.dataobs import metric__client_pb2 as _metric__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataObservabilityConfig(_message.Message):
    __slots__ = ["feature_expectation_validation_schedule", "feature_expectations", "feature_view_name", "metric_expectations", "metrics", "workspace"]
    FEATURE_EXPECTATIONS_FIELD_NUMBER: ClassVar[int]
    FEATURE_EXPECTATION_VALIDATION_SCHEDULE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    METRICS_FIELD_NUMBER: ClassVar[int]
    METRIC_EXPECTATIONS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_expectation_validation_schedule: str
    feature_expectations: _containers.RepeatedCompositeFieldContainer[_expectation__client_pb2.FeatureExpectation]
    feature_view_name: str
    metric_expectations: _containers.RepeatedCompositeFieldContainer[_expectation__client_pb2.MetricExpectation]
    metrics: _containers.RepeatedCompositeFieldContainer[_metric__client_pb2.Metric]
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., feature_expectation_validation_schedule: Optional[str] = ..., metrics: Optional[Iterable[Union[_metric__client_pb2.Metric, Mapping]]] = ..., feature_expectations: Optional[Iterable[Union[_expectation__client_pb2.FeatureExpectation, Mapping]]] = ..., metric_expectations: Optional[Iterable[Union[_expectation__client_pb2.MetricExpectation, Mapping]]] = ...) -> None: ...

class DataObservabilityMaterializationConfig(_message.Message):
    __slots__ = ["enabled", "metric_interval", "metric_table_name"]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    METRIC_INTERVAL_FIELD_NUMBER: ClassVar[int]
    METRIC_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    enabled: bool
    metric_interval: _duration_pb2.Duration
    metric_table_name: str
    def __init__(self, enabled: bool = ..., metric_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., metric_table_name: Optional[str] = ...) -> None: ...
