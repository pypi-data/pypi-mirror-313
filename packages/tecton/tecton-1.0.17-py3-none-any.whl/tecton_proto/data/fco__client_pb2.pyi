from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import entity__client_pb2 as _entity__client_pb2
from tecton_proto.data import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.data import server_group__client_pb2 as _server_group__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.data import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Fco(_message.Message):
    __slots__ = ["entity", "feature_service", "feature_view", "server_group", "transformation", "virtual_data_source"]
    ENTITY_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    SERVER_GROUP_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCE_FIELD_NUMBER: ClassVar[int]
    entity: _entity__client_pb2.Entity
    feature_service: _feature_service__client_pb2.FeatureService
    feature_view: _feature_view__client_pb2.FeatureView
    server_group: _server_group__client_pb2.ServerGroup
    transformation: _transformation__client_pb2.Transformation
    virtual_data_source: _virtual_data_source__client_pb2.VirtualDataSource
    def __init__(self, virtual_data_source: Optional[Union[_virtual_data_source__client_pb2.VirtualDataSource, Mapping]] = ..., entity: Optional[Union[_entity__client_pb2.Entity, Mapping]] = ..., feature_view: Optional[Union[_feature_view__client_pb2.FeatureView, Mapping]] = ..., feature_service: Optional[Union[_feature_service__client_pb2.FeatureService, Mapping]] = ..., transformation: Optional[Union[_transformation__client_pb2.Transformation, Mapping]] = ..., server_group: Optional[Union[_server_group__client_pb2.ServerGroup, Mapping]] = ...) -> None: ...

class FcoContainer(_message.Message):
    __slots__ = ["fcos", "root_ids", "workspace", "workspace_state_id"]
    FCOS_FIELD_NUMBER: ClassVar[int]
    ROOT_IDS_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    fcos: _containers.RepeatedCompositeFieldContainer[Fco]
    root_ids: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    workspace: str
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, root_ids: Optional[Iterable[Union[_id__client_pb2.Id, Mapping]]] = ..., fcos: Optional[Iterable[Union[Fco, Mapping]]] = ..., workspace: Optional[str] = ..., workspace_state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...
