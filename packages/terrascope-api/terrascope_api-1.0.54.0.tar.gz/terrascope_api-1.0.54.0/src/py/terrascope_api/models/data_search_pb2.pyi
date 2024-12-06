from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
import tile_pb2 as _tile_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from tile_pb2 import Bounds as Bounds
from tile_pb2 import TileMatrix as TileMatrix
from tile_pb2 import TileAccessInfo as TileAccessInfo
from tile_pb2 import TileSet as TileSet
from tile_pb2 import TileSetListRequest as TileSetListRequest
from tile_pb2 import TileSetListResponse as TileSetListResponse

DESCRIPTOR: _descriptor.FileDescriptor

class DataSearchSchemaGetRequest(_message.Message):
    __slots__ = ("data_source_id",)
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    def __init__(self, data_source_id: _Optional[str] = ...) -> None: ...

class DataSearchSchemaGetResponse(_message.Message):
    __slots__ = ("data_source_id", "json_schema")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    JSON_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    json_schema: _struct_pb2.Struct
    def __init__(self, data_source_id: _Optional[str] = ..., json_schema: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DataSearchRequest(_message.Message):
    __slots__ = ("data_source_id", "search_params", "aoi_geom", "aoi_id", "time_range", "toi_id", "pagination")
    class TimeRange(_message.Message):
        __slots__ = ("start_utc", "finish_utc")
        START_UTC_FIELD_NUMBER: _ClassVar[int]
        FINISH_UTC_FIELD_NUMBER: _ClassVar[int]
        start_utc: _timestamp_pb2.Timestamp
        finish_utc: _timestamp_pb2.Timestamp
        def __init__(self, start_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., finish_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SEARCH_PARAMS_FIELD_NUMBER: _ClassVar[int]
    AOI_GEOM_FIELD_NUMBER: _ClassVar[int]
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    search_params: _struct_pb2.Struct
    aoi_geom: bytes
    aoi_id: str
    time_range: DataSearchRequest.TimeRange
    toi_id: str
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, data_source_id: _Optional[str] = ..., search_params: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., aoi_geom: _Optional[bytes] = ..., aoi_id: _Optional[str] = ..., time_range: _Optional[_Union[DataSearchRequest.TimeRange, _Mapping]] = ..., toi_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class DataSearchResponse(_message.Message):
    __slots__ = ("geojson_struct", "pagination", "geojson_string")
    GEOJSON_STRUCT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    GEOJSON_STRING_FIELD_NUMBER: _ClassVar[int]
    geojson_struct: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    pagination: _common_models_pb2_1.Pagination
    geojson_string: str
    def __init__(self, geojson_struct: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., geojson_string: _Optional[str] = ...) -> None: ...

class DataSearchDisplayTilesBatchGetRequest(_message.Message):
    __slots__ = ("ids", "search_params", "pagination", "data_source_id")
    IDS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_PARAMS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    search_params: _struct_pb2.Struct
    pagination: _common_models_pb2_1.Pagination
    data_source_id: str
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., search_params: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., data_source_id: _Optional[str] = ...) -> None: ...

class TileSetWithId(_message.Message):
    __slots__ = ("id", "tile_set")
    ID_FIELD_NUMBER: _ClassVar[int]
    TILE_SET_FIELD_NUMBER: _ClassVar[int]
    id: str
    tile_set: _tile_pb2.TileSet
    def __init__(self, id: _Optional[str] = ..., tile_set: _Optional[_Union[_tile_pb2.TileSet, _Mapping]] = ...) -> None: ...

class DataSearchDisplayTilesBatchGetResponse(_message.Message):
    __slots__ = ("tile_sets", "pagination")
    TILE_SETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    tile_sets: _containers.RepeatedCompositeFieldContainer[TileSetWithId]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, tile_sets: _Optional[_Iterable[_Union[TileSetWithId, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class DataSearchResourceBatchGetRequest(_message.Message):
    __slots__ = ("ids", "allow_missing", "pagination", "data_source_id")
    IDS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MISSING_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    allow_missing: bool
    pagination: _common_models_pb2_1.Pagination
    data_source_id: str
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., allow_missing: bool = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., data_source_id: _Optional[str] = ...) -> None: ...

class DataSearchResourceBatchGetResponse(_message.Message):
    __slots__ = ("geojson_struct", "pagination")
    GEOJSON_STRUCT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    geojson_struct: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, geojson_struct: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class DataSearchEstimatedSummaryGetRequest(_message.Message):
    __slots__ = ("data_source_id",)
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    def __init__(self, data_source_id: _Optional[str] = ...) -> None: ...

class SummaryByDate(_message.Message):
    __slots__ = ("count", "unixtime")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UNIXTIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    unixtime: _timestamp_pb2.Timestamp
    def __init__(self, count: _Optional[int] = ..., unixtime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DataSearchEstimatedSummaryGetResponse(_message.Message):
    __slots__ = ("data_source_id", "total_count", "summary_by_date")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_BY_DATE_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    total_count: int
    summary_by_date: _containers.RepeatedCompositeFieldContainer[SummaryByDate]
    def __init__(self, data_source_id: _Optional[str] = ..., total_count: _Optional[int] = ..., summary_by_date: _Optional[_Iterable[_Union[SummaryByDate, _Mapping]]] = ...) -> None: ...

class DataSourceGetDownloadLinkRequest(_message.Message):
    __slots__ = ("data_source_id", "id")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    id: str
    def __init__(self, data_source_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class DataSourceGetDownloadLinkResponse(_message.Message):
    __slots__ = ("data_source_id", "id", "download_link")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_LINK_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    id: str
    download_link: str
    def __init__(self, data_source_id: _Optional[str] = ..., id: _Optional[str] = ..., download_link: _Optional[str] = ...) -> None: ...
