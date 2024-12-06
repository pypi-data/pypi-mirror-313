from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class AlgorithmComputationExecution(_message.Message):
    __slots__ = ("id", "computation_id", "start_ts", "finish_ts", "partial_results", "status", "created_on", "validation_details", "input_ids")
    class AlgorithmComputationExecutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        NEW: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        PERMISSION_CHECKING: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        PERMISSION_CHECK_SUCCEEDED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        PERMISSION_CHECK_FAILED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        VALIDATING: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        VALIDATION_SUCCEEDED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        VALIDATION_FAILED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        RUNNING: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        SUCCEEDED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        FAILED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        STOPPED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        CANCELLED: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
        RETRYING: _ClassVar[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus]
    UNKNOWN: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    NEW: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    PERMISSION_CHECKING: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    PERMISSION_CHECK_SUCCEEDED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    PERMISSION_CHECK_FAILED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    VALIDATING: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    VALIDATION_SUCCEEDED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    VALIDATION_FAILED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    RUNNING: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    SUCCEEDED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    FAILED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    STOPPED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    CANCELLED: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    RETRYING: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    START_TS_FIELD_NUMBER: _ClassVar[int]
    FINISH_TS_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_RESULTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    INPUT_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    computation_id: str
    start_ts: _timestamp_pb2.Timestamp
    finish_ts: _timestamp_pb2.Timestamp
    partial_results: bool
    status: AlgorithmComputationExecution.AlgorithmComputationExecutionStatus
    created_on: _timestamp_pb2.Timestamp
    validation_details: _struct_pb2.Struct
    input_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., computation_id: _Optional[str] = ..., start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., finish_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., partial_results: bool = ..., status: _Optional[_Union[AlgorithmComputationExecution.AlgorithmComputationExecutionStatus, str]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., validation_details: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., input_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmComputationExecutionGetRequest(_message.Message):
    __slots__ = ("ids", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    pagination: _common_models_pb2.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmComputationExecutionGetResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_computation_executions", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_EXECUTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_computation_executions: _containers.RepeatedCompositeFieldContainer[AlgorithmComputationExecution]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithm_computation_executions: _Optional[_Iterable[_Union[AlgorithmComputationExecution, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...
