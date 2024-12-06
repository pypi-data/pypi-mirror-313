from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
import toi_pb2 as _toi_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from toi_pb2 import Cadence as Cadence
from toi_pb2 import Recurrence as Recurrence
from toi_pb2 import TOI as TOI
from toi_pb2 import TOICreateRequest as TOICreateRequest
from toi_pb2 import TOICreateResponse as TOICreateResponse
from toi_pb2 import TOIDeleteRequest as TOIDeleteRequest
from toi_pb2 import TOIDeleteResponse as TOIDeleteResponse
from toi_pb2 import TOIGetRequest as TOIGetRequest
from toi_pb2 import TOIGetResponse as TOIGetResponse
from toi_pb2 import TOIListRequest as TOIListRequest
from toi_pb2 import TOIListResponse as TOIListResponse

DESCRIPTOR: _descriptor.FileDescriptor

class ExportFile(_message.Message):
    __slots__ = ("url", "file_size_bytes")
    URL_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    url: str
    file_size_bytes: int
    def __init__(self, url: _Optional[str] = ..., file_size_bytes: _Optional[int] = ...) -> None: ...

class ExportCredentials(_message.Message):
    __slots__ = ("credentials", "base_url_template")
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    credentials: _struct_pb2.Struct
    base_url_template: str
    def __init__(self, credentials: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., base_url_template: _Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ("id", "created_on", "source_aoi_version", "dest_aoi_version", "algo_config_class", "algo_config_subclass", "observations", "data_type", "algorithm_computation_id", "artifact_credentials")
    class Observation(_message.Message):
        __slots__ = ("id", "data_view_id", "created_on", "start_ts", "end_ts", "value", "status", "measurements", "export_file")
        class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            UNKNOWN_STATUS: _ClassVar[Result.Observation.Status]
            COMPLETE: _ClassVar[Result.Observation.Status]
            PARTIAL: _ClassVar[Result.Observation.Status]
        UNKNOWN_STATUS: Result.Observation.Status
        COMPLETE: Result.Observation.Status
        PARTIAL: Result.Observation.Status
        class Measurement(_message.Message):
            __slots__ = ("id", "dimensions", "artifact_path")
            ID_FIELD_NUMBER: _ClassVar[int]
            DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
            ARTIFACT_PATH_FIELD_NUMBER: _ClassVar[int]
            id: str
            dimensions: _struct_pb2.Struct
            artifact_path: str
            def __init__(self, id: _Optional[str] = ..., dimensions: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., artifact_path: _Optional[str] = ...) -> None: ...
        ID_FIELD_NUMBER: _ClassVar[int]
        DATA_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
        CREATED_ON_FIELD_NUMBER: _ClassVar[int]
        START_TS_FIELD_NUMBER: _ClassVar[int]
        END_TS_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
        EXPORT_FILE_FIELD_NUMBER: _ClassVar[int]
        id: str
        data_view_id: str
        created_on: _timestamp_pb2.Timestamp
        start_ts: _timestamp_pb2.Timestamp
        end_ts: _timestamp_pb2.Timestamp
        value: _struct_pb2.Struct
        status: Result.Observation.Status
        measurements: _containers.RepeatedCompositeFieldContainer[Result.Observation.Measurement]
        export_file: ExportFile
        def __init__(self, id: _Optional[str] = ..., data_view_id: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., status: _Optional[_Union[Result.Observation.Status, str]] = ..., measurements: _Optional[_Iterable[_Union[Result.Observation.Measurement, _Mapping]]] = ..., export_file: _Optional[_Union[ExportFile, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    SOURCE_AOI_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEST_AOI_VERSION_FIELD_NUMBER: _ClassVar[int]
    ALGO_CONFIG_CLASS_FIELD_NUMBER: _ClassVar[int]
    ALGO_CONFIG_SUBCLASS_FIELD_NUMBER: _ClassVar[int]
    OBSERVATIONS_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    id: str
    created_on: _timestamp_pb2.Timestamp
    source_aoi_version: int
    dest_aoi_version: int
    algo_config_class: str
    algo_config_subclass: str
    observations: _containers.RepeatedCompositeFieldContainer[Result.Observation]
    data_type: str
    algorithm_computation_id: str
    artifact_credentials: ExportCredentials
    def __init__(self, id: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., source_aoi_version: _Optional[int] = ..., dest_aoi_version: _Optional[int] = ..., algo_config_class: _Optional[str] = ..., algo_config_subclass: _Optional[str] = ..., observations: _Optional[_Iterable[_Union[Result.Observation, _Mapping]]] = ..., data_type: _Optional[str] = ..., algorithm_computation_id: _Optional[str] = ..., artifact_credentials: _Optional[_Union[ExportCredentials, _Mapping]] = ...) -> None: ...

class ResultGetRequest(_message.Message):
    __slots__ = ("source_aoi_version", "dest_aoi_version", "algo_config_class", "algo_config_subclass", "created_on", "observation_start_ts", "max_observation_start_ts", "observation_status", "data_type", "pagination", "algorithm_computation_ids", "analysis_computation_ids", "include_export_files")
    SOURCE_AOI_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEST_AOI_VERSION_FIELD_NUMBER: _ClassVar[int]
    ALGO_CONFIG_CLASS_FIELD_NUMBER: _ClassVar[int]
    ALGO_CONFIG_SUBCLASS_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    OBSERVATION_START_TS_FIELD_NUMBER: _ClassVar[int]
    MAX_OBSERVATION_START_TS_FIELD_NUMBER: _ClassVar[int]
    OBSERVATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EXPORT_FILES_FIELD_NUMBER: _ClassVar[int]
    source_aoi_version: int
    dest_aoi_version: int
    algo_config_class: str
    algo_config_subclass: str
    created_on: _timestamp_pb2.Timestamp
    observation_start_ts: _timestamp_pb2.Timestamp
    max_observation_start_ts: _timestamp_pb2.Timestamp
    observation_status: Result.Observation.Status
    data_type: str
    pagination: _common_models_pb2_1.Pagination
    algorithm_computation_ids: _containers.RepeatedScalarFieldContainer[str]
    analysis_computation_ids: _containers.RepeatedScalarFieldContainer[str]
    include_export_files: bool
    def __init__(self, source_aoi_version: _Optional[int] = ..., dest_aoi_version: _Optional[int] = ..., algo_config_class: _Optional[str] = ..., algo_config_subclass: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., observation_start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_observation_start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., observation_status: _Optional[_Union[Result.Observation.Status, str]] = ..., data_type: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., algorithm_computation_ids: _Optional[_Iterable[str]] = ..., analysis_computation_ids: _Optional[_Iterable[str]] = ..., include_export_files: bool = ...) -> None: ...

class ResultGetResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "results", "export_credentials")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2_1.Pagination
    results: _containers.RepeatedCompositeFieldContainer[Result]
    export_credentials: ExportCredentials
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., results: _Optional[_Iterable[_Union[Result, _Mapping]]] = ..., export_credentials: _Optional[_Union[ExportCredentials, _Mapping]] = ...) -> None: ...
