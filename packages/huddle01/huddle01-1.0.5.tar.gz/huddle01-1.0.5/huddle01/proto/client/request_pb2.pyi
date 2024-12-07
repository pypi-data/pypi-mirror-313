from typing import (
    ClassVar as _ClassVar,
)
from typing import (
    Iterable as _Iterable,
)
from typing import (
    Mapping as _Mapping,
)
from typing import (
    Optional as _Optional,
)
from typing import (
    Union as _Union,
)

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

from ..client import app_data_pb2 as _app_data_pb2
from ..client import permissions_pb2 as _permissions_pb2
from ..client import room_control_pb2 as _room_control_pb2
from ..rtc import rtp_parameters_pb2 as _rtp_parameters_pb2
from ..rtc import sctp_capabilities_pb2 as _sctp_capabilities_pb2
from ..rtc import sctp_stream_parameters_pb2 as _sctp_stream_parameters_pb2
from ..rtc import sdp_info_pb2 as _sdp_info_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class TestEvent(_message.Message):
    __slots__ = ("name", "payload", "to")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    name: str
    payload: str
    to: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        payload: _Optional[str] = ...,
        to: _Optional[str] = ...,
        **kwargs,
    ) -> None: ...

class ConnectRoom(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class CreateTransport(_message.Message):
    __slots__ = ("sctpCapabilities", "transportType")
    SCTPCAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTTYPE_FIELD_NUMBER: _ClassVar[int]
    sctpCapabilities: _sctp_capabilities_pb2.ProtoSctpCapabilities
    transportType: str
    def __init__(
        self,
        sctpCapabilities: _Optional[
            _Union[_sctp_capabilities_pb2.ProtoSctpCapabilities, _Mapping]
        ] = ...,
        transportType: _Optional[str] = ...,
    ) -> None: ...

class ConnectTransport(_message.Message):
    __slots__ = ("transportType", "dtlsParameters")
    TRANSPORTTYPE_FIELD_NUMBER: _ClassVar[int]
    DTLSPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    transportType: str
    dtlsParameters: _sdp_info_pb2.ProtoDtlsParameters
    def __init__(
        self,
        transportType: _Optional[str] = ...,
        dtlsParameters: _Optional[
            _Union[_sdp_info_pb2.ProtoDtlsParameters, _Mapping]
        ] = ...,
    ) -> None: ...

class CreateDataConsumer(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: str
    def __init__(self, label: _Optional[str] = ...) -> None: ...

class Produce(_message.Message):
    __slots__ = ("label", "kind", "rtpParameters", "paused", "appData")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RTPPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    label: str
    kind: str
    rtpParameters: _rtp_parameters_pb2.ProtoRtpParameters
    paused: bool
    appData: _app_data_pb2.AppData
    def __init__(
        self,
        label: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        rtpParameters: _Optional[
            _Union[_rtp_parameters_pb2.ProtoRtpParameters, _Mapping]
        ] = ...,
        paused: bool = ...,
        appData: _Optional[_Union[_app_data_pb2.AppData, _Mapping]] = ...,
    ) -> None: ...

class ProduceData(_message.Message):
    __slots__ = ("transportId", "sctpStreamParameters", "label", "protocol", "appData")
    TRANSPORTID_FIELD_NUMBER: _ClassVar[int]
    SCTPSTREAMPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    transportId: str
    sctpStreamParameters: _sctp_stream_parameters_pb2.ProtoSctpStreamParameters
    label: str
    protocol: str
    appData: _app_data_pb2.AppData
    def __init__(
        self,
        transportId: _Optional[str] = ...,
        sctpStreamParameters: _Optional[
            _Union[_sctp_stream_parameters_pb2.ProtoSctpStreamParameters, _Mapping]
        ] = ...,
        label: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        appData: _Optional[_Union[_app_data_pb2.AppData, _Mapping]] = ...,
    ) -> None: ...

class Consume(_message.Message):
    __slots__ = ("producerPeerId", "producerId", "appData")
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    producerPeerId: str
    producerId: str
    appData: _app_data_pb2.AppData
    def __init__(
        self,
        producerPeerId: _Optional[str] = ...,
        producerId: _Optional[str] = ...,
        appData: _Optional[_Union[_app_data_pb2.AppData, _Mapping]] = ...,
    ) -> None: ...

class CloseProducer(_message.Message):
    __slots__ = ("producerId",)
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    producerId: str
    def __init__(self, producerId: _Optional[str] = ...) -> None: ...

class PauseProducer(_message.Message):
    __slots__ = ("producerId",)
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    producerId: str
    def __init__(self, producerId: _Optional[str] = ...) -> None: ...

class ResumeProducer(_message.Message):
    __slots__ = ("producerId",)
    PRODUCERID_FIELD_NUMBER: _ClassVar[int]
    producerId: str
    def __init__(self, producerId: _Optional[str] = ...) -> None: ...

class CloseConsumer(_message.Message):
    __slots__ = ("consumerId",)
    CONSUMERID_FIELD_NUMBER: _ClassVar[int]
    consumerId: str
    def __init__(self, consumerId: _Optional[str] = ...) -> None: ...

class ResumeConsumer(_message.Message):
    __slots__ = ("consumerId", "producerPeerId")
    CONSUMERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCERPEERID_FIELD_NUMBER: _ClassVar[int]
    consumerId: str
    producerPeerId: str
    def __init__(
        self, consumerId: _Optional[str] = ..., producerPeerId: _Optional[str] = ...
    ) -> None: ...

class SyncMeetingState(_message.Message):
    __slots__ = ("localProducerIds",)
    LOCALPRODUCERIDS_FIELD_NUMBER: _ClassVar[int]
    localProducerIds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, localProducerIds: _Optional[_Iterable[str]] = ...) -> None: ...

class RestartTransportIce(_message.Message):
    __slots__ = ("transportType", "transportId")
    TRANSPORTTYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTID_FIELD_NUMBER: _ClassVar[int]
    transportType: str
    transportId: str
    def __init__(
        self, transportType: _Optional[str] = ..., transportId: _Optional[str] = ...
    ) -> None: ...

class SendData(_message.Message):
    __slots__ = ("to", "label", "payload")
    TO_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    to: _containers.RepeatedScalarFieldContainer[str]
    label: str
    payload: str
    def __init__(
        self,
        to: _Optional[_Iterable[str]] = ...,
        label: _Optional[str] = ...,
        payload: _Optional[str] = ...,
    ) -> None: ...

class UpdateRoomControls(_message.Message):
    __slots__ = ("room_control", "produce_sources_control")
    ROOM_CONTROL_FIELD_NUMBER: _ClassVar[int]
    PRODUCE_SOURCES_CONTROL_FIELD_NUMBER: _ClassVar[int]
    room_control: _room_control_pb2.RoomControlType
    produce_sources_control: _room_control_pb2.ProduceSourcesControl
    def __init__(
        self,
        room_control: _Optional[
            _Union[_room_control_pb2.RoomControlType, _Mapping]
        ] = ...,
        produce_sources_control: _Optional[
            _Union[_room_control_pb2.ProduceSourcesControl, _Mapping]
        ] = ...,
    ) -> None: ...

class UpdatePeerPermission(_message.Message):
    __slots__ = ("peerId", "permissions")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    permissions: _permissions_pb2.Permissions
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        permissions: _Optional[_Union[_permissions_pb2.Permissions, _Mapping]] = ...,
    ) -> None: ...

class ActivateSpeakerNotification(_message.Message):
    __slots__ = ("size",)
    SIZE_FIELD_NUMBER: _ClassVar[int]
    size: int
    def __init__(self, size: _Optional[int] = ...) -> None: ...

class UpdatePeerRole(_message.Message):
    __slots__ = ("peerId", "role", "options")
    class Options(_message.Message):
        __slots__ = ("custom",)
        CUSTOM_FIELD_NUMBER: _ClassVar[int]
        custom: _permissions_pb2.Permissions
        def __init__(
            self,
            custom: _Optional[_Union[_permissions_pb2.Permissions, _Mapping]] = ...,
        ) -> None: ...

    PEERID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    role: str
    options: UpdatePeerRole.Options
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        role: _Optional[str] = ...,
        options: _Optional[_Union[UpdatePeerRole.Options, _Mapping]] = ...,
    ) -> None: ...

class UpdatePeerMetadata(_message.Message):
    __slots__ = ("peerId", "metadata")
    PEERID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    metadata: str
    def __init__(
        self, peerId: _Optional[str] = ..., metadata: _Optional[str] = ...
    ) -> None: ...

class UpdateRoomMetadata(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: str
    def __init__(self, metadata: _Optional[str] = ...) -> None: ...

class CloseStreamOfLabel(_message.Message):
    __slots__ = ("label", "peerIds")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PEERIDS_FIELD_NUMBER: _ClassVar[int]
    label: str
    peerIds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, label: _Optional[str] = ..., peerIds: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class AcceptLobbyPeer(_message.Message):
    __slots__ = ("peerId",)
    PEERID_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    def __init__(self, peerId: _Optional[str] = ...) -> None: ...

class DenyLobbyPeer(_message.Message):
    __slots__ = ("peerId",)
    PEERID_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    def __init__(self, peerId: _Optional[str] = ...) -> None: ...

class KickPeer(_message.Message):
    __slots__ = ("peerId",)
    PEERID_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    def __init__(self, peerId: _Optional[str] = ...) -> None: ...

class CloseRoom(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Request(_message.Message):
    __slots__ = (
        "connect_room",
        "create_transport",
        "connect_transport",
        "create_data_consumer",
        "produce",
        "produce_data",
        "consume",
        "close_producer",
        "pause_producer",
        "resume_producer",
        "close_consumer",
        "resume_consumer",
        "sync_meeting_state",
        "restart_transport_ice",
        "send_data",
        "update_room_controls",
        "update_peer_permission",
        "activate_speaker_notification",
        "update_peer_role",
        "update_peer_metadata",
        "update_room_metadata",
        "close_stream_of_label",
        "accept_lobby_peer",
        "deny_lobby_peer",
        "kick_peer",
        "close_room",
    )
    CONNECT_ROOM_FIELD_NUMBER: _ClassVar[int]
    CREATE_TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    CONNECT_TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    CREATE_DATA_CONSUMER_FIELD_NUMBER: _ClassVar[int]
    PRODUCE_FIELD_NUMBER: _ClassVar[int]
    PRODUCE_DATA_FIELD_NUMBER: _ClassVar[int]
    CONSUME_FIELD_NUMBER: _ClassVar[int]
    CLOSE_PRODUCER_FIELD_NUMBER: _ClassVar[int]
    PAUSE_PRODUCER_FIELD_NUMBER: _ClassVar[int]
    RESUME_PRODUCER_FIELD_NUMBER: _ClassVar[int]
    CLOSE_CONSUMER_FIELD_NUMBER: _ClassVar[int]
    RESUME_CONSUMER_FIELD_NUMBER: _ClassVar[int]
    SYNC_MEETING_STATE_FIELD_NUMBER: _ClassVar[int]
    RESTART_TRANSPORT_ICE_FIELD_NUMBER: _ClassVar[int]
    SEND_DATA_FIELD_NUMBER: _ClassVar[int]
    UPDATE_ROOM_CONTROLS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PEER_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_SPEAKER_NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PEER_ROLE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PEER_METADATA_FIELD_NUMBER: _ClassVar[int]
    UPDATE_ROOM_METADATA_FIELD_NUMBER: _ClassVar[int]
    CLOSE_STREAM_OF_LABEL_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_LOBBY_PEER_FIELD_NUMBER: _ClassVar[int]
    DENY_LOBBY_PEER_FIELD_NUMBER: _ClassVar[int]
    KICK_PEER_FIELD_NUMBER: _ClassVar[int]
    CLOSE_ROOM_FIELD_NUMBER: _ClassVar[int]
    connect_room: ConnectRoom
    create_transport: CreateTransport
    connect_transport: ConnectTransport
    create_data_consumer: CreateDataConsumer
    produce: Produce
    produce_data: ProduceData
    consume: Consume
    close_producer: CloseProducer
    pause_producer: PauseProducer
    resume_producer: ResumeProducer
    close_consumer: CloseConsumer
    resume_consumer: ResumeConsumer
    sync_meeting_state: SyncMeetingState
    restart_transport_ice: RestartTransportIce
    send_data: SendData
    update_room_controls: UpdateRoomControls
    update_peer_permission: UpdatePeerPermission
    activate_speaker_notification: ActivateSpeakerNotification
    update_peer_role: UpdatePeerRole
    update_peer_metadata: UpdatePeerMetadata
    update_room_metadata: UpdateRoomMetadata
    close_stream_of_label: CloseStreamOfLabel
    accept_lobby_peer: AcceptLobbyPeer
    deny_lobby_peer: DenyLobbyPeer
    kick_peer: KickPeer
    close_room: CloseRoom
    def __init__(
        self,
        connect_room: _Optional[_Union[ConnectRoom, _Mapping]] = ...,
        create_transport: _Optional[_Union[CreateTransport, _Mapping]] = ...,
        connect_transport: _Optional[_Union[ConnectTransport, _Mapping]] = ...,
        create_data_consumer: _Optional[_Union[CreateDataConsumer, _Mapping]] = ...,
        produce: _Optional[_Union[Produce, _Mapping]] = ...,
        produce_data: _Optional[_Union[ProduceData, _Mapping]] = ...,
        consume: _Optional[_Union[Consume, _Mapping]] = ...,
        close_producer: _Optional[_Union[CloseProducer, _Mapping]] = ...,
        pause_producer: _Optional[_Union[PauseProducer, _Mapping]] = ...,
        resume_producer: _Optional[_Union[ResumeProducer, _Mapping]] = ...,
        close_consumer: _Optional[_Union[CloseConsumer, _Mapping]] = ...,
        resume_consumer: _Optional[_Union[ResumeConsumer, _Mapping]] = ...,
        sync_meeting_state: _Optional[_Union[SyncMeetingState, _Mapping]] = ...,
        restart_transport_ice: _Optional[_Union[RestartTransportIce, _Mapping]] = ...,
        send_data: _Optional[_Union[SendData, _Mapping]] = ...,
        update_room_controls: _Optional[_Union[UpdateRoomControls, _Mapping]] = ...,
        update_peer_permission: _Optional[_Union[UpdatePeerPermission, _Mapping]] = ...,
        activate_speaker_notification: _Optional[
            _Union[ActivateSpeakerNotification, _Mapping]
        ] = ...,
        update_peer_role: _Optional[_Union[UpdatePeerRole, _Mapping]] = ...,
        update_peer_metadata: _Optional[_Union[UpdatePeerMetadata, _Mapping]] = ...,
        update_room_metadata: _Optional[_Union[UpdateRoomMetadata, _Mapping]] = ...,
        close_stream_of_label: _Optional[_Union[CloseStreamOfLabel, _Mapping]] = ...,
        accept_lobby_peer: _Optional[_Union[AcceptLobbyPeer, _Mapping]] = ...,
        deny_lobby_peer: _Optional[_Union[DenyLobbyPeer, _Mapping]] = ...,
        kick_peer: _Optional[_Union[KickPeer, _Mapping]] = ...,
        close_room: _Optional[_Union[CloseRoom, _Mapping]] = ...,
    ) -> None: ...
