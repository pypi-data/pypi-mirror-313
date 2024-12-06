from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
INTERNAL_SPARK_CLUSTER_STATUS_CREATING_CLUSTER: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_HEALTHY: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_NO_CLUSTER: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_UNHEALTHY: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_UNSPECIFIED: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_WAITING_FOR_CLUSTER_TO_START: InternalSparkClusterStatusEnum

class InternalSparkClusterStatus(_message.Message):
    __slots__ = ["cluster_url", "error", "error_message", "status"]
    CLUSTER_URL_FIELD_NUMBER: ClassVar[int]
    ERROR_FIELD_NUMBER: ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    cluster_url: str
    error: bool
    error_message: str
    status: InternalSparkClusterStatusEnum
    def __init__(self, status: Optional[Union[InternalSparkClusterStatusEnum, str]] = ..., error: bool = ..., error_message: Optional[str] = ..., cluster_url: Optional[str] = ...) -> None: ...

class InternalSparkClusterStatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
