import common_models_pb2 as _common_models_pb2
import subject_pb2 as _subject_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from subject_pb2 import Subject as Subject

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceRegisterTypeRequest(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class ResourceRegisterTypeResponse(_message.Message):
    __slots__ = ("status_code", "value", "already_existed")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ALREADY_EXISTED_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    value: int
    already_existed: bool
    def __init__(self, status_code: _Optional[int] = ..., value: _Optional[int] = ..., already_existed: bool = ...) -> None: ...

class ResourceTypesListRequest(_message.Message):
    __slots__ = ("value", "name", "regex")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REGEX_FIELD_NUMBER: _ClassVar[int]
    value: int
    name: str
    regex: bool
    def __init__(self, value: _Optional[int] = ..., name: _Optional[str] = ..., regex: bool = ...) -> None: ...

class ResourceTypesListResponse(_message.Message):
    __slots__ = ("type_to_name",)
    class TypeToNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    TYPE_TO_NAME_FIELD_NUMBER: _ClassVar[int]
    type_to_name: _containers.ScalarMap[int, str]
    def __init__(self, type_to_name: _Optional[_Mapping[int, str]] = ...) -> None: ...

class Resource(_message.Message):
    __slots__ = ("id", "type")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PERMISSION_RESOURCE_TYPE_UNKNOWN: _ClassVar[Resource.Type]
        ALGORITHM: _ClassVar[Resource.Type]
        ALGORITHM_COMPUTATION: _ClassVar[Resource.Type]
        ALGORITHM_CONFIG: _ClassVar[Resource.Type]
        ANALYSIS: _ClassVar[Resource.Type]
        ANALYSIS_COMPUTATION: _ClassVar[Resource.Type]
        ANALYSIS_CONFIG: _ClassVar[Resource.Type]
        AOI_COLLECTION: _ClassVar[Resource.Type]
        RESULT: _ClassVar[Resource.Type]
        TOI: _ClassVar[Resource.Type]
        DIRECT_RANGE_START: _ClassVar[Resource.Type]
        DATA_SOURCE: _ClassVar[Resource.Type]
        DATA_SOURCES: _ClassVar[Resource.Type]
        APPLICATION_RANGE_START: _ClassVar[Resource.Type]
        MOBILE_WORKFORCE_TASK: _ClassVar[Resource.Type]
        MOBILE_WORKFORCE_CAMPAIGN: _ClassVar[Resource.Type]
    PERMISSION_RESOURCE_TYPE_UNKNOWN: Resource.Type
    ALGORITHM: Resource.Type
    ALGORITHM_COMPUTATION: Resource.Type
    ALGORITHM_CONFIG: Resource.Type
    ANALYSIS: Resource.Type
    ANALYSIS_COMPUTATION: Resource.Type
    ANALYSIS_CONFIG: Resource.Type
    AOI_COLLECTION: Resource.Type
    RESULT: Resource.Type
    TOI: Resource.Type
    DIRECT_RANGE_START: Resource.Type
    DATA_SOURCE: Resource.Type
    DATA_SOURCES: Resource.Type
    APPLICATION_RANGE_START: Resource.Type
    MOBILE_WORKFORCE_TASK: Resource.Type
    MOBILE_WORKFORCE_CAMPAIGN: Resource.Type
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: Resource.Type
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[Resource.Type, str]] = ...) -> None: ...

class ResourceCreateRequest(_message.Message):
    __slots__ = ("resources", "parent")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[Resource]
    parent: Resource
    def __init__(self, resources: _Optional[_Iterable[_Union[Resource, _Mapping]]] = ..., parent: _Optional[_Union[Resource, _Mapping]] = ...) -> None: ...

class ResourceCreateResponse(_message.Message):
    __slots__ = ("status_code", "resources", "message")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    resources: _containers.RepeatedCompositeFieldContainer[Resource]
    message: str
    def __init__(self, status_code: _Optional[int] = ..., resources: _Optional[_Iterable[_Union[Resource, _Mapping]]] = ..., message: _Optional[str] = ...) -> None: ...

class ResourceListRequest(_message.Message):
    __slots__ = ("type", "permission_types", "parent", "subject")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPES_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    type: Resource.Type
    permission_types: _containers.RepeatedScalarFieldContainer[int]
    parent: Resource
    subject: _subject_pb2.Subject
    def __init__(self, type: _Optional[_Union[Resource.Type, str]] = ..., permission_types: _Optional[_Iterable[int]] = ..., parent: _Optional[_Union[Resource, _Mapping]] = ..., subject: _Optional[_Union[_subject_pb2.Subject, _Mapping]] = ...) -> None: ...

class ResourceListResponse(_message.Message):
    __slots__ = ("status_code", "resources")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    resources: _containers.RepeatedCompositeFieldContainer[Resource]
    def __init__(self, status_code: _Optional[int] = ..., resources: _Optional[_Iterable[_Union[Resource, _Mapping]]] = ...) -> None: ...
