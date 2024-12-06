from google.protobuf import timestamp_pb2 as _timestamp_pb2
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
import project_filter_pb2 as _project_filter_pb2
import common_models_pb2 as _common_models_pb2_1_1_1_1_1
import filter_pb2 as _filter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
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
from project_filter_pb2 import ProjectFilter as ProjectFilter
from project_filter_pb2 import ProjectFilterMappingCreateRequest as ProjectFilterMappingCreateRequest
from project_filter_pb2 import ProjectFilterMappingCreateResponse as ProjectFilterMappingCreateResponse
from project_filter_pb2 import ProjectFilterMappingDeleteRequest as ProjectFilterMappingDeleteRequest
from project_filter_pb2 import ProjectFilterMappingDeleteResponse as ProjectFilterMappingDeleteResponse

DESCRIPTOR: _descriptor.FileDescriptor

class Project(_message.Message):
    __slots__ = ("id", "name", "description", "creator", "status", "aoi_collections", "analysis_computations", "analysis_configs", "start_date", "end_date", "created_ts", "available_filters", "applied_filters", "time_ranges", "type")
    class ProjectStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_PROJECT_STATUS: _ClassVar[Project.ProjectStatus]
        COMPLETED: _ClassVar[Project.ProjectStatus]
        RUNNING: _ClassVar[Project.ProjectStatus]
        STOPPED: _ClassVar[Project.ProjectStatus]
        NOT_STARTED: _ClassVar[Project.ProjectStatus]
        FAILED: _ClassVar[Project.ProjectStatus]
    UNKNOWN_PROJECT_STATUS: Project.ProjectStatus
    COMPLETED: Project.ProjectStatus
    RUNNING: Project.ProjectStatus
    STOPPED: Project.ProjectStatus
    NOT_STARTED: Project.ProjectStatus
    FAILED: Project.ProjectStatus
    class TimeRange(_message.Message):
        __slots__ = ("start", "end")
        START_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        start: _timestamp_pb2.Timestamp
        end: _timestamp_pb2.Timestamp
        def __init__(self, start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AOI_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_COMPUTATIONS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_TS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    APPLIED_FILTERS_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    creator: str
    status: Project.ProjectStatus
    aoi_collections: _containers.RepeatedCompositeFieldContainer[_aoi_collection_pb2.AOICollection]
    analysis_computations: _containers.RepeatedCompositeFieldContainer[_analysis_computation_pb2.AnalysisComputation]
    analysis_configs: _containers.RepeatedCompositeFieldContainer[_analysis_config_pb2.AnalysisConfig]
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    created_ts: _timestamp_pb2.Timestamp
    available_filters: _containers.RepeatedCompositeFieldContainer[_project_filter_pb2.ProjectFilter]
    applied_filters: _containers.RepeatedCompositeFieldContainer[_project_filter_pb2.ProjectFilter]
    time_ranges: _containers.RepeatedCompositeFieldContainer[Project.TimeRange]
    type: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., creator: _Optional[str] = ..., status: _Optional[_Union[Project.ProjectStatus, str]] = ..., aoi_collections: _Optional[_Iterable[_Union[_aoi_collection_pb2.AOICollection, _Mapping]]] = ..., analysis_computations: _Optional[_Iterable[_Union[_analysis_computation_pb2.AnalysisComputation, _Mapping]]] = ..., analysis_configs: _Optional[_Iterable[_Union[_analysis_config_pb2.AnalysisConfig, _Mapping]]] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., available_filters: _Optional[_Iterable[_Union[_project_filter_pb2.ProjectFilter, _Mapping]]] = ..., applied_filters: _Optional[_Iterable[_Union[_project_filter_pb2.ProjectFilter, _Mapping]]] = ..., time_ranges: _Optional[_Iterable[_Union[Project.TimeRange, _Mapping]]] = ..., type: _Optional[str] = ...) -> None: ...

class ProjectListRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2_1_1_1_1_1.Pagination
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2_1_1_1_1_1.Pagination, _Mapping]] = ...) -> None: ...

class ProjectListResponse(_message.Message):
    __slots__ = ("status_code", "projects", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    projects: _containers.RepeatedCompositeFieldContainer[Project]
    pagination: _common_models_pb2_1_1_1_1_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., projects: _Optional[_Iterable[_Union[Project, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1_1_1_1_1.Pagination, _Mapping]] = ...) -> None: ...

class ProjectGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ProjectGetResponse(_message.Message):
    __slots__ = ("status_code", "project")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    project: Project
    def __init__(self, status_code: _Optional[int] = ..., project: _Optional[_Union[Project, _Mapping]] = ...) -> None: ...

class ProjectCreateRequest(_message.Message):
    __slots__ = ("name", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ProjectCreateResponse(_message.Message):
    __slots__ = ("status_code", "project")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    project: Project
    def __init__(self, status_code: _Optional[int] = ..., project: _Optional[_Union[Project, _Mapping]] = ...) -> None: ...

class ProjectUpdateRequest(_message.Message):
    __slots__ = ("projects",)
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    projects: _containers.RepeatedCompositeFieldContainer[Project]
    def __init__(self, projects: _Optional[_Iterable[_Union[Project, _Mapping]]] = ...) -> None: ...

class ProjectUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class ProjectDeleteRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class ProjectRunRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectRunResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class ProjectCloneRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ProjectCloneResponse(_message.Message):
    __slots__ = ("status_code", "project")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    project: Project
    def __init__(self, status_code: _Optional[int] = ..., project: _Optional[_Union[Project, _Mapping]] = ...) -> None: ...

class ProjectCreditEstimateRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ProjectCreditEstimateResponse(_message.Message):
    __slots__ = ("status_code", "applied_credits", "new_credits", "message", "is_runnable")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    APPLIED_CREDITS_FIELD_NUMBER: _ClassVar[int]
    NEW_CREDITS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IS_RUNNABLE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    applied_credits: float
    new_credits: float
    message: str
    is_runnable: bool
    def __init__(self, status_code: _Optional[int] = ..., applied_credits: _Optional[float] = ..., new_credits: _Optional[float] = ..., message: _Optional[str] = ..., is_runnable: bool = ...) -> None: ...

class ProjectRequestAccessRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ProjectRequestAccessResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
