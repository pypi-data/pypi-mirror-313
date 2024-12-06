from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
import analysis_pb2 as _analysis_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from analysis_pb2 import AnalysisAlgorithmNode as AnalysisAlgorithmNode
from analysis_pb2 import AnalysisCreateRequest as AnalysisCreateRequest
from analysis_pb2 import AnalysisCreateResponse as AnalysisCreateResponse
from analysis_pb2 import AnalysisAlgorithmConfigNode as AnalysisAlgorithmConfigNode
from analysis_pb2 import AnalysisGetRequest as AnalysisGetRequest
from analysis_pb2 import Analysis as Analysis
from analysis_pb2 import AnalysisGetResponse as AnalysisGetResponse
from analysis_pb2 import AnalysisListRequest as AnalysisListRequest
from analysis_pb2 import AnalysisListResponse as AnalysisListResponse

DESCRIPTOR: _descriptor.FileDescriptor

class AnalysisComputationCreateRequest(_message.Message):
    __slots__ = ("analysis_config_id", "toi_id", "aoi_collection_id")
    ANALYSIS_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    analysis_config_id: str
    toi_id: str
    aoi_collection_id: str
    def __init__(self, analysis_config_id: _Optional[str] = ..., toi_id: _Optional[str] = ..., aoi_collection_id: _Optional[str] = ...) -> None: ...

class AnalysisComputationCreateResponse(_message.Message):
    __slots__ = ("status_code", "analysis_computation")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_computation: AnalysisComputation
    def __init__(self, status_code: _Optional[int] = ..., analysis_computation: _Optional[_Union[AnalysisComputation, _Mapping]] = ...) -> None: ...

class AnalysisComputationRunRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AnalysisComputationRunResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AnalysisComputationGetRequest(_message.Message):
    __slots__ = ("ids", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisComputationNode(_message.Message):
    __slots__ = ("name", "computation_id", "children", "has_results")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    HAS_RESULTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    computation_id: str
    children: _containers.RepeatedScalarFieldContainer[str]
    has_results: bool
    def __init__(self, name: _Optional[str] = ..., computation_id: _Optional[str] = ..., children: _Optional[_Iterable[str]] = ..., has_results: bool = ...) -> None: ...

class AnalysisComputation(_message.Message):
    __slots__ = ("id", "analysis_id", "toi_id", "aoi_collection_id", "analysis_config_id", "submitted_on", "state", "computation_nodes", "progress")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_STATE: _ClassVar[AnalysisComputation.State]
        NOT_STARTED: _ClassVar[AnalysisComputation.State]
        IN_PROGRESS: _ClassVar[AnalysisComputation.State]
        PAUSED: _ClassVar[AnalysisComputation.State]
        COMPLETE: _ClassVar[AnalysisComputation.State]
    UNKNOWN_STATE: AnalysisComputation.State
    NOT_STARTED: AnalysisComputation.State
    IN_PROGRESS: AnalysisComputation.State
    PAUSED: AnalysisComputation.State
    COMPLETE: AnalysisComputation.State
    class Progress(_message.Message):
        __slots__ = ("running", "succeeded", "failed")
        RUNNING_FIELD_NUMBER: _ClassVar[int]
        SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
        FAILED_FIELD_NUMBER: _ClassVar[int]
        running: float
        succeeded: float
        failed: float
        def __init__(self, running: _Optional[float] = ..., succeeded: _Optional[float] = ..., failed: _Optional[float] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_ID_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_ON_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_NODES_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    id: str
    analysis_id: str
    toi_id: str
    aoi_collection_id: str
    analysis_config_id: str
    submitted_on: _timestamp_pb2.Timestamp
    state: AnalysisComputation.State
    computation_nodes: _containers.RepeatedCompositeFieldContainer[AnalysisComputationNode]
    progress: AnalysisComputation.Progress
    def __init__(self, id: _Optional[str] = ..., analysis_id: _Optional[str] = ..., toi_id: _Optional[str] = ..., aoi_collection_id: _Optional[str] = ..., analysis_config_id: _Optional[str] = ..., submitted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[_Union[AnalysisComputation.State, str]] = ..., computation_nodes: _Optional[_Iterable[_Union[AnalysisComputationNode, _Mapping]]] = ..., progress: _Optional[_Union[AnalysisComputation.Progress, _Mapping]] = ...) -> None: ...

class AnalysisComputationGetResponse(_message.Message):
    __slots__ = ("status_code", "analysis_computations", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_computations: _containers.RepeatedCompositeFieldContainer[AnalysisComputation]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analysis_computations: _Optional[_Iterable[_Union[AnalysisComputation, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisComputationListRequest(_message.Message):
    __slots__ = ("state", "status", "min_submitted_on", "max_submitted_on", "analysis_config_id", "toi_id", "aoi_collection_id", "analysis_id", "pagination")
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MIN_SUBMITTED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_SUBMITTED_ON_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    state: str
    status: str
    min_submitted_on: _timestamp_pb2.Timestamp
    max_submitted_on: _timestamp_pb2.Timestamp
    analysis_config_id: str
    toi_id: str
    aoi_collection_id: str
    analysis_id: str
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, state: _Optional[str] = ..., status: _Optional[str] = ..., min_submitted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_submitted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., analysis_config_id: _Optional[str] = ..., toi_id: _Optional[str] = ..., aoi_collection_id: _Optional[str] = ..., analysis_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisComputationListResponse(_message.Message):
    __slots__ = ("status_code", "analysis_computations", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_computations: _containers.RepeatedCompositeFieldContainer[AnalysisComputation]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analysis_computations: _Optional[_Iterable[_Union[AnalysisComputation, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...
