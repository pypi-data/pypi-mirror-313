from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Visualization(_message.Message):
    __slots__ = ("id", "computation_id", "result_observation_id", "type", "state", "metadata", "observation_metadata", "access_info", "created_on", "updated_on", "visualizer_config_id", "data_type_name")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_TYPE: _ClassVar[Visualization.Type]
        STANDARD: _ClassVar[Visualization.Type]
        SPATIAL: _ClassVar[Visualization.Type]
        TEMPORAL: _ClassVar[Visualization.Type]
        RASTER: _ClassVar[Visualization.Type]
        VIDEO_JSON: _ClassVar[Visualization.Type]
    UNKNOWN_TYPE: Visualization.Type
    STANDARD: Visualization.Type
    SPATIAL: Visualization.Type
    TEMPORAL: Visualization.Type
    RASTER: Visualization.Type
    VIDEO_JSON: Visualization.Type
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_STATE: _ClassVar[Visualization.State]
        NEW: _ClassVar[Visualization.State]
        QUEUED: _ClassVar[Visualization.State]
        VALIDATING: _ClassVar[Visualization.State]
        EMPTY: _ClassVar[Visualization.State]
        UPLOADED: _ClassVar[Visualization.State]
        FAILED: _ClassVar[Visualization.State]
        DELETING: _ClassVar[Visualization.State]
        DELETED: _ClassVar[Visualization.State]
    UNKNOWN_STATE: Visualization.State
    NEW: Visualization.State
    QUEUED: Visualization.State
    VALIDATING: Visualization.State
    EMPTY: Visualization.State
    UPLOADED: Visualization.State
    FAILED: Visualization.State
    DELETING: Visualization.State
    DELETED: Visualization.State
    class AccessInfo(_message.Message):
        __slots__ = ("url_template", "credentials")
        URL_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
        CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
        url_template: str
        credentials: _struct_pb2.Struct
        def __init__(self, url_template: _Optional[str] = ..., credentials: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_OBSERVATION_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OBSERVATION_METADATA_FIELD_NUMBER: _ClassVar[int]
    ACCESS_INFO_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
    VISUALIZER_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    computation_id: str
    result_observation_id: str
    type: Visualization.Type
    state: Visualization.State
    metadata: _struct_pb2.Struct
    observation_metadata: _struct_pb2.Struct
    access_info: Visualization.AccessInfo
    created_on: _timestamp_pb2.Timestamp
    updated_on: _timestamp_pb2.Timestamp
    visualizer_config_id: str
    data_type_name: str
    def __init__(self, id: _Optional[str] = ..., computation_id: _Optional[str] = ..., result_observation_id: _Optional[str] = ..., type: _Optional[_Union[Visualization.Type, str]] = ..., state: _Optional[_Union[Visualization.State, str]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., observation_metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., access_info: _Optional[_Union[Visualization.AccessInfo, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., visualizer_config_id: _Optional[str] = ..., data_type_name: _Optional[str] = ...) -> None: ...

class VisualizationGetRequest(_message.Message):
    __slots__ = ("result_observation_ids",)
    RESULT_OBSERVATION_IDS_FIELD_NUMBER: _ClassVar[int]
    result_observation_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, result_observation_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class VisualizationGetResponse(_message.Message):
    __slots__ = ("status_code", "visualizations", "base_url_template")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    VISUALIZATIONS_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    visualizations: _containers.RepeatedCompositeFieldContainer[Visualization]
    base_url_template: str
    def __init__(self, status_code: _Optional[int] = ..., visualizations: _Optional[_Iterable[_Union[Visualization, _Mapping]]] = ..., base_url_template: _Optional[str] = ...) -> None: ...

class Visualizer(_message.Message):
    __slots__ = ("id", "name", "visualizer_type", "data_types")
    class VisualizerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_VISUALIZER_TYPE: _ClassVar[Visualizer.VisualizerType]
        KEPLER: _ClassVar[Visualizer.VisualizerType]
        OI_VISUALIZATION_SERVICE: _ClassVar[Visualizer.VisualizerType]
        UI_TERRASCOPE_RESULTS: _ClassVar[Visualizer.VisualizerType]
    UNKNOWN_VISUALIZER_TYPE: Visualizer.VisualizerType
    KEPLER: Visualizer.VisualizerType
    OI_VISUALIZATION_SERVICE: Visualizer.VisualizerType
    UI_TERRASCOPE_RESULTS: Visualizer.VisualizerType
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VISUALIZER_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    visualizer_type: Visualizer.VisualizerType
    data_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., visualizer_type: _Optional[_Union[Visualizer.VisualizerType, str]] = ..., data_types: _Optional[_Iterable[str]] = ...) -> None: ...

class VisualizerConfig(_message.Message):
    __slots__ = ("id", "config", "visualizer")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    VISUALIZER_FIELD_NUMBER: _ClassVar[int]
    id: str
    config: _struct_pb2.Struct
    visualizer: Visualizer
    def __init__(self, id: _Optional[str] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., visualizer: _Optional[_Union[Visualizer, _Mapping]] = ...) -> None: ...

class VisualizerConfigAlgoVersionCreateRequest(_message.Message):
    __slots__ = ("visualizer_config_id", "algorithm_version_id")
    VISUALIZER_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    visualizer_config_id: str
    algorithm_version_id: str
    def __init__(self, visualizer_config_id: _Optional[str] = ..., algorithm_version_id: _Optional[str] = ...) -> None: ...

class VisualizerConfigAlgoVersionCreateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class VisualizerConfigAlgoGetRequest(_message.Message):
    __slots__ = ("algorithm_config_ids",)
    ALGORITHM_CONFIG_IDS_FIELD_NUMBER: _ClassVar[int]
    algorithm_config_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, algorithm_config_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class VisualizerConfigAlgo(_message.Message):
    __slots__ = ("algorithm_version_id", "visualizer_configs", "algorithm_config_id")
    ALGORITHM_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    VISUALIZER_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    algorithm_version_id: str
    visualizer_configs: _containers.RepeatedCompositeFieldContainer[VisualizerConfig]
    algorithm_config_id: str
    def __init__(self, algorithm_version_id: _Optional[str] = ..., visualizer_configs: _Optional[_Iterable[_Union[VisualizerConfig, _Mapping]]] = ..., algorithm_config_id: _Optional[str] = ...) -> None: ...

class VisualizerConfigAlgoGetResponse(_message.Message):
    __slots__ = ("status_code", "visualizer_config_algos")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    VISUALIZER_CONFIG_ALGOS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    visualizer_config_algos: _containers.RepeatedCompositeFieldContainer[VisualizerConfigAlgo]
    def __init__(self, status_code: _Optional[int] = ..., visualizer_config_algos: _Optional[_Iterable[_Union[VisualizerConfigAlgo, _Mapping]]] = ...) -> None: ...

class VisualizerConfigAlgoConfigCreateRequest(_message.Message):
    __slots__ = ("visualizer_config_id", "algorithm_config_id")
    VISUALIZER_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    visualizer_config_id: str
    algorithm_config_id: str
    def __init__(self, visualizer_config_id: _Optional[str] = ..., algorithm_config_id: _Optional[str] = ...) -> None: ...

class VisualizerConfigAlgoConfigCreateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
