from google.protobuf import duration_pb2 as _duration_pb2
from tecton_proto.args import data_source__client_pb2 as _data_source__client_pb2
from tecton_proto.args import data_source_config__client_pb2 as _data_source_config__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.data import hive_metastore__client_pb2 as _hive_metastore__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
FILE_DATA_SOURCE_FORMAT_CSV: FileDataSourceFormat
FILE_DATA_SOURCE_FORMAT_JSON: FileDataSourceFormat
FILE_DATA_SOURCE_FORMAT_PARQUET: FileDataSourceFormat

class BatchDataSource(_message.Message):
    __slots__ = ["batch_config", "bigquery", "data_delay", "date_partition_column", "datetime_partition_columns", "file", "hive_table", "pandas_data_source_function", "push_source_table", "raw_batch_translator", "redshift_db", "secrets", "snowflake", "spark_data_source_function", "spark_schema", "timestamp_column_properties", "unity_table"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[_secret__client_pb2.SecretReference, Mapping]] = ...) -> None: ...
    BATCH_CONFIG_FIELD_NUMBER: ClassVar[int]
    BIGQUERY_FIELD_NUMBER: ClassVar[int]
    DATA_DELAY_FIELD_NUMBER: ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: ClassVar[int]
    DATE_PARTITION_COLUMN_FIELD_NUMBER: ClassVar[int]
    FILE_FIELD_NUMBER: ClassVar[int]
    HIVE_TABLE_FIELD_NUMBER: ClassVar[int]
    PANDAS_DATA_SOURCE_FUNCTION_FIELD_NUMBER: ClassVar[int]
    PUSH_SOURCE_TABLE_FIELD_NUMBER: ClassVar[int]
    RAW_BATCH_TRANSLATOR_FIELD_NUMBER: ClassVar[int]
    REDSHIFT_DB_FIELD_NUMBER: ClassVar[int]
    SECRETS_FIELD_NUMBER: ClassVar[int]
    SNOWFLAKE_FIELD_NUMBER: ClassVar[int]
    SPARK_DATA_SOURCE_FUNCTION_FIELD_NUMBER: ClassVar[int]
    SPARK_SCHEMA_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_COLUMN_PROPERTIES_FIELD_NUMBER: ClassVar[int]
    UNITY_TABLE_FIELD_NUMBER: ClassVar[int]
    batch_config: _data_source_config__client_pb2.BatchConfig
    bigquery: BigqueryDataSource
    data_delay: _duration_pb2.Duration
    date_partition_column: str
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumn]
    file: FileDataSource
    hive_table: _hive_metastore__client_pb2.HiveTableDataSource
    pandas_data_source_function: PandasBatchDataSourceFunction
    push_source_table: PushDataSource
    raw_batch_translator: _user_defined_function__client_pb2.UserDefinedFunction
    redshift_db: RedshiftDataSource
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    snowflake: SnowflakeDataSource
    spark_data_source_function: SparkBatchDataSourceFunction
    spark_schema: _spark_schema__client_pb2.SparkSchema
    timestamp_column_properties: TimestampColumnProperties
    unity_table: UnityTableDataSource
    def __init__(self, hive_table: Optional[Union[_hive_metastore__client_pb2.HiveTableDataSource, Mapping]] = ..., file: Optional[Union[FileDataSource, Mapping]] = ..., redshift_db: Optional[Union[RedshiftDataSource, Mapping]] = ..., snowflake: Optional[Union[SnowflakeDataSource, Mapping]] = ..., spark_data_source_function: Optional[Union[SparkBatchDataSourceFunction, Mapping]] = ..., unity_table: Optional[Union[UnityTableDataSource, Mapping]] = ..., push_source_table: Optional[Union[PushDataSource, Mapping]] = ..., pandas_data_source_function: Optional[Union[PandasBatchDataSourceFunction, Mapping]] = ..., bigquery: Optional[Union[BigqueryDataSource, Mapping]] = ..., spark_schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., timestamp_column_properties: Optional[Union[TimestampColumnProperties, Mapping]] = ..., batch_config: Optional[Union[_data_source_config__client_pb2.BatchConfig, Mapping]] = ..., date_partition_column: Optional[str] = ..., datetime_partition_columns: Optional[Iterable[Union[DatetimePartitionColumn, Mapping]]] = ..., raw_batch_translator: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., data_delay: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., secrets: Optional[Mapping[str, _secret__client_pb2.SecretReference]] = ...) -> None: ...

class BigqueryDataSource(_message.Message):
    __slots__ = ["credentials", "dataset", "location", "project_id", "query", "table"]
    CREDENTIALS_FIELD_NUMBER: ClassVar[int]
    DATASET_FIELD_NUMBER: ClassVar[int]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    credentials: _secret__client_pb2.SecretReference
    dataset: str
    location: str
    project_id: str
    query: str
    table: str
    def __init__(self, project_id: Optional[str] = ..., dataset: Optional[str] = ..., location: Optional[str] = ..., table: Optional[str] = ..., query: Optional[str] = ..., credentials: Optional[Union[_secret__client_pb2.SecretReference, Mapping]] = ...) -> None: ...

class DatetimePartitionColumn(_message.Message):
    __slots__ = ["column_name", "format_string", "minimum_seconds"]
    COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    FORMAT_STRING_FIELD_NUMBER: ClassVar[int]
    MINIMUM_SECONDS_FIELD_NUMBER: ClassVar[int]
    column_name: str
    format_string: str
    minimum_seconds: int
    def __init__(self, column_name: Optional[str] = ..., format_string: Optional[str] = ..., minimum_seconds: Optional[int] = ...) -> None: ...

class FileDataSource(_message.Message):
    __slots__ = ["convert_to_glue_format", "format", "schema_override", "schema_uri", "uri"]
    CONVERT_TO_GLUE_FORMAT_FIELD_NUMBER: ClassVar[int]
    FORMAT_FIELD_NUMBER: ClassVar[int]
    SCHEMA_OVERRIDE_FIELD_NUMBER: ClassVar[int]
    SCHEMA_URI_FIELD_NUMBER: ClassVar[int]
    URI_FIELD_NUMBER: ClassVar[int]
    convert_to_glue_format: bool
    format: FileDataSourceFormat
    schema_override: _spark_schema__client_pb2.SparkSchema
    schema_uri: str
    uri: str
    def __init__(self, uri: Optional[str] = ..., format: Optional[Union[FileDataSourceFormat, str]] = ..., convert_to_glue_format: bool = ..., schema_uri: Optional[str] = ..., schema_override: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...

class PandasBatchDataSourceFunction(_message.Message):
    __slots__ = ["function", "supports_time_filtering"]
    FUNCTION_FIELD_NUMBER: ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class PushDataSource(_message.Message):
    __slots__ = ["ingested_data_location"]
    INGESTED_DATA_LOCATION_FIELD_NUMBER: ClassVar[int]
    ingested_data_location: str
    def __init__(self, ingested_data_location: Optional[str] = ...) -> None: ...

class RedshiftDataSource(_message.Message):
    __slots__ = ["cluster_id", "database", "endpoint", "query", "table", "temp_s3"]
    CLUSTER_ID_FIELD_NUMBER: ClassVar[int]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    ENDPOINT_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    TEMP_S3_FIELD_NUMBER: ClassVar[int]
    cluster_id: str
    database: str
    endpoint: str
    query: str
    table: str
    temp_s3: str
    def __init__(self, endpoint: Optional[str] = ..., cluster_id: Optional[str] = ..., database: Optional[str] = ..., table: Optional[str] = ..., query: Optional[str] = ..., temp_s3: Optional[str] = ...) -> None: ...

class SnowflakeDataSource(_message.Message):
    __slots__ = ["snowflakeArgs"]
    SNOWFLAKEARGS_FIELD_NUMBER: ClassVar[int]
    snowflakeArgs: _data_source__client_pb2.SnowflakeDataSourceArgs
    def __init__(self, snowflakeArgs: Optional[Union[_data_source__client_pb2.SnowflakeDataSourceArgs, Mapping]] = ...) -> None: ...

class SparkBatchDataSourceFunction(_message.Message):
    __slots__ = ["function", "supports_time_filtering"]
    FUNCTION_FIELD_NUMBER: ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class TimestampColumnProperties(_message.Message):
    __slots__ = ["column_name", "format"]
    COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    FORMAT_FIELD_NUMBER: ClassVar[int]
    column_name: str
    format: str
    def __init__(self, column_name: Optional[str] = ..., format: Optional[str] = ...) -> None: ...

class UnityTableDataSource(_message.Message):
    __slots__ = ["access_mode", "catalog", "schema", "table"]
    ACCESS_MODE_FIELD_NUMBER: ClassVar[int]
    CATALOG_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    access_mode: _data_source__client_pb2.UnityCatalogAccessMode
    catalog: str
    schema: str
    table: str
    def __init__(self, catalog: Optional[str] = ..., schema: Optional[str] = ..., table: Optional[str] = ..., access_mode: Optional[Union[_data_source__client_pb2.UnityCatalogAccessMode, str]] = ...) -> None: ...

class FileDataSourceFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
