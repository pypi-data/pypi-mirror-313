from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import data_source__client_pb2 as _data_source__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.common import data_source_type__client_pb2 as _data_source_type__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema_container__client_pb2 as _schema_container__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class VirtualDataSourceArgs(_message.Message):
    __slots__ = ["bigquery_ds_config", "file_ds_config", "forced_batch_schema", "forced_stream_schema", "hive_ds_config", "info", "kafka_ds_config", "kinesis_ds_config", "options", "pandas_batch_config", "prevent_destroy", "push_config", "redshift_ds_config", "schema", "snowflake_ds_config", "spark_batch_config", "spark_stream_config", "type", "unity_ds_config", "version", "virtual_data_source_id"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    BIGQUERY_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    FILE_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    FORCED_BATCH_SCHEMA_FIELD_NUMBER: ClassVar[int]
    FORCED_STREAM_SCHEMA_FIELD_NUMBER: ClassVar[int]
    HIVE_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    INFO_FIELD_NUMBER: ClassVar[int]
    KAFKA_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    KINESIS_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    PANDAS_BATCH_CONFIG_FIELD_NUMBER: ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: ClassVar[int]
    PUSH_CONFIG_FIELD_NUMBER: ClassVar[int]
    REDSHIFT_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    SNOWFLAKE_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    SPARK_BATCH_CONFIG_FIELD_NUMBER: ClassVar[int]
    SPARK_STREAM_CONFIG_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    UNITY_DS_CONFIG_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCE_ID_FIELD_NUMBER: ClassVar[int]
    bigquery_ds_config: _data_source__client_pb2.BigqueryDataSourceArgs
    file_ds_config: _data_source__client_pb2.FileDataSourceArgs
    forced_batch_schema: _spark_schema__client_pb2.SparkSchema
    forced_stream_schema: _spark_schema__client_pb2.SparkSchema
    hive_ds_config: _data_source__client_pb2.HiveDataSourceArgs
    info: _basic_info__client_pb2.BasicInfo
    kafka_ds_config: _data_source__client_pb2.KafkaDataSourceArgs
    kinesis_ds_config: _data_source__client_pb2.KinesisDataSourceArgs
    options: _containers.ScalarMap[str, str]
    pandas_batch_config: _data_source__client_pb2.PandasBatchConfigArgs
    prevent_destroy: bool
    push_config: _data_source__client_pb2.PushSourceArgs
    redshift_ds_config: _data_source__client_pb2.RedshiftDataSourceArgs
    schema: _schema_container__client_pb2.SchemaContainer
    snowflake_ds_config: _data_source__client_pb2.SnowflakeDataSourceArgs
    spark_batch_config: _data_source__client_pb2.SparkBatchConfigArgs
    spark_stream_config: _data_source__client_pb2.SparkStreamConfigArgs
    type: _data_source_type__client_pb2.DataSourceType
    unity_ds_config: _data_source__client_pb2.UnityDataSourceArgs
    version: _framework_version__client_pb2.FrameworkVersion
    virtual_data_source_id: _id__client_pb2.Id
    def __init__(self, virtual_data_source_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., info: Optional[Union[_basic_info__client_pb2.BasicInfo, Mapping]] = ..., version: Optional[Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., prevent_destroy: bool = ..., options: Optional[Mapping[str, str]] = ..., hive_ds_config: Optional[Union[_data_source__client_pb2.HiveDataSourceArgs, Mapping]] = ..., file_ds_config: Optional[Union[_data_source__client_pb2.FileDataSourceArgs, Mapping]] = ..., redshift_ds_config: Optional[Union[_data_source__client_pb2.RedshiftDataSourceArgs, Mapping]] = ..., snowflake_ds_config: Optional[Union[_data_source__client_pb2.SnowflakeDataSourceArgs, Mapping]] = ..., spark_batch_config: Optional[Union[_data_source__client_pb2.SparkBatchConfigArgs, Mapping]] = ..., unity_ds_config: Optional[Union[_data_source__client_pb2.UnityDataSourceArgs, Mapping]] = ..., pandas_batch_config: Optional[Union[_data_source__client_pb2.PandasBatchConfigArgs, Mapping]] = ..., bigquery_ds_config: Optional[Union[_data_source__client_pb2.BigqueryDataSourceArgs, Mapping]] = ..., kinesis_ds_config: Optional[Union[_data_source__client_pb2.KinesisDataSourceArgs, Mapping]] = ..., kafka_ds_config: Optional[Union[_data_source__client_pb2.KafkaDataSourceArgs, Mapping]] = ..., spark_stream_config: Optional[Union[_data_source__client_pb2.SparkStreamConfigArgs, Mapping]] = ..., push_config: Optional[Union[_data_source__client_pb2.PushSourceArgs, Mapping]] = ..., schema: Optional[Union[_schema_container__client_pb2.SchemaContainer, Mapping]] = ..., type: Optional[Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., forced_batch_schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., forced_stream_schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...
