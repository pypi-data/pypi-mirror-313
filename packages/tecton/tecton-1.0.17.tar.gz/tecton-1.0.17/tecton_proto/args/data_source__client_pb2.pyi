from google.protobuf import duration_pb2 as _duration_pb2
from tecton_proto.args import data_source_config__client_pb2 as _data_source_config__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
UNITY_CATALOG_ACCESS_MODE_SHARED: UnityCatalogAccessMode
UNITY_CATALOG_ACCESS_MODE_SINGLE_USER: UnityCatalogAccessMode
UNITY_CATALOG_ACCESS_MODE_SINGLE_USER_WITH_FGAC: UnityCatalogAccessMode
UNITY_CATALOG_ACCESS_MODE_UNSPECIFIED: UnityCatalogAccessMode

class BatchDataSourceCommonArgs(_message.Message):
    __slots__ = ["data_delay", "post_processor", "timestamp_field"]
    DATA_DELAY_FIELD_NUMBER: ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: ClassVar[int]
    data_delay: _duration_pb2.Duration
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    timestamp_field: str
    def __init__(self, timestamp_field: Optional[str] = ..., post_processor: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., data_delay: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class BigqueryDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "credentials", "dataset", "location", "project_id", "query", "table"]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: ClassVar[int]
    DATASET_FIELD_NUMBER: ClassVar[int]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    credentials: _secret__client_pb2.SecretReference
    dataset: str
    location: str
    project_id: str
    query: str
    table: str
    def __init__(self, project_id: Optional[str] = ..., dataset: Optional[str] = ..., location: Optional[str] = ..., table: Optional[str] = ..., query: Optional[str] = ..., common_args: Optional[Union[BatchDataSourceCommonArgs, Mapping]] = ..., credentials: Optional[Union[_secret__client_pb2.SecretReference, Mapping]] = ...) -> None: ...

class DatetimePartitionColumnArgs(_message.Message):
    __slots__ = ["column_name", "datepart", "format_string", "zero_padded"]
    COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    DATEPART_FIELD_NUMBER: ClassVar[int]
    FORMAT_STRING_FIELD_NUMBER: ClassVar[int]
    ZERO_PADDED_FIELD_NUMBER: ClassVar[int]
    column_name: str
    datepart: str
    format_string: str
    zero_padded: bool
    def __init__(self, column_name: Optional[str] = ..., datepart: Optional[str] = ..., zero_padded: bool = ..., format_string: Optional[str] = ...) -> None: ...

class FileDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "convert_to_glue_format", "datetime_partition_columns", "file_format", "schema_override", "schema_uri", "timestamp_format", "uri"]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    CONVERT_TO_GLUE_FORMAT_FIELD_NUMBER: ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: ClassVar[int]
    FILE_FORMAT_FIELD_NUMBER: ClassVar[int]
    SCHEMA_OVERRIDE_FIELD_NUMBER: ClassVar[int]
    SCHEMA_URI_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FORMAT_FIELD_NUMBER: ClassVar[int]
    URI_FIELD_NUMBER: ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    convert_to_glue_format: bool
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumnArgs]
    file_format: str
    schema_override: _spark_schema__client_pb2.SparkSchema
    schema_uri: str
    timestamp_format: str
    uri: str
    def __init__(self, uri: Optional[str] = ..., file_format: Optional[str] = ..., convert_to_glue_format: bool = ..., schema_uri: Optional[str] = ..., timestamp_format: Optional[str] = ..., schema_override: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., common_args: Optional[Union[BatchDataSourceCommonArgs, Mapping]] = ..., datetime_partition_columns: Optional[Iterable[Union[DatetimePartitionColumnArgs, Mapping]]] = ...) -> None: ...

class HiveDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "database", "datetime_partition_columns", "table", "timestamp_format"]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FORMAT_FIELD_NUMBER: ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    database: str
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumnArgs]
    table: str
    timestamp_format: str
    def __init__(self, table: Optional[str] = ..., database: Optional[str] = ..., timestamp_format: Optional[str] = ..., datetime_partition_columns: Optional[Iterable[Union[DatetimePartitionColumnArgs, Mapping]]] = ..., common_args: Optional[Union[BatchDataSourceCommonArgs, Mapping]] = ...) -> None: ...

class KafkaDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "kafka_bootstrap_servers", "options", "security_protocol", "ssl_keystore_location", "ssl_keystore_password_secret_id", "ssl_truststore_location", "ssl_truststore_password_secret_id", "topics"]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    KAFKA_BOOTSTRAP_SERVERS_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    SECURITY_PROTOCOL_FIELD_NUMBER: ClassVar[int]
    SSL_KEYSTORE_LOCATION_FIELD_NUMBER: ClassVar[int]
    SSL_KEYSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: ClassVar[int]
    SSL_TRUSTSTORE_LOCATION_FIELD_NUMBER: ClassVar[int]
    SSL_TRUSTSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: ClassVar[int]
    TOPICS_FIELD_NUMBER: ClassVar[int]
    common_args: StreamDataSourceCommonArgs
    kafka_bootstrap_servers: str
    options: _containers.RepeatedCompositeFieldContainer[Option]
    security_protocol: str
    ssl_keystore_location: str
    ssl_keystore_password_secret_id: str
    ssl_truststore_location: str
    ssl_truststore_password_secret_id: str
    topics: str
    def __init__(self, kafka_bootstrap_servers: Optional[str] = ..., topics: Optional[str] = ..., options: Optional[Iterable[Union[Option, Mapping]]] = ..., ssl_keystore_location: Optional[str] = ..., ssl_keystore_password_secret_id: Optional[str] = ..., ssl_truststore_location: Optional[str] = ..., ssl_truststore_password_secret_id: Optional[str] = ..., security_protocol: Optional[str] = ..., common_args: Optional[Union[StreamDataSourceCommonArgs, Mapping]] = ...) -> None: ...

class KinesisDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "initial_stream_position", "options", "region", "stream_name"]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    INITIAL_STREAM_POSITION_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: ClassVar[int]
    common_args: StreamDataSourceCommonArgs
    initial_stream_position: _data_source_config__client_pb2.InitialStreamPosition
    options: _containers.RepeatedCompositeFieldContainer[Option]
    region: str
    stream_name: str
    def __init__(self, stream_name: Optional[str] = ..., region: Optional[str] = ..., initial_stream_position: Optional[Union[_data_source_config__client_pb2.InitialStreamPosition, str]] = ..., options: Optional[Iterable[Union[Option, Mapping]]] = ..., common_args: Optional[Union[StreamDataSourceCommonArgs, Mapping]] = ...) -> None: ...

class Option(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    key: str
    value: str
    def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...

class PandasBatchConfigArgs(_message.Message):
    __slots__ = ["data_delay", "data_source_function", "secrets", "supports_time_filtering"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[_secret__client_pb2.SecretReference, Mapping]] = ...) -> None: ...
    DATA_DELAY_FIELD_NUMBER: ClassVar[int]
    DATA_SOURCE_FUNCTION_FIELD_NUMBER: ClassVar[int]
    SECRETS_FIELD_NUMBER: ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: ClassVar[int]
    data_delay: _duration_pb2.Duration
    data_source_function: _user_defined_function__client_pb2.UserDefinedFunction
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    supports_time_filtering: bool
    def __init__(self, data_source_function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., data_delay: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., supports_time_filtering: bool = ..., secrets: Optional[Mapping[str, _secret__client_pb2.SecretReference]] = ...) -> None: ...

class PushSourceArgs(_message.Message):
    __slots__ = ["input_schema", "log_offline", "post_processor", "post_processor_mode", "timestamp_field"]
    INPUT_SCHEMA_FIELD_NUMBER: ClassVar[int]
    LOG_OFFLINE_FIELD_NUMBER: ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: ClassVar[int]
    POST_PROCESSOR_MODE_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: ClassVar[int]
    input_schema: _schema__client_pb2.Schema
    log_offline: bool
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    post_processor_mode: _transformation__client_pb2.TransformationMode
    timestamp_field: str
    def __init__(self, log_offline: bool = ..., post_processor: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., input_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., post_processor_mode: Optional[Union[_transformation__client_pb2.TransformationMode, str]] = ..., timestamp_field: Optional[str] = ...) -> None: ...

class RedshiftDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "endpoint", "query", "table"]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    ENDPOINT_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    endpoint: str
    query: str
    table: str
    def __init__(self, endpoint: Optional[str] = ..., table: Optional[str] = ..., query: Optional[str] = ..., common_args: Optional[Union[BatchDataSourceCommonArgs, Mapping]] = ...) -> None: ...

class SnowflakeDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "database", "password", "query", "role", "schema", "table", "url", "user", "warehouse"]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    PASSWORD_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    ROLE_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    URL_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    database: str
    password: _secret__client_pb2.SecretReference
    query: str
    role: str
    schema: str
    table: str
    url: str
    user: _secret__client_pb2.SecretReference
    warehouse: str
    def __init__(self, url: Optional[str] = ..., role: Optional[str] = ..., database: Optional[str] = ..., schema: Optional[str] = ..., warehouse: Optional[str] = ..., table: Optional[str] = ..., query: Optional[str] = ..., common_args: Optional[Union[BatchDataSourceCommonArgs, Mapping]] = ..., user: Optional[Union[_secret__client_pb2.SecretReference, Mapping]] = ..., password: Optional[Union[_secret__client_pb2.SecretReference, Mapping]] = ...) -> None: ...

class SparkBatchConfigArgs(_message.Message):
    __slots__ = ["data_delay", "data_source_function", "supports_time_filtering"]
    DATA_DELAY_FIELD_NUMBER: ClassVar[int]
    DATA_SOURCE_FUNCTION_FIELD_NUMBER: ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: ClassVar[int]
    data_delay: _duration_pb2.Duration
    data_source_function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, data_source_function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., data_delay: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class SparkStreamConfigArgs(_message.Message):
    __slots__ = ["data_source_function"]
    DATA_SOURCE_FUNCTION_FIELD_NUMBER: ClassVar[int]
    data_source_function: _user_defined_function__client_pb2.UserDefinedFunction
    def __init__(self, data_source_function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ...) -> None: ...

class StreamDataSourceCommonArgs(_message.Message):
    __slots__ = ["deduplication_columns", "post_processor", "timestamp_field", "watermark_delay_threshold"]
    DEDUPLICATION_COLUMNS_FIELD_NUMBER: ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: ClassVar[int]
    WATERMARK_DELAY_THRESHOLD_FIELD_NUMBER: ClassVar[int]
    deduplication_columns: _containers.RepeatedScalarFieldContainer[str]
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    timestamp_field: str
    watermark_delay_threshold: _duration_pb2.Duration
    def __init__(self, timestamp_field: Optional[str] = ..., watermark_delay_threshold: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., post_processor: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., deduplication_columns: Optional[Iterable[str]] = ...) -> None: ...

class UnityDataSourceArgs(_message.Message):
    __slots__ = ["access_mode", "catalog", "common_args", "datetime_partition_columns", "schema", "table", "timestamp_format"]
    ACCESS_MODE_FIELD_NUMBER: ClassVar[int]
    CATALOG_FIELD_NUMBER: ClassVar[int]
    COMMON_ARGS_FIELD_NUMBER: ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FORMAT_FIELD_NUMBER: ClassVar[int]
    access_mode: UnityCatalogAccessMode
    catalog: str
    common_args: BatchDataSourceCommonArgs
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumnArgs]
    schema: str
    table: str
    timestamp_format: str
    def __init__(self, catalog: Optional[str] = ..., schema: Optional[str] = ..., table: Optional[str] = ..., common_args: Optional[Union[BatchDataSourceCommonArgs, Mapping]] = ..., timestamp_format: Optional[str] = ..., datetime_partition_columns: Optional[Iterable[Union[DatetimePartitionColumnArgs, Mapping]]] = ..., access_mode: Optional[Union[UnityCatalogAccessMode, str]] = ...) -> None: ...

class UnityCatalogAccessMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
