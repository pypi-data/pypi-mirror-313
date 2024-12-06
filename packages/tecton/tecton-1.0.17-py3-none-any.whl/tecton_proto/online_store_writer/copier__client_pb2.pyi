from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.online_store_writer import config__client_pb2 as _config__client_pb2
from tecton_proto.snowflake import snowflake_credentials__client_pb2 as _snowflake_credentials__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
MICROS: TimestampUnit
MILLIS: TimestampUnit
UNSPECIFIED: TimestampUnit

class DeletionRequest(_message.Message):
    __slots__ = ["online_join_keys_full_path", "online_join_keys_path"]
    ONLINE_JOIN_KEYS_FULL_PATH_FIELD_NUMBER: ClassVar[int]
    ONLINE_JOIN_KEYS_PATH_FIELD_NUMBER: ClassVar[int]
    online_join_keys_full_path: str
    online_join_keys_path: str
    def __init__(self, online_join_keys_path: Optional[str] = ..., online_join_keys_full_path: Optional[str] = ...) -> None: ...

class GCSStage(_message.Message):
    __slots__ = ["blob", "bucket"]
    BLOB_FIELD_NUMBER: ClassVar[int]
    BUCKET_FIELD_NUMBER: ClassVar[int]
    blob: str
    bucket: str
    def __init__(self, bucket: Optional[str] = ..., blob: Optional[str] = ...) -> None: ...

class LocalFileStage(_message.Message):
    __slots__ = ["location"]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    location: str
    def __init__(self, location: Optional[str] = ...) -> None: ...

class ObjectCopyRequest(_message.Message):
    __slots__ = ["gcs_stage", "local_file_stage", "s3_stage", "skip_rows", "snowflake_internal_stage", "timestamp_units"]
    GCS_STAGE_FIELD_NUMBER: ClassVar[int]
    LOCAL_FILE_STAGE_FIELD_NUMBER: ClassVar[int]
    S3_STAGE_FIELD_NUMBER: ClassVar[int]
    SKIP_ROWS_FIELD_NUMBER: ClassVar[int]
    SNOWFLAKE_INTERNAL_STAGE_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_UNITS_FIELD_NUMBER: ClassVar[int]
    gcs_stage: GCSStage
    local_file_stage: LocalFileStage
    s3_stage: S3Stage
    skip_rows: int
    snowflake_internal_stage: SnowflakeInternalStage
    timestamp_units: TimestampUnit
    def __init__(self, s3_stage: Optional[Union[S3Stage, Mapping]] = ..., snowflake_internal_stage: Optional[Union[SnowflakeInternalStage, Mapping]] = ..., local_file_stage: Optional[Union[LocalFileStage, Mapping]] = ..., gcs_stage: Optional[Union[GCSStage, Mapping]] = ..., skip_rows: Optional[int] = ..., timestamp_units: Optional[Union[TimestampUnit, str]] = ...) -> None: ...

class OnlineStoreCopierRequest(_message.Message):
    __slots__ = ["attempt_index", "deletion_request", "enable_new_consumption_metrics", "feature_view", "materialization_task_attempt_id", "object_copy_request", "online_store_metadata_configuration", "online_store_writer_configuration", "sqs_url", "status_update_request", "task_key"]
    ATTEMPT_INDEX_FIELD_NUMBER: ClassVar[int]
    DELETION_REQUEST_FIELD_NUMBER: ClassVar[int]
    ENABLE_NEW_CONSUMPTION_METRICS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_TASK_ATTEMPT_ID_FIELD_NUMBER: ClassVar[int]
    OBJECT_COPY_REQUEST_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_METADATA_CONFIGURATION_FIELD_NUMBER: ClassVar[int]
    ONLINE_STORE_WRITER_CONFIGURATION_FIELD_NUMBER: ClassVar[int]
    SQS_URL_FIELD_NUMBER: ClassVar[int]
    STATUS_UPDATE_REQUEST_FIELD_NUMBER: ClassVar[int]
    TASK_KEY_FIELD_NUMBER: ClassVar[int]
    attempt_index: int
    deletion_request: DeletionRequest
    enable_new_consumption_metrics: bool
    feature_view: _feature_view__client_pb2.FeatureView
    materialization_task_attempt_id: _id__client_pb2.Id
    object_copy_request: ObjectCopyRequest
    online_store_metadata_configuration: _config__client_pb2.OnlineStoreMetadataConfiguration
    online_store_writer_configuration: _config__client_pb2.OnlineStoreWriterConfiguration
    sqs_url: str
    status_update_request: StatusUpdateRequest
    task_key: str
    def __init__(self, online_store_writer_configuration: Optional[Union[_config__client_pb2.OnlineStoreWriterConfiguration, Mapping]] = ..., feature_view: Optional[Union[_feature_view__client_pb2.FeatureView, Mapping]] = ..., materialization_task_attempt_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., task_key: Optional[str] = ..., attempt_index: Optional[int] = ..., sqs_url: Optional[str] = ..., online_store_metadata_configuration: Optional[Union[_config__client_pb2.OnlineStoreMetadataConfiguration, Mapping]] = ..., enable_new_consumption_metrics: bool = ..., object_copy_request: Optional[Union[ObjectCopyRequest, Mapping]] = ..., status_update_request: Optional[Union[StatusUpdateRequest, Mapping]] = ..., deletion_request: Optional[Union[DeletionRequest, Mapping]] = ...) -> None: ...

class S3Stage(_message.Message):
    __slots__ = ["bucket", "key"]
    BUCKET_FIELD_NUMBER: ClassVar[int]
    KEY_FIELD_NUMBER: ClassVar[int]
    bucket: str
    key: str
    def __init__(self, bucket: Optional[str] = ..., key: Optional[str] = ...) -> None: ...

class SnowflakeInternalStage(_message.Message):
    __slots__ = ["credentials", "location", "snowflake_account_identifier"]
    CREDENTIALS_FIELD_NUMBER: ClassVar[int]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    SNOWFLAKE_ACCOUNT_IDENTIFIER_FIELD_NUMBER: ClassVar[int]
    credentials: _snowflake_credentials__client_pb2.SnowflakeCredentials
    location: str
    snowflake_account_identifier: str
    def __init__(self, snowflake_account_identifier: Optional[str] = ..., credentials: Optional[Union[_snowflake_credentials__client_pb2.SnowflakeCredentials, Mapping]] = ..., location: Optional[str] = ...) -> None: ...

class StatusUpdateRequest(_message.Message):
    __slots__ = ["anchor_time", "materialized_raw_data_end_time"]
    ANCHOR_TIME_FIELD_NUMBER: ClassVar[int]
    MATERIALIZED_RAW_DATA_END_TIME_FIELD_NUMBER: ClassVar[int]
    anchor_time: _timestamp_pb2.Timestamp
    materialized_raw_data_end_time: _timestamp_pb2.Timestamp
    def __init__(self, anchor_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., materialized_raw_data_end_time: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...

class TimestampUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
