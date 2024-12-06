from __future__ import annotations

from typing import List

from tecton_core import schema
from tecton_proto.modelartifactservice import model_artifact_service__client_pb2 as model_artifact_service_pb2


class ModelArtifactInfo:
    _proto: model_artifact_service_pb2.ModelArtifactInfo

    def __init__(self, proto: model_artifact_service_pb2.ModelArtifactInfo) -> None:
        self._proto = proto

    @property
    def model_name(self) -> str:
        return self._proto.name

    @property
    def model_artifact_id(self) -> str:
        return self._proto.id

    @property
    def storage_path(self) -> str:
        return self._proto.storage_path

    @property
    def model_file_path(self) -> str:
        return self._proto.model_file_path

    @property
    def input_schema(self) -> List[schema.Column]:
        return [schema.Column(name, dtype) for name, dtype in schema.Schema(self._proto.input_schema).to_dict().items()]
