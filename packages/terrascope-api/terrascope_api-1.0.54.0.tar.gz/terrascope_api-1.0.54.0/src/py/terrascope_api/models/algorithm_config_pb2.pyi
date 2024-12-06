from google.protobuf import struct_pb2 as _struct_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import algorithm_pb2 as _algorithm_pb2
import common_models_pb2 as _common_models_pb2_1
import algorithm_version_pb2 as _algorithm_version_pb2
import common_models_pb2 as _common_models_pb2_1_1
import algorithm_pb2 as _algorithm_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from algorithm_pb2 import Algorithm as Algorithm
from algorithm_pb2 import AlgorithmCreateRequest as AlgorithmCreateRequest
from algorithm_pb2 import AlgorithmCreateResponse as AlgorithmCreateResponse
from algorithm_pb2 import AlgorithmGetRequest as AlgorithmGetRequest
from algorithm_pb2 import AlgorithmGetResponse as AlgorithmGetResponse
from algorithm_pb2 import AlgorithmListRequest as AlgorithmListRequest
from algorithm_pb2 import AlgorithmListResponse as AlgorithmListResponse
from algorithm_pb2 import AlgorithmUpdateRequest as AlgorithmUpdateRequest
from algorithm_pb2 import AlgorithmUpdateResponse as AlgorithmUpdateResponse
from algorithm_version_pb2 import Manifest as Manifest
from algorithm_version_pb2 import AlgorithmVersion as AlgorithmVersion
from algorithm_version_pb2 import AlgorithmVersionCreateRequest as AlgorithmVersionCreateRequest
from algorithm_version_pb2 import AlgorithmVersionCreateResponse as AlgorithmVersionCreateResponse
from algorithm_version_pb2 import AlgorithmVersionGetRequest as AlgorithmVersionGetRequest
from algorithm_version_pb2 import AlgorithmVersionGetResponse as AlgorithmVersionGetResponse
from algorithm_version_pb2 import AlgorithmVersionListRequest as AlgorithmVersionListRequest
from algorithm_version_pb2 import AlgorithmVersionListResponse as AlgorithmVersionListResponse
from algorithm_version_pb2 import AlgorithmVersionDeprecateRequest as AlgorithmVersionDeprecateRequest
from algorithm_version_pb2 import AlgorithmVersionDeprecateResponse as AlgorithmVersionDeprecateResponse
from algorithm_version_pb2 import AlgorithmVersionDeactivateRequest as AlgorithmVersionDeactivateRequest
from algorithm_version_pb2 import AlgorithmVersionDeactivateResponse as AlgorithmVersionDeactivateResponse
from algorithm_version_pb2 import AlgorithmVersionActivateRequest as AlgorithmVersionActivateRequest
from algorithm_version_pb2 import AlgorithmVersionActivateResponse as AlgorithmVersionActivateResponse

DESCRIPTOR: _descriptor.FileDescriptor

class AlgorithmConfig(_message.Message):
    __slots__ = ("id", "algorithm_version", "config", "algorithm", "created_on", "is_deactivated", "is_deprecated", "name", "description", "resources_locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    IS_DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    IS_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: str
    algorithm_version: _algorithm_version_pb2.AlgorithmVersion
    config: _struct_pb2.Struct
    algorithm: _algorithm_pb2_1.Algorithm
    created_on: _timestamp_pb2.Timestamp
    is_deactivated: bool
    is_deprecated: bool
    name: str
    description: str
    resources_locked: bool
    def __init__(self, id: _Optional[str] = ..., algorithm_version: _Optional[_Union[_algorithm_version_pb2.AlgorithmVersion, _Mapping]] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., algorithm: _Optional[_Union[_algorithm_pb2_1.Algorithm, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_deactivated: bool = ..., is_deprecated: bool = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., resources_locked: bool = ...) -> None: ...

class AlgorithmConfigCreateRequest(_message.Message):
    __slots__ = ("algorithm_version_id", "params", "name", "description")
    ALGORITHM_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    algorithm_version_id: str
    params: _struct_pb2.Struct
    name: str
    description: str
    def __init__(self, algorithm_version_id: _Optional[str] = ..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class AlgorithmConfigCreateResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_config")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_config: AlgorithmConfig
    def __init__(self, status_code: _Optional[int] = ..., algorithm_config: _Optional[_Union[AlgorithmConfig, _Mapping]] = ...) -> None: ...

class AlgorithmConfigUpdateRequest(_message.Message):
    __slots__ = ("id", "algorithm_config")
    ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    algorithm_config: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., algorithm_config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class AlgorithmConfigUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AlgorithmConfigGetRequest(_message.Message):
    __slots__ = ("ids", "algorithm_id", "pagination", "algorithm_version_id")
    IDS_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    algorithm_id: str
    pagination: _common_models_pb2_1_1.Pagination
    algorithm_version_id: str
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., algorithm_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ..., algorithm_version_id: _Optional[str] = ...) -> None: ...

class AlgorithmConfigGetResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_configs", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_configs: _containers.RepeatedCompositeFieldContainer[AlgorithmConfig]
    pagination: _common_models_pb2_1_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithm_configs: _Optional[_Iterable[_Union[AlgorithmConfig, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmConfigListRequest(_message.Message):
    __slots__ = ("algorithm_id", "algorithm_version_id", "search_text", "min_created_on", "max_created_on", "include_deactivated", "pagination")
    ALGORITHM_ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    algorithm_id: str
    algorithm_version_id: str
    search_text: str
    min_created_on: _timestamp_pb2.Timestamp
    max_created_on: _timestamp_pb2.Timestamp
    include_deactivated: bool
    pagination: _common_models_pb2_1_1.Pagination
    def __init__(self, algorithm_id: _Optional[str] = ..., algorithm_version_id: _Optional[str] = ..., search_text: _Optional[str] = ..., min_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., include_deactivated: bool = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmConfigListResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_configs", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_configs: _containers.RepeatedCompositeFieldContainer[AlgorithmConfig]
    pagination: _common_models_pb2_1_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithm_configs: _Optional[_Iterable[_Union[AlgorithmConfig, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmConfigDeleteRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmConfigDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AlgorithmConfigDeprecateRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmConfigDeprecateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AlgorithmConfigDeactivateRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmConfigDeactivateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
