import common_models_pb2 as _common_models_pb2
import project_pb2 as _project_pb2
import common_models_pb2 as _common_models_pb2_1
import analysis_config_pb2 as _analysis_config_pb2
import analysis_computation_pb2 as _analysis_computation_pb2
import aoi_collection_pb2 as _aoi_collection_pb2
import result_pb2 as _result_pb2
import project_filter_pb2 as _project_filter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from project_pb2 import Project as Project
from project_pb2 import ProjectListRequest as ProjectListRequest
from project_pb2 import ProjectListResponse as ProjectListResponse
from project_pb2 import ProjectGetRequest as ProjectGetRequest
from project_pb2 import ProjectGetResponse as ProjectGetResponse
from project_pb2 import ProjectCreateRequest as ProjectCreateRequest
from project_pb2 import ProjectCreateResponse as ProjectCreateResponse
from project_pb2 import ProjectUpdateRequest as ProjectUpdateRequest
from project_pb2 import ProjectUpdateResponse as ProjectUpdateResponse
from project_pb2 import ProjectDeleteRequest as ProjectDeleteRequest
from project_pb2 import ProjectDeleteResponse as ProjectDeleteResponse
from project_pb2 import ProjectRunRequest as ProjectRunRequest
from project_pb2 import ProjectRunResponse as ProjectRunResponse
from project_pb2 import ProjectCloneRequest as ProjectCloneRequest
from project_pb2 import ProjectCloneResponse as ProjectCloneResponse
from project_pb2 import ProjectCreditEstimateRequest as ProjectCreditEstimateRequest
from project_pb2 import ProjectCreditEstimateResponse as ProjectCreditEstimateResponse
from project_pb2 import ProjectRequestAccessRequest as ProjectRequestAccessRequest
from project_pb2 import ProjectRequestAccessResponse as ProjectRequestAccessResponse

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectGroup(_message.Message):
    __slots__ = ("id", "name", "projects", "collapsed", "sort_order")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    COLLAPSED_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    projects: _containers.RepeatedCompositeFieldContainer[_project_pb2.Project]
    collapsed: bool
    sort_order: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., projects: _Optional[_Iterable[_Union[_project_pb2.Project, _Mapping]]] = ..., collapsed: bool = ..., sort_order: _Optional[int] = ...) -> None: ...

class ProjectGroupListRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class ProjectGroupListResponse(_message.Message):
    __slots__ = ("status_code", "project_groups", "pagination")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_GROUPS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    project_groups: _containers.RepeatedCompositeFieldContainer[ProjectGroup]
    pagination: _common_models_pb2_1.Pagination
    def __init__(self, status_code: _Optional[int] = ..., project_groups: _Optional[_Iterable[_Union[ProjectGroup, _Mapping]]] = ..., pagination: _Optional[_Union[_common_models_pb2_1.Pagination, _Mapping]] = ...) -> None: ...

class ProjectGroupCreateRequest(_message.Message):
    __slots__ = ("name", "project_ids")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_IDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    project_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., project_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectGroupCreateResponse(_message.Message):
    __slots__ = ("status_code", "project_group")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_GROUP_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    project_group: ProjectGroup
    def __init__(self, status_code: _Optional[int] = ..., project_group: _Optional[_Union[ProjectGroup, _Mapping]] = ...) -> None: ...

class ProjectGroupDeleteRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectGroupDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class ProjectGroupUpdateRequest(_message.Message):
    __slots__ = ("project_groups", "update_projects", "update_details")
    PROJECT_GROUPS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PROJECTS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DETAILS_FIELD_NUMBER: _ClassVar[int]
    project_groups: _containers.RepeatedCompositeFieldContainer[ProjectGroup]
    update_projects: bool
    update_details: bool
    def __init__(self, project_groups: _Optional[_Iterable[_Union[ProjectGroup, _Mapping]]] = ..., update_projects: bool = ..., update_details: bool = ...) -> None: ...

class ProjectGroupUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
