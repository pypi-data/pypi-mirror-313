from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
import common_models_pb2 as _common_models_pb2
import aoi_pb2 as _aoi_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
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

class ImagerySearchRequest(_message.Message):
    __slots__ = ("aoi_id", "geometry_wkb", "toi_id", "time_range", "data_source_id", "product_spec_name", "data_source_filters", "pagination", "sampling_config")
    class SamplingConfig(_message.Message):
        __slots__ = ("frequency_hours", "tolerance_hours")
        FREQUENCY_HOURS_FIELD_NUMBER: _ClassVar[int]
        TOLERANCE_HOURS_FIELD_NUMBER: _ClassVar[int]
        frequency_hours: int
        tolerance_hours: int
        def __init__(self, frequency_hours: _Optional[int] = ..., tolerance_hours: _Optional[int] = ...) -> None: ...
    class TimeRange(_message.Message):
        __slots__ = ("start_utc", "finish_utc")
        START_UTC_FIELD_NUMBER: _ClassVar[int]
        FINISH_UTC_FIELD_NUMBER: _ClassVar[int]
        start_utc: _timestamp_pb2.Timestamp
        finish_utc: _timestamp_pb2.Timestamp
        def __init__(self, start_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., finish_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_WKB_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_SPEC_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    aoi_id: _aoi_pb2.AOIIdentifier
    geometry_wkb: bytes
    toi_id: str
    time_range: ImagerySearchRequest.TimeRange
    data_source_id: str
    product_spec_name: str
    data_source_filters: _struct_pb2.Struct
    pagination: _common_models_pb2_1.Pagination
    sampling_config: ImagerySearchRequest.SamplingConfig
    def __init__(self, aoi_id: _Optional[_Union[_aoi_pb2.AOIIdentifier, _Mapping]] = ..., geometry_wkb: _Optional[bytes] = ..., toi_id: _Optional[str] = ..., time_range: _Optional[_Union[ImagerySearchRequest.TimeRange, _Mapping]] = ..., data_source_id: _Optional[str] = ..., product_spec_name: _Optional[str] = ..., data_source_filters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., sampling_config: _Optional[_Union[ImagerySearchRequest.SamplingConfig, _Mapping]] = ...) -> None: ...

class ImagerySearchResponse(_message.Message):
    __slots__ = ("status_code", "results", "pagination")
    class ImagerySearchResult(_message.Message):
        __slots__ = ("id", "provider_scene_id", "image_geom_wkb", "acquired_ts", "metadata")
        ID_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_SCENE_ID_FIELD_NUMBER: _ClassVar[int]
        IMAGE_GEOM_WKB_FIELD_NUMBER: _ClassVar[int]
        ACQUIRED_TS_FIELD_NUMBER: _ClassVar[int]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        id: str
        provider_scene_id: str
        image_geom_wkb: bytes
        acquired_ts: _timestamp_pb2.Timestamp
        metadata: _struct_pb2.Struct
        def __init__(self, id: _Optional[str] = ..., provider_scene_id: _Optional[str] = ..., image_geom_wkb: _Optional[bytes] = ..., acquired_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    results: _containers.RepeatedCompositeFieldContainer[ImagerySearchResponse.ImagerySearchResult]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., results: _Optional[_Iterable[_Union[ImagerySearchResponse.ImagerySearchResult, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...
