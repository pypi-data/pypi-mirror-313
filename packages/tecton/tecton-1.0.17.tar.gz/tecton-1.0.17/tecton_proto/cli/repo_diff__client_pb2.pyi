from tecton_proto.data import state_update__client_pb2 as _state_update__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DATA_SOURCE: TectonObjectType
DESCRIPTOR: _descriptor.FileDescriptor
ENTITY: TectonObjectType
FEATURE_SERVICE: TectonObjectType
FEATURE_VIEW: TectonObjectType
SERVER_GROUP: TectonObjectType
TECTON_OBJECT_TYPE_UNKNOWN: TectonObjectType
TRANSFORMATION: TectonObjectType

class TectonObjectDiff(_message.Message):
    __slots__ = ["object_metadata", "transition_side_effects", "transition_type", "warnings"]
    OBJECT_METADATA_FIELD_NUMBER: ClassVar[int]
    TRANSITION_SIDE_EFFECTS_FIELD_NUMBER: ClassVar[int]
    TRANSITION_TYPE_FIELD_NUMBER: ClassVar[int]
    WARNINGS_FIELD_NUMBER: ClassVar[int]
    object_metadata: TectonObjectMetadata
    transition_side_effects: _state_update__client_pb2.FcoTransitionSideEffects
    transition_type: _state_update__client_pb2.FcoTransitionType
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, transition_type: Optional[Union[_state_update__client_pb2.FcoTransitionType, str]] = ..., transition_side_effects: Optional[Union[_state_update__client_pb2.FcoTransitionSideEffects, Mapping]] = ..., object_metadata: Optional[Union[TectonObjectMetadata, Mapping]] = ..., warnings: Optional[Iterable[str]] = ...) -> None: ...

class TectonObjectMetadata(_message.Message):
    __slots__ = ["description", "name", "object_type", "owner", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: ClassVar[int]
    OWNER_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    description: str
    name: str
    object_type: TectonObjectType
    owner: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: Optional[str] = ..., object_type: Optional[Union[TectonObjectType, str]] = ..., owner: Optional[str] = ..., description: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ...) -> None: ...

class TectonRepoDiffSummary(_message.Message):
    __slots__ = ["object_diffs", "plan_id"]
    OBJECT_DIFFS_FIELD_NUMBER: ClassVar[int]
    PLAN_ID_FIELD_NUMBER: ClassVar[int]
    object_diffs: _containers.RepeatedCompositeFieldContainer[TectonObjectDiff]
    plan_id: str
    def __init__(self, object_diffs: Optional[Iterable[Union[TectonObjectDiff, Mapping]]] = ..., plan_id: Optional[str] = ...) -> None: ...

class TectonObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
