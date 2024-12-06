from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class Links(_message.Message):
    __slots__ = ("href", "type", "rel", "description", "title")
    HREF_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    href: str
    type: str
    rel: str
    description: str
    title: str
    def __init__(self, href: _Optional[str] = ..., type: _Optional[str] = ..., rel: _Optional[str] = ..., description: _Optional[str] = ..., title: _Optional[str] = ...) -> None: ...

class ParentRef(_message.Message):
    __slots__ = ("id", "parent_id", "key")
    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    parent_id: str
    key: str
    def __init__(self, id: _Optional[str] = ..., parent_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class TrackedEvent(_message.Message):
    __slots__ = ("id", "data_tracking_id", "event_type", "received_timestamp", "contents", "context")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TRACKING_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    data_tracking_id: str
    event_type: str
    received_timestamp: _timestamp_pb2.Timestamp
    contents: _struct_pb2.Struct
    context: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., data_tracking_id: _Optional[str] = ..., event_type: _Optional[str] = ..., received_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., contents: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class JobInfo(_message.Message):
    __slots__ = ("id", "name", "status", "user_id", "last_updated_ts", "created_ts", "parent_ref", "provider_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_TS_FIELD_NUMBER: _ClassVar[int]
    CREATED_TS_FIELD_NUMBER: _ClassVar[int]
    PARENT_REF_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    status: str
    user_id: str
    last_updated_ts: _timestamp_pb2.Timestamp
    created_ts: _timestamp_pb2.Timestamp
    parent_ref: ParentRef
    provider_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., status: _Optional[str] = ..., user_id: _Optional[str] = ..., last_updated_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., parent_ref: _Optional[_Union[ParentRef, _Mapping]] = ..., provider_id: _Optional[str] = ...) -> None: ...

class TrackedStatusHistory(_message.Message):
    __slots__ = ("data_tracking_id", "status", "ts")
    DATA_TRACKING_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    data_tracking_id: str
    status: str
    ts: _timestamp_pb2.Timestamp
    def __init__(self, data_tracking_id: _Optional[str] = ..., status: _Optional[str] = ..., ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TrackedJob(_message.Message):
    __slots__ = ("parent_ref", "info", "events", "status_history", "links")
    PARENT_REF_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_HISTORY_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    parent_ref: ParentRef
    info: JobInfo
    events: _containers.RepeatedCompositeFieldContainer[TrackedEvent]
    status_history: _containers.RepeatedCompositeFieldContainer[TrackedStatusHistory]
    links: _containers.RepeatedCompositeFieldContainer[Links]
    def __init__(self, parent_ref: _Optional[_Union[ParentRef, _Mapping]] = ..., info: _Optional[_Union[JobInfo, _Mapping]] = ..., events: _Optional[_Iterable[_Union[TrackedEvent, _Mapping]]] = ..., status_history: _Optional[_Iterable[_Union[TrackedStatusHistory, _Mapping]]] = ..., links: _Optional[_Iterable[_Union[Links, _Mapping]]] = ...) -> None: ...

class DataTrackingGetQueryablesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DataTrackingGetQueryablesResponse(_message.Message):
    __slots__ = ("queryables",)
    QUERYABLES_FIELD_NUMBER: _ClassVar[int]
    queryables: _struct_pb2.Struct
    def __init__(self, queryables: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DataTrackingTrackedJobSearchRequest(_message.Message):
    __slots__ = ("pagination", "filter_lang", "filter", "order_by")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    FILTER_LANG_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2.Pagination
    filter_lang: str
    filter: str
    order_by: str
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., filter_lang: _Optional[str] = ..., filter: _Optional[str] = ..., order_by: _Optional[str] = ...) -> None: ...

class DataTrackingTrackedJobSearchResponse(_message.Message):
    __slots__ = ("pagination", "jobs")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    JOBS_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2.Pagination
    jobs: _containers.RepeatedCompositeFieldContainer[TrackedJob]
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ..., jobs: _Optional[_Iterable[_Union[TrackedJob, _Mapping]]] = ...) -> None: ...
