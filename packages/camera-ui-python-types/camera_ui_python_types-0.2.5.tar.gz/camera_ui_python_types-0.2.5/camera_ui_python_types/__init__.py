from abc import ABCMeta, abstractmethod
from collections.abc import AsyncGenerator, Awaitable, Coroutine
from typing import Any, Callable, Generic, Optional, Union, overload, runtime_checkable

from PIL import Image
from typing_extensions import Literal, NotRequired, Protocol, TypedDict, TypeVar

from .hybrid_observer import HybridObservable

# Literals
CameraType = Literal["camera", "doorbell"]
ZoneType = Literal["intersect", "contain"]
ZoneFilter = Literal["include", "exclude"]
ObjectClass = Literal[
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
    "motion",
]
CameraRoles = Literal["high-resolution", "mid-resolution", "low-resolution", "snapshot"]
DecoderFormat = Literal["yuv", "rgb"]
ImageInputFormat = Literal["yuv", "rgb", "rgba", "gray"]
ImageOutputFormat = Literal["rgb", "rgba", "gray"]
CameraExtension = Literal["hub", "motionDetection", "objectDetection", "audioDetection", "ptz"]
CameraFrameWorkerDecoder = Literal["pillow", "wasm", "rust"]
CameraFrameWorkerResolution = Literal[
    "3840x2160",
    "3072x1728",
    "2560x1440",
    "1920x1080",
    "1440x1080",
    "1280x720",
    "960x540",
    "640x480",
    "640x360",
    "320x240",
    "320x180",
]
AudioCodec = Literal["PCMU", "PCMA", "MPEG4-GENERIC", "opus", "G722", "MPA", "PCM", "FLAC"]
AudioFFmpegCodec = Literal[
    "pcm_mulaw", "pcm_alaw", "aac", "libopus", "g722", "mp3", "pcm_s16be", "pcm_s16le", "flac"
]
VideoCodec = Literal["H264", "H265", "VP8", "VP9", "AV1", "JPEG", "RAW"]
VideoFFmpegCodec = Literal["h264", "hevc", "vp8", "vp9", "av1", "mjpeg", "rawvideo"]
PythonVersion = Literal["3.9", "3.10", "3.11", "3.12"]
InternalSourceType = Literal["aac", "opus", "pcma"]
StateNames = Literal["light", "motion", "audio", "doorbell", "siren", "battery", "object"]
CameraPublicProperties = Literal[
    "_id",
    "nativeId",
    "pluginId",
    "name",
    "disabled",
    "isCloud",
    "hasLight",
    "hasSiren",
    "hasBinarySensor",
    "hasBattery",
    "info",
    "type",
    "detectionZones",
    "detectionSettings",
    "hasAudioDetector",
    "hasMotionDetector",
    "hasObjectDetector",
    "extendedMotionDetector",
    "hasPtz",
    "sources",
    "frameWorkerSettings",
]
DeviceManagerEventType = Literal[
    "cameraSelected",
    "cameraDeselected",
]
JsonSchemaType = Literal["string", "number", "boolean", "object", "array", "button"]
LoggerLevel = Literal["error", "warn", "info", "debug", "trace", "attention", "success"]
APIEventType = Literal["finishLaunching", "shutdown"]

# Basic types
Callback = Union[
    Callable[..., Any],
    Callable[..., Coroutine[Any, Any, Any]],
]

JSONValue = Union[str, int, float, bool, dict[str, Any], list[Any]]
JSONObject = dict[str, JSONValue]
JSONArray = list[JSONValue]
Path = Union[list[Union[int, str]], int, str]


# Interfaces as TypedDict
class CameraInformation(TypedDict, total=False):
    model: str
    manufacturer: str
    hardware: str
    serialNumber: str
    firmwareVersion: str
    supportUrl: str


Point = tuple[float, float]
BoundingBox = tuple[float, float, float, float]


class Detection(TypedDict):
    id: NotRequired[str]
    label: ObjectClass
    confidence: float
    boundingBox: BoundingBox
    inputWidth: int
    inputHeight: int
    origWidth: int
    origHeight: int


class ZoneCoord(TypedDict):
    _id: str
    points: Point


class ZoneRegion(TypedDict):
    _id: str
    coords: list[ZoneCoord]
    type: ZoneType
    filter: ZoneFilter
    classes: list[ObjectClass]
    isPrivacyMask: bool


class CameraZone(TypedDict):
    name: str
    regions: list[ZoneRegion]


class DetectionZone(TypedDict):
    name: str
    points: list[Point]
    type: ZoneType
    filter: ZoneFilter
    classes: list[ObjectClass]
    isPrivacyMask: bool


class MotionDetectionSettings(TypedDict):
    timeout: int


class ObjectDetectionSettings(TypedDict):
    confidence: float


class CameraDetectionSettings(TypedDict):
    motion: MotionDetectionSettings
    object: ObjectDetectionSettings


class CameraFrameWorkerSettings(TypedDict):
    decoder: CameraFrameWorkerDecoder
    fps: int
    resolution: CameraFrameWorkerResolution


class StreamUrls(TypedDict):
    ws: "Go2RtcWSSource"
    rtsp: "Go2RtcRTSPSource"
    www: "Go2RtcEndpoint"


class CameraInput(TypedDict):
    _id: str
    name: str
    roles: list[CameraRoles]
    urls: StreamUrls
    internal: bool


class RTPInfo(TypedDict):
    payload: Optional[int]
    codec: str
    rate: Optional[int]
    encoding: Optional[int]


class FMTPInfo(TypedDict):
    payload: int
    config: str


class AudioCodecProperties(TypedDict):
    sampleRate: int
    channels: int
    payloadType: int
    fmtpInfo: Optional[FMTPInfo]


class VideoCodecProperties(TypedDict):
    clockRate: int
    payloadType: int
    fmtpInfo: Optional[FMTPInfo]


class AudioStreamInfo(TypedDict):
    codec: AudioCodec
    ffmpegCodec: AudioFFmpegCodec
    properties: AudioCodecProperties
    direction: Literal["sendonly", "recvonly", "sendrecv", "inactive"]


class VideoStreamInfo(TypedDict):
    codec: VideoCodec
    ffmpegCodec: VideoFFmpegCodec
    properties: VideoCodecProperties
    direction: Literal["sendonly", "recvonly", "sendrecv", "inactive"]


class ProbeConfig(TypedDict, total=False):
    video: VideoCodec
    audio: AudioCodec
    microphone: AudioCodec


class ProbeStream(TypedDict):
    sdp: str
    audio: list[AudioStreamInfo]
    video: list[VideoStreamInfo]


class Go2RtcRTSPSource(TypedDict):
    default: str
    defaultMicrophone: str
    h264: str
    h265: str
    aac: str
    opus: str
    pcma: str
    mp4: str


class Go2RtcEndpoint(TypedDict):
    webrtc: str
    mse: str
    lmp4: str
    mmp4: str
    mp4: str
    mp4Snapshot: str
    jpegSnapshot: str
    lHlsTs: str
    lHlsFmp4: str
    mHlsFmp4: str
    mjpeg: str
    mjpegHtml: str


class Go2RtcSource(TypedDict):
    name: str
    src: str
    ws: str


class Go2RtcWSSource(TypedDict):
    webrtc: str


T = TypeVar(
    "T",
    bound=Union[
        "LightStateWithoutLastEvent",
        "AudioStateWithoutLastEvent",
        "MotionStateWithoutLastEvent",
        "ObjectStateWithoutLastEvent",
        "SirenStateWithoutLastEvent",
        "BatteryStateWithoutLastEvent",
        "DoorbellStateWithoutLastEvent",
    ],
)


class BaseState(TypedDict, Generic[T]):
    timestamp: int
    lastEvent: NotRequired[Optional[T]]


class BaseStateWithoutLastEvent(TypedDict):
    timestamp: int


class MotionSetEvent(TypedDict):
    state: bool
    detections: NotRequired[Optional[list[Detection]]]


class AudioSetEvent(TypedDict):
    state: bool
    db: NotRequired[Optional[float]]


class ObjectSetEvent(TypedDict):
    detections: list[Detection]


class LightSetEvent(TypedDict):
    state: bool


class DoorbellSetEvent(TypedDict):
    state: bool


class SirenSetEvent(TypedDict):
    state: bool
    level: NotRequired[Optional[int]]


class BatterySetEvent(TypedDict):
    level: int
    lowBattery: NotRequired[Optional[bool]]
    charging: NotRequired[Optional[bool]]


class LightState(BaseState["LightStateWithoutLastEvent"], LightSetEvent):
    pass


class LightStateWithoutLastEvent(BaseStateWithoutLastEvent, LightSetEvent):
    pass


class MotionState(BaseState["MotionStateWithoutLastEvent"], MotionSetEvent):
    pass


class MotionStateWithoutLastEvent(BaseStateWithoutLastEvent, MotionSetEvent):
    pass


class AudioState(BaseState["AudioStateWithoutLastEvent"], AudioSetEvent):
    pass


class AudioStateWithoutLastEvent(BaseStateWithoutLastEvent, AudioSetEvent):
    pass


class DoorbellState(BaseState["DoorbellStateWithoutLastEvent"], DoorbellSetEvent):
    pass


class DoorbellStateWithoutLastEvent(BaseStateWithoutLastEvent, DoorbellSetEvent):
    pass


class SirenState(BaseState["SirenStateWithoutLastEvent"], SirenSetEvent):
    pass


class SirenStateWithoutLastEvent(BaseStateWithoutLastEvent, SirenSetEvent):
    pass


class ObjectState(BaseState["ObjectStateWithoutLastEvent"], ObjectSetEvent):
    pass


class ObjectStateWithoutLastEvent(BaseStateWithoutLastEvent, ObjectSetEvent):
    pass


class BatteryState(BaseState["BatteryStateWithoutLastEvent"], BatterySetEvent):
    pass


class BatteryStateWithoutLastEvent(BaseStateWithoutLastEvent, BatterySetEvent):
    pass


class StateValues(TypedDict):
    light: LightState
    motion: MotionState
    audio: AudioState
    object: ObjectState
    doorbell: DoorbellState
    siren: SirenState
    battery: BatteryState


class SetValues(TypedDict):
    light: LightSetEvent
    motion: MotionSetEvent
    audio: AudioSetEvent
    object: ObjectSetEvent
    doorbell: DoorbellSetEvent
    siren: SirenSetEvent
    battery: BatterySetEvent


class FrameData(TypedDict):
    frameId: str
    timestamp: int


class FrameMetadata(TypedDict):
    format: DecoderFormat
    frameSize: Union[float, int]
    width: int
    origWidth: int
    height: int
    origHeight: int


class ImageInformation(TypedDict):
    width: int
    height: int
    channels: Literal[1, 3, 4]
    format: ImageInputFormat


class ImageCrop(TypedDict):
    top: int
    left: int
    width: int
    height: int


class ImageResize(TypedDict):
    width: int
    height: int


class ImageFormat(TypedDict):
    to: ImageOutputFormat


class ImageOptions(TypedDict, total=False):
    format: ImageFormat
    crop: ImageCrop
    resize: ImageResize


class FrameImage(TypedDict):
    image: Image.Image
    info: ImageInformation


class FrameBuffer(TypedDict):
    image: bytes
    info: ImageInformation


class VideoFrame(Protocol):
    @property
    def frame_data(self) -> FrameData: ...
    @property
    def metadata(self) -> FrameMetadata: ...
    @property
    def input_width(self) -> int: ...
    @property
    def input_height(self) -> int: ...
    @property
    def input_format(self) -> DecoderFormat: ...

    async def to_buffer(self, options: Optional[ImageOptions] = None) -> FrameBuffer: ...
    async def to_image(self, options: Optional[ImageOptions] = None) -> FrameImage: ...
    async def save(self, path: str, options: Optional[ImageOptions] = None) -> None: ...


class MotionFrame(VideoFrame, Protocol):
    @property
    def motion(self) -> MotionState: ...


class CameraInputSettings(TypedDict):
    _id: str
    name: str
    roles: list[CameraRoles]
    urls: list[str]
    internal: bool


class CameraConfigInputSettings(TypedDict):
    name: str
    roles: list[CameraRoles]
    urls: list[str]


class BaseCameraConfig(TypedDict, total=False):
    name: str
    nativeId: str
    isCloud: bool
    hasLight: bool
    hasSiren: bool
    hasBinarySensor: bool
    hasBattery: bool
    disabled: bool
    info: CameraInformation


class CameraConfig(BaseCameraConfig):
    sources: list[CameraConfigInputSettings]


class CameraDelegate(Protocol):
    async def snapshot(self) -> Optional[bytes]: ...


class CameraPTZDelegate(Protocol):
    async def moveAbsolute(self, pan: float, tilt: float, zoom: float) -> None: ...
    async def moveRelative(self, pan: float, tilt: float, zoom: float) -> None: ...
    async def moveContinuous(self, pan: float, tilt: float, zoom: float) -> None: ...
    async def stop(self) -> None: ...


class CameraDelegates(TypedDict):
    cameraDelegate: CameraDelegate
    ptzDelegate: CameraPTZDelegate


class CameraBaseSource(Protocol):
    # from CameraInput
    id: str  # _id
    name: str
    roles: list[CameraRoles]
    urls: StreamUrls
    internal: bool
    # end CameraInput

    async def probe_stream(
        self, probe_config: Optional[ProbeConfig] = None, refresh: Optional[bool] = None
    ) -> Optional[ProbeStream]: ...


class CameraDeviceSource(CameraBaseSource, Protocol):
    def get_internal_source(self, type: InternalSourceType) -> "CameraDeviceInternalSource": ...


class CameraDeviceInternalSource(CameraBaseSource, Protocol):
    type: InternalSourceType


class WebRTCConnectionOptions(TypedDict, total=False):
    iceServers: list["IceServer"]


class RTSPConnectionOptions(TypedDict, total=False):
    target: Literal[
        "default",
        "defaultMicrophone",
        "h264",
        "h265",
        "aac",
        "opus",
        "pcma",
        "h264aac",
        "h265aac",
        "h264opus",
        "h265opus",
        "h264pcma",
        "h265pcma",
        "mp4",
    ]


SpawnInput = Union[str, int]


class FfmpegOptions(TypedDict):
    ffmpegPath: str
    input: Optional[list[SpawnInput]]
    video: Optional[list[SpawnInput]]
    audio: Optional[list[SpawnInput]]
    output: list[SpawnInput]
    logger: Optional[dict[str, Any]]


class ReturnAudioFFmpegOptions(TypedDict):
    ffmpegPath: str
    input: list[SpawnInput]


class BaseCamera(TypedDict):
    _id: str
    nativeId: Optional[str]
    pluginId: str
    name: str
    disabled: bool
    isCloud: bool
    hasLight: bool
    hasSiren: bool
    hasBinarySensor: bool
    hasBattery: bool
    info: CameraInformation
    type: CameraType
    snapshotTTL: int
    detectionSettings: CameraDetectionSettings
    frameWorkerSettings: CameraFrameWorkerSettings


class Camera(BaseCamera):
    hasAudioDetector: bool
    hasMotionDetector: bool
    hasObjectDetector: bool
    extendedMotionDetector: bool
    hasPtz: bool
    sources: list[CameraInput]
    detectionZones: list[DetectionZone]


StateValue = Union[
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
]

SV = TypeVar("SV", bound=StateValue)


class CameraStateChangedObject(Generic[SV], TypedDict):
    old_state: SV
    new_state: SV


class CameraPropertyObservableObject(TypedDict):
    property: str
    old_state: Any
    new_state: Any


class CameraConfigInputSettingsPartial(TypedDict, total=False):
    # _id: str
    name: str
    roles: list[CameraRoles]
    urls: list[str]


@runtime_checkable
class CameraDevice(Protocol):
    @property
    def id(self) -> str: ...
    @property
    def native_id(self) -> Optional[str]: ...
    @property
    def plugin_id(self) -> str: ...
    @property
    def connected(self) -> bool: ...
    @property
    def disabled(self) -> bool: ...
    @property
    def name(self) -> str: ...
    @property
    def type(self) -> CameraType: ...
    @property
    def snapshot_ttl(self) -> int: ...
    @property
    def info(self) -> CameraInformation: ...
    @property
    def is_cloud(self) -> bool: ...
    @property
    def has_light(self) -> bool: ...
    @property
    def has_siren(self) -> bool: ...
    @property
    def has_binary_sensor(self) -> bool: ...
    @property
    def has_battery(self) -> bool: ...
    @property
    def has_motion_detector(self) -> bool: ...
    @property
    def extended_motion_detector(self) -> bool: ...
    @property
    def has_audio_detector(self) -> bool: ...
    @property
    def has_object_detector(self) -> bool: ...
    @property
    def has_ptz(self) -> bool: ...
    @property
    def detection_zones(self) -> list[DetectionZone]: ...
    @property
    def detection_settings(self) -> CameraDetectionSettings: ...
    @property
    def frameworker_settings(self) -> CameraFrameWorkerSettings: ...
    @property
    def stream_source(self) -> CameraDeviceSource: ...
    @property
    def snapshot_source(self) -> Optional[CameraInput]: ...
    @property
    def high_resolution_source(self) -> Optional[CameraDeviceSource]: ...
    @property
    def mid_resolution_source(self) -> Optional[CameraDeviceSource]: ...
    @property
    def low_resolution_source(self) -> Optional[CameraDeviceSource]: ...
    @property
    def ptz(self) -> CameraPTZDelegate: ...
    @property
    def sources(self) -> list[CameraDeviceSource]: ...
    @property
    def internal_sources(self) -> list[CameraDeviceInternalSource]: ...

    on_connected: HybridObservable[bool]
    on_light_switched: HybridObservable[LightState]
    on_motion_detected: HybridObservable[MotionState]
    on_audio_detected: HybridObservable[AudioState]
    on_object_detected: HybridObservable[ObjectState]
    on_doorbell_pressed: HybridObservable[DoorbellState]
    on_siren_detected: HybridObservable[SirenState]
    on_battery_changed: HybridObservable[BatteryState]

    logger: "LoggerService"

    async def snapshot(self, force_new: Optional[bool] = None) -> Optional[bytes]: ...

    @overload
    def on_state_change(
        self, state_name: Literal["light"]
    ) -> HybridObservable[CameraStateChangedObject[LightState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["motion"]
    ) -> HybridObservable[CameraStateChangedObject[MotionState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["audio"]
    ) -> HybridObservable[CameraStateChangedObject[AudioState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["doorbell"]
    ) -> HybridObservable[CameraStateChangedObject[DoorbellState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["siren"]
    ) -> HybridObservable[CameraStateChangedObject[SirenState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["battery"]
    ) -> HybridObservable[CameraStateChangedObject[BatteryState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["object"]
    ) -> HybridObservable[CameraStateChangedObject[ObjectState]]: ...
    def on_state_change(self, state_name: Any) -> Any: ...

    def on_property_change(
        self, property: Union[CameraPublicProperties, list[CameraPublicProperties]]
    ) -> HybridObservable[CameraPropertyObservableObject]: ...

    @overload
    def get_value(self, state_name: Literal["light"]) -> LightState: ...
    @overload
    def get_value(self, state_name: Literal["motion"]) -> MotionState: ...
    @overload
    def get_value(self, state_name: Literal["audio"]) -> AudioState: ...
    @overload
    def get_value(self, state_name: Literal["object"]) -> ObjectState: ...
    @overload
    def get_value(self, state_name: Literal["doorbell"]) -> DoorbellState: ...
    @overload
    def get_value(self, state_name: Literal["siren"]) -> SirenState: ...
    @overload
    def get_value(self, state_name: Literal["battery"]) -> BatteryState: ...
    def get_value(
        self, state_name: Literal["light", "motion", "audio", "object", "doorbell", "siren", "battery"]
    ) -> Union[
        LightState,
        MotionState,
        AudioState,
        ObjectState,
        DoorbellState,
        SirenState,
        BatteryState,
    ]: ...

    @overload
    def set_delegate(self, name: Literal["cameraDelegate"], delegate: CameraDelegate) -> None: ...
    @overload
    def set_delegate(self, name: Literal["ptzDelegate"], delegate: CameraPTZDelegate) -> None: ...

    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...

    def get_frames(self, prebuffer_duration: Optional[int] = None) -> AsyncGenerator[VideoFrame, None]: ...
    def get_motion_frames(self) -> AsyncGenerator[MotionFrame, None]: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["light"],
        event_data: LightSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["motion"],
        event_data: MotionSetEvent,
        frame: Optional[VideoFrame] = None,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["audio"],
        event_data: AudioSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["object"],
        event_data: ObjectSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["doorbell"],
        event_data: DoorbellSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["siren"],
        event_data: SirenSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["battery"],
        event_data: BatterySetEvent,
    ) -> None: ...
    async def update_state(
        self,
        state_name: Literal["light", "motion", "audio", "object", "doorbell", "siren", "battery"],
        event_data: Union[
            LightSetEvent,
            MotionSetEvent,
            AudioSetEvent,
            ObjectSetEvent,
            DoorbellSetEvent,
            SirenSetEvent,
            BatterySetEvent,
        ],
        frame: Optional[VideoFrame] = None,
    ) -> None: ...

    async def add_camera_source(self, source: CameraConfigInputSettings) -> None: ...
    async def update_camera_source(
        self, source_id: str, source: CameraConfigInputSettingsPartial
    ) -> None: ...
    async def remove_camera_source(self, source_id: str) -> None: ...


CameraSelectedCallback = Union[
    Callable[[CameraDevice, CameraExtension], None],
    Callable[[CameraDevice, CameraExtension], Coroutine[None, None, None]],
]
CameraDeselectedCallback = Union[
    Callable[[str, CameraExtension], None],
    Callable[[str, CameraExtension], Coroutine[None, None, None]],
]


@runtime_checkable
class DeviceManager(Protocol):
    async def create_camera(self, camera_config: CameraConfig) -> CameraDevice: ...
    async def get_camera_by_name(self, camera_name: str) -> Optional[CameraDevice]: ...
    async def get_camera_by_id(self, camera_id: str) -> Optional[CameraDevice]: ...
    async def remove_camera_by_name(self, camera_name: str) -> None: ...
    async def remove_camera_by_id(self, camera_id: str) -> None: ...

    @overload
    def on(self, event: Literal["cameraSelected"], f: CameraSelectedCallback) -> Any: ...
    @overload
    def on(self, event: Literal["cameraDeselected"], f: CameraDeselectedCallback) -> Any: ...

    @overload
    def once(self, event: Literal["cameraSelected"], f: CameraSelectedCallback) -> Any: ...
    @overload
    def once(self, event: Literal["cameraDeselected"], f: CameraDeselectedCallback) -> Any: ...

    @overload
    def remove_listener(self, event: Literal["cameraSelected"], f: CameraSelectedCallback) -> None: ...
    @overload
    def remove_listener(self, event: Literal["cameraDeselected"], f: CameraDeselectedCallback) -> None: ...

    def remove_all_listeners(self, event: Optional[DeviceManagerEventType] = None) -> None: ...


class FfmpegArgs(TypedDict):
    codec: str
    hwaccel: str
    hwaccelArgs: list[str]
    hwaccelFilters: list[str]
    hwDeviceArgs: list[str]
    threads: str


class IceServer(TypedDict):
    urls: list[str]
    username: Optional[str]
    credential: Optional[str]


@runtime_checkable
class CoreManager(Protocol):
    async def get_ffmpeg_path(self) -> str: ...
    async def get_hwaccel_info(self, target_codec: Union[Literal["h264"], Literal["h265"]]) -> FfmpegArgs: ...
    async def get_server_addresses(self) -> list[str]: ...
    async def get_ice_servers(self) -> list[IceServer]: ...


# Schema related types and interfaces
PluginConfig = dict[str, Any]

J = TypeVar("J")


class JsonBaseSchema(TypedDict, Generic[J]):
    key: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    required: NotRequired[bool]
    readonly: NotRequired[bool]
    placeholder: NotRequired[str]
    hidden: NotRequired[bool]
    group: NotRequired[str]
    defaultValue: NotRequired[J]
    store: NotRequired[bool]
    onSet: NotRequired[
        Union[Callable[[Any, Any], Awaitable[Union[None, Any]]], Callable[[Any, Any], Union[None, Any]]]
    ]  # only for plugins
    onGet: NotRequired[
        Union[Callable[[], Awaitable[Union[Any, None]]], Callable[[], Union[Any, None]]]
    ]  # only for plugins


class JsonSchemaString(JsonBaseSchema[str]):
    type: Literal["string"]
    format: NotRequired[
        Literal["date-time", "date", "time", "email", "uuid", "ipv4", "ipv6", "password", "qrCode", "image"]
    ]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class JsonSchemaNumber(JsonBaseSchema[float]):
    type: Literal["number"]
    minimum: NotRequired[float]
    maximum: NotRequired[float]
    step: NotRequired[float]


class JsonSchemaBoolean(JsonBaseSchema[bool]):
    type: Literal["boolean"]


class JsonSchemaEnum(JsonBaseSchema[str]):
    type: Literal["string"]
    enum: list[str]
    multiple: NotRequired[bool]


class JsonSchemaObject(JsonBaseSchema[Any]):
    type: Literal["object"]
    opened: NotRequired[bool]
    properties: NotRequired["JsonSchemaForm"]


class JsonSchemaArray(JsonBaseSchema[Any]):
    type: Literal["array"]
    opened: NotRequired[bool]
    items: NotRequired["JsonSchema"]


class JsonSchemaButton(JsonBaseSchema[Any]):
    type: Literal["button"]
    color: NotRequired[str]


class JsonSchemaObjectButton(TypedDict):
    label: str
    onSubmit: str
    color: NotRequired[str]


class JsonSchemaObjectWithButtons(JsonSchemaObject):
    buttons: list[JsonSchemaObjectButton]


JsonSchema = Union[
    JsonSchemaString,
    JsonSchemaNumber,
    JsonSchemaBoolean,
    JsonSchemaEnum,
    JsonSchemaObject,
    JsonSchemaObjectWithButtons,
    JsonSchemaArray,
    JsonSchemaButton,
]

JsonSchemaForm = dict[str, JsonSchema]


class RootSchema(TypedDict):
    schema: JsonSchemaForm


class ToastMessage(TypedDict):
    type: Literal["info", "success", "warning", "error"]
    message: str


class FormSubmitSchema(TypedDict):
    config: JsonSchemaObjectWithButtons


class FormSubmitResponse(TypedDict, total=False):
    toast: ToastMessage
    schema: FormSubmitSchema


class SchemaConfig(TypedDict):
    rootSchema: RootSchema
    config: dict[str, Any]


# Plugin related interfaces
class ImageMetadata(TypedDict):
    width: int
    height: int


class AudioMetadata(TypedDict):
    mimeType: Literal["audio/mpeg", "audio/wav", "audio/ogg"]


class MotionDetectionPluginResponse(TypedDict):
    filePath: str


class ObjectDetectionPluginResponse(TypedDict):
    detections: list[Detection]


class AudioDetectionPluginResponse(TypedDict):
    detected: bool


class BasePlugin(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, logger: "LoggerService", api: "PluginAPI") -> None: ...
    @abstractmethod
    async def onFormSubmit(self, action_id: str, payload: Any) -> Union[FormSubmitResponse, None]: ...
    @abstractmethod
    def configureCameras(self, cameras: list[CameraDevice]) -> None: ...


class MotionDetectionPlugin(BasePlugin):
    @abstractmethod
    def interfaceSchema(self) -> Optional[RootSchema]: ...
    @abstractmethod
    async def detectMotion(
        self, video_path: str, config: dict[str, Any]
    ) -> MotionDetectionPluginResponse: ...


class ObjectDetectionPlugin(BasePlugin):
    @abstractmethod
    def interfaceSchema(self) -> Optional[RootSchema]: ...
    @abstractmethod
    async def detectObjects(
        self, image_path: str, metadata: ImageMetadata, config: dict[str, Any]
    ) -> ObjectDetectionPluginResponse: ...


class AudioDetectionPlugin(BasePlugin):
    @abstractmethod
    def interfaceSchema(self) -> Optional[RootSchema]: ...
    @abstractmethod
    async def detectAudio(
        self, audio_path: str, metadata: AudioMetadata, config: dict[str, Any]
    ) -> AudioDetectionPluginResponse: ...


@runtime_checkable
class LoggerService(Protocol):
    def log(self, *args: Any) -> None: ...
    def error(self, *args: Any) -> None: ...
    def warn(self, *args: Any) -> None: ...
    def debug(self, *args: Any) -> None: ...
    def trace(self, *args: Any) -> None: ...
    def attention(self, *args: Any) -> None: ...
    def success(self, *args: Any) -> None: ...


PA = TypeVar("PA", bound="CameraStorage[Any]", default="CameraStorage[Any]")


@runtime_checkable
class PluginAPI(Protocol):
    core_manager: CoreManager
    device_manager: DeviceManager
    storage_controller: "StorageController"
    config_service: "ConfigService"
    storage_path: str
    config_file: str

    def on(self, event: APIEventType, f: Callback) -> Any: ...
    def once(self, event: APIEventType, f: Callback) -> Any: ...
    def remove_listener(self, event: APIEventType, f: Callback) -> None: ...
    def remove_all_listeners(self, event: Optional[APIEventType] = None) -> None: ...


@runtime_checkable
class ConfigService(Protocol):
    def get(
        self,
        key: Path,
        default_value: Optional[JSONValue] = None,
        validate: Optional[Callable[[Any], bool]] = None,
        refresh: bool = False,
        write_if_not_valid: bool = False,
    ) -> Any: ...
    def has(self, key: Path, refresh: bool = False) -> bool: ...
    def ensure_exists(self, key: Path, default_value: JSONValue, write: bool = False) -> None: ...
    def set(self, key: Path, value: Any, write: bool = False) -> None: ...
    def insert(self, key: Path, value: Any, at: int = 0, write: bool = False) -> None: ...
    def push(self, key: Path, write: bool = False, *items: Any) -> None: ...
    def delete(self, key: Path, write: bool = False) -> None: ...
    def all(self, refresh: bool = False) -> dict[str, Any]: ...
    def replace(self, config: dict[str, Any], write: bool = False) -> None: ...
    def update_value(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        target_key: str,
        new_value: Any,
        write: bool = False,
    ) -> None: ...
    def replace_or_add_item(
        self, path: str, search_key: str, search_value: Any, new_item: Any, write: bool = False
    ) -> None: ...


V1 = TypeVar("V1", default=str)
V2 = TypeVar("V2", default=dict[str, Any])


@runtime_checkable
class CameraStorage(Protocol, Generic[V2]):
    values: V2
    schema: JsonSchemaForm

    def initializeStorage(self) -> None: ...
    @overload
    async def getValue(self, path: str) -> Union[V1, None]: ...
    @overload
    async def getValue(self, path: str, default_value: V1) -> V1: ...
    async def getValue(self, path: str, default_value: Optional[V1] = None) -> Union[V1, None]: ...
    async def setValue(self, path: str, new_value: Any) -> None: ...
    def hasValue(self, path: str) -> bool: ...
    async def getConfig(self) -> SchemaConfig: ...
    async def setConfig(self, new_config: V2) -> None: ...
    @overload
    async def addSchema(self, schema_or_path: JsonSchemaForm) -> None: ...
    @overload
    async def addSchema(self, schema_or_path: str, schema: JsonSchema) -> None: ...
    async def addSchema(
        self,
        schema_or_path: Union[JsonSchemaForm, str],
        schema: Optional[JsonSchema] = None,
    ) -> None: ...
    def removeSchema(self, path: str) -> None: ...
    async def changeSchema(self, path: str, new_schema: dict[str, Any]) -> None: ...
    def getSchema(self, path: str) -> Optional[JsonSchema]: ...
    def hasSchema(self, path: str) -> bool: ...


S = TypeVar("S", default=CameraStorage[Any], covariant=True)


@runtime_checkable
class StorageController(Protocol[S]):
    def create_camera_storage(
        self,
        instance: Any,
        camera_id: str,
        schema: Optional[JsonSchemaForm] = None,
    ) -> S: ...
    def get_camera_storage(self, camera_id: str) -> Optional[S]: ...
    def remove_camera_storage(self, camera_id: str) -> None: ...
