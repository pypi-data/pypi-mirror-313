from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class Subscription(_message.Message):
    __slots__ = ("id", "topic_id", "channel_id", "filter")
    class Filter(_message.Message):
        __slots__ = ("data_types", "algorithm_version_ids")
        DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
        ALGORITHM_VERSION_IDS_FIELD_NUMBER: _ClassVar[int]
        data_types: _containers.RepeatedScalarFieldContainer[str]
        algorithm_version_ids: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, data_types: _Optional[_Iterable[str]] = ..., algorithm_version_ids: _Optional[_Iterable[str]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    id: str
    topic_id: str
    channel_id: str
    filter: Subscription.Filter
    def __init__(self, id: _Optional[str] = ..., topic_id: _Optional[str] = ..., channel_id: _Optional[str] = ..., filter: _Optional[_Union[Subscription.Filter, _Mapping]] = ...) -> None: ...

class SubscriptionCreateRequest(_message.Message):
    __slots__ = ("subscriptions",)
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    subscriptions: _containers.RepeatedCompositeFieldContainer[Subscription]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[Subscription, _Mapping]]] = ...) -> None: ...

class SubscriptionCreateResponse(_message.Message):
    __slots__ = ("status_code", "subscription_ids")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_IDS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    subscription_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, status_code: _Optional[int] = ..., subscription_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class Topic(_message.Message):
    __slots__ = ("id", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    description: str
    def __init__(self, id: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class TopicListRequest(_message.Message):
    __slots__ = ("search_text",)
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    def __init__(self, search_text: _Optional[str] = ...) -> None: ...

class TopicListResponse(_message.Message):
    __slots__ = ("status_code", "topics")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    topics: _containers.RepeatedCompositeFieldContainer[Topic]
    def __init__(self, status_code: _Optional[int] = ..., topics: _Optional[_Iterable[_Union[Topic, _Mapping]]] = ...) -> None: ...

class Channel(_message.Message):
    __slots__ = ("id", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class ChannelListRequest(_message.Message):
    __slots__ = ("search_text",)
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    def __init__(self, search_text: _Optional[str] = ...) -> None: ...

class ChannelListResponse(_message.Message):
    __slots__ = ("status_code", "channels")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    channels: _containers.RepeatedCompositeFieldContainer[Channel]
    def __init__(self, status_code: _Optional[int] = ..., channels: _Optional[_Iterable[_Union[Channel, _Mapping]]] = ...) -> None: ...

class SubscriptionDeleteRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class SubscriptionDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class SubscriptionListRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2.Pagination
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class SubscriptionListResponse(_message.Message):
    __slots__ = ("status_code", "subscriptions", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    subscriptions: _containers.RepeatedCompositeFieldContainer[Subscription]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., subscriptions: _Optional[_Iterable[_Union[Subscription, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class NotificationSendRequest(_message.Message):
    __slots__ = ("topic", "message", "user_id", "filters")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    topic: str
    message: str
    user_id: str
    filters: _struct_pb2.Struct
    def __init__(self, topic: _Optional[str] = ..., message: _Optional[str] = ..., user_id: _Optional[str] = ..., filters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class NotificationSendResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class Notification(_message.Message):
    __slots__ = ("id", "subscription_id", "message_data", "delivered_on", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    DELIVERED_ON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    subscription_id: str
    message_data: _struct_pb2.Struct
    delivered_on: _timestamp_pb2.Timestamp
    status: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., subscription_id: _Optional[str] = ..., message_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., delivered_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class NotificationListRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2.Pagination
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class NotificationListResponse(_message.Message):
    __slots__ = ("status_code", "notifications", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    notifications: _containers.RepeatedCompositeFieldContainer[Notification]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., notifications: _Optional[_Iterable[_Union[Notification, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class NotificationUpdateRequest(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class NotificationUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
