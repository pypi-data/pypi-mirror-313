from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_models_pb2 as _common_models_pb2
import result_pb2 as _result_pb2
import common_models_pb2 as _common_models_pb2_1
import toi_pb2 as _toi_pb2
import analysis_pb2 as _analysis_pb2
import common_models_pb2 as _common_models_pb2_1_1
import algorithm_config_pb2 as _algorithm_config_pb2
import common_models_pb2 as _common_models_pb2_1_1_1
import algorithm_pb2 as _algorithm_pb2
import algorithm_version_pb2 as _algorithm_version_pb2
import visualization_pb2 as _visualization_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from result_pb2 import ExportFile as ExportFile
from result_pb2 import ExportCredentials as ExportCredentials
from result_pb2 import Result as Result
from result_pb2 import ResultGetRequest as ResultGetRequest
from result_pb2 import ResultGetResponse as ResultGetResponse
from analysis_pb2 import AnalysisAlgorithmNode as AnalysisAlgorithmNode
from analysis_pb2 import AnalysisCreateRequest as AnalysisCreateRequest
from analysis_pb2 import AnalysisCreateResponse as AnalysisCreateResponse
from analysis_pb2 import AnalysisAlgorithmConfigNode as AnalysisAlgorithmConfigNode
from analysis_pb2 import AnalysisGetRequest as AnalysisGetRequest
from analysis_pb2 import Analysis as Analysis
from analysis_pb2 import AnalysisGetResponse as AnalysisGetResponse
from analysis_pb2 import AnalysisListRequest as AnalysisListRequest
from analysis_pb2 import AnalysisListResponse as AnalysisListResponse
from algorithm_config_pb2 import AlgorithmConfig as AlgorithmConfig
from algorithm_config_pb2 import AlgorithmConfigCreateRequest as AlgorithmConfigCreateRequest
from algorithm_config_pb2 import AlgorithmConfigCreateResponse as AlgorithmConfigCreateResponse
from algorithm_config_pb2 import AlgorithmConfigUpdateRequest as AlgorithmConfigUpdateRequest
from algorithm_config_pb2 import AlgorithmConfigUpdateResponse as AlgorithmConfigUpdateResponse
from algorithm_config_pb2 import AlgorithmConfigGetRequest as AlgorithmConfigGetRequest
from algorithm_config_pb2 import AlgorithmConfigGetResponse as AlgorithmConfigGetResponse
from algorithm_config_pb2 import AlgorithmConfigListRequest as AlgorithmConfigListRequest
from algorithm_config_pb2 import AlgorithmConfigListResponse as AlgorithmConfigListResponse
from algorithm_config_pb2 import AlgorithmConfigDeleteRequest as AlgorithmConfigDeleteRequest
from algorithm_config_pb2 import AlgorithmConfigDeleteResponse as AlgorithmConfigDeleteResponse
from algorithm_config_pb2 import AlgorithmConfigDeprecateRequest as AlgorithmConfigDeprecateRequest
from algorithm_config_pb2 import AlgorithmConfigDeprecateResponse as AlgorithmConfigDeprecateResponse
from algorithm_config_pb2 import AlgorithmConfigDeactivateRequest as AlgorithmConfigDeactivateRequest
from algorithm_config_pb2 import AlgorithmConfigDeactivateResponse as AlgorithmConfigDeactivateResponse
from visualization_pb2 import Visualization as Visualization
from visualization_pb2 import VisualizationGetRequest as VisualizationGetRequest
from visualization_pb2 import VisualizationGetResponse as VisualizationGetResponse
from visualization_pb2 import Visualizer as Visualizer
from visualization_pb2 import VisualizerConfig as VisualizerConfig
from visualization_pb2 import VisualizerConfigAlgoVersionCreateRequest as VisualizerConfigAlgoVersionCreateRequest
from visualization_pb2 import VisualizerConfigAlgoVersionCreateResponse as VisualizerConfigAlgoVersionCreateResponse
from visualization_pb2 import VisualizerConfigAlgoGetRequest as VisualizerConfigAlgoGetRequest
from visualization_pb2 import VisualizerConfigAlgo as VisualizerConfigAlgo
from visualization_pb2 import VisualizerConfigAlgoGetResponse as VisualizerConfigAlgoGetResponse
from visualization_pb2 import VisualizerConfigAlgoConfigCreateRequest as VisualizerConfigAlgoConfigCreateRequest
from visualization_pb2 import VisualizerConfigAlgoConfigCreateResponse as VisualizerConfigAlgoConfigCreateResponse

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectResultStatus(_message.Message):
    __slots__ = ("analysis_config_id", "aoi_id", "result_indicator")
    class ProjectResultIndicator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_RESULT_STATUS: _ClassVar[ProjectResultStatus.ProjectResultIndicator]
        NOT_STARTED: _ClassVar[ProjectResultStatus.ProjectResultIndicator]
        IN_PROGRESS: _ClassVar[ProjectResultStatus.ProjectResultIndicator]
        AVAILABLE: _ClassVar[ProjectResultStatus.ProjectResultIndicator]
        FAILED: _ClassVar[ProjectResultStatus.ProjectResultIndicator]
    UNKNOWN_RESULT_STATUS: ProjectResultStatus.ProjectResultIndicator
    NOT_STARTED: ProjectResultStatus.ProjectResultIndicator
    IN_PROGRESS: ProjectResultStatus.ProjectResultIndicator
    AVAILABLE: ProjectResultStatus.ProjectResultIndicator
    FAILED: ProjectResultStatus.ProjectResultIndicator
    ANALYSIS_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    AOI_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    analysis_config_id: str
    aoi_id: str
    result_indicator: ProjectResultStatus.ProjectResultIndicator
    def __init__(self, analysis_config_id: _Optional[str] = ..., aoi_id: _Optional[str] = ..., result_indicator: _Optional[_Union[ProjectResultStatus.ProjectResultIndicator, str]] = ...) -> None: ...

class ProjectResultDownloadInput(_message.Message):
    __slots__ = ("project_id", "observation_start_ts", "observation_end_ts", "file_type", "data_type")
    class ProjectResultDownloadFileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_FILE_TYPE: _ClassVar[ProjectResultDownloadInput.ProjectResultDownloadFileType]
        CSV: _ClassVar[ProjectResultDownloadInput.ProjectResultDownloadFileType]
        SHAPEFILE: _ClassVar[ProjectResultDownloadInput.ProjectResultDownloadFileType]
        GEOJSON: _ClassVar[ProjectResultDownloadInput.ProjectResultDownloadFileType]
        PARQUET: _ClassVar[ProjectResultDownloadInput.ProjectResultDownloadFileType]
    UNKNOWN_FILE_TYPE: ProjectResultDownloadInput.ProjectResultDownloadFileType
    CSV: ProjectResultDownloadInput.ProjectResultDownloadFileType
    SHAPEFILE: ProjectResultDownloadInput.ProjectResultDownloadFileType
    GEOJSON: ProjectResultDownloadInput.ProjectResultDownloadFileType
    PARQUET: ProjectResultDownloadInput.ProjectResultDownloadFileType
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    OBSERVATION_START_TS_FIELD_NUMBER: _ClassVar[int]
    OBSERVATION_END_TS_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    observation_start_ts: _timestamp_pb2.Timestamp
    observation_end_ts: _timestamp_pb2.Timestamp
    file_type: ProjectResultDownloadInput.ProjectResultDownloadFileType
    data_type: str
    def __init__(self, project_id: _Optional[str] = ..., observation_start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., observation_end_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., file_type: _Optional[_Union[ProjectResultDownloadInput.ProjectResultDownloadFileType, str]] = ..., data_type: _Optional[str] = ...) -> None: ...

class ProjectResultDownloadOutput(_message.Message):
    __slots__ = ("download_url", "download_status", "created_ts", "file_size_bytes", "download_input")
    class ProjectResultDownloadStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_DOWNLOAD_STATUS: _ClassVar[ProjectResultDownloadOutput.ProjectResultDownloadStatus]
        PROCESSING: _ClassVar[ProjectResultDownloadOutput.ProjectResultDownloadStatus]
        SUCCEEDED: _ClassVar[ProjectResultDownloadOutput.ProjectResultDownloadStatus]
        FAILED: _ClassVar[ProjectResultDownloadOutput.ProjectResultDownloadStatus]
    UNKNOWN_DOWNLOAD_STATUS: ProjectResultDownloadOutput.ProjectResultDownloadStatus
    PROCESSING: ProjectResultDownloadOutput.ProjectResultDownloadStatus
    SUCCEEDED: ProjectResultDownloadOutput.ProjectResultDownloadStatus
    FAILED: ProjectResultDownloadOutput.ProjectResultDownloadStatus
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_TS_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_INPUT_FIELD_NUMBER: _ClassVar[int]
    download_url: str
    download_status: ProjectResultDownloadOutput.ProjectResultDownloadStatus
    created_ts: _timestamp_pb2.Timestamp
    file_size_bytes: int
    download_input: ProjectResultDownloadInput
    def __init__(self, download_url: _Optional[str] = ..., download_status: _Optional[_Union[ProjectResultDownloadOutput.ProjectResultDownloadStatus, str]] = ..., created_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., file_size_bytes: _Optional[int] = ..., download_input: _Optional[_Union[ProjectResultDownloadInput, _Mapping]] = ...) -> None: ...

class ProjectResult(_message.Message):
    __slots__ = ("result_get_response", "analysis_algorithm_node", "algorithm_config")
    RESULT_GET_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_ALGORITHM_NODE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    result_get_response: _result_pb2.ResultGetResponse
    analysis_algorithm_node: _analysis_pb2.AnalysisAlgorithmNode
    algorithm_config: _algorithm_config_pb2.AlgorithmConfig
    def __init__(self, result_get_response: _Optional[_Union[_result_pb2.ResultGetResponse, _Mapping]] = ..., analysis_algorithm_node: _Optional[_Union[_analysis_pb2.AnalysisAlgorithmNode, _Mapping]] = ..., algorithm_config: _Optional[_Union[_algorithm_config_pb2.AlgorithmConfig, _Mapping]] = ...) -> None: ...

class ProjectResultGetRequest(_message.Message):
    __slots__ = ("project_id", "analysis_config_id", "source_aoi_version", "visualizer_type", "include_export_files", "include_measurement_files")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_AOI_VERSION_FIELD_NUMBER: _ClassVar[int]
    VISUALIZER_TYPE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EXPORT_FILES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MEASUREMENT_FILES_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    analysis_config_id: str
    source_aoi_version: int
    visualizer_type: _visualization_pb2.Visualizer.VisualizerType
    include_export_files: bool
    include_measurement_files: bool
    def __init__(self, project_id: _Optional[str] = ..., analysis_config_id: _Optional[str] = ..., source_aoi_version: _Optional[int] = ..., visualizer_type: _Optional[_Union[_visualization_pb2.Visualizer.VisualizerType, str]] = ..., include_export_files: bool = ..., include_measurement_files: bool = ...) -> None: ...

class ProjectResultGetResponse(_message.Message):
    __slots__ = ("status_code", "project_results")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_RESULTS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    project_results: _containers.RepeatedCompositeFieldContainer[ProjectResult]
    def __init__(self, status_code: _Optional[int] = ..., project_results: _Optional[_Iterable[_Union[ProjectResult, _Mapping]]] = ...) -> None: ...

class ProjectResultGetStatusRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ProjectResultGetStatusResponse(_message.Message):
    __slots__ = ("status_code", "results_status", "progress")
    class Progress(_message.Message):
        __slots__ = ("running", "succeeded", "failed")
        RUNNING_FIELD_NUMBER: _ClassVar[int]
        SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
        FAILED_FIELD_NUMBER: _ClassVar[int]
        running: float
        succeeded: float
        failed: float
        def __init__(self, running: _Optional[float] = ..., succeeded: _Optional[float] = ..., failed: _Optional[float] = ...) -> None: ...
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    results_status: _containers.RepeatedCompositeFieldContainer[ProjectResultStatus]
    progress: ProjectResultGetStatusResponse.Progress
    def __init__(self, status_code: _Optional[int] = ..., results_status: _Optional[_Iterable[_Union[ProjectResultStatus, _Mapping]]] = ..., progress: _Optional[_Union[ProjectResultGetStatusResponse.Progress, _Mapping]] = ...) -> None: ...

class ProjectResultGetDownloadRequest(_message.Message):
    __slots__ = ("download_input",)
    DOWNLOAD_INPUT_FIELD_NUMBER: _ClassVar[int]
    download_input: ProjectResultDownloadInput
    def __init__(self, download_input: _Optional[_Union[ProjectResultDownloadInput, _Mapping]] = ...) -> None: ...

class ProjectResultGetDownloadResponse(_message.Message):
    __slots__ = ("status_code", "download_outputs")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    download_outputs: _containers.RepeatedCompositeFieldContainer[ProjectResultDownloadOutput]
    def __init__(self, status_code: _Optional[int] = ..., download_outputs: _Optional[_Iterable[_Union[ProjectResultDownloadOutput, _Mapping]]] = ...) -> None: ...

class ProjectResultGenerateDownloadRequest(_message.Message):
    __slots__ = ("download_input",)
    DOWNLOAD_INPUT_FIELD_NUMBER: _ClassVar[int]
    download_input: ProjectResultDownloadInput
    def __init__(self, download_input: _Optional[_Union[ProjectResultDownloadInput, _Mapping]] = ...) -> None: ...

class ProjectResultGenerateDownloadResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
