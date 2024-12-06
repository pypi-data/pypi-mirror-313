import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class FilterCreateRequest(_message.Message):
    __slots__ = ("data_type", "expression", "description", "name")
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    data_type: str
    expression: str
    description: str
    name: str
    def __init__(self, data_type: _Optional[str] = ..., expression: _Optional[str] = ..., description: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class FilterCreateResponse(_message.Message):
    __slots__ = ("status_code", "filter_id")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    FILTER_ID_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    filter_id: str
    def __init__(self, status_code: _Optional[int] = ..., filter_id: _Optional[str] = ...) -> None: ...

class FilterDeleteRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class FilterDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class FilterMappingCreateRequest(_message.Message):
    __slots__ = ("computation_id", "filter_id")
    COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_ID_FIELD_NUMBER: _ClassVar[int]
    computation_id: str
    filter_id: str
    def __init__(self, computation_id: _Optional[str] = ..., filter_id: _Optional[str] = ...) -> None: ...

class FilterMappingCreateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class FilterListRequest(_message.Message):
    __slots__ = ("pagination", "data_types")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2.Pagination
    data_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., data_types: _Optional[_Iterable[str]] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("id", "name", "description", "expression", "data_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    expression: str
    data_type: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., expression: _Optional[str] = ..., data_type: _Optional[str] = ...) -> None: ...

class FilterListResponse(_message.Message):
    __slots__ = ("status_code", "filters", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    filters: _containers.RepeatedCompositeFieldContainer[Filter]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., filters: _Optional[_Iterable[_Union[Filter, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...
