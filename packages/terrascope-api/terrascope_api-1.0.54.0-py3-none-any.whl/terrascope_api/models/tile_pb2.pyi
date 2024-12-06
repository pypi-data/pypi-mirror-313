from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class Bounds(_message.Message):
    __slots__ = ("x_min", "y_min", "x_max", "y_max")
    X_MIN_FIELD_NUMBER: _ClassVar[int]
    Y_MIN_FIELD_NUMBER: _ClassVar[int]
    X_MAX_FIELD_NUMBER: _ClassVar[int]
    Y_MAX_FIELD_NUMBER: _ClassVar[int]
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    def __init__(self, x_min: _Optional[float] = ..., y_min: _Optional[float] = ..., x_max: _Optional[float] = ..., y_max: _Optional[float] = ...) -> None: ...

class TileMatrix(_message.Message):
    __slots__ = ("id", "zoom")
    ID_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    id: str
    zoom: int
    def __init__(self, id: _Optional[str] = ..., zoom: _Optional[int] = ...) -> None: ...

class TileAccessInfo(_message.Message):
    __slots__ = ("url_template", "credentials")
    URL_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    url_template: str
    credentials: _struct_pb2.Struct
    def __init__(self, url_template: _Optional[str] = ..., credentials: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class TileSet(_message.Message):
    __slots__ = ("id", "name", "bounds", "matrices", "tile_access", "from_ts")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    MATRICES_FIELD_NUMBER: _ClassVar[int]
    TILE_ACCESS_FIELD_NUMBER: _ClassVar[int]
    FROM_TS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    bounds: Bounds
    matrices: _containers.RepeatedCompositeFieldContainer[TileMatrix]
    tile_access: TileAccessInfo
    from_ts: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., bounds: _Optional[_Union[Bounds, _Mapping]] = ..., matrices: _Optional[_Iterable[_Union[TileMatrix, _Mapping]]] = ..., tile_access: _Optional[_Union[TileAccessInfo, _Mapping]] = ..., from_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TileSetListRequest(_message.Message):
    __slots__ = ("search_id", "pagination", "tile_ts_from", "tile_ts_to")
    SEARCH_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    TILE_TS_FROM_FIELD_NUMBER: _ClassVar[int]
    TILE_TS_TO_FIELD_NUMBER: _ClassVar[int]
    search_id: str
    pagination: _common_models_pb2.Pagination
    tile_ts_from: _timestamp_pb2.Timestamp
    tile_ts_to: _timestamp_pb2.Timestamp
    def __init__(self, search_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., tile_ts_from: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., tile_ts_to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TileSetListResponse(_message.Message):
    __slots__ = ("tile_sets", "pagination")
    TILE_SETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    tile_sets: _containers.RepeatedCompositeFieldContainer[TileSet]
    pagination: _common_models_pb2.Pagination
    def __init__(self, tile_sets: _Optional[_Iterable[_Union[TileSet, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...
