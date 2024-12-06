from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.dataobs import metric__client_pb2 as _metric__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureExpectation(_message.Message):
    __slots__ = ["alert_message_template", "creation_time", "expression", "input_column_names", "last_update_time", "name"]
    ALERT_MESSAGE_TEMPLATE_FIELD_NUMBER: ClassVar[int]
    CREATION_TIME_FIELD_NUMBER: ClassVar[int]
    EXPRESSION_FIELD_NUMBER: ClassVar[int]
    INPUT_COLUMN_NAMES_FIELD_NUMBER: ClassVar[int]
    LAST_UPDATE_TIME_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    alert_message_template: str
    creation_time: _timestamp_pb2.Timestamp
    expression: str
    input_column_names: _containers.RepeatedScalarFieldContainer[str]
    last_update_time: _timestamp_pb2.Timestamp
    name: str
    def __init__(self, name: Optional[str] = ..., expression: Optional[str] = ..., alert_message_template: Optional[str] = ..., input_column_names: Optional[Iterable[str]] = ..., creation_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., last_update_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class MetricExpectation(_message.Message):
    __slots__ = ["alert_message_template", "creation_time", "display_name", "expression", "input_metrics", "last_update_time", "name"]
    ALERT_MESSAGE_TEMPLATE_FIELD_NUMBER: ClassVar[int]
    CREATION_TIME_FIELD_NUMBER: ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: ClassVar[int]
    EXPRESSION_FIELD_NUMBER: ClassVar[int]
    INPUT_METRICS_FIELD_NUMBER: ClassVar[int]
    LAST_UPDATE_TIME_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    alert_message_template: str
    creation_time: _timestamp_pb2.Timestamp
    display_name: str
    expression: str
    input_metrics: _containers.RepeatedCompositeFieldContainer[_metric__client_pb2.FeatureMetric]
    last_update_time: _timestamp_pb2.Timestamp
    name: str
    def __init__(self, name: Optional[str] = ..., display_name: Optional[str] = ..., expression: Optional[str] = ..., alert_message_template: Optional[str] = ..., input_metrics: Optional[Iterable[Union[_metric__client_pb2.FeatureMetric, Mapping]]] = ..., creation_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., last_update_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...
