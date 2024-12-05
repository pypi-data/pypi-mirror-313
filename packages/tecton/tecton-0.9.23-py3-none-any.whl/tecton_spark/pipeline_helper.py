import random
import re
import string
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

import numpy as np
import pandas
import pandas as pd
import pendulum
from pyspark.sql.column import Column
from pyspark.sql.types import ArrayType
from pyspark.sql.types import MapType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructType

from tecton_core import conf
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.errors import UDF_ERROR
from tecton_core.errors import UDF_TYPE_ERROR
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.id_helper import IdHelper
from tecton_core.materialization_context import BaseMaterializationContext
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_core.pipeline_common import CONSTANT_TYPE
from tecton_core.pipeline_common import CONSTANT_TYPE_OBJECTS
from tecton_core.pipeline_common import constant_node_to_value
from tecton_core.pipeline_common import get_keyword_inputs
from tecton_core.pipeline_common import positional_inputs
from tecton_core.pipeline_common import transformation_type_checker
from tecton_core.query_consts import udf_internal
from tecton_proto.args.pipeline_pb2 import Input as InputProto
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import TransformationNode
from tecton_proto.args.transformation_pb2 import TransformationMode
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_spark import feature_view_spark_utils
from tecton_spark.schema_spark_utils import schema_to_spark
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper
from tecton_spark.type_annotations import PySparkDataFrame
from tecton_spark.type_annotations import PySparkSession
from tecton_spark.type_annotations import is_pyspark_df


MAX_INT64 = (2**63) - 1

# TODO(TEC-8978): remove \. from namespace regex when FWv3 FVs are no longer supported.
_NAMESPACE_SEPARATOR_REGEX = re.compile(r"__|\.")


def feature_name(namespaced_feature_name: str) -> str:
    """Gets the base feature name from a namespaced_feature_name (e.g. feature_view__feature)

    Supports both `__` (fwv5) and `.` (fwv3) separators. Does two attempts at
    getting the feature name since `__` was allowed in feature view names in
    fwv3.
    """

    spl = _NAMESPACE_SEPARATOR_REGEX.split(namespaced_feature_name)
    if len(spl) == 2:
        return spl[1]

    return namespaced_feature_name.split(".")[1]


def build_odfv_udf_col(
    input_df: PySparkDataFrame, fdw: FeatureDefinitionWrapper, namespace: str, use_namespace_feature_prefix: bool = True
) -> Tuple[Column, List[Column]]:
    """
    Builds a Spark udf for executing a specific ODFV. This runs an ODFV,
    which outputs a single temporary object (dict/map for python mode, json for
    pandas mode). We then deserialize this to get the feature columns.

    We use this function in two phases in parallel across multiple ODFVs:
    1. Run an ODFV to get the tmp object
    2. Select columns from the tmp object

    To support running these two phases in parallel, we use this method
    to output the column for (1) and the columns for (2), and concat them
    all together.

    :return: select_column (the tmp odfv output col), output_columns (the
    columns of the tmp odfv output, which map to the output features of an
    odfv)
    """
    fv_name = fdw.name
    fv_id = fdw.id
    pipeline = fdw.pipeline
    output_schema = schema_to_spark(fdw.view_schema)
    transformations = fdw.transformations
    namespace_separator = fdw.namespace_separator
    if namespace is None:
        namespace = fv_name

    odfv_tmp_output_name = f"_{namespace}_odfv_output"

    # Pass in only the non-internal fields and udf-internal fields
    # corresponding to this particular odfv
    udf_args = []
    for input_col in input_df.schema:
        if udf_internal(ComputeMode.SPARK) not in input_col.name or fv_id in input_col.name:
            udf_args.append(input_col.name)
    udf_arg_idx_map = {}
    for arg_idx in range(len(udf_args)):
        udf_arg_idx_map[udf_args[arg_idx]] = arg_idx
    builder = _ODFVPipelineBuilder(
        name=fv_name,
        fv_id=fv_id,
        pipeline=pipeline,
        transformations=transformations,
        udf_arg_idx_map=udf_arg_idx_map,
        output_schema=output_schema,
    )

    from pyspark.sql.functions import col

    output_columns = []
    for c in output_schema:
        output_column_name = f"{namespace}{namespace_separator}{c.name}" if use_namespace_feature_prefix else c.name
        output_columns.append(col(f"{odfv_tmp_output_name}.{c.name}").alias(output_column_name))

    from pyspark.sql.functions import from_json
    from pyspark.sql.functions import pandas_udf
    from pyspark.sql.functions import udf

    if builder.mode == "python":
        # Python features are output as a single dict / map column, so we
        # map that into individual columns
        _odfv_udf = udf(builder.py_wrapper, output_schema)
        udf_col = _odfv_udf(*[f"`{c}`" for c in udf_args]).alias(odfv_tmp_output_name)
        return udf_col, output_columns
    else:
        assert builder.mode == "pandas"
        # Pandas features are output into a single struct, so we deserialize
        # here + cast into multiple columns.
        # Note: from_json will return null in the case of an unparseable
        # string.
        _odfv_udf = pandas_udf(builder.pandas_udf_wrapper, StringType())
        deserialized_udf_col = from_json(_odfv_udf(*[f"`{c}`" for c in udf_args]), output_schema)
        return deserialized_udf_col.alias(odfv_tmp_output_name), output_columns


# TODO: if the run api should support some type of mock inputs other than dicts, then we'd need to modify this
# For now, the same pipeline evaluation works for both.
def run_mock_odfv_pipeline(
    pipeline: Pipeline,
    transformations: List[specs.TransformationSpec],
    name: str,
    mock_inputs: Dict[str, Union[Dict[str, Any], pandas.DataFrame]],
) -> Union[Dict[str, Any], pd.DataFrame]:
    builder = _ODFVPipelineBuilder(
        name=name,
        pipeline=pipeline,
        transformations=transformations,
        udf_arg_idx_map={},
        output_schema=None,
        passed_in_inputs=mock_inputs,
    )
    return builder._udf_node_to_value(pipeline.root)


def pipeline_to_dataframe(
    spark: PySparkSession,
    pipeline: Pipeline,
    consume_streaming_data_sources: bool,
    data_sources: List[specs.DataSourceSpec],
    transformations: List[specs.TransformationSpec],
    schedule_interval: Optional[pendulum.Duration] = None,
    passed_in_inputs: Optional[Dict[str, PySparkDataFrame]] = None,
) -> PySparkDataFrame:
    return _PipelineBuilder(
        spark,
        pipeline,
        consume_streaming_data_sources,
        data_sources,
        transformations,
        schedule_interval=schedule_interval,
        passed_in_inputs=passed_in_inputs,
    ).get_dataframe()


def get_all_input_keys(node: PipelineNode) -> Set[str]:
    names_set = set()
    _get_all_input_keys_helper(node, names_set)
    return names_set


def _get_all_input_keys_helper(node: PipelineNode, names_set: Set[str]) -> Set[str]:
    if node.HasField("request_data_source_node"):
        names_set.add(node.request_data_source_node.input_name)
    elif node.HasField("data_source_node"):
        names_set.add(node.data_source_node.input_name)
    elif node.HasField("feature_view_node"):
        names_set.add(node.feature_view_node.input_name)
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _get_all_input_keys_helper(child.node, names_set)
    return names_set


def get_fco_ids_to_input_keys(node: PipelineNode) -> Dict[str, str]:
    names_dict = {}
    _get_fco_ids_to_input_keys_helper(node, names_dict)
    return names_dict


def _get_fco_ids_to_input_keys_helper(node: PipelineNode, names_dict: Dict[str, str]) -> Dict[str, str]:
    if node.HasField("request_data_source_node"):
        # request data sources don't have fco ids
        pass
    elif node.HasField("data_source_node"):
        ds_node = node.data_source_node
        names_dict[IdHelper.to_string(ds_node.virtual_data_source_id)] = ds_node.input_name
    elif node.HasField("feature_view_node"):
        fv_node = node.feature_view_node
        names_dict[IdHelper.to_string(fv_node.feature_view_id)] = fv_node.input_name
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _get_fco_ids_to_input_keys_helper(child.node, names_dict)
    return names_dict


# Constructs empty data frames matching schema of DS inputs for the purpose of
# schema-validating the transformation pipeline.
def populate_empty_passed_in_inputs(
    node: PipelineNode,
    ds_map: Dict[str, specs.DataSourceSpec],
    spark: PySparkSession,
) -> Dict[str, PySparkDataFrame]:
    empty_passed_in_inputs = {}
    _populate_empty_passed_in_inputs_helper(node, empty_passed_in_inputs, ds_map, spark)
    return empty_passed_in_inputs


def _populate_empty_passed_in_inputs_helper(
    node: PipelineNode,
    empty_passed_in_inputs: Dict[str, PySparkDataFrame],
    ds_map: Dict[str, specs.DataSourceSpec],
    spark: PySparkSession,
) -> None:
    if node.HasField("data_source_node"):
        ds_id = IdHelper.to_string(node.data_source_node.virtual_data_source_id)
        ds_spec = ds_map[ds_id]
        assert (
            ds_spec.type != DataSourceType.PUSH_NO_BATCH
        ), "This utility does not support FeatureView with PushSources that do not have a batch_config"
        ds_schema = ds_spec.batch_source.spark_schema
        empty_passed_in_inputs[node.data_source_node.input_name] = spark.createDataFrame(
            [], SparkSchemaWrapper.from_proto(ds_schema).unwrap()
        )
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _populate_empty_passed_in_inputs_helper(child.node, empty_passed_in_inputs, ds_map, spark)


# This class is for Spark pipelines
class _PipelineBuilder:
    # The value of internal nodes in the tree
    _VALUE_TYPE = Union[PySparkDataFrame, CONSTANT_TYPE, BaseMaterializationContext]

    def __init__(
        self,
        spark: PySparkSession,
        pipeline: Pipeline,
        consume_streaming_data_sources: bool,
        data_sources: List[specs.DataSourceSpec],
        # we only use mode and name from these
        transformations: List[specs.TransformationSpec],
        # Feature time limits are only used to control the materialization context. No filtering is performed.
        feature_time_limits: Optional[pendulum.Period] = None,
        schedule_interval: Optional[pendulum.Duration] = None,
        # If None, we will compute inputs from raw data sources and apply time filtering.
        # Otherwise we will prefer these inputs instead
        passed_in_inputs: Optional[Dict[str, PySparkDataFrame]] = None,
        # output_schema is only used by python/pandas transformations during backfills.
        # Specifically, it applies for Stream feature views with push sources and batch config, during
        # the batch materialization jobs.
        output_schema: Optional[StructType] = None,
    ) -> None:
        self._spark = spark
        self._pipeline = pipeline
        self._output_schema = output_schema
        self._consume_streaming_data_sources = consume_streaming_data_sources
        self._feature_time_limits = feature_time_limits
        self._id_to_ds = {ds.id: ds for ds in data_sources}
        self._id_to_transformation = {t.id: t for t in transformations}

        self._registered_temp_view_names: List[str] = []
        self._schedule_interval = schedule_interval

        self._passed_in_inputs = passed_in_inputs

    def get_dataframe(self) -> PySparkDataFrame:
        df = self._node_to_value(self._pipeline.root)
        # Cleanup any temporary tables created during the process
        for temp_name in self._registered_temp_view_names:
            # DROP VIEW/DROP TABLE sql syntax is invalidated when spark_catalog is set to DeltaCatalog on EMR clusters
            if (
                self._spark.conf.get("spark.sql.catalog.spark_catalog", "")
                == "org.apache.spark.sql.delta.catalog.DeltaCatalog"
            ):
                self._spark.catalog.dropTempView(temp_name)
            else:
                self._spark.sql(f"DROP VIEW IF EXISTS {temp_name}")
        assert is_pyspark_df(df)
        return df

    def _node_to_value(self, pipeline_node: PipelineNode) -> _VALUE_TYPE:
        if pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_dataframe(pipeline_node.transformation_node)
        elif pipeline_node.HasField("data_source_node"):
            data_source_node = pipeline_node.data_source_node
            if data_source_node.input_name not in self._passed_in_inputs:
                msg = f"Expected inputs {self._passed_in_inputs} to contain {data_source_node.input_name}"
                raise ValueError(msg)
            return self._passed_in_inputs[data_source_node.input_name]
        elif pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("materialization_context_node"):
            if self._feature_time_limits is not None:
                feature_start_time = self._feature_time_limits.start
                feature_end_time = self._feature_time_limits.end
                batch_schedule = self._schedule_interval
            else:
                feature_start_time = pendulum.from_timestamp(0, pendulum.tz.UTC)
                feature_end_time = pendulum.datetime(2100, 1, 1)
                batch_schedule = self._schedule_interval or pendulum.duration()
            return BoundMaterializationContext._create_internal(feature_start_time, feature_end_time, batch_schedule)
        elif pipeline_node.HasField("request_data_source_node"):
            msg = "RequestDataSource is not supported in Spark pipelines"
            raise ValueError(msg)
        elif pipeline_node.HasField("feature_view_node"):
            msg = "Dependent FeatureViews are not supported in Spark pipelines"
            raise ValueError(msg)
        else:
            msg = f"Unknown PipelineNode type: {pipeline_node}"
            raise KeyError(msg)

    def _transformation_node_to_dataframe(self, transformation_node: TransformationNode) -> PySparkDataFrame:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[PySparkDataFrame, str, int, float, bool]] = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        return self._apply_transformation_function(transformation_node, args, kwargs)

    def _apply_transformation_function(
        self, transformation_node: TransformationNode, args: List[Any], kwargs: Dict[str, Any]
    ) -> Union[Dict[str, Any], pd.DataFrame, PySparkDataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation.

        If needed, resulted function is wrapped with a function that translates mode-specific input/output types to DataFrames.
        """
        transformation = self._id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function

        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYSPARK:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e)
            transformation_type_checker(transformation.name, res, "pyspark", self._possible_modes())
            return res
        elif transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_SPARK_SQL:
            # type checking happens inside this function
            return self._wrap_sql_function(transformation_node, user_function)(*args, **kwargs)
        elif transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            # TODO(achal): This code block should be cleaned up by breaking out some udf wrapping logic in a separate
            # top level function.
            try:
                if isinstance(self, _ODFVPipelineBuilder):
                    res = user_function(*args, **kwargs)
                else:
                    import pyspark.pandas as ps

                    # Assumes that we only have one argument that is a pyspark Dataframe built from the batch source
                    # because this code path is for ingest api which should only read from one batch source.
                    assert len(args) + len(kwargs) == 1, "Pandas transformations only support a single input"
                    df = args[0] if len(args) == 1 else next(iter(kwargs.values()))

                    psdf = ps.DataFrame(df)
                    psdf = psdf.pandas_on_spark.apply_batch(user_function)

                    res = psdf.to_spark()

                return res
            except Exception as e:
                raise UDF_ERROR(e)
        elif transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            # TODO(achal): This code block should be cleaned up by breaking out some udf wrapping logic in a separate
            # top level function.
            try:
                if isinstance(self, _ODFVPipelineBuilder):
                    res = user_function(*args, **kwargs)
                else:
                    from pyspark.sql.functions import struct
                    from pyspark.sql.functions import udf

                    # Assumes that we only have one argument that is a pyspark Dataframe built from the batch source
                    # because this code path is for ingest api which should only read from one batch source.
                    assert len(args) + len(kwargs) == 1, "Pandas transformations only support a single input"
                    df = args[0] if len(args) == 1 else next(iter(kwargs.values()))

                    @udf(self._output_schema)
                    def transform_rows(df_group):
                        # Apply your desired transformation on the input group of Rows(this applies row by row)
                        transformed_df_group = user_function(df_group.asDict())

                        # Return the transformed group of rows as a Pandas DataFrame
                        return transformed_df_group

                    df = df.select(struct("*").alias("data"))
                    df = df.select(transform_rows("data").alias("result"))
                    res = df.select(*[f"result.{field.name}" for field in self._output_schema])
                return res
            except TypeError as e:
                raise UDF_TYPE_ERROR(e)
            except Exception as e:
                raise UDF_ERROR(e)
        else:
            msg = f"unknown transformation mode({transformation.transformation_mode})"
            raise KeyError(msg)

    def _wrap_sql_function(
        self, transformation_node: TransformationNode, user_function: Callable[..., str]
    ) -> Callable[..., PySparkDataFrame]:
        def wrapped(*args, **kwargs):
            wrapped_args = []
            for arg, node_input in zip(args, positional_inputs(transformation_node)):
                wrapped_args.append(self._wrap_node_inputvalue(node_input, arg))
            keyword_inputs = get_keyword_inputs(transformation_node)
            wrapped_kwargs = {}
            for k, v in kwargs.items():
                node_input = keyword_inputs[k]
                wrapped_kwargs[k] = self._wrap_node_inputvalue(node_input, v)
            sql_string = user_function(*wrapped_args, **wrapped_kwargs)
            transformation_name = self._id_to_transformation[
                IdHelper.to_string(transformation_node.transformation_id)
            ].name
            transformation_type_checker(transformation_name, sql_string, "spark_sql", self._possible_modes())
            return self._spark.sql(sql_string)

        return wrapped

    def _wrap_node_inputvalue(
        self, node_input: InputProto, value: _VALUE_TYPE
    ) -> Optional[Union[InputProto, str, int, float, bool]]:
        if node_input.node.HasField("constant_node"):
            assert value is None or isinstance(value, CONSTANT_TYPE_OBJECTS)
            return value
        elif node_input.node.HasField("materialization_context_node"):
            assert isinstance(value, BoundMaterializationContext)
            return value
        else:
            assert is_pyspark_df(value)
            return self._register_temp_table(self._node_name(node_input.node), value)

    def _node_name(self, node: PipelineNode) -> str:
        """Returns a human-readable name for the node."""
        if node.HasField("transformation_node"):
            name = self._id_to_transformation[IdHelper.to_string(node.transformation_node.transformation_id)].name
            return f"transformation_{name}_output"
        elif node.HasField("data_source_node"):
            if node.data_source_node.HasField("input_name"):
                return node.data_source_node.input_name
            # TODO(TEC-5076): remove this legacy code, since input_name will always be set
            name = self._id_to_ds[IdHelper.to_string(node.data_source_node.virtual_data_source_id)].fco_metadata.name
            return f"data_source_{name}_output"
        else:
            msg = f"Expected transformation or data source node: {node}"
            raise Exception(msg)

    def _register_temp_table(self, name: str, df: PySparkDataFrame) -> str:
        """Registers a Dataframe as a temp table and returns its name."""
        unique_name = name + self._random_suffix()
        self._registered_temp_view_names.append(unique_name)
        df.createOrReplaceTempView(unique_name)
        return unique_name

    def _random_suffix(self) -> str:
        return "".join(random.choice(string.ascii_letters) for i in range(6))

    def _possible_modes(self):
        # note that pipeline is included since this is meant to be a user hint, and it's
        # theoretically possible a pipeline wound up deeper than expected
        return ["pyspark", "spark_sql", "pipeline", "python", "pandas"]


# For Pandas-mode:
# We need to take the call a udf constructed from the pipeline that will generate the on-demand features.
# A pandas udf takes as inputs (pd.Series...) and outputs pd.Series.
# However, the user-defined transforms take as input pd.DataFrame and output pd.DataFrame.
# We use _ODFVPipelineBuilder to construct a udf wrapper function that translates the inputs and outputs and
# performs some type checking.
# The general idea is that each Node of the pipeline evaluates to a pandas.DataFrame.
# This is what we want since the user-defined transforms take pandas.DataFrame as inputs both from RequestDataSourceNode or FeatureViewNode.
# pandas_udf_wrapper then typechecks and translates the final pandas.DataFrame into a jsonized pandas.Series to match what spark expects.
#
# For Python-mode, we can use a simpler wrapper function for the udf because we don't do any spark<->pandas type conversions.
class _ODFVPipelineBuilder(_PipelineBuilder):
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
        # maps input + feature name to arg index that udf function wrapper will be called with.
        # this is needed because we need to know which pd.Series that are inputs to this function correspond to the desired request context fields or dependent fv features that the customer-defined udf uses.
        udf_arg_idx_map: Dict[str, int],
        output_schema: StructType,
        # the id of this OnDemandFeatureView; only required to be set when reading from source data
        fv_id: Optional[str] = None,
        passed_in_inputs: Optional[Dict[str, Union[Dict[str, Any], pandas.DataFrame]]] = None,
    ) -> None:
        self._pipeline = pipeline
        self._name = name
        self._fv_id = fv_id
        self.udf_arg_idx_map = udf_arg_idx_map
        self._id_to_transformation = {t.id: t for t in transformations}
        self._output_schema = output_schema
        self._passed_in_inputs = passed_in_inputs
        # In Spark, the UDF cannot reference a proto enum, so instead save mode as a string
        self.mode = (
            "python"
            if self._id_to_transformation[
                IdHelper.to_string(self._pipeline.root.transformation_node.transformation_id)
            ].transformation_mode
            == TransformationMode.TRANSFORMATION_MODE_PYTHON
            else "pandas"
        )
        # Access this conf value outside of the UDF to avoid doing it many times and avoiding any worker/driver state issues.
        self._should_check_output_schema = conf.get_bool("TECTON_PYTHON_ODFV_OUTPUT_SCHEMA_CHECK_ENABLED")

    # FOR PYTHON
    def py_wrapper(self, *args):
        assert self.mode == "python"
        self._udf_args: List = args
        res = self._udf_node_to_value(self._pipeline.root)
        if self._should_check_output_schema:
            feature_view_spark_utils.check_python_odfv_output_schema(res, self._output_schema, self._name)
        return res

    # FOR PANDAS
    def pandas_udf_wrapper(self, *args):
        import json

        import pandas as pd

        assert self.mode == "pandas"

        # self.udf_arg_idx_map tells us which of these pd.Series correspond to a given RequestDataSource or FeatureView input
        self._udf_args: List[pd.Series] = args

        output_df = self._udf_node_to_value(self._pipeline.root)

        assert isinstance(
            output_df, pd.DataFrame
        ), f"Transformer returns {str(output_df)}, but must return a pandas.DataFrame instead."

        for field in self._output_schema:
            assert field.name in output_df.columns, (
                f"Expected output schema field '{field.name}' not found in columns of DataFrame returned by "
                f"'{self._name}': [" + ", ".join(output_df.columns) + "]"
            )
            # Convert np.arrays to python lists which are JSON serializable by the default serializer.
            if isinstance(field.dataType, (ArrayType, MapType, StructType)):
                output_df[field.name] = output_df[field.name].apply(_convert_ndarray_to_list)

        output_strs = []

        # itertuples() is used instead of iterrows() to preserve type safety.
        # See notes in https://pandas.pydata.org/pandas-docs/version/0.17.1/generated/pandas.DataFrame.iterrows.html.
        for row in output_df.itertuples(index=False):
            output_strs.append(json.dumps(row._asdict()))
        return pd.Series(output_strs)

    def _transformation_node_to_online_dataframe(
        self, transformation_node: TransformationNode
    ) -> Union[Dict[str, Any], pd.DataFrame]:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[PySparkDataFrame, str, int, float, bool]] = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._udf_node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        return self._apply_transformation_function(transformation_node, args, kwargs)

    # evaluate a node in the Pipeline
    def _udf_node_to_value(
        self, pipeline_node: PipelineNode
    ) -> Union[str, int, float, bool, None, Dict[str, Any], pd.DataFrame, PySparkDataFrame, pd.Series]:
        if pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("feature_view_node"):
            if self._passed_in_inputs is not None:
                return self._passed_in_inputs[pipeline_node.feature_view_node.input_name]
            elif self.mode == "python":
                fields_dict = {}
                # The input name of this FeatureViewNode tells us which of the udf_args correspond to the Dict we should generate that the parent TransformationNode expects as an input.
                # It also expects the DataFrame to have its columns named by the feature names.
                for feature in self.udf_arg_idx_map:
                    if not feature.startswith(
                        f"{udf_internal(ComputeMode.SPARK)}_{pipeline_node.feature_view_node.input_name}_{self._fv_id}"
                    ):
                        continue
                    idx = self.udf_arg_idx_map[feature]
                    fields_dict[feature_name(feature)] = self._udf_args[idx]
                return fields_dict
            elif self.mode == "pandas":
                all_series = []
                features = []
                # The input name of this FeatureViewNode tells us which of the udf_args correspond to the pandas.DataFrame we should generate that the parent TransformationNode expects as an input.
                # It also expects the DataFrame to have its columns named by the feature names.
                for feature in self.udf_arg_idx_map:
                    if not feature.startswith(
                        f"{udf_internal(ComputeMode.SPARK)}_{pipeline_node.feature_view_node.input_name}_{self._fv_id}"
                    ):
                        continue
                    idx = self.udf_arg_idx_map[feature]
                    all_series.append(self._udf_args[idx])
                    features.append(feature_name(feature))
                df = pd.concat(all_series, keys=features, axis=1)
                return df
            else:
                msg = "Transform mode {self.mode} is not yet implemented"
                raise NotImplementedError(msg)
        elif pipeline_node.HasField("request_data_source_node"):
            if self._passed_in_inputs is not None:
                return self._passed_in_inputs[pipeline_node.request_data_source_node.input_name]
            elif self.mode == "python":
                request_context = pipeline_node.request_data_source_node.request_context
                field_names = [c.name for c in request_context.tecton_schema.columns]
                fields_dict = {}
                for input_col in field_names:
                    idx = self.udf_arg_idx_map[input_col]
                    fields_dict[input_col] = self._udf_args[idx]
                return fields_dict
            elif self.mode == "pandas":
                all_series = []
                request_context = pipeline_node.request_data_source_node.request_context
                field_names = [c.name for c in request_context.tecton_schema.columns]
                for input_col in field_names:
                    idx = self.udf_arg_idx_map[input_col]
                    all_series.append(self._udf_args[idx])
                df = pd.concat(all_series, keys=field_names, axis=1)
                return df
            else:
                msg = "Transform mode {self.mode} is not yet implemented"
                raise NotImplementedError(msg)
        elif pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_online_dataframe(pipeline_node.transformation_node)
        elif pipeline_node.HasField("materialization_context_node"):
            msg = "MaterializationContext is unsupported for pandas pipelines"
            raise ValueError(msg)
        else:
            msg = "This is not yet implemented"
            raise NotImplementedError(msg)

    def _possible_modes(self):
        # note that pipeline is included since this is meant to be a user hint, and it's
        # theoretically possible a pipeline wound up deeper than expected
        return ["pandas", "pipeline", "python"]


def _convert_ndarray_to_list(item):
    if isinstance(item, np.ndarray):
        return item.tolist()
    elif isinstance(item, dict):
        return {key: _convert_ndarray_to_list(value) for key, value in item.items()}
    elif isinstance(item, list):
        return [_convert_ndarray_to_list(value) for value in item]
    else:
        return item
