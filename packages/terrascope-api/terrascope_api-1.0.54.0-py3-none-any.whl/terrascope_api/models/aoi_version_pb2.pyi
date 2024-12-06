import common_models_pb2 as _common_models_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import aoi_pb2 as _aoi_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from aoi_pb2 import AOITransaction as AOITransaction
from aoi_pb2 import AOIIdentifier as AOIIdentifier
from aoi_pb2 import AOIObject as AOIObject
from aoi_pb2 import AOIVersion as AOIVersion
from aoi_pb2 import AOIInput as AOIInput
from aoi_pb2 import AOICreateRequest as AOICreateRequest
from aoi_pb2 import AOICreateResponse as AOICreateResponse
from aoi_pb2 import AOIUploadRequest as AOIUploadRequest
from aoi_pb2 import AOIUploadResponse as AOIUploadResponse
from aoi_pb2 import AOIGetRequest as AOIGetRequest
from aoi_pb2 import AOIGetResponse as AOIGetResponse
from aoi_pb2 import AOIUpdateRequest as AOIUpdateRequest
from aoi_pb2 import AOIUpdateResponse as AOIUpdateResponse

DESCRIPTOR: _descriptor.FileDescriptor

class AOIField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_AOI_FIELD: _ClassVar[AOIField]
    AOI_ID: _ClassVar[AOIField]
    GEOM_WKT: _ClassVar[AOIField]
    LAT: _ClassVar[AOIField]
    LONG: _ClassVar[AOIField]
    NAME: _ClassVar[AOIField]
    AREA_KM2: _ClassVar[AOIField]
    CATEGORY: _ClassVar[AOIField]
    TYPE: _ClassVar[AOIField]
    SOURCE: _ClassVar[AOIField]
    COUNTRY: _ClassVar[AOIField]
    STATE: _ClassVar[AOIField]
    TAGS: _ClassVar[AOIField]
    ATTRIBUTES: _ClassVar[AOIField]
    TIMEZONE: _ClassVar[AOIField]
    CREATED_ON: _ClassVar[AOIField]
    CREATED_BY: _ClassVar[AOIField]
UNKNOWN_AOI_FIELD: AOIField
AOI_ID: AOIField
GEOM_WKT: AOIField
LAT: AOIField
LONG: AOIField
NAME: AOIField
AREA_KM2: AOIField
CATEGORY: AOIField
TYPE: AOIField
SOURCE: AOIField
COUNTRY: AOIField
STATE: AOIField
TAGS: AOIField
ATTRIBUTES: AOIField
TIMEZONE: AOIField
CREATED_ON: AOIField
CREATED_BY: AOIField

class AOIVersionGetRequest(_message.Message):
    __slots__ = ("ids", "aoi_fields", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    AOI_FIELDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    aoi_fields: _containers.RepeatedScalarFieldContainer[AOIField]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., aoi_fields: _Optional[_Iterable[_Union[AOIField, str]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AOIVersionGetResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_versions")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2_1.Pagination
    aoi_versions: _containers.RepeatedCompositeFieldContainer[_aoi_pb2.AOIVersion]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., aoi_versions: _Optional[_Iterable[_Union[_aoi_pb2.AOIVersion, _Mapping]]] = ...) -> None: ...

class AOIVersionCreateRequest(_message.Message):
    __slots__ = ("aoi_id", "aoi_modification_input")
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_MODIFICATION_INPUT_FIELD_NUMBER: _ClassVar[int]
    aoi_id: str
    aoi_modification_input: _aoi_pb2.AOIInput
    def __init__(self, aoi_id: _Optional[str] = ..., aoi_modification_input: _Optional[_Union[_aoi_pb2.AOIInput, _Mapping]] = ...) -> None: ...

class AOIVersionCreateResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_version")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2_1.Pagination
    aoi_version: _aoi_pb2.AOIVersion
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., aoi_version: _Optional[_Union[_aoi_pb2.AOIVersion, _Mapping]] = ...) -> None: ...

class AOIVersionListRequest(_message.Message):
    __slots__ = ("geom_wkt", "category", "tags", "search_text", "min_created_on", "max_created_on", "aoi_fields", "pagination", "verbose", "bbox", "sort_keys", "sort_order", "aoi_type", "country", "state", "min_area", "max_area", "data_sources", "library_type")
    class LibraryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_LIBRARY_TYPE: _ClassVar[AOIVersionListRequest.LibraryType]
        PRIVATE: _ClassVar[AOIVersionListRequest.LibraryType]
        PUBLIC: _ClassVar[AOIVersionListRequest.LibraryType]
    UNKNOWN_LIBRARY_TYPE: AOIVersionListRequest.LibraryType
    PRIVATE: AOIVersionListRequest.LibraryType
    PUBLIC: AOIVersionListRequest.LibraryType
    class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_SORT_ORDER: _ClassVar[AOIVersionListRequest.SortOrder]
        ASC: _ClassVar[AOIVersionListRequest.SortOrder]
        DESC: _ClassVar[AOIVersionListRequest.SortOrder]
    UNKNOWN_SORT_ORDER: AOIVersionListRequest.SortOrder
    ASC: AOIVersionListRequest.SortOrder
    DESC: AOIVersionListRequest.SortOrder
    GEOM_WKT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    AOI_FIELDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    VERBOSE_FIELD_NUMBER: _ClassVar[int]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    SORT_KEYS_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    AOI_TYPE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MIN_AREA_FIELD_NUMBER: _ClassVar[int]
    MAX_AREA_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_TYPE_FIELD_NUMBER: _ClassVar[int]
    geom_wkt: str
    category: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    search_text: str
    min_created_on: _timestamp_pb2.Timestamp
    max_created_on: _timestamp_pb2.Timestamp
    aoi_fields: _containers.RepeatedScalarFieldContainer[AOIField]
    pagination: _common_models_pb2_1.Pagination
    verbose: bool
    bbox: _containers.RepeatedScalarFieldContainer[float]
    sort_keys: AOIField
    sort_order: AOIVersionListRequest.SortOrder
    aoi_type: str
    country: str
    state: str
    min_area: float
    max_area: float
    data_sources: _containers.RepeatedScalarFieldContainer[str]
    library_type: AOIVersionListRequest.LibraryType
    def __init__(self, geom_wkt: _Optional[str] = ..., category: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., search_text: _Optional[str] = ..., min_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., aoi_fields: _Optional[_Iterable[_Union[AOIField, str]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., verbose: bool = ..., bbox: _Optional[_Iterable[float]] = ..., sort_keys: _Optional[_Union[AOIField, str]] = ..., sort_order: _Optional[_Union[AOIVersionListRequest.SortOrder, str]] = ..., aoi_type: _Optional[str] = ..., country: _Optional[str] = ..., state: _Optional[str] = ..., min_area: _Optional[float] = ..., max_area: _Optional[float] = ..., data_sources: _Optional[_Iterable[str]] = ..., library_type: _Optional[_Union[AOIVersionListRequest.LibraryType, str]] = ...) -> None: ...

class AOIVersionListResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_versions")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2_1.Pagination
    aoi_versions: _containers.RepeatedCompositeFieldContainer[_aoi_pb2.AOIVersion]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., aoi_versions: _Optional[_Iterable[_Union[_aoi_pb2.AOIVersion, _Mapping]]] = ...) -> None: ...
