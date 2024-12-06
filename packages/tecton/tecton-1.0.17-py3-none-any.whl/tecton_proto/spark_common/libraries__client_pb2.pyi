from tecton_proto.spark_common import clusters__client_pb2 as _clusters__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Library(_message.Message):
    __slots__ = ["egg", "egg_resource", "jar", "jar_resource", "maven", "pypi", "whl", "whl_resource"]
    EGG_FIELD_NUMBER: ClassVar[int]
    EGG_RESOURCE_FIELD_NUMBER: ClassVar[int]
    JAR_FIELD_NUMBER: ClassVar[int]
    JAR_RESOURCE_FIELD_NUMBER: ClassVar[int]
    MAVEN_FIELD_NUMBER: ClassVar[int]
    PYPI_FIELD_NUMBER: ClassVar[int]
    WHL_FIELD_NUMBER: ClassVar[int]
    WHL_RESOURCE_FIELD_NUMBER: ClassVar[int]
    egg: str
    egg_resource: _clusters__client_pb2.ResourceLocation
    jar: str
    jar_resource: _clusters__client_pb2.ResourceLocation
    maven: MavenLibrary
    pypi: PyPiLibrary
    whl: str
    whl_resource: _clusters__client_pb2.ResourceLocation
    def __init__(self, jar: Optional[str] = ..., egg: Optional[str] = ..., whl: Optional[str] = ..., jar_resource: Optional[Union[_clusters__client_pb2.ResourceLocation, Mapping]] = ..., egg_resource: Optional[Union[_clusters__client_pb2.ResourceLocation, Mapping]] = ..., whl_resource: Optional[Union[_clusters__client_pb2.ResourceLocation, Mapping]] = ..., maven: Optional[Union[MavenLibrary, Mapping]] = ..., pypi: Optional[Union[PyPiLibrary, Mapping]] = ...) -> None: ...

class MavenLibrary(_message.Message):
    __slots__ = ["coordinates", "exclusions", "repo"]
    COORDINATES_FIELD_NUMBER: ClassVar[int]
    EXCLUSIONS_FIELD_NUMBER: ClassVar[int]
    REPO_FIELD_NUMBER: ClassVar[int]
    coordinates: str
    exclusions: _containers.RepeatedScalarFieldContainer[str]
    repo: str
    def __init__(self, coordinates: Optional[str] = ..., repo: Optional[str] = ..., exclusions: Optional[Iterable[str]] = ...) -> None: ...

class PyPiLibrary(_message.Message):
    __slots__ = ["package", "repo"]
    PACKAGE_FIELD_NUMBER: ClassVar[int]
    REPO_FIELD_NUMBER: ClassVar[int]
    package: str
    repo: str
    def __init__(self, package: Optional[str] = ..., repo: Optional[str] = ...) -> None: ...
