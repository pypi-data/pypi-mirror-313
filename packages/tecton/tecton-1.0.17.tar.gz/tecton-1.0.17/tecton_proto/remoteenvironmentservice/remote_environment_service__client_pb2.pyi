from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.common import container_image__client_pb2 as _container_image__client_pb2
from tecton_proto.data import remote_compute_environment__client_pb2 as _remote_compute_environment__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompletePackagesUploadRequest(_message.Message):
    __slots__ = ["upload_info"]
    UPLOAD_INFO_FIELD_NUMBER: ClassVar[int]
    upload_info: _remote_compute_environment__client_pb2.RemoteEnvironmentUploadInfo
    def __init__(self, upload_info: Optional[Union[_remote_compute_environment__client_pb2.RemoteEnvironmentUploadInfo, Mapping]] = ...) -> None: ...

class CompletePackagesUploadResponse(_message.Message):
    __slots__ = ["storage_location"]
    STORAGE_LOCATION_FIELD_NUMBER: ClassVar[int]
    storage_location: str
    def __init__(self, storage_location: Optional[str] = ...) -> None: ...

class CreateRemoteEnvironmentRequest(_message.Message):
    __slots__ = ["description", "id", "image_info", "name", "online_provisioned", "python_version", "requirements", "resolved_requirements", "rift_materialization_runtime_version", "s3_wheels_location", "sdk_version", "transform_runtime_version"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    ONLINE_PROVISIONED_FIELD_NUMBER: ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: ClassVar[int]
    RESOLVED_REQUIREMENTS_FIELD_NUMBER: ClassVar[int]
    RIFT_MATERIALIZATION_RUNTIME_VERSION_FIELD_NUMBER: ClassVar[int]
    S3_WHEELS_LOCATION_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    TRANSFORM_RUNTIME_VERSION_FIELD_NUMBER: ClassVar[int]
    description: str
    id: str
    image_info: _container_image__client_pb2.ContainerImage
    name: str
    online_provisioned: bool
    python_version: str
    requirements: str
    resolved_requirements: str
    rift_materialization_runtime_version: str
    s3_wheels_location: str
    sdk_version: str
    transform_runtime_version: str
    def __init__(self, name: Optional[str] = ..., description: Optional[str] = ..., image_info: Optional[Union[_container_image__client_pb2.ContainerImage, Mapping]] = ..., id: Optional[str] = ..., python_version: Optional[str] = ..., requirements: Optional[str] = ..., resolved_requirements: Optional[str] = ..., s3_wheels_location: Optional[str] = ..., transform_runtime_version: Optional[str] = ..., rift_materialization_runtime_version: Optional[str] = ..., sdk_version: Optional[str] = ..., online_provisioned: bool = ...) -> None: ...

class CreateRemoteEnvironmentResponse(_message.Message):
    __slots__ = ["remote_environment"]
    REMOTE_ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    remote_environment: _remote_compute_environment__client_pb2.RemoteComputeEnvironment
    def __init__(self, remote_environment: Optional[Union[_remote_compute_environment__client_pb2.RemoteComputeEnvironment, Mapping]] = ...) -> None: ...

class DeleteRemoteEnvironmentsRequest(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: Optional[Iterable[str]] = ...) -> None: ...

class DeleteRemoteEnvironmentsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDependentFeatureServicesRequest(_message.Message):
    __slots__ = ["environment_id"]
    ENVIRONMENT_ID_FIELD_NUMBER: ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: Optional[str] = ...) -> None: ...

class GetDependentFeatureServicesResponse(_message.Message):
    __slots__ = ["dependent_feature_services"]
    DEPENDENT_FEATURE_SERVICES_FIELD_NUMBER: ClassVar[int]
    dependent_feature_services: _containers.RepeatedCompositeFieldContainer[_remote_compute_environment__client_pb2.DependentFeatureService]
    def __init__(self, dependent_feature_services: Optional[Iterable[Union[_remote_compute_environment__client_pb2.DependentFeatureService, Mapping]]] = ...) -> None: ...

class GetPackagesUploadUrlRequest(_message.Message):
    __slots__ = ["environment_id", "upload_part"]
    ENVIRONMENT_ID_FIELD_NUMBER: ClassVar[int]
    UPLOAD_PART_FIELD_NUMBER: ClassVar[int]
    environment_id: str
    upload_part: _remote_compute_environment__client_pb2.ObjectStoreUploadPart
    def __init__(self, environment_id: Optional[str] = ..., upload_part: Optional[Union[_remote_compute_environment__client_pb2.ObjectStoreUploadPart, Mapping]] = ...) -> None: ...

class GetPackagesUploadUrlResponse(_message.Message):
    __slots__ = ["upload_url"]
    UPLOAD_URL_FIELD_NUMBER: ClassVar[int]
    upload_url: str
    def __init__(self, upload_url: Optional[str] = ...) -> None: ...

class GetRemoteEnvironmentRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: ClassVar[int]
    id: str
    def __init__(self, id: Optional[str] = ...) -> None: ...

class GetRemoteEnvironmentResponse(_message.Message):
    __slots__ = ["remote_environment"]
    REMOTE_ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    remote_environment: _remote_compute_environment__client_pb2.RemoteComputeEnvironment
    def __init__(self, remote_environment: Optional[Union[_remote_compute_environment__client_pb2.RemoteComputeEnvironment, Mapping]] = ...) -> None: ...

class ListRemoteEnvironmentsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListRemoteEnvironmentsResponse(_message.Message):
    __slots__ = ["remote_environments"]
    REMOTE_ENVIRONMENTS_FIELD_NUMBER: ClassVar[int]
    remote_environments: _containers.RepeatedCompositeFieldContainer[_remote_compute_environment__client_pb2.RemoteComputeEnvironment]
    def __init__(self, remote_environments: Optional[Iterable[Union[_remote_compute_environment__client_pb2.RemoteComputeEnvironment, Mapping]]] = ...) -> None: ...

class StartPackagesUploadRequest(_message.Message):
    __slots__ = ["environment_id"]
    ENVIRONMENT_ID_FIELD_NUMBER: ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: Optional[str] = ...) -> None: ...

class StartPackagesUploadResponse(_message.Message):
    __slots__ = ["upload_info"]
    UPLOAD_INFO_FIELD_NUMBER: ClassVar[int]
    upload_info: _remote_compute_environment__client_pb2.RemoteEnvironmentUploadInfo
    def __init__(self, upload_info: Optional[Union[_remote_compute_environment__client_pb2.RemoteEnvironmentUploadInfo, Mapping]] = ...) -> None: ...

class UpdateRemoteEnvironmentRequest(_message.Message):
    __slots__ = ["id", "remote_function_version", "status"]
    ID_FIELD_NUMBER: ClassVar[int]
    REMOTE_FUNCTION_VERSION_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    id: str
    remote_function_version: str
    status: _remote_compute_environment__client_pb2.RemoteEnvironmentStatus
    def __init__(self, id: Optional[str] = ..., remote_function_version: Optional[str] = ..., status: Optional[Union[_remote_compute_environment__client_pb2.RemoteEnvironmentStatus, str]] = ...) -> None: ...

class UpdateRemoteEnvironmentResponse(_message.Message):
    __slots__ = ["remote_environment"]
    REMOTE_ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    remote_environment: _remote_compute_environment__client_pb2.RemoteComputeEnvironment
    def __init__(self, remote_environment: Optional[Union[_remote_compute_environment__client_pb2.RemoteComputeEnvironment, Mapping]] = ...) -> None: ...
