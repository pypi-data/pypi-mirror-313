from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateWorkspaceDirectoryRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class GetWorkspaceObjectStatusRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class GetWorkspaceObjectStatusResponse(_message.Message):
    __slots__ = ["created_at", "language", "modified_at", "object_id", "object_type", "path", "size"]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    LANGUAGE_FIELD_NUMBER: ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: ClassVar[int]
    PATH_FIELD_NUMBER: ClassVar[int]
    SIZE_FIELD_NUMBER: ClassVar[int]
    created_at: int
    language: str
    modified_at: int
    object_id: int
    object_type: str
    path: str
    size: int
    def __init__(self, object_type: Optional[str] = ..., path: Optional[str] = ..., language: Optional[str] = ..., created_at: Optional[int] = ..., modified_at: Optional[int] = ..., object_id: Optional[int] = ..., size: Optional[int] = ...) -> None: ...

class ListWorkspaceRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: ClassVar[int]
    path: str
    def __init__(self, path: Optional[str] = ...) -> None: ...

class ListWorkspaceResponse(_message.Message):
    __slots__ = ["objects"]
    OBJECTS_FIELD_NUMBER: ClassVar[int]
    objects: _containers.RepeatedCompositeFieldContainer[ObjectInfo]
    def __init__(self, objects: Optional[Iterable[Union[ObjectInfo, Mapping]]] = ...) -> None: ...

class ObjectInfo(_message.Message):
    __slots__ = ["language", "object_id", "object_type", "path"]
    LANGUAGE_FIELD_NUMBER: ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: ClassVar[int]
    PATH_FIELD_NUMBER: ClassVar[int]
    language: str
    object_id: int
    object_type: str
    path: str
    def __init__(self, object_type: Optional[str] = ..., object_id: Optional[int] = ..., path: Optional[str] = ..., language: Optional[str] = ...) -> None: ...
