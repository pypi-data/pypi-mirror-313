from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
GENERAL_PURPOSE_SSD: EbsVolumeType
INSTANCE_FLEET_FOR_INTEGRATION_TESTS_ONLY: AwsAvailability
ON_DEMAND: AwsAvailability
SPOT: AwsAvailability
SPOT_WITH_FALLBACK: AwsAvailability
THROUGHPUT_OPTIMIZED_HDD: EbsVolumeType
UNKNOWN_AWS_AVAILABILITY: AwsAvailability
UNKNOWN_EBS_VOLUME_TYPE: EbsVolumeType

class AutoScale(_message.Message):
    __slots__ = ["max_workers", "min_workers"]
    MAX_WORKERS_FIELD_NUMBER: ClassVar[int]
    MIN_WORKERS_FIELD_NUMBER: ClassVar[int]
    max_workers: int
    min_workers: int
    def __init__(self, min_workers: Optional[int] = ..., max_workers: Optional[int] = ...) -> None: ...

class AwsAttributes(_message.Message):
    __slots__ = ["availability", "ebs_volume_count", "ebs_volume_size", "ebs_volume_type", "first_on_demand", "instance_profile_arn", "spot_bid_price_percent", "zone_id"]
    AVAILABILITY_FIELD_NUMBER: ClassVar[int]
    EBS_VOLUME_COUNT_FIELD_NUMBER: ClassVar[int]
    EBS_VOLUME_SIZE_FIELD_NUMBER: ClassVar[int]
    EBS_VOLUME_TYPE_FIELD_NUMBER: ClassVar[int]
    FIRST_ON_DEMAND_FIELD_NUMBER: ClassVar[int]
    INSTANCE_PROFILE_ARN_FIELD_NUMBER: ClassVar[int]
    SPOT_BID_PRICE_PERCENT_FIELD_NUMBER: ClassVar[int]
    ZONE_ID_FIELD_NUMBER: ClassVar[int]
    availability: AwsAvailability
    ebs_volume_count: int
    ebs_volume_size: int
    ebs_volume_type: EbsVolumeType
    first_on_demand: int
    instance_profile_arn: str
    spot_bid_price_percent: int
    zone_id: str
    def __init__(self, first_on_demand: Optional[int] = ..., availability: Optional[Union[AwsAvailability, str]] = ..., zone_id: Optional[str] = ..., spot_bid_price_percent: Optional[int] = ..., instance_profile_arn: Optional[str] = ..., ebs_volume_type: Optional[Union[EbsVolumeType, str]] = ..., ebs_volume_count: Optional[int] = ..., ebs_volume_size: Optional[int] = ...) -> None: ...

class ClusterInfo(_message.Message):
    __slots__ = ["final_json", "new_cluster", "warnings"]
    FINAL_JSON_FIELD_NUMBER: ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: ClassVar[int]
    WARNINGS_FIELD_NUMBER: ClassVar[int]
    final_json: str
    new_cluster: NewCluster
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, new_cluster: Optional[Union[NewCluster, Mapping]] = ..., final_json: Optional[str] = ..., warnings: Optional[Iterable[str]] = ...) -> None: ...

class ClusterLogConf(_message.Message):
    __slots__ = ["s3"]
    S3_FIELD_NUMBER: ClassVar[int]
    s3: S3StorageInfo
    def __init__(self, s3: Optional[Union[S3StorageInfo, Mapping]] = ...) -> None: ...

class ClusterTag(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    key: str
    value: str
    def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...

class DbfsStorageInfo(_message.Message):
    __slots__ = ["destination"]
    DESTINATION_FIELD_NUMBER: ClassVar[int]
    destination: str
    def __init__(self, destination: Optional[str] = ...) -> None: ...

class ExistingCluster(_message.Message):
    __slots__ = ["cluster_id"]
    CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: Optional[str] = ...) -> None: ...

class GCPAttributes(_message.Message):
    __slots__ = ["availability", "boot_disk_size", "google_service_account", "use_preemptible_executors", "zone_id"]
    AVAILABILITY_FIELD_NUMBER: ClassVar[int]
    BOOT_DISK_SIZE_FIELD_NUMBER: ClassVar[int]
    GOOGLE_SERVICE_ACCOUNT_FIELD_NUMBER: ClassVar[int]
    USE_PREEMPTIBLE_EXECUTORS_FIELD_NUMBER: ClassVar[int]
    ZONE_ID_FIELD_NUMBER: ClassVar[int]
    availability: str
    boot_disk_size: int
    google_service_account: str
    use_preemptible_executors: bool
    zone_id: str
    def __init__(self, use_preemptible_executors: bool = ..., google_service_account: Optional[str] = ..., boot_disk_size: Optional[int] = ..., availability: Optional[str] = ..., zone_id: Optional[str] = ...) -> None: ...

class LocalStorageInfo(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class NewCluster(_message.Message):
    __slots__ = ["apply_policy_default_values", "autoscale", "aws_attributes", "cluster_log_conf", "cluster_name", "custom_tags", "data_security_mode", "driver_node_type_id", "enable_elastic_disk", "gcp_attributes", "init_scripts", "instance_pool_id", "json_cluster_config", "node_type_id", "num_workers", "policy_id", "root_volume_size_in_gb", "single_user_name", "spark_conf", "spark_env_vars", "spark_version", "terminateOnComplete"]
    class SparkConfEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    class SparkEnvVarsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    APPLY_POLICY_DEFAULT_VALUES_FIELD_NUMBER: ClassVar[int]
    AUTOSCALE_FIELD_NUMBER: ClassVar[int]
    AWS_ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    CLUSTER_LOG_CONF_FIELD_NUMBER: ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: ClassVar[int]
    CUSTOM_TAGS_FIELD_NUMBER: ClassVar[int]
    DATA_SECURITY_MODE_FIELD_NUMBER: ClassVar[int]
    DRIVER_NODE_TYPE_ID_FIELD_NUMBER: ClassVar[int]
    ENABLE_ELASTIC_DISK_FIELD_NUMBER: ClassVar[int]
    GCP_ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    INIT_SCRIPTS_FIELD_NUMBER: ClassVar[int]
    INSTANCE_POOL_ID_FIELD_NUMBER: ClassVar[int]
    JSON_CLUSTER_CONFIG_FIELD_NUMBER: ClassVar[int]
    NODE_TYPE_ID_FIELD_NUMBER: ClassVar[int]
    NUM_WORKERS_FIELD_NUMBER: ClassVar[int]
    POLICY_ID_FIELD_NUMBER: ClassVar[int]
    ROOT_VOLUME_SIZE_IN_GB_FIELD_NUMBER: ClassVar[int]
    SINGLE_USER_NAME_FIELD_NUMBER: ClassVar[int]
    SPARK_CONF_FIELD_NUMBER: ClassVar[int]
    SPARK_ENV_VARS_FIELD_NUMBER: ClassVar[int]
    SPARK_VERSION_FIELD_NUMBER: ClassVar[int]
    TERMINATEONCOMPLETE_FIELD_NUMBER: ClassVar[int]
    apply_policy_default_values: bool
    autoscale: AutoScale
    aws_attributes: AwsAttributes
    cluster_log_conf: ResourceLocation
    cluster_name: str
    custom_tags: _containers.RepeatedCompositeFieldContainer[ClusterTag]
    data_security_mode: str
    driver_node_type_id: str
    enable_elastic_disk: bool
    gcp_attributes: GCPAttributes
    init_scripts: _containers.RepeatedCompositeFieldContainer[ResourceLocation]
    instance_pool_id: str
    json_cluster_config: _struct_pb2.Struct
    node_type_id: str
    num_workers: int
    policy_id: str
    root_volume_size_in_gb: int
    single_user_name: str
    spark_conf: _containers.ScalarMap[str, str]
    spark_env_vars: _containers.ScalarMap[str, str]
    spark_version: str
    terminateOnComplete: bool
    def __init__(self, num_workers: Optional[int] = ..., autoscale: Optional[Union[AutoScale, Mapping]] = ..., cluster_name: Optional[str] = ..., spark_version: Optional[str] = ..., spark_conf: Optional[Mapping[str, str]] = ..., aws_attributes: Optional[Union[AwsAttributes, Mapping]] = ..., node_type_id: Optional[str] = ..., enable_elastic_disk: bool = ..., init_scripts: Optional[Iterable[Union[ResourceLocation, Mapping]]] = ..., cluster_log_conf: Optional[Union[ResourceLocation, Mapping]] = ..., custom_tags: Optional[Iterable[Union[ClusterTag, Mapping]]] = ..., terminateOnComplete: bool = ..., spark_env_vars: Optional[Mapping[str, str]] = ..., gcp_attributes: Optional[Union[GCPAttributes, Mapping]] = ..., json_cluster_config: Optional[Union[_struct_pb2.Struct, Mapping]] = ..., policy_id: Optional[str] = ..., apply_policy_default_values: bool = ..., driver_node_type_id: Optional[str] = ..., root_volume_size_in_gb: Optional[int] = ..., data_security_mode: Optional[str] = ..., single_user_name: Optional[str] = ..., instance_pool_id: Optional[str] = ...) -> None: ...

class ResourceLocation(_message.Message):
    __slots__ = ["dbfs", "local", "s3", "workspace"]
    DBFS_FIELD_NUMBER: ClassVar[int]
    LOCAL_FIELD_NUMBER: ClassVar[int]
    S3_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    dbfs: DbfsStorageInfo
    local: LocalStorageInfo
    s3: S3StorageInfo
    workspace: WorkspaceStorageInfo
    def __init__(self, s3: Optional[Union[S3StorageInfo, Mapping]] = ..., dbfs: Optional[Union[DbfsStorageInfo, Mapping]] = ..., workspace: Optional[Union[WorkspaceStorageInfo, Mapping]] = ..., local: Optional[Union[LocalStorageInfo, Mapping]] = ...) -> None: ...

class S3StorageInfo(_message.Message):
    __slots__ = ["destination", "region"]
    DESTINATION_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    destination: str
    region: str
    def __init__(self, destination: Optional[str] = ..., region: Optional[str] = ...) -> None: ...

class WorkspaceStorageInfo(_message.Message):
    __slots__ = ["destination"]
    DESTINATION_FIELD_NUMBER: ClassVar[int]
    destination: str
    def __init__(self, destination: Optional[str] = ...) -> None: ...

class AwsAvailability(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class EbsVolumeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
