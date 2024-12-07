import asyncio
from typing import Optional

from pydantic import BaseModel

from .active_speaker import ActiveSpeakersOptions
from .handlers import Response
from .handlers.socket_handler import SocketResponseEvents
from .local_peer import LocalPeer, LocalPeerOptions
from .log import base_logger
from .permissions import ACL, Permissions, ProduceSources
from .room import Room, RoomOptions
from .socket import ConnectionState as SocketConnectionState
from .socket import Socket, SocketCloseCode

logger = base_logger.getChild("Client")


class HuddleClientOptions(BaseModel):
    autoConsume: Optional[bool] = True
    volatileMessaging: Optional[bool] = False
    activeSpeakers: Optional[ActiveSpeakersOptions] = None


class HuddleClient:
    def __init__(self, project_id, options: HuddleClientOptions):
        # Project Id of the Huddle Project
        self.project_id = project_id

        # Options for the Huddle Client
        self.options = options

        # Socket which is going to be used for communication
        self.__socket: Optional[Socket] = None

        # Local Peer is the Local User, who is going to be connected to the Room
        self.local_peer: Optional[LocalPeer] = None

        # Room is the Room, where the Local Peer is going to be connected
        self.room: Optional[Room] = None

    def __subscribe_to_socket_events(self):
        """
        Subscribe to the Socket Events, acts as a Events bus to Accept Socket Events
        and handle logic between different components
        """
        if self.__socket is None:
            raise ValueError(
                "Socket is not created, make sure to create the Socket before subscribing to the events"
            )

    async def create(self, room_id: str, token: str) -> Room:
        """
        Creates the Local Peer and Room
        and connects to the Room
        """
        self.local_peer = await self._create_peer(token)

        self.room = await self._create_room(room_id)

        return self.room

    async def _create_peer(self, token: str) -> LocalPeer:
        """
        Create a Peer for the Local User, who is going to be connected to the Room
        Connects to the Huddle01 Sockets and After receiving the Hello Event, creates the Local Peer
        """
        self.__socket = Socket()

        self.__subscribe_to_socket_events()

        local_peer_created = asyncio.Event()

        @self.__socket.on(SocketResponseEvents.Hello)
        async def socket_hello(data: Response.Hello):
            if self.__socket is None:
                raise ValueError(
                    "Socket is not created, make sure to create the Socket before creating the Local Peer"
                )

            if self.__socket.connection_state != SocketConnectionState.CONNECTED:
                raise ValueError(
                    "Socket is not connected, make sure to connect the Socket before creating the Local Peer"
                )

            if self.local_peer:
                logger.info("Local Peer Reconnected, Updating the Local Peer")
                return

            logger.info(f"Creating Local Peer: {data.peerId}")

            local_peer_options = LocalPeerOptions(
                peer_id=data.peerId,
                session_id=data.sessionId,
                permissions=Permissions(
                    ACL(
                        admin=data.acl.admin,
                        can_consume=data.acl.canConsume,
                        can_produce=data.acl.canProduce,
                        can_produce_sources=ProduceSources(
                            cam=data.acl.canProduceSources.cam,
                            mic=data.acl.canProduceSources.mic,
                            screen=data.acl.canProduceSources.screen,
                        ),
                        can_send_data=data.acl.canSendData,
                        can_recv_data=data.acl.canRecvData,
                        can_update_metadata=data.acl.canUpdateMetadata,
                    ),
                    data.role,
                ),
                volatile_messaging=True if self.options.volatileMessaging else False,
            )

            # Create the Local Peer - When the Hello Event is received
            self.local_peer = LocalPeer(
                options=local_peer_options,
                socket=self.__socket,
            )

            local_peer_created.set()

        await self.__socket.connect(token)

        await local_peer_created.wait()

        if not self.local_peer:
            raise ValueError(
                "Local Peer is not created, But the Event is received, this should not happen"
            )

        return self.local_peer

    async def _create_room(self, room_id: str):
        """
        Create a Room for the Local Peer to join
        """
        if not self.local_peer:
            raise ValueError(
                "Local Peer is not created, make sure to create the Local Peer before creating the Room"
            )

        if not self.__socket:
            raise ValueError(
                "Socket is not created, make sure to create the Socket before creating the Room"
            )

        if self.__socket.connection_state != SocketConnectionState.CONNECTED:
            raise ValueError(
                "Socket is not connected, make sure to connect the Socket before creating the Room"
            )

        if self.room:
            raise ValueError(
                "Room is already created, make sure to close the connection before creating a new Room"
            )

        roomOptions = RoomOptions(room_id=room_id)

        room = Room(
            local_peer=self.local_peer, socket=self.__socket, options=roomOptions
        )

        self.local_peer._set_room(room)

        return room

    async def close(self):
        """
        Close the Huddle Client, and every other associated resources,
        like Local Peer, Room, and Socket. This should be called when the Client needs to leave the room
        """
        if self.__socket:
            await self.__socket.close(SocketCloseCode.GOING_AWAY)
