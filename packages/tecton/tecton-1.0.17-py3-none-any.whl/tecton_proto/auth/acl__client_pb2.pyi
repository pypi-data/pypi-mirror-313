from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Acl(_message.Message):
    __slots__ = ["api_key_ids", "okta_ids", "permission"]
    API_KEY_IDS_FIELD_NUMBER: ClassVar[int]
    OKTA_IDS_FIELD_NUMBER: ClassVar[int]
    PERMISSION_FIELD_NUMBER: ClassVar[int]
    api_key_ids: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    okta_ids: _containers.RepeatedScalarFieldContainer[str]
    permission: str
    def __init__(self, permission: Optional[str] = ..., api_key_ids: Optional[Iterable[Union[_id__client_pb2.Id, Mapping]]] = ..., okta_ids: Optional[Iterable[str]] = ...) -> None: ...
