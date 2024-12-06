from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandsExecuteRequest(_message.Message):
    __slots__ = ["clusterId", "command", "contextId", "language"]
    CLUSTERID_FIELD_NUMBER: ClassVar[int]
    COMMAND_FIELD_NUMBER: ClassVar[int]
    CONTEXTID_FIELD_NUMBER: ClassVar[int]
    LANGUAGE_FIELD_NUMBER: ClassVar[int]
    clusterId: str
    command: str
    contextId: str
    language: str
    def __init__(self, language: Optional[str] = ..., clusterId: Optional[str] = ..., contextId: Optional[str] = ..., command: Optional[str] = ...) -> None: ...

class CommandsExecuteResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: ClassVar[int]
    id: str
    def __init__(self, id: Optional[str] = ...) -> None: ...

class CommandsStatusRequest(_message.Message):
    __slots__ = ["clusterId", "commandId", "contextId"]
    CLUSTERID_FIELD_NUMBER: ClassVar[int]
    COMMANDID_FIELD_NUMBER: ClassVar[int]
    CONTEXTID_FIELD_NUMBER: ClassVar[int]
    clusterId: str
    commandId: str
    contextId: str
    def __init__(self, clusterId: Optional[str] = ..., contextId: Optional[str] = ..., commandId: Optional[str] = ...) -> None: ...

class CommandsStatusResponse(_message.Message):
    __slots__ = ["results", "status"]
    RESULTS_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    results: Results
    status: str
    def __init__(self, results: Optional[Union[Results, Mapping]] = ..., status: Optional[str] = ...) -> None: ...

class ContextDestroyRequest(_message.Message):
    __slots__ = ["clusterId", "contextId"]
    CLUSTERID_FIELD_NUMBER: ClassVar[int]
    CONTEXTID_FIELD_NUMBER: ClassVar[int]
    clusterId: str
    contextId: str
    def __init__(self, clusterId: Optional[str] = ..., contextId: Optional[str] = ...) -> None: ...

class ContextDestroyResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: ClassVar[int]
    id: str
    def __init__(self, id: Optional[str] = ...) -> None: ...

class ContextStatusRequest(_message.Message):
    __slots__ = ["clusterId", "contextId"]
    CLUSTERID_FIELD_NUMBER: ClassVar[int]
    CONTEXTID_FIELD_NUMBER: ClassVar[int]
    clusterId: str
    contextId: str
    def __init__(self, clusterId: Optional[str] = ..., contextId: Optional[str] = ...) -> None: ...

class ContextStatusResponse(_message.Message):
    __slots__ = ["error", "id", "status"]
    ERROR_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    error: str
    id: str
    status: str
    def __init__(self, id: Optional[str] = ..., status: Optional[str] = ..., error: Optional[str] = ...) -> None: ...

class ContextsCreateRequest(_message.Message):
    __slots__ = ["clusterId", "language"]
    CLUSTERID_FIELD_NUMBER: ClassVar[int]
    LANGUAGE_FIELD_NUMBER: ClassVar[int]
    clusterId: str
    language: str
    def __init__(self, language: Optional[str] = ..., clusterId: Optional[str] = ...) -> None: ...

class ContextsCreateResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: ClassVar[int]
    id: str
    def __init__(self, id: Optional[str] = ...) -> None: ...

class Results(_message.Message):
    __slots__ = ["cause", "data", "resultType"]
    CAUSE_FIELD_NUMBER: ClassVar[int]
    DATA_FIELD_NUMBER: ClassVar[int]
    RESULTTYPE_FIELD_NUMBER: ClassVar[int]
    cause: str
    data: str
    resultType: str
    def __init__(self, data: Optional[str] = ..., resultType: Optional[str] = ..., cause: Optional[str] = ...) -> None: ...
