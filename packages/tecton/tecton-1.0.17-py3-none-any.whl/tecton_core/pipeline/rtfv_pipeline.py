from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas

from tecton_core import conf
from tecton_core import specs
from tecton_core.errors import UDF_ERROR
from tecton_core.errors import UDF_TYPE_ERROR
from tecton_core.id_helper import IdHelper
from tecton_core.pipeline.feature_pipeline import FeaturePipeline
from tecton_core.pipeline.feature_pipeline import NodeValueType
from tecton_core.pipeline.pipeline_common import CONSTANT_TYPE
from tecton_core.pipeline.pipeline_common import constant_node_to_value
from tecton_core.realtime_context import RealtimeContext
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode
from tecton_proto.args.transformation__client_pb2 import TransformationMode
from tecton_proto.common.id__client_pb2 import Id as TectonId


class RealtimeFeaturePipeline(FeaturePipeline):
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
        is_prompt: bool,
        events_df_timestamp_field: Optional[str] = None,
        pipeline_inputs: Optional[Dict[str, Union[Dict[str, Any], pandas.DataFrame, RealtimeContext]]] = None,
    ) -> None:
        self._pipeline = pipeline
        self._name = name
        self._id_to_transformation = {t.id: t for t in transformations}
        self._events_df_timestamp_field = events_df_timestamp_field
        self._is_prompt = is_prompt

        root_transformation = self.get_transformation_by_id(self._pipeline.root.transformation_node.transformation_id)
        assert root_transformation.transformation_mode in (
            TransformationMode.TRANSFORMATION_MODE_PYTHON,
            TransformationMode.TRANSFORMATION_MODE_PANDAS,
        )
        # In Spark, the UDF cannot reference a proto enum, so instead save mode as a string
        self.mode = (
            "python"
            if root_transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON
            else "pandas"
        )

        # Access this conf value outside of the UDF to avoid doing it many times and avoiding any worker/driver state issues.
        self._should_check_output_schema = conf.get_bool("TECTON_PYTHON_ODFV_OUTPUT_SCHEMA_CHECK_ENABLED")
        self._pipeline_inputs = pipeline_inputs

    def get_transformation_by_id(self, id: TectonId) -> specs.TransformationSpec:
        return self._id_to_transformation[IdHelper.to_string(id)]

    @property
    def is_pandas_mode(self):
        return self.mode == "pandas"

    @property
    def is_python_mode(self):
        return self.mode == "python"

    def _context_node_to_value(self, pipeline_node: PipelineNode) -> Optional[Union[pandas.DataFrame, RealtimeContext]]:
        assert self._pipeline_inputs is not None
        return self._pipeline_inputs[pipeline_node.context_node.input_name]

    def _request_data_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        assert self._pipeline_inputs is not None
        return self._pipeline_inputs[pipeline_node.request_data_source_node.input_name]

    def _feature_view_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        assert self._pipeline_inputs is not None
        return self._pipeline_inputs[pipeline_node.feature_view_node.input_name]

    def _node_to_value(self, pipeline_node: PipelineNode) -> NodeValueType:
        if pipeline_node.HasField("constant_node"):
            return self._constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("feature_view_node"):
            return self._feature_view_node_to_value(pipeline_node)
        elif pipeline_node.HasField("request_data_source_node"):
            return self._request_data_node_to_value(pipeline_node)
        elif pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_value(pipeline_node.transformation_node)
        elif pipeline_node.HasField("context_node"):
            return self._context_node_to_value(pipeline_node)
        elif pipeline_node.HasField("materialization_context_node"):
            msg = f"MaterializationContext is unsupported for {self._fco_name}s."
            raise ValueError(msg)
        else:
            msg = f"This is not yet implemented {pipeline_node}"
            raise NotImplementedError(msg)

    def _constant_node_to_value(self, pipeline_node: PipelineNode) -> CONSTANT_TYPE:
        return constant_node_to_value(pipeline_node)

    @staticmethod
    def _format_values_for_pandas_mode(input_df: pandas.DataFrame) -> pandas.DataFrame:
        for col in input_df.select_dtypes(include=["datetime64"]).columns:
            input_df[col] = pandas.to_datetime(input_df[col], utc=True)
        return input_df

    def _transformation_node_to_value(
        self, transformation_node: TransformationNode
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[str, int, float, bool]] = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            input_node = transformation_input.node
            node_value = self._node_to_value(input_node)

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
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation.

        If needed, resulted function is wrapped with a function that translates mode-specific input/output types to DataFrames.
        """
        transformation = self.get_transformation_by_id(transformation_node.transformation_id)
        mode = transformation.transformation_mode
        user_function = transformation.user_function

        if (
            mode != TransformationMode.TRANSFORMATION_MODE_PANDAS
            and mode != TransformationMode.TRANSFORMATION_MODE_PYTHON
        ):
            msg = f"Unsupported transformation mode({transformation.transformation_mode}) for {self._fco_name}s."
            raise KeyError(msg)

        try:
            resp = user_function(*args, **kwargs)
            return self._wrap_resp(resp)
        except TypeError as e:
            raise UDF_TYPE_ERROR(e)
        except Exception as e:
            raise UDF_ERROR(e, transformation.metadata.name)

    def _wrap_resp(self, resp):
        if self._is_prompt:
            if not isinstance(resp, str):
                msg = "Prompt functions must return strings"
                raise TypeError(msg)
            return {"prompt": resp}
        else:
            return resp

    @property
    def _fco_name(self):
        if self._is_prompt:
            return "Prompt"
        else:
            return "Realtime Feature View"

    def run_with_inputs(
        self, inputs: Union[Dict[str, pandas.DataFrame], Dict[str, Any]]
    ) -> Union[CONSTANT_TYPE, Dict[str, Any], pandas.DataFrame, pandas.Series]:
        self._pipeline_inputs = inputs
        return self.get_dataframe()
