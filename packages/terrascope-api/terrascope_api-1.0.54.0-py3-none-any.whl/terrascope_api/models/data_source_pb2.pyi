import data_type_pb2 as _data_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from data_type_pb2 import DataType as DataType
from data_type_pb2 import DataTypeCreateRequest as DataTypeCreateRequest
from data_type_pb2 import DataTypeCreateResponse as DataTypeCreateResponse
from data_type_pb2 import DataTypeGetRequest as DataTypeGetRequest
from data_type_pb2 import DataTypeGetResponse as DataTypeGetResponse
from data_type_pb2 import DataTypeListRequest as DataTypeListRequest
from data_type_pb2 import DataTypeListResponse as DataTypeListResponse

DESCRIPTOR: _descriptor.FileDescriptor

class DataSource(_message.Message):
    __slots__ = ("id", "name", "description", "data_types", "delivery_lag_seconds", "display_name", "indicator", "data_explorer")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_LAG_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    INDICATOR_FIELD_NUMBER: _ClassVar[int]
    DATA_EXPLORER_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    data_types: _containers.RepeatedCompositeFieldContainer[_data_type_pb2.DataType]
    delivery_lag_seconds: int
    display_name: str
    indicator: str
    data_explorer: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., data_types: _Optional[_Iterable[_Union[_data_type_pb2.DataType, _Mapping]]] = ..., delivery_lag_seconds: _Optional[int] = ..., display_name: _Optional[str] = ..., indicator: _Optional[str] = ..., data_explorer: bool = ...) -> None: ...

class DataSourceGetRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DataSourceGetResponse(_message.Message):
    __slots__ = ("status_code", "data_sources")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    data_sources: _containers.RepeatedCompositeFieldContainer[DataSource]
    def __init__(self, status_code: _Optional[int] = ..., data_sources: _Optional[_Iterable[_Union[DataSource, _Mapping]]] = ...) -> None: ...

class DataSourceListRequest(_message.Message):
    __slots__ = ("search_text",)
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    def __init__(self, search_text: _Optional[str] = ...) -> None: ...

class DataSourceListResponse(_message.Message):
    __slots__ = ("status_code", "data_sources")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    data_sources: _containers.RepeatedCompositeFieldContainer[DataSource]
    def __init__(self, status_code: _Optional[int] = ..., data_sources: _Optional[_Iterable[_Union[DataSource, _Mapping]]] = ...) -> None: ...
