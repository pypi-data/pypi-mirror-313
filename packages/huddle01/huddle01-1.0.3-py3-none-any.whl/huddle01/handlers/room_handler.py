from typing import Literal, TypedDict

from pymediasoup.consumer import Consumer

from huddle01.remote_peer import RemotePeer


class RoomEvents(str):
    RoomJoined = "room_joined"
    RoomJoinFailed = "room_join_failed"
    RoomClosed = "room_closed"
    RoomConnecting = "room_connecting"
    RoomWaiting = "room_waiting"
    NewPeerJoined = "new_peer_joined"
    LobbyPeerUpdated = "lobby_peer_updated"
    NewLobbyPeer = "new_lobby_peer"
    MetadataUpdated = "metadata_updated"
    RemotePeerLeft = "remote_peer_left"
    RoomControlsUpdated = "room_controls_updated"
    ActiveSpeakersChanged = "active_speakers_changed"
    RemotePeerRoleUpdated = "remote_peer_role_updated"

    RemoteProducerAdded = "remote_producer_added"
    RemoteProducerClosed = "remote_producer_closed"

    NewConsumerAdded = "consumer_added"
    ConsumerClosed = "consumer_closed"
    ConsumerPaused = "consumer_paused"
    ConsumerResumed = "consumer_resumed"

class RoomEventsData:

    class RoomJoinFailed(TypedDict):
        error: str

    class RoomClosed(TypedDict):
        room_id: str

    class RoomConnecting(TypedDict):
        room_id: str

    class RoomWaiting(TypedDict):
        reason: str
    
    class NewPeerJoined(TypedDict):
        remote_peer_id: str
        remote_peer: RemotePeer

    class NewConsumerAdded(TypedDict):
        kind: Literal["audio", "video"]
        label: str
        consumer_id: str
        consumer: Consumer

    class ConsumerClosed(TypedDict):
        consumer_id: str
        label: str

    class ConsumerResumed(TypedDict):
        consumer_id: str
        label: str

    class ConsumerPaused(TypedDict):
        consumer_id: str
        label: str

    class RemotePeerLeft(TypedDict):
        remote_peer_id: str
    
    class RemoteProducerAdded(TypedDict):
        remote_peer_id: str
        label: str
        producer_id: str

    class RemoteProducerClosed(TypedDict):
        remote_peer_id: str
        producer_id: str
        label: str
