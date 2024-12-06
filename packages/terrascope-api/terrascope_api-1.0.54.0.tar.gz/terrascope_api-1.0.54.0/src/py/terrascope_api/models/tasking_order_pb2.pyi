from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import order_recommendation_pb2 as _order_recommendation_pb2
import order_pb2 as _order_pb2
import order_recommendation_pb2 as _order_recommendation_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from order_recommendation_pb2 import OrderRecommendation as OrderRecommendation
from order_recommendation_pb2 import OrderRecommendationCreateRequest as OrderRecommendationCreateRequest
from order_recommendation_pb2 import OrderRecommendationCreateResponse as OrderRecommendationCreateResponse
from order_recommendation_pb2 import OrderRecommendationUpdateRequest as OrderRecommendationUpdateRequest
from order_recommendation_pb2 import OrderRecommendationUpdateResponse as OrderRecommendationUpdateResponse
from order_recommendation_pb2 import OrderRecommendationDeleteRequest as OrderRecommendationDeleteRequest
from order_recommendation_pb2 import OrderRecommendationDeleteResponse as OrderRecommendationDeleteResponse

DESCRIPTOR: _descriptor.FileDescriptor

class TimeRange(_message.Message):
    __slots__ = ("start_utc", "finish_utc")
    START_UTC_FIELD_NUMBER: _ClassVar[int]
    FINISH_UTC_FIELD_NUMBER: _ClassVar[int]
    start_utc: _timestamp_pb2.Timestamp
    finish_utc: _timestamp_pb2.Timestamp
    def __init__(self, start_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., finish_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TaskingOrder(_message.Message):
    __slots__ = ("id", "data_source_id", "target_geom", "acq_window", "product_spec_name", "state", "details", "url", "metadata", "creator", "created_on", "updated_on", "approved_by", "approval_comment", "recommendations")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_GEOM_FIELD_NUMBER: _ClassVar[int]
    ACQ_WINDOW_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_SPEC_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
    APPROVED_BY_FIELD_NUMBER: _ClassVar[int]
    APPROVAL_COMMENT_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDATIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    data_source_id: str
    target_geom: bytes
    acq_window: TimeRange
    product_spec_name: str
    state: _order_pb2.OrderState
    details: str
    url: str
    metadata: _struct_pb2.Struct
    creator: str
    created_on: _timestamp_pb2.Timestamp
    updated_on: _timestamp_pb2.Timestamp
    approved_by: str
    approval_comment: str
    recommendations: _containers.RepeatedCompositeFieldContainer[_order_recommendation_pb2_1.OrderRecommendation]
    def __init__(self, id: _Optional[str] = ..., data_source_id: _Optional[str] = ..., target_geom: _Optional[bytes] = ..., acq_window: _Optional[_Union[TimeRange, _Mapping]] = ..., product_spec_name: _Optional[str] = ..., state: _Optional[_Union[_order_pb2.OrderState, str]] = ..., details: _Optional[str] = ..., url: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., creator: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., approved_by: _Optional[str] = ..., approval_comment: _Optional[str] = ..., recommendations: _Optional[_Iterable[_Union[_order_recommendation_pb2_1.OrderRecommendation, _Mapping]]] = ...) -> None: ...

class TaskingOrderListRequest(_message.Message):
    __slots__ = ("states", "data_source_ids", "analysis_computation_ids", "algorithm_computation_ids")
    STATES_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedScalarFieldContainer[_order_pb2.OrderState]
    data_source_ids: _containers.RepeatedScalarFieldContainer[str]
    analysis_computation_ids: _containers.RepeatedScalarFieldContainer[str]
    algorithm_computation_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, states: _Optional[_Iterable[_Union[_order_pb2.OrderState, str]]] = ..., data_source_ids: _Optional[_Iterable[str]] = ..., analysis_computation_ids: _Optional[_Iterable[str]] = ..., algorithm_computation_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class TaskingOrderListResponse(_message.Message):
    __slots__ = ("status_code", "orders")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    orders: _containers.RepeatedCompositeFieldContainer[TaskingOrder]
    def __init__(self, status_code: _Optional[int] = ..., orders: _Optional[_Iterable[_Union[TaskingOrder, _Mapping]]] = ...) -> None: ...

class TaskingOrderGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TaskingOrderGetResponse(_message.Message):
    __slots__ = ("status_code", "order")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    order: TaskingOrder
    def __init__(self, status_code: _Optional[int] = ..., order: _Optional[_Union[TaskingOrder, _Mapping]] = ...) -> None: ...

class TaskingOrderApproveRequest(_message.Message):
    __slots__ = ("id", "comment")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    comment: str
    def __init__(self, id: _Optional[str] = ..., comment: _Optional[str] = ...) -> None: ...

class TaskingOrderApproveResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class TaskingOrderCreateRequest(_message.Message):
    __slots__ = ("data_source_id", "product_spec_name", "target_geom", "acq_window", "metadata")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_SPEC_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_GEOM_FIELD_NUMBER: _ClassVar[int]
    ACQ_WINDOW_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    product_spec_name: str
    target_geom: bytes
    acq_window: TimeRange
    metadata: _struct_pb2.Struct
    def __init__(self, data_source_id: _Optional[str] = ..., product_spec_name: _Optional[str] = ..., target_geom: _Optional[bytes] = ..., acq_window: _Optional[_Union[TimeRange, _Mapping]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class TaskingOrderCreateResponse(_message.Message):
    __slots__ = ("status_code", "order")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    order: TaskingOrder
    def __init__(self, status_code: _Optional[int] = ..., order: _Optional[_Union[TaskingOrder, _Mapping]] = ...) -> None: ...

class TaskingOrderCancelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TaskingOrderCancelResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
