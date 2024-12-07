from ..rtc import rtp_parameters_pb2 as _rtp_parameters_pb2
from ..rtc import sctp_stream_parameters_pb2 as _sctp_stream_parameters_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePipeTransportRequest(_message.Message):
    __slots__ = ("roomId", "remoteIp", "remoteMomoId")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    REMOTEIP_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    remoteIp: str
    remoteMomoId: str
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        remoteIp: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
    ) -> None: ...

class CreatePipeTransportResponse(_message.Message):
    __slots__ = (
        "roomId",
        "localMomoId",
        "remoteMomoId",
        "transportId",
        "srtpParameters",
        "tuple",
    )
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    LOCALMOMOID_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTID_FIELD_NUMBER: _ClassVar[int]
    SRTPPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    TUPLE_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    localMomoId: str
    remoteMomoId: str
    transportId: str
    srtpParameters: _rtp_parameters_pb2.ProtoSrtpParameters
    tuple: _rtp_parameters_pb2.ProtoTransportTuple
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        localMomoId: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
        transportId: _Optional[str] = ...,
        srtpParameters: _Optional[
            _Union[_rtp_parameters_pb2.ProtoSrtpParameters, _Mapping]
        ] = ...,
        tuple: _Optional[
            _Union[_rtp_parameters_pb2.ProtoTransportTuple, _Mapping]
        ] = ...,
    ) -> None: ...

class ConnectPipeTransportRequest(_message.Message):
    __slots__ = (
        "roomId",
        "remoteIp",
        "remoteMomoId",
        "transportId",
        "srtpParameters",
        "tuple",
    )
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    REMOTEIP_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTID_FIELD_NUMBER: _ClassVar[int]
    SRTPPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    TUPLE_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    remoteIp: str
    remoteMomoId: str
    transportId: str
    srtpParameters: _rtp_parameters_pb2.ProtoSrtpParameters
    tuple: _rtp_parameters_pb2.ProtoTransportTuple
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        remoteIp: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
        transportId: _Optional[str] = ...,
        srtpParameters: _Optional[
            _Union[_rtp_parameters_pb2.ProtoSrtpParameters, _Mapping]
        ] = ...,
        tuple: _Optional[
            _Union[_rtp_parameters_pb2.ProtoTransportTuple, _Mapping]
        ] = ...,
    ) -> None: ...

class ConnectPipeTransportResponse(_message.Message):
    __slots__ = ("roomId", "remoteMomoId", "remoteMomoIp")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOIP_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    remoteMomoId: str
    remoteMomoIp: str
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
        remoteMomoIp: _Optional[str] = ...,
    ) -> None: ...

class PipeProduceRequest(_message.Message):
    __slots__ = (
        "roomId",
        "kind",
        "remoteMomoId",
        "producerId",
        "producerPeerId",
        "rtpParameters",
        "label",
    )
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    RTPPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    kind: str
    remoteMomoId: str
    producerId: str
    producerPeerId: str
    rtpParameters: _rtp_parameters_pb2.ProtoRtpParameters
    label: str
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        producerPeerId: _Optional[str] = ...,
        rtpParameters: _Optional[
            _Union[_rtp_parameters_pb2.ProtoRtpParameters, _Mapping]
        ] = ...,
        label: _Optional[str] = ...,
    ) -> None: ...

class PipeProduceResponse(_message.Message):
    __slots__ = ("roomId", "pipeProducerId", "status")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    PIPEPRODUCERID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    pipeProducerId: str
    status: bool
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        pipeProducerId: _Optional[str] = ...,
        status: bool = ...,
    ) -> None: ...

class PipeConsumeRequest(_message.Message):
    __slots__ = ("roomId", "remoteMomoId", "producerId", "producerPeerId")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    remoteMomoId: str
    producerId: str
    producerPeerId: str
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        producerPeerId: _Optional[str] = ...,
    ) -> None: ...

class PipeConsumeResponse(_message.Message):
    __slots__ = ("roomId", "producerPeerId", "rtpParameters", "label", "kind")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    RTPPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    producerPeerId: str
    rtpParameters: _rtp_parameters_pb2.ProtoRtpParameters
    label: str
    kind: str
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        producerPeerId: _Optional[str] = ...,
        rtpParameters: _Optional[
            _Union[_rtp_parameters_pb2.ProtoRtpParameters, _Mapping]
        ] = ...,
        label: _Optional[str] = ...,
        kind: _Optional[str] = ...,
    ) -> None: ...

class PipeDataProduceRequest(_message.Message):
    __slots__ = (
        "roomId",
        "remoteMomoId",
        "dataProducerId",
        "producerPeerId",
        "label",
        "protocol",
        "sctpStreamParameters",
        "appData",
    )
    class AppDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    ROOMID_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    DATAPRODUCERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SCTPSTREAMPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    remoteMomoId: str
    dataProducerId: str
    producerPeerId: str
    label: str
    protocol: str
    sctpStreamParameters: _sctp_stream_parameters_pb2.ProtoSctpStreamParameters
    appData: _containers.ScalarMap[str, str]
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
        dataProducerId: _Optional[str] = ...,
        producerPeerId: _Optional[str] = ...,
        label: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        sctpStreamParameters: _Optional[
            _Union[_sctp_stream_parameters_pb2.ProtoSctpStreamParameters, _Mapping]
        ] = ...,
        appData: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class PipeDataProduceResponse(_message.Message):
    __slots__ = ("roomId", "pipeDataProducerId", "status")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    PIPEDATAPRODUCERID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    pipeDataProducerId: str
    status: bool
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        pipeDataProducerId: _Optional[str] = ...,
        status: bool = ...,
    ) -> None: ...

class PipeDataConsumeRequest(_message.Message):
    __slots__ = ("roomId", "remoteMomoId", "dataProducerId", "producerPeerId")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    REMOTEMOMOID_FIELD_NUMBER: _ClassVar[int]
    DATAPRODUCERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    remoteMomoId: str
    dataProducerId: str
    producerPeerId: str
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        remoteMomoId: _Optional[str] = ...,
        dataProducerId: _Optional[str] = ...,
        producerPeerId: _Optional[str] = ...,
    ) -> None: ...

class PipeDataConsumeResponse(_message.Message):
    __slots__ = (
        "roomId",
        "producerPeerId",
        "sctpStreamParameters",
        "label",
        "protocol",
        "appData",
    )
    class AppDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    ROOMID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    SCTPSTREAMPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    producerPeerId: str
    sctpStreamParameters: _sctp_stream_parameters_pb2.ProtoSctpStreamParameters
    label: str
    protocol: str
    appData: _containers.ScalarMap[str, str]
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        producerPeerId: _Optional[str] = ...,
        sctpStreamParameters: _Optional[
            _Union[_sctp_stream_parameters_pb2.ProtoSctpStreamParameters, _Mapping]
        ] = ...,
        label: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        appData: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...
