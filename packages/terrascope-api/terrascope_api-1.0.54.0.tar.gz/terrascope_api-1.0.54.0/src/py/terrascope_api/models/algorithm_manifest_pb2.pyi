from google.protobuf import struct_pb2 as _struct_pb2
import common_models_pb2 as _common_models_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class AlgorithmManifestSchemaGetRequest(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    def __init__(self, version: _Optional[str] = ...) -> None: ...

class AlgorithmManifestSchemaGetResponse(_message.Message):
    __slots__ = ("status_code", "version", "schema")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    version: str
    schema: _struct_pb2.Struct
    def __init__(self, status_code: _Optional[int] = ..., version: _Optional[str] = ..., schema: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
