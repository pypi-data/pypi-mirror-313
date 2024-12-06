from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class Algorithm(_message.Message):
    __slots__ = ("id", "name", "display_name", "author", "created_on")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    display_name: str
    author: str
    created_on: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ..., author: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AlgorithmCreateRequest(_message.Message):
    __slots__ = ("name", "display_name", "author")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    author: str
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class AlgorithmCreateResponse(_message.Message):
    __slots__ = ("status_code", "algorithm")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm: Algorithm
    def __init__(self, status_code: _Optional[int] = ..., algorithm: _Optional[_Union[Algorithm, _Mapping]] = ...) -> None: ...

class AlgorithmGetRequest(_message.Message):
    __slots__ = ("ids", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    pagination: _common_models_pb2.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmGetResponse(_message.Message):
    __slots__ = ("status_code", "algorithms", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHMS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithms: _containers.RepeatedCompositeFieldContainer[Algorithm]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithms: _Optional[_Iterable[_Union[Algorithm, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmListRequest(_message.Message):
    __slots__ = ("search_text", "min_created_on", "max_created_on", "pagination")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    min_created_on: _timestamp_pb2.Timestamp
    max_created_on: _timestamp_pb2.Timestamp
    pagination: _common_models_pb2.Pagination
    def __init__(self, search_text: _Optional[str] = ..., min_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmListResponse(_message.Message):
    __slots__ = ("status_code", "algorithms", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHMS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithms: _containers.RepeatedCompositeFieldContainer[Algorithm]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithms: _Optional[_Iterable[_Union[Algorithm, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmUpdateRequest(_message.Message):
    __slots__ = ("algorithms",)
    ALGORITHMS_FIELD_NUMBER: _ClassVar[int]
    algorithms: _containers.RepeatedCompositeFieldContainer[Algorithm]
    def __init__(self, algorithms: _Optional[_Iterable[_Union[Algorithm, _Mapping]]] = ...) -> None: ...

class AlgorithmUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
