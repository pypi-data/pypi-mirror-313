from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoDtlsFingerPrints(_message.Message):
    __slots__ = ("algorithm", "value")
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    algorithm: str
    value: str
    def __init__(self, algorithm: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ProtoIceParameters(_message.Message):
    __slots__ = ("usernameFragment", "password", "iceLite")
    USERNAMEFRAGMENT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ICELITE_FIELD_NUMBER: _ClassVar[int]
    usernameFragment: str
    password: str
    iceLite: bool
    def __init__(self, usernameFragment: _Optional[str] = ..., password: _Optional[str] = ..., iceLite: bool = ...) -> None: ...

class ProtoIceCandidates(_message.Message):
    __slots__ = ("foundation", "priority", "ip", "port", "type", "protocol", "tcpType", "address")
    FOUNDATION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    TCPTYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    foundation: str
    priority: int
    ip: str
    port: int
    type: str
    protocol: str
    tcpType: str
    address: str
    def __init__(self, foundation: _Optional[str] = ..., priority: _Optional[int] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ..., type: _Optional[str] = ..., protocol: _Optional[str] = ..., tcpType: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

class ProtoDtlsParameters(_message.Message):
    __slots__ = ("role", "fingerprints")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    FINGERPRINTS_FIELD_NUMBER: _ClassVar[int]
    role: str
    fingerprints: _containers.RepeatedCompositeFieldContainer[ProtoDtlsFingerPrints]
    def __init__(self, role: _Optional[str] = ..., fingerprints: _Optional[_Iterable[_Union[ProtoDtlsFingerPrints, _Mapping]]] = ...) -> None: ...

class ProtoSctpParameters(_message.Message):
    __slots__ = ("port", "OS", "MIS", "maxMessageSize")
    PORT_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    MIS_FIELD_NUMBER: _ClassVar[int]
    MAXMESSAGESIZE_FIELD_NUMBER: _ClassVar[int]
    port: int
    OS: int
    MIS: int
    maxMessageSize: int
    def __init__(self, port: _Optional[int] = ..., OS: _Optional[int] = ..., MIS: _Optional[int] = ..., maxMessageSize: _Optional[int] = ...) -> None: ...

class ProtoTransportSDPInfo(_message.Message):
    __slots__ = ("id", "iceCandidates", "iceParameters", "dtlsParameters", "sctpParameters")
    ID_FIELD_NUMBER: _ClassVar[int]
    ICECANDIDATES_FIELD_NUMBER: _ClassVar[int]
    ICEPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    DTLSPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    SCTPPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    iceCandidates: _containers.RepeatedCompositeFieldContainer[ProtoIceCandidates]
    iceParameters: ProtoIceParameters
    dtlsParameters: ProtoDtlsParameters
    sctpParameters: ProtoSctpParameters
    def __init__(self, id: _Optional[str] = ..., iceCandidates: _Optional[_Iterable[_Union[ProtoIceCandidates, _Mapping]]] = ..., iceParameters: _Optional[_Union[ProtoIceParameters, _Mapping]] = ..., dtlsParameters: _Optional[_Union[ProtoDtlsParameters, _Mapping]] = ..., sctpParameters: _Optional[_Union[ProtoSctpParameters, _Mapping]] = ...) -> None: ...
