import math
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas
import pyarrow

from tecton_core import feature_set_config
from tecton_core import specs
from tecton_core.errors import TectonValidationError
from tecton_core.fco_container import FcoContainer
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.pipeline.feature_pipeline import NodeValueType
from tecton_core.pipeline.rtfv_pipeline import RealtimeFeaturePipeline
from tecton_core.realtime_context import REQUEST_TIMESTAMP_FIELD_NAME
from tecton_core.realtime_context import RealtimeContext
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError
from tecton_core.schema_validation import cast
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.common.schema__client_pb2 import Schema as SchemaProto


class PandasRealtimeFeaturePipeline(RealtimeFeaturePipeline):
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
        fco_container: FcoContainer,
        id: str,
        # Input dataframe containing the necessary inputs to the Realtime Feature Pipeline
        data_df: Union[pandas.DataFrame, pyarrow.RecordBatch],
        # Only used by Tecton on Snowflake to uppercase all column names. Should be deprecated
        # with it.
        column_name_updater: Callable,
        is_prompt: bool,
        events_df_timestamp_field: Optional[str] = None,
        pipeline_inputs: Optional[Dict[str, Union[Dict[str, Any], pandas.DataFrame, RealtimeContext]]] = None,
    ) -> None:
        self._data_df = data_df
        self._fco_container = fco_container
        self._fv_id = id
        self._column_name_updater = column_name_updater
        self._context_param_name = None
        self._num_rows = (
            self._data_df.num_rows if isinstance(self._data_df, pyarrow.RecordBatch) else len(self._data_df)
        )

        # For Python Mode we go through each row of inputs in _data_df and run the pipeline for
        # each of them.
        self._current_row_index = 0
        # Cache so we don't run the Spine -> Pandas Input DF logic for every row
        self._input_name_to_df = {}

        super().__init__(
            name=name,
            pipeline=pipeline,
            transformations=transformations,
            is_prompt=is_prompt,
            events_df_timestamp_field=events_df_timestamp_field,
            pipeline_inputs=pipeline_inputs,
        )

    @classmethod
    def from_feature_definition(
        cls,
        fdw: FeatureDefinitionWrapper,
        data_df: Union[pandas.DataFrame, pyarrow.RecordBatch],
        column_name_updater: Callable,
        events_df_timestamp_field: Optional[str] = None,
    ) -> "PandasRealtimeFeaturePipeline":
        return cls(
            fdw.name,
            fdw.pipeline,
            fdw.transformations,
            fdw.fco_container,
            fdw.id,
            data_df,
            column_name_updater,
            fdw.is_prompt,
            events_df_timestamp_field,
        )

    def get_dataframe(self):
        if self.is_pandas_mode:
            return self._node_to_value(self._pipeline.root)
        # For Python Mode, we go through each row of inputs in the Pandas DF
        # self._data_df and run the Pipeline for each of them
        elif self.is_python_mode:
            rtfv_result_list = []
            for row_index in range(self._num_rows):
                self._current_row_index = row_index
                rtfv_result_dict = self._node_to_value(self._pipeline.root)
                rtfv_result_list.append(rtfv_result_dict)
            return pandas.DataFrame.from_dict(rtfv_result_list)
        else:
            msg = "Realtime Feature Views only support Pandas or Python Mode."
            raise Exception(msg)

    def _node_to_value(self, pipeline_node: PipelineNode) -> NodeValueType:
        value = super()._node_to_value(pipeline_node)

        # For Python Mode, only get the current row of inputs
        if self.is_python_mode and isinstance(value, pandas.DataFrame):
            input_dict = value.iloc[self._current_row_index].to_dict()
            return self._format_values_for_python_mode(input_dict)
        elif self.is_pandas_mode and isinstance(value, pandas.DataFrame):
            return self._format_values_for_pandas_mode(value)

        return value

    @staticmethod
    def _format_values_for_python_mode(input_dict: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in input_dict.items():
            if isinstance(value, datetime):
                input_dict[key] = value.replace(tzinfo=timezone.utc)
            if value is pandas.NaT:
                input_dict[key] = None
            if isinstance(value, float) and math.isnan(value):
                input_dict[key] = None
        return input_dict

    def _request_data_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        input_name = pipeline_node.request_data_source_node.input_name

        # Use cache for Python Mode
        if input_name in self._input_name_to_df:
            return self._input_name_to_df[input_name]

        request_context_schema = pipeline_node.request_data_source_node.request_context.tecton_schema

        if isinstance(self._data_df, pandas.DataFrame):
            # TODO(Oleksii): remove this path once Snowflake & Athena are deprecated
            input_df = self._get_request_context_pandas_df(request_context_schema, input_name)
        elif isinstance(self._data_df, pyarrow.RecordBatch):
            try:
                input_df = cast(self._data_df, Schema(request_context_schema)).to_pandas()
            except CastError as exc:
                msg = f"{self._fco_name} {self._name} has a dependency on the Request Data Source named '{input_name}', but it didn't pass schema validation: "
                raise CastError(msg + str(exc)) from None
        else:
            msg = f"Unexpected input dataframe type: {type(self._data_df)}"
            raise RuntimeError(msg)

        self._input_name_to_df[input_name] = input_df
        return input_df

    def _feature_view_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        input_name = pipeline_node.feature_view_node.input_name

        # Use cache for Python Mode
        if input_name in self._input_name_to_df:
            return self._input_name_to_df[input_name]

        fv_features = feature_set_config.find_dependent_feature_set_items(
            self._fco_container, pipeline_node, {}, self._fv_id
        )[0]
        # Generate dependent column mappings since dependent FV have
        # internal column names with _udf_internal
        select_columns_and_rename_map = {}
        for f in fv_features.features:
            column_name = self._column_name_updater(f"{fv_features.namespace}__{f}")
            mapped_name = self._column_name_updater(f)
            select_columns_and_rename_map[column_name] = mapped_name
        if isinstance(self._data_df, pandas.DataFrame):
            # TODO(Oleksii): remove this path once Snowflake & Athena are deprecated
            feature_view_input_df = self._rename_pandas_columns(select_columns_and_rename_map, input_name)
        elif isinstance(self._data_df, pyarrow.RecordBatch):
            columns = []
            for f in select_columns_and_rename_map:
                try:
                    columns.append(self._data_df.column(f))
                except KeyError:
                    msg = f"{self._fco_name} {self._name} has a dependency on the Feature View '{input_name}'. Feature {f} of this Feature View is not found in the retrieved historical data. Available columns: {list(self._data_df.column_names)}"
                    raise TectonValidationError(msg)

            feature_view_input_df = pyarrow.RecordBatch.from_arrays(
                columns, names=list(select_columns_and_rename_map.values())
            ).to_pandas()
        else:
            msg = f"Unexpected input dataframe type: {type(self._data_df)}"
            raise RuntimeError(msg)

        self._input_name_to_df[input_name] = feature_view_input_df
        return feature_view_input_df

    def _context_node_to_value(self, pipeline_node: PipelineNode) -> Optional[RealtimeContext]:
        if not isinstance(self._data_df, pyarrow.RecordBatch):
            msg = "Realtime Context is only supported on Rift and Spark Feature Views."
            raise Exception(msg)

        data_df = self._data_df.to_pandas()
        input_name = pipeline_node.context_node.input_name

        # Use cache for Python Mode
        if input_name in self._input_name_to_df:
            context_df = self._input_name_to_df[input_name]
            context_dict = context_df.iloc[self._current_row_index].to_dict()
            return RealtimeContext(request_timestamp=context_dict[REQUEST_TIMESTAMP_FIELD_NAME], _is_python_mode=True)

        if self._events_df_timestamp_field is None or self._events_df_timestamp_field not in data_df:
            timestamp_field = self._events_df_timestamp_field if self._events_df_timestamp_field is not None else ""
            msg = f"Unable to extract timestamp field '{timestamp_field}' from events dataframe."
            raise Exception(msg)

        context_df = data_df[[self._events_df_timestamp_field]].rename(
            columns={self._events_df_timestamp_field: REQUEST_TIMESTAMP_FIELD_NAME}
        )

        self._input_name_to_df[input_name] = context_df
        if self.is_python_mode:
            context_dict = context_df.iloc[self._current_row_index].to_dict()
            return RealtimeContext(request_timestamp=context_dict[REQUEST_TIMESTAMP_FIELD_NAME], _is_python_mode=True)
        else:
            # For Pandas Mode, set the entire context dataframe
            return RealtimeContext(row_level_data=context_df, _is_python_mode=False)

    # TODO(Oleksii): remove this once Snowflake & Athena are deprecated
    def _rename_pandas_columns(
        self, select_columns_and_rename_map: Dict[str, str], input_name: str
    ) -> pandas.DataFrame:
        for f in select_columns_and_rename_map.keys():
            if f not in self._data_df.columns:
                msg = f"{self._fco_name} {self._name} has a dependency on the Feature View '{input_name}'. Feature {f} of this Feature View is not found in the retrieved historical data. Available columns: {list(self._data_df.columns)}"
                raise TectonValidationError(msg)

        # Select all of the features of the input FV from data_df
        return self._data_df.rename(columns=select_columns_and_rename_map)[[*select_columns_and_rename_map.values()]]

    # TODO(Oleksii): remove this once Snowflake & Athena are deprecated
    def _get_request_context_pandas_df(self, request_context_schema: SchemaProto, input_name: str) -> pandas.DataFrame:
        request_context_fields = [self._column_name_updater(c.name) for c in request_context_schema.columns]
        for f in request_context_fields:
            if f not in self._data_df.columns:
                msg = f"{self._fco_name} {self._name} has a dependency on the Request Data Source named '{input_name}'. Field {f} of this Request Data Source is not found in the spine. Available columns: {list(self._data_df.columns)}"
                raise TectonValidationError(msg)

        return self._data_df[request_context_fields]
