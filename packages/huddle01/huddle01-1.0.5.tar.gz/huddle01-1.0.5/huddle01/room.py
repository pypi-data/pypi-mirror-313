"""
Room Module defines the Room Class, which is used to connect to a Room
"""

from typing import Dict, List, Optional

from pydantic import BaseModel

from huddle01.bot import Bot

from .active_speaker import ActiveSpeakersOptions
from .emitter import EnhancedEventEmitter
from .handlers import Request, Response
from .handlers.room_handler import RoomEvents, RoomEventsData
from .handlers.socket_handler import SocketRequestEvents
from .local_peer import LocalPeer
from .log import base_logger
from .remote_peer import RemotePeer, RemotePeerData, RemotePeerProducer
from .socket import Socket

logger = base_logger.getChild("Room")


class ConnectionState:
    """
    ConnectionState defines the different states in which the
    """

    IDLE = "idle"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    FAILED = "failed"


class RoomOptions(BaseModel):
    """
    RoomOptions defines the options which are required to
    """

    room_id: str
    active_speakers: Optional[ActiveSpeakersOptions] = None


class LobbyPeer:
    """
    LobbyPeer defines the structure of the Peer which is in the Lobby
    """

    def __init__(self, peer_id: str, metadata: Optional[str] = None):
        self.peer_id = peer_id
        self.metadata = metadata


class Room(EnhancedEventEmitter):
    """
    Room is defined as a grouping of different Peers, who all are connected and communicating
    under a common RoomId.

    A Room can have multiple Peers, and each Peer can have multiple Tracks, every Peer based on there
    Roles and Permissions can Produce or Consume Tracks.

    Room class exposes the following events:
    - open -> Emitted when the Room is successfully opened
    - close -> Emitted when the Room is closed
    - error -> Emitted when there is an error in Room
    """

    def __init__(self, options: RoomOptions, socket: Socket, local_peer: LocalPeer):
        super(Room, self).__init__()

        logger.info("[constructor] Room, initializing")

        # Id of the Current Room, attempting to join
        self.room_id = options.room_id

        # Socket Instance, to be used for communication
        self.__socket = socket

        # Local Peer Instance, which is the Local User
        self.__local_peer = local_peer

        # Remote Peers Connected to the Room
        self.__remote_peers: Dict[str, RemotePeer] = {}

        # Lobby Peers Connected to the Room
        self.__lobby_peers: Dict[str, LobbyPeer] = {}

        # State of the Room
        self.__state = ConnectionState.IDLE

        self.bot: Optional[Bot] = None

    @property
    def local_peer(self):
        """
        Local Peer is the Local User, who is connected to the Room
        """
        return self.__local_peer

    @property
    def state(self):
        return self.__state

    @property
    def remote_peers(self):
        return self.__remote_peers

    @property
    def lobby_peers(self):
        return self.__lobby_peers

    async def connect(self):
        """
        Connects to the Room with the given RoomId, and starts listening to the Room Events
        Emits the join event, when the Room is successfully joined
        """
        if self.state == ConnectionState.CONNECTING:
            raise Exception(f"Room is already in {self.state} state")

        if self.state == ConnectionState.CONNECTED:
            raise Exception("Room is already Connected")

        self.__state = ConnectionState.CONNECTING

        logger.info(f"Connecting to Room: {self.room_id}")

        try:
            await self.__socket.request(
                SocketRequestEvents.ConnectRoom,
                Request.ConnectRoom(roomId=self.room_id),
            )

            await self.__local_peer.joined

            self.__state = ConnectionState.CONNECTED

            logger.info(f"Connected to Room: {self.room_id}")

            self.emit(RoomEvents.RoomJoined)
        except Exception as e:
            logger.error(f"Error in connecting to Room: {e}")

            self.emit(RoomEvents.RoomJoinFailed, e)

            self.__state = ConnectionState.FAILED

            raise

    def _update_room_info(
        self, room_info: Response.RoomInfo
    ) -> List[RemotePeerProducer]:
        """
        Internal Method to update the Room Info based on the RoomInfo received,
        Returns the list of ProducerIds of the Remote Peers
        """
        try:
            logger.info("Updating Room Info")

            remote_producers: List[RemotePeerProducer] = []

            for peer in room_info.peers:
                if peer.peerId == self.__local_peer.peer_id:
                    continue

                label_to_producer: Dict[str, RemotePeerProducer] = {}

                for producer in peer.producers:
                    remote_producer = RemotePeerProducer(
                        peer_id=peer.peerId,
                        label=producer.label,
                        producer_id=producer.id,
                        consuming=False,
                    )

                    label_to_producer.update({remote_producer.label: remote_producer})

                    remote_producers.append(remote_producer)

                remotePeer = RemotePeer(
                    RemotePeerData(
                        peer_id=peer.peerId,
                        metadata=peer.metadata,
                        role=peer.role,
                        label_to_producers=label_to_producer,
                    ),
                )

                self.__remote_peers.update({peer.peerId: remotePeer})

                self.emit(RoomEvents.NewPeerJoined, RoomEventsData.NewPeerJoined(
                    remote_peer=remotePeer,
                    remote_peer_id=peer.peerId,
                ))

            for peer in room_info.lobbyPeers:
                lobby_peer = LobbyPeer(peer_id=peer.peerId, metadata=peer.metadata)

                self.__lobby_peers.update({peer.peerId: lobby_peer})

            return remote_producers

        except Exception as e:
            logger.error(f"Error in updating Room Info: {e}")

            raise
