from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import fco_args__client_pb2 as _fco_args__client_pb2
from tecton_proto.args import repo_metadata__client_pb2 as _repo_metadata__client_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

AUTO: PlanIntegrationTestSelectType
CREATE: FcoTransitionType
DELETE: FcoTransitionType
DESCRIPTOR: _descriptor.FileDescriptor
JOB_STATUS_CANCELLED: IntegrationTestJobStatus
JOB_STATUS_FAILED: IntegrationTestJobStatus
JOB_STATUS_NOT_STARTED: IntegrationTestJobStatus
JOB_STATUS_RUNNING: IntegrationTestJobStatus
JOB_STATUS_SUCCEED: IntegrationTestJobStatus
JOB_STATUS_UNSPECIFIED: IntegrationTestJobStatus
MATERIALIZATION_TASK_DIFF_DESTINATION_BULK_LOAD_ONLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_OFFLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_ONLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_ONLINE_AND_OFFLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_UNSPECIFIED: MaterializationTaskDiffDestination
NONE: PlanIntegrationTestSelectType
PLAN_APPLIED: PlanStatusType
PLAN_APPLY_FAILED: PlanStatusType
PLAN_CREATED: PlanStatusType
PLAN_INTEGRATION_TESTS_CANCELLED: PlanStatusType
PLAN_INTEGRATION_TESTS_FAILED: PlanStatusType
PLAN_INTEGRATION_TESTS_NOT_STARTED: PlanStatusType
PLAN_INTEGRATION_TESTS_RUNNING: PlanStatusType
PLAN_INTEGRATION_TESTS_SKIPPED: PlanStatusType
PLAN_INTEGRATION_TESTS_SUCCEED: PlanStatusType
PLAN_UNSPECIFIED: PlanStatusType
RECREATE: FcoTransitionType
RESTART_STREAM_CHECKPOINTS_INVALIDATED: FcoTransitionSideEffectStreamRestartType
RESTART_STREAM_NONE: FcoTransitionSideEffectStreamRestartType
RESTART_STREAM_REUSE_CHECKPOINTS: FcoTransitionSideEffectStreamRestartType
SELECTED_FEATURE_VIEWS: PlanIntegrationTestSelectType
UNCHANGED: FcoTransitionType
UNKNOWN: FcoTransitionType
UNSPECIFIED: PlanIntegrationTestSelectType
UPDATE: FcoTransitionType
UPGRADE: FcoTransitionType

class BackfillFeaturePublishTaskDiff(_message.Message):
    __slots__ = ["display_string", "feature_end_time", "feature_start_time", "number_of_jobs"]
    DISPLAY_STRING_FIELD_NUMBER: ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    NUMBER_OF_JOBS_FIELD_NUMBER: ClassVar[int]
    display_string: str
    feature_end_time: _timestamp_pb2.Timestamp
    feature_start_time: _timestamp_pb2.Timestamp
    number_of_jobs: int
    def __init__(self, display_string: Optional[str] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., number_of_jobs: Optional[int] = ...) -> None: ...

class BackfillMaterializationTaskDiff(_message.Message):
    __slots__ = ["destination", "display_string", "feature_end_time", "feature_start_time", "number_of_jobs"]
    DESTINATION_FIELD_NUMBER: ClassVar[int]
    DISPLAY_STRING_FIELD_NUMBER: ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: ClassVar[int]
    NUMBER_OF_JOBS_FIELD_NUMBER: ClassVar[int]
    destination: MaterializationTaskDiffDestination
    display_string: str
    feature_end_time: _timestamp_pb2.Timestamp
    feature_start_time: _timestamp_pb2.Timestamp
    number_of_jobs: int
    def __init__(self, display_string: Optional[str] = ..., feature_start_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., feature_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., number_of_jobs: Optional[int] = ..., destination: Optional[Union[MaterializationTaskDiffDestination, str]] = ...) -> None: ...

class BatchMaterializationTaskDiff(_message.Message):
    __slots__ = ["destination", "display_string", "schedule_interval"]
    DESTINATION_FIELD_NUMBER: ClassVar[int]
    DISPLAY_STRING_FIELD_NUMBER: ClassVar[int]
    SCHEDULE_INTERVAL_FIELD_NUMBER: ClassVar[int]
    destination: MaterializationTaskDiffDestination
    display_string: str
    schedule_interval: _duration_pb2.Duration
    def __init__(self, display_string: Optional[str] = ..., schedule_interval: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., destination: Optional[Union[MaterializationTaskDiffDestination, str]] = ...) -> None: ...

class FcoDiff(_message.Message):
    __slots__ = ["declared_args", "diff", "existing_args", "materialization_info", "transition_side_effects", "type"]
    DECLARED_ARGS_FIELD_NUMBER: ClassVar[int]
    DIFF_FIELD_NUMBER: ClassVar[int]
    EXISTING_ARGS_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_INFO_FIELD_NUMBER: ClassVar[int]
    TRANSITION_SIDE_EFFECTS_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    declared_args: _fco_args__client_pb2.FcoArgs
    diff: _containers.RepeatedCompositeFieldContainer[FcoPropertyDiff]
    existing_args: _fco_args__client_pb2.FcoArgs
    materialization_info: MaterializationInfo
    transition_side_effects: FcoTransitionSideEffects
    type: FcoTransitionType
    def __init__(self, type: Optional[Union[FcoTransitionType, str]] = ..., transition_side_effects: Optional[Union[FcoTransitionSideEffects, Mapping]] = ..., existing_args: Optional[Union[_fco_args__client_pb2.FcoArgs, Mapping]] = ..., declared_args: Optional[Union[_fco_args__client_pb2.FcoArgs, Mapping]] = ..., diff: Optional[Iterable[Union[FcoPropertyDiff, Mapping]]] = ..., materialization_info: Optional[Union[MaterializationInfo, Mapping]] = ...) -> None: ...

class FcoFieldRef(_message.Message):
    __slots__ = ["fco_id"]
    FCO_ID_FIELD_NUMBER: ClassVar[int]
    fco_id: _id__client_pb2.Id
    def __init__(self, fco_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class FcoPropertyDiff(_message.Message):
    __slots__ = ["custom_comparator", "property_name", "rendering_type", "val_declared", "val_existing"]
    CUSTOM_COMPARATOR_FIELD_NUMBER: ClassVar[int]
    PROPERTY_NAME_FIELD_NUMBER: ClassVar[int]
    RENDERING_TYPE_FIELD_NUMBER: ClassVar[int]
    VAL_DECLARED_FIELD_NUMBER: ClassVar[int]
    VAL_EXISTING_FIELD_NUMBER: ClassVar[int]
    custom_comparator: _diff_options__client_pb2.CustomComparator
    property_name: str
    rendering_type: _diff_options__client_pb2.FcoPropertyRenderingType
    val_declared: str
    val_existing: str
    def __init__(self, property_name: Optional[str] = ..., val_existing: Optional[str] = ..., val_declared: Optional[str] = ..., rendering_type: Optional[Union[_diff_options__client_pb2.FcoPropertyRenderingType, str]] = ..., custom_comparator: Optional[Union[_diff_options__client_pb2.CustomComparator, str]] = ...) -> None: ...

class FcoTransitionSideEffects(_message.Message):
    __slots__ = ["stream_restart_type"]
    STREAM_RESTART_TYPE_FIELD_NUMBER: ClassVar[int]
    stream_restart_type: FcoTransitionSideEffectStreamRestartType
    def __init__(self, stream_restart_type: Optional[Union[FcoTransitionSideEffectStreamRestartType, str]] = ...) -> None: ...

class IntegrationTestJobSummary(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: ClassVar[int]
    status: IntegrationTestJobStatus
    def __init__(self, status: Optional[Union[IntegrationTestJobStatus, str]] = ...) -> None: ...

class MaterializationInfo(_message.Message):
    __slots__ = ["backfill_publish_task_diffs", "backfill_task_diffs", "batch_task_diff", "integration_test_task_diffs", "stream_task_diff"]
    BACKFILL_PUBLISH_TASK_DIFFS_FIELD_NUMBER: ClassVar[int]
    BACKFILL_TASK_DIFFS_FIELD_NUMBER: ClassVar[int]
    BATCH_TASK_DIFF_FIELD_NUMBER: ClassVar[int]
    INTEGRATION_TEST_TASK_DIFFS_FIELD_NUMBER: ClassVar[int]
    STREAM_TASK_DIFF_FIELD_NUMBER: ClassVar[int]
    backfill_publish_task_diffs: _containers.RepeatedCompositeFieldContainer[BackfillFeaturePublishTaskDiff]
    backfill_task_diffs: _containers.RepeatedCompositeFieldContainer[BackfillMaterializationTaskDiff]
    batch_task_diff: BatchMaterializationTaskDiff
    integration_test_task_diffs: _containers.RepeatedCompositeFieldContainer[PlanIntegrationTestTaskDiff]
    stream_task_diff: StreamMaterializationTaskDiff
    def __init__(self, backfill_task_diffs: Optional[Iterable[Union[BackfillMaterializationTaskDiff, Mapping]]] = ..., batch_task_diff: Optional[Union[BatchMaterializationTaskDiff, Mapping]] = ..., stream_task_diff: Optional[Union[StreamMaterializationTaskDiff, Mapping]] = ..., backfill_publish_task_diffs: Optional[Iterable[Union[BackfillFeaturePublishTaskDiff, Mapping]]] = ..., integration_test_task_diffs: Optional[Iterable[Union[PlanIntegrationTestTaskDiff, Mapping]]] = ...) -> None: ...

class PlanIntegrationTestConfig(_message.Message):
    __slots__ = ["auto_apply_upon_test_success", "feature_view_names"]
    AUTO_APPLY_UPON_TEST_SUCCESS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAMES_FIELD_NUMBER: ClassVar[int]
    auto_apply_upon_test_success: bool
    feature_view_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, auto_apply_upon_test_success: bool = ..., feature_view_names: Optional[Iterable[str]] = ...) -> None: ...

class PlanIntegrationTestSummary(_message.Message):
    __slots__ = ["feature_view_id", "feature_view_name", "job_summaries"]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    JOB_SUMMARIES_FIELD_NUMBER: ClassVar[int]
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    job_summaries: _containers.RepeatedCompositeFieldContainer[IntegrationTestJobSummary]
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., job_summaries: Optional[Iterable[Union[IntegrationTestJobSummary, Mapping]]] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class PlanIntegrationTestTaskDiff(_message.Message):
    __slots__ = ["display_string", "feature_view_name"]
    DISPLAY_STRING_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: ClassVar[int]
    display_string: str
    feature_view_name: str
    def __init__(self, display_string: Optional[str] = ..., feature_view_name: Optional[str] = ...) -> None: ...

class StateUpdateEntry(_message.Message):
    __slots__ = ["applied_at", "applied_by", "applied_by_principal", "commit_id", "created_at", "created_by", "error", "sdk_version", "status_type", "successful_plan_output", "workspace"]
    APPLIED_AT_FIELD_NUMBER: ClassVar[int]
    APPLIED_BY_FIELD_NUMBER: ClassVar[int]
    APPLIED_BY_PRINCIPAL_FIELD_NUMBER: ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: ClassVar[int]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    CREATED_BY_FIELD_NUMBER: ClassVar[int]
    ERROR_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    STATUS_TYPE_FIELD_NUMBER: ClassVar[int]
    SUCCESSFUL_PLAN_OUTPUT_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    applied_at: _timestamp_pb2.Timestamp
    applied_by: str
    applied_by_principal: _principal__client_pb2.PrincipalBasic
    commit_id: str
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    error: str
    sdk_version: str
    status_type: PlanStatusType
    successful_plan_output: SuccessfulPlanOutput
    workspace: str
    def __init__(self, commit_id: Optional[str] = ..., applied_by: Optional[str] = ..., applied_by_principal: Optional[Union[_principal__client_pb2.PrincipalBasic, Mapping]] = ..., applied_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., workspace: Optional[str] = ..., sdk_version: Optional[str] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., status_type: Optional[Union[PlanStatusType, str]] = ..., error: Optional[str] = ..., successful_plan_output: Optional[Union[SuccessfulPlanOutput, Mapping]] = ..., created_by: Optional[str] = ...) -> None: ...

class StateUpdatePlanSummary(_message.Message):
    __slots__ = ["applied_at", "applied_by", "applied_by_principal", "created_at", "created_by", "diff_items", "sdk_version", "workspace"]
    APPLIED_AT_FIELD_NUMBER: ClassVar[int]
    APPLIED_BY_FIELD_NUMBER: ClassVar[int]
    APPLIED_BY_PRINCIPAL_FIELD_NUMBER: ClassVar[int]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    CREATED_BY_FIELD_NUMBER: ClassVar[int]
    DIFF_ITEMS_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    applied_at: _timestamp_pb2.Timestamp
    applied_by: str
    applied_by_principal: _principal__client_pb2.PrincipalBasic
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    diff_items: _containers.RepeatedCompositeFieldContainer[StateUpdatePlanSummaryDiff]
    sdk_version: str
    workspace: str
    def __init__(self, diff_items: Optional[Iterable[Union[StateUpdatePlanSummaryDiff, Mapping]]] = ..., applied_by: Optional[str] = ..., applied_by_principal: Optional[Union[_principal__client_pb2.PrincipalBasic, Mapping]] = ..., created_by: Optional[str] = ..., applied_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., workspace: Optional[str] = ..., sdk_version: Optional[str] = ...) -> None: ...

class StateUpdatePlanSummaryDiff(_message.Message):
    __slots__ = ["description", "diffs", "fco_type", "materialization_info", "name", "transition_side_effects", "type"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    DIFFS_FIELD_NUMBER: ClassVar[int]
    FCO_TYPE_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_INFO_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TRANSITION_SIDE_EFFECTS_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    description: str
    diffs: _containers.RepeatedCompositeFieldContainer[FcoPropertyDiff]
    fco_type: str
    materialization_info: MaterializationInfo
    name: str
    transition_side_effects: FcoTransitionSideEffects
    type: FcoTransitionType
    def __init__(self, fco_type: Optional[str] = ..., type: Optional[Union[FcoTransitionType, str]] = ..., transition_side_effects: Optional[Union[FcoTransitionSideEffects, Mapping]] = ..., diffs: Optional[Iterable[Union[FcoPropertyDiff, Mapping]]] = ..., name: Optional[str] = ..., description: Optional[str] = ..., materialization_info: Optional[Union[MaterializationInfo, Mapping]] = ...) -> None: ...

class StateUpdateRequest(_message.Message):
    __slots__ = ["fco_args", "plan_integration_config", "plan_integration_type", "repo_source_info", "requested_by", "requested_by_principal", "sdk_version", "suppress_recreates", "upgrade_all", "workspace"]
    FCO_ARGS_FIELD_NUMBER: ClassVar[int]
    PLAN_INTEGRATION_CONFIG_FIELD_NUMBER: ClassVar[int]
    PLAN_INTEGRATION_TYPE_FIELD_NUMBER: ClassVar[int]
    REPO_SOURCE_INFO_FIELD_NUMBER: ClassVar[int]
    REQUESTED_BY_FIELD_NUMBER: ClassVar[int]
    REQUESTED_BY_PRINCIPAL_FIELD_NUMBER: ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: ClassVar[int]
    SUPPRESS_RECREATES_FIELD_NUMBER: ClassVar[int]
    UPGRADE_ALL_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    fco_args: _containers.RepeatedCompositeFieldContainer[_fco_args__client_pb2.FcoArgs]
    plan_integration_config: PlanIntegrationTestConfig
    plan_integration_type: PlanIntegrationTestSelectType
    repo_source_info: _repo_metadata__client_pb2.FeatureRepoSourceInfo
    requested_by: str
    requested_by_principal: _principal__client_pb2.Principal
    sdk_version: str
    suppress_recreates: bool
    upgrade_all: bool
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., fco_args: Optional[Iterable[Union[_fco_args__client_pb2.FcoArgs, Mapping]]] = ..., repo_source_info: Optional[Union[_repo_metadata__client_pb2.FeatureRepoSourceInfo, Mapping]] = ..., suppress_recreates: bool = ..., upgrade_all: bool = ..., requested_by: Optional[str] = ..., requested_by_principal: Optional[Union[_principal__client_pb2.Principal, Mapping]] = ..., sdk_version: Optional[str] = ..., plan_integration_type: Optional[Union[PlanIntegrationTestSelectType, str]] = ..., plan_integration_config: Optional[Union[PlanIntegrationTestConfig, Mapping]] = ...) -> None: ...

class StreamMaterializationTaskDiff(_message.Message):
    __slots__ = ["display_string"]
    DISPLAY_STRING_FIELD_NUMBER: ClassVar[int]
    display_string: str
    def __init__(self, display_string: Optional[str] = ...) -> None: ...

class SuccessfulPlanOutput(_message.Message):
    __slots__ = ["apply_warnings", "json_output", "num_fcos_changed", "num_warnings", "plan_url", "string_output", "test_summaries"]
    APPLY_WARNINGS_FIELD_NUMBER: ClassVar[int]
    JSON_OUTPUT_FIELD_NUMBER: ClassVar[int]
    NUM_FCOS_CHANGED_FIELD_NUMBER: ClassVar[int]
    NUM_WARNINGS_FIELD_NUMBER: ClassVar[int]
    PLAN_URL_FIELD_NUMBER: ClassVar[int]
    STRING_OUTPUT_FIELD_NUMBER: ClassVar[int]
    TEST_SUMMARIES_FIELD_NUMBER: ClassVar[int]
    apply_warnings: str
    json_output: str
    num_fcos_changed: int
    num_warnings: int
    plan_url: str
    string_output: str
    test_summaries: _containers.RepeatedCompositeFieldContainer[PlanIntegrationTestSummary]
    def __init__(self, string_output: Optional[str] = ..., json_output: Optional[str] = ..., apply_warnings: Optional[str] = ..., num_fcos_changed: Optional[int] = ..., num_warnings: Optional[int] = ..., test_summaries: Optional[Iterable[Union[PlanIntegrationTestSummary, Mapping]]] = ..., plan_url: Optional[str] = ...) -> None: ...

class ValidationMessage(_message.Message):
    __slots__ = ["fco_refs", "message"]
    FCO_REFS_FIELD_NUMBER: ClassVar[int]
    MESSAGE_FIELD_NUMBER: ClassVar[int]
    fco_refs: _containers.RepeatedCompositeFieldContainer[FcoFieldRef]
    message: str
    def __init__(self, message: Optional[str] = ..., fco_refs: Optional[Iterable[Union[FcoFieldRef, Mapping]]] = ...) -> None: ...

class ValidationResult(_message.Message):
    __slots__ = ["errors", "warnings"]
    ERRORS_FIELD_NUMBER: ClassVar[int]
    WARNINGS_FIELD_NUMBER: ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[ValidationMessage]
    warnings: _containers.RepeatedCompositeFieldContainer[ValidationMessage]
    def __init__(self, errors: Optional[Iterable[Union[ValidationMessage, Mapping]]] = ..., warnings: Optional[Iterable[Union[ValidationMessage, Mapping]]] = ...) -> None: ...

class FcoTransitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FcoTransitionSideEffectStreamRestartType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MaterializationTaskDiffDestination(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class IntegrationTestJobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PlanIntegrationTestSelectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PlanStatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
