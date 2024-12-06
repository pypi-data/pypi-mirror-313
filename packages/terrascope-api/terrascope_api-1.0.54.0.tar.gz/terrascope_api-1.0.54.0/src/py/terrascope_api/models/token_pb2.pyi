import common_models_pb2 as _common_models_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class TokenCreateRequest(_message.Message):
    __slots__ = ("duration_minutes", "for_user_id")
    DURATION_MINUTES_FIELD_NUMBER: _ClassVar[int]
    FOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    duration_minutes: int
    for_user_id: str
    def __init__(self, duration_minutes: _Optional[int] = ..., for_user_id: _Optional[str] = ...) -> None: ...

class TokenCreateResponse(_message.Message):
    __slots__ = ("status_code", "jwt_token")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    JWT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    jwt_token: str
    def __init__(self, status_code: _Optional[int] = ..., jwt_token: _Optional[str] = ...) -> None: ...
