from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProviderQuotasListRequest(_message.Message):
    __slots__ = ("provider",)
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    provider: str
    def __init__(self, provider: _Optional[str] = ...) -> None: ...

class ProviderQuota(_message.Message):
    __slots__ = ("data_source_id", "quota_name", "used", "limit", "unit")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_NAME_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    data_source_id: str
    quota_name: str
    used: float
    limit: float
    unit: str
    def __init__(self, data_source_id: _Optional[str] = ..., quota_name: _Optional[str] = ..., used: _Optional[float] = ..., limit: _Optional[float] = ..., unit: _Optional[str] = ...) -> None: ...

class ProviderQuotasListResponse(_message.Message):
    __slots__ = ("quotas",)
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    quotas: _containers.RepeatedCompositeFieldContainer[ProviderQuota]
    def __init__(self, quotas: _Optional[_Iterable[_Union[ProviderQuota, _Mapping]]] = ...) -> None: ...
