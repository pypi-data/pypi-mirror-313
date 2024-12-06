from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AOIExportFileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_EXPORT_FILETYPE: _ClassVar[AOIExportFileType]
    GEOJSON: _ClassVar[AOIExportFileType]
    ESRI_SHAPEFILE: _ClassVar[AOIExportFileType]
    GEOPACKAGE: _ClassVar[AOIExportFileType]

class AOIExportArchiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ARCHIVE_TYPE: _ClassVar[AOIExportArchiveType]
    ZIP_FILE: _ClassVar[AOIExportArchiveType]
UNKNOWN_EXPORT_FILETYPE: AOIExportFileType
GEOJSON: AOIExportFileType
ESRI_SHAPEFILE: AOIExportFileType
GEOPACKAGE: AOIExportFileType
UNKNOWN_ARCHIVE_TYPE: AOIExportArchiveType
ZIP_FILE: AOIExportArchiveType

class AOIExportRequest(_message.Message):
    __slots__ = ("aoi_ids", "file_type", "archive_type", "file_name")
    AOI_IDS_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    aoi_ids: _containers.RepeatedScalarFieldContainer[str]
    file_type: AOIExportFileType
    archive_type: AOIExportArchiveType
    file_name: str
    def __init__(self, aoi_ids: _Optional[_Iterable[str]] = ..., file_type: _Optional[_Union[AOIExportFileType, str]] = ..., archive_type: _Optional[_Union[AOIExportArchiveType, str]] = ..., file_name: _Optional[str] = ...) -> None: ...

class AOICollectionExportRequest(_message.Message):
    __slots__ = ("aoi_collection_id", "file_type", "archive_type", "file_name")
    AOI_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    aoi_collection_id: str
    file_type: AOIExportFileType
    archive_type: AOIExportArchiveType
    file_name: str
    def __init__(self, aoi_collection_id: _Optional[str] = ..., file_type: _Optional[_Union[AOIExportFileType, str]] = ..., archive_type: _Optional[_Union[AOIExportArchiveType, str]] = ..., file_name: _Optional[str] = ...) -> None: ...

class AOIExportResponse(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: str
    def __init__(self, location: _Optional[str] = ...) -> None: ...

class AOICollectionExportResponse(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: str
    def __init__(self, location: _Optional[str] = ...) -> None: ...
