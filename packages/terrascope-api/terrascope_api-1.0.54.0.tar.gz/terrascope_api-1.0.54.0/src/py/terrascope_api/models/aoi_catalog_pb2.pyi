from google.protobuf import struct_pb2 as _struct_pb2
import common_models_pb2 as _common_models_pb2
import aoi_collection_pb2 as _aoi_collection_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from aoi_collection_pb2 import AOICollection as AOICollection
from aoi_collection_pb2 import AOIInfo as AOIInfo
from aoi_collection_pb2 import AOICollectionCreateRequest as AOICollectionCreateRequest
from aoi_collection_pb2 import AOICollectionCreateResponse as AOICollectionCreateResponse
from aoi_collection_pb2 import AOICollectionGetRequest as AOICollectionGetRequest
from aoi_collection_pb2 import AOICollectionGetResponse as AOICollectionGetResponse
from aoi_collection_pb2 import AOICollectionAddRequest as AOICollectionAddRequest
from aoi_collection_pb2 import AOICollectionAddResponse as AOICollectionAddResponse
from aoi_collection_pb2 import AOICollectionRemoveRequest as AOICollectionRemoveRequest
from aoi_collection_pb2 import AOICollectionRemoveResponse as AOICollectionRemoveResponse
from aoi_collection_pb2 import AOICollectionCloneRequest as AOICollectionCloneRequest
from aoi_collection_pb2 import AOICollectionCloneResponse as AOICollectionCloneResponse
from aoi_collection_pb2 import AOICollectionListRequest as AOICollectionListRequest
from aoi_collection_pb2 import AOICollectionListResponse as AOICollectionListResponse

DESCRIPTOR: _descriptor.FileDescriptor

class LibraryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRIVATE: _ClassVar[LibraryType]
    PUBLIC: _ClassVar[LibraryType]
PRIVATE: LibraryType
PUBLIC: LibraryType

class AOIStats(_message.Message):
    __slots__ = ("categories", "countries", "sources", "states", "tags", "types")
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    COUNTRIES_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    categories: _struct_pb2.Struct
    countries: _struct_pb2.Struct
    sources: _struct_pb2.Struct
    states: _struct_pb2.Struct
    tags: _struct_pb2.Struct
    types: _struct_pb2.Struct
    def __init__(self, categories: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., countries: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., sources: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., states: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., tags: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., types: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class AOIStatsGetRequest(_message.Message):
    __slots__ = ("bbox", "category", "type", "tags", "search_text", "country", "state", "min_area", "max_area", "sources", "library_type")
    BBOX_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MIN_AREA_FIELD_NUMBER: _ClassVar[int]
    MAX_AREA_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_TYPE_FIELD_NUMBER: _ClassVar[int]
    bbox: _containers.RepeatedScalarFieldContainer[float]
    category: str
    type: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    search_text: str
    country: str
    state: str
    min_area: float
    max_area: float
    sources: _containers.RepeatedScalarFieldContainer[str]
    library_type: LibraryType
    def __init__(self, bbox: _Optional[_Iterable[float]] = ..., category: _Optional[str] = ..., type: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., search_text: _Optional[str] = ..., country: _Optional[str] = ..., state: _Optional[str] = ..., min_area: _Optional[float] = ..., max_area: _Optional[float] = ..., sources: _Optional[_Iterable[str]] = ..., library_type: _Optional[_Union[LibraryType, str]] = ...) -> None: ...

class AOIStatsGetResponse(_message.Message):
    __slots__ = ("status_code", "aoi_stats")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_STATS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_stats: AOIStats
    def __init__(self, status_code: _Optional[int] = ..., aoi_stats: _Optional[_Union[AOIStats, _Mapping]] = ...) -> None: ...

class AOICluster(_message.Message):
    __slots__ = ("lat", "long", "count")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    lat: float
    long: float
    count: int
    def __init__(self, lat: _Optional[float] = ..., long: _Optional[float] = ..., count: _Optional[int] = ...) -> None: ...

class AOIClusterGetRequest(_message.Message):
    __slots__ = ("bbox", "category", "type", "tags", "search_text", "country", "state", "min_area", "max_area", "sources", "library_type")
    BBOX_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MIN_AREA_FIELD_NUMBER: _ClassVar[int]
    MAX_AREA_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_TYPE_FIELD_NUMBER: _ClassVar[int]
    bbox: _containers.RepeatedScalarFieldContainer[float]
    category: str
    type: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    search_text: str
    country: str
    state: str
    min_area: float
    max_area: float
    sources: _containers.RepeatedScalarFieldContainer[str]
    library_type: LibraryType
    def __init__(self, bbox: _Optional[_Iterable[float]] = ..., category: _Optional[str] = ..., type: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., search_text: _Optional[str] = ..., country: _Optional[str] = ..., state: _Optional[str] = ..., min_area: _Optional[float] = ..., max_area: _Optional[float] = ..., sources: _Optional[_Iterable[str]] = ..., library_type: _Optional[_Union[LibraryType, str]] = ...) -> None: ...

class AOIClusterGetResponse(_message.Message):
    __slots__ = ("status_code", "aoi_clusters")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_clusters: _containers.RepeatedCompositeFieldContainer[AOICluster]
    def __init__(self, status_code: _Optional[int] = ..., aoi_clusters: _Optional[_Iterable[_Union[AOICluster, _Mapping]]] = ...) -> None: ...

class AOICatalogAddRequest(_message.Message):
    __slots__ = ("aoi_ids",)
    AOI_IDS_FIELD_NUMBER: _ClassVar[int]
    aoi_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, aoi_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AOICatalogAddResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AOICatalogDeleteRequest(_message.Message):
    __slots__ = ("aoi_ids",)
    AOI_IDS_FIELD_NUMBER: _ClassVar[int]
    aoi_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, aoi_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AOICatalogDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AOICatalogGetPrivateCatalogRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AOICatalogGetPrivateCatalogResponse(_message.Message):
    __slots__ = ("user_collection",)
    USER_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    user_collection: _aoi_collection_pb2.AOICollection
    def __init__(self, user_collection: _Optional[_Union[_aoi_collection_pb2.AOICollection, _Mapping]] = ...) -> None: ...
