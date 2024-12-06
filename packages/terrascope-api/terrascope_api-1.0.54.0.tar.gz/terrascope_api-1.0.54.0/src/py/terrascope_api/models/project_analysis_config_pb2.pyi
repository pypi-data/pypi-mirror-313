import common_models_pb2 as _common_models_pb2
import analysis_config_pb2 as _analysis_config_pb2
import common_models_pb2 as _common_models_pb2_1
import analysis_pb2 as _analysis_pb2
import analysis_version_pb2 as _analysis_version_pb2
import algorithm_config_pb2 as _algorithm_config_pb2
import analysis_computation_pb2 as _analysis_computation_pb2
import common_models_pb2 as _common_models_pb2_1_1
import analysis_pb2 as _analysis_pb2_1
import aoi_collection_pb2 as _aoi_collection_pb2
import common_models_pb2 as _common_models_pb2_1_1_1
import result_pb2 as _result_pb2
import common_models_pb2 as _common_models_pb2_1_1_1_1
import toi_pb2 as _toi_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
from common_models_pb2 import Pagination as Pagination
from analysis_config_pb2 import AnalysisConfig as AnalysisConfig
from analysis_config_pb2 import AnalysisConfigCreateRequest as AnalysisConfigCreateRequest
from analysis_config_pb2 import AnalysisConfigCreateResponse as AnalysisConfigCreateResponse
from analysis_config_pb2 import AnalysisConfigUpdateRequest as AnalysisConfigUpdateRequest
from analysis_config_pb2 import AnalysisConfigUpdateResponse as AnalysisConfigUpdateResponse
from analysis_config_pb2 import AnalysisConfigGetRequest as AnalysisConfigGetRequest
from analysis_config_pb2 import AnalysisConfigGetResponse as AnalysisConfigGetResponse
from analysis_config_pb2 import AnalysisConfigListRequest as AnalysisConfigListRequest
from analysis_config_pb2 import AnalysisConfigListResponse as AnalysisConfigListResponse
from analysis_config_pb2 import AnalysisConfigDeactivateRequest as AnalysisConfigDeactivateRequest
from analysis_config_pb2 import AnalysisConfigDeactivateResponse as AnalysisConfigDeactivateResponse
from analysis_computation_pb2 import AnalysisComputationCreateRequest as AnalysisComputationCreateRequest
from analysis_computation_pb2 import AnalysisComputationCreateResponse as AnalysisComputationCreateResponse
from analysis_computation_pb2 import AnalysisComputationRunRequest as AnalysisComputationRunRequest
from analysis_computation_pb2 import AnalysisComputationRunResponse as AnalysisComputationRunResponse
from analysis_computation_pb2 import AnalysisComputationGetRequest as AnalysisComputationGetRequest
from analysis_computation_pb2 import AnalysisComputationNode as AnalysisComputationNode
from analysis_computation_pb2 import AnalysisComputation as AnalysisComputation
from analysis_computation_pb2 import AnalysisComputationGetResponse as AnalysisComputationGetResponse
from analysis_computation_pb2 import AnalysisComputationListRequest as AnalysisComputationListRequest
from analysis_computation_pb2 import AnalysisComputationListResponse as AnalysisComputationListResponse
from aoi_collection_pb2 import AOICollection as AOICollection
from aoi_collection_pb2 import AOIInfo as AOIInfo
from aoi_collection_pb2 import AOICollectionCreateRequest as AOICollectionCreateRequest
from aoi_collection_pb2 import AOICollectionCreateResponse as AOICollectionCreateResponse
from aoi_collection_pb2 import AOICollectionGetRequest as AOICollectionGetRequest
from aoi_collection_pb2 import AOICollectionGetResponse as AOICollectionGetResponse
from aoi_collection_pb2 import AOICollectionAddRequest as AOICollectionAddRequest
from aoi_collection_pb2 import AOICollectionAddResponse as AOICollectionAddResponse
from aoi_collection_pb2 import AOICollectionRemoveRequest as AOICollectionRemoveRequest
from aoi_collection_pb2 import AOICollectionRemoveResponse as AOICollectionRemoveResponse
from aoi_collection_pb2 import AOICollectionCloneRequest as AOICollectionCloneRequest
from aoi_collection_pb2 import AOICollectionCloneResponse as AOICollectionCloneResponse
from aoi_collection_pb2 import AOICollectionListRequest as AOICollectionListRequest
from aoi_collection_pb2 import AOICollectionListResponse as AOICollectionListResponse
from result_pb2 import ExportFile as ExportFile
from result_pb2 import ExportCredentials as ExportCredentials
from result_pb2 import Result as Result
from result_pb2 import ResultGetRequest as ResultGetRequest
from result_pb2 import ResultGetResponse as ResultGetResponse

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectAnalysisConfigUpdateRequest(_message.Message):
    __slots__ = ("project_id", "analysis_config_ids")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIG_IDS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    analysis_config_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project_id: _Optional[str] = ..., analysis_config_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectAnalysisConfigUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
