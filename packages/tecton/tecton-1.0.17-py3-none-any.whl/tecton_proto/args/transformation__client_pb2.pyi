from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
TRANSFORMATION_MODE_BIGQUERY_SQL: TransformationMode
TRANSFORMATION_MODE_PANDAS: TransformationMode
TRANSFORMATION_MODE_PYSPARK: TransformationMode
TRANSFORMATION_MODE_PYTHON: TransformationMode
TRANSFORMATION_MODE_SNOWFLAKE_SQL: TransformationMode
TRANSFORMATION_MODE_SNOWPARK: TransformationMode
TRANSFORMATION_MODE_SPARK_SQL: TransformationMode
TRANSFORMATION_MODE_UNSPECIFIED: TransformationMode

class TransformationArgs(_message.Message):
    __slots__ = ["docstring", "info", "is_builtin", "options", "prevent_destroy", "transformation_id", "transformation_mode", "user_function", "version"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    DOCSTRING_FIELD_NUMBER: ClassVar[int]
    INFO_FIELD_NUMBER: ClassVar[int]
    IS_BUILTIN_FIELD_NUMBER: ClassVar[int]
    OPTIONS_FIELD_NUMBER: ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_ID_FIELD_NUMBER: ClassVar[int]
    TRANSFORMATION_MODE_FIELD_NUMBER: ClassVar[int]
    USER_FUNCTION_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    docstring: str
    info: _basic_info__client_pb2.BasicInfo
    is_builtin: bool
    options: _containers.ScalarMap[str, str]
    prevent_destroy: bool
    transformation_id: _id__client_pb2.Id
    transformation_mode: TransformationMode
    user_function: _user_defined_function__client_pb2.UserDefinedFunction
    version: _framework_version__client_pb2.FrameworkVersion
    def __init__(self, transformation_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., info: Optional[Union[_basic_info__client_pb2.BasicInfo, Mapping]] = ..., version: Optional[Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., prevent_destroy: bool = ..., options: Optional[Mapping[str, str]] = ..., transformation_mode: Optional[Union[TransformationMode, str]] = ..., user_function: Optional[Union[_user_defined_function__client_pb2.UserDefinedFunction, Mapping]] = ..., docstring: Optional[str] = ..., is_builtin: bool = ...) -> None: ...

class TransformationMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
