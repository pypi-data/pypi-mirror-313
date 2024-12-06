from tecton_proto.args import entity__client_pb2 as _entity__client_pb2
from tecton_proto.args import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import server_group__client_pb2 as _server_group__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.modelartifactservice import model_artifact_service__client_pb2 as _model_artifact_service__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    args: _entity__client_pb2.EntityArgs
    def __init__(self, args: Optional[Union[_entity__client_pb2.EntityArgs, Mapping]] = ...) -> None: ...

class FcoValidationArgs(_message.Message):
    __slots__ = ["entity", "feature_service", "feature_view", "server_group", "transformation", "virtual_data_source"]
    ENTITY_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    SERVER_GROUP_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCE_FIELD_NUMBER: ClassVar[int]
    entity: EntityValidationArgs
    feature_service: FeatureServiceValidationArgs
    feature_view: FeatureViewValidationArgs
    server_group: ServerGroupValidationArgs
    transformation: TransformationValidationArgs
    virtual_data_source: VirtualDataSourceValidationArgs
    def __init__(self, virtual_data_source: Optional[Union[VirtualDataSourceValidationArgs, Mapping]] = ..., entity: Optional[Union[EntityValidationArgs, Mapping]] = ..., feature_view: Optional[Union[FeatureViewValidationArgs, Mapping]] = ..., feature_service: Optional[Union[FeatureServiceValidationArgs, Mapping]] = ..., transformation: Optional[Union[TransformationValidationArgs, Mapping]] = ..., server_group: Optional[Union[ServerGroupValidationArgs, Mapping]] = ...) -> None: ...

class FeatureServiceValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    args: _feature_service__client_pb2.FeatureServiceArgs
    def __init__(self, args: Optional[Union[_feature_service__client_pb2.FeatureServiceArgs, Mapping]] = ...) -> None: ...

class FeatureViewValidationArgs(_message.Message):
    __slots__ = ["args", "local_model_artifacts", "materialization_schema", "view_schema"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    LOCAL_MODEL_ARTIFACTS_FIELD_NUMBER: ClassVar[int]
    MATERIALIZATION_SCHEMA_FIELD_NUMBER: ClassVar[int]
    VIEW_SCHEMA_FIELD_NUMBER: ClassVar[int]
    args: _feature_view__client_pb2.FeatureViewArgs
    local_model_artifacts: _containers.RepeatedCompositeFieldContainer[_model_artifact_service__client_pb2.ModelArtifactInfo]
    materialization_schema: _schema__client_pb2.Schema
    view_schema: _schema__client_pb2.Schema
    def __init__(self, args: Optional[Union[_feature_view__client_pb2.FeatureViewArgs, Mapping]] = ..., view_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., materialization_schema: Optional[Union[_schema__client_pb2.Schema, Mapping]] = ..., local_model_artifacts: Optional[Iterable[Union[_model_artifact_service__client_pb2.ModelArtifactInfo, Mapping]]] = ...) -> None: ...

class ServerGroupValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    args: _server_group__client_pb2.ServerGroupArgs
    def __init__(self, args: Optional[Union[_server_group__client_pb2.ServerGroupArgs, Mapping]] = ...) -> None: ...

class TransformationValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    args: _transformation__client_pb2.TransformationArgs
    def __init__(self, args: Optional[Union[_transformation__client_pb2.TransformationArgs, Mapping]] = ...) -> None: ...

class ValidationRequest(_message.Message):
    __slots__ = ["validation_args"]
    VALIDATION_ARGS_FIELD_NUMBER: ClassVar[int]
    validation_args: _containers.RepeatedCompositeFieldContainer[FcoValidationArgs]
    def __init__(self, validation_args: Optional[Iterable[Union[FcoValidationArgs, Mapping]]] = ...) -> None: ...

class VirtualDataSourceValidationArgs(_message.Message):
    __slots__ = ["args", "batch_schema", "stream_schema"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    BATCH_SCHEMA_FIELD_NUMBER: ClassVar[int]
    STREAM_SCHEMA_FIELD_NUMBER: ClassVar[int]
    args: _virtual_data_source__client_pb2.VirtualDataSourceArgs
    batch_schema: _spark_schema__client_pb2.SparkSchema
    stream_schema: _spark_schema__client_pb2.SparkSchema
    def __init__(self, args: Optional[Union[_virtual_data_source__client_pb2.VirtualDataSourceArgs, Mapping]] = ..., batch_schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ..., stream_schema: Optional[Union[_spark_schema__client_pb2.SparkSchema, Mapping]] = ...) -> None: ...
