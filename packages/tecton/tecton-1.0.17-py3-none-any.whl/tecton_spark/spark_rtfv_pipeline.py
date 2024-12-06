import re
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import numpy
import pandas
from pyspark.sql import types as PysparkTypes

from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.pipeline.rtfv_pipeline import RealtimeFeaturePipeline
from tecton_core.query_consts import udf_internal
from tecton_core.realtime_context import RealtimeContext
from tecton_core.spark_type_annotations import PySparkDataFrame
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_spark.feature_view_spark_utils import check_python_odfv_output_schema


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


def _convert_object_to_serializable_format(item):
    if isinstance(item, numpy.ndarray):
        return [_convert_object_to_serializable_format(value) for value in item.tolist()]
    elif isinstance(item, dict):
        return {key: _convert_object_to_serializable_format(value) for key, value in item.items()}
    elif isinstance(item, list):
        return [_convert_object_to_serializable_format(value) for value in item]
    elif isinstance(item, PysparkTypes.TimestampType):
        return item.fromInternal()
    elif isinstance(item, pandas.Timestamp):
        return item.isoformat()
    elif isinstance(item, pandas.DatetimeIndex):
        return item.isoformat()
    elif isinstance(item, datetime):
        return item.isoformat()
    else:
        return item


class SparkRealtimeFeaturePipeline(RealtimeFeaturePipeline):
    """
    For Pandas-mode:
    A pandas udf takes as inputs List[pandas.Series] and outputs List[pandas.Series]
    However, the user-defined transforms take as input pandas.DataFrame and output
    pandas.DataFrame. RealtimeFeaturePipeline will construct a UDF Wrapper functions
    that translates the inputs and outputs and performs some type checking.

    The general idea is that each Node of the pipeline evaluates to a pandas.DataFrame.
    This is what we want since the user-defined transforms take pandas.DataFrame
    as inputs both from RequestDataSourceNode or FeatureViewNode.
    pandas_udf_wrapper then typechecks and translates the final pandas.DataFrame into a
    jsonized pandas.Series to match what spark expects.

    For Python-mode, we can use a simpler wrapper function for the udf because we don't do
    any spark<->pandas type conversions.
    """

    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
        # maps input + feature name to arg index that udf function wrapper will be called with.
        # this is needed because we need to know which pandas.Series that are inputs to this
        # function correspond to the desired request context fields or dependent fv features
        # that the customer-defined udf uses.
        udf_arg_idx_map: Dict[str, int],
        output_schema: Optional[PysparkTypes.StructType],
        is_prompt: bool,
        events_df_timestamp_field: Optional[str] = None,
        # the id of this OnDemandFeatureView; only required to be set when reading from source data
        fv_id: Optional[str] = None,
        pipeline_inputs: Optional[Dict[str, Union[Dict[str, Any], pandas.DataFrame, RealtimeContext]]] = None,
    ) -> None:
        self.udf_arg_idx_map = udf_arg_idx_map
        self._output_schema = output_schema
        self._fv_id = fv_id
        self._udf_args = []
        super().__init__(
            name=name,
            pipeline=pipeline,
            transformations=transformations,
            is_prompt=is_prompt,
            events_df_timestamp_field=events_df_timestamp_field,
            pipeline_inputs=pipeline_inputs,
        )

    def _feature_view_node_to_value(
        self, pipeline_node: PipelineNode
    ) -> Union[Dict[str, Any], pandas.DataFrame, PySparkDataFrame]:
        if self._pipeline_inputs is not None:
            return self._pipeline_inputs[pipeline_node.feature_view_node.input_name]
        elif self.is_python_mode:
            fields_dict = {}
            # The input name of this FeatureViewNode tells us which of the udf_args
            # correspond to the Dict we should generate that the parent TransformationNode
            # expects as an input. It also expects the DataFrame to have its columns named
            # by the feature names.
            for feature in self.udf_arg_idx_map:
                if not feature.startswith(
                    f"{udf_internal(ComputeMode.SPARK)}_{pipeline_node.feature_view_node.input_name}_{self._fv_id}"
                ):
                    continue
                idx = self.udf_arg_idx_map[feature]
                value = self._udf_args[idx]
                if isinstance(value, datetime):
                    value = value.replace(tzinfo=timezone.utc)
                fields_dict[feature_name(feature)] = value
            return fields_dict
        elif self.is_pandas_mode:
            all_series = []
            features = []
            # The input name of this FeatureViewNode tells us which of the udf_args
            # correspond to the pandas.DataFrame we should generate that the parent TransformationNode
            # expects as an input. It also expects the DataFrame to have its columns named
            # by the feature names.
            for feature in self.udf_arg_idx_map:
                if not feature.startswith(
                    f"{udf_internal(ComputeMode.SPARK)}_{pipeline_node.feature_view_node.input_name}_{self._fv_id}"
                ):
                    continue
                idx = self.udf_arg_idx_map[feature]
                all_series.append(self._udf_args[idx])
                features.append(feature_name(feature))
            df = pandas.concat(all_series, keys=features, axis=1)
            return self._format_values_for_pandas_mode(df)
        else:
            msg = "Transform mode {self.mode} is not yet implemented"
            raise NotImplementedError(msg)

    def _request_data_node_to_value(
        self, pipeline_node: PipelineNode
    ) -> Union[Dict[str, Any], pandas.DataFrame, PySparkDataFrame]:
        if self._pipeline_inputs is not None:
            return self._pipeline_inputs[pipeline_node.request_data_source_node.input_name]
        elif self.is_python_mode:
            request_context = pipeline_node.request_data_source_node.request_context
            field_names = [c.name for c in request_context.tecton_schema.columns]
            fields_dict = {}
            for input_col in field_names:
                idx = self.udf_arg_idx_map[input_col]
                value = self._udf_args[idx]
                if isinstance(value, datetime):
                    value = value.replace(tzinfo=timezone.utc)
                fields_dict[input_col] = value
            return fields_dict
        elif self.is_pandas_mode:
            all_series = []
            request_context = pipeline_node.request_data_source_node.request_context
            field_names = [c.name for c in request_context.tecton_schema.columns]
            for input_col in field_names:
                idx = self.udf_arg_idx_map[input_col]
                all_series.append(self._udf_args[idx])
            df = pandas.concat(all_series, keys=field_names, axis=1)
            return self._format_values_for_pandas_mode(df)
        else:
            msg = "Transform mode {self.mode} is not yet implemented"
            raise NotImplementedError(msg)

    def _context_node_to_value(self, pipeline_node: PipelineNode) -> RealtimeContext:
        # Used for `run_transformation` with a mock Context
        if self._pipeline_inputs is not None:
            return self._pipeline_inputs[pipeline_node.context_node.input_name]

        if self._events_df_timestamp_field not in self.udf_arg_idx_map:
            msg = f"Could not extract field '{self._events_df_timestamp_field}' from events data frame."
            raise Exception(msg)

        timestamp_index = self.udf_arg_idx_map[self._events_df_timestamp_field]
        request_timestamp = self._udf_args[timestamp_index]

        if self.is_python_mode:
            request_timestamp = request_timestamp.replace(tzinfo=timezone.utc)
            return RealtimeContext(request_timestamp=request_timestamp, _is_python_mode=True)
        elif self.is_pandas_mode:
            df = pandas.to_datetime(request_timestamp, utc=True).to_frame(name="request_timestamp")
            return RealtimeContext(row_level_data=df, _is_python_mode=False)

        else:
            msg = f"{self._fco_name}s must use 'python' or 'pandas' mode."
            raise Exception(msg)

    def py_udf_wrapper(self, *args):
        assert self.is_python_mode
        self._udf_args: List = args
        res = self._node_to_value(self._pipeline.root)
        if self._should_check_output_schema:
            check_python_odfv_output_schema(res, self._output_schema, self._name)
        return res

    def pandas_udf_wrapper(self, *args):
        assert self.is_pandas_mode

        import json

        import pandas

        # self.udf_arg_idx_map tells us which of these pandas.Series correspond to a given
        # RequestDataSource or FeatureView input
        self._udf_args: List[pandas.Series] = args

        output_df = self._node_to_value(self._pipeline.root)
        assert isinstance(
            output_df, pandas.DataFrame
        ), f"Transformer returns {str(output_df)}, but must return a pandas.DataFrame instead."

        for field in self._output_schema:
            assert field.name in output_df.columns, (
                f"Expected output schema field '{field.name}' not found in columns of DataFrame returned by "
                f"'{self._name}': [" + ", ".join(output_df.columns) + "]"
            )
            if isinstance(
                field.dataType,
                (
                    PysparkTypes.ArrayType,
                    PysparkTypes.MapType,
                    PysparkTypes.StructType,
                    PysparkTypes.TimestampType,
                    pandas.Timestamp,
                    pandas.DatetimeIndex,
                ),
            ):
                output_df[field.name] = output_df[field.name].apply(_convert_object_to_serializable_format)

        output_strs = []

        # itertuples() is used instead of iterrows() to preserve type safety.
        # See notes in https://pandas.pydata.org/pandas-docs/version/0.17.1/generated/pandas.DataFrame.iterrows.html.
        for row in output_df.itertuples(index=False):
            output_strs.append(json.dumps(row._asdict()))
        return pandas.Series(output_strs)
