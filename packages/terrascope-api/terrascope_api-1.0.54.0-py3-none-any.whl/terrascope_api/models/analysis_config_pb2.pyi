from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
import analysis_pb2 as _analysis_pb2
import common_models_pb2 as _common_models_pb2_1
import analysis_version_pb2 as _analysis_version_pb2
import common_models_pb2 as _common_models_pb2_1_1
import analysis_pb2 as _analysis_pb2_1
import algorithm_version_pb2 as _algorithm_version_pb2
import algorithm_config_pb2 as _algorithm_config_pb2
import common_models_pb2 as _common_models_pb2_1_1_1
import algorithm_pb2 as _algorithm_pb2
import algorithm_version_pb2 as _algorithm_version_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from analysis_pb2 import AnalysisAlgorithmNode as AnalysisAlgorithmNode
from analysis_pb2 import AnalysisCreateRequest as AnalysisCreateRequest
from analysis_pb2 import AnalysisCreateResponse as AnalysisCreateResponse
from analysis_pb2 import AnalysisAlgorithmConfigNode as AnalysisAlgorithmConfigNode
from analysis_pb2 import AnalysisGetRequest as AnalysisGetRequest
from analysis_pb2 import Analysis as Analysis
from analysis_pb2 import AnalysisGetResponse as AnalysisGetResponse
from analysis_pb2 import AnalysisListRequest as AnalysisListRequest
from analysis_pb2 import AnalysisListResponse as AnalysisListResponse
from analysis_version_pb2 import AnalysisManifest as AnalysisManifest
from analysis_version_pb2 import AnalysisVersion as AnalysisVersion
from analysis_version_pb2 import AnalysisVersionCreateRequest as AnalysisVersionCreateRequest
from analysis_version_pb2 import AnalysisVersionCreateResponse as AnalysisVersionCreateResponse
from analysis_version_pb2 import AnalysisVersionGetRequest as AnalysisVersionGetRequest
from analysis_version_pb2 import AnalysisVersionGetResponse as AnalysisVersionGetResponse
from analysis_version_pb2 import AnalysisVersionListRequest as AnalysisVersionListRequest
from analysis_version_pb2 import AnalysisVersionListResponse as AnalysisVersionListResponse
from algorithm_config_pb2 import AlgorithmConfig as AlgorithmConfig
from algorithm_config_pb2 import AlgorithmConfigCreateRequest as AlgorithmConfigCreateRequest
from algorithm_config_pb2 import AlgorithmConfigCreateResponse as AlgorithmConfigCreateResponse
from algorithm_config_pb2 import AlgorithmConfigUpdateRequest as AlgorithmConfigUpdateRequest
from algorithm_config_pb2 import AlgorithmConfigUpdateResponse as AlgorithmConfigUpdateResponse
from algorithm_config_pb2 import AlgorithmConfigGetRequest as AlgorithmConfigGetRequest
from algorithm_config_pb2 import AlgorithmConfigGetResponse as AlgorithmConfigGetResponse
from algorithm_config_pb2 import AlgorithmConfigListRequest as AlgorithmConfigListRequest
from algorithm_config_pb2 import AlgorithmConfigListResponse as AlgorithmConfigListResponse
from algorithm_config_pb2 import AlgorithmConfigDeleteRequest as AlgorithmConfigDeleteRequest
from algorithm_config_pb2 import AlgorithmConfigDeleteResponse as AlgorithmConfigDeleteResponse
from algorithm_config_pb2 import AlgorithmConfigDeprecateRequest as AlgorithmConfigDeprecateRequest
from algorithm_config_pb2 import AlgorithmConfigDeprecateResponse as AlgorithmConfigDeprecateResponse
from algorithm_config_pb2 import AlgorithmConfigDeactivateRequest as AlgorithmConfigDeactivateRequest
from algorithm_config_pb2 import AlgorithmConfigDeactivateResponse as AlgorithmConfigDeactivateResponse

DESCRIPTOR: _descriptor.FileDescriptor

class AnalysisConfig(_message.Message):
    __slots__ = ("analysis", "analysis_version", "id", "name", "description", "created_on", "algorithm_config_nodes", "algorithm_configs", "is_deprecated", "is_deactivated", "resources_locked")
    ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_NODES_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    IS_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    IS_DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_LOCKED_FIELD_NUMBER: _ClassVar[int]
    analysis: _analysis_pb2_1.Analysis
    analysis_version: _analysis_version_pb2.AnalysisVersion
    id: str
    name: str
    description: str
    created_on: _timestamp_pb2.Timestamp
    algorithm_config_nodes: _containers.RepeatedCompositeFieldContainer[_analysis_pb2_1.AnalysisAlgorithmConfigNode]
    algorithm_configs: _containers.RepeatedCompositeFieldContainer[_algorithm_config_pb2.AlgorithmConfig]
    is_deprecated: bool
    is_deactivated: bool
    resources_locked: bool
    def __init__(self, analysis: _Optional[_Union[_analysis_pb2_1.Analysis, _Mapping]] = ..., analysis_version: _Optional[_Union[_analysis_version_pb2.AnalysisVersion, _Mapping]] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., algorithm_config_nodes: _Optional[_Iterable[_Union[_analysis_pb2_1.AnalysisAlgorithmConfigNode, _Mapping]]] = ..., algorithm_configs: _Optional[_Iterable[_Union[_algorithm_config_pb2.AlgorithmConfig, _Mapping]]] = ..., is_deprecated: bool = ..., is_deactivated: bool = ..., resources_locked: bool = ...) -> None: ...

class AnalysisConfigCreateRequest(_message.Message):
    __slots__ = ("analysis_version_id", "name", "description", "algorithm_config_nodes")
    ANALYSIS_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_NODES_FIELD_NUMBER: _ClassVar[int]
    analysis_version_id: str
    name: str
    description: str
    algorithm_config_nodes: _containers.RepeatedCompositeFieldContainer[_analysis_pb2_1.AnalysisAlgorithmConfigNode]
    def __init__(self, analysis_version_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., algorithm_config_nodes: _Optional[_Iterable[_Union[_analysis_pb2_1.AnalysisAlgorithmConfigNode, _Mapping]]] = ...) -> None: ...

class AnalysisConfigCreateResponse(_message.Message):
    __slots__ = ("status_code", "analysis_config")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_config: AnalysisConfig
    def __init__(self, status_code: _Optional[int] = ..., analysis_config: _Optional[_Union[AnalysisConfig, _Mapping]] = ...) -> None: ...

class AnalysisConfigUpdateRequest(_message.Message):
    __slots__ = ("id", "name", "description", "algorithm_config_nodes")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_NODES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    algorithm_config_nodes: _containers.RepeatedCompositeFieldContainer[_analysis_pb2_1.AnalysisAlgorithmConfigNode]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., algorithm_config_nodes: _Optional[_Iterable[_Union[_analysis_pb2_1.AnalysisAlgorithmConfigNode, _Mapping]]] = ...) -> None: ...

class AnalysisConfigUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class AnalysisConfigGetRequest(_message.Message):
    __slots__ = ("ids", "include_algorithm_details", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ALGORITHM_DETAILS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    include_algorithm_details: bool
    pagination: _common_models_pb2_1_1_1.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., include_algorithm_details: bool = ..., pagination: _Optional[_Union[_common_models_pb2_1_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisConfigGetResponse(_message.Message):
    __slots__ = ("status_code", "analysis_configs", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_configs: _containers.RepeatedCompositeFieldContainer[AnalysisConfig]
    pagination: _common_models_pb2_1_1_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analysis_configs: _Optional[_Iterable[_Union[AnalysisConfig, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisConfigListRequest(_message.Message):
    __slots__ = ("analysis_id", "analysis_version_id", "search_text", "min_created_on", "max_created_on", "include_deactivated", "subject_id", "pagination")
    ANALYSIS_ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    analysis_id: str
    analysis_version_id: str
    search_text: str
    min_created_on: _timestamp_pb2.Timestamp
    max_created_on: _timestamp_pb2.Timestamp
    include_deactivated: bool
    subject_id: str
    pagination: _common_models_pb2_1_1_1.Pagination
    def __init__(self, analysis_id: _Optional[str] = ..., analysis_version_id: _Optional[str] = ..., search_text: _Optional[str] = ..., min_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., include_deactivated: bool = ..., subject_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisConfigListResponse(_message.Message):
    __slots__ = ("status_code", "analysis_configs", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_configs: _containers.RepeatedCompositeFieldContainer[AnalysisConfig]
    pagination: _common_models_pb2_1_1_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analysis_configs: _Optional[_Iterable[_Union[AnalysisConfig, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisConfigDeactivateRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AnalysisConfigDeactivateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
