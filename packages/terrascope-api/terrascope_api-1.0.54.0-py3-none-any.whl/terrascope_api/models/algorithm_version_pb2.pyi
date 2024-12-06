from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
import algorithm_pb2 as _algorithm_pb2
import common_models_pb2 as _common_models_pb2_1
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

DESCRIPTOR: _descriptor.FileDescriptor

class Manifest(_message.Message):
    __slots__ = ("metadata", "inputs", "outputs", "container_parameters", "interface", "resource_request", "parameters", "manifest_version")
    class Metadata(_message.Message):
        __slots__ = ("description", "version", "tags")
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        description: str
        version: str
        tags: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, description: _Optional[str] = ..., version: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
    class Interface(_message.Message):
        __slots__ = ("interface_type", "adapter")
        INTERFACE_TYPE_FIELD_NUMBER: _ClassVar[int]
        ADAPTER_FIELD_NUMBER: _ClassVar[int]
        interface_type: str
        adapter: str
        def __init__(self, interface_type: _Optional[str] = ..., adapter: _Optional[str] = ...) -> None: ...
    class AlgorithmInputs(_message.Message):
        __slots__ = ("data_type_name", "min_count", "max_count")
        DATA_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        MIN_COUNT_FIELD_NUMBER: _ClassVar[int]
        MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
        data_type_name: str
        min_count: int
        max_count: int
        def __init__(self, data_type_name: _Optional[str] = ..., min_count: _Optional[int] = ..., max_count: _Optional[int] = ...) -> None: ...
    class AlgorithmOutputs(_message.Message):
        __slots__ = ("observation_value_columns", "data_type_name")
        OBSERVATION_VALUE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        DATA_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        observation_value_columns: _containers.RepeatedScalarFieldContainer[str]
        data_type_name: str
        def __init__(self, observation_value_columns: _Optional[_Iterable[str]] = ..., data_type_name: _Optional[str] = ...) -> None: ...
    class ContainerParameters(_message.Message):
        __slots__ = ("image", "resource_request", "command")
        IMAGE_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_REQUEST_FIELD_NUMBER: _ClassVar[int]
        COMMAND_FIELD_NUMBER: _ClassVar[int]
        image: str
        resource_request: Manifest.ResourceRequest
        command: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, image: _Optional[str] = ..., resource_request: _Optional[_Union[Manifest.ResourceRequest, _Mapping]] = ..., command: _Optional[_Iterable[str]] = ...) -> None: ...
    class ResourceRequest(_message.Message):
        __slots__ = ("gpu", "memory_gb", "cpu_millicore", "max_input_gb")
        GPU_FIELD_NUMBER: _ClassVar[int]
        MEMORY_GB_FIELD_NUMBER: _ClassVar[int]
        CPU_MILLICORE_FIELD_NUMBER: _ClassVar[int]
        MAX_INPUT_GB_FIELD_NUMBER: _ClassVar[int]
        gpu: int
        memory_gb: int
        cpu_millicore: int
        max_input_gb: float
        def __init__(self, gpu: _Optional[int] = ..., memory_gb: _Optional[int] = ..., cpu_millicore: _Optional[int] = ..., max_input_gb: _Optional[float] = ...) -> None: ...
    class Parameter(_message.Message):
        __slots__ = ("name", "type", "units", "description", "min", "max", "allowed_values", "default")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        ALLOWED_VALUES_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: int
        units: str
        description: str
        min: int
        max: int
        allowed_values: _containers.RepeatedScalarFieldContainer[str]
        default: int
        def __init__(self, name: _Optional[str] = ..., type: _Optional[int] = ..., units: _Optional[str] = ..., description: _Optional[str] = ..., min: _Optional[int] = ..., max: _Optional[int] = ..., allowed_values: _Optional[_Iterable[str]] = ..., default: _Optional[int] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    metadata: Manifest.Metadata
    inputs: _containers.RepeatedCompositeFieldContainer[Manifest.AlgorithmInputs]
    outputs: _containers.RepeatedCompositeFieldContainer[Manifest.AlgorithmOutputs]
    container_parameters: Manifest.ContainerParameters
    interface: Manifest.Interface
    resource_request: Manifest.ResourceRequest
    parameters: _containers.RepeatedCompositeFieldContainer[Manifest.Parameter]
    manifest_version: str
    def __init__(self, metadata: _Optional[_Union[Manifest.Metadata, _Mapping]] = ..., inputs: _Optional[_Iterable[_Union[Manifest.AlgorithmInputs, _Mapping]]] = ..., outputs: _Optional[_Iterable[_Union[Manifest.AlgorithmOutputs, _Mapping]]] = ..., container_parameters: _Optional[_Union[Manifest.ContainerParameters, _Mapping]] = ..., interface: _Optional[_Union[Manifest.Interface, _Mapping]] = ..., resource_request: _Optional[_Union[Manifest.ResourceRequest, _Mapping]] = ..., parameters: _Optional[_Iterable[_Union[Manifest.Parameter, _Mapping]]] = ..., manifest_version: _Optional[str] = ...) -> None: ...

class AlgorithmVersion(_message.Message):
    __slots__ = ("id", "algorithm", "version", "manifest", "created_on", "is_deactivated", "is_deprecated")
    ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    IS_DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    IS_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    algorithm: _algorithm_pb2.Algorithm
    version: str
    manifest: _struct_pb2.Struct
    created_on: _timestamp_pb2.Timestamp
    is_deactivated: bool
    is_deprecated: bool
    def __init__(self, id: _Optional[str] = ..., algorithm: _Optional[_Union[_algorithm_pb2.Algorithm, _Mapping]] = ..., version: _Optional[str] = ..., manifest: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_deactivated: bool = ..., is_deprecated: bool = ...) -> None: ...

class AlgorithmVersionCreateRequest(_message.Message):
    __slots__ = ("algorithm_id", "manifest_struct", "manifest_message")
    ALGORITHM_ID_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_STRUCT_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    algorithm_id: str
    manifest_struct: _struct_pb2.Struct
    manifest_message: Manifest
    def __init__(self, algorithm_id: _Optional[str] = ..., manifest_struct: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., manifest_message: _Optional[_Union[Manifest, _Mapping]] = ...) -> None: ...

class AlgorithmVersionCreateResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_version")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_version: AlgorithmVersion
    def __init__(self, status_code: _Optional[int] = ..., algorithm_version: _Optional[_Union[AlgorithmVersion, _Mapping]] = ...) -> None: ...

class AlgorithmVersionGetRequest(_message.Message):
    __slots__ = ("ids", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmVersionGetResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_versions", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_versions: _containers.RepeatedCompositeFieldContainer[AlgorithmVersion]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithm_versions: _Optional[_Iterable[_Union[AlgorithmVersion, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmVersionListRequest(_message.Message):
    __slots__ = ("algorithm_id", "search_text", "tag", "min_created_on", "max_created_on", "include_all_versions", "pagination")
    ALGORITHM_ID_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ALL_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    algorithm_id: str
    search_text: str
    tag: str
    min_created_on: _timestamp_pb2.Timestamp
    max_created_on: _timestamp_pb2.Timestamp
    include_all_versions: bool
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, algorithm_id: _Optional[str] = ..., search_text: _Optional[str] = ..., tag: _Optional[str] = ..., min_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., include_all_versions: bool = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmVersionListResponse(_message.Message):
    __slots__ = ("status_code", "algorithm_versions", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    algorithm_versions: _containers.RepeatedCompositeFieldContainer[AlgorithmVersion]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., algorithm_versions: _Optional[_Iterable[_Union[AlgorithmVersion, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class AlgorithmVersionDeprecateRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmVersionDeprecateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AlgorithmVersionDeactivateRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmVersionDeactivateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AlgorithmVersionActivateRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlgorithmVersionActivateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
