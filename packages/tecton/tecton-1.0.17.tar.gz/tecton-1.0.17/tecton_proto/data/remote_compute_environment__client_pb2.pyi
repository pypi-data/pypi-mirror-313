from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.common import container_image__client_pb2 as _container_image__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
JOB_ENVIRONMENT_REALTIME: JobEnvironment
JOB_ENVIRONMENT_RIFT_BATCH: JobEnvironment
JOB_ENVIRONMENT_RIFT_STREAM: JobEnvironment
JOB_ENVIRONMENT_UNSPECIFIED: JobEnvironment
REMOTE_COMPUTE_TYPE_CORE: RemoteComputeType
REMOTE_COMPUTE_TYPE_CUSTOM: RemoteComputeType
REMOTE_COMPUTE_TYPE_EXTENDED: RemoteComputeType
REMOTE_COMPUTE_TYPE_SNOWPARK_DEPRECATED_DO_NOT_USE: RemoteComputeType
REMOTE_ENVIRONMENT_STATUS_DELETING: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_DELETION_FAILED: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_ERROR: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_PENDING: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_READY: RemoteEnvironmentStatus

class DependentFeatureService(_message.Message):
    __slots__ = ["feature_service_name", "workspace_name"]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    feature_service_name: str
    workspace_name: str
    def __init__(self, workspace_name: Optional[str] = ..., feature_service_name: Optional[str] = ...) -> None: ...

class DependentFeatureView(_message.Message):
    __slots__ = ["feature_view_name", "workspace_name"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    workspace_name: str
    def __init__(self, workspace_name: Optional[str] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class ObjectStoreUploadPart(_message.Message):
    __slots__ = ["s3_upload_part"]
    S3_UPLOAD_PART_FIELD_NUMBER: ClassVar[int]
    s3_upload_part: S3UploadPart
    def __init__(self, s3_upload_part: Optional[Union[S3UploadPart, Mapping]] = ...) -> None: ...

class RealtimeEnvironment(_message.Message):
    __slots__ = ["feature_services", "image_info", "online_provisioned", "remote_function_uri", "tecton_transform_runtime_version"]
    FEATURE_SERVICES_FIELD_NUMBER: ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: ClassVar[int]
    ONLINE_PROVISIONED_FIELD_NUMBER: ClassVar[int]
    REMOTE_FUNCTION_URI_FIELD_NUMBER: ClassVar[int]
    TECTON_TRANSFORM_RUNTIME_VERSION_FIELD_NUMBER: ClassVar[int]
    feature_services: _containers.RepeatedCompositeFieldContainer[DependentFeatureService]
    image_info: _container_image__client_pb2.ContainerImage
    online_provisioned: bool
    remote_function_uri: str
    tecton_transform_runtime_version: str
    def __init__(self, tecton_transform_runtime_version: Optional[str] = ..., image_info: Optional[Union[_container_image__client_pb2.ContainerImage, Mapping]] = ..., remote_function_uri: Optional[str] = ..., feature_services: Optional[Iterable[Union[DependentFeatureService, Mapping]]] = ..., online_provisioned: bool = ...) -> None: ...

class RemoteComputeEnvironment(_message.Message):
    __slots__ = ["created_at", "created_by", "description", "feature_services", "id", "image_info", "name", "python_version", "realtime_job_environment", "requirements", "resolved_requirements", "rift_batch_job_environment", "s3_wheels_location", "sdk_version", "status", "status_details", "supported_job_environments", "type", "updated_at"]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    CREATED_BY_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICES_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: ClassVar[int]
    REALTIME_JOB_ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: ClassVar[int]
    RESOLVED_REQUIREMENTS_FIELD_NUMBER: ClassVar[int]
    RIFT_BATCH_JOB_ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    S3_WHEELS_LOCATION_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    SUPPORTED_JOB_ENVIRONMENTS_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    created_by: _principal__client_pb2.Principal
    description: str
    feature_services: _containers.RepeatedCompositeFieldContainer[DependentFeatureService]
    id: str
    image_info: _container_image__client_pb2.ContainerImage
    name: str
    python_version: str
    realtime_job_environment: RealtimeEnvironment
    requirements: str
    resolved_requirements: str
    rift_batch_job_environment: RiftBatchEnvironment
    s3_wheels_location: str
    sdk_version: str
    status: RemoteEnvironmentStatus
    status_details: str
    supported_job_environments: _containers.RepeatedScalarFieldContainer[JobEnvironment]
    type: RemoteComputeType
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., type: Optional[Union[RemoteComputeType, str]] = ..., status: Optional[Union[RemoteEnvironmentStatus, str]] = ..., image_info: Optional[Union[_container_image__client_pb2.ContainerImage, Mapping]] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., updated_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., created_by: Optional[Union[_principal__client_pb2.Principal, Mapping]] = ..., description: Optional[str] = ..., python_version: Optional[str] = ..., requirements: Optional[str] = ..., resolved_requirements: Optional[str] = ..., s3_wheels_location: Optional[str] = ..., feature_services: Optional[Iterable[Union[DependentFeatureService, Mapping]]] = ..., realtime_job_environment: Optional[Union[RealtimeEnvironment, Mapping]] = ..., rift_batch_job_environment: Optional[Union[RiftBatchEnvironment, Mapping]] = ..., supported_job_environments: Optional[Iterable[Union[JobEnvironment, str]]] = ..., sdk_version: Optional[str] = ..., status_details: Optional[str] = ...) -> None: ...

class RemoteEnvironmentUploadInfo(_message.Message):
    __slots__ = ["environment_id", "s3_upload_info"]
    ENVIRONMENT_ID_FIELD_NUMBER: ClassVar[int]
    S3_UPLOAD_INFO_FIELD_NUMBER: ClassVar[int]
    environment_id: str
    s3_upload_info: S3UploadInfo
    def __init__(self, environment_id: Optional[str] = ..., s3_upload_info: Optional[Union[S3UploadInfo, Mapping]] = ...) -> None: ...

class RiftBatchEnvironment(_message.Message):
    __slots__ = ["cluster_environment_build_id", "image_info", "tecton_materialization_runtime_version"]
    CLUSTER_ENVIRONMENT_BUILD_ID_FIELD_NUMBER: ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_VERSION_FIELD_NUMBER: ClassVar[int]
    cluster_environment_build_id: str
    image_info: _container_image__client_pb2.ContainerImage
    tecton_materialization_runtime_version: str
    def __init__(self, tecton_materialization_runtime_version: Optional[str] = ..., image_info: Optional[Union[_container_image__client_pb2.ContainerImage, Mapping]] = ..., cluster_environment_build_id: Optional[str] = ...) -> None: ...

class S3UploadInfo(_message.Message):
    __slots__ = ["upload_id", "upload_parts"]
    UPLOAD_ID_FIELD_NUMBER: ClassVar[int]
    UPLOAD_PARTS_FIELD_NUMBER: ClassVar[int]
    upload_id: str
    upload_parts: _containers.RepeatedCompositeFieldContainer[S3UploadPart]
    def __init__(self, upload_id: Optional[str] = ..., upload_parts: Optional[Iterable[Union[S3UploadPart, Mapping]]] = ...) -> None: ...

class S3UploadPart(_message.Message):
    __slots__ = ["e_tag", "parent_upload_id", "part_number", "upload_url"]
    E_TAG_FIELD_NUMBER: ClassVar[int]
    PARENT_UPLOAD_ID_FIELD_NUMBER: ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: ClassVar[int]
    e_tag: str
    parent_upload_id: str
    part_number: int
    upload_url: str
    def __init__(self, parent_upload_id: Optional[str] = ..., part_number: Optional[int] = ..., e_tag: Optional[str] = ..., upload_url: Optional[str] = ...) -> None: ...

class JobEnvironment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RemoteEnvironmentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RemoteComputeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
