import common_models_pb2 as _common_models_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class UserForgotPasswordRequest(_message.Message):
    __slots__ = ("user_email",)
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    user_email: str
    def __init__(self, user_email: _Optional[str] = ...) -> None: ...

class UserForgotPasswordResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
