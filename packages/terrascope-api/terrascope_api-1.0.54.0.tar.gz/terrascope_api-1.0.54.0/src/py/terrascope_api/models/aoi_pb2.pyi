from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class AOITransaction(_message.Message):
    __slots__ = ("id", "status", "created_on", "updated_on")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    created_on: _timestamp_pb2.Timestamp
    updated_on: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AOIIdentifier(_message.Message):
    __slots__ = ("aoi_id", "aoi_version_id")
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    aoi_id: str
    aoi_version_id: int
    def __init__(self, aoi_id: _Optional[str] = ..., aoi_version_id: _Optional[int] = ...) -> None: ...

class AOIObject(_message.Message):
    __slots__ = ("aoi_identifier", "geom_wkt", "lat", "long", "name", "area_km2", "category", "type", "source", "country", "state", "tags", "attributes", "timezone")
    AOI_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    GEOM_WKT_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AREA_KM2_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    aoi_identifier: AOIIdentifier
    geom_wkt: str
    lat: float
    long: float
    name: str
    area_km2: float
    category: str
    type: str
    source: str
    country: str
    state: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    attributes: _struct_pb2.Struct
    timezone: str
    def __init__(self, aoi_identifier: _Optional[_Union[AOIIdentifier, _Mapping]] = ..., geom_wkt: _Optional[str] = ..., lat: _Optional[float] = ..., long: _Optional[float] = ..., name: _Optional[str] = ..., area_km2: _Optional[float] = ..., category: _Optional[str] = ..., type: _Optional[str] = ..., source: _Optional[str] = ..., country: _Optional[str] = ..., state: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., timezone: _Optional[str] = ...) -> None: ...

class AOIVersion(_message.Message):
    __slots__ = ("id", "aoi_id", "creation_timestamp", "creator", "aoi_name", "geom_wkt", "lat", "long", "area_km2", "category", "type", "source", "country", "state", "tags", "attributes", "timezone")
    ID_FIELD_NUMBER: _ClassVar[int]
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    AOI_NAME_FIELD_NUMBER: _ClassVar[int]
    GEOM_WKT_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    AREA_KM2_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    id: int
    aoi_id: str
    creation_timestamp: _timestamp_pb2.Timestamp
    creator: str
    aoi_name: str
    geom_wkt: str
    lat: float
    long: float
    area_km2: float
    category: str
    type: str
    source: str
    country: str
    state: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    attributes: _struct_pb2.Struct
    timezone: str
    def __init__(self, id: _Optional[int] = ..., aoi_id: _Optional[str] = ..., creation_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., creator: _Optional[str] = ..., aoi_name: _Optional[str] = ..., geom_wkt: _Optional[str] = ..., lat: _Optional[float] = ..., long: _Optional[float] = ..., area_km2: _Optional[float] = ..., category: _Optional[str] = ..., type: _Optional[str] = ..., source: _Optional[str] = ..., country: _Optional[str] = ..., state: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., timezone: _Optional[str] = ...) -> None: ...

class AOIInput(_message.Message):
    __slots__ = ("aoi_id", "geom_wkt", "name", "category", "type", "tags", "attributes")
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    GEOM_WKT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    aoi_id: str
    geom_wkt: str
    name: str
    category: str
    type: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    attributes: _struct_pb2.Struct
    def __init__(self, aoi_id: _Optional[str] = ..., geom_wkt: _Optional[str] = ..., name: _Optional[str] = ..., category: _Optional[str] = ..., type: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class AOICreateRequest(_message.Message):
    __slots__ = ("aoi_inputs", "aoi_collection_id")
    AOI_INPUTS_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    aoi_inputs: _containers.RepeatedCompositeFieldContainer[AOIInput]
    aoi_collection_id: str
    def __init__(self, aoi_inputs: _Optional[_Iterable[_Union[AOIInput, _Mapping]]] = ..., aoi_collection_id: _Optional[str] = ...) -> None: ...

class AOICreateResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_identifiers", "area_km2")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    AREA_KM2_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2.Pagination
    aoi_identifiers: _containers.RepeatedCompositeFieldContainer[AOIIdentifier]
    area_km2: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., aoi_identifiers: _Optional[_Iterable[_Union[AOIIdentifier, _Mapping]]] = ..., area_km2: _Optional[_Iterable[float]] = ...) -> None: ...

class AOIUploadRequest(_message.Message):
    __slots__ = ("aoi_collection_id", "chunk")
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    aoi_collection_id: str
    chunk: bytes
    def __init__(self, aoi_collection_id: _Optional[str] = ..., chunk: _Optional[bytes] = ...) -> None: ...

class AOIUploadResponse(_message.Message):
    __slots__ = ("status_code", "aoi_transaction")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_transaction: AOITransaction
    def __init__(self, status_code: _Optional[int] = ..., aoi_transaction: _Optional[_Union[AOITransaction, _Mapping]] = ...) -> None: ...

class AOIGetRequest(_message.Message):
    __slots__ = ("ids", "verbose", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    VERBOSE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    verbose: bool
    pagination: _common_models_pb2.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., verbose: bool = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AOIGetResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_versions")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2.Pagination
    aoi_versions: _containers.RepeatedCompositeFieldContainer[AOIVersion]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., aoi_versions: _Optional[_Iterable[_Union[AOIVersion, _Mapping]]] = ...) -> None: ...

class AOIUpdateRequest(_message.Message):
    __slots__ = ("aoi_id", "aoi_modification_input")
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_MODIFICATION_INPUT_FIELD_NUMBER: _ClassVar[int]
    aoi_id: str
    aoi_modification_input: AOIInput
    def __init__(self, aoi_id: _Optional[str] = ..., aoi_modification_input: _Optional[_Union[AOIInput, _Mapping]] = ...) -> None: ...

class AOIUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
