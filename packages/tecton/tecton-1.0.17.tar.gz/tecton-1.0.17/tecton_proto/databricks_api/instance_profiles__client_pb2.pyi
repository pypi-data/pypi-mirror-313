from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class InstanceProfile(_message.Message):
    __slots__ = ["instance_profile_arn"]
    INSTANCE_PROFILE_ARN_FIELD_NUMBER: ClassVar[int]
    instance_profile_arn: str
    def __init__(self, instance_profile_arn: Optional[str] = ...) -> None: ...

class InstanceProfilesListResponse(_message.Message):
    __slots__ = ["instance_profiles"]
    INSTANCE_PROFILES_FIELD_NUMBER: ClassVar[int]
    instance_profiles: _containers.RepeatedCompositeFieldContainer[InstanceProfile]
    def __init__(self, instance_profiles: Optional[Iterable[Union[InstanceProfile, Mapping]]] = ...) -> None: ...
