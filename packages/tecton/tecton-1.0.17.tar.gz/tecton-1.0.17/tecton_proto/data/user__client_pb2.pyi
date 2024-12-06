from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ["created_at", "first_name", "is_admin", "last_login", "last_name", "login_email", "okta_id", "okta_status"]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: ClassVar[int]
    IS_ADMIN_FIELD_NUMBER: ClassVar[int]
    LAST_LOGIN_FIELD_NUMBER: ClassVar[int]
    LAST_NAME_FIELD_NUMBER: ClassVar[int]
    LOGIN_EMAIL_FIELD_NUMBER: ClassVar[int]
    OKTA_ID_FIELD_NUMBER: ClassVar[int]
    OKTA_STATUS_FIELD_NUMBER: ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    first_name: str
    is_admin: bool
    last_login: _timestamp_pb2.Timestamp
    last_name: str
    login_email: str
    okta_id: str
    okta_status: str
    def __init__(self, okta_id: Optional[str] = ..., first_name: Optional[str] = ..., last_name: Optional[str] = ..., login_email: Optional[str] = ..., okta_status: Optional[str] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., is_admin: bool = ..., last_login: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ...) -> None: ...
