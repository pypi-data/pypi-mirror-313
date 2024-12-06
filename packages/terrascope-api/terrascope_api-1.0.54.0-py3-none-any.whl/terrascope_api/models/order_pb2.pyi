from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import order_recommendation_pb2 as _order_recommendation_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class OrderState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[OrderState]
    CREATED: _ClassVar[OrderState]
    APPROVED: _ClassVar[OrderState]
    QUEUED: _ClassVar[OrderState]
    PROCESSING: _ClassVar[OrderState]
    ORDERED: _ClassVar[OrderState]
    CANCELLED: _ClassVar[OrderState]
    DELIVERED: _ClassVar[OrderState]
    FAILED: _ClassVar[OrderState]
    PENDING_APPROVAL: _ClassVar[OrderState]
    SUBMITTED: _ClassVar[OrderState]
UNKNOWN: OrderState
CREATED: OrderState
APPROVED: OrderState
QUEUED: OrderState
PROCESSING: OrderState
ORDERED: OrderState
CANCELLED: OrderState
DELIVERED: OrderState
FAILED: OrderState
PENDING_APPROVAL: OrderState
SUBMITTED: OrderState

class Item(_message.Message):
    __slots__ = ("id", "scene_id", "target_geom", "item_metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    SCENE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_GEOM_FIELD_NUMBER: _ClassVar[int]
    ITEM_METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    scene_id: str
    target_geom: bytes
    item_metadata: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., scene_id: _Optional[str] = ..., target_geom: _Optional[bytes] = ..., item_metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ("id", "data_source_id", "items", "product_spec_name", "state", "details", "url", "metadata", "creator", "created_on", "updated_on", "approved_by", "approval_comment", "recommendations")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
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
    items: _containers.RepeatedCompositeFieldContainer[Item]
    product_spec_name: str
    state: OrderState
    details: str
    url: str
    metadata: _struct_pb2.Struct
    creator: str
    created_on: _timestamp_pb2.Timestamp
    updated_on: _timestamp_pb2.Timestamp
    approved_by: str
    approval_comment: str
    recommendations: _containers.RepeatedCompositeFieldContainer[_order_recommendation_pb2.OrderRecommendation]
    def __init__(self, id: _Optional[str] = ..., data_source_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., product_spec_name: _Optional[str] = ..., state: _Optional[_Union[OrderState, str]] = ..., details: _Optional[str] = ..., url: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., creator: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., approved_by: _Optional[str] = ..., approval_comment: _Optional[str] = ..., recommendations: _Optional[_Iterable[_Union[_order_recommendation_pb2.OrderRecommendation, _Mapping]]] = ...) -> None: ...

class OrderListRequest(_message.Message):
    __slots__ = ("states", "data_source_ids", "provider_ids", "analysis_computation_ids", "algorithm_computation_ids")
    STATES_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_IDS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_COMPUTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedScalarFieldContainer[OrderState]
    data_source_ids: _containers.RepeatedScalarFieldContainer[str]
    provider_ids: _containers.RepeatedScalarFieldContainer[str]
    analysis_computation_ids: _containers.RepeatedScalarFieldContainer[str]
    algorithm_computation_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, states: _Optional[_Iterable[_Union[OrderState, str]]] = ..., data_source_ids: _Optional[_Iterable[str]] = ..., provider_ids: _Optional[_Iterable[str]] = ..., analysis_computation_ids: _Optional[_Iterable[str]] = ..., algorithm_computation_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class OrderListResponse(_message.Message):
    __slots__ = ("status_code", "orders")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    def __init__(self, status_code: _Optional[int] = ..., orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...

class OrderGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class OrderGetResponse(_message.Message):
    __slots__ = ("status_code", "order")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    order: Order
    def __init__(self, status_code: _Optional[int] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class OrderApproveRequest(_message.Message):
    __slots__ = ("id", "comment")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    comment: str
    def __init__(self, id: _Optional[str] = ..., comment: _Optional[str] = ...) -> None: ...

class OrderApproveResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class OrderCreateRequest(_message.Message):
    __slots__ = ("data_source_id", "product_spec_name", "metadata", "items")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_SPEC_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    product_spec_name: str
    metadata: _struct_pb2.Struct
    items: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, data_source_id: _Optional[str] = ..., product_spec_name: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class OrderCreateResponse(_message.Message):
    __slots__ = ("status_code", "order")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    order: Order
    def __init__(self, status_code: _Optional[int] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class OrderCancelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class OrderCancelResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
