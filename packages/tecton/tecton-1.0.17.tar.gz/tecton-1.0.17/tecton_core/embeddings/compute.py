from __future__ import annotations

import logging
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import pyarrow
import torch

from tecton_core.embeddings import custom_model
from tecton_core.embeddings import execution_utils
from tecton_core.embeddings import models
from tecton_core.embeddings import threaded_execution
from tecton_core.embeddings.artifacts_provider import ARTIFACT_PROVIDER
from tecton_core.embeddings.artifacts_provider import InferenceDeviceHardware
from tecton_core.embeddings.artifacts_provider import retrieve_custom_model_artifacts
from tecton_core.embeddings.artifacts_provider import retrieve_open_source_model_artifacts
from tecton_core.embeddings.config import BaseInferenceConfig
from tecton_core.embeddings.config import CustomModelConfig
from tecton_core.embeddings.config import TextEmbeddingInferenceConfig
from tecton_core.embeddings.config import TextEmbeddingModel
from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.query_tree_compute import ModelInferenceCompute
from tecton_proto.common.id__client_pb2 import Id


logger = logging.getLogger(__name__)


def _model_path(model: TextEmbeddingModel) -> str:
    return retrieve_open_source_model_artifacts(model, use_http=True)


def _custom_model_path(
    model_name: str,
    model_artifact_id: Id,
    s3_path: str,
    model_file_path: str,
    model_artifact_provider: ModelArtifactProvider,
) -> str:
    return retrieve_custom_model_artifacts(
        model_name, model_artifact_id, s3_path, model_file_path, model_artifact_provider
    )


def _data_output_type(model: TextEmbeddingModel) -> pyarrow.DataType:
    # NOTE: using dynamic sized pyarrow list due to https://github.com/apache/arrow/issues/35697
    # Need to derive this from the model config in the future
    return pyarrow.list_(pyarrow.float32())


_PreProcessInfo = Tuple[execution_utils.PreprocessorCallable, execution_utils.FuncConfig]
_ModelInfo = Tuple[execution_utils.ModelCallable, Sequence[execution_utils.FuncConfig]]


def _get_device_name() -> InferenceDeviceHardware:
    if torch.cuda.is_available():
        return InferenceDeviceHardware(torch.cuda.get_device_properties(0).name)
    return InferenceDeviceHardware.CPU


def _get_execution_info(
    inference_config: BaseInferenceConfig,
    model_artifact_provider: ModelArtifactProvider,
    token_budget: Optional[int] = None,
) -> Tuple[_PreProcessInfo, _ModelInfo, pyarrow.Field]:
    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        device_name = torch.cuda.get_device_properties(0).name
        cuda_devices = [f"cuda:{i}" for i in range(device_count)]
    else:
        device_name = InferenceDeviceHardware.CPU
        cuda_devices = [InferenceDeviceHardware.CPU]

    if isinstance(inference_config, TextEmbeddingInferenceConfig):
        if token_budget is None:
            token_budget = ARTIFACT_PROVIDER.get_model_info(inference_config.model).get_token_budget(device_name)
        preprocess_func = models.dynamic_token_batching
        preprocess_func_config = models.DynamicBatchingFuncConfig.create(
            token_budget=token_budget,
            column_name=inference_config.input_column,
            model_filename=_model_path(inference_config.model),
        )
        preprocess_info = (preprocess_func, preprocess_func_config)

        inference_func = models.embed_pytorch

        inference_func_configs = [
            models.EmbedPytorchFuncConfig.create(
                model_filename=_model_path(inference_config.model),
                cuda_device=cuda_device,
                input_column_name=inference_config.input_column,
                output_column_name=inference_config.output_column,
            )
            for cuda_device in cuda_devices
        ]
        inference_info = (inference_func, inference_func_configs)

        output_field = pyarrow.field(inference_config.output_column, _data_output_type(inference_config.model))

        return preprocess_info, inference_info, output_field

    if isinstance(inference_config, CustomModelConfig):
        preprocess_func = custom_model.default_custom_batch_fn
        preprocess_func_config = custom_model.CustomModelBatchFuncConfig.create()
        preprocess_info = (preprocess_func, preprocess_func_config)

        inference_func = custom_model.custom_model_inference
        inference_func_configs = [
            custom_model.CustomModelInferenceFuncConfig.create(
                model_dir=_custom_model_path(
                    inference_config.model_artifact.model_name,
                    inference_config.model_artifact.model_artifact_id,
                    inference_config.model_artifact.storage_path,
                    model_file_path=inference_config.model_artifact.model_file_path,
                    model_artifact_provider=model_artifact_provider,
                ),
                model_file_path=inference_config.model_artifact.model_file_path,
                cuda_device=cuda_device,
                input_columns=inference_config.input_columns,
                output_column=inference_config.output_column,
                model_input_schema=inference_config.model_artifact.input_schema,
            )
            for cuda_device in cuda_devices
        ]
        inference_info = (inference_func, inference_func_configs)
        output_field = pyarrow.field(
            inference_config.output_column.name,
            custom_model.tecton_type_to_pyarrow(inference_config.output_column.dtype),
        )

        return preprocess_info, inference_info, output_field

    msg = "Internal Error: inference_config should be either CustomModelConfig or TextEmbeddingInferenceConfig"
    raise NotImplementedError(msg)


@attrs.frozen
class TorchCompute(ModelInferenceCompute):
    model_artifact_provider: Optional[ModelArtifactProvider] = None

    @staticmethod
    def from_context(model_artifact_provider: ModelArtifactProvider) -> TorchCompute:
        return TorchCompute(model_artifact_provider=model_artifact_provider)

    def get_dialect(self) -> Dialect:
        return Dialect.TORCH

    def run_inference(
        self, qt_node: NodeRef, input_data: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> pyarrow.RecordBatchReader:
        if not isinstance(qt_node.node, TextEmbeddingInferenceNode):
            msg = "`run_inference` only supports `TextEmbeddingInferenceNode`"
            raise ValueError(msg)

        for inference_config in qt_node.node.inference_configs:
            print(f"Running inference for {inference_config}")
            # Clear the memory before running the inference in case there are objects cached from prior steps in the GPU
            execution_utils.gc_all()
            preprocess_info, inference_info, output_field = _get_execution_info(
                inference_config, model_artifact_provider=self.model_artifact_provider
            )

            # TODO(jiadong): Enable batch size estimation for custom model.
            if isinstance(inference_config, TextEmbeddingInferenceConfig):
                device_name = _get_device_name()
                token_budget = ARTIFACT_PROVIDER.get_model_info(inference_config.model).get_token_budget(device_name)
                if token_budget is None:
                    print(f"Token budget not found for model {inference_config.model} for device {device_name}.")
                    token_budget = models.estimate_token_budget(inference_info, device_name)
                    ARTIFACT_PROVIDER.get_model_info(inference_config.model).set_token_budget(device_name, token_budget)
                    preprocess_info, inference_info, output_field = _get_execution_info(
                        inference_config,
                        model_artifact_provider=self.model_artifact_provider,
                        token_budget=token_budget,
                    )
                    print(f"Estimated token budget for {inference_config.model} on {device_name} is: {token_budget}")

            if len(inference_info[1]) == 1:
                output_batches = threaded_execution.execute_singlethreaded(
                    data_source=input_data, preprocess_info=preprocess_info, inference_info=inference_info
                )
            else:
                output_batches = threaded_execution.execute_multithreaded(
                    data_source=input_data, preprocess_info=preprocess_info, inference_info=inference_info
                )

            schema = input_data.schema.append(output_field)

            # HACK: round trip through a pyarrow.Table to avoid the segfault
            # when we create a record batch reader over the output batches.
            # Will dig into this more as a follow up.
            input_data = pyarrow.Table.from_batches(output_batches, schema=schema)
            input_data = pyarrow.RecordBatchReader.from_batches(schema, input_data.to_batches())

        return input_data
