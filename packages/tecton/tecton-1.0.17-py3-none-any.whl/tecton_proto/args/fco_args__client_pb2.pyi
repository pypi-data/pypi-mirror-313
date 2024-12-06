from tecton_proto.args import entity__client_pb2 as _entity__client_pb2
from tecton_proto.args import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import server_group__client_pb2 as _server_group__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class FcoArgs(_message.Message):
    __slots__ = ["entity", "feature_service", "feature_view", "server_group", "transformation", "virtual_data_source"]
    ENTITY_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: ClassVar[int]
    SERVER_GROUP_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: ClassVar[int]
    VIRTUAL_DATA_SOURCE_FIELD_NUMBER: ClassVar[int]
    entity: _entity__client_pb2.EntityArgs
    feature_service: _feature_service__client_pb2.FeatureServiceArgs
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    server_group: _server_group__client_pb2.ServerGroupArgs
    transformation: _transformation__client_pb2.TransformationArgs
    virtual_data_source: _virtual_data_source__client_pb2.VirtualDataSourceArgs
    def __init__(self, virtual_data_source: Optional[Union[_virtual_data_source__client_pb2.VirtualDataSourceArgs, Mapping]] = ..., entity: Optional[Union[_entity__client_pb2.EntityArgs, Mapping]] = ..., feature_view: Optional[Union[_feature_view__client_pb2.FeatureViewArgs, Mapping]] = ..., feature_service: Optional[Union[_feature_service__client_pb2.FeatureServiceArgs, Mapping]] = ..., transformation: Optional[Union[_transformation__client_pb2.TransformationArgs, Mapping]] = ..., server_group: Optional[Union[_server_group__client_pb2.ServerGroupArgs, Mapping]] = ...) -> None: ...
