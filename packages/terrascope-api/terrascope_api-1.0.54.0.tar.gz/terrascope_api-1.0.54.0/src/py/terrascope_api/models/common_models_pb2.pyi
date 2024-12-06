from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Pagination(_message.Message):
    __slots__ = ("page_token", "page_size", "next_page_token")
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_token: str
    page_size: int
    next_page_token: str
    def __init__(self, page_token: _Optional[str] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...
