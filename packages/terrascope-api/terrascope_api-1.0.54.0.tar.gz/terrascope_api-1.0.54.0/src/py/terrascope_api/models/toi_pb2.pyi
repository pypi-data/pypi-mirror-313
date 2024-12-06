import common_models_pb2 as _common_models_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class Cadence(_message.Message):
    __slots__ = ("frequency", "value")
    class Frequency(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_FREQUENCY: _ClassVar[Cadence.Frequency]
        MINUTELY: _ClassVar[Cadence.Frequency]
        HOURLY: _ClassVar[Cadence.Frequency]
        DAILY: _ClassVar[Cadence.Frequency]
        WEEKLY: _ClassVar[Cadence.Frequency]
        MONTHLY: _ClassVar[Cadence.Frequency]
        YEARLY: _ClassVar[Cadence.Frequency]
    UNKNOWN_FREQUENCY: Cadence.Frequency
    MINUTELY: Cadence.Frequency
    HOURLY: Cadence.Frequency
    DAILY: Cadence.Frequency
    WEEKLY: Cadence.Frequency
    MONTHLY: Cadence.Frequency
    YEARLY: Cadence.Frequency
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    frequency: Cadence.Frequency
    value: int
    def __init__(self, frequency: _Optional[_Union[Cadence.Frequency, str]] = ..., value: _Optional[int] = ...) -> None: ...

class Recurrence(_message.Message):
    __slots__ = ("id", "rule", "duration")
    ID_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    rule: str
    duration: Cadence
    def __init__(self, id: _Optional[str] = ..., rule: _Optional[str] = ..., duration: _Optional[_Union[Cadence, _Mapping]] = ...) -> None: ...

class TOI(_message.Message):
    __slots__ = ("id", "start_local", "finish_local", "recurrences", "exclude_dates", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    START_LOCAL_FIELD_NUMBER: _ClassVar[int]
    FINISH_LOCAL_FIELD_NUMBER: _ClassVar[int]
    RECURRENCES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DATES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    start_local: _timestamp_pb2.Timestamp
    finish_local: _timestamp_pb2.Timestamp
    recurrences: _containers.RepeatedCompositeFieldContainer[Recurrence]
    exclude_dates: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    description: str
    def __init__(self, id: _Optional[str] = ..., start_local: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., finish_local: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., recurrences: _Optional[_Iterable[_Union[Recurrence, _Mapping]]] = ..., exclude_dates: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ..., description: _Optional[str] = ...) -> None: ...

class TOICreateRequest(_message.Message):
    __slots__ = ("start_local", "finish_local", "recurrences", "exclude_dates", "description")
    START_LOCAL_FIELD_NUMBER: _ClassVar[int]
    FINISH_LOCAL_FIELD_NUMBER: _ClassVar[int]
    RECURRENCES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DATES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    start_local: _timestamp_pb2.Timestamp
    finish_local: _timestamp_pb2.Timestamp
    recurrences: _containers.RepeatedCompositeFieldContainer[Recurrence]
    exclude_dates: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    description: str
    def __init__(self, start_local: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., finish_local: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., recurrences: _Optional[_Iterable[_Union[Recurrence, _Mapping]]] = ..., exclude_dates: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ..., description: _Optional[str] = ...) -> None: ...

class TOICreateResponse(_message.Message):
    __slots__ = ("status_code", "toi")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TOI_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    toi: TOI
    def __init__(self, status_code: _Optional[int] = ..., toi: _Optional[_Union[TOI, _Mapping]] = ...) -> None: ...

class TOIDeleteRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class TOIDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class TOIGetRequest(_message.Message):
    __slots__ = ("ids", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    pagination: _common_models_pb2.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class TOIGetResponse(_message.Message):
    __slots__ = ("status_code", "toi_objects", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TOI_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    toi_objects: _containers.RepeatedCompositeFieldContainer[TOI]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., toi_objects: _Optional[_Iterable[_Union[TOI, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class TOIListRequest(_message.Message):
    __slots__ = ("search_text", "pagination")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    pagination: _common_models_pb2.Pagination
    def __init__(self, search_text: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...

class TOIListResponse(_message.Message):
    __slots__ = ("status_code", "toi_objects", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TOI_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    toi_objects: _containers.RepeatedCompositeFieldContainer[TOI]
    pagination: _common_models_pb2.Pagination
    def __init__(self, status_code: _Optional[int] = ..., toi_objects: _Optional[_Iterable[_Union[TOI, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2.Pagination, _Mapping]] = ...) -> None: ...
