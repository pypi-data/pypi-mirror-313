from tecton_proto.spark_api import jobs__client_pb2 as _jobs__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

BATCH: TaskType
DATASET_GENERATION: TaskType
DELETION: TaskType
DELTA_MAINTENANCE: TaskType
DESCRIPTOR: _descriptor.FileDescriptor
ENV_DATABRICKS_NOTEBOOK: SparkExecutionEnvironment
ENV_DATAPROC: SparkExecutionEnvironment
ENV_EMR: SparkExecutionEnvironment
ENV_UNSPECIFIED: SparkExecutionEnvironment
FEATURE_EXPORT: TaskType
INGEST: TaskType
PLAN_INTEGRATION_TEST_BATCH: TaskType
PLAN_INTEGRATION_TEST_STREAM: TaskType
STREAMING: TaskType
UNKNOWN: TaskType

class JobRequestTemplates(_message.Message):
    __slots__ = ["databricks_template", "emr_template"]
    DATABRICKS_TEMPLATE_FIELD_NUMBER: ClassVar[int]
    EMR_TEMPLATE_FIELD_NUMBER: ClassVar[int]
    databricks_template: _jobs__client_pb2.StartJobRequest
    emr_template: _jobs__client_pb2.StartJobRequest
    def __init__(self, databricks_template: Optional[Union[_jobs__client_pb2.StartJobRequest, Mapping]] = ..., emr_template: Optional[Union[_jobs__client_pb2.StartJobRequest, Mapping]] = ...) -> None: ...

class SparkClusterEnvironment(_message.Message):
    __slots__ = ["job_request_templates", "merged_user_deployment_settings_version", "spark_cluster_environment_version"]
    JOB_REQUEST_TEMPLATES_FIELD_NUMBER: ClassVar[int]
    MERGED_USER_DEPLOYMENT_SETTINGS_VERSION_FIELD_NUMBER: ClassVar[int]
    SPARK_CLUSTER_ENVIRONMENT_VERSION_FIELD_NUMBER: ClassVar[int]
    job_request_templates: JobRequestTemplates
    merged_user_deployment_settings_version: int
    spark_cluster_environment_version: int
    def __init__(self, spark_cluster_environment_version: Optional[int] = ..., job_request_templates: Optional[Union[JobRequestTemplates, Mapping]] = ..., merged_user_deployment_settings_version: Optional[int] = ...) -> None: ...

class TaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SparkExecutionEnvironment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
