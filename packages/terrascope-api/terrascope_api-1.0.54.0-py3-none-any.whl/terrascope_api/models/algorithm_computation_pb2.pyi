from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class AlgorithmComputation(_message.Message):
    __slots__ = ("id", "aoi_collection_id", "algo_config_id", "toi_id", "input_ids", "submitted_on", "state", "progress", "last_execution")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_STATE: _ClassVar[AlgorithmComputation.State]
        NOT_STARTED: _ClassVar[AlgorithmComputation.State]
        IN_PROGRESS: _ClassVar[AlgorithmComputation.State]
        PAUSED: _ClassVar[AlgorithmComputation.State]
        COMPLETE: _ClassVar[AlgorithmComputation.State]
    UNKNOWN_STATE: AlgorithmComputation.State
    NOT_STARTED: AlgorithmComputation.State
    IN_PROGRESS: AlgorithmComputation.State
    PAUSED: AlgorithmComputation.State
    COMPLETE: AlgorithmComputation.State
    class Progress(_message.Message):
        __slots__ = ("running", "succeeded", "failed", "no_data")
        RUNNING_FIELD_NUMBER: _ClassVar[int]
        SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
        FAILED_FIELD_NUMBER: _ClassVar[int]
        NO_DATA_FIELD_NUMBER: _ClassVar[int]
        running: float
        succeeded: float
        failed: float
        no_data: float
        def __init__(self, running: _Optional[float] = ..., succeeded: _Optional[float] = ..., failed: _Optional[float] = ..., no_data: _Optional[float] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ALGO_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_IDS_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_ON_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    aoi_collection_id: str
    algo_config_id: str
    toi_id: str
    input_ids: _containers.RepeatedScalarFieldContainer[str]
    submitted_on: _timestamp_pb2.Timestamp
    state: AlgorithmComputation.State
    progress: AlgorithmComputation.Progress
    last_execution: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., aoi_collection_id: _Optional[str] = ..., algo_config_id: _Optional[str] = ..., toi_id: _Optional[str] = ..., input_ids: _Optional[_Iterable[str]] = ..., submitted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[_Union[AlgorithmComputation.State, str]] = ..., progress: _Optional[_Union[AlgorithmComputation.Progress, _Mapping]] = ..., last_execution: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AlgorithmComputationCreateRequest(_message.Message):
    __slots__ = ("algorithm_config_id", "aoi_collection_id", "toi_id")
    ALGORITHM_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    algorithm_config_id: str
    aoi_collection_id: str
    toi_id: str
    def __init__(self, algorithm_config_id: _Optional[str] = ..., aoi_collection_id: _Optional[str] = ..., toi_id: _Optional[str] = ...) -> None: ...

class AlgorithmComputationCreateResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_computation")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_computation: AlgorithmComputation
    def __init__(self, status_code: _Optional[int] = ..., algorithm_computation: _Optional[_Union[AlgorithmComputation, _Mapping]] = ...) -> None: ...

class AlgorithmComputationRunRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmComputationRunResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AlgorithmComputationGetRequest(_message.Message):
    __slots__ = ("ids", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    pagination: _common_models_pb2.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmComputationGetResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_computations", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_computations: _containers.RepeatedCompositeFieldContainer[AlgorithmComputation]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithm_computations: _Optional[_Iterable[_Union[AlgorithmComputation, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmComputationListRequest(_message.Message):
    __slots__ = ("state", "min_submitted_on", "max_submitted_on", "algorithm_config_id", "toi_id", "aoi_collection_id", "pagination")
    STATE_FIELD_NUMBER: _ClassVar[int]
    MIN_SUBMITTED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_SUBMITTED_ON_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    TOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    state: AlgorithmComputation.State
    min_submitted_on: _timestamp_pb2.Timestamp
    max_submitted_on: _timestamp_pb2.Timestamp
    algorithm_config_id: str
    toi_id: str
    aoi_collection_id: str
    pagination: _common_models_pb2.Pagination
    def __init__(self, state: _Optional[_Union[AlgorithmComputation.State, str]] = ..., min_submitted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_submitted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., algorithm_config_id: _Optional[str] = ..., toi_id: _Optional[str] = ..., aoi_collection_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmComputationListResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_computations", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_computations: _containers.RepeatedCompositeFieldContainer[AlgorithmComputation]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithm_computations: _Optional[_Iterable[_Union[AlgorithmComputation, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...
