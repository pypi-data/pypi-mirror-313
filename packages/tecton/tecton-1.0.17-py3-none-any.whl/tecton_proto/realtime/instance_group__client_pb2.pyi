from tecton_proto.common import container_image__client_pb2 as _container_image__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AWSInstanceGroup(_message.Message):
    __slots__ = ["ami_image_id", "autoscaling_group_arn", "autoscaling_group_name", "health_check_path", "iam_instance_profile_arn", "instance_type", "launch_template_id", "port", "region", "security_group_ids", "subnet_ids"]
    AMI_IMAGE_ID_FIELD_NUMBER: ClassVar[int]
    AUTOSCALING_GROUP_ARN_FIELD_NUMBER: ClassVar[int]
    AUTOSCALING_GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    HEALTH_CHECK_PATH_FIELD_NUMBER: ClassVar[int]
    IAM_INSTANCE_PROFILE_ARN_FIELD_NUMBER: ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    LAUNCH_TEMPLATE_ID_FIELD_NUMBER: ClassVar[int]
    PORT_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    SECURITY_GROUP_IDS_FIELD_NUMBER: ClassVar[int]
    SUBNET_IDS_FIELD_NUMBER: ClassVar[int]
    ami_image_id: str
    autoscaling_group_arn: str
    autoscaling_group_name: str
    health_check_path: str
    iam_instance_profile_arn: str
    instance_type: str
    launch_template_id: str
    port: int
    region: str
    security_group_ids: _containers.RepeatedScalarFieldContainer[str]
    subnet_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, autoscaling_group_arn: Optional[str] = ..., autoscaling_group_name: Optional[str] = ..., region: Optional[str] = ..., port: Optional[int] = ..., health_check_path: Optional[str] = ..., instance_type: Optional[str] = ..., ami_image_id: Optional[str] = ..., iam_instance_profile_arn: Optional[str] = ..., security_group_ids: Optional[Iterable[str]] = ..., subnet_ids: Optional[Iterable[str]] = ..., launch_template_id: Optional[str] = ...) -> None: ...

class AWSInstanceGroupUpdateConfig(_message.Message):
    __slots__ = ["ami_image_id", "instance_type"]
    AMI_IMAGE_ID_FIELD_NUMBER: ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    ami_image_id: str
    instance_type: str
    def __init__(self, instance_type: Optional[str] = ..., ami_image_id: Optional[str] = ...) -> None: ...

class AWSTargetGroup(_message.Message):
    __slots__ = ["arn", "instance_group", "name"]
    ARN_FIELD_NUMBER: ClassVar[int]
    INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    arn: str
    instance_group: AWSInstanceGroup
    name: str
    def __init__(self, arn: Optional[str] = ..., name: Optional[str] = ..., instance_group: Optional[Union[AWSInstanceGroup, Mapping]] = ...) -> None: ...

class CapacityConfig(_message.Message):
    __slots__ = ["autoscaling_enabled", "desired_nodes", "max_nodes", "min_nodes"]
    AUTOSCALING_ENABLED_FIELD_NUMBER: ClassVar[int]
    DESIRED_NODES_FIELD_NUMBER: ClassVar[int]
    MAX_NODES_FIELD_NUMBER: ClassVar[int]
    MIN_NODES_FIELD_NUMBER: ClassVar[int]
    autoscaling_enabled: bool
    desired_nodes: int
    max_nodes: int
    min_nodes: int
    def __init__(self, autoscaling_enabled: bool = ..., min_nodes: Optional[int] = ..., max_nodes: Optional[int] = ..., desired_nodes: Optional[int] = ...) -> None: ...

class GoogleCloudBackendService(_message.Message):
    __slots__ = ["instance_group", "project", "region", "target_id"]
    INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    PROJECT_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    TARGET_ID_FIELD_NUMBER: ClassVar[int]
    instance_group: GoogleCloudInstanceGroup
    project: str
    region: str
    target_id: str
    def __init__(self, target_id: Optional[str] = ..., project: Optional[str] = ..., region: Optional[str] = ..., instance_group: Optional[Union[GoogleCloudInstanceGroup, Mapping]] = ...) -> None: ...

class GoogleCloudInstanceGroup(_message.Message):
    __slots__ = ["health_check_name", "machine_type", "project", "region", "subnetworks", "target_id"]
    HEALTH_CHECK_NAME_FIELD_NUMBER: ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: ClassVar[int]
    PROJECT_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    SUBNETWORKS_FIELD_NUMBER: ClassVar[int]
    TARGET_ID_FIELD_NUMBER: ClassVar[int]
    health_check_name: str
    machine_type: str
    project: str
    region: str
    subnetworks: _containers.RepeatedScalarFieldContainer[str]
    target_id: str
    def __init__(self, project: Optional[str] = ..., region: Optional[str] = ..., target_id: Optional[str] = ..., machine_type: Optional[str] = ..., subnetworks: Optional[Iterable[str]] = ..., health_check_name: Optional[str] = ...) -> None: ...

class HealthCheckConfig(_message.Message):
    __slots__ = ["path", "port", "protocol_type"]
    PATH_FIELD_NUMBER: ClassVar[int]
    PORT_FIELD_NUMBER: ClassVar[int]
    PROTOCOL_TYPE_FIELD_NUMBER: ClassVar[int]
    path: str
    port: NamedPort
    protocol_type: str
    def __init__(self, port: Optional[Union[NamedPort, Mapping]] = ..., path: Optional[str] = ..., protocol_type: Optional[str] = ...) -> None: ...

class InstanceGroup(_message.Message):
    __slots__ = ["aws_instance_group", "capacity", "container_image", "environment_variables", "google_cloud_instance_group", "grpc_port", "health_check_config", "health_check_name", "http_port", "name", "prometheus_port", "tags"]
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    AWS_INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    CAPACITY_FIELD_NUMBER: ClassVar[int]
    CONTAINER_IMAGE_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: ClassVar[int]
    GOOGLE_CLOUD_INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    GRPC_PORT_FIELD_NUMBER: ClassVar[int]
    HEALTH_CHECK_CONFIG_FIELD_NUMBER: ClassVar[int]
    HEALTH_CHECK_NAME_FIELD_NUMBER: ClassVar[int]
    HTTP_PORT_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    PROMETHEUS_PORT_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    aws_instance_group: AWSInstanceGroup
    capacity: CapacityConfig
    container_image: _container_image__client_pb2.ContainerImage
    environment_variables: _containers.ScalarMap[str, str]
    google_cloud_instance_group: GoogleCloudInstanceGroup
    grpc_port: NamedPort
    health_check_config: HealthCheckConfig
    health_check_name: str
    http_port: NamedPort
    name: str
    prometheus_port: NamedPort
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: Optional[str] = ..., container_image: Optional[Union[_container_image__client_pb2.ContainerImage, Mapping]] = ..., capacity: Optional[Union[CapacityConfig, Mapping]] = ..., health_check_config: Optional[Union[HealthCheckConfig, Mapping]] = ..., health_check_name: Optional[str] = ..., prometheus_port: Optional[Union[NamedPort, Mapping]] = ..., grpc_port: Optional[Union[NamedPort, Mapping]] = ..., http_port: Optional[Union[NamedPort, Mapping]] = ..., aws_instance_group: Optional[Union[AWSInstanceGroup, Mapping]] = ..., google_cloud_instance_group: Optional[Union[GoogleCloudInstanceGroup, Mapping]] = ..., tags: Optional[Mapping[str, str]] = ..., environment_variables: Optional[Mapping[str, str]] = ...) -> None: ...

class InstanceGroupHandle(_message.Message):
    __slots__ = ["instance_group_id", "instance_group_name", "instance_group_template_id"]
    INSTANCE_GROUP_ID_FIELD_NUMBER: ClassVar[int]
    INSTANCE_GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    INSTANCE_GROUP_TEMPLATE_ID_FIELD_NUMBER: ClassVar[int]
    instance_group_id: str
    instance_group_name: str
    instance_group_template_id: str
    def __init__(self, instance_group_id: Optional[str] = ..., instance_group_name: Optional[str] = ..., instance_group_template_id: Optional[str] = ...) -> None: ...

class InstanceGroupStatus(_message.Message):
    __slots__ = ["healthy_instances"]
    HEALTHY_INSTANCES_FIELD_NUMBER: ClassVar[int]
    healthy_instances: int
    def __init__(self, healthy_instances: Optional[int] = ...) -> None: ...

class LoadBalancerTarget(_message.Message):
    __slots__ = ["aws_target_group", "google_backend_service"]
    AWS_TARGET_GROUP_FIELD_NUMBER: ClassVar[int]
    GOOGLE_BACKEND_SERVICE_FIELD_NUMBER: ClassVar[int]
    aws_target_group: AWSTargetGroup
    google_backend_service: GoogleCloudBackendService
    def __init__(self, aws_target_group: Optional[Union[AWSTargetGroup, Mapping]] = ..., google_backend_service: Optional[Union[GoogleCloudBackendService, Mapping]] = ...) -> None: ...

class NamedPort(_message.Message):
    __slots__ = ["port_name", "port_number"]
    PORT_NAME_FIELD_NUMBER: ClassVar[int]
    PORT_NUMBER_FIELD_NUMBER: ClassVar[int]
    port_name: str
    port_number: int
    def __init__(self, port_number: Optional[int] = ..., port_name: Optional[str] = ...) -> None: ...
