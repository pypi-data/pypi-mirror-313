from tecton_proto.args import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.data import realtime_compute__client_pb2 as _realtime_compute__client_pb2
from tecton_proto.data import server_group__client_pb2 as _server_group__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
JOIN_KEY_BINDING_TYPE_BOUND: JoinKeyBindingType
JOIN_KEY_BINDING_TYPE_UNSPECIFIED: JoinKeyBindingType
JOIN_KEY_BINDING_TYPE_WILDCARD: JoinKeyBindingType

class FeatureService(_message.Message):
    __slots__ = ["enable_online_caching", "fco_metadata", "feature_server_group", "feature_service_id", "feature_set_items", "logging", "online_serving_enabled", "options", "realtime_environment", "transform_server_group", "validation_args"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ENABLE_ONLINE_CACHING_FIELD_NUMBER: ClassVar[int]
    FCO_METADATA_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_GROUP_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: ClassVar[int]
    FEATURE_SET_ITEMS_FIELD_NUMBER: ClassVar[int]
    LOGGING_FIELD_NUMBER: ClassVar[int]
    ONLINE_SERVING_ENABLED_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    REALTIME_ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    TRANSFORM_SERVER_GROUP_FIELD_NUMBER: ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: ClassVar[int]
    enable_online_caching: bool
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    feature_server_group: _server_group__client_pb2.ServerGroup
    feature_service_id: _id__client_pb2.Id
    feature_set_items: _containers.RepeatedCompositeFieldContainer[FeatureSetItem]
    logging: _feature_service__client_pb2.LoggingConfigArgs
    online_serving_enabled: bool
    options: _containers.ScalarMap[str, str]
    realtime_environment: _realtime_compute__client_pb2.OnlineComputeConfig
    transform_server_group: _server_group__client_pb2.ServerGroup
    validation_args: _validator__client_pb2.FeatureServiceValidationArgs
    def __init__(self, feature_service_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., feature_set_items: Optional[Iterable[Union[FeatureSetItem, Mapping]]] = ..., fco_metadata: Optional[Union[_fco_metadata__client_pb2.FcoMetadata, Mapping]] = ..., online_serving_enabled: bool = ..., logging: Optional[Union[_feature_service__client_pb2.LoggingConfigArgs, Mapping]] = ..., validation_args: Optional[Union[_validator__client_pb2.FeatureServiceValidationArgs, Mapping]] = ..., realtime_environment: Optional[Union[_realtime_compute__client_pb2.OnlineComputeConfig, Mapping]] = ..., enable_online_caching: bool = ..., transform_server_group: Optional[Union[_server_group__client_pb2.ServerGroup, Mapping]] = ..., feature_server_group: Optional[Union[_server_group__client_pb2.ServerGroup, Mapping]] = ..., options: Optional[Mapping[str, str]] = ...) -> None: ...

class FeatureSetItem(_message.Message):
    __slots__ = ["feature_columns", "feature_view_id", "join_configuration_items", "namespace"]
    FEATURE_COLUMNS_FIELD_NUMBER: ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: ClassVar[int]
    JOIN_CONFIGURATION_ITEMS_FIELD_NUMBER: ClassVar[int]
    NAMESPACE_FIELD_NUMBER: ClassVar[int]
    feature_columns: _containers.RepeatedScalarFieldContainer[str]
    feature_view_id: _id__client_pb2.Id
    join_configuration_items: _containers.RepeatedCompositeFieldContainer[JoinConfigurationItem]
    namespace: str
    def __init__(self, feature_view_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., join_configuration_items: Optional[Iterable[Union[JoinConfigurationItem, Mapping]]] = ..., namespace: Optional[str] = ..., feature_columns: Optional[Iterable[str]] = ...) -> None: ...

class JoinConfigurationItem(_message.Message):
    __slots__ = ["package_column_name", "spine_column_name"]
    PACKAGE_COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    SPINE_COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    package_column_name: str
    spine_column_name: str
    def __init__(self, spine_column_name: Optional[str] = ..., package_column_name: Optional[str] = ...) -> None: ...

class JoinKeyComponent(_message.Message):
    __slots__ = ["binding_type", "data_type", "spine_column_name"]
    BINDING_TYPE_FIELD_NUMBER: ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: ClassVar[int]
    SPINE_COLUMN_NAME_FIELD_NUMBER: ClassVar[int]
    binding_type: JoinKeyBindingType
    data_type: _data_type__client_pb2.DataType
    spine_column_name: str
    def __init__(self, spine_column_name: Optional[str] = ..., binding_type: Optional[Union[JoinKeyBindingType, str]] = ..., data_type: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ...) -> None: ...

class JoinKeyTemplate(_message.Message):
    __slots__ = ["components"]
    COMPONENTS_FIELD_NUMBER: ClassVar[int]
    components: _containers.RepeatedCompositeFieldContainer[JoinKeyComponent]
    def __init__(self, components: Optional[Iterable[Union[JoinKeyComponent, Mapping]]] = ...) -> None: ...

class JoinKeyBindingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
