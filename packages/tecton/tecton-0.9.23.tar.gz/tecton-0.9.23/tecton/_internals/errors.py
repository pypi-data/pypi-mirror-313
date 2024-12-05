from typing import List
from typing import Optional
from typing import Set

from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.schema import Schema
from tecton_proto.common import schema_pb2


# Generic
def INTERNAL_ERROR(message):
    return TectonInternalError(
        f"We seem to have encountered an error. Please contact support for assistance. Error details: {message}"
    )


def MDS_INACCESSIBLE(host_port):
    return TectonInternalError(
        f"Failed to connect to Tecton at {host_port}, please check your connectivity or contact support"
    )


def VALIDATION_ERROR_FROM_MDS(message, trace_id: Optional[str] = None):
    suffix = f", trace ID: {trace_id}" if trace_id else ""
    return TectonValidationError(f"{message}{suffix}")


def UNSUPPORTED_OPERATION(op, reason):
    return TectonValidationError(f"Operation '{op}' is not supported: {reason}")


def INVALID_SPINE_TIME_KEY_TYPE_SPARK(t):
    return TectonValidationError(
        f"Invalid type of timestamp_key column in the input events dataframe. Expected TimestampType, got {t}"
    )


INVALID_NULL_SPINE_TIME_KEY = TectonValidationError(
    "Unable to infer the time range of the events dataframe. This typically occurs when all the timestamps in the dataframe are null."
)


def INVALID_SPINE_TIME_KEY_TYPE_PANDAS(t):
    return TectonValidationError(
        f"Invalid type of timestamp_key column in the given events dataframe. Expected datetime, got {t}"
    )


def MISSING_SPINE_COLUMN(param, col, existing_cols):
    return TectonValidationError(
        f"{param} column is missing from the events dataframe. Expected to find '{col}' among available columns: '{', '.join(existing_cols)}'."
    )


def MISSING_REQUEST_DATA_IN_SPINE(key, existing_cols):
    return TectonValidationError(
        f"Request context key '{key}' not found in the events dataframe schema. Expected to find '{key}' among available columns: '{', '.join(existing_cols)}'."
    )


def NONEXISTENT_WORKSPACE(name, workspaces):
    return TectonValidationError(f'Workspace "{name}" not found. Available workspaces: {workspaces}')


def INCORRECT_MATERIALIZATION_ENABLED_FLAG(user_set_bool, server_side_bool):
    return TectonValidationError(
        f"'is_live={user_set_bool}' argument does not match the value on the server: {server_side_bool}"
    )


def UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(op):
    return TectonValidationError(f"Operation '{op}' is not supported in a development workspace")


def INVALID_JOIN_KEYS_TYPE(t):
    return TectonValidationError(f"Invalid type for join_keys. Expected Dict[str, Union[int, str, bytes]], got {t}")


def INVALID_REQUEST_DATA_TYPE(t):
    return TectonValidationError(
        f"Invalid type for request_data. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
    )


def INVALID_REQUEST_CONTEXT_TYPE(t):
    return TectonValidationError(
        f"Invalid type for request_context_map. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
    )


def INVALID_INDIVIDUAL_JOIN_KEY_TYPE(key: str, type_str: str):
    return TectonValidationError(
        f"Invalid type for join_key '{key}'. Expected either type int, str, or bytes, got {type_str}"
    )


def EMPTY_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not be empty.")


def EMPTY_ELEMENT_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have an empty element.")


def DUPLICATED_ELEMENTS_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have duplicated elements.")


def DATA_SOURCE_HAS_NO_BATCH_CONFIG(data_source: str):
    return TectonValidationError(
        f"Cannot run get_dataframe on locally defined Data Source '{data_source}' because it does not have a batch_config"
    )


def FEATURE_VIEW_HAS_NO_BATCH_SOURCE(feature_view: str):
    return TectonValidationError(
        f"Cannot run get_historical_features with from_source=True for Feature View {feature_view} because it depends on a Data Source which does not have a batch config set. Please retry with from_source=False"
    )


def FEATURE_VIEW_HAS_NO_STREAM_SOURCE(feature_view: str):
    return TectonValidationError(
        f"Cannot run run_stream on Feature View {feature_view} because it does not have a Stream Source"
    )


def UNKNOWN_REQUEST_CONTEXT_KEY(keys, key):
    return TectonValidationError(f"Unknown request context key '{key}', expected one of: {keys}")


def FV_TIME_KEY_MISSING(fv_name):
    return TectonValidationError(f"Argument 'timestamp_key' is required for the feature definition '{fv_name}'")


def FV_NO_MATERIALIZED_DATA(fv_name):
    return TectonValidationError(
        f"Feature definition '{fv_name}' doesn't have any materialized data. Materialization jobs may not have updated the offline feature store yet. Please monitor using materialization_status() or use from_source=True to compute from source data."
    )


def ODFV_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(odfv_name, workspace):
    return TectonValidationError(
        f"On-Demand Feature View {odfv_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). Please use from_source=True when retrieving features or alternatively use a live workspace and configure offline materialization for all dependent Feature Views."
    )


def FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(fd_name, workspace):
    return TectonValidationError(
        f"Feature Definition {fd_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). Please use from_source=True when getting features (not applicable for Feature Tables) or alternatively configure offline materialization for this Feature Definition in a live workspace."
    )


def FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(ft_name, workspace):
    return TectonValidationError(
        f"Feature Table {ft_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). Please apply this Feature Table to a live workspace and ingest some features before using with get_historical_features()."
    )


def FEATURE_TABLE_GET_ONLINE_FEATURES_FROM_DEVELOPMENT_WORKSPACE(ft_name, workspace):
    return TectonValidationError(
        f"Feature Table {ft_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). Please apply this Feature Table to a live workspace and ingest some features before using with get_online_features()."
    )


def STREAM_COMPACTION_ENABLED_DEPRECATED():
    return TectonValidationError(
        "FeatureView.stream_compaction_enabled is deprecated. Please use stream_tiling_enabled instead. stream_tiling_enabled has the same semantics and is just a new name."
    )


def FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE(ft_name):
    return TectonValidationError(
        f"Feature Table {ft_name} does not have offline materialization enabled, i.e. offline=True. Cannot retrieve offline feature if offline materializaiton is not enabled."
    )


def FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(fv_name, fco_name):
    return TectonValidationError(
        f"{fco_name} {fv_name} is defined locally, i.e. it has not been applied to a Tecton workspace. In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
    )


def FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE_GFD(fv_name, workspace):
    return TectonValidationError(
        f"Feature View {fv_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
    )


def FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(fv_name, workspace):
    return TectonValidationError(
        f"Feature view {fv_name} uses incremental backfills and is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
        + "Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
        + "Enable offline materialization for this feature view in a live workspace to use `get_historical_features()`, or use `run()` to test this feature view without materializing data."
    )


def FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_IN_LOCAL_MODE(fv_name):
    return TectonValidationError(
        f"Feature view {fv_name} uses incremental backfills and is locally defined which means materialization is not enabled."
        + "Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
        + "Apply and enable offline materialization for this feature view in a live workspace to use `get_historical_features()`, or use `run()` to test this feature view locally in a notebook."
    )


def FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_MOCK_DATA(
    fv_name: str, method_name: str = "get_historical_features"
):
    return TectonValidationError(
        f"Feature view {fv_name} uses incremental backfills and is locally defined which means materialization is not enabled."
        + "Computing features from mock data is not supported for Batch Feature Views with incremental_backfills set to True."
        + f"Apply and enable offline materialization for this feature view in a live workspace to use `{method_name}()` or use `run_transformation()` to test this Feature View."
    )


def FD_GET_FEATURES_MATERIALIZATION_DISABLED(fd_name):
    return TectonValidationError(
        f"Feature View {fd_name} does not have offline materialization turned on. In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
    )


def FV_GET_FEATURES_MATERIALIZATION_DISABLED_GFD(fv_name):
    return TectonValidationError(
        f"Feature View {fv_name} does not have offline materialization turned on. Try calling this function with 'use_materialized_data=False' or alternatively configure offline materialization for this Feature View."
    )


# DataSources
DS_STREAM_PREVIEW_ON_NON_STREAM = TectonValidationError("'start_stream_preview' called on non-streaming data source")

DS_DATAFRAME_NO_TIMESTAMP = TectonValidationError(
    "Cannot find timestamp column for this data source. Please call 'get_dataframe' without parameters 'start_time' or 'end_time'."
)

DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER = TectonValidationError(
    "The method 'get_dataframe()' cannot filter on timestamps when 'apply_translator' is False. "
    "'start_time' and 'end_time' must be None."
)

DS_INCORRECT_SUPPORTS_TIME_FILTERING = TectonValidationError(
    "Cannot filter on timestamps when supports_time_filtering on data source is False. "
    "'start_time' and 'end_time' must be None."
)


def FS_BACKEND_ERROR(message):
    return TectonInternalError(f"Error calling Feature Service API: {message}")


FS_GET_FEATURE_VECTOR_REQUIRED_ARGS = TectonValidationError(
    "get_feature_vector requires at least one of join_keys or request_context_map"
)

FS_API_KEY_MISSING = TectonValidationError(
    "API key is required for online feature requests, but was not found in the environment. Please generate a key and set TECTON_API_KEY "
    + "using https://docs.tecton.ai/docs/reading-feature-data/reading-feature-data-for-inference"
)


def FV_INVALID_MOCK_SOURCES(mock_sources_keys: List[str], fv_params: List[str]):
    return TectonValidationError(
        f"Mock sources {mock_sources_keys} do not match the Feature View's input parameters {fv_params}"
    )


def FV_INVALID_MOCK_INPUTS(mock_inputs: List[str], inputs: List[str]):
    return TectonValidationError(f"Mock input {mock_inputs} do not match FeatureView's inputs {inputs}")


def UNDEFINED_REQUEST_SOURCE_INPUT(undefined_inputs: List[str], expected_inputs: List[str]):
    return TectonValidationError(
        f"The provided request source data contains keys not defined in the request source schema. Extraneous keys: {undefined_inputs}. Expected keys: {expected_inputs}."
    )


def FV_INVALID_MOCK_INPUTS_NUM_ROWS(num_rows: List[int]):
    return TectonValidationError(
        f"Number of rows are not equal across all mock_inputs. Number of rows found are: {str(num_rows)}."
    )


def FV_UNSUPPORTED_ARG(invalid_arg_name: str):
    return TectonValidationError(f"Argument '{invalid_arg_name}' is not supported for this FeatureView type.")


def FV_INVALID_ARG_VALUE(arg_name: str, value: str, expected: str):
    return TectonValidationError(f"Invalid argument value '{arg_name}={value}', supported value(s): '{expected}'")


def FV_INVALID_ARG_COMBO(arg_names: List[str]):
    return TectonValidationError(f"Invalid argument combinations; {str(arg_names)} cannot be used together.")


def FT_UNABLE_TO_ACCESS_SOURCE_DATA(fv_name):
    return TectonValidationError(
        f"The source data for FeatureTable {fv_name} does not exist. Please use from_source=False when calling this function."
    )


def UNVALIDATED_FEATURE_VIEWS_FROM_SOURCE_FALSE(fv_name, method_name):
    return TectonValidationError(
        f"Feature view {fv_name} is not validated since `TECTON_VALIDATION_MODE=skip`. When calling `{method_name}` on unvalidated feature views, `from_source` cannot be set to False. Please remove the `from_source` parameter from your call or set `from_source=True`."
    )


class InvalidTransformationMode(TectonValidationError):
    def __init__(self, name: str, got: str, allowed_modes: List[str]):
        super().__init__(f"Mode for '{name}' is '{got}', must be one of: {', '.join(allowed_modes)}")


class InvalidConstantType(TectonValidationError):
    def __init__(self, value, allowed_types):
        allowed_types = [str(allowed_type) for allowed_type in allowed_types]
        super().__init__(
            f"Tecton const value '{value}' must have one of the following types: {', '.join(allowed_types)}"
        )


class InvalidTransformInvocation(TectonValidationError):
    def __init__(self, transformation_name: str, got: str):
        super().__init__(
            f"Allowed arguments for Transformation '{transformation_name}' are: "
            f"tecton.const, tecton.materialization_context, transformations, and DataSource inputs. Got: '{got}'"
        )


# Dataset
DATASET_SPINE_COLUMNS_NOT_SET = TectonValidationError(
    "Cannot retrieve the events dataframe when Dataset was created without one."
)

UNSUPPORTED_FETCH_AS_PANDAS_AVRO = TectonValidationError(
    "Logged datasets require spark. Please use `to_spark()` to fetch."
)


def INVALID_DATASET_PATH(path: str):
    return TectonValidationError(f"Dataset storage location must be an s3 path or a local directory. path={path}")


# Feature Retrevial
def GET_HISTORICAL_FEATURES_WRONG_PARAMS(params: List[str], if_statement: str):
    return TectonValidationError("Cannot provide parameters " + ", ".join(params) + f" if {if_statement}")


GET_ONLINE_FEATURES_REQUIRED_ARGS = TectonValidationError(
    "get_online_features requires at least one of join_keys or request_data to be set."
)

GET_ONLINE_FEATURES_ODFV_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this On-Demand Feature View since it has other Feature Views as inputs"
)

GET_ONLINE_FEATURES_FS_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this Feature Service"
)

GET_FEATURE_VECTOR_FS_JOIN_KEYS = TectonValidationError(
    "get_feature_vector requires the 'join_keys' argument for this Feature Service"
)

FS_GET_ONLINE_FEATURES_REQUIRED_ARGS = TectonValidationError(
    "get_online_features requires at least one of join_keys or request_data"
)


def GET_ONLINE_FEATURES_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError("The following required keys are missing in request_data: " + ", ".join(keys))


def GET_FEATURE_VECTOR_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError("The following required keys are missing in request_context_map: " + ", ".join(keys))


def GET_ONLINE_FEATURES_FS_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for this Feature Service since it contains an On-Demand Feature View. "
        + "Expected the following request data keys: "
        + ", ".join(keys)
    )


def GET_FEATURE_VECTOR_FS_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_feature_vector requires the 'request_context_map' argument for this Feature Service since it contains an On-Demand Feature View. "
        + "Expected the following request context keys: "
        + ", ".join(keys)
    )


def GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for On-Demand Feature Views. Expected the following request context keys: "
        + ", ".join(keys)
    )


def GET_FEATURE_VECTOR_FV_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_feature_vector requires the 'request_context_map' argument for On-Demand Feature Views. Expected the following request context keys: "
        + ", ".join(keys)
    )


def ODFV_WITH_FT_INPUT_DEV_WORKSPACE(ft_name):
    return TectonValidationError(
        f"This On-Demand Feature View has a Feature Table, {ft_name}, as an input. Feature Table feature retrieval cannot be used in a dev workspace. Please apply the Feature Table to a live workspace to retrieve features."
    )


def ODFV_WITH_FT_INPUT_LOCAL_MODE(ft_name):
    return TectonValidationError(
        f"This On-Demand Feature View has a Feature Table, {ft_name}, as an input. Feature Table feature retrieval cannot be used when the Feature Table is locally defined. Please apply the Feature Table to a live workspace to retrieve features."
    )


def ODFV_WITH_FT_INPUT_FROM_SOURCE(ft_name):
    return TectonValidationError(
        f"This On-Demand Feature View has a Feature Table, {ft_name}, as an input. Feature Table features must be retrieved from the offline store, i.e. with from_source=False."
    )


def ODFV_WITH_UNMATERIALIZED_FV_INPUT_FROM_SOURCE_FALSE(fv_name):
    return TectonValidationError(
        f"This On-Demand Feature View has a Feature View, {fv_name}, as an input, which does not have materialization enabled (offline=False). Either retrieve features with from_source=True (not applicable for Feature Tables) or enable offline materialization for the input feature views."
    )


def LOCAL_ODFV_WITH_DEV_WORKSPACE_FV_INPUT_FROM_SOURCE_FALSE(fv_name):
    return TectonValidationError(
        f"This On-Demand Feature View has a Feature View, {fv_name}, as an input, which belongs to a dev workspace and therefore does not have materialization enabled. Either retrieve features with from_source=True (not applicable for Feature Tables) or apply this Feature View to a live workspace with offline=True."
    )


def LOCAL_ODFV_WITH_LOCAL_FV_INPUT_FROM_SOURCE_FALSE(fv_name):
    return TectonValidationError(
        f"This On-Demand Feature View has a Feature View, {fv_name}, as an input, that is locally defined and therefore does not have materialization enabled. Either retrieve features with from_source=True or apply this Feature View to a live workspace with offline=True."
    )


FROM_SOURCE_WITH_FT = TectonValidationError(
    "Computing features from source is not supported for Feature Tables. Try calling this method with from_source=False."
)

USE_MATERIALIZED_DATA_WITH_FT = TectonValidationError(
    "Computing features from source is not supported for Feature Tables. Try calling this method with use_materialized_data=True."
)

FS_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    "This Feature Service contains a Feature Table and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)

FV_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    "This Feature View has a Feature Table input and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)

# Backfill Config Validation
BFC_MODE_SINGLE_REQUIRED_FEATURE_END_TIME_WHEN_START_TIME_SET = TectonValidationError(
    "feature_end_time is required when feature_start_time is set, for a FeatureView with "
    + "single_batch_schedule_interval_per_job backfill mode."
)

BFC_MODE_SINGLE_INVALID_FEATURE_TIME_RANGE = TectonValidationError(
    "Run with single_batch_schedule_interval_per_job backfill mode only supports time range equal to batch_schedule"
)


def INCORRECT_KEYS(keys, join_keys):
    return TectonValidationError(
        f"Requested keys to be deleted ({keys}) do not match the expected join keys ({join_keys})."
    )


NO_STORE_SELECTED = TectonValidationError("One of online or offline store must be selected.")


def TOO_MANY_KEYS(max_keys: int):
    return TectonValidationError(f"Max number of keys to be deleted is {max_keys}.")


OFFLINE_STORE_NOT_SUPPORTED = TectonValidationError(
    "Only DeltaLake is supported for entity deletion in offline feature stores."
)

FV_UNSUPPORTED_AGGREGATION = TectonValidationError(
    "Argument 'aggregation_level' is not supported for Feature Views with `aggregations` not specified."
)

RUN_API_PARTIAL_LEVEL_UNSUPPORTED_FOR_COMPACTION = TectonValidationError(
    "aggregation_level='partial' is only supported for Aggregate Feature Views with Compaction Disabled. Use aggregation_level='full' or aggregation_level='disabled' instead."
)


def INVALID_JOIN_KEY_TYPE(t):
    return TectonValidationError(
        f"Invalid type of join keys '{t}'. Keys must be an instance of [pyspark.sql.dataframe.DataFrame, pandas.DataFrame]."
    )


def DUPLICATED_COLS_IN_KEYS(t):
    return TectonValidationError(f"Argument keys {t} have duplicated column names. ")


ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE = TectonValidationError(
    "Athena compute can only be used in live workspaces. Current workspace is not live. Please use a different compute mode or switch to a live workspace."
)

ATHENA_COMPUTE_NOT_SUPPORTED_IN_LOCAL_MODE = TectonValidationError(
    "Athena compute can only be used in on applied Tecton objects in live workspaces. Using a locally defined Tecton object is not currently supported with Athena."
)

ATHENA_COMPUTE_MOCK_SOURCES_UNSUPPORTED = TectonValidationError(
    "Athena compute can only be used with materialized data in live workspaces. Using mock data is not supported with Athena."
)

SNOWFLAKE_COMPUTE_MOCK_SOURCES_UNSUPPORTED = TectonValidationError(
    "Using mock data in `get_historical_features` is not supported with Snowflake."
)


# Notebook Development
def TECTON_OBJECT_REQUIRES_VALIDATION(function_name: str, class_name: str, fco_name: str):
    return TectonValidationError(
        f"{class_name} '{fco_name}' must be validated before `{function_name}` can be called. Call `validate()` to validate this object. If you'd like to enable automatic validation, you can use `tecton.set_validation_mode('auto')` or set the environment variable `TECTON_VALIDATION_MODE=auto`. Note that validation requires connected compute (Spark/Snowflake/etc.) and makes requests to your Tecton instance's API."
    )


def RUN_REQUIRES_VALIDATION(function_name: str, class_name: str, fco_name: str):
    return TectonValidationError(
        f"{class_name} '{fco_name}' must be validated before `{function_name}` can be called. If you'd like to skip validation (e.g. for unit testing), use `test_run()` instead. In order to run validations either call `validate()` or enable automatic validation, you can use `tecton.set_validation_mode('auto')` or set the environment variable `TECTON_VALIDATION_MODE=auto`. Note that validation requires connected compute (Spark/Snowflake/etc.) and makes requests to your Tecton instance's API."
    )


def RUN_TRANSFORMATION_REQUIRES_VALIDATION(function_name: str, class_name: str, fco_name: str):
    return TectonValidationError(
        f"{class_name} '{fco_name}' must be validated before `{function_name}` can be called. If you'd like to skip validation (e.g. for unit testing using mock inputs), please set the validation mode to 'skip' using tecton.set_validation_mode('skip'). In order to run validations either call `validate()` or enable automatic validation using `tecton.set_validation_mode('auto')` or setting the environment variable `TECTON_VALIDATION_MODE=auto`. Note that validation requires connected compute (Spark/Snowflake/etc.) and makes requests to your Tecton instance's API."
    )


def INVALID_USAGE_FOR_LOCAL_TECTON_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Tecton objects that have been applied to a Tecton workspace. This object was defined locally."
    )


def INVALID_USAGE_FOR_REMOTE_TECTON_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Tecton objects that have been defined locally. This object was retrieved from a Tecton workspace."
    )


def INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Feature Tables that have been applied to a Tecton workspace. This object was defined locally, which means this Feature Table cannot be materialized. Feature Tables require materialization in order to ingest features and perform feature retrieval."
    )


def CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on locally defined Tecton objects. This object was retrieved from a Tecton workpace. Please use `run()` instead."
    )


def INVALID_NUMBER_OF_FEATURE_VIEW_INPUTS(num_sources: int, num_inputs: int):
    return TectonValidationError(
        f"Number of Feature View Inputs ({num_inputs}) should match the number of Data Sources ({num_sources}) in the definition."
    )


def SCHEMAS_DO_NOT_MATCH(schema: schema_pb2.Schema, derived_schema: schema_pb2.Schema):
    return TectonValidationError(
        f"The provided schema does not match the derived schema.\nProvided schema: {Schema(schema)}\nDerived schema: {Schema(derived_schema)}"
    )


def INGESTAPI_USER_ERROR(status_code: int, reason: str, error_message: str):
    return TectonValidationError(f"Received {status_code} {reason} from Stream IngestAPI. Details: \n {error_message}")


def AGGREGATION_INTERVAL_SET_COMPACTION():
    return TectonValidationError("Feature views with stream compaction enabled cannot have `aggregation_interval` set.")


def COMPACTION_TIME_WINDOW_SERIES_UNSUPPORTED():
    return TectonValidationError(
        "Aggregations using a TimeWindowSeries window are not supported when `compaction_enabled=True`."
    )


# New Read API
GET_FEATURES_FOR_EVENTS_UNSUPPORTED = TectonValidationError(
    "get_features_for_events() is only supported for SPARK or RIFT Compute Modes."
)

GET_FEATURES_IN_RANGE_UNSUPPORTED = TectonValidationError(
    "get_features_in_range() is only supported for SPARK or RIFT Compute Modes."
)

GET_PARTIAL_AGGREGATES_UNSUPPORTED_NON_AGGREGATE = TectonValidationError(
    "get_partial_aggregates() is only supported for Feature Views with Tecton Managed Aggregations."
)

GET_PARTIAL_AGGREGATES_UNSUPPORTED_COMPACTED = TectonValidationError(
    "get_partial_aggregates() is only supported for Aggregate Feature Views with Compaction Disabled."
)

GET_PARTIAL_AGGREGATES_UNSUPPORTED_CONTINUOUS = TectonValidationError(
    'Tecton does not create partial aggregates for Feature Views with "Continuous" Stream Processing Mode.'
)

RUN_TRANSFORMATION_UNSUPPORTED = TectonValidationError(
    "run_transformation() for Batch and Stream Feature Views is only supported for SPARK and RIFT Compute Modes."
)


def READ_API_DEPRECATION_TEMPLATE(old_method, new_method):
    return f"{old_method}() has been deprecated in Tecton 0.9 and will be fully removed in the next major SDK release. Please use {new_method}() instead. See https://docs.tecton.ai/docs/reading-feature-data/reading-feature-data-for-training/offline-retrieval-methods for more information."


GET_HISTORICAL_FEATURES_DEPRECATED_SPINE = READ_API_DEPRECATION_TEMPLATE(
    "get_historical_features", "get_features_for_events"
)

GET_HISTORICAL_FEATURES_DEPRECATED_TIME_RANGE = READ_API_DEPRECATION_TEMPLATE(
    "get_historical_features", "get_features_in_range"
)

RUN_DEPRECATED_TRANSFORMATION = READ_API_DEPRECATION_TEMPLATE("run", "run_transformation")

RUN_DEPRECATED_PARTIAL_AGGS = READ_API_DEPRECATION_TEMPLATE("run", "get_partial_aggregates")

RUN_DEPRECATED_FULL_AGG = READ_API_DEPRECATION_TEMPLATE("run", "get_features_in_range")

GET_SPINE_DF_DEPRECATED = READ_API_DEPRECATION_TEMPLATE("get_spine_dataframe", "get_events_dataframe")


class SchemaRequired(TectonValidationError):
    def __init__(self, feature_view_name: str):
        super().__init__(f"The 'schema' parameter for {feature_view_name} must be set.")


BUILD_ARGS_INTERNAL_ERROR = TectonInternalError(
    "_build_args() is for internal use only and can only be called on local objects"
)

UNSUPPORTED_FRAMEWORK_VERSION = RuntimeError(
    "The existing feature definitions have been applied with an older SDK. Please downgrade the Tecton SDK or upgrade the feature definitions."
)
