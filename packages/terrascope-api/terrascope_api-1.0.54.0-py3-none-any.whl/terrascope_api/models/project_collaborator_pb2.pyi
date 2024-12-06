import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectCollaborator(_message.Message):
    __slots__ = ("user_id", "role", "customer_id", "name")
    class ProjectRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_PROJECT_ROLE: _ClassVar[ProjectCollaborator.ProjectRole]
        CREATOR: _ClassVar[ProjectCollaborator.ProjectRole]
        COLLABORATOR: _ClassVar[ProjectCollaborator.ProjectRole]
        VIEWER: _ClassVar[ProjectCollaborator.ProjectRole]
    UNKNOWN_PROJECT_ROLE: ProjectCollaborator.ProjectRole
    CREATOR: ProjectCollaborator.ProjectRole
    COLLABORATOR: ProjectCollaborator.ProjectRole
    VIEWER: ProjectCollaborator.ProjectRole
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    role: ProjectCollaborator.ProjectRole
    customer_id: str
    name: str
    def __init__(self, user_id: _Optional[str] = ..., role: _Optional[_Union[ProjectCollaborator.ProjectRole, str]] = ..., customer_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ProjectCollaboratorGetRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ProjectCollaboratorGetResponse(_message.Message):
    __slots__ = ("status_code", "project_collaborators")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_COLLABORATORS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    project_collaborators: _containers.RepeatedCompositeFieldContainer[ProjectCollaborator]
    def __init__(self, status_code: _Optional[int] = ..., project_collaborators: _Optional[_Iterable[_Union[ProjectCollaborator, _Mapping]]] = ...) -> None: ...

class ProjectCollaboratorUpdateRequest(_message.Message):
    __slots__ = ("project_id", "project_collaborators")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_COLLABORATORS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    project_collaborators: _containers.RepeatedCompositeFieldContainer[ProjectCollaborator]
    def __init__(self, project_id: _Optional[str] = ..., project_collaborators: _Optional[_Iterable[_Union[ProjectCollaborator, _Mapping]]] = ...) -> None: ...

class ProjectCollaboratorUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class ProjectCollaboratorDeleteRequest(_message.Message):
    __slots__ = ("project_id", "user_ids")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project_id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectCollaboratorDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
