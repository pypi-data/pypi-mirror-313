from tecton_proto.realtime import instance_group__client_pb2 as _instance_group__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColocatedComputeConfig(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class InstanceGroupComputeConfig(_message.Message):
    __slots__ = ["group_name", "instance_group"]
    GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    group_name: str
    instance_group: _instance_group__client_pb2.InstanceGroupHandle
    def __init__(self, group_name: Optional[str] = ..., instance_group: Optional[Union[_instance_group__client_pb2.InstanceGroupHandle, Mapping]] = ...) -> None: ...

class OnlineComputeConfig(_message.Message):
    __slots__ = ["colocated_compute", "instance_group_config", "remote_compute"]
    COLOCATED_COMPUTE_FIELD_NUMBER: ClassVar[int]
    INSTANCE_GROUP_CONFIG_FIELD_NUMBER: ClassVar[int]
    REMOTE_COMPUTE_FIELD_NUMBER: ClassVar[int]
    colocated_compute: ColocatedComputeConfig
    instance_group_config: InstanceGroupComputeConfig
    remote_compute: RemoteFunctionComputeConfig
    def __init__(self, colocated_compute: Optional[Union[ColocatedComputeConfig, Mapping]] = ..., remote_compute: Optional[Union[RemoteFunctionComputeConfig, Mapping]] = ..., instance_group_config: Optional[Union[InstanceGroupComputeConfig, Mapping]] = ...) -> None: ...

class RemoteFunctionComputeConfig(_message.Message):
    __slots__ = ["function_uri", "id", "name"]
    FUNCTION_URI_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    function_uri: str
    id: str
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., function_uri: Optional[str] = ...) -> None: ...
