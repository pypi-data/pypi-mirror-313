from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class AnalysisAlgorithmNode(_message.Message):
    __slots__ = ("name", "algorithm_version_id", "children")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    name: str
    algorithm_version_id: str
    children: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., algorithm_version_id: _Optional[str] = ..., children: _Optional[_Iterable[str]] = ...) -> None: ...

class AnalysisCreateRequest(_message.Message):
    __slots__ = ("name", "author")
    NAME_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    author: str
    def __init__(self, name: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class AnalysisCreateResponse(_message.Message):
    __slots__ = ("status_code", "analysis")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis: Analysis
    def __init__(self, status_code: _Optional[int] = ..., analysis: _Optional[_Union[Analysis, _Mapping]] = ...) -> None: ...

class AnalysisAlgorithmConfigNode(_message.Message):
    __slots__ = ("name", "algorithm_config_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    algorithm_config_id: str
    def __init__(self, name: _Optional[str] = ..., algorithm_config_id: _Optional[str] = ...) -> None: ...

class AnalysisGetRequest(_message.Message):
    __slots__ = ("ids", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    pagination: _common_models_pb2.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class Analysis(_message.Message):
    __slots__ = ("id", "author", "created_on", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    author: str
    created_on: _timestamp_pb2.Timestamp
    name: str
    def __init__(self, id: _Optional[str] = ..., author: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class AnalysisGetResponse(_message.Message):
    __slots__ = ("status_code", "analyses", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analyses: _containers.RepeatedCompositeFieldContainer[Analysis]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analyses: _Optional[_Iterable[_Union[Analysis, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisListRequest(_message.Message):
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

class AnalysisListResponse(_message.Message):
    __slots__ = ("status_code", "analyses", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analyses: _containers.RepeatedCompositeFieldContainer[Analysis]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analyses: _Optional[_Iterable[_Union[Analysis, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...
