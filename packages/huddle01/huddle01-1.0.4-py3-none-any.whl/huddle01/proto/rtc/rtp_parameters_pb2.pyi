from ..rtc import rtp_capabilities_pb2 as _rtp_capabilities_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoRtcpFeedback(_message.Message):
    __slots__ = ("type", "parameter")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_FIELD_NUMBER: _ClassVar[int]
    type: str
    parameter: str
    def __init__(
        self, type: _Optional[str] = ..., parameter: _Optional[str] = ...
    ) -> None: ...

class ProtoCodecParameters(_message.Message):
    __slots__ = (
        "mimeType",
        "payloadType",
        "clockRate",
        "channels",
        "parameters",
        "rtcpFeedback",
    )
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    MIMETYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOADTYPE_FIELD_NUMBER: _ClassVar[int]
    CLOCKRATE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    RTCPFEEDBACK_FIELD_NUMBER: _ClassVar[int]
    mimeType: str
    payloadType: int
    clockRate: int
    channels: int
    parameters: _containers.ScalarMap[str, str]
    rtcpFeedback: _containers.RepeatedCompositeFieldContainer[ProtoRtcpFeedback]
    def __init__(
        self,
        mimeType: _Optional[str] = ...,
        payloadType: _Optional[int] = ...,
        clockRate: _Optional[int] = ...,
        channels: _Optional[int] = ...,
        parameters: _Optional[_Mapping[str, str]] = ...,
        rtcpFeedback: _Optional[_Iterable[_Union[ProtoRtcpFeedback, _Mapping]]] = ...,
    ) -> None: ...

class ProtoHeaderExtensionParameters(_message.Message):
    __slots__ = ("uri", "id", "encrypt", "parameters")
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    URI_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ENCRYPT_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    id: int
    encrypt: bool
    parameters: _containers.ScalarMap[str, str]
    def __init__(
        self,
        uri: _Optional[str] = ...,
        id: _Optional[int] = ...,
        encrypt: bool = ...,
        parameters: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ProtoEncodings(_message.Message):
    __slots__ = (
        "ssrc",
        "rid",
        "codecPayloadType",
        "rtx",
        "dtx",
        "scalabilityMode",
        "scaleResolutionDownBy",
        "maxBitrate",
        "active",
        "maxFramerate",
    )
    class ProtoRTX(_message.Message):
        __slots__ = ("ssrc",)
        SSRC_FIELD_NUMBER: _ClassVar[int]
        ssrc: int
        def __init__(self, ssrc: _Optional[int] = ...) -> None: ...

    SSRC_FIELD_NUMBER: _ClassVar[int]
    RID_FIELD_NUMBER: _ClassVar[int]
    CODECPAYLOADTYPE_FIELD_NUMBER: _ClassVar[int]
    RTX_FIELD_NUMBER: _ClassVar[int]
    DTX_FIELD_NUMBER: _ClassVar[int]
    SCALABILITYMODE_FIELD_NUMBER: _ClassVar[int]
    SCALERESOLUTIONDOWNBY_FIELD_NUMBER: _ClassVar[int]
    MAXBITRATE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MAXFRAMERATE_FIELD_NUMBER: _ClassVar[int]
    ssrc: int
    rid: str
    codecPayloadType: int
    rtx: ProtoEncodings.ProtoRTX
    dtx: bool
    scalabilityMode: str
    scaleResolutionDownBy: int
    maxBitrate: int
    active: bool
    maxFramerate: int
    def __init__(
        self,
        ssrc: _Optional[int] = ...,
        rid: _Optional[str] = ...,
        codecPayloadType: _Optional[int] = ...,
        rtx: _Optional[_Union[ProtoEncodings.ProtoRTX, _Mapping]] = ...,
        dtx: bool = ...,
        scalabilityMode: _Optional[str] = ...,
        scaleResolutionDownBy: _Optional[int] = ...,
        maxBitrate: _Optional[int] = ...,
        active: bool = ...,
        maxFramerate: _Optional[int] = ...,
    ) -> None: ...

class RtcpParameters(_message.Message):
    __slots__ = ("cname", "reducedSize", "mux")
    CNAME_FIELD_NUMBER: _ClassVar[int]
    REDUCEDSIZE_FIELD_NUMBER: _ClassVar[int]
    MUX_FIELD_NUMBER: _ClassVar[int]
    cname: str
    reducedSize: bool
    mux: bool
    def __init__(
        self, cname: _Optional[str] = ..., reducedSize: bool = ..., mux: bool = ...
    ) -> None: ...

class ProtoRtpParameters(_message.Message):
    __slots__ = ("mid", "codecs", "headerExtensions", "encodings", "rtcp")
    MID_FIELD_NUMBER: _ClassVar[int]
    CODECS_FIELD_NUMBER: _ClassVar[int]
    HEADEREXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    ENCODINGS_FIELD_NUMBER: _ClassVar[int]
    RTCP_FIELD_NUMBER: _ClassVar[int]
    mid: str
    codecs: _containers.RepeatedCompositeFieldContainer[ProtoCodecParameters]
    headerExtensions: _containers.RepeatedCompositeFieldContainer[
        ProtoHeaderExtensionParameters
    ]
    encodings: _containers.RepeatedCompositeFieldContainer[ProtoEncodings]
    rtcp: RtcpParameters
    def __init__(
        self,
        mid: _Optional[str] = ...,
        codecs: _Optional[_Iterable[_Union[ProtoCodecParameters, _Mapping]]] = ...,
        headerExtensions: _Optional[
            _Iterable[_Union[ProtoHeaderExtensionParameters, _Mapping]]
        ] = ...,
        encodings: _Optional[_Iterable[_Union[ProtoEncodings, _Mapping]]] = ...,
        rtcp: _Optional[_Union[RtcpParameters, _Mapping]] = ...,
    ) -> None: ...

class ProtoSrtpParameters(_message.Message):
    __slots__ = ("cryptoSuite", "keyBase64")
    CRYPTOSUITE_FIELD_NUMBER: _ClassVar[int]
    KEYBASE64_FIELD_NUMBER: _ClassVar[int]
    cryptoSuite: str
    keyBase64: str
    def __init__(
        self, cryptoSuite: _Optional[str] = ..., keyBase64: _Optional[str] = ...
    ) -> None: ...

class ProtoTransportTuple(_message.Message):
    __slots__ = (
        "localIp",
        "localPort",
        "remoteIp",
        "remotePort",
        "protocol",
        "localAddress",
    )
    LOCALIP_FIELD_NUMBER: _ClassVar[int]
    LOCALPORT_FIELD_NUMBER: _ClassVar[int]
    REMOTEIP_FIELD_NUMBER: _ClassVar[int]
    REMOTEPORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    LOCALADDRESS_FIELD_NUMBER: _ClassVar[int]
    localIp: str
    localPort: int
    remoteIp: str
    remotePort: int
    protocol: str
    localAddress: str
    def __init__(
        self,
        localIp: _Optional[str] = ...,
        localPort: _Optional[int] = ...,
        remoteIp: _Optional[str] = ...,
        remotePort: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
        localAddress: _Optional[str] = ...,
    ) -> None: ...
