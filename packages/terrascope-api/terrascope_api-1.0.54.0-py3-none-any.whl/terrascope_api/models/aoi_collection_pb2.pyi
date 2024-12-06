import common_models_pb2 as _common_models_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class AOICollection(_message.Message):
    __slots__ = ("id", "name", "created_on", "user_id", "num_aois")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_AOIS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_on: _timestamp_pb2.Timestamp
    user_id: str
    num_aois: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_id: _Optional[str] = ..., num_aois: _Optional[int] = ...) -> None: ...

class AOIInfo(_message.Message):
    __slots__ = ("aoi_id", "aoi_version_id", "aoi_name", "lat", "long", "area_km2", "geom", "timezone")
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_NAME_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    AREA_KM2_FIELD_NUMBER: _ClassVar[int]
    GEOM_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    aoi_id: str
    aoi_version_id: str
    aoi_name: str
    lat: float
    long: float
    area_km2: float
    geom: str
    timezone: str
    def __init__(self, aoi_id: _Optional[str] = ..., aoi_version_id: _Optional[str] = ..., aoi_name: _Optional[str] = ..., lat: _Optional[float] = ..., long: _Optional[float] = ..., area_km2: _Optional[float] = ..., geom: _Optional[str] = ..., timezone: _Optional[str] = ...) -> None: ...

class AOICollectionCreateRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class AOICollectionCreateResponse(_message.Message):
    __slots__ = ("status_code", "aoi_collection")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_collection: AOICollection
    def __init__(self, status_code: _Optional[int] = ..., aoi_collection: _Optional[_Union[AOICollection, _Mapping]] = ...) -> None: ...

class AOICollectionGetRequest(_message.Message):
    __slots__ = ("id", "verbose", "pagination")
    ID_FIELD_NUMBER: _ClassVar[int]
    VERBOSE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    verbose: bool
    pagination: _common_models_pb2.Pagination
    def __init__(self, id: _Optional[str] = ..., verbose: bool = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AOICollectionGetResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_info")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_INFO_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2.Pagination
    aoi_info: _containers.RepeatedCompositeFieldContainer[AOIInfo]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., aoi_info: _Optional[_Iterable[_Union[AOIInfo, _Mapping]]] = ...) -> None: ...

class AOICollectionAddRequest(_message.Message):
    __slots__ = ("id", "aoi_version_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSION_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    aoi_version_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[str] = ..., aoi_version_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class AOICollectionAddResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AOICollectionRemoveRequest(_message.Message):
    __slots__ = ("id", "aoi_version_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSION_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    aoi_version_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[str] = ..., aoi_version_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class AOICollectionRemoveResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AOICollectionCloneRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class AOICollectionCloneResponse(_message.Message):
    __slots__ = ("status_code", "aoi_collection_id")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_collection_id: str
    def __init__(self, status_code: _Optional[int] = ..., aoi_collection_id: _Optional[str] = ...) -> None: ...

class AOICollectionListRequest(_message.Message):
    __slots__ = ("pagination", "min_created_on", "max_created_on", "search_text")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2.Pagination
    min_created_on: _timestamp_pb2.Timestamp
    max_created_on: _timestamp_pb2.Timestamp
    search_text: str
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., min_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., search_text: _Optional[str] = ...) -> None: ...

class AOICollectionListResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_collections")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2.Pagination
    aoi_collections: _containers.RepeatedCompositeFieldContainer[AOICollection]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., aoi_collections: _Optional[_Iterable[_Union[AOICollection, _Mapping]]] = ...) -> None: ...
