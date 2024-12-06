from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ContainerImage(_message.Message):
    __slots__ = ["image_digest", "image_tag", "image_uri", "repository_name"]
    IMAGE_DIGEST_FIELD_NUMBER: ClassVar[int]
    IMAGE_TAG_FIELD_NUMBER: ClassVar[int]
    IMAGE_URI_FIELD_NUMBER: ClassVar[int]
    REPOSITORY_NAME_FIELD_NUMBER: ClassVar[int]
    image_digest: str
    image_tag: str
    image_uri: str
    repository_name: str
    def __init__(self, repository_name: Optional[str] = ..., image_uri: Optional[str] = ..., image_digest: Optional[str] = ..., image_tag: Optional[str] = ...) -> None: ...
