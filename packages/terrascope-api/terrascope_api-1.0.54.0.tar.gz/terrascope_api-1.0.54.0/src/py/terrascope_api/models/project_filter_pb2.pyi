import common_models_pb2 as _common_models_pb2
import filter_pb2 as _filter_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from filter_pb2 import FilterCreateRequest as FilterCreateRequest
from filter_pb2 import FilterCreateResponse as FilterCreateResponse
from filter_pb2 import FilterDeleteRequest as FilterDeleteRequest
from filter_pb2 import FilterDeleteResponse as FilterDeleteResponse
from filter_pb2 import FilterMappingCreateRequest as FilterMappingCreateRequest
from filter_pb2 import FilterMappingCreateResponse as FilterMappingCreateResponse
from filter_pb2 import FilterListRequest as FilterListRequest
from filter_pb2 import Filter as Filter
from filter_pb2 import FilterListResponse as FilterListResponse

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectFilter(_message.Message):
    __slots__ = ("filter", "analysis_config_id", "node_name", "project_id")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    filter: _filter_pb2.Filter
    analysis_config_id: str
    node_name: str
    project_id: str
    def __init__(self, filter: _Optional[_Union[_filter_pb2.Filter, _Mapping]] = ..., analysis_config_id: _Optional[str] = ..., node_name: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class ProjectFilterMappingCreateRequest(_message.Message):
    __slots__ = ("project_filters",)
    PROJECT_FILTERS_FIELD_NUMBER: _ClassVar[int]
    project_filters: _containers.RepeatedCompositeFieldContainer[ProjectFilter]
    def __init__(self, project_filters: _Optional[_Iterable[_Union[ProjectFilter, _Mapping]]] = ...) -> None: ...

class ProjectFilterMappingCreateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class ProjectFilterMappingDeleteRequest(_message.Message):
    __slots__ = ("project_filters",)
    PROJECT_FILTERS_FIELD_NUMBER: _ClassVar[int]
    project_filters: _containers.RepeatedCompositeFieldContainer[ProjectFilter]
    def __init__(self, project_filters: _Optional[_Iterable[_Union[ProjectFilter, _Mapping]]] = ...) -> None: ...

class ProjectFilterMappingDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
