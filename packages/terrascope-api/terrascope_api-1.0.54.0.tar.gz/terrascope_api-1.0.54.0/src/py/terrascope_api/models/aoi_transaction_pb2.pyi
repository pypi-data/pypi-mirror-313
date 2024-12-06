import aoi_pb2 as _aoi_pb2
import common_models_pb2 as _common_models_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from aoi_pb2 import AOITransaction as AOITransaction
from aoi_pb2 import AOIIdentifier as AOIIdentifier
from aoi_pb2 import AOIObject as AOIObject
from aoi_pb2 import AOIVersion as AOIVersion
from aoi_pb2 import AOIInput as AOIInput
from aoi_pb2 import AOICreateRequest as AOICreateRequest
from aoi_pb2 import AOICreateResponse as AOICreateResponse
from aoi_pb2 import AOIUploadRequest as AOIUploadRequest
from aoi_pb2 import AOIUploadResponse as AOIUploadResponse
from aoi_pb2 import AOIGetRequest as AOIGetRequest
from aoi_pb2 import AOIGetResponse as AOIGetResponse
from aoi_pb2 import AOIUpdateRequest as AOIUpdateRequest
from aoi_pb2 import AOIUpdateResponse as AOIUpdateResponse
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class AOITransactionStatusRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AOITransactionStatusResponse(_message.Message):
    __slots__ = ("status_code", "transaction")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    transaction: _aoi_pb2.AOITransaction
    def __init__(self, status_code: _Optional[int] = ..., transaction: _Optional[_Union[_aoi_pb2.AOITransaction, _Mapping]] = ...) -> None: ...

class AOITransactionGetRequest(_message.Message):
    __slots__ = ("pagination", "id")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2_1.Pagination
    id: str
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., id: _Optional[str] = ...) -> None: ...

class AOITransactionGetResponse(_message.Message):
    __slots__ = ("status_code", "pagination", "aoi_identifiers")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AOI_IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    pagination: _common_models_pb2_1.Pagination
    aoi_identifiers: _containers.RepeatedCompositeFieldContainer[_aoi_pb2.AOIIdentifier]
    def __init__(self, status_code: _Optional[int] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ..., aoi_identifiers: _Optional[_Iterable[_Union[_aoi_pb2.AOIIdentifier, _Mapping]]] = ...) -> None: ...
