from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SnowflakeCredentials(_message.Message):
    __slots__ = ["password_secret_name", "private_key_alias", "user"]
    PASSWORD_SECRET_NAME_FIELD_NUMBER: ClassVar[int]
    PRIVATE_KEY_ALIAS_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    password_secret_name: str
    private_key_alias: str
    user: str
    def __init__(self, user: Optional[str] = ..., password_secret_name: Optional[str] = ..., private_key_alias: Optional[str] = ...) -> None: ...
