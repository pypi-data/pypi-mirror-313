from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoRtpCodecCapability(_message.Message):
    __slots__ = ("kind", "mimeType", "preferredPayloadType", "clockRate", "channels", "parameters", "rtcpFeedback")
    class ProtoRtcpFeedback(_message.Message):
        __slots__ = ("type", "parameter")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        PARAMETER_FIELD_NUMBER: _ClassVar[int]
        type: str
        parameter: str
        def __init__(self, type: _Optional[str] = ..., parameter: _Optional[str] = ...) -> None: ...
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    KIND_FIELD_NUMBER: _ClassVar[int]
    MIMETYPE_FIELD_NUMBER: _ClassVar[int]
    PREFERREDPAYLOADTYPE_FIELD_NUMBER: _ClassVar[int]
    CLOCKRATE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    RTCPFEEDBACK_FIELD_NUMBER: _ClassVar[int]
    kind: str
    mimeType: str
    preferredPayloadType: int
    clockRate: int
    channels: int
    parameters: _containers.ScalarMap[str, str]
    rtcpFeedback: _containers.RepeatedCompositeFieldContainer[ProtoRtpCodecCapability.ProtoRtcpFeedback]
    def __init__(self, kind: _Optional[str] = ..., mimeType: _Optional[str] = ..., preferredPayloadType: _Optional[int] = ..., clockRate: _Optional[int] = ..., channels: _Optional[int] = ..., parameters: _Optional[_Mapping[str, str]] = ..., rtcpFeedback: _Optional[_Iterable[_Union[ProtoRtpCodecCapability.ProtoRtcpFeedback, _Mapping]]] = ...) -> None: ...

class ProtoRtpHeaderExtension(_message.Message):
    __slots__ = ("kind", "uri", "preferredId", "preferredEncrypt", "direction")
    KIND_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    PREFERREDID_FIELD_NUMBER: _ClassVar[int]
    PREFERREDENCRYPT_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    kind: str
    uri: str
    preferredId: int
    preferredEncrypt: bool
    direction: str
    def __init__(self, kind: _Optional[str] = ..., uri: _Optional[str] = ..., preferredId: _Optional[int] = ..., preferredEncrypt: bool = ..., direction: _Optional[str] = ...) -> None: ...

class ProtoRtpCapabilities(_message.Message):
    __slots__ = ("codecs", "headerExtensions")
    CODECS_FIELD_NUMBER: _ClassVar[int]
    HEADEREXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    codecs: _containers.RepeatedCompositeFieldContainer[ProtoRtpCodecCapability]
    headerExtensions: _containers.RepeatedCompositeFieldContainer[ProtoRtpHeaderExtension]
    def __init__(self, codecs: _Optional[_Iterable[_Union[ProtoRtpCodecCapability, _Mapping]]] = ..., headerExtensions: _Optional[_Iterable[_Union[ProtoRtpHeaderExtension, _Mapping]]] = ...) -> None: ...
