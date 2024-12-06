from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.amplitude import amplitude__client_pb2 as _amplitude__client_pb2
from tecton_proto.amplitude import client_logging__client_pb2 as _client_logging__client_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.common import aws_credentials__client_pb2 as _aws_credentials__client_pb2
from tecton_proto.common import fco_locator__client_pb2 as _fco_locator__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.consumption import consumption__client_pb2 as _consumption__client_pb2
from tecton_proto.data import entity__client_pb2 as _entity__client_pb2
from tecton_proto.data import fco__client_pb2 as _fco__client_pb2
from tecton_proto.data import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.data import freshness_status__client_pb2 as _freshness_status__client_pb2
from tecton_proto.data import hive_metastore__client_pb2 as _hive_metastore__client_pb2
from tecton_proto.data import internal_spark_cluster_status__client_pb2 as _internal_spark_cluster_status__client_pb2
from tecton_proto.data import materialization_roles_allowlists__client_pb2 as _materialization_roles_allowlists__client_pb2
from tecton_proto.data import materialization_status__client_pb2 as _materialization_status__client_pb2
from tecton_proto.data import onboarding__client_pb2 as _onboarding__client_pb2
from tecton_proto.data import saved_feature_data_frame__client_pb2 as _saved_feature_data_frame__client_pb2
from tecton_proto.data import serving_status__client_pb2 as _serving_status__client_pb2
from tecton_proto.data import state_update__client_pb2 as _state_update__client_pb2
from tecton_proto.data import summary__client_pb2 as _summary__client_pb2
from tecton_proto.data import tecton_api_key__client_pb2 as _tecton_api_key__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.data import user__client_pb2 as _user__client_pb2
from tecton_proto.data import user_deployment_settings__client_pb2 as _user_deployment_settings__client_pb2
from tecton_proto.data import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from tecton_proto.data import workspace__client_pb2 as _workspace__client_pb2
from tecton_proto.dataobs import expectation__client_pb2 as _expectation__client_pb2
from tecton_proto.dataobs import metric__client_pb2 as _metric__client_pb2
from tecton_proto.dataobs import validation__client_pb2 as _validation__client_pb2
from tecton_proto.feature_analytics import feature_analytics__client_pb2 as _feature_analytics__client_pb2
from tecton_proto.materialization import job_metadata__client_pb2 as _job_metadata__client_pb2
from tecton_proto.materialization import spark_cluster__client_pb2 as _spark_cluster__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor
FCO_TYPE_ENTITY: FcoType
FCO_TYPE_FEATURE_SERVICE: FcoType
FCO_TYPE_FEATURE_VIEW: FcoType
FCO_TYPE_TRANSFORMATION: FcoType
FCO_TYPE_UNSPECIFIED: FcoType
FCO_TYPE_VIRTUAL_DATA_SOURCE: FcoType
FILTER_FIELD_FCO_TYPE: FilterField
FILTER_FIELD_MATERIALIZATION_OFFLINE: FilterField
FILTER_FIELD_MATERIALIZATION_ONLINE: FilterField
FILTER_FIELD_OWNER: FilterField
FILTER_FIELD_SEARCH_TYPE: FilterField
FILTER_FIELD_UNSPECIFIED: FilterField
FILTER_FIELD_WORKSPACE: FilterField
FILTER_FIELD_WORKSPACE_STATUS: FilterField
MATERIALIZATION_ENABLED_SEARCH_FILTER_DISABLED: MaterializationEnabledSearchFilter
MATERIALIZATION_ENABLED_SEARCH_FILTER_ENABLED: MaterializationEnabledSearchFilter
MATERIALIZATION_ENABLED_SEARCH_FILTER_UNSPECIFIED: MaterializationEnabledSearchFilter
SORT_ASC: SortDirection
SORT_DESC: SortDirection
SORT_UNKNOWN: SortDirection
WORKSPACE_CAPABILITIES_FILTER_DEV: WorkspaceCapabilitiesFilter
WORKSPACE_CAPABILITIES_FILTER_LIVE: WorkspaceCapabilitiesFilter
WORKSPACE_CAPABILITIES_FILTER_UNSPECIFIED: WorkspaceCapabilitiesFilter

class ApplyStateUpdateRequest(_message.Message):
    __slots__ = ["applied_by", "plan_integration_config", "state_id"]
    APPLIED_BY_FIELD_NUMBER: ClassVar[int]
    PLAN_INTEGRATION_CONFIG_FIELD_NUMBER: ClassVar[int]
    STATE_ID_FIELD_NUMBER: ClassVar[int]
    applied_by: str
    plan_integration_config: _state_update__client_pb2.PlanIntegrationTestConfig
    state_id: _id__client_pb2.Id
    def __init__(self, state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., applied_by: Optional[str] = ..., plan_integration_config: Optional[Union[_state_update__client_pb2.PlanIntegrationTestConfig, Mapping]] = ...) -> None: ...

class ApplyStateUpdateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ArchiveSavedFeatureDataFrameRequest(_message.Message):
    __slots__ = ["saved_feature_dataframe_id"]
    SAVED_FEATURE_DATAFRAME_ID_FIELD_NUMBER: ClassVar[int]
    saved_feature_dataframe_id: _id__client_pb2.Id
    def __init__(self, saved_feature_dataframe_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class ArchiveSavedFeatureDataFrameResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ClusterUserActionRequest(_message.Message):
    __slots__ = ["grant_admin", "okta_id", "resend_activation_email", "revoke_admin", "unlock_user"]
    GRANT_ADMIN_FIELD_NUMBER: ClassVar[int]
    OKTA_ID_FIELD_NUMBER: ClassVar[int]
    RESEND_ACTIVATION_EMAIL_FIELD_NUMBER: ClassVar[int]
    REVOKE_ADMIN_FIELD_NUMBER: ClassVar[int]
    UNLOCK_USER_FIELD_NUMBER: ClassVar[int]
    grant_admin: bool
    okta_id: str
    resend_activation_email: bool
    revoke_admin: bool
    unlock_user: bool
    def __init__(self, okta_id: Optional[str] = ..., resend_activation_email: bool = ..., unlock_user: bool = ..., grant_admin: bool = ..., revoke_admin: bool = ...) -> None: ...

class ClusterUserActionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CountRange(_message.Message):
    __slots__ = ["end", "start"]
    END_FIELD_NUMBER: ClassVar[int]
    START_FIELD_NUMBER: ClassVar[int]
    end: int
    start: int
    def __init__(self, start: Optional[int] = ..., end: Optional[int] = ...) -> None: ...

class CreateApiKeyRequest(_message.Message):
    __slots__ = ["description", "is_admin"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    IS_ADMIN_FIELD_NUMBER: ClassVar[int]
    description: str
    is_admin: bool
    def __init__(self, description: Optional[str] = ..., is_admin: bool = ...) -> None: ...

class CreateApiKeyResponse(_message.Message):
    __slots__ = ["id", "key"]
    ID_FIELD_NUMBER: ClassVar[int]
    KEY_FIELD_NUMBER: ClassVar[int]
    id: _id__client_pb2.Id
    key: str
    def __init__(self, key: Optional[str] = ..., id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class CreateClusterUserRequest(_message.Message):
    __slots__ = ["login_email"]
    LOGIN_EMAIL_FIELD_NUMBER: ClassVar[int]
    login_email: str
    def __init__(self, login_email: Optional[str] = ...) -> None: ...

class CreateClusterUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateSavedFeatureDataFrameRequest(_message.Message):
    __slots__ = ["feature_package_id", "feature_service_id", "join_key_column_names", "name", "schema", "timestamp_column_name", "workspace"]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    JOIN_KEY_COLUMN_NAMES_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_package_id: _id__client_pb2.Id
    feature_service_id: _id__client_pb2.Id
    join_key_column_names: _containers.RepeatedScalarFieldContainer[str]
    name: str
    schema: _spark_schema__client_pb2.SparkSchema
    timestamp_column_name: str
    workspace: str
    def __init__(self, name: Optional[str] = ..., workspace: Optional[str] = ..., feature_package_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., join_key_column_names: Optional[Iterable[str]] = ..., timestamp_column_name: Optional[str] = ..., schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...

class CreateSavedFeatureDataFrameResponse(_message.Message):
    __slots__ = ["saved_feature_dataframe"]
    SAVED_FEATURE_DATAFRAME_FIELD_NUMBER: ClassVar[int]
    saved_feature_dataframe: _saved_feature_data_frame__client_pb2.SavedFeatureDataFrame
    def __init__(self, saved_feature_dataframe: Optional[Union[_saved_feature_data_frame__client_pb2.SavedFeatureDataFrame, Mapping]] = ...) -> None: ...

class CreateServiceAccountRequest(_message.Message):
    __slots__ = ["description", "name"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    description: str
    name: str
    def __init__(self, name: Optional[str] = ..., description: Optional[str] = ...) -> None: ...

class CreateServiceAccountResponse(_message.Message):
    __slots__ = ["api_key", "created_at", "description", "id", "is_active", "name"]
    API_KEY_FIELD_NUMBER: ClassVar[int]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    api_key: str
    created_at: _timestamp_pb2.Timestamp
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., description: Optional[str] = ..., is_active: bool = ..., api_key: Optional[str] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class CreateWorkspaceRequest(_message.Message):
    __slots__ = ["capabilities", "workspace_name"]
    CAPABILITIES_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    capabilities: _workspace__client_pb2.WorkspaceCapabilities
    workspace_name: str
    def __init__(self, workspace_name: Optional[str] = ..., capabilities: Optional[Union[_workspace__client_pb2.WorkspaceCapabilities, Mapping]] = ...) -> None: ...

class DateTimeRange(_message.Message):
    __slots__ = ["end", "start"]
    END_FIELD_NUMBER: ClassVar[int]
    START_FIELD_NUMBER: ClassVar[int]
    end: _timestamp_pb2.Timestamp
    start: _timestamp_pb2.Timestamp
    def __init__(self, start: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., end: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class DeleteApiKeyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: ClassVar[int]
    id: _id__client_pb2.Id
    def __init__(self, id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class DeleteClusterUserRequest(_message.Message):
    __slots__ = ["okta_id"]
    OKTA_ID_FIELD_NUMBER: ClassVar[int]
    okta_id: str
    def __init__(self, okta_id: Optional[str] = ...) -> None: ...

class DeleteClusterUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteEntitiesRequest(_message.Message):
    __slots__ = ["fco_locator", "offline", "offline_join_keys_path", "online", "online_join_keys_full_path", "online_join_keys_path"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    OFFLINE_FIELD_NUMBER: ClassVar[int]
    OFFLINE_JOIN_KEYS_PATH_FIELD_NUMBER: ClassVar[int]
    ONLINE_FIELD_NUMBER: ClassVar[int]
    ONLINE_JOIN_KEYS_FULL_PATH_FIELD_NUMBER: ClassVar[int]
    ONLINE_JOIN_KEYS_PATH_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    offline: bool
    offline_join_keys_path: str
    online: bool
    online_join_keys_full_path: str
    online_join_keys_path: str
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ..., online_join_keys_path: Optional[str] = ..., online_join_keys_full_path: Optional[str] = ..., offline_join_keys_path: Optional[str] = ..., online: bool = ..., offline: bool = ...) -> None: ...

class DeleteEntitiesResponse(_message.Message):
    __slots__ = ["job_ids"]
    JOB_IDS_FIELD_NUMBER: ClassVar[int]
    job_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, job_ids: Optional[Iterable[str]] = ...) -> None: ...

class DeleteServiceAccountRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: ClassVar[int]
    id: str
    def __init__(self, id: Optional[str] = ...) -> None: ...

class DeleteServiceAccountResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteWorkspaceRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class DurationRange(_message.Message):
    __slots__ = ["end", "start"]
    END_FIELD_NUMBER: ClassVar[int]
    START_FIELD_NUMBER: ClassVar[int]
    end: _duration_pb2.Duration
    start: _duration_pb2.Duration
    def __init__(self, start: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., end: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class FcoSearchResult(_message.Message):
    __slots__ = ["description", "fco_id", "fco_type", "features", "last_updated", "materialization_offline", "materialization_online", "name", "owner", "tags", "workplace_state_id", "workspace", "workspace_status"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    FCO_ID_FIELD_NUMBER: ClassVar[int]
    FCO_TYPE_FIELD_NUMBER: ClassVar[int]
    FEATURES_FIELD_NUMBER: ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_OFFLINE_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_ONLINE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    OWNER_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    WORKPLACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATUS_FIELD_NUMBER: ClassVar[int]
    description: str
    fco_id: str
    fco_type: FcoType
    features: _containers.RepeatedScalarFieldContainer[str]
    last_updated: _timestamp_pb2.Timestamp
    materialization_offline: MaterializationEnabledSearchFilter
    materialization_online: MaterializationEnabledSearchFilter
    name: str
    owner: str
    tags: _containers.ScalarMap[str, str]
    workplace_state_id: str
    workspace: str
    workspace_status: WorkspaceCapabilitiesFilter
    def __init__(self, fco_id: Optional[str] = ..., workplace_state_id: Optional[str] = ..., fco_type: Optional[Union[FcoType, str]] = ..., name: Optional[str] = ..., description: Optional[str] = ..., owner: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ..., workspace: Optional[str] = ..., last_updated: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., materialization_offline: Optional[Union[MaterializationEnabledSearchFilter, str]] = ..., materialization_online: Optional[Union[MaterializationEnabledSearchFilter, str]] = ..., workspace_status: Optional[Union[WorkspaceCapabilitiesFilter, str]] = ..., features: Optional[Iterable[str]] = ...) -> None: ...

class FeatureServerAutoScalingConfig(_message.Message):
    __slots__ = ["enabled", "max_node_count", "min_node_count"]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    MAX_NODE_COUNT_FIELD_NUMBER: ClassVar[int]
    MIN_NODE_COUNT_FIELD_NUMBER: ClassVar[int]
    enabled: bool
    max_node_count: int
    min_node_count: int
    def __init__(self, enabled: bool = ..., min_node_count: Optional[int] = ..., max_node_count: Optional[int] = ...) -> None: ...

class FeatureViewMaterializationStatus(_message.Message):
    __slots__ = ["fco_locator", "materialization_status"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_STATUS_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    materialization_status: _materialization_status__client_pb2.MaterializationStatus
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ..., materialization_status: Optional[Union[_materialization_status__client_pb2.MaterializationStatus, Mapping]] = ...) -> None: ...

class FilterSearchResult(_message.Message):
    __slots__ = ["last_updated", "result"]
    LAST_UPDATED_FIELD_NUMBER: ClassVar[int]
    RESULT_FIELD_NUMBER: ClassVar[int]
    last_updated: _timestamp_pb2.Timestamp
    result: str
    def __init__(self, result: Optional[str] = ..., last_updated: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class FindFcoWorkspaceRequest(_message.Message):
    __slots__ = ["feature_view_id"]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    feature_view_id: _id__client_pb2.Id
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class FindFcoWorkspaceResponse(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class ForceRetryMaterializationTaskRequest(_message.Message):
    __slots__ = ["allow_overwrite", "materialization_task_id"]
    ALLOW_OVERWRITE_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_TASK_ID_FIELD_NUMBER: ClassVar[int]
    allow_overwrite: bool
    materialization_task_id: _id__client_pb2.Id
    def __init__(self, materialization_task_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., allow_overwrite: bool = ...) -> None: ...

class ForceRetryMaterializationTaskResponse(_message.Message):
    __slots__ = ["error_message"]
    ERROR_MESSAGE_FIELD_NUMBER: ClassVar[int]
    error_message: str
    def __init__(self, error_message: Optional[str] = ...) -> None: ...

class GetAllEntitiesRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetAllEntitiesResponse(_message.Message):
    __slots__ = ["entities"]
    ENTITIES_FIELD_NUMBER: ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[_entity__client_pb2.Entity]
    def __init__(self, entities: Optional[Iterable[Union[_entity__client_pb2.Entity, Mapping]]] = ...) -> None: ...

class GetAllFeatureFreshnessRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetAllFeatureFreshnessResponse(_message.Message):
    __slots__ = ["freshness_statuses"]
    FRESHNESS_STATUSES_FIELD_NUMBER: ClassVar[int]
    freshness_statuses: _containers.RepeatedCompositeFieldContainer[_freshness_status__client_pb2.FreshnessStatus]
    def __init__(self, freshness_statuses: Optional[Iterable[Union[_freshness_status__client_pb2.FreshnessStatus, Mapping]]] = ...) -> None: ...

class GetAllFeatureServicesRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetAllFeatureServicesResponse(_message.Message):
    __slots__ = ["feature_services"]
    FEATURE_SERVICES_FIELD_NUMBER: ClassVar[int]
    feature_services: _containers.RepeatedCompositeFieldContainer[_feature_service__client_pb2.FeatureService]
    def __init__(self, feature_services: Optional[Iterable[Union[_feature_service__client_pb2.FeatureService, Mapping]]] = ...) -> None: ...

class GetAllMaterializationStatusInLiveWorkspacesRequest(_message.Message):
    __slots__ = ["cut_off_days"]
    CUT_OFF_DAYS_FIELD_NUMBER: ClassVar[int]
    cut_off_days: int
    def __init__(self, cut_off_days: Optional[int] = ...) -> None: ...

class GetAllMaterializationStatusInLiveWorkspacesResponse(_message.Message):
    __slots__ = ["feature_view_materialization_status"]
    FEATURE_VIEW_MATERIALIZATION_STATUS_FIELD_NUMBER: ClassVar[int]
    feature_view_materialization_status: _containers.RepeatedCompositeFieldContainer[FeatureViewMaterializationStatus]
    def __init__(self, feature_view_materialization_status: Optional[Iterable[Union[FeatureViewMaterializationStatus, Mapping]]] = ...) -> None: ...

class GetAllSavedFeatureDataFramesRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetAllSavedFeatureDataFramesResponse(_message.Message):
    __slots__ = ["saved_feature_dataframes"]
    SAVED_FEATURE_DATAFRAMES_FIELD_NUMBER: ClassVar[int]
    saved_feature_dataframes: _containers.RepeatedCompositeFieldContainer[_saved_feature_data_frame__client_pb2.SavedFeatureDataFrame]
    def __init__(self, saved_feature_dataframes: Optional[Iterable[Union[_saved_feature_data_frame__client_pb2.SavedFeatureDataFrame, Mapping]]] = ...) -> None: ...

class GetAllTransformationsRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetAllTransformationsResponse(_message.Message):
    __slots__ = ["transformations"]
    TRANSFORMATIONS_FIELD_NUMBER: ClassVar[int]
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    def __init__(self, transformations: Optional[Iterable[Union[_transformation__client_pb2.Transformation, Mapping]]] = ...) -> None: ...

class GetAllVirtualDataSourcesRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetAllVirtualDataSourcesResponse(_message.Message):
    __slots__ = ["virtual_data_sources"]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: ClassVar[int]
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSource]
    def __init__(self, virtual_data_sources: Optional[Iterable[Union[_virtual_data_source__client_pb2.VirtualDataSource, Mapping]]] = ...) -> None: ...

class GetClusterAdminInfoResponse(_message.Message):
    __slots__ = ["admins", "caller_is_admin", "users"]
    ADMINS_FIELD_NUMBER: ClassVar[int]
    CALLER_IS_ADMIN_FIELD_NUMBER: ClassVar[int]
    USERS_FIELD_NUMBER: ClassVar[int]
    admins: _containers.RepeatedCompositeFieldContainer[_user__client_pb2.User]
    caller_is_admin: bool
    users: _containers.RepeatedCompositeFieldContainer[_user__client_pb2.User]
    def __init__(self, caller_is_admin: bool = ..., users: Optional[Iterable[Union[_user__client_pb2.User, Mapping]]] = ..., admins: Optional[Iterable[Union[_user__client_pb2.User, Mapping]]] = ...) -> None: ...

class GetConfigsResponse(_message.Message):
    __slots__ = ["key_values"]
    class KeyValuesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    KEY_VALUES_FIELD_NUMBER: ClassVar[int]
    key_values: _containers.ScalarMap[str, str]
    def __init__(self, key_values: Optional[Mapping[str, str]] = ...) -> None: ...

class GetConsumptionRecordsRequest(_message.Message):
    __slots__ = ["consumption_type", "end_time", "start_time"]
    CONSUMPTION_TYPE_FIELD_NUMBER: ClassVar[int]
    END_TIME_FIELD_NUMBER: ClassVar[int]
    START_TIME_FIELD_NUMBER: ClassVar[int]
    consumption_type: _consumption__client_pb2.ConsumptionType
    end_time: _timestamp_pb2.Timestamp
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, consumption_type: Optional[Union[_consumption__client_pb2.ConsumptionType, str]] = ..., start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class GetConsumptionRecordsResponse(_message.Message):
    __slots__ = ["consumption_records"]
    CONSUMPTION_RECORDS_FIELD_NUMBER: ClassVar[int]
    consumption_records: _containers.RepeatedCompositeFieldContainer[_consumption__client_pb2.ConsumptionRecord]
    def __init__(self, consumption_records: Optional[Iterable[Union[_consumption__client_pb2.ConsumptionRecord, Mapping]]] = ...) -> None: ...

class GetDataPlatformSetupStatusResponse(_message.Message):
    __slots__ = ["setupCompleted", "tasks"]
    SETUPCOMPLETED_FIELD_NUMBER: ClassVar[int]
    TASKS_FIELD_NUMBER: ClassVar[int]
    setupCompleted: bool
    tasks: _containers.RepeatedCompositeFieldContainer[_onboarding__client_pb2.DataPlatformSetupTaskStatus]
    def __init__(self, setupCompleted: bool = ..., tasks: Optional[Iterable[Union[_onboarding__client_pb2.DataPlatformSetupTaskStatus, Mapping]]] = ...) -> None: ...

class GetDeleteEntitiesInfoRequest(_message.Message):
    __slots__ = ["feature_definition_id"]
    FEATURE_DEFINITION_ID_FIELD_NUMBER: ClassVar[int]
    feature_definition_id: _id__client_pb2.Id
    def __init__(self, feature_definition_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class GetDeleteEntitiesInfoResponse(_message.Message):
    __slots__ = ["df_path", "signed_url_for_df_upload_offline", "signed_url_for_df_upload_online"]
    DF_PATH_FIELD_NUMBER: ClassVar[int]
    SIGNED_URL_FOR_DF_UPLOAD_OFFLINE_FIELD_NUMBER: ClassVar[int]
    SIGNED_URL_FOR_DF_UPLOAD_ONLINE_FIELD_NUMBER: ClassVar[int]
    df_path: str
    signed_url_for_df_upload_offline: str
    signed_url_for_df_upload_online: str
    def __init__(self, df_path: Optional[str] = ..., signed_url_for_df_upload_online: Optional[str] = ..., signed_url_for_df_upload_offline: Optional[str] = ...) -> None: ...

class GetEntityRequest(_message.Message):
    __slots__ = ["entity_id", "name", "run_object_version_check", "workspace"]
    ENTITY_ID_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    RUN_OBJECT_VERSION_CHECK_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    entity_id: _id__client_pb2.Id
    name: str
    run_object_version_check: bool
    workspace: str
    def __init__(self, entity_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., name: Optional[str] = ..., workspace: Optional[str] = ..., run_object_version_check: bool = ...) -> None: ...

class GetEntityResponse(_message.Message):
    __slots__ = ["fco_container"]
    FCO_CONTAINER_FIELD_NUMBER: ClassVar[int]
    fco_container: _fco__client_pb2.FcoContainer
    def __init__(self, fco_container: Optional[Union[_fco__client_pb2.FcoContainer, Mapping]] = ...) -> None: ...

class GetEntitySummaryRequest(_message.Message):
    __slots__ = ["fco_locator"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ...) -> None: ...

class GetEntitySummaryResponse(_message.Message):
    __slots__ = ["fco_summary"]
    FCO_SUMMARY_FIELD_NUMBER: ClassVar[int]
    fco_summary: _summary__client_pb2.FcoSummary
    def __init__(self, fco_summary: Optional[Union[_summary__client_pb2.FcoSummary, Mapping]] = ...) -> None: ...

class GetFVServingStatusForFSRequest(_message.Message):
    __slots__ = ["feature_service_id", "pagination", "workspace"]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    PAGINATION_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service_id: _id__client_pb2.Id
    pagination: PaginationRequest
    workspace: str
    def __init__(self, feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., workspace: Optional[str] = ..., pagination: Optional[Union[PaginationRequest, Mapping]] = ...) -> None: ...

class GetFVServingStatusForFSResponse(_message.Message):
    __slots__ = ["full_serving_status_summary", "pagination"]
    FULL_SERVING_STATUS_SUMMARY_FIELD_NUMBER: ClassVar[int]
    PAGINATION_FIELD_NUMBER: ClassVar[int]
    full_serving_status_summary: _serving_status__client_pb2.FullFeatureServiceServingSummary
    pagination: PaginationResponse
    def __init__(self, full_serving_status_summary: Optional[Union[_serving_status__client_pb2.FullFeatureServiceServingSummary, Mapping]] = ..., pagination: Optional[Union[PaginationResponse, Mapping]] = ...) -> None: ...

class GetFcosRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetFcosResponse(_message.Message):
    __slots__ = ["fco_container"]
    FCO_CONTAINER_FIELD_NUMBER: ClassVar[int]
    fco_container: _fco__client_pb2.FcoContainer
    def __init__(self, fco_container: Optional[Union[_fco__client_pb2.FcoContainer, Mapping]] = ...) -> None: ...

class GetFeatureAnalyticsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetFeatureAnalyticsResponse(_message.Message):
    __slots__ = ["feature_analytics"]
    FEATURE_ANALYTICS_FIELD_NUMBER: ClassVar[int]
    feature_analytics: _feature_analytics__client_pb2.FeatureSimilarityAnalysisResult
    def __init__(self, feature_analytics: Optional[Union[_feature_analytics__client_pb2.FeatureSimilarityAnalysisResult, Mapping]] = ...) -> None: ...

class GetFeatureFreshnessRequest(_message.Message):
    __slots__ = ["fco_locator"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ...) -> None: ...

class GetFeatureFreshnessResponse(_message.Message):
    __slots__ = ["freshness_status"]
    FRESHNESS_STATUS_FIELD_NUMBER: ClassVar[int]
    freshness_status: _freshness_status__client_pb2.FreshnessStatus
    def __init__(self, freshness_status: Optional[Union[_freshness_status__client_pb2.FreshnessStatus, Mapping]] = ...) -> None: ...

class GetFeatureServerConfigRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetFeatureServerConfigResponse(_message.Message):
    __slots__ = ["autoScalingConfig", "availableCount", "currentCount", "desiredCount"]
    AUTOSCALINGCONFIG_FIELD_NUMBER: ClassVar[int]
    AVAILABLECOUNT_FIELD_NUMBER: ClassVar[int]
    CURRENTCOUNT_FIELD_NUMBER: ClassVar[int]
    DESIREDCOUNT_FIELD_NUMBER: ClassVar[int]
    autoScalingConfig: FeatureServerAutoScalingConfig
    availableCount: int
    currentCount: int
    desiredCount: int
    def __init__(self, currentCount: Optional[int] = ..., availableCount: Optional[int] = ..., desiredCount: Optional[int] = ..., autoScalingConfig: Optional[Union[FeatureServerAutoScalingConfig, Mapping]] = ...) -> None: ...

class GetFeatureServiceRequest(_message.Message):
    __slots__ = ["id", "run_object_version_check", "service_reference", "workspace"]
    ID_FIELD_NUMBER: ClassVar[int]
    RUN_OBJECT_VERSION_CHECK_FIELD_NUMBER: ClassVar[int]
    SERVICE_REFERENCE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    id: _id__client_pb2.Id
    run_object_version_check: bool
    service_reference: str
    workspace: str
    def __init__(self, service_reference: Optional[str] = ..., workspace: Optional[str] = ..., id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., run_object_version_check: bool = ...) -> None: ...

class GetFeatureServiceResponse(_message.Message):
    __slots__ = ["fco_container"]
    FCO_CONTAINER_FIELD_NUMBER: ClassVar[int]
    fco_container: _fco__client_pb2.FcoContainer
    def __init__(self, fco_container: Optional[Union[_fco__client_pb2.FcoContainer, Mapping]] = ...) -> None: ...

class GetFeatureServiceSummaryRequest(_message.Message):
    __slots__ = ["feature_service_id", "feature_service_name", "workspace"]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_service_id: _id__client_pb2.Id
    feature_service_name: str
    workspace: str
    def __init__(self, feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_service_name: Optional[str] = ..., workspace: Optional[str] = ...) -> None: ...

class GetFeatureServiceSummaryResponse(_message.Message):
    __slots__ = ["general_items", "variant_names"]
    GENERAL_ITEMS_FIELD_NUMBER: ClassVar[int]
    VARIANT_NAMES_FIELD_NUMBER: ClassVar[int]
    general_items: _containers.RepeatedCompositeFieldContainer[_summary__client_pb2.SummaryItem]
    variant_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, general_items: Optional[Iterable[Union[_summary__client_pb2.SummaryItem, Mapping]]] = ..., variant_names: Optional[Iterable[str]] = ...) -> None: ...

class GetFeatureValidationResultRequest(_message.Message):
    __slots__ = ["filter_expectation_names", "filter_feature_view_names", "filter_result_types", "pagination", "validation_end_time", "validation_start_time", "workspace"]
    FILTER_EXPECTATION_NAMES_FIELD_NUMBER: ClassVar[int]
    FILTER_FEATURE_VIEW_NAMES_FIELD_NUMBER: ClassVar[int]
    FILTER_RESULT_TYPES_FIELD_NUMBER: ClassVar[int]
    PAGINATION_FIELD_NUMBER: ClassVar[int]
    VALIDATION_END_TIME_FIELD_NUMBER: ClassVar[int]
    VALIDATION_START_TIME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    filter_expectation_names: _containers.RepeatedScalarFieldContainer[str]
    filter_feature_view_names: _containers.RepeatedScalarFieldContainer[str]
    filter_result_types: _containers.RepeatedScalarFieldContainer[_validation__client_pb2.ExpectationResultEnum]
    pagination: PaginationRequest
    validation_end_time: _timestamp_pb2.Timestamp
    validation_start_time: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., validation_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., validation_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., filter_feature_view_names: Optional[Iterable[str]] = ..., filter_expectation_names: Optional[Iterable[str]] = ..., filter_result_types: Optional[Iterable[Union[_validation__client_pb2.ExpectationResultEnum, str]]] = ..., pagination: Optional[Union[PaginationRequest, Mapping]] = ...) -> None: ...

class GetFeatureValidationResultResponse(_message.Message):
    __slots__ = ["pagination", "results"]
    PAGINATION_FIELD_NUMBER: ClassVar[int]
    RESULTS_FIELD_NUMBER: ClassVar[int]
    pagination: PaginationResponse
    results: _containers.RepeatedCompositeFieldContainer[_validation__client_pb2.ExpectationResult]
    def __init__(self, results: Optional[Iterable[Union[_validation__client_pb2.ExpectationResult, Mapping]]] = ..., pagination: Optional[Union[PaginationResponse, Mapping]] = ...) -> None: ...

class GetFeatureValidationSummaryRequest(_message.Message):
    __slots__ = ["validation_end_time", "validation_start_time", "workspace"]
    VALIDATION_END_TIME_FIELD_NUMBER: ClassVar[int]
    VALIDATION_START_TIME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    validation_end_time: _timestamp_pb2.Timestamp
    validation_start_time: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., validation_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., validation_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class GetFeatureValidationSummaryResponse(_message.Message):
    __slots__ = ["validation_end_time", "validation_start_time", "workspace", "workspace_summary"]
    VALIDATION_END_TIME_FIELD_NUMBER: ClassVar[int]
    VALIDATION_START_TIME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_SUMMARY_FIELD_NUMBER: ClassVar[int]
    validation_end_time: _timestamp_pb2.Timestamp
    validation_start_time: _timestamp_pb2.Timestamp
    workspace: str
    workspace_summary: _validation__client_pb2.WorkspaceResultSummary
    def __init__(self, workspace: Optional[str] = ..., validation_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., validation_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., workspace_summary: Optional[Union[_validation__client_pb2.WorkspaceResultSummary, Mapping]] = ...) -> None: ...

class GetFeatureViewRequest(_message.Message):
    __slots__ = ["id", "run_object_version_check", "version_specifier", "workspace"]
    ID_FIELD_NUMBER: ClassVar[int]
    RUN_OBJECT_VERSION_CHECK_FIELD_NUMBER: ClassVar[int]
    VERSION_SPECIFIER_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    id: _id__client_pb2.Id
    run_object_version_check: bool
    version_specifier: str
    workspace: str
    def __init__(self, version_specifier: Optional[str] = ..., workspace: Optional[str] = ..., id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., run_object_version_check: bool = ...) -> None: ...

class GetFeatureViewResponse(_message.Message):
    __slots__ = ["fco_container"]
    FCO_CONTAINER_FIELD_NUMBER: ClassVar[int]
    fco_container: _fco__client_pb2.FcoContainer
    def __init__(self, fco_container: Optional[Union[_fco__client_pb2.FcoContainer, Mapping]] = ...) -> None: ...

class GetFeatureViewSummaryRequest(_message.Message):
    __slots__ = ["fco_locator"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ...) -> None: ...

class GetFeatureViewSummaryResponse(_message.Message):
    __slots__ = ["fco_summary"]
    FCO_SUMMARY_FIELD_NUMBER: ClassVar[int]
    fco_summary: _summary__client_pb2.FcoSummary
    def __init__(self, fco_summary: Optional[Union[_summary__client_pb2.FcoSummary, Mapping]] = ...) -> None: ...

class GetGlobalsForWebUIResponse(_message.Message):
    __slots__ = ["key_values"]
    class KeyValuesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    KEY_VALUES_FIELD_NUMBER: ClassVar[int]
    key_values: _containers.ScalarMap[str, str]
    def __init__(self, key_values: Optional[Mapping[str, str]] = ...) -> None: ...

class GetHiveMetadataRequest(_message.Message):
    __slots__ = ["action", "database", "table"]
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACTION_FIELD_NUMBER: ClassVar[int]
    ACTION_LIST_DATABASES: GetHiveMetadataRequest.Action
    DATABASE_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    action: GetHiveMetadataRequest.Action
    database: str
    table: str
    def __init__(self, action: Optional[Union[GetHiveMetadataRequest.Action, str]] = ..., database: Optional[str] = ..., table: Optional[str] = ...) -> None: ...

class GetHiveMetadataResponse(_message.Message):
    __slots__ = ["databases", "debug_error_message", "error_message", "success"]
    DATABASES_FIELD_NUMBER: ClassVar[int]
    DEBUG_ERROR_MESSAGE_FIELD_NUMBER: ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: ClassVar[int]
    SUCCESS_FIELD_NUMBER: ClassVar[int]
    databases: _hive_metastore__client_pb2.ListHiveResult
    debug_error_message: str
    error_message: str
    success: bool
    def __init__(self, success: bool = ..., error_message: Optional[str] = ..., databases: Optional[Union[_hive_metastore__client_pb2.ListHiveResult, Mapping]] = ..., debug_error_message: Optional[str] = ...) -> None: ...

class GetInternalSparkClusterStatusResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: ClassVar[int]
    status: _internal_spark_cluster_status__client_pb2.InternalSparkClusterStatus
    def __init__(self, status: Optional[Union[_internal_spark_cluster_status__client_pb2.InternalSparkClusterStatus, Mapping]] = ...) -> None: ...

class GetJobDetailsRequest(_message.Message):
    __slots__ = ["tecton_managed_attempt_id"]
    TECTON_MANAGED_ATTEMPT_ID_FIELD_NUMBER: ClassVar[int]
    tecton_managed_attempt_id: _id__client_pb2.Id
    def __init__(self, tecton_managed_attempt_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class GetJobDetailsResponse(_message.Message):
    __slots__ = ["attempt_details", "fco_locator"]
    ATTEMPT_DETAILS_FIELD_NUMBER: ClassVar[int]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    attempt_details: TaskAttemptDetails
    fco_locator: _fco_locator__client_pb2.FcoLocator
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ..., attempt_details: Optional[Union[TaskAttemptDetails, Mapping]] = ...) -> None: ...

class GetJobLogsRequest(_message.Message):
    __slots__ = ["tecton_managed_attempt_id"]
    TECTON_MANAGED_ATTEMPT_ID_FIELD_NUMBER: ClassVar[int]
    tecton_managed_attempt_id: _id__client_pb2.Id
    def __init__(self, tecton_managed_attempt_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class GetJobLogsResponse(_message.Message):
    __slots__ = ["fco_locator", "logs"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    LOGS_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    logs: str
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ..., logs: Optional[str] = ...) -> None: ...

class GetJobStatusRequest(_message.Message):
    __slots__ = ["task_id", "workspace"]
    TASK_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    task_id: _id__client_pb2.Id
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., task_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class GetJobStatusResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: ClassVar[int]
    status: _materialization_status__client_pb2.MaterializationStatus
    def __init__(self, status: Optional[Union[_materialization_status__client_pb2.MaterializationStatus, Mapping]] = ...) -> None: ...

class GetJobsRequest(_message.Message):
    __slots__ = ["duration", "fco_type", "feature_end_time", "feature_services", "feature_start_time", "feature_views", "include_update_materialization_flags", "last_task_state_change", "manually_triggered", "num_attempts", "pagination", "statuses", "task_type", "workspaces", "writes_offline", "writes_online"]
    class FCOTypeFilter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DURATION_FIELD_NUMBER: ClassVar[int]
    FCO_TYPE_FIELD_NUMBER: ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICES_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ONLY: GetJobsRequest.FCOTypeFilter
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEWS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ONLY: GetJobsRequest.FCOTypeFilter
    INCLUDE_UPDATE_MATERIALIZATION_FLAGS_FIELD_NUMBER: ClassVar[int]
    LAST_TASK_STATE_CHANGE_FIELD_NUMBER: ClassVar[int]
    MANUALLY_TRIGGERED_FIELD_NUMBER: ClassVar[int]
    NUM_ATTEMPTS_FIELD_NUMBER: ClassVar[int]
    PAGINATION_FIELD_NUMBER: ClassVar[int]
    STATUSES_FIELD_NUMBER: ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: ClassVar[int]
    UNSPECIFIED: GetJobsRequest.FCOTypeFilter
    WORKSPACES_FIELD_NUMBER: ClassVar[int]
    WRITES_OFFLINE_FIELD_NUMBER: ClassVar[int]
    WRITES_ONLINE_FIELD_NUMBER: ClassVar[int]
    duration: DurationRange
    fco_type: GetJobsRequest.FCOTypeFilter
    feature_end_time: DateTimeRange
    feature_services: _containers.RepeatedScalarFieldContainer[str]
    feature_start_time: DateTimeRange
    feature_views: _containers.RepeatedScalarFieldContainer[str]
    include_update_materialization_flags: bool
    last_task_state_change: DateTimeRange
    manually_triggered: bool
    num_attempts: CountRange
    pagination: PaginationRequest
    statuses: _containers.RepeatedScalarFieldContainer[_materialization_status__client_pb2.MaterializationStatusState]
    task_type: _containers.RepeatedScalarFieldContainer[_spark_cluster__client_pb2.TaskType]
    workspaces: _containers.RepeatedScalarFieldContainer[str]
    writes_offline: bool
    writes_online: bool
    def __init__(self, workspaces: Optional[Iterable[str]] = ..., feature_views: Optional[Iterable[str]] = ..., feature_services: Optional[Iterable[str]] = ..., fco_type: Optional[Union[GetJobsRequest.FCOTypeFilter, str]] = ..., statuses: Optional[Iterable[Union[_materialization_status__client_pb2.MaterializationStatusState, str]]] = ..., last_task_state_change: Optional[Union[DateTimeRange, Mapping]] = ..., task_type: Optional[Iterable[Union[_spark_cluster__client_pb2.TaskType, str]]] = ..., num_attempts: Optional[Union[CountRange, Mapping]] = ..., manually_triggered: bool = ..., duration: Optional[Union[DurationRange, Mapping]] = ..., feature_start_time: Optional[Union[DateTimeRange, Mapping]] = ..., feature_end_time: Optional[Union[DateTimeRange, Mapping]] = ..., include_update_materialization_flags: bool = ..., writes_online: bool = ..., writes_offline: bool = ..., pagination: Optional[Union[PaginationRequest, Mapping]] = ...) -> None: ...

class GetJobsResponse(_message.Message):
    __slots__ = ["pagination", "tasksWithAttempts"]
    PAGINATION_FIELD_NUMBER: ClassVar[int]
    TASKSWITHATTEMPTS_FIELD_NUMBER: ClassVar[int]
    pagination: PaginationResponse
    tasksWithAttempts: _containers.RepeatedCompositeFieldContainer[TaskWithAttempts]
    def __init__(self, tasksWithAttempts: Optional[Iterable[Union[TaskWithAttempts, Mapping]]] = ..., pagination: Optional[Union[PaginationResponse, Mapping]] = ...) -> None: ...

class GetMaterializationRolesAllowlistRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetMaterializationRolesAllowlistResponse(_message.Message):
    __slots__ = ["allowlist", "global_validation_role"]
    ALLOWLIST_FIELD_NUMBER: ClassVar[int]
    GLOBAL_VALIDATION_ROLE_FIELD_NUMBER: ClassVar[int]
    allowlist: _materialization_roles_allowlists__client_pb2.WorkspaceMaterializationRolesAllowlist
    global_validation_role: str
    def __init__(self, allowlist: Optional[Union[_materialization_roles_allowlists__client_pb2.WorkspaceMaterializationRolesAllowlist, Mapping]] = ..., global_validation_role: Optional[str] = ...) -> None: ...

class GetMaterializationStatusRequest(_message.Message):
    __slots__ = ["feature_package_id", "include_deleted", "workspace"]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_package_id: _id__client_pb2.Id
    include_deleted: bool
    workspace: str
    def __init__(self, feature_package_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., workspace: Optional[str] = ..., include_deleted: bool = ...) -> None: ...

class GetMaterializationStatusResponse(_message.Message):
    __slots__ = ["materialization_status"]
    MATERIALIZATION_STATUS_FIELD_NUMBER: ClassVar[int]
    materialization_status: _materialization_status__client_pb2.MaterializationStatus
    def __init__(self, materialization_status: Optional[Union[_materialization_status__client_pb2.MaterializationStatus, Mapping]] = ...) -> None: ...

class GetMaterializingFeatureViewsInLiveWorkspacesResponse(_message.Message):
    __slots__ = ["feature_views"]
    FEATURE_VIEWS_FIELD_NUMBER: ClassVar[int]
    feature_views: _containers.RepeatedCompositeFieldContainer[_feature_view__client_pb2.FeatureView]
    def __init__(self, feature_views: Optional[Iterable[Union[_feature_view__client_pb2.FeatureView, Mapping]]] = ...) -> None: ...

class GetMetricAndExpectationDefinitionRequest(_message.Message):
    __slots__ = ["feature_view_name", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class GetMetricAndExpectationDefinitionResponse(_message.Message):
    __slots__ = ["feature_expectations", "feature_view_name", "metric_expectations", "metrics", "workspace"]
    FEATURE_EXPECTATIONS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    METRICS_FIELD_NUMBER: ClassVar[int]
    METRIC_EXPECTATIONS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_expectations: _containers.RepeatedCompositeFieldContainer[_expectation__client_pb2.FeatureExpectation]
    feature_view_name: str
    metric_expectations: _containers.RepeatedCompositeFieldContainer[_expectation__client_pb2.MetricExpectation]
    metrics: _containers.RepeatedCompositeFieldContainer[_metric__client_pb2.Metric]
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., metrics: Optional[Iterable[Union[_metric__client_pb2.Metric, Mapping]]] = ..., feature_expectations: Optional[Iterable[Union[_expectation__client_pb2.FeatureExpectation, Mapping]]] = ..., metric_expectations: Optional[Iterable[Union[_expectation__client_pb2.MetricExpectation, Mapping]]] = ...) -> None: ...

class GetNewIngestDataframeInfoRequest(_message.Message):
    __slots__ = ["feature_definition_id"]
    FEATURE_DEFINITION_ID_FIELD_NUMBER: ClassVar[int]
    feature_definition_id: _id__client_pb2.Id
    def __init__(self, feature_definition_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class GetNewIngestDataframeInfoResponse(_message.Message):
    __slots__ = ["df_path", "signed_url_for_df_upload"]
    DF_PATH_FIELD_NUMBER: ClassVar[int]
    SIGNED_URL_FOR_DF_UPLOAD_FIELD_NUMBER: ClassVar[int]
    df_path: str
    signed_url_for_df_upload: str
    def __init__(self, df_path: Optional[str] = ..., signed_url_for_df_upload: Optional[str] = ...) -> None: ...

class GetObservabilityConfigRequest(_message.Message):
    __slots__ = ["feature_view_name", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class GetObservabilityConfigResponse(_message.Message):
    __slots__ = ["feature_view_name", "is_dataobs_metric_enabled", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    IS_DATAOBS_METRIC_ENABLED_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    is_dataobs_metric_enabled: bool
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., is_dataobs_metric_enabled: bool = ...) -> None: ...

class GetOfflineStoreCredentialsRequest(_message.Message):
    __slots__ = ["data_source_id", "feature_view_id", "saved_feature_data_frame_id"]
    DATA_SOURCE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    SAVED_FEATURE_DATA_FRAME_ID_FIELD_NUMBER: ClassVar[int]
    data_source_id: _id__client_pb2.Id
    feature_view_id: _id__client_pb2.Id
    saved_feature_data_frame_id: _id__client_pb2.Id
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., data_source_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., saved_feature_data_frame_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class GetOfflineStoreCredentialsResponse(_message.Message):
    __slots__ = ["aws"]
    AWS_FIELD_NUMBER: ClassVar[int]
    aws: _aws_credentials__client_pb2.AwsCredentials
    def __init__(self, aws: Optional[Union[_aws_credentials__client_pb2.AwsCredentials, Mapping]] = ...) -> None: ...

class GetOnboardingStatusRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: str
    def __init__(self, workspace: Optional[str] = ...) -> None: ...

class GetOnboardingStatusResponse(_message.Message):
    __slots__ = ["finish_onboarding", "setup_platform"]
    FINISH_ONBOARDING_FIELD_NUMBER: ClassVar[int]
    SETUP_PLATFORM_FIELD_NUMBER: ClassVar[int]
    finish_onboarding: _onboarding__client_pb2.OnboardingStatusEnum
    setup_platform: _onboarding__client_pb2.OnboardingStatusEnum
    def __init__(self, setup_platform: Optional[Union[_onboarding__client_pb2.OnboardingStatusEnum, str]] = ..., finish_onboarding: Optional[Union[_onboarding__client_pb2.OnboardingStatusEnum, str]] = ...) -> None: ...

class GetRestoreInfoRequest(_message.Message):
    __slots__ = ["commit_id", "workspace"]
    COMMIT_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    commit_id: str
    workspace: str
    def __init__(self, commit_id: Optional[str] = ..., workspace: Optional[str] = ...) -> None: ...

class GetRestoreInfoResponse(_message.Message):
    __slots__ = ["commit_id", "sdk_version", "signed_url_for_repo_download"]
    COMMIT_ID_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    SIGNED_URL_FOR_REPO_DOWNLOAD_FIELD_NUMBER: ClassVar[int]
    commit_id: str
    sdk_version: str
    signed_url_for_repo_download: str
    def __init__(self, signed_url_for_repo_download: Optional[str] = ..., commit_id: Optional[str] = ..., sdk_version: Optional[str] = ...) -> None: ...

class GetSavedFeatureDataFrameRequest(_message.Message):
    __slots__ = ["saved_feature_dataframe_id", "saved_feature_dataframe_name", "workspace"]
    SAVED_FEATURE_DATAFRAME_ID_FIELD_NUMBER: ClassVar[int]
    SAVED_FEATURE_DATAFRAME_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    saved_feature_dataframe_id: _id__client_pb2.Id
    saved_feature_dataframe_name: str
    workspace: str
    def __init__(self, saved_feature_dataframe_name: Optional[str] = ..., saved_feature_dataframe_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., workspace: Optional[str] = ...) -> None: ...

class GetSavedFeatureDataFrameResponse(_message.Message):
    __slots__ = ["saved_feature_dataframe"]
    SAVED_FEATURE_DATAFRAME_FIELD_NUMBER: ClassVar[int]
    saved_feature_dataframe: _saved_feature_data_frame__client_pb2.SavedFeatureDataFrame
    def __init__(self, saved_feature_dataframe: Optional[Union[_saved_feature_data_frame__client_pb2.SavedFeatureDataFrame, Mapping]] = ...) -> None: ...

class GetServiceAccountsRequest(_message.Message):
    __slots__ = ["ids", "search"]
    IDS_FIELD_NUMBER: ClassVar[int]
    SEARCH_FIELD_NUMBER: ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    search: str
    def __init__(self, search: Optional[str] = ..., ids: Optional[Iterable[str]] = ...) -> None: ...

class GetServiceAccountsResponse(_message.Message):
    __slots__ = ["service_accounts"]
    SERVICE_ACCOUNTS_FIELD_NUMBER: ClassVar[int]
    service_accounts: _containers.RepeatedCompositeFieldContainer[ServiceAccount]
    def __init__(self, service_accounts: Optional[Iterable[Union[ServiceAccount, Mapping]]] = ...) -> None: ...

class GetServingStatusRequest(_message.Message):
    __slots__ = ["feature_package_id", "feature_service_id", "workspace"]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_package_id: _id__client_pb2.Id
    feature_service_id: _id__client_pb2.Id
    workspace: str
    def __init__(self, feature_package_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., workspace: Optional[str] = ...) -> None: ...

class GetServingStatusResponse(_message.Message):
    __slots__ = ["serving_status_summary"]
    SERVING_STATUS_SUMMARY_FIELD_NUMBER: ClassVar[int]
    serving_status_summary: _serving_status__client_pb2.ServingStatusSummary
    def __init__(self, serving_status_summary: Optional[Union[_serving_status__client_pb2.ServingStatusSummary, Mapping]] = ...) -> None: ...

class GetSparkConfigRequest(_message.Message):
    __slots__ = ["feature_view_name", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    feature_view_name: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class GetSparkConfigResponse(_message.Message):
    __slots__ = ["batch_config", "stream_config"]
    BATCH_CONFIG_FIELD_NUMBER: ClassVar[int]
    STREAM_CONFIG_FIELD_NUMBER: ClassVar[int]
    batch_config: SparkClusterConfig
    stream_config: SparkClusterConfig
    def __init__(self, batch_config: Optional[Union[SparkClusterConfig, Mapping]] = ..., stream_config: Optional[Union[SparkClusterConfig, Mapping]] = ...) -> None: ...

class GetStateUpdateLogRequest(_message.Message):
    __slots__ = ["limit", "workspace"]
    LIMIT_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    limit: int
    workspace: str
    def __init__(self, limit: Optional[int] = ..., workspace: Optional[str] = ...) -> None: ...

class GetStateUpdateLogResponse(_message.Message):
    __slots__ = ["entries"]
    ENTRIES_FIELD_NUMBER: ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_state_update__client_pb2.StateUpdateEntry]
    def __init__(self, entries: Optional[Iterable[Union[_state_update__client_pb2.StateUpdateEntry, Mapping]]] = ...) -> None: ...

class GetStateUpdatePlanListRequest(_message.Message):
    __slots__ = ["limit", "workspace"]
    LIMIT_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    limit: int
    workspace: str
    def __init__(self, limit: Optional[int] = ..., workspace: Optional[str] = ...) -> None: ...

class GetStateUpdatePlanListResponse(_message.Message):
    __slots__ = ["entries"]
    ENTRIES_FIELD_NUMBER: ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_state_update__client_pb2.StateUpdateEntry]
    def __init__(self, entries: Optional[Iterable[Union[_state_update__client_pb2.StateUpdateEntry, Mapping]]] = ...) -> None: ...

class GetStateUpdatePlanSummaryRequest(_message.Message):
    __slots__ = ["plan_id"]
    PLAN_ID_FIELD_NUMBER: ClassVar[int]
    plan_id: _id__client_pb2.Id
    def __init__(self, plan_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class GetStateUpdatePlanSummaryResponse(_message.Message):
    __slots__ = ["plan"]
    PLAN_FIELD_NUMBER: ClassVar[int]
    plan: _state_update__client_pb2.StateUpdatePlanSummary
    def __init__(self, plan: Optional[Union[_state_update__client_pb2.StateUpdatePlanSummary, Mapping]] = ...) -> None: ...

class GetTransformationRequest(_message.Message):
    __slots__ = ["name", "run_object_version_check", "transformation_id", "workspace"]
    NAME_FIELD_NUMBER: ClassVar[int]
    RUN_OBJECT_VERSION_CHECK_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    name: str
    run_object_version_check: bool
    transformation_id: _id__client_pb2.Id
    workspace: str
    def __init__(self, transformation_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., name: Optional[str] = ..., workspace: Optional[str] = ..., run_object_version_check: bool = ...) -> None: ...

class GetTransformationResponse(_message.Message):
    __slots__ = ["fco_container"]
    FCO_CONTAINER_FIELD_NUMBER: ClassVar[int]
    fco_container: _fco__client_pb2.FcoContainer
    def __init__(self, fco_container: Optional[Union[_fco__client_pb2.FcoContainer, Mapping]] = ...) -> None: ...

class GetTransformationSummaryRequest(_message.Message):
    __slots__ = ["fco_locator"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ...) -> None: ...

class GetTransformationSummaryResponse(_message.Message):
    __slots__ = ["fco_summary"]
    FCO_SUMMARY_FIELD_NUMBER: ClassVar[int]
    fco_summary: _summary__client_pb2.FcoSummary
    def __init__(self, fco_summary: Optional[Union[_summary__client_pb2.FcoSummary, Mapping]] = ...) -> None: ...

class GetUserDeploymentSettingsResponse(_message.Message):
    __slots__ = ["user_deployment_settings"]
    USER_DEPLOYMENT_SETTINGS_FIELD_NUMBER: ClassVar[int]
    user_deployment_settings: _user_deployment_settings__client_pb2.UserDeploymentSettings
    def __init__(self, user_deployment_settings: Optional[Union[_user_deployment_settings__client_pb2.UserDeploymentSettings, Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ["email", "id"]
    EMAIL_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    email: str
    id: str
    def __init__(self, id: Optional[str] = ..., email: Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: ClassVar[int]
    user: _principal__client_pb2.UserBasic
    def __init__(self, user: Optional[Union[_principal__client_pb2.UserBasic, Mapping]] = ...) -> None: ...

class GetVirtualDataSourceRequest(_message.Message):
    __slots__ = ["name", "run_object_version_check", "virtual_data_source_id", "workspace"]
    NAME_FIELD_NUMBER: ClassVar[int]
    RUN_OBJECT_VERSION_CHECK_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCE_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    name: str
    run_object_version_check: bool
    virtual_data_source_id: _id__client_pb2.Id
    workspace: str
    def __init__(self, virtual_data_source_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., name: Optional[str] = ..., workspace: Optional[str] = ..., run_object_version_check: bool = ...) -> None: ...

class GetVirtualDataSourceResponse(_message.Message):
    __slots__ = ["fco_container"]
    FCO_CONTAINER_FIELD_NUMBER: ClassVar[int]
    fco_container: _fco__client_pb2.FcoContainer
    def __init__(self, fco_container: Optional[Union[_fco__client_pb2.FcoContainer, Mapping]] = ...) -> None: ...

class GetVirtualDataSourceSummaryRequest(_message.Message):
    __slots__ = ["fco_locator"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ...) -> None: ...

class GetVirtualDataSourceSummaryResponse(_message.Message):
    __slots__ = ["fco_summary"]
    FCO_SUMMARY_FIELD_NUMBER: ClassVar[int]
    fco_summary: _summary__client_pb2.FcoSummary
    def __init__(self, fco_summary: Optional[Union[_summary__client_pb2.FcoSummary, Mapping]] = ...) -> None: ...

class GetWorkspaceRequest(_message.Message):
    __slots__ = ["workspace_name"]
    WORKSPACE_NAME_FIELD_NUMBER: ClassVar[int]
    workspace_name: str
    def __init__(self, workspace_name: Optional[str] = ...) -> None: ...

class GetWorkspaceResponse(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    workspace: _workspace__client_pb2.Workspace
    def __init__(self, workspace: Optional[Union[_workspace__client_pb2.Workspace, Mapping]] = ...) -> None: ...

class GlobalSearchRequest(_message.Message):
    __slots__ = ["current_workspace", "fco_type_filters", "materialization_offline_filter", "materialization_online_filter", "owner_filters", "text", "workspace_filters", "workspace_live_filter"]
    CURRENT_WORKSPACE_FIELD_NUMBER: ClassVar[int]
    FCO_TYPE_FILTERS_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_OFFLINE_FILTER_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_ONLINE_FILTER_FIELD_NUMBER: ClassVar[int]
    OWNER_FILTERS_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FILTERS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_LIVE_FILTER_FIELD_NUMBER: ClassVar[int]
    current_workspace: str
    fco_type_filters: _containers.RepeatedScalarFieldContainer[FcoType]
    materialization_offline_filter: MaterializationEnabledSearchFilter
    materialization_online_filter: MaterializationEnabledSearchFilter
    owner_filters: _containers.RepeatedScalarFieldContainer[str]
    text: str
    workspace_filters: _containers.RepeatedScalarFieldContainer[str]
    workspace_live_filter: WorkspaceCapabilitiesFilter
    def __init__(self, text: Optional[str] = ..., current_workspace: Optional[str] = ..., fco_type_filters: Optional[Iterable[Union[FcoType, str]]] = ..., workspace_filters: Optional[Iterable[str]] = ..., owner_filters: Optional[Iterable[str]] = ..., materialization_offline_filter: Optional[Union[MaterializationEnabledSearchFilter, str]] = ..., materialization_online_filter: Optional[Union[MaterializationEnabledSearchFilter, str]] = ..., workspace_live_filter: Optional[Union[WorkspaceCapabilitiesFilter, str]] = ...) -> None: ...

class GlobalSearchResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[GlobalSearchResult]
    def __init__(self, results: Optional[Iterable[Union[GlobalSearchResult, Mapping]]] = ...) -> None: ...

class GlobalSearchResult(_message.Message):
    __slots__ = ["fco_result", "filter_result"]
    FCO_RESULT_FIELD_NUMBER: ClassVar[int]
    FILTER_RESULT_FIELD_NUMBER: ClassVar[int]
    fco_result: FcoSearchResult
    filter_result: FilterSearchResult
    def __init__(self, fco_result: Optional[Union[FcoSearchResult, Mapping]] = ..., filter_result: Optional[Union[FilterSearchResult, Mapping]] = ...) -> None: ...

class IngestAnalyticsRequest(_message.Message):
    __slots__ = ["events", "workspace"]
    EVENTS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_amplitude__client_pb2.AmplitudeEvent]
    workspace: str
    def __init__(self, events: Optional[Iterable[Union[_amplitude__client_pb2.AmplitudeEvent, Mapping]]] = ..., workspace: Optional[str] = ...) -> None: ...

class IngestClientLogsRequest(_message.Message):
    __slots__ = ["sdk_method_invocation"]
    SDK_METHOD_INVOCATION_FIELD_NUMBER: ClassVar[int]
    sdk_method_invocation: _client_logging__client_pb2.SDKMethodInvocation
    def __init__(self, sdk_method_invocation: Optional[Union[_client_logging__client_pb2.SDKMethodInvocation, Mapping]] = ...) -> None: ...

class IngestDataframeRequest(_message.Message):
    __slots__ = ["df_path", "feature_definition_id", "workspace"]
    DF_PATH_FIELD_NUMBER: ClassVar[int]
    FEATURE_DEFINITION_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    df_path: str
    feature_definition_id: _id__client_pb2.Id
    workspace: str
    def __init__(self, feature_definition_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., df_path: Optional[str] = ..., workspace: Optional[str] = ...) -> None: ...

class IngestDataframeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class IntrospectApiKeyRequest(_message.Message):
    __slots__ = ["api_key"]
    API_KEY_FIELD_NUMBER: ClassVar[int]
    api_key: str
    def __init__(self, api_key: Optional[str] = ...) -> None: ...

class IntrospectApiKeyResponse(_message.Message):
    __slots__ = ["active", "created_by", "description", "id", "is_admin", "name"]
    ACTIVE_FIELD_NUMBER: ClassVar[int]
    CREATED_BY_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IS_ADMIN_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    active: bool
    created_by: str
    description: str
    id: _id__client_pb2.Id
    is_admin: bool
    name: str
    def __init__(self, id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., description: Optional[str] = ..., created_by: Optional[str] = ..., active: bool = ..., is_admin: bool = ..., name: Optional[str] = ...) -> None: ...

class JobsKeySet(_message.Message):
    __slots__ = ["comparison", "id", "updated_at"]
    COMPARISON_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: ClassVar[int]
    comparison: int
    id: _id__client_pb2.Id
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, updated_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., comparison: Optional[int] = ..., id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class ListApiKeysRequest(_message.Message):
    __slots__ = ["include_archived"]
    INCLUDE_ARCHIVED_FIELD_NUMBER: ClassVar[int]
    include_archived: bool
    def __init__(self, include_archived: bool = ...) -> None: ...

class ListApiKeysResponse(_message.Message):
    __slots__ = ["api_keys"]
    API_KEYS_FIELD_NUMBER: ClassVar[int]
    api_keys: _containers.RepeatedCompositeFieldContainer[_tecton_api_key__client_pb2.TectonApiKey]
    def __init__(self, api_keys: Optional[Iterable[Union[_tecton_api_key__client_pb2.TectonApiKey, Mapping]]] = ...) -> None: ...

class ListWorkspacesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListWorkspacesResponse(_message.Message):
    __slots__ = ["workspaces"]
    WORKSPACES_FIELD_NUMBER: ClassVar[int]
    workspaces: _containers.RepeatedCompositeFieldContainer[_workspace__client_pb2.Workspace]
    def __init__(self, workspaces: Optional[Iterable[Union[_workspace__client_pb2.Workspace, Mapping]]] = ...) -> None: ...

class NewStateUpdateRequest(_message.Message):
    __slots__ = ["blocking_dry_run_mode", "enable_eager_response", "request"]
    BLOCKING_DRY_RUN_MODE_FIELD_NUMBER: ClassVar[int]
    ENABLE_EAGER_RESPONSE_FIELD_NUMBER: ClassVar[int]
    REQUEST_FIELD_NUMBER: ClassVar[int]
    blocking_dry_run_mode: bool
    enable_eager_response: bool
    request: _state_update__client_pb2.StateUpdateRequest
    def __init__(self, request: Optional[Union[_state_update__client_pb2.StateUpdateRequest, Mapping]] = ..., blocking_dry_run_mode: bool = ..., enable_eager_response: bool = ...) -> None: ...

class NewStateUpdateRequestV2(_message.Message):
    __slots__ = ["blocking_dry_run_mode", "enable_eager_response", "json_output", "no_color", "request", "suppress_warnings"]
    BLOCKING_DRY_RUN_MODE_FIELD_NUMBER: ClassVar[int]
    ENABLE_EAGER_RESPONSE_FIELD_NUMBER: ClassVar[int]
    JSON_OUTPUT_FIELD_NUMBER: ClassVar[int]
    NO_COLOR_FIELD_NUMBER: ClassVar[int]
    REQUEST_FIELD_NUMBER: ClassVar[int]
    SUPPRESS_WARNINGS_FIELD_NUMBER: ClassVar[int]
    blocking_dry_run_mode: bool
    enable_eager_response: bool
    json_output: bool
    no_color: bool
    request: _state_update__client_pb2.StateUpdateRequest
    suppress_warnings: bool
    def __init__(self, request: Optional[Union[_state_update__client_pb2.StateUpdateRequest, Mapping]] = ..., blocking_dry_run_mode: bool = ..., enable_eager_response: bool = ..., no_color: bool = ..., json_output: bool = ..., suppress_warnings: bool = ...) -> None: ...

class NewStateUpdateResponse(_message.Message):
    __slots__ = ["eager_response", "signed_url_for_repo_upload", "state_id"]
    EAGER_RESPONSE_FIELD_NUMBER: ClassVar[int]
    SIGNED_URL_FOR_REPO_UPLOAD_FIELD_NUMBER: ClassVar[int]
    STATE_ID_FIELD_NUMBER: ClassVar[int]
    eager_response: QueryStateUpdateResponse
    signed_url_for_repo_upload: str
    state_id: _id__client_pb2.Id
    def __init__(self, state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., signed_url_for_repo_upload: Optional[str] = ..., eager_response: Optional[Union[QueryStateUpdateResponse, Mapping]] = ...) -> None: ...

class NewStateUpdateResponseV2(_message.Message):
    __slots__ = ["eager_response", "signed_url_for_repo_upload", "state_id"]
    EAGER_RESPONSE_FIELD_NUMBER: ClassVar[int]
    SIGNED_URL_FOR_REPO_UPLOAD_FIELD_NUMBER: ClassVar[int]
    STATE_ID_FIELD_NUMBER: ClassVar[int]
    eager_response: QueryStateUpdateResponseV2
    signed_url_for_repo_upload: str
    state_id: _id__client_pb2.Id
    def __init__(self, state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., signed_url_for_repo_upload: Optional[str] = ..., eager_response: Optional[Union[QueryStateUpdateResponseV2, Mapping]] = ...) -> None: ...

class PaginationRequest(_message.Message):
    __slots__ = ["page", "page_token", "per_page", "sort_direction", "sort_key"]
    PAGE_FIELD_NUMBER: ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: ClassVar[int]
    PER_PAGE_FIELD_NUMBER: ClassVar[int]
    SORT_DIRECTION_FIELD_NUMBER: ClassVar[int]
    SORT_KEY_FIELD_NUMBER: ClassVar[int]
    page: int
    page_token: str
    per_page: int
    sort_direction: SortDirection
    sort_key: str
    def __init__(self, page: Optional[int] = ..., per_page: Optional[int] = ..., sort_key: Optional[str] = ..., sort_direction: Optional[Union[SortDirection, str]] = ..., page_token: Optional[str] = ...) -> None: ...

class PaginationResponse(_message.Message):
    __slots__ = ["next_page_token", "page", "per_page", "sort_direction", "sort_key", "total"]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: ClassVar[int]
    PAGE_FIELD_NUMBER: ClassVar[int]
    PER_PAGE_FIELD_NUMBER: ClassVar[int]
    SORT_DIRECTION_FIELD_NUMBER: ClassVar[int]
    SORT_KEY_FIELD_NUMBER: ClassVar[int]
    TOTAL_FIELD_NUMBER: ClassVar[int]
    next_page_token: str
    page: int
    per_page: int
    sort_direction: SortDirection
    sort_key: str
    total: int
    def __init__(self, page: Optional[int] = ..., per_page: Optional[int] = ..., total: Optional[int] = ..., next_page_token: Optional[str] = ..., sort_key: Optional[str] = ..., sort_direction: Optional[Union[SortDirection, str]] = ...) -> None: ...

class QueryFeatureViewsRequest(_message.Message):
    __slots__ = ["name", "workspace"]
    NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    name: str
    workspace: str
    def __init__(self, name: Optional[str] = ..., workspace: Optional[str] = ...) -> None: ...

class QueryFeatureViewsResponse(_message.Message):
    __slots__ = ["fco_container"]
    FCO_CONTAINER_FIELD_NUMBER: ClassVar[int]
    fco_container: _fco__client_pb2.FcoContainer
    def __init__(self, fco_container: Optional[Union[_fco__client_pb2.FcoContainer, Mapping]] = ...) -> None: ...

class QueryMetricRequest(_message.Message):
    __slots__ = ["end_time", "feature_view_name", "limit", "metric_type", "start_time", "workspace"]
    END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    LIMIT_FIELD_NUMBER: ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: ClassVar[int]
    START_TIME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    end_time: _timestamp_pb2.Timestamp
    feature_view_name: str
    limit: int
    metric_type: _metric__client_pb2.MetricType
    start_time: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., metric_type: Optional[Union[_metric__client_pb2.MetricType, str]] = ..., start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., limit: Optional[int] = ...) -> None: ...

class QueryMetricResponse(_message.Message):
    __slots__ = ["aligned_end_time", "aligned_start_time", "column_names", "feature_view_name", "metric_data", "metric_data_point_interval", "metric_type", "workspace"]
    ALIGNED_END_TIME_FIELD_NUMBER: ClassVar[int]
    ALIGNED_START_TIME_FIELD_NUMBER: ClassVar[int]
    COLUMN_NAMES_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    METRIC_DATA_FIELD_NUMBER: ClassVar[int]
    METRIC_DATA_POINT_INTERVAL_FIELD_NUMBER: ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    aligned_end_time: _timestamp_pb2.Timestamp
    aligned_start_time: _timestamp_pb2.Timestamp
    column_names: _containers.RepeatedScalarFieldContainer[str]
    feature_view_name: str
    metric_data: _containers.RepeatedCompositeFieldContainer[_metric__client_pb2.MetricDataPoint]
    metric_data_point_interval: _duration_pb2.Duration
    metric_type: _metric__client_pb2.MetricType
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., feature_view_name: Optional[str] = ..., metric_type: Optional[Union[_metric__client_pb2.MetricType, str]] = ..., metric_data_point_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., aligned_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., aligned_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., metric_data: Optional[Iterable[Union[_metric__client_pb2.MetricDataPoint, Mapping]]] = ..., column_names: Optional[Iterable[str]] = ...) -> None: ...

class QueryStateUpdateRequest(_message.Message):
    __slots__ = ["state_id", "workspace"]
    STATE_ID_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    state_id: _id__client_pb2.Id
    workspace: str
    def __init__(self, state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., workspace: Optional[str] = ...) -> None: ...

class QueryStateUpdateRequestV2(_message.Message):
    __slots__ = ["json_output", "no_color", "state_id", "suppress_warnings", "workspace"]
    JSON_OUTPUT_FIELD_NUMBER: ClassVar[int]
    NO_COLOR_FIELD_NUMBER: ClassVar[int]
    STATE_ID_FIELD_NUMBER: ClassVar[int]
    SUPPRESS_WARNINGS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    json_output: bool
    no_color: bool
    state_id: _id__client_pb2.Id
    suppress_warnings: bool
    workspace: str
    def __init__(self, state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., workspace: Optional[str] = ..., no_color: bool = ..., json_output: bool = ..., suppress_warnings: bool = ...) -> None: ...

class QueryStateUpdateResponse(_message.Message):
    __slots__ = ["diff_items", "error", "latest_status_message", "ready", "recreates_suppressed", "success", "validation_result"]
    DIFF_ITEMS_FIELD_NUMBER: ClassVar[int]
    ERROR_FIELD_NUMBER: ClassVar[int]
    LATEST_STATUS_MESSAGE_FIELD_NUMBER: ClassVar[int]
    READY_FIELD_NUMBER: ClassVar[int]
    RECREATES_SUPPRESSED_FIELD_NUMBER: ClassVar[int]
    SUCCESS_FIELD_NUMBER: ClassVar[int]
    VALIDATION_RESULT_FIELD_NUMBER: ClassVar[int]
    diff_items: _containers.RepeatedCompositeFieldContainer[_state_update__client_pb2.FcoDiff]
    error: str
    latest_status_message: str
    ready: bool
    recreates_suppressed: bool
    success: bool
    validation_result: _state_update__client_pb2.ValidationResult
    def __init__(self, ready: bool = ..., success: bool = ..., error: Optional[str] = ..., recreates_suppressed: bool = ..., validation_result: Optional[Union[_state_update__client_pb2.ValidationResult, Mapping]] = ..., diff_items: Optional[Iterable[Union[_state_update__client_pb2.FcoDiff, Mapping]]] = ..., latest_status_message: Optional[str] = ...) -> None: ...

class QueryStateUpdateResponseV2(_message.Message):
    __slots__ = ["applied_at", "applied_by", "applied_by_principal", "created_at", "created_by", "error", "latest_status_message", "ready", "sdk_version", "success", "successful_plan_output", "validation_errors", "workspace"]
    APPLIED_AT_FIELD_NUMBER: ClassVar[int]
    APPLIED_BY_FIELD_NUMBER: ClassVar[int]
    APPLIED_BY_PRINCIPAL_FIELD_NUMBER: ClassVar[int]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    CREATED_BY_FIELD_NUMBER: ClassVar[int]
    ERROR_FIELD_NUMBER: ClassVar[int]
    LATEST_STATUS_MESSAGE_FIELD_NUMBER: ClassVar[int]
    READY_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    SUCCESSFUL_PLAN_OUTPUT_FIELD_NUMBER: ClassVar[int]
    SUCCESS_FIELD_NUMBER: ClassVar[int]
    VALIDATION_ERRORS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    applied_at: _timestamp_pb2.Timestamp
    applied_by: str
    applied_by_principal: _principal__client_pb2.PrincipalBasic
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    error: str
    latest_status_message: str
    ready: bool
    sdk_version: str
    success: bool
    successful_plan_output: _state_update__client_pb2.SuccessfulPlanOutput
    validation_errors: _state_update__client_pb2.ValidationResult
    workspace: str
    def __init__(self, ready: bool = ..., success: bool = ..., error: Optional[str] = ..., latest_status_message: Optional[str] = ..., validation_errors: Optional[Union[_state_update__client_pb2.ValidationResult, Mapping]] = ..., successful_plan_output: Optional[Union[_state_update__client_pb2.SuccessfulPlanOutput, Mapping]] = ..., applied_by: Optional[str] = ..., applied_by_principal: Optional[Union[_principal__client_pb2.PrincipalBasic, Mapping]] = ..., applied_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., workspace: Optional[str] = ..., sdk_version: Optional[str] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., created_by: Optional[str] = ...) -> None: ...

class RestartMaterializationTaskRequest(_message.Message):
    __slots__ = ["materialization_task_id"]
    MATERIALIZATION_TASK_ID_FIELD_NUMBER: ClassVar[int]
    materialization_task_id: _id__client_pb2.Id
    def __init__(self, materialization_task_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class RestartMaterializationTaskResponse(_message.Message):
    __slots__ = ["error_message", "new_materialization_task_id"]
    ERROR_MESSAGE_FIELD_NUMBER: ClassVar[int]
    NEW_MATERIALIZATION_TASK_ID_FIELD_NUMBER: ClassVar[int]
    error_message: str
    new_materialization_task_id: _id__client_pb2.Id
    def __init__(self, error_message: Optional[str] = ..., new_materialization_task_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class ServiceAccount(_message.Message):
    __slots__ = ["created_at", "created_by", "description", "id", "is_active", "name"]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    CREATED_BY_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    created_by: _principal__client_pb2.PrincipalBasic
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., description: Optional[str] = ..., is_active: bool = ..., created_by: Optional[Union[_principal__client_pb2.PrincipalBasic, Mapping]] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class SetFeatureServerConfigRequest(_message.Message):
    __slots__ = ["autoScalingConfig", "count"]
    AUTOSCALINGCONFIG_FIELD_NUMBER: ClassVar[int]
    COUNT_FIELD_NUMBER: ClassVar[int]
    autoScalingConfig: FeatureServerAutoScalingConfig
    count: int
    def __init__(self, count: Optional[int] = ..., autoScalingConfig: Optional[Union[FeatureServerAutoScalingConfig, Mapping]] = ...) -> None: ...

class SparkClusterConfig(_message.Message):
    __slots__ = ["final", "original"]
    FINAL_FIELD_NUMBER: ClassVar[int]
    ORIGINAL_FIELD_NUMBER: ClassVar[int]
    final: str
    original: str
    def __init__(self, original: Optional[str] = ..., final: Optional[str] = ...) -> None: ...

class SuggestGlobalSearchFiltersRequest(_message.Message):
    __slots__ = ["filter_type", "text"]
    FILTER_TYPE_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    filter_type: FilterField
    text: str
    def __init__(self, text: Optional[str] = ..., filter_type: Optional[Union[FilterField, str]] = ...) -> None: ...

class SuggestGlobalSearchFiltersResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[GlobalSearchResult]
    def __init__(self, results: Optional[Iterable[Union[GlobalSearchResult, Mapping]]] = ...) -> None: ...

class TaskAttemptDetails(_message.Message):
    __slots__ = ["anyscale_url", "attempt_status", "cluster_config", "feature_end_time", "feature_start_time", "run_details", "task_id", "task_state", "task_type"]
    ANYSCALE_URL_FIELD_NUMBER: ClassVar[int]
    ATTEMPT_STATUS_FIELD_NUMBER: ClassVar[int]
    CLUSTER_CONFIG_FIELD_NUMBER: ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    RUN_DETAILS_FIELD_NUMBER: ClassVar[int]
    TASK_ID_FIELD_NUMBER: ClassVar[int]
    TASK_STATE_FIELD_NUMBER: ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: ClassVar[int]
    anyscale_url: str
    attempt_status: _materialization_status__client_pb2.MaterializationAttemptStatus
    cluster_config: _feature_view__client_pb2.RiftClusterConfig
    feature_end_time: _timestamp_pb2.Timestamp
    feature_start_time: _timestamp_pb2.Timestamp
    run_details: _job_metadata__client_pb2.TectonManagedInfo
    task_id: _id__client_pb2.Id
    task_state: _materialization_status__client_pb2.MaterializationStatusState
    task_type: _spark_cluster__client_pb2.TaskType
    def __init__(self, task_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., task_type: Optional[Union[_spark_cluster__client_pb2.TaskType, str]] = ..., task_state: Optional[Union[_materialization_status__client_pb2.MaterializationStatusState, str]] = ..., attempt_status: Optional[Union[_materialization_status__client_pb2.MaterializationAttemptStatus, Mapping]] = ..., run_details: Optional[Union[_job_metadata__client_pb2.TectonManagedInfo, Mapping]] = ..., cluster_config: Optional[Union[_feature_view__client_pb2.RiftClusterConfig, Mapping]] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., anyscale_url: Optional[str] = ...) -> None: ...

class TaskWithAttempts(_message.Message):
    __slots__ = ["fco_locator", "feature_end_time", "feature_service_name", "feature_start_time", "feature_view_name", "last_task_state_change", "manually_triggered", "materialization_status", "taskState", "task_id", "task_type"]
    FCO_LOCATOR_FIELD_NUMBER: ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    LAST_TASK_STATE_CHANGE_FIELD_NUMBER: ClassVar[int]
    MANUALLY_TRIGGERED_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_STATUS_FIELD_NUMBER: ClassVar[int]
    TASKSTATE_FIELD_NUMBER: ClassVar[int]
    TASK_ID_FIELD_NUMBER: ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: ClassVar[int]
    fco_locator: _fco_locator__client_pb2.FcoLocator
    feature_end_time: _timestamp_pb2.Timestamp
    feature_service_name: str
    feature_start_time: _timestamp_pb2.Timestamp
    feature_view_name: str
    last_task_state_change: _timestamp_pb2.Timestamp
    manually_triggered: bool
    materialization_status: _materialization_status__client_pb2.MaterializationStatus
    taskState: _materialization_status__client_pb2.MaterializationStatusState
    task_id: _id__client_pb2.Id
    task_type: _spark_cluster__client_pb2.TaskType
    def __init__(self, fco_locator: Optional[Union[_fco_locator__client_pb2.FcoLocator, Mapping]] = ..., taskState: Optional[Union[_materialization_status__client_pb2.MaterializationStatusState, str]] = ..., materialization_status: Optional[Union[_materialization_status__client_pb2.MaterializationStatus, Mapping]] = ..., task_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., task_type: Optional[Union[_spark_cluster__client_pb2.TaskType, str]] = ..., manually_triggered: bool = ..., last_task_state_change: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_view_name: Optional[str] = ..., feature_service_name: Optional[str] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class UpdateServiceAccountRequest(_message.Message):
    __slots__ = ["description", "id", "is_active", "name"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., description: Optional[str] = ..., is_active: bool = ...) -> None: ...

class UpdateServiceAccountResponse(_message.Message):
    __slots__ = ["created_at", "description", "id", "is_active", "name"]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., description: Optional[str] = ..., is_active: bool = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class UpdateUserDeploymentSettingsRequest(_message.Message):
    __slots__ = ["field_mask", "user_deployment_settings"]
    FIELD_MASK_FIELD_NUMBER: ClassVar[int]
    USER_DEPLOYMENT_SETTINGS_FIELD_NUMBER: ClassVar[int]
    field_mask: _field_mask_pb2.FieldMask
    user_deployment_settings: _user_deployment_settings__client_pb2.UserDeploymentSettings
    def __init__(self, user_deployment_settings: Optional[Union[_user_deployment_settings__client_pb2.UserDeploymentSettings, Mapping]] = ..., field_mask: Optional[Union[_field_mask_pb2.FieldMask, Mapping]] = ...) -> None: ...

class UpdateUserDeploymentSettingsResponse(_message.Message):
    __slots__ = ["error_message", "success"]
    ERROR_MESSAGE_FIELD_NUMBER: ClassVar[int]
    SUCCESS_FIELD_NUMBER: ClassVar[int]
    error_message: str
    success: bool
    def __init__(self, success: bool = ..., error_message: Optional[str] = ...) -> None: ...

class ValidateLocalFcoRequest(_message.Message):
    __slots__ = ["sdk_version", "validation_request"]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    VALIDATION_REQUEST_FIELD_NUMBER: ClassVar[int]
    sdk_version: str
    validation_request: _validator__client_pb2.ValidationRequest
    def __init__(self, validation_request: Optional[Union[_validator__client_pb2.ValidationRequest, Mapping]] = ..., sdk_version: Optional[str] = ...) -> None: ...

class ValidateLocalFcoResponse(_message.Message):
    __slots__ = ["error", "success", "validation_result"]
    ERROR_FIELD_NUMBER: ClassVar[int]
    SUCCESS_FIELD_NUMBER: ClassVar[int]
    VALIDATION_RESULT_FIELD_NUMBER: ClassVar[int]
    error: str
    success: bool
    validation_result: _state_update__client_pb2.ValidationResult
    def __init__(self, success: bool = ..., validation_result: Optional[Union[_state_update__client_pb2.ValidationResult, Mapping]] = ..., error: Optional[str] = ...) -> None: ...

class ValidationResultToken(_message.Message):
    __slots__ = ["expectation_name", "result_id", "validation_time"]
    EXPECTATION_NAME_FIELD_NUMBER: ClassVar[int]
    RESULT_ID_FIELD_NUMBER: ClassVar[int]
    VALIDATION_TIME_FIELD_NUMBER: ClassVar[int]
    expectation_name: str
    result_id: _id__client_pb2.Id
    validation_time: _timestamp_pb2.Timestamp
    def __init__(self, validation_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., result_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., expectation_name: Optional[str] = ...) -> None: ...

class SortDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MaterializationEnabledSearchFilter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class WorkspaceCapabilitiesFilter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FcoType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FilterField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
