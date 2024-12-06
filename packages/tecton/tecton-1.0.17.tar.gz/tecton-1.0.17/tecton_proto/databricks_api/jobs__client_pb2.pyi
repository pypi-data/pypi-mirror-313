from tecton_proto.spark_common import clusters__client_pb2 as _clusters__client_pb2
from tecton_proto.spark_common import libraries__client_pb2 as _libraries__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClusterInstance(_message.Message):
    __slots__ = ["cluster_id"]
    CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: Optional[str] = ...) -> None: ...

class ClusterSpec(_message.Message):
    __slots__ = ["existing_cluster_id", "libraries", "new_cluster"]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    LIBRARIES_FIELD_NUMBER: ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: ClassVar[int]
    existing_cluster_id: str
    libraries: _containers.RepeatedCompositeFieldContainer[RemoteLibrary]
    new_cluster: NewCluster
    def __init__(self, new_cluster: Optional[Union[NewCluster, Mapping]] = ..., existing_cluster_id: Optional[str] = ..., libraries: Optional[Iterable[Union[RemoteLibrary, Mapping]]] = ...) -> None: ...

class JobsCancelRunRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    run_id: int
    def __init__(self, run_id: Optional[int] = ...) -> None: ...

class JobsRunsGetRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    run_id: int
    def __init__(self, run_id: Optional[int] = ...) -> None: ...

class JobsRunsGetResponse(_message.Message):
    __slots__ = ["cluster_instance", "end_time", "execution_duration", "job_id", "run_id", "run_page_url", "setup_duration", "start_time", "state"]
    CLUSTER_INSTANCE_FIELD_NUMBER: ClassVar[int]
    END_TIME_FIELD_NUMBER: ClassVar[int]
    EXECUTION_DURATION_FIELD_NUMBER: ClassVar[int]
    JOB_ID_FIELD_NUMBER: ClassVar[int]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    RUN_PAGE_URL_FIELD_NUMBER: ClassVar[int]
    SETUP_DURATION_FIELD_NUMBER: ClassVar[int]
    START_TIME_FIELD_NUMBER: ClassVar[int]
    STATE_FIELD_NUMBER: ClassVar[int]
    cluster_instance: ClusterInstance
    end_time: int
    execution_duration: int
    job_id: int
    run_id: int
    run_page_url: str
    setup_duration: int
    start_time: int
    state: RunState
    def __init__(self, run_id: Optional[int] = ..., job_id: Optional[int] = ..., execution_duration: Optional[int] = ..., start_time: Optional[int] = ..., end_time: Optional[int] = ..., setup_duration: Optional[int] = ..., cluster_instance: Optional[Union[ClusterInstance, Mapping]] = ..., run_page_url: Optional[str] = ..., state: Optional[Union[RunState, Mapping]] = ...) -> None: ...

class JobsRunsListRequest(_message.Message):
    __slots__ = ["active_only", "limit", "offset", "run_type"]
    ACTIVE_ONLY_FIELD_NUMBER: ClassVar[int]
    LIMIT_FIELD_NUMBER: ClassVar[int]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    RUN_TYPE_FIELD_NUMBER: ClassVar[int]
    active_only: bool
    limit: int
    offset: int
    run_type: str
    def __init__(self, offset: Optional[int] = ..., active_only: bool = ..., run_type: Optional[str] = ..., limit: Optional[int] = ...) -> None: ...

class JobsRunsListResponse(_message.Message):
    __slots__ = ["has_more", "runs"]
    HAS_MORE_FIELD_NUMBER: ClassVar[int]
    RUNS_FIELD_NUMBER: ClassVar[int]
    has_more: bool
    runs: _containers.RepeatedCompositeFieldContainer[Run]
    def __init__(self, runs: Optional[Iterable[Union[Run, Mapping]]] = ..., has_more: bool = ...) -> None: ...

class JobsRunsSubmitRequest(_message.Message):
    __slots__ = ["existing_cluster_id", "libraries", "new_cluster", "notebook_task", "run_name", "tasks", "timeout_seconds"]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    LIBRARIES_FIELD_NUMBER: ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: ClassVar[int]
    NOTEBOOK_TASK_FIELD_NUMBER: ClassVar[int]
    RUN_NAME_FIELD_NUMBER: ClassVar[int]
    TASKS_FIELD_NUMBER: ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: ClassVar[int]
    existing_cluster_id: str
    libraries: _containers.RepeatedCompositeFieldContainer[RemoteLibrary]
    new_cluster: _clusters__client_pb2.NewCluster
    notebook_task: NotebookTask
    run_name: str
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    timeout_seconds: int
    def __init__(self, new_cluster: Optional[Union[_clusters__client_pb2.NewCluster, Mapping]] = ..., existing_cluster_id: Optional[str] = ..., notebook_task: Optional[Union[NotebookTask, Mapping]] = ..., run_name: Optional[str] = ..., libraries: Optional[Iterable[Union[RemoteLibrary, Mapping]]] = ..., timeout_seconds: Optional[int] = ..., tasks: Optional[Iterable[Union[Task, Mapping]]] = ...) -> None: ...

class JobsRunsSubmitResponse(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    run_id: int
    def __init__(self, run_id: Optional[int] = ...) -> None: ...

class NewCluster(_message.Message):
    __slots__ = ["custom_tags"]
    class CustomTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    CUSTOM_TAGS_FIELD_NUMBER: ClassVar[int]
    custom_tags: _containers.ScalarMap[str, str]
    def __init__(self, custom_tags: Optional[Mapping[str, str]] = ...) -> None: ...

class NotebookTask(_message.Message):
    __slots__ = ["base_parameters", "notebook_path"]
    class BaseParametersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BASE_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    NOTEBOOK_PATH_FIELD_NUMBER: ClassVar[int]
    base_parameters: _containers.ScalarMap[str, str]
    notebook_path: str
    def __init__(self, notebook_path: Optional[str] = ..., base_parameters: Optional[Mapping[str, str]] = ...) -> None: ...

class RemoteLibrary(_message.Message):
    __slots__ = ["egg", "jar", "maven", "pypi", "whl"]
    EGG_FIELD_NUMBER: ClassVar[int]
    JAR_FIELD_NUMBER: ClassVar[int]
    MAVEN_FIELD_NUMBER: ClassVar[int]
    PYPI_FIELD_NUMBER: ClassVar[int]
    WHL_FIELD_NUMBER: ClassVar[int]
    egg: str
    jar: str
    maven: _libraries__client_pb2.MavenLibrary
    pypi: _libraries__client_pb2.PyPiLibrary
    whl: str
    def __init__(self, jar: Optional[str] = ..., egg: Optional[str] = ..., whl: Optional[str] = ..., maven: Optional[Union[_libraries__client_pb2.MavenLibrary, Mapping]] = ..., pypi: Optional[Union[_libraries__client_pb2.PyPiLibrary, Mapping]] = ...) -> None: ...

class Run(_message.Message):
    __slots__ = ["cluster_spec", "job_id", "run_id", "run_page_url", "state"]
    CLUSTER_SPEC_FIELD_NUMBER: ClassVar[int]
    JOB_ID_FIELD_NUMBER: ClassVar[int]
    RUN_ID_FIELD_NUMBER: ClassVar[int]
    RUN_PAGE_URL_FIELD_NUMBER: ClassVar[int]
    STATE_FIELD_NUMBER: ClassVar[int]
    cluster_spec: ClusterSpec
    job_id: int
    run_id: int
    run_page_url: str
    state: RunState
    def __init__(self, job_id: Optional[int] = ..., run_id: Optional[int] = ..., state: Optional[Union[RunState, Mapping]] = ..., cluster_spec: Optional[Union[ClusterSpec, Mapping]] = ..., run_page_url: Optional[str] = ...) -> None: ...

class RunState(_message.Message):
    __slots__ = ["life_cycle_state", "result_state", "state_message"]
    class RunLifeCycleState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class RunResultState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CANCELED: RunState.RunResultState
    FAILED: RunState.RunResultState
    INTERNAL_ERROR: RunState.RunLifeCycleState
    LIFE_CYCLE_STATE_FIELD_NUMBER: ClassVar[int]
    PENDING: RunState.RunLifeCycleState
    RESULT_STATE_FIELD_NUMBER: ClassVar[int]
    RUNNING: RunState.RunLifeCycleState
    SKIPPED: RunState.RunLifeCycleState
    STATE_MESSAGE_FIELD_NUMBER: ClassVar[int]
    SUCCESS: RunState.RunResultState
    TERMINATED: RunState.RunLifeCycleState
    TERMINATING: RunState.RunLifeCycleState
    TIMEDOUT: RunState.RunResultState
    UNKNOWN_RUN_LIFE_CYCLE_STATE: RunState.RunLifeCycleState
    UNKNOWN_RUN_RESULT_STATE: RunState.RunResultState
    life_cycle_state: RunState.RunLifeCycleState
    result_state: RunState.RunResultState
    state_message: str
    def __init__(self, life_cycle_state: Optional[Union[RunState.RunLifeCycleState, str]] = ..., result_state: Optional[Union[RunState.RunResultState, str]] = ..., state_message: Optional[str] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ["depends_on", "description", "existing_cluster_id", "libraries", "new_cluster", "notebook_task", "task_key", "timeout_seconds"]
    DEPENDS_ON_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    LIBRARIES_FIELD_NUMBER: ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: ClassVar[int]
    NOTEBOOK_TASK_FIELD_NUMBER: ClassVar[int]
    TASK_KEY_FIELD_NUMBER: ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: ClassVar[int]
    depends_on: _containers.RepeatedCompositeFieldContainer[Task]
    description: str
    existing_cluster_id: str
    libraries: _containers.RepeatedCompositeFieldContainer[RemoteLibrary]
    new_cluster: _clusters__client_pb2.NewCluster
    notebook_task: NotebookTask
    task_key: str
    timeout_seconds: int
    def __init__(self, task_key: Optional[str] = ..., description: Optional[str] = ..., depends_on: Optional[Iterable[Union[Task, Mapping]]] = ..., new_cluster: Optional[Union[_clusters__client_pb2.NewCluster, Mapping]] = ..., existing_cluster_id: Optional[str] = ..., notebook_task: Optional[Union[NotebookTask, Mapping]] = ..., libraries: Optional[Iterable[Union[RemoteLibrary, Mapping]]] = ..., timeout_seconds: Optional[int] = ...) -> None: ...
