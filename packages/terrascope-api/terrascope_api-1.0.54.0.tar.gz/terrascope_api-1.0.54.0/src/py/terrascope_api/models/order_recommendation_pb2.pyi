from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderRecommendation(_message.Message):
    __slots__ = ("id", "creator", "justification", "team", "contact_info", "expiration", "created_on")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    JUSTIFICATION_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    CONTACT_INFO_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    id: str
    creator: str
    justification: str
    team: str
    contact_info: str
    expiration: _timestamp_pb2.Timestamp
    created_on: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., creator: _Optional[str] = ..., justification: _Optional[str] = ..., team: _Optional[str] = ..., contact_info: _Optional[str] = ..., expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OrderRecommendationCreateRequest(_message.Message):
    __slots__ = ("order_id", "justification", "team", "contact_info", "expiration")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    JUSTIFICATION_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    CONTACT_INFO_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    justification: str
    team: str
    contact_info: str
    expiration: _timestamp_pb2.Timestamp
    def __init__(self, order_id: _Optional[str] = ..., justification: _Optional[str] = ..., team: _Optional[str] = ..., contact_info: _Optional[str] = ..., expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OrderRecommendationCreateResponse(_message.Message):
    __slots__ = ("status_code", "order_recommendation")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_RECOMMENDATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    order_recommendation: OrderRecommendation
    def __init__(self, status_code: _Optional[int] = ..., order_recommendation: _Optional[_Union[OrderRecommendation, _Mapping]] = ...) -> None: ...

class OrderRecommendationUpdateRequest(_message.Message):
    __slots__ = ("order_recommendation_id", "justification", "team", "contact_info", "expiration")
    ORDER_RECOMMENDATION_ID_FIELD_NUMBER: _ClassVar[int]
    JUSTIFICATION_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    CONTACT_INFO_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    order_recommendation_id: str
    justification: str
    team: str
    contact_info: str
    expiration: _timestamp_pb2.Timestamp
    def __init__(self, order_recommendation_id: _Optional[str] = ..., justification: _Optional[str] = ..., team: _Optional[str] = ..., contact_info: _Optional[str] = ..., expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OrderRecommendationUpdateResponse(_message.Message):
    __slots__ = ("status_code", "order_recommendation")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_RECOMMENDATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    order_recommendation: OrderRecommendation
    def __init__(self, status_code: _Optional[int] = ..., order_recommendation: _Optional[_Union[OrderRecommendation, _Mapping]] = ...) -> None: ...

class OrderRecommendationDeleteRequest(_message.Message):
    __slots__ = ("order_recommendation_id",)
    ORDER_RECOMMENDATION_ID_FIELD_NUMBER: _ClassVar[int]
    order_recommendation_id: str
    def __init__(self, order_recommendation_id: _Optional[str] = ...) -> None: ...

class OrderRecommendationDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
