from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(_message.Message):
    __slots__ = ("name", "description", "schema", "data_source_ids", "sensor_type", "query_schema")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUERY_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    schema: str
    data_source_ids: _containers.RepeatedScalarFieldContainer[str]
    sensor_type: str
    query_schema: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., schema: _Optional[str] = ..., data_source_ids: _Optional[_Iterable[str]] = ..., sensor_type: _Optional[str] = ..., query_schema: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DataTypeCreateRequest(_message.Message):
    __slots__ = ("name", "description", "schema", "sensor_type", "query_schema")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUERY_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    schema: str
    sensor_type: str
    query_schema: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., schema: _Optional[str] = ..., sensor_type: _Optional[str] = ..., query_schema: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DataTypeCreateResponse(_message.Message):
    __slots__ = ("status_code", "data_type")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    data_type: DataType
    def __init__(self, status_code: _Optional[int] = ..., data_type: _Optional[_Union[DataType, _Mapping]] = ...) -> None: ...

class DataTypeGetRequest(_message.Message):
    __slots__ = ("names",)
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...

class DataTypeGetResponse(_message.Message):
    __slots__ = ("status_code", "data_types")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    data_types: _containers.RepeatedCompositeFieldContainer[DataType]
    def __init__(self, status_code: _Optional[int] = ..., data_types: _Optional[_Iterable[_Union[DataType, _Mapping]]] = ...) -> None: ...

class DataTypeListRequest(_message.Message):
    __slots__ = ("search_text",)
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    def __init__(self, search_text: _Optional[str] = ...) -> None: ...

class DataTypeListResponse(_message.Message):
    __slots__ = ("status_code", "data_types")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    data_types: _containers.RepeatedCompositeFieldContainer[DataType]
    def __init__(self, status_code: _Optional[int] = ..., data_types: _Optional[_Iterable[_Union[DataType, _Mapping]]] = ...) -> None: ...
