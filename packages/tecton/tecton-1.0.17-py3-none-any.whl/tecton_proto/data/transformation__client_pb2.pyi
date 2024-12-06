from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transformation(_message.Message):
    __slots__ = ["fco_metadata", "options", "transformation_id", "transformation_mode", "user_function", "validation_args"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    FCO_METADATA_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_ID_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_MODE_FIELD_NUMBER: ClassVar[int]
    USER_FUNCTION_FIELD_NUMBER: ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: ClassVar[int]
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    options: _containers.ScalarMap[str, str]
    transformation_id: _id__client_pb2.Id
    transformation_mode: _transformation__client_pb2.TransformationMode
    user_function: _user_defined_function__client_pb2.UserDefinedFunction
    validation_args: _validator__client_pb2.TransformationValidationArgs
    def __init__(self, transformation_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., fco_metadata: Optional[Union[_fco_metadata__client_pb2.FcoMetadata, Mapping]] = ..., transformation_mode: Optional[Union[_transformation__client_pb2.TransformationMode, str]] = ..., user_function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., validation_args: Optional[Union[_validator__client_pb2.TransformationValidationArgs, Mapping]] = ..., options: Optional[Mapping[str, str]] = ...) -> None: ...
