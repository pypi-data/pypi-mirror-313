from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class FcoSummary(_message.Message):
    __slots__ = ["fco_metadata", "summary_items"]
    FCO_METADATA_FIELD_NUMBER: ClassVar[int]
    SUMMARY_ITEMS_FIELD_NUMBER: ClassVar[int]
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    summary_items: _containers.RepeatedCompositeFieldContainer[SummaryItem]
    def __init__(self, fco_metadata: Optional[Union[_fco_metadata__client_pb2.FcoMetadata, Mapping]] = ..., summary_items: Optional[Iterable[Union[SummaryItem, Mapping]]] = ...) -> None: ...

class SummaryItem(_message.Message):
    __slots__ = ["display_name", "key", "multi_values", "nested_summary_items", "value"]
    DISPLAY_NAME_FIELD_NUMBER: ClassVar[int]
    KEY_FIELD_NUMBER: ClassVar[int]
    MULTI_VALUES_FIELD_NUMBER: ClassVar[int]
    NESTED_SUMMARY_ITEMS_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    display_name: str
    key: str
    multi_values: _containers.RepeatedScalarFieldContainer[str]
    nested_summary_items: _containers.RepeatedCompositeFieldContainer[SummaryItem]
    value: str
    def __init__(self, key: Optional[str] = ..., display_name: Optional[str] = ..., value: Optional[str] = ..., multi_values: Optional[Iterable[str]] = ..., nested_summary_items: Optional[Iterable[Union[SummaryItem, Mapping]]] = ...) -> None: ...
