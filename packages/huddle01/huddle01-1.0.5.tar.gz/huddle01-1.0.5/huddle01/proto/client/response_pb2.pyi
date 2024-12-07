from ..client import permissions_pb2 as _permissions_pb2
from ..client import app_data_pb2 as _app_data_pb2
from ..rtc import sdp_info_pb2 as _sdp_info_pb2
from ..rtc import sctp_stream_parameters_pb2 as _sctp_stream_parameters_pb2
from ..rtc import rtp_parameters_pb2 as _rtp_parameters_pb2
from ..rtc import rtp_capabilities_pb2 as _rtp_capabilities_pb2
from ..client import room_control_pb2 as _room_control_pb2
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

class Hello(_message.Message):
    __slots__ = ("peerId", "roomId", "sessionId", "acl", "role", "metadata")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    ACL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    roomId: str
    sessionId: str
    acl: _permissions_pb2.Permissions
    role: str
    metadata: str
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        roomId: _Optional[str] = ...,
        sessionId: _Optional[str] = ...,
        acl: _Optional[_Union[_permissions_pb2.Permissions, _Mapping]] = ...,
        role: _Optional[str] = ...,
        metadata: _Optional[str] = ...,
    ) -> None: ...

class RoomControls(_message.Message):
    __slots__ = (
        "roomLocked",
        "allowProduce",
        "allowProduceSources",
        "allowConsume",
        "allowSendData",
    )
    class ProduceSources(_message.Message):
        __slots__ = ("cam", "mic", "screen")
        CAM_FIELD_NUMBER: _ClassVar[int]
        MIC_FIELD_NUMBER: _ClassVar[int]
        SCREEN_FIELD_NUMBER: _ClassVar[int]
        cam: bool
        mic: bool
        screen: bool
        def __init__(
            self, cam: bool = ..., mic: bool = ..., screen: bool = ...
        ) -> None: ...

    ROOMLOCKED_FIELD_NUMBER: _ClassVar[int]
    ALLOWPRODUCE_FIELD_NUMBER: _ClassVar[int]
    ALLOWPRODUCESOURCES_FIELD_NUMBER: _ClassVar[int]
    ALLOWCONSUME_FIELD_NUMBER: _ClassVar[int]
    ALLOWSENDDATA_FIELD_NUMBER: _ClassVar[int]
    roomLocked: bool
    allowProduce: bool
    allowProduceSources: RoomControls.ProduceSources
    allowConsume: bool
    allowSendData: bool
    def __init__(
        self,
        roomLocked: bool = ...,
        allowProduce: bool = ...,
        allowProduceSources: _Optional[
            _Union[RoomControls.ProduceSources, _Mapping]
        ] = ...,
        allowConsume: bool = ...,
        allowSendData: bool = ...,
    ) -> None: ...

class PeersInfo(_message.Message):
    __slots__ = ("peerId", "metadata", "role", "producers")
    class ProducerInfo(_message.Message):
        __slots__ = ("id", "label", "paused")
        ID_FIELD_NUMBER: _ClassVar[int]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        PAUSED_FIELD_NUMBER: _ClassVar[int]
        id: str
        label: str
        paused: bool
        def __init__(
            self,
            id: _Optional[str] = ...,
            label: _Optional[str] = ...,
            paused: bool = ...,
        ) -> None: ...

    PEERID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    PRODUCERS_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    metadata: str
    role: str
    producers: _containers.RepeatedCompositeFieldContainer[PeersInfo.ProducerInfo]
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        metadata: _Optional[str] = ...,
        role: _Optional[str] = ...,
        producers: _Optional[_Iterable[_Union[PeersInfo.ProducerInfo, _Mapping]]] = ...,
    ) -> None: ...

class RoomInfo(_message.Message):
    __slots__ = ("roomLocked", "config", "peers", "lobbyPeers", "metadata", "startTime")
    ROOMLOCKED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    PEERS_FIELD_NUMBER: _ClassVar[int]
    LOBBYPEERS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    roomLocked: bool
    config: RoomControls
    peers: _containers.RepeatedCompositeFieldContainer[PeersInfo]
    lobbyPeers: _containers.RepeatedCompositeFieldContainer[LobbyPeers]
    metadata: str
    startTime: int
    def __init__(
        self,
        roomLocked: bool = ...,
        config: _Optional[_Union[RoomControls, _Mapping]] = ...,
        peers: _Optional[_Iterable[_Union[PeersInfo, _Mapping]]] = ...,
        lobbyPeers: _Optional[_Iterable[_Union[LobbyPeers, _Mapping]]] = ...,
        metadata: _Optional[str] = ...,
        startTime: _Optional[int] = ...,
    ) -> None: ...

class LobbyPeers(_message.Message):
    __slots__ = ("peerId", "metadata")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    metadata: str
    def __init__(
        self, peerId: _Optional[str] = ..., metadata: _Optional[str] = ...
    ) -> None: ...

class ConnectRoomResponse(_message.Message):
    __slots__ = ("roomId", "roomInfo", "routerRTPCapabilities", "turnServers")
    class RTCIceServer(_message.Message):
        __slots__ = ("urls", "username", "credential")
        URLS_FIELD_NUMBER: _ClassVar[int]
        USERNAME_FIELD_NUMBER: _ClassVar[int]
        CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
        urls: str
        username: str
        credential: str
        def __init__(
            self,
            urls: _Optional[str] = ...,
            username: _Optional[str] = ...,
            credential: _Optional[str] = ...,
        ) -> None: ...

    ROOMID_FIELD_NUMBER: _ClassVar[int]
    ROOMINFO_FIELD_NUMBER: _ClassVar[int]
    ROUTERRTPCAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    TURNSERVERS_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    roomInfo: RoomInfo
    routerRTPCapabilities: _rtp_capabilities_pb2.ProtoRtpCapabilities
    turnServers: _containers.RepeatedCompositeFieldContainer[
        ConnectRoomResponse.RTCIceServer
    ]
    def __init__(
        self,
        roomId: _Optional[str] = ...,
        roomInfo: _Optional[_Union[RoomInfo, _Mapping]] = ...,
        routerRTPCapabilities: _Optional[
            _Union[_rtp_capabilities_pb2.ProtoRtpCapabilities, _Mapping]
        ] = ...,
        turnServers: _Optional[
            _Iterable[_Union[ConnectRoomResponse.RTCIceServer, _Mapping]]
        ] = ...,
    ) -> None: ...

class CreateTransportOnClient(_message.Message):
    __slots__ = ("transportType", "transportSDPInfo")
    TRANSPORTTYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTSDPINFO_FIELD_NUMBER: _ClassVar[int]
    transportType: str
    transportSDPInfo: _sdp_info_pb2.ProtoTransportSDPInfo
    def __init__(
        self,
        transportType: _Optional[str] = ...,
        transportSDPInfo: _Optional[
            _Union[_sdp_info_pb2.ProtoTransportSDPInfo, _Mapping]
        ] = ...,
    ) -> None: ...

class ConnectTransportResponse(_message.Message):
    __slots__ = ("transportType", "transportId")
    TRANSPORTTYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTID_FIELD_NUMBER: _ClassVar[int]
    transportType: str
    transportId: str
    def __init__(
        self, transportType: _Optional[str] = ..., transportId: _Optional[str] = ...
    ) -> None: ...

class ProduceResponse(_message.Message):
    __slots__ = ("peerId", "producerId", "label", "appData")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    producerId: str
    label: str
    appData: _app_data_pb2.AppData
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        label: _Optional[str] = ...,
        appData: _Optional[_Union[_app_data_pb2.AppData, _Mapping]] = ...,
    ) -> None: ...

class ProduceDataResponse(_message.Message):
    __slots__ = (
        "id",
        "dataProducerId",
        "label",
        "peerId",
        "protocol",
        "sctpStreamParameters",
        "appData",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    DATAPRODUCERID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PEERID_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SCTPSTREAMPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    dataProducerId: str
    label: str
    peerId: str
    protocol: str
    sctpStreamParameters: _sctp_stream_parameters_pb2.ProtoSctpStreamParameters
    appData: _app_data_pb2.AppData
    def __init__(
        self,
        id: _Optional[str] = ...,
        dataProducerId: _Optional[str] = ...,
        label: _Optional[str] = ...,
        peerId: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        sctpStreamParameters: _Optional[
            _Union[_sctp_stream_parameters_pb2.ProtoSctpStreamParameters, _Mapping]
        ] = ...,
        appData: _Optional[_Union[_app_data_pb2.AppData, _Mapping]] = ...,
    ) -> None: ...

class ConsumeDataResponse(_message.Message):
    __slots__ = (
        "id",
        "dataProducerId",
        "label",
        "peerId",
        "protocol",
        "sctpStreamParameters",
        "appData",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    DATAPRODUCERID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PEERID_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SCTPSTREAMPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    dataProducerId: str
    label: str
    peerId: str
    protocol: str
    sctpStreamParameters: _sctp_stream_parameters_pb2.ProtoSctpStreamParameters
    appData: _app_data_pb2.AppData
    def __init__(
        self,
        id: _Optional[str] = ...,
        dataProducerId: _Optional[str] = ...,
        label: _Optional[str] = ...,
        peerId: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        sctpStreamParameters: _Optional[
            _Union[_sctp_stream_parameters_pb2.ProtoSctpStreamParameters, _Mapping]
        ] = ...,
        appData: _Optional[_Union[_app_data_pb2.AppData, _Mapping]] = ...,
    ) -> None: ...

class SyncMeetingStateResponse(_message.Message):
    __slots__ = ("roomInfo",)
    ROOMINFO_FIELD_NUMBER: _ClassVar[int]
    roomInfo: RoomInfo
    def __init__(
        self, roomInfo: _Optional[_Union[RoomInfo, _Mapping]] = ...
    ) -> None: ...

class ConsumeResponse(_message.Message):
    __slots__ = (
        "label",
        "consumerId",
        "producerId",
        "kind",
        "rtpParameters",
        "producerPeerId",
        "appData",
        "producerPaused",
    )
    LABEL_FIELD_NUMBER: _ClassVar[int]
    CONSUMERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RTPPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPAUSED_FIELD_NUMBER: _ClassVar[int]
    label: str
    consumerId: str
    producerId: str
    kind: str
    rtpParameters: _rtp_parameters_pb2.ProtoRtpParameters
    producerPeerId: str
    appData: _app_data_pb2.AppData
    producerPaused: bool
    def __init__(
        self,
        label: _Optional[str] = ...,
        consumerId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        rtpParameters: _Optional[
            _Union[_rtp_parameters_pb2.ProtoRtpParameters, _Mapping]
        ] = ...,
        producerPeerId: _Optional[str] = ...,
        appData: _Optional[_Union[_app_data_pb2.AppData, _Mapping]] = ...,
        producerPaused: bool = ...,
    ) -> None: ...

class CloseProducerSuccess(_message.Message):
    __slots__ = ("peerId", "producerId", "label")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    producerId: str
    label: str
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        label: _Optional[str] = ...,
    ) -> None: ...

class PauseProducerSuccess(_message.Message):
    __slots__ = ("peerId", "producerId", "label")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    producerId: str
    label: str
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        label: _Optional[str] = ...,
    ) -> None: ...

class ResumeProducerSuccess(_message.Message):
    __slots__ = ("peerId", "producerId", "label")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    producerId: str
    label: str
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        label: _Optional[str] = ...,
    ) -> None: ...

class CloseConsumerSuccess(_message.Message):
    __slots__ = ("peerId", "consumerId")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    CONSUMERID_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    consumerId: str
    def __init__(
        self, peerId: _Optional[str] = ..., consumerId: _Optional[str] = ...
    ) -> None: ...

class RestartTransportIceResponse(_message.Message):
    __slots__ = ("transportType", "iceParameters")
    TRANSPORTTYPE_FIELD_NUMBER: _ClassVar[int]
    ICEPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    transportType: str
    iceParameters: _sdp_info_pb2.ProtoIceParameters
    def __init__(
        self,
        transportType: _Optional[str] = ...,
        iceParameters: _Optional[
            _Union[_sdp_info_pb2.ProtoIceParameters, _Mapping]
        ] = ...,
    ) -> None: ...

class NewPeerJoined(_message.Message):
    __slots__ = ("peerId", "metadata", "role")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    metadata: str
    role: str
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        metadata: _Optional[str] = ...,
        role: _Optional[str] = ...,
    ) -> None: ...

class NewLobbyPeer(_message.Message):
    __slots__ = ("peerId", "metadata")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    metadata: str
    def __init__(
        self, peerId: _Optional[str] = ..., metadata: _Optional[str] = ...
    ) -> None: ...

class NewPermissions(_message.Message):
    __slots__ = ("acl",)
    ACL_FIELD_NUMBER: _ClassVar[int]
    acl: _permissions_pb2.Permissions
    def __init__(
        self, acl: _Optional[_Union[_permissions_pb2.Permissions, _Mapping]] = ...
    ) -> None: ...

class NewRoomControls(_message.Message):
    __slots__ = ("controls",)
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    controls: RoomControls
    def __init__(
        self, controls: _Optional[_Union[RoomControls, _Mapping]] = ...
    ) -> None: ...

class NewPeerRole(_message.Message):
    __slots__ = ("peerId", "role")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    role: str
    def __init__(
        self, peerId: _Optional[str] = ..., role: _Optional[str] = ...
    ) -> None: ...

class ReceiveData(_message.Message):
    __slots__ = ("payload", "label")
    FROM_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    payload: str
    label: str
    def __init__(
        self, payload: _Optional[str] = ..., label: _Optional[str] = ..., **kwargs
    ) -> None: ...

class PeerMetadataUpdated(_message.Message):
    __slots__ = ("peerId", "metadata")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    metadata: str
    def __init__(
        self, peerId: _Optional[str] = ..., metadata: _Optional[str] = ...
    ) -> None: ...

class RoomMetadataUpdated(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: str
    def __init__(self, metadata: _Optional[str] = ...) -> None: ...

class RoomClosedProducers(_message.Message):
    __slots__ = ("producers", "reason")
    class CloseProducerInfo(_message.Message):
        __slots__ = ("peerId", "producerId", "label")
        PEERID_FIELD_NUMBER: _ClassVar[int]
        PRODUCERID_FIELD_NUMBER: _ClassVar[int]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        peerId: str
        producerId: str
        label: str
        def __init__(
            self,
            peerId: _Optional[str] = ...,
            producerId: _Optional[str] = ...,
            label: _Optional[str] = ...,
        ) -> None: ...

    class CloseProducerReason(_message.Message):
        __slots__ = ("code", "tag", "message")
        CODE_FIELD_NUMBER: _ClassVar[int]
        TAG_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        code: int
        tag: str
        message: str
        def __init__(
            self,
            code: _Optional[int] = ...,
            tag: _Optional[str] = ...,
            message: _Optional[str] = ...,
        ) -> None: ...

    PRODUCERS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    producers: _containers.RepeatedCompositeFieldContainer[
        RoomClosedProducers.CloseProducerInfo
    ]
    reason: RoomClosedProducers.CloseProducerReason
    def __init__(
        self,
        producers: _Optional[
            _Iterable[_Union[RoomClosedProducers.CloseProducerInfo, _Mapping]]
        ] = ...,
        reason: _Optional[
            _Union[RoomClosedProducers.CloseProducerReason, _Mapping]
        ] = ...,
    ) -> None: ...

class PeerLeft(_message.Message):
    __slots__ = ("peerId",)
    PEERID_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    def __init__(self, peerId: _Optional[str] = ...) -> None: ...

class LobbyPeerLeft(_message.Message):
    __slots__ = ("peerId", "status", "message")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    status: str
    message: str
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        status: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class WaitingRoom(_message.Message):
    __slots__ = ("reason", "metadata")
    REASON_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    reason: str
    metadata: str
    def __init__(
        self, reason: _Optional[str] = ..., metadata: _Optional[str] = ...
    ) -> None: ...

class Error(_message.Message):
    __slots__ = ("event", "error")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    event: str
    error: str
    def __init__(
        self, event: _Optional[str] = ..., error: _Optional[str] = ...
    ) -> None: ...

class Response(_message.Message):
    __slots__ = (
        "hello",
        "connectRoomResponse",
        "createTransportOnClient",
        "produceResponse",
        "consumeDataResponse",
        "produceDataResponse",
        "syncMeetingStateResponse",
        "consumeResponse",
        "closeProducerSuccess",
        "pauseProducerSuccess",
        "resumeProducerSuccess",
        "closeConsumerSuccess",
        "connectTransportResponse",
        "restartTransportIceResponse",
        "newPeerJoined",
        "newLobbyPeer",
        "newPermissions",
        "newRoomControls",
        "newPeerRole",
        "receiveData",
        "peerMetadataUpdated",
        "roomMetadataUpdated",
        "roomClosedProducers",
        "peerLeft",
        "lobbyPeerLeft",
        "waitingRoom",
        "error",
    )
    HELLO_FIELD_NUMBER: _ClassVar[int]
    CONNECTROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATETRANSPORTONCLIENT_FIELD_NUMBER: _ClassVar[int]
    PRODUCERESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONSUMEDATARESPONSE_FIELD_NUMBER: _ClassVar[int]
    PRODUCEDATARESPONSE_FIELD_NUMBER: _ClassVar[int]
    SYNCMEETINGSTATERESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONSUMERESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLOSEPRODUCERSUCCESS_FIELD_NUMBER: _ClassVar[int]
    PAUSEPRODUCERSUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESUMEPRODUCERSUCCESS_FIELD_NUMBER: _ClassVar[int]
    CLOSECONSUMERSUCCESS_FIELD_NUMBER: _ClassVar[int]
    CONNECTTRANSPORTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    RESTARTTRANSPORTICERESPONSE_FIELD_NUMBER: _ClassVar[int]
    NEWPEERJOINED_FIELD_NUMBER: _ClassVar[int]
    NEWLOBBYPEER_FIELD_NUMBER: _ClassVar[int]
    NEWPERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    NEWROOMCONTROLS_FIELD_NUMBER: _ClassVar[int]
    NEWPEERROLE_FIELD_NUMBER: _ClassVar[int]
    RECEIVEDATA_FIELD_NUMBER: _ClassVar[int]
    PEERMETADATAUPDATED_FIELD_NUMBER: _ClassVar[int]
    ROOMMETADATAUPDATED_FIELD_NUMBER: _ClassVar[int]
    ROOMCLOSEDPRODUCERS_FIELD_NUMBER: _ClassVar[int]
    PEERLEFT_FIELD_NUMBER: _ClassVar[int]
    LOBBYPEERLEFT_FIELD_NUMBER: _ClassVar[int]
    WAITINGROOM_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    hello: Hello
    connectRoomResponse: ConnectRoomResponse
    createTransportOnClient: CreateTransportOnClient
    produceResponse: ProduceResponse
    consumeDataResponse: ConsumeDataResponse
    produceDataResponse: ProduceDataResponse
    syncMeetingStateResponse: SyncMeetingStateResponse
    consumeResponse: ConsumeResponse
    closeProducerSuccess: CloseProducerSuccess
    pauseProducerSuccess: PauseProducerSuccess
    resumeProducerSuccess: ResumeProducerSuccess
    closeConsumerSuccess: CloseConsumerSuccess
    connectTransportResponse: ConnectTransportResponse
    restartTransportIceResponse: RestartTransportIceResponse
    newPeerJoined: NewPeerJoined
    newLobbyPeer: NewLobbyPeer
    newPermissions: NewPermissions
    newRoomControls: NewRoomControls
    newPeerRole: NewPeerRole
    receiveData: ReceiveData
    peerMetadataUpdated: PeerMetadataUpdated
    roomMetadataUpdated: RoomMetadataUpdated
    roomClosedProducers: RoomClosedProducers
    peerLeft: PeerLeft
    lobbyPeerLeft: LobbyPeerLeft
    waitingRoom: WaitingRoom
    error: Error
    def __init__(
        self,
        hello: _Optional[_Union[Hello, _Mapping]] = ...,
        connectRoomResponse: _Optional[_Union[ConnectRoomResponse, _Mapping]] = ...,
        createTransportOnClient: _Optional[
            _Union[CreateTransportOnClient, _Mapping]
        ] = ...,
        produceResponse: _Optional[_Union[ProduceResponse, _Mapping]] = ...,
        consumeDataResponse: _Optional[_Union[ConsumeDataResponse, _Mapping]] = ...,
        produceDataResponse: _Optional[_Union[ProduceDataResponse, _Mapping]] = ...,
        syncMeetingStateResponse: _Optional[
            _Union[SyncMeetingStateResponse, _Mapping]
        ] = ...,
        consumeResponse: _Optional[_Union[ConsumeResponse, _Mapping]] = ...,
        closeProducerSuccess: _Optional[_Union[CloseProducerSuccess, _Mapping]] = ...,
        pauseProducerSuccess: _Optional[_Union[PauseProducerSuccess, _Mapping]] = ...,
        resumeProducerSuccess: _Optional[_Union[ResumeProducerSuccess, _Mapping]] = ...,
        closeConsumerSuccess: _Optional[_Union[CloseConsumerSuccess, _Mapping]] = ...,
        connectTransportResponse: _Optional[
            _Union[ConnectTransportResponse, _Mapping]
        ] = ...,
        restartTransportIceResponse: _Optional[
            _Union[RestartTransportIceResponse, _Mapping]
        ] = ...,
        newPeerJoined: _Optional[_Union[NewPeerJoined, _Mapping]] = ...,
        newLobbyPeer: _Optional[_Union[NewLobbyPeer, _Mapping]] = ...,
        newPermissions: _Optional[_Union[NewPermissions, _Mapping]] = ...,
        newRoomControls: _Optional[_Union[NewRoomControls, _Mapping]] = ...,
        newPeerRole: _Optional[_Union[NewPeerRole, _Mapping]] = ...,
        receiveData: _Optional[_Union[ReceiveData, _Mapping]] = ...,
        peerMetadataUpdated: _Optional[_Union[PeerMetadataUpdated, _Mapping]] = ...,
        roomMetadataUpdated: _Optional[_Union[RoomMetadataUpdated, _Mapping]] = ...,
        roomClosedProducers: _Optional[_Union[RoomClosedProducers, _Mapping]] = ...,
        peerLeft: _Optional[_Union[PeerLeft, _Mapping]] = ...,
        lobbyPeerLeft: _Optional[_Union[LobbyPeerLeft, _Mapping]] = ...,
        waitingRoom: _Optional[_Union[WaitingRoom, _Mapping]] = ...,
        error: _Optional[_Union[Error, _Mapping]] = ...,
    ) -> None: ...
