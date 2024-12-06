from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.common import server_group_status__client_pb2 as _server_group_status__client_pb2
from tecton_proto.common import server_group_type__client_pb2 as _server_group_type__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetServerGroupRequest(_message.Message):
    __slots__ = ["server_group_name", "workspace"]
    SERVER_GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    server_group_name: str
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., server_group_name: Optional[str] = ...) -> None: ...

class GetServerGroupResponse(_message.Message):
    __slots__ = ["server_group"]
    SERVER_GROUP_FIELD_NUMBER: ClassVar[int]
    server_group: ServerGroupInfo
    def __init__(self, server_group: Optional[Union[ServerGroupInfo, Mapping]] = ...) -> None: ...

class ListServerGroupsRequest(_message.Message):
    __slots__ = ["type", "workspace"]
    TYPE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    type: _server_group_type__client_pb2.ServerGroupType
    workspace: str
    def __init__(self, workspace: Optional[str] = ..., type: Optional[Union[_server_group_type__client_pb2.ServerGroupType, str]] = ...) -> None: ...

class ListServerGroupsResponse(_message.Message):
    __slots__ = ["server_groups"]
    SERVER_GROUPS_FIELD_NUMBER: ClassVar[int]
    server_groups: _containers.RepeatedCompositeFieldContainer[ServerGroupInfo]
    def __init__(self, server_groups: Optional[Iterable[Union[ServerGroupInfo, Mapping]]] = ...) -> None: ...

class ServerGroupInfo(_message.Message):
    __slots__ = ["created_at", "current_config", "description", "desired_config", "environment", "last_modified_by", "name", "owner", "server_group_id", "status", "status_details", "tags", "type"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    CURRENT_CONFIG_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    DESIRED_CONFIG_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: ClassVar[int]
    LAST_MODIFIED_BY_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    OWNER_FIELD_NUMBER: ClassVar[int]
    SERVER_GROUP_ID_FIELD_NUMBER: ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    current_config: ServerGroupScalingConfig
    description: str
    desired_config: ServerGroupScalingConfig
    environment: str
    last_modified_by: str
    name: str
    owner: str
    server_group_id: str
    status: _server_group_status__client_pb2.ServerGroupStatus
    status_details: str
    tags: _containers.ScalarMap[str, str]
    type: _server_group_type__client_pb2.ServerGroupType
    def __init__(self, server_group_id: Optional[str] = ..., name: Optional[str] = ..., type: Optional[Union[_server_group_type__client_pb2.ServerGroupType, str]] = ..., description: Optional[str] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., owner: Optional[str] = ..., last_modified_by: Optional[str] = ..., tags: Optional[Mapping[str, str]] = ..., desired_config: Optional[Union[ServerGroupScalingConfig, Mapping]] = ..., current_config: Optional[Union[ServerGroupScalingConfig, Mapping]] = ..., status: Optional[Union[_server_group_status__client_pb2.ServerGroupStatus, str]] = ..., status_details: Optional[str] = ..., environment: Optional[str] = ...) -> None: ...

class ServerGroupScalingConfig(_message.Message):
    __slots__ = ["autoscaling_enabled", "desired_nodes", "last_updated_at", "max_nodes", "min_nodes", "workspace_state_id"]
    AUTOSCALING_ENABLED_FIELD_NUMBER: ClassVar[int]
    DESIRED_NODES_FIELD_NUMBER: ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: ClassVar[int]
    MAX_NODES_FIELD_NUMBER: ClassVar[int]
    MIN_NODES_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    autoscaling_enabled: bool
    desired_nodes: int
    last_updated_at: _timestamp_pb2.Timestamp
    max_nodes: int
    min_nodes: int
    workspace_state_id: str
    def __init__(self, min_nodes: Optional[int] = ..., max_nodes: Optional[int] = ..., desired_nodes: Optional[int] = ..., autoscaling_enabled: bool = ..., last_updated_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., workspace_state_id: Optional[str] = ...) -> None: ...
