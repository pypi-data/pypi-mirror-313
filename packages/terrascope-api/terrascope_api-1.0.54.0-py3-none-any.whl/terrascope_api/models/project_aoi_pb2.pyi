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

class ProjectAOICreateRequest(_message.Message):
    __slots__ = ("project_id", "aoi_ids", "aoi_inputs")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_IDS_FIELD_NUMBER: _ClassVar[int]
    AOI_INPUTS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    aoi_ids: _containers.RepeatedScalarFieldContainer[str]
    aoi_inputs: _containers.RepeatedCompositeFieldContainer[_aoi_pb2.AOIInput]
    def __init__(self, project_id: _Optional[str] = ..., aoi_ids: _Optional[_Iterable[str]] = ..., aoi_inputs: _Optional[_Iterable[_Union[_aoi_pb2.AOIInput, _Mapping]]] = ...) -> None: ...

class ProjectAOICreateResponse(_message.Message):
    __slots__ = ("status_code", "aoi_objects")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_objects: _containers.RepeatedCompositeFieldContainer[_aoi_pb2.AOIObject]
    def __init__(self, status_code: _Optional[int] = ..., aoi_objects: _Optional[_Iterable[_Union[_aoi_pb2.AOIObject, _Mapping]]] = ...) -> None: ...

class ProjectAOIUploadRequest(_message.Message):
    __slots__ = ("project_id", "chunk")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    chunk: bytes
    def __init__(self, project_id: _Optional[str] = ..., chunk: _Optional[bytes] = ...) -> None: ...

class ProjectAOIFileUploadResponse(_message.Message):
    __slots__ = ("status_code", "aoi_transaction")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_transaction: _aoi_pb2.AOITransaction
    def __init__(self, status_code: _Optional[int] = ..., aoi_transaction: _Optional[_Union[_aoi_pb2.AOITransaction, _Mapping]] = ...) -> None: ...

class ProjectAOIDeleteRequest(_message.Message):
    __slots__ = ("project_id", "aoi_ids")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_IDS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    aoi_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project_id: _Optional[str] = ..., aoi_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectAOIDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class ProjectAOIGetRequest(_message.Message):
    __slots__ = ("project_id", "pagination")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, project_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AOICollectionAOIs(_message.Message):
    __slots__ = ("aoi_collection_id", "aoi_collection_state", "aoi_objects")
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    AOI_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    aoi_collection_id: str
    aoi_collection_state: str
    aoi_objects: _containers.RepeatedCompositeFieldContainer[_aoi_pb2.AOIObject]
    def __init__(self, aoi_collection_id: _Optional[str] = ..., aoi_collection_state: _Optional[str] = ..., aoi_objects: _Optional[_Iterable[_Union[_aoi_pb2.AOIObject, _Mapping]]] = ...) -> None: ...

class ProjectAOIGetResponse(_message.Message):
    __slots__ = ("status_code", "aoi_collection_aois", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_AOIS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_collection_aois: _containers.RepeatedCompositeFieldContainer[AOICollectionAOIs]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., aoi_collection_aois: _Optional[_Iterable[_Union[AOICollectionAOIs, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class ProjectAOIUpdateRequest(_message.Message):
    __slots__ = ("project_id", "aoi_id", "aoi_modification_input")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_MODIFICATION_INPUT_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    aoi_id: str
    aoi_modification_input: _aoi_pb2.AOIInput
    def __init__(self, project_id: _Optional[str] = ..., aoi_id: _Optional[str] = ..., aoi_modification_input: _Optional[_Union[_aoi_pb2.AOIInput, _Mapping]] = ...) -> None: ...

class ProjectAOIUpdateResponse(_message.Message):
    __slots__ = ("status_code", "aoi_collection_aois")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTION_AOIS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    aoi_collection_aois: AOICollectionAOIs
    def __init__(self, status_code: _Optional[int] = ..., aoi_collection_aois: _Optional[_Union[AOICollectionAOIs, _Mapping]] = ...) -> None: ...
