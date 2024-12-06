from tecton_proto.common import aws_credentials__client_pb2 as _aws_credentials__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsSettings(_message.Message):
    __slots__ = ["compute_extra_tags", "dynamo_extra_tags", "dynamo_role", "dynamo_table_names", "ec2_settings", "emr_settings", "object_store_locations"]
    class ComputeExtraTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    class DynamoExtraTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COMPUTE_EXTRA_TAGS_FIELD_NUMBER: ClassVar[int]
    DYNAMO_EXTRA_TAGS_FIELD_NUMBER: ClassVar[int]
    DYNAMO_ROLE_FIELD_NUMBER: ClassVar[int]
    DYNAMO_TABLE_NAMES_FIELD_NUMBER: ClassVar[int]
    EC2_SETTINGS_FIELD_NUMBER: ClassVar[int]
    EMR_SETTINGS_FIELD_NUMBER: ClassVar[int]
    OBJECT_STORE_LOCATIONS_FIELD_NUMBER: ClassVar[int]
    compute_extra_tags: _containers.ScalarMap[str, str]
    dynamo_extra_tags: _containers.ScalarMap[str, str]
    dynamo_role: _aws_credentials__client_pb2.AwsIamRole
    dynamo_table_names: DynamoTableNames
    ec2_settings: Ec2Settings
    emr_settings: EmrSettings
    object_store_locations: ObjectStoreLocations
    def __init__(self, dynamo_role: Optional[Union[_aws_credentials__client_pb2.AwsIamRole, Mapping]] = ..., dynamo_extra_tags: Optional[Mapping[str, str]] = ..., compute_extra_tags: Optional[Mapping[str, str]] = ..., emr_settings: Optional[Union[EmrSettings, Mapping]] = ..., ec2_settings: Optional[Union[Ec2Settings, Mapping]] = ..., dynamo_table_names: Optional[Union[DynamoTableNames, Mapping]] = ..., object_store_locations: Optional[Union[ObjectStoreLocations, Mapping]] = ...) -> None: ...

class DBFSLocation(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class DatabricksConfig(_message.Message):
    __slots__ = ["api_token", "spark_version", "user_display_name", "user_name", "workspace_url"]
    API_TOKEN_FIELD_NUMBER: ClassVar[int]
    SPARK_VERSION_FIELD_NUMBER: ClassVar[int]
    USER_DISPLAY_NAME_FIELD_NUMBER: ClassVar[int]
    USER_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_URL_FIELD_NUMBER: ClassVar[int]
    api_token: _secret__client_pb2.Secret
    spark_version: str
    user_display_name: str
    user_name: str
    workspace_url: str
    def __init__(self, workspace_url: Optional[str] = ..., api_token: Optional[Union[_secret__client_pb2.Secret, Mapping]] = ..., user_name: Optional[str] = ..., user_display_name: Optional[str] = ..., spark_version: Optional[str] = ...) -> None: ...

class DatabricksWorkspaceFileLocation(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class DynamoTableNames(_message.Message):
    __slots__ = ["canary_table_name", "data_table_prefix", "delta_log_table_name", "delta_log_table_name_v2", "job_idempotence_key_table_name", "job_metadata_table_name", "metric_table_prefix", "status_table_name"]
    CANARY_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    DATA_TABLE_PREFIX_FIELD_NUMBER: ClassVar[int]
    DELTA_LOG_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    DELTA_LOG_TABLE_NAME_V2_FIELD_NUMBER: ClassVar[int]
    JOB_IDEMPOTENCE_KEY_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    JOB_METADATA_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    METRIC_TABLE_PREFIX_FIELD_NUMBER: ClassVar[int]
    STATUS_TABLE_NAME_FIELD_NUMBER: ClassVar[int]
    canary_table_name: str
    data_table_prefix: str
    delta_log_table_name: str
    delta_log_table_name_v2: str
    job_idempotence_key_table_name: str
    job_metadata_table_name: str
    metric_table_prefix: str
    status_table_name: str
    def __init__(self, data_table_prefix: Optional[str] = ..., status_table_name: Optional[str] = ..., job_idempotence_key_table_name: Optional[str] = ..., canary_table_name: Optional[str] = ..., delta_log_table_name: Optional[str] = ..., metric_table_prefix: Optional[str] = ..., delta_log_table_name_v2: Optional[str] = ..., job_metadata_table_name: Optional[str] = ...) -> None: ...

class Ec2Settings(_message.Message):
    __slots__ = ["ray_cluster_manager_role", "ray_instance_profile"]
    RAY_CLUSTER_MANAGER_ROLE_FIELD_NUMBER: ClassVar[int]
    RAY_INSTANCE_PROFILE_FIELD_NUMBER: ClassVar[int]
    ray_cluster_manager_role: _aws_credentials__client_pb2.AwsIamRole
    ray_instance_profile: _aws_credentials__client_pb2.AwsIamRole
    def __init__(self, ray_cluster_manager_role: Optional[Union[_aws_credentials__client_pb2.AwsIamRole, Mapping]] = ..., ray_instance_profile: Optional[Union[_aws_credentials__client_pb2.AwsIamRole, Mapping]] = ...) -> None: ...

class EmrSettings(_message.Message):
    __slots__ = ["emr_control_role"]
    EMR_CONTROL_ROLE_FIELD_NUMBER: ClassVar[int]
    emr_control_role: _aws_credentials__client_pb2.AwsIamRole
    def __init__(self, emr_control_role: Optional[Union[_aws_credentials__client_pb2.AwsIamRole, Mapping]] = ...) -> None: ...

class GCSLocation(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class ObjectStoreLocation(_message.Message):
    __slots__ = ["dbfs_location", "gcs_location", "s3_location", "workspace_location"]
    DBFS_LOCATION_FIELD_NUMBER: ClassVar[int]
    GCS_LOCATION_FIELD_NUMBER: ClassVar[int]
    S3_LOCATION_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_LOCATION_FIELD_NUMBER: ClassVar[int]
    dbfs_location: DBFSLocation
    gcs_location: GCSLocation
    s3_location: S3Location
    workspace_location: DatabricksWorkspaceFileLocation
    def __init__(self, s3_location: Optional[Union[S3Location, Mapping]] = ..., dbfs_location: Optional[Union[DBFSLocation, Mapping]] = ..., gcs_location: Optional[Union[GCSLocation, Mapping]] = ..., workspace_location: Optional[Union[DatabricksWorkspaceFileLocation, Mapping]] = ...) -> None: ...

class ObjectStoreLocations(_message.Message):
    __slots__ = ["custom_environment_dependencies", "data_validation", "databricks_scripts", "emr_scripts", "feature_export", "feature_repo", "feature_server_configuration", "feature_server_logging", "intermediate_data", "job_metadata_table", "kafka_credentials_base", "materialization", "materialization_params", "model_artifacts", "observability_service_configuration", "push_api_configuration", "rift_logs", "self_serve_consumption", "streaming_checkpoint", "system_audit_logging", "transformation_config"]
    CUSTOM_ENVIRONMENT_DEPENDENCIES_FIELD_NUMBER: ClassVar[int]
    DATABRICKS_SCRIPTS_FIELD_NUMBER: ClassVar[int]
    DATA_VALIDATION_FIELD_NUMBER: ClassVar[int]
    EMR_SCRIPTS_FIELD_NUMBER: ClassVar[int]
    FEATURE_EXPORT_FIELD_NUMBER: ClassVar[int]
    FEATURE_REPO_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_CONFIGURATION_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_LOGGING_FIELD_NUMBER: ClassVar[int]
    INTERMEDIATE_DATA_FIELD_NUMBER: ClassVar[int]
    JOB_METADATA_TABLE_FIELD_NUMBER: ClassVar[int]
    KAFKA_CREDENTIALS_BASE_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_PARAMS_FIELD_NUMBER: ClassVar[int]
    MODEL_ARTIFACTS_FIELD_NUMBER: ClassVar[int]
    OBSERVABILITY_SERVICE_CONFIGURATION_FIELD_NUMBER: ClassVar[int]
    PUSH_API_CONFIGURATION_FIELD_NUMBER: ClassVar[int]
    RIFT_LOGS_FIELD_NUMBER: ClassVar[int]
    SELF_SERVE_CONSUMPTION_FIELD_NUMBER: ClassVar[int]
    STREAMING_CHECKPOINT_FIELD_NUMBER: ClassVar[int]
    SYSTEM_AUDIT_LOGGING_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_CONFIG_FIELD_NUMBER: ClassVar[int]
    custom_environment_dependencies: ObjectStoreLocation
    data_validation: ObjectStoreLocation
    databricks_scripts: ObjectStoreLocation
    emr_scripts: ObjectStoreLocation
    feature_export: ObjectStoreLocation
    feature_repo: ObjectStoreLocation
    feature_server_configuration: ObjectStoreLocation
    feature_server_logging: ObjectStoreLocation
    intermediate_data: ObjectStoreLocation
    job_metadata_table: ObjectStoreLocation
    kafka_credentials_base: ObjectStoreLocation
    materialization: ObjectStoreLocation
    materialization_params: ObjectStoreLocation
    model_artifacts: ObjectStoreLocation
    observability_service_configuration: ObjectStoreLocation
    push_api_configuration: ObjectStoreLocation
    rift_logs: ObjectStoreLocation
    self_serve_consumption: ObjectStoreLocation
    streaming_checkpoint: ObjectStoreLocation
    system_audit_logging: ObjectStoreLocation
    transformation_config: ObjectStoreLocation
    def __init__(self, materialization: Optional[Union[ObjectStoreLocation, Mapping]] = ..., streaming_checkpoint: Optional[Union[ObjectStoreLocation, Mapping]] = ..., feature_server_configuration: Optional[Union[ObjectStoreLocation, Mapping]] = ..., feature_repo: Optional[Union[ObjectStoreLocation, Mapping]] = ..., emr_scripts: Optional[Union[ObjectStoreLocation, Mapping]] = ..., materialization_params: Optional[Union[ObjectStoreLocation, Mapping]] = ..., intermediate_data: Optional[Union[ObjectStoreLocation, Mapping]] = ..., feature_server_logging: Optional[Union[ObjectStoreLocation, Mapping]] = ..., kafka_credentials_base: Optional[Union[ObjectStoreLocation, Mapping]] = ..., job_metadata_table: Optional[Union[ObjectStoreLocation, Mapping]] = ..., push_api_configuration: Optional[Union[ObjectStoreLocation, Mapping]] = ..., data_validation: Optional[Union[ObjectStoreLocation, Mapping]] = ..., observability_service_configuration: Optional[Union[ObjectStoreLocation, Mapping]] = ..., system_audit_logging: Optional[Union[ObjectStoreLocation, Mapping]] = ..., databricks_scripts: Optional[Union[ObjectStoreLocation, Mapping]] = ..., self_serve_consumption: Optional[Union[ObjectStoreLocation, Mapping]] = ..., custom_environment_dependencies: Optional[Union[ObjectStoreLocation, Mapping]] = ..., feature_export: Optional[Union[ObjectStoreLocation, Mapping]] = ..., transformation_config: Optional[Union[ObjectStoreLocation, Mapping]] = ..., model_artifacts: Optional[Union[ObjectStoreLocation, Mapping]] = ..., rift_logs: Optional[Union[ObjectStoreLocation, Mapping]] = ...) -> None: ...

class S3Location(_message.Message):
    __slots__ = ["path", "role"]
    PATH_FIELD_NUMBER: ClassVar[int]
    ROLE_FIELD_NUMBER: ClassVar[int]
    path: str
    role: _aws_credentials__client_pb2.AwsIamRole
    def __init__(self, path: Optional[str] = ..., role: Optional[Union[_aws_credentials__client_pb2.AwsIamRole, Mapping]] = ...) -> None: ...

class TenantSettingsProto(_message.Message):
    __slots__ = ["aws_settings", "base_feature_service_url", "base_metadata_service_url", "chronosphere_api_key", "chronosphere_restrict_label_value", "chronosphere_tecton_cluster_name", "customer_facing_tenant_name", "enable_user_editing_deployment_settings", "internal_tenant_name", "okta_user_group_id", "pseudonymize_amplitude_user_name", "spicedb_organization_name"]
    AWS_SETTINGS_FIELD_NUMBER: ClassVar[int]
    BASE_FEATURE_SERVICE_URL_FIELD_NUMBER: ClassVar[int]
    BASE_METADATA_SERVICE_URL_FIELD_NUMBER: ClassVar[int]
    CHRONOSPHERE_API_KEY_FIELD_NUMBER: ClassVar[int]
    CHRONOSPHERE_RESTRICT_LABEL_VALUE_FIELD_NUMBER: ClassVar[int]
    CHRONOSPHERE_TECTON_CLUSTER_NAME_FIELD_NUMBER: ClassVar[int]
    CUSTOMER_FACING_TENANT_NAME_FIELD_NUMBER: ClassVar[int]
    ENABLE_USER_EDITING_DEPLOYMENT_SETTINGS_FIELD_NUMBER: ClassVar[int]
    INTERNAL_TENANT_NAME_FIELD_NUMBER: ClassVar[int]
    OKTA_USER_GROUP_ID_FIELD_NUMBER: ClassVar[int]
    PSEUDONYMIZE_AMPLITUDE_USER_NAME_FIELD_NUMBER: ClassVar[int]
    SPICEDB_ORGANIZATION_NAME_FIELD_NUMBER: ClassVar[int]
    aws_settings: AwsSettings
    base_feature_service_url: str
    base_metadata_service_url: str
    chronosphere_api_key: _secret__client_pb2.Secret
    chronosphere_restrict_label_value: str
    chronosphere_tecton_cluster_name: str
    customer_facing_tenant_name: str
    enable_user_editing_deployment_settings: bool
    internal_tenant_name: str
    okta_user_group_id: str
    pseudonymize_amplitude_user_name: bool
    spicedb_organization_name: str
    def __init__(self, chronosphere_api_key: Optional[Union[_secret__client_pb2.Secret, Mapping]] = ..., chronosphere_restrict_label_value: Optional[str] = ..., pseudonymize_amplitude_user_name: bool = ..., enable_user_editing_deployment_settings: bool = ..., okta_user_group_id: Optional[str] = ..., base_metadata_service_url: Optional[str] = ..., base_feature_service_url: Optional[str] = ..., spicedb_organization_name: Optional[str] = ..., customer_facing_tenant_name: Optional[str] = ..., chronosphere_tecton_cluster_name: Optional[str] = ..., aws_settings: Optional[Union[AwsSettings, Mapping]] = ..., internal_tenant_name: Optional[str] = ...) -> None: ...

class UserDeploymentSettings(_message.Message):
    __slots__ = ["databricks_config", "tenant_settings", "user_deployment_settings_version", "user_spark_settings"]
    DATABRICKS_CONFIG_FIELD_NUMBER: ClassVar[int]
    TENANT_SETTINGS_FIELD_NUMBER: ClassVar[int]
    USER_DEPLOYMENT_SETTINGS_VERSION_FIELD_NUMBER: ClassVar[int]
    USER_SPARK_SETTINGS_FIELD_NUMBER: ClassVar[int]
    databricks_config: DatabricksConfig
    tenant_settings: TenantSettingsProto
    user_deployment_settings_version: int
    user_spark_settings: UserSparkSettings
    def __init__(self, user_deployment_settings_version: Optional[int] = ..., databricks_config: Optional[Union[DatabricksConfig, Mapping]] = ..., user_spark_settings: Optional[Union[UserSparkSettings, Mapping]] = ..., tenant_settings: Optional[Union[TenantSettingsProto, Mapping]] = ...) -> None: ...

class UserSparkSettings(_message.Message):
    __slots__ = ["instance_profile_arn", "spark_conf"]
    class SparkConfEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    INSTANCE_PROFILE_ARN_FIELD_NUMBER: ClassVar[int]
    SPARK_CONF_FIELD_NUMBER: ClassVar[int]
    instance_profile_arn: str
    spark_conf: _containers.ScalarMap[str, str]
    def __init__(self, instance_profile_arn: Optional[str] = ..., spark_conf: Optional[Mapping[str, str]] = ...) -> None: ...
