from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class CreditAddRequest(_message.Message):
    __slots__ = ("source_id", "amount", "reason")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    amount: float
    reason: str
    def __init__(self, source_id: _Optional[str] = ..., amount: _Optional[float] = ..., reason: _Optional[str] = ...) -> None: ...

class CreditAddResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class CreditRemoveRequest(_message.Message):
    __slots__ = ("source_id", "amount", "reason")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    amount: float
    reason: str
    def __init__(self, source_id: _Optional[str] = ..., amount: _Optional[float] = ..., reason: _Optional[str] = ...) -> None: ...

class CreditRemoveResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class CreditRefundRequest(_message.Message):
    __slots__ = ("source_id", "amount", "reason")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    amount: float
    reason: str
    def __init__(self, source_id: _Optional[str] = ..., amount: _Optional[float] = ..., reason: _Optional[str] = ...) -> None: ...

class CreditRefundResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class CreditAlgorithmMultiplierSetRequest(_message.Message):
    __slots__ = ("algorithm_version_id", "algorithm_execution_price", "algorithm_value_price")
    ALGORITHM_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_EXECUTION_PRICE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VALUE_PRICE_FIELD_NUMBER: _ClassVar[int]
    algorithm_version_id: str
    algorithm_execution_price: float
    algorithm_value_price: float
    def __init__(self, algorithm_version_id: _Optional[str] = ..., algorithm_execution_price: _Optional[float] = ..., algorithm_value_price: _Optional[float] = ...) -> None: ...

class CreditAlgorithmMultiplierSetResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class CreditDataSourceMultiplierSetRequest(_message.Message):
    __slots__ = ("data_source_id", "data_source_price")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_PRICE_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    data_source_price: float
    def __init__(self, data_source_id: _Optional[str] = ..., data_source_price: _Optional[float] = ...) -> None: ...

class CreditDataSourceMultiplierSetResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class CreditEstimateRequest(_message.Message):
    __slots__ = ("algorithm_computation_id", "analysis_computation_ids", "analysis_resources")
    class AnalysisResources(_message.Message):
        __slots__ = ("aoi_collection_ids", "analysis_config_ids", "start_ts", "end_ts")
        AOI_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
        ANALYSIS_CONFIG_IDS_FIELD_NUMBER: _ClassVar[int]
        START_TS_FIELD_NUMBER: _ClassVar[int]
        END_TS_FIELD_NUMBER: _ClassVar[int]
        aoi_collection_ids: _containers.RepeatedScalarFieldContainer[str]
        analysis_config_ids: _containers.RepeatedScalarFieldContainer[str]
        start_ts: _timestamp_pb2.Timestamp
        end_ts: _timestamp_pb2.Timestamp
        def __init__(self, aoi_collection_ids: _Optional[_Iterable[str]] = ..., analysis_config_ids: _Optional[_Iterable[str]] = ..., start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    ALGORITHM_COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    algorithm_computation_id: str
    analysis_computation_ids: _containers.RepeatedScalarFieldContainer[str]
    analysis_resources: CreditEstimateRequest.AnalysisResources
    def __init__(self, algorithm_computation_id: _Optional[str] = ..., analysis_computation_ids: _Optional[_Iterable[str]] = ..., analysis_resources: _Optional[_Union[CreditEstimateRequest.AnalysisResources, _Mapping]] = ...) -> None: ...

class CreditEstimateResponse(_message.Message):
    __slots__ = ("status_code", "credit_estimate", "msg")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    credit_estimate: float
    msg: str
    def __init__(self, status_code: _Optional[int] = ..., credit_estimate: _Optional[float] = ..., msg: _Optional[str] = ...) -> None: ...

class Credit(_message.Message):
    __slots__ = ("source_id", "available", "reserved", "used")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    available: float
    reserved: float
    used: float
    def __init__(self, source_id: _Optional[str] = ..., available: _Optional[float] = ..., reserved: _Optional[float] = ..., used: _Optional[float] = ...) -> None: ...

class CreditSummaryRequest(_message.Message):
    __slots__ = ("source_id",)
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    def __init__(self, source_id: _Optional[str] = ...) -> None: ...

class CreditSummaryResponse(_message.Message):
    __slots__ = ("status_code", "credit")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    credit: Credit
    def __init__(self, status_code: _Optional[int] = ..., credit: _Optional[_Union[Credit, _Mapping]] = ...) -> None: ...

class Transaction(_message.Message):
    __slots__ = ("id", "credit_source_id", "user_id", "transaction_type", "amount", "reason", "transacted_on", "credit_available", "credit_reserved", "credit_used", "algorithm_computation_id")
    class TransactionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_TRANSACTION_TYPE: _ClassVar[Transaction.TransactionType]
        ADD: _ClassVar[Transaction.TransactionType]
        REMOVE: _ClassVar[Transaction.TransactionType]
        REFUND: _ClassVar[Transaction.TransactionType]
        RESERVE: _ClassVar[Transaction.TransactionType]
        UNRESERVE: _ClassVar[Transaction.TransactionType]
        DEDUCT: _ClassVar[Transaction.TransactionType]
    UNKNOWN_TRANSACTION_TYPE: Transaction.TransactionType
    ADD: Transaction.TransactionType
    REMOVE: Transaction.TransactionType
    REFUND: Transaction.TransactionType
    RESERVE: Transaction.TransactionType
    UNRESERVE: Transaction.TransactionType
    DEDUCT: Transaction.TransactionType
    ID_FIELD_NUMBER: _ClassVar[int]
    CREDIT_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    TRANSACTED_ON_FIELD_NUMBER: _ClassVar[int]
    CREDIT_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_RESERVED_FIELD_NUMBER: _ClassVar[int]
    CREDIT_USED_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    credit_source_id: str
    user_id: str
    transaction_type: Transaction.TransactionType
    amount: float
    reason: str
    transacted_on: _timestamp_pb2.Timestamp
    credit_available: float
    credit_reserved: float
    credit_used: float
    algorithm_computation_id: str
    def __init__(self, id: _Optional[str] = ..., credit_source_id: _Optional[str] = ..., user_id: _Optional[str] = ..., transaction_type: _Optional[_Union[Transaction.TransactionType, str]] = ..., amount: _Optional[float] = ..., reason: _Optional[str] = ..., transacted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., credit_available: _Optional[float] = ..., credit_reserved: _Optional[float] = ..., credit_used: _Optional[float] = ..., algorithm_computation_id: _Optional[str] = ...) -> None: ...

class CreditTransactionsRequest(_message.Message):
    __slots__ = ("pagination", "source_id", "transaction_type", "min_transacted_on", "max_transacted_on", "algorithm_computation_id")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MIN_TRANSACTED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_TRANSACTED_ON_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2.Pagination
    source_id: str
    transaction_type: Transaction.TransactionType
    min_transacted_on: _timestamp_pb2.Timestamp
    max_transacted_on: _timestamp_pb2.Timestamp
    algorithm_computation_id: str
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., source_id: _Optional[str] = ..., transaction_type: _Optional[_Union[Transaction.TransactionType, str]] = ..., min_transacted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_transacted_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., algorithm_computation_id: _Optional[str] = ...) -> None: ...

class CreditTransactionsResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "transactions")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2.Pagination
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ...) -> None: ...
