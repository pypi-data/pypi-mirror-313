from tecton_proto.args import data_source_config__client_pb2 as _data_source_config__client_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.data import hive_metastore__client_pb2 as _hive_metastore__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.data import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecuteRequest(_message.Message):
    __slots__ = ["envVars", "getBatchDataSourceFunctionSchema", "getFeatureViewSchema", "getFileSourceSchema", "getHiveTableSchema", "getKafkaSourceSchema", "getKinesisSourceSchema", "getMultipleDataSourceSchemasRequest", "getMultipleFeatureViewSchemasRequest", "getQueryPlanInfoForFeatureViewPipeline", "getRedshiftTableSchema", "getSnowflakeSchema", "getStreamDataSourceFunctionSchema", "getUnityTableSchema", "listHiveDatabases", "listHiveTableColumns", "listHiveTables"]
    class EnvVarsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ENVVARS_FIELD_NUMBER: ClassVar[int]
    GETBATCHDATASOURCEFUNCTIONSCHEMA_FIELD_NUMBER: ClassVar[int]
    GETFEATUREVIEWSCHEMA_FIELD_NUMBER: ClassVar[int]
    GETFILESOURCESCHEMA_FIELD_NUMBER: ClassVar[int]
    GETHIVETABLESCHEMA_FIELD_NUMBER: ClassVar[int]
    GETKAFKASOURCESCHEMA_FIELD_NUMBER: ClassVar[int]
    GETKINESISSOURCESCHEMA_FIELD_NUMBER: ClassVar[int]
    GETMULTIPLEDATASOURCESCHEMASREQUEST_FIELD_NUMBER: ClassVar[int]
    GETMULTIPLEFEATUREVIEWSCHEMASREQUEST_FIELD_NUMBER: ClassVar[int]
    GETQUERYPLANINFOFORFEATUREVIEWPIPELINE_FIELD_NUMBER: ClassVar[int]
    GETREDSHIFTTABLESCHEMA_FIELD_NUMBER: ClassVar[int]
    GETSNOWFLAKESCHEMA_FIELD_NUMBER: ClassVar[int]
    GETSTREAMDATASOURCEFUNCTIONSCHEMA_FIELD_NUMBER: ClassVar[int]
    GETUNITYTABLESCHEMA_FIELD_NUMBER: ClassVar[int]
    LISTHIVEDATABASES_FIELD_NUMBER: ClassVar[int]
    LISTHIVETABLECOLUMNS_FIELD_NUMBER: ClassVar[int]
    LISTHIVETABLES_FIELD_NUMBER: ClassVar[int]
    envVars: _containers.ScalarMap[str, str]
    getBatchDataSourceFunctionSchema: GetBatchDataSourceFunctionSchema
    getFeatureViewSchema: GetFeatureViewSchema
    getFileSourceSchema: GetFileSourceSchema
    getHiveTableSchema: GetHiveTableSchema
    getKafkaSourceSchema: GetKafkaSourceSchema
    getKinesisSourceSchema: GetKinesisSourceSchema
    getMultipleDataSourceSchemasRequest: GetMultipleDataSourceSchemasRequest
    getMultipleFeatureViewSchemasRequest: GetMultipleFeatureViewSchemasRequest
    getQueryPlanInfoForFeatureViewPipeline: GetQueryPlanInfoForFeatureViewPipeline
    getRedshiftTableSchema: GetRedshiftTableSchema
    getSnowflakeSchema: GetSnowflakeSchema
    getStreamDataSourceFunctionSchema: GetStreamDataSourceFunctionSchema
    getUnityTableSchema: GetUnityTableSchema
    listHiveDatabases: ListHiveDatabases
    listHiveTableColumns: ListHiveTableColumns
    listHiveTables: ListHiveTables
    def __init__(self, getMultipleFeatureViewSchemasRequest: Optional[Union[GetMultipleFeatureViewSchemasRequest, Mapping]] = ..., getMultipleDataSourceSchemasRequest: Optional[Union[GetMultipleDataSourceSchemasRequest, Mapping]] = ..., getHiveTableSchema: Optional[Union[GetHiveTableSchema, Mapping]] = ..., getRedshiftTableSchema: Optional[Union[GetRedshiftTableSchema, Mapping]] = ..., getFileSourceSchema: Optional[Union[GetFileSourceSchema, Mapping]] = ..., getKinesisSourceSchema: Optional[Union[GetKinesisSourceSchema, Mapping]] = ..., getKafkaSourceSchema: Optional[Union[GetKafkaSourceSchema, Mapping]] = ..., getFeatureViewSchema: Optional[Union[GetFeatureViewSchema, Mapping]] = ..., getSnowflakeSchema: Optional[Union[GetSnowflakeSchema, Mapping]] = ..., getBatchDataSourceFunctionSchema: Optional[Union[GetBatchDataSourceFunctionSchema, Mapping]] = ..., getStreamDataSourceFunctionSchema: Optional[Union[GetStreamDataSourceFunctionSchema, Mapping]] = ..., getUnityTableSchema: Optional[Union[GetUnityTableSchema, Mapping]] = ..., listHiveDatabases: Optional[Union[ListHiveDatabases, Mapping]] = ..., listHiveTables: Optional[Union[ListHiveTables, Mapping]] = ..., listHiveTableColumns: Optional[Union[ListHiveTableColumns, Mapping]] = ..., getQueryPlanInfoForFeatureViewPipeline: Optional[Union[GetQueryPlanInfoForFeatureViewPipeline, Mapping]] = ..., envVars: Optional[Mapping[str, str]] = ...) -> None: ...

class ExecuteResult(_message.Message):
    __slots__ = ["listHiveResult", "multipleDataSourceSchemaResponse", "multipleFeatureViewSchemaResponse", "queryPlanInfo", "schema", "sparkSchema", "uncaughtError", "validationError"]
    LISTHIVERESULT_FIELD_NUMBER: ClassVar[int]
    MULTIPLEDATASOURCESCHEMARESPONSE_FIELD_NUMBER: ClassVar[int]
    MULTIPLEFEATUREVIEWSCHEMARESPONSE_FIELD_NUMBER: ClassVar[int]
    QUERYPLANINFO_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    SPARKSCHEMA_FIELD_NUMBER: ClassVar[int]
    UNCAUGHTERROR_FIELD_NUMBER: ClassVar[int]
    VALIDATIONERROR_FIELD_NUMBER: ClassVar[int]
    listHiveResult: _hive_metastore__client_pb2.ListHiveResult
    multipleDataSourceSchemaResponse: GetMultipleDataSourceSchemasResponse
    multipleFeatureViewSchemaResponse: GetMultipleFeatureViewSchemasResponse
    queryPlanInfo: QueryPlanInfo
    schema: _schema__client_pb2.Schema
    sparkSchema: _spark_schema__client_pb2.SparkSchema
    uncaughtError: str
    validationError: str
    def __init__(self, uncaughtError: Optional[str] = ..., validationError: Optional[str] = ..., sparkSchema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., queryPlanInfo: Optional[Union[QueryPlanInfo, Mapping]] = ..., schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., listHiveResult: Optional[Union[_hive_metastore__client_pb2.ListHiveResult, Mapping]] = ..., multipleFeatureViewSchemaResponse: Optional[Union[GetMultipleFeatureViewSchemasResponse, Mapping]] = ..., multipleDataSourceSchemaResponse: Optional[Union[GetMultipleDataSourceSchemasResponse, Mapping]] = ...) -> None: ...

class FeatureViewSchemaRequest(_message.Message):
    __slots__ = ["feature_view", "join_keys", "temporal_aggregate"]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: ClassVar[int]
    TEMPORAL_AGGREGATE_FIELD_NUMBER: ClassVar[int]
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    temporal_aggregate: _feature_view__client_pb2.TemporalAggregate
    def __init__(self, feature_view: Optional[Union[_feature_view__client_pb2.FeatureViewArgs, Mapping]] = ..., join_keys: Optional[Iterable[str]] = ..., temporal_aggregate: Optional[Union[_feature_view__client_pb2.TemporalAggregate, Mapping]] = ...) -> None: ...

class FeatureViewSchemaResponse(_message.Message):
    __slots__ = ["timestamp_key", "view_schema"]
    TIMESTAMP_KEY_FIELD_NUMBER: ClassVar[int]
    VIEW_SCHEMA_FIELD_NUMBER: ClassVar[int]
    timestamp_key: str
    view_schema: _schema__client_pb2.Schema
    def __init__(self, view_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., timestamp_key: Optional[str] = ...) -> None: ...

class GetBatchDataSourceFunctionSchema(_message.Message):
    __slots__ = ["function", "supports_time_filtering"]
    FUNCTION_FIELD_NUMBER: ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class GetFeatureViewSchema(_message.Message):
    __slots__ = ["feature_view", "transformations", "virtual_data_sources"]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: ClassVar[int]
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSource]
    def __init__(self, virtual_data_sources: Optional[Iterable[Union[_virtual_data_source__client_pb2.VirtualDataSource, Mapping]]] = ..., transformations: Optional[Iterable[Union[_transformation__client_pb2.Transformation, Mapping]]] = ..., feature_view: Optional[Union[_feature_view__client_pb2.FeatureViewArgs, Mapping]] = ...) -> None: ...

class GetFileSourceSchema(_message.Message):
    __slots__ = ["convertToGlueFormat", "fileFormat", "rawBatchTranslator", "schemaOverride", "schemaUri", "timestampColumn", "timestampFormat", "uri"]
    CONVERTTOGLUEFORMAT_FIELD_NUMBER: ClassVar[int]
    FILEFORMAT_FIELD_NUMBER: ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: ClassVar[int]
    SCHEMAOVERRIDE_FIELD_NUMBER: ClassVar[int]
    SCHEMAURI_FIELD_NUMBER: ClassVar[int]
    TIMESTAMPCOLUMN_FIELD_NUMBER: ClassVar[int]
    TIMESTAMPFORMAT_FIELD_NUMBER: ClassVar[int]
    URI_FIELD_NUMBER: ClassVar[int]
    convertToGlueFormat: bool
    fileFormat: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    schemaOverride: _spark_schema__client_pb2.SparkSchema
    schemaUri: str
    timestampColumn: str
    timestampFormat: str
    uri: str
    def __init__(self, uri: Optional[str] = ..., fileFormat: Optional[str] = ..., convertToGlueFormat: bool = ..., rawBatchTranslator: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., schemaUri: Optional[str] = ..., timestampColumn: Optional[str] = ..., timestampFormat: Optional[str] = ..., schemaOverride: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...

class GetHiveTableSchema(_message.Message):
    __slots__ = ["database", "rawBatchTranslator", "table", "timestampColumn", "timestampFormat"]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    TIMESTAMPCOLUMN_FIELD_NUMBER: ClassVar[int]
    TIMESTAMPFORMAT_FIELD_NUMBER: ClassVar[int]
    database: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    table: str
    timestampColumn: str
    timestampFormat: str
    def __init__(self, database: Optional[str] = ..., table: Optional[str] = ..., timestampColumn: Optional[str] = ..., timestampFormat: Optional[str] = ..., rawBatchTranslator: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ...) -> None: ...

class GetKafkaSourceSchema(_message.Message):
    __slots__ = ["rawStreamTranslator", "ssl_keystore_location", "ssl_keystore_password_secret_id"]
    RAWSTREAMTRANSLATOR_FIELD_NUMBER: ClassVar[int]
    SSL_KEYSTORE_LOCATION_FIELD_NUMBER: ClassVar[int]
    SSL_KEYSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: ClassVar[int]
    rawStreamTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    ssl_keystore_location: str
    ssl_keystore_password_secret_id: str
    def __init__(self, rawStreamTranslator: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., ssl_keystore_location: Optional[str] = ..., ssl_keystore_password_secret_id: Optional[str] = ...) -> None: ...

class GetKinesisSourceSchema(_message.Message):
    __slots__ = ["rawStreamTranslator", "streamName"]
    RAWSTREAMTRANSLATOR_FIELD_NUMBER: ClassVar[int]
    STREAMNAME_FIELD_NUMBER: ClassVar[int]
    rawStreamTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    streamName: str
    def __init__(self, streamName: Optional[str] = ..., rawStreamTranslator: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ...) -> None: ...

class GetMultipleDataSourceSchemasRequest(_message.Message):
    __slots__ = ["data_source_args"]
    DATA_SOURCE_ARGS_FIELD_NUMBER: ClassVar[int]
    data_source_args: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSourceArgs]
    def __init__(self, data_source_args: Optional[Iterable[Union[_virtual_data_source__client_pb2.VirtualDataSourceArgs, Mapping]]] = ...) -> None: ...

class GetMultipleDataSourceSchemasResponse(_message.Message):
    __slots__ = ["data_source_responses"]
    class DataSourceResponsesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: SparkSchemas
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[SparkSchemas, Mapping]] = ...) -> None: ...
    DATA_SOURCE_RESPONSES_FIELD_NUMBER: ClassVar[int]
    data_source_responses: _containers.MessageMap[str, SparkSchemas]
    def __init__(self, data_source_responses: Optional[Mapping[str, SparkSchemas]] = ...) -> None: ...

class GetMultipleFeatureViewSchemasRequest(_message.Message):
    __slots__ = ["feature_view_requests", "transformations", "virtual_data_sources"]
    FEATURE_VIEW_REQUESTS_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: ClassVar[int]
    feature_view_requests: _containers.RepeatedCompositeFieldContainer[FeatureViewSchemaRequest]
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSource]
    def __init__(self, virtual_data_sources: Optional[Iterable[Union[_virtual_data_source__client_pb2.VirtualDataSource, Mapping]]] = ..., transformations: Optional[Iterable[Union[_transformation__client_pb2.Transformation, Mapping]]] = ..., feature_view_requests: Optional[Iterable[Union[FeatureViewSchemaRequest, Mapping]]] = ...) -> None: ...

class GetMultipleFeatureViewSchemasResponse(_message.Message):
    __slots__ = ["feature_view_responses"]
    class FeatureViewResponsesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: FeatureViewSchemaResponse
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[FeatureViewSchemaResponse, Mapping]] = ...) -> None: ...
    FEATURE_VIEW_RESPONSES_FIELD_NUMBER: ClassVar[int]
    feature_view_responses: _containers.MessageMap[str, FeatureViewSchemaResponse]
    def __init__(self, feature_view_responses: Optional[Mapping[str, FeatureViewSchemaResponse]] = ...) -> None: ...

class GetQueryPlanInfoForFeatureViewPipeline(_message.Message):
    __slots__ = ["feature_view", "transformations", "virtual_data_sources"]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: ClassVar[int]
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSource]
    def __init__(self, virtual_data_sources: Optional[Iterable[Union[_virtual_data_source__client_pb2.VirtualDataSource, Mapping]]] = ..., transformations: Optional[Iterable[Union[_transformation__client_pb2.Transformation, Mapping]]] = ..., feature_view: Optional[Union[_feature_view__client_pb2.FeatureViewArgs, Mapping]] = ...) -> None: ...

class GetRedshiftTableSchema(_message.Message):
    __slots__ = ["endpoint", "query", "rawBatchTranslator", "table", "temp_s3_dir"]
    ENDPOINT_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    TEMP_S3_DIR_FIELD_NUMBER: ClassVar[int]
    endpoint: str
    query: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    table: str
    temp_s3_dir: str
    def __init__(self, endpoint: Optional[str] = ..., table: Optional[str] = ..., query: Optional[str] = ..., rawBatchTranslator: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., temp_s3_dir: Optional[str] = ...) -> None: ...

class GetSnowflakeSchema(_message.Message):
    __slots__ = ["database", "post_processor", "query", "role", "schema", "table", "url", "warehouse"]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    ROLE_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    URL_FIELD_NUMBER: ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: ClassVar[int]
    database: str
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    query: str
    role: str
    schema: str
    table: str
    url: str
    warehouse: str
    def __init__(self, url: Optional[str] = ..., role: Optional[str] = ..., database: Optional[str] = ..., schema: Optional[str] = ..., warehouse: Optional[str] = ..., table: Optional[str] = ..., query: Optional[str] = ..., post_processor: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ...) -> None: ...

class GetStreamDataSourceFunctionSchema(_message.Message):
    __slots__ = ["function"]
    FUNCTION_FIELD_NUMBER: ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    def __init__(self, function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ...) -> None: ...

class GetUnityTableSchema(_message.Message):
    __slots__ = ["catalog", "rawBatchTranslator", "schema", "table", "timestampColumn", "timestampFormat"]
    CATALOG_FIELD_NUMBER: ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: ClassVar[int]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    TIMESTAMPCOLUMN_FIELD_NUMBER: ClassVar[int]
    TIMESTAMPFORMAT_FIELD_NUMBER: ClassVar[int]
    catalog: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    schema: str
    table: str
    timestampColumn: str
    timestampFormat: str
    def __init__(self, catalog: Optional[str] = ..., schema: Optional[str] = ..., table: Optional[str] = ..., timestampColumn: Optional[str] = ..., timestampFormat: Optional[str] = ..., rawBatchTranslator: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ...) -> None: ...

class ListHiveDatabases(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListHiveTableColumns(_message.Message):
    __slots__ = ["database", "table"]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    TABLE_FIELD_NUMBER: ClassVar[int]
    database: str
    table: str
    def __init__(self, database: Optional[str] = ..., table: Optional[str] = ...) -> None: ...

class ListHiveTables(_message.Message):
    __slots__ = ["database"]
    DATABASE_FIELD_NUMBER: ClassVar[int]
    database: str
    def __init__(self, database: Optional[str] = ...) -> None: ...

class QueryPlanInfo(_message.Message):
    __slots__ = ["has_aggregations", "has_joins"]
    HAS_AGGREGATIONS_FIELD_NUMBER: ClassVar[int]
    HAS_JOINS_FIELD_NUMBER: ClassVar[int]
    has_aggregations: bool
    has_joins: bool
    def __init__(self, has_joins: bool = ..., has_aggregations: bool = ...) -> None: ...

class SparkSchemas(_message.Message):
    __slots__ = ["batchSchema", "streamSchema"]
    BATCHSCHEMA_FIELD_NUMBER: ClassVar[int]
    STREAMSCHEMA_FIELD_NUMBER: ClassVar[int]
    batchSchema: _spark_schema__client_pb2.SparkSchema
    streamSchema: _spark_schema__client_pb2.SparkSchema
    def __init__(self, batchSchema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., streamSchema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...
