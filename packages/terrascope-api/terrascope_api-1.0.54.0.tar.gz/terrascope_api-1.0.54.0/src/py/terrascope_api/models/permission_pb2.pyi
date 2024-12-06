import common_models_pb2 as _common_models_pb2
import resource_pb2 as _resource_pb2
import common_models_pb2 as _common_models_pb2_1
import subject_pb2 as _subject_pb2
import subject_pb2 as _subject_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from resource_pb2 import ResourceRegisterTypeRequest as ResourceRegisterTypeRequest
from resource_pb2 import ResourceRegisterTypeResponse as ResourceRegisterTypeResponse
from resource_pb2 import ResourceTypesListRequest as ResourceTypesListRequest
from resource_pb2 import ResourceTypesListResponse as ResourceTypesListResponse
from resource_pb2 import Resource as Resource
from resource_pb2 import ResourceCreateRequest as ResourceCreateRequest
from resource_pb2 import ResourceCreateResponse as ResourceCreateResponse
from resource_pb2 import ResourceListRequest as ResourceListRequest
from resource_pb2 import ResourceListResponse as ResourceListResponse
from subject_pb2 import Subject as Subject

DESCRIPTOR: _descriptor.FileDescriptor

class Permission(_message.Message):
    __slots__ = ("subjects", "permission_types", "resources")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PERMISSION_TYPE_UNKNOWN: _ClassVar[Permission.Type]
        READ: _ClassVar[Permission.Type]
        WRITE: _ClassVar[Permission.Type]
        ADMIN: _ClassVar[Permission.Type]
        EXECUTE: _ClassVar[Permission.Type]
        ORDER: _ClassVar[Permission.Type]
        ORDER_APPROVER: _ClassVar[Permission.Type]
    PERMISSION_TYPE_UNKNOWN: Permission.Type
    READ: Permission.Type
    WRITE: Permission.Type
    ADMIN: Permission.Type
    EXECUTE: Permission.Type
    ORDER: Permission.Type
    ORDER_APPROVER: Permission.Type
    SUBJECTS_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPES_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    subjects: _containers.RepeatedCompositeFieldContainer[_subject_pb2_1.Subject]
    permission_types: _containers.RepeatedScalarFieldContainer[Permission.Type]
    resources: _containers.RepeatedCompositeFieldContainer[_resource_pb2.Resource]
    def __init__(self, subjects: _Optional[_Iterable[_Union[_subject_pb2_1.Subject, _Mapping]]] = ..., permission_types: _Optional[_Iterable[_Union[Permission.Type, str]]] = ..., resources: _Optional[_Iterable[_Union[_resource_pb2.Resource, _Mapping]]] = ...) -> None: ...

class PermissionCreateRequest(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

class PermissionCreateResponse(_message.Message):
    __slots__ = ("status_code", "message")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    message: str
    def __init__(self, status_code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class PermissionDeleteRequest(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

class PermissionDeleteResponse(_message.Message):
    __slots__ = ("status_code", "message")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    message: str
    def __init__(self, status_code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class PermissionGetRequest(_message.Message):
    __slots__ = ("resources", "permission_type", "subject")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[_resource_pb2.Resource]
    permission_type: Permission.Type
    subject: _subject_pb2_1.Subject
    def __init__(self, resources: _Optional[_Iterable[_Union[_resource_pb2.Resource, _Mapping]]] = ..., permission_type: _Optional[_Union[Permission.Type, str]] = ..., subject: _Optional[_Union[_subject_pb2_1.Subject, _Mapping]] = ...) -> None: ...

class PermissionGetResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class PermissionListRequest(_message.Message):
    __slots__ = ("resources", "permission_types", "subject")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPES_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[_resource_pb2.Resource]
    permission_types: _containers.RepeatedScalarFieldContainer[Permission.Type]
    subject: _subject_pb2_1.Subject
    def __init__(self, resources: _Optional[_Iterable[_Union[_resource_pb2.Resource, _Mapping]]] = ..., permission_types: _Optional[_Iterable[_Union[Permission.Type, str]]] = ..., subject: _Optional[_Union[_subject_pb2_1.Subject, _Mapping]] = ...) -> None: ...

class PermissionList(_message.Message):
    __slots__ = ("permission_type", "resources")
    PERMISSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    permission_type: Permission.Type
    resources: _containers.RepeatedCompositeFieldContainer[_resource_pb2.Resource]
    def __init__(self, permission_type: _Optional[_Union[Permission.Type, str]] = ..., resources: _Optional[_Iterable[_Union[_resource_pb2.Resource, _Mapping]]] = ...) -> None: ...

class PermissionListResponse(_message.Message):
    __slots__ = ("status_code", "permission_and_resources")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_AND_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    permission_and_resources: _containers.RepeatedCompositeFieldContainer[PermissionList]
    def __init__(self, status_code: _Optional[int] = ..., permission_and_resources: _Optional[_Iterable[_Union[PermissionList, _Mapping]]] = ...) -> None: ...

class PermissionSystemMetadata(_message.Message):
    __slots__ = ("resource_types_metadata", "permission_types_metadata", "resource_permissions")
    class ResourceTypeMetadata(_message.Message):
        __slots__ = ("name", "display_name", "description", "ord")
        NAME_FIELD_NUMBER: _ClassVar[int]
        DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ORD_FIELD_NUMBER: _ClassVar[int]
        name: str
        display_name: str
        description: str
        ord: int
        def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., ord: _Optional[int] = ...) -> None: ...
    class PermissionTypeMetadata(_message.Message):
        __slots__ = ("name", "display_name", "description", "ord")
        NAME_FIELD_NUMBER: _ClassVar[int]
        DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ORD_FIELD_NUMBER: _ClassVar[int]
        name: str
        display_name: str
        description: str
        ord: int
        def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., ord: _Optional[int] = ...) -> None: ...
    class ResourcePermission(_message.Message):
        __slots__ = ("resource_type", "permission_type", "description")
        RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PERMISSION_TYPE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        resource_type: str
        permission_type: str
        description: str
        def __init__(self, resource_type: _Optional[str] = ..., permission_type: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
    RESOURCE_TYPES_METADATA_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPES_METADATA_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    resource_types_metadata: _containers.RepeatedCompositeFieldContainer[PermissionSystemMetadata.ResourceTypeMetadata]
    permission_types_metadata: _containers.RepeatedCompositeFieldContainer[PermissionSystemMetadata.PermissionTypeMetadata]
    resource_permissions: _containers.RepeatedCompositeFieldContainer[PermissionSystemMetadata.ResourcePermission]
    def __init__(self, resource_types_metadata: _Optional[_Iterable[_Union[PermissionSystemMetadata.ResourceTypeMetadata, _Mapping]]] = ..., permission_types_metadata: _Optional[_Iterable[_Union[PermissionSystemMetadata.PermissionTypeMetadata, _Mapping]]] = ..., resource_permissions: _Optional[_Iterable[_Union[PermissionSystemMetadata.ResourcePermission, _Mapping]]] = ...) -> None: ...

class PermissionGetMetadataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PermissionGetMetadataResponse(_message.Message):
    __slots__ = ("status_code", "metadata")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    metadata: PermissionSystemMetadata
    def __init__(self, status_code: _Optional[int] = ..., metadata: _Optional[_Union[PermissionSystemMetadata, _Mapping]] = ...) -> None: ...
