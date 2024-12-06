from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class PingRequestServerStreaming(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PingResponseServerStreaming(_message.Message):
    __slots__ = ("status_code", "count")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    count: int
    def __init__(self, status_code: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
