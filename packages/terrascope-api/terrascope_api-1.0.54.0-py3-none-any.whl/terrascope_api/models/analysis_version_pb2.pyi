from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
import analysis_pb2 as _analysis_pb2
import common_models_pb2 as _common_models_pb2_1
import algorithm_version_pb2 as _algorithm_version_pb2
import common_models_pb2 as _common_models_pb2_1_1
import algorithm_pb2 as _algorithm_pb2
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

class AnalysisManifest(_message.Message):
    __slots__ = ("manifest_version", "metadata", "algorithm_nodes")
    class Metadata(_message.Message):
        __slots__ = ("description", "version", "tags")
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        description: str
        version: str
        tags: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, description: _Optional[str] = ..., version: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
    MANIFEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_NODES_FIELD_NUMBER: _ClassVar[int]
    manifest_version: str
    metadata: AnalysisManifest.Metadata
    algorithm_nodes: _containers.RepeatedCompositeFieldContainer[_analysis_pb2.AnalysisAlgorithmNode]
    def __init__(self, manifest_version: _Optional[str] = ..., metadata: _Optional[_Union[AnalysisManifest.Metadata, _Mapping]] = ..., algorithm_nodes: _Optional[_Iterable[_Union[_analysis_pb2.AnalysisAlgorithmNode, _Mapping]]] = ...) -> None: ...

class AnalysisVersion(_message.Message):
    __slots__ = ("id", "analysis", "analysis_manifest", "created_on", "algorithm_versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    analysis: _analysis_pb2.Analysis
    analysis_manifest: AnalysisManifest
    created_on: _timestamp_pb2.Timestamp
    algorithm_versions: _containers.RepeatedCompositeFieldContainer[_algorithm_version_pb2.AlgorithmVersion]
    def __init__(self, id: _Optional[str] = ..., analysis: _Optional[_Union[_analysis_pb2.Analysis, _Mapping]] = ..., analysis_manifest: _Optional[_Union[AnalysisManifest, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., algorithm_versions: _Optional[_Iterable[_Union[_algorithm_version_pb2.AlgorithmVersion, _Mapping]]] = ...) -> None: ...

class AnalysisVersionCreateRequest(_message.Message):
    __slots__ = ("analysis_id", "analysis_manifest")
    ANALYSIS_ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    analysis_id: str
    analysis_manifest: AnalysisManifest
    def __init__(self, analysis_id: _Optional[str] = ..., analysis_manifest: _Optional[_Union[AnalysisManifest, _Mapping]] = ...) -> None: ...

class AnalysisVersionCreateResponse(_message.Message):
    __slots__ = ("status_code", "analysis_version")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_VERSION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_version: AnalysisVersion
    def __init__(self, status_code: _Optional[int] = ..., analysis_version: _Optional[_Union[AnalysisVersion, _Mapping]] = ...) -> None: ...

class AnalysisVersionGetRequest(_message.Message):
    __slots__ = ("ids", "include_manifest", "include_algorithm_details", "pagination")
    IDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ALGORITHM_DETAILS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    include_manifest: bool
    include_algorithm_details: bool
    pagination: _common_models_pb2_1_1.Pagination
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., include_manifest: bool = ..., include_algorithm_details: bool = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisVersionGetResponse(_message.Message):
    __slots__ = ("status_code", "analysis_versions", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_versions: _containers.RepeatedCompositeFieldContainer[AnalysisVersion]
    pagination: _common_models_pb2_1_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analysis_versions: _Optional[_Iterable[_Union[AnalysisVersion, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisVersionListRequest(_message.Message):
    __slots__ = ("analysis_id", "tag", "search_text", "min_created_on", "max_created_on", "include_manifest", "include_all_versions", "pagination")
    ANALYSIS_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ALL_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    analysis_id: str
    tag: str
    search_text: str
    min_created_on: _timestamp_pb2.Timestamp
    max_created_on: _timestamp_pb2.Timestamp
    include_manifest: bool
    include_all_versions: bool
    pagination: _common_models_pb2_1_1.Pagination
    def __init__(self, analysis_id: _Optional[str] = ..., tag: _Optional[str] = ..., search_text: _Optional[str] = ..., min_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., include_manifest: bool = ..., include_all_versions: bool = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ...) -> None: ...

class AnalysisVersionListResponse(_message.Message):
    __slots__ = ("status_code", "analysis_versions", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    analysis_versions: _containers.RepeatedCompositeFieldContainer[AnalysisVersion]
    pagination: _common_models_pb2_1_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., analysis_versions: _Optional[_Iterable[_Union[AnalysisVersion, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1.Pagination, _Mapping]] = ...) -> None: ...
