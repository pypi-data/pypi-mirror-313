import asyncio
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Union,
    cast,
)

from pydantic import BaseModel, Field, validator
from pymediasoup.models.transport import IceCandidate

from huddle01.bot import Bot, BotOptions, VolatileDataMessage
from huddle01.handlers.local_peer_handler import (
    DataConsumerOptions,
    DataProducerOptions,
    IceRestartDebounce,
    LocalPeerEvents,
    SendDataResult,
)
from huddle01.proto.client.request_pb2 import RestartTransportIce
from huddle01.remote_peer import RemotePeer

from .async_manager import AsyncOperationManager, OperationsType
from .emitter import EnhancedEventEmitter
from .handlers import (
    ConsumeOptions,
    MediaKind,
    ProduceOptions,
    Request,
    Response,
    RTCIceServer,
    SendDataOptions,
)
from .handlers.room_handler import RoomEvents, RoomEventsData
from .handlers.socket_handler import SocketRequestEvents, SocketResponseEvents
from .log import base_logger
from .permissions import Permissions
from .remote_peer import RemotePeerData, RemotePeerProducer
from .socket import Socket
from .utils import (
    parse_from_proto_rtp_parameters,
    parse_ice_parameters,
    parse_router_rtp_capabilities,
    parse_sdp_info,
    parse_to_proto_app_data,
    parse_to_proto_dtls,
    parse_to_proto_rtp_parameters,
    parse_to_proto_sctp_capabilities,
    parse_to_proto_sctp_parameters,
    parse_to_sctp_parameters,
)

if TYPE_CHECKING:
    from .room import Room

from pymediasoup import AiortcHandler, Device
from pymediasoup.consumer import Consumer
from pymediasoup.producer import Producer
from pymediasoup.transport import (
    ConnectionState,
    DtlsParameters,
    RtpParameters,
    SctpStreamParameters,
    Transport,
)

logger = base_logger.getChild("LocalPeer")

MAX_DATA_MESSAGE_SIZE = 1 * 1024  # 1kb


class LocalPeerOptions(BaseModel):
    peer_id: str = Field(description="Peer Id of the Local Peer")
    session_id: str = Field(description="Session Id of the Local Peer")
    auto_consume: bool = Field(
        default=True, description="Consume Media of Remote Peers Automatically"
    )
    permissions: Permissions
    metadata: Optional[str] = None
    volatile_messaging: bool = Field(
        default=True, description="Enable Volatile Messaging"
    )

    @validator("permissions", pre=True)
    def validate_permissions(cls, v):
        if not isinstance(v, Permissions):
            raise ValueError("Must be a Permissions instance")
        return v

    class Config:
        arbitrary_types_allowed = True


class LocalPeer(EnhancedEventEmitter):
    def __init__(self, options: LocalPeerOptions, socket: Socket):
        super(LocalPeer, self).__init__()

        logger.info("[constructor] LocalPeer, initializing")

        self.__volatile_messaging = options.volatile_messaging
        # Socket Instance, to be used for communication
        self.__socket = socket

        # PeerId is the unique identifier of the Peer which is the Local User.
        self.peer_id = options.peer_id

        # Room at which the Local Peer is connected
        self.__room: Optional["Room"] = None

        # Consume Media of Remote Peers Automatically
        self.__auto_consume = options.auto_consume

        # Mediasoup Device with Aiortc Handler as the handler factory
        self.__device: Optional[Device] = None

        self._ice_restart_debounce: IceRestartDebounce = IceRestartDebounce(
            send=False, recv=False
        )

        # WebRTC Transport which is used for sending the Media ( Audio, Video, Data )
        self.__send_transport: Optional[Transport] = None

        # Mapping of Labels to Producer Ids
        # Args: [ Label -> ProducerId ]
        self.__labels_to_producer_id: Dict[str, str] = {}

        # WebRTC Transport which is used for receiving the Media ( Audio, Video, Data )
        self.__recv_transport: Optional[Transport] = None

        # Mapping of Producer Ids to Consumer Ids
        self.__remote_producer_id_to_consumer_id: Dict[str, str] = {}

        # Turn Server Information
        self.__turn_servers: List[RTCIceServer] = []

        # Permissions for the Local Peer
        self.permissions = options.permissions

        # Role of the Local Peer as peer the token which was used for socket connection.
        self.role: Optional[str] = options.permissions.role

        # Metadata for the Local Peer which can be used to store additional information
        self.metadata: Optional[str] = options.metadata

        # Variable to store if local peer joined the room
        self.__joined: asyncio.Future = asyncio.Future()

        # Async Operation Manager to manage the async operations
        self.__async_manager = AsyncOperationManager()

        # Subscribe to the Observer Events
        self.__handle_socket_events()

    def __str__(self):
        return f"LocalPeer: {self.peer_id}"

    def __repr__(self):
        return f"LocalPeer: {self.peer_id}"

    def _set_room(self, room: "Room"):
        """
        Set the Room for the Local Peer
        """
        if self.__room is not None:
            raise Exception(
                f"Room already set for Local Peer: {self.peer_id}, Close the Room before setting a new Room"
            )

        self.__room = room

        async def on_room_joined():
            logger.debug(
                f"Local Peer: {self.peer_id} On Joined Room triggered",
                self.__volatile_messaging,
            )
            if self.__volatile_messaging:
                try:
                    await self.__activate_volatile_messaging()
                except Exception as e:
                    logger.error(
                        f"Error while activating volatile messaging for Local Peer: {self.peer_id}, Error: {e}"
                    )

        self.room.on(RoomEvents.RoomJoined, on_room_joined)

    @property
    def room(self) -> "Room":
        """
        Get the Room of the Local Peer
        """
        if self.__room is None:
            raise Exception(f"Room not set for Local Peer: {self.peer_id}")

        return self.__room

    @property
    def remote_peers(self) -> Dict[str, RemotePeer]:
        """
        Get the RemotePeers of the Room
        """
        if self.__room is None:
            raise Exception(f"Room not set for Local Peer: {self.peer_id}")

        remote_peers = self.__room.remote_peers

        logger.info(f"Remote Peers: {remote_peers}")

        return self.__room.remote_peers

    @property
    async def joined(
        self,
    ):
        return await self.__joined

    @property
    def device(self) -> Device:
        """
        Handler for the Device of the Local Peer, which is used to create the Transports and Producers
        """
        if self.__device is None:
            raise Exception(f"Device not created for Local Peer: {self.peer_id}")
        return self.__device

    @property
    def socket(self) -> Socket:
        """
        Get the Socket of the Local Peer, which is used for communication between the Local Peer and the Huddle01 RTC Engine
        """
        if self.__socket is None:
            raise Exception(f"Socket not created for Local Peer: {self.peer_id}")

        return self.__socket

    @property
    def send_transport(self) -> Transport:
        """ "
        Get the Send Transport of the Local Peer, which is used to send the Media ( Audio, Video, Data )
        """
        if self.__send_transport is None:
            raise Exception(
                f"Send Transport not created for Local Peer: {self.peer_id}"
            )

        return self.__send_transport

    @property
    def recv_transport(self) -> Transport:
        if self.__recv_transport is None:
            raise Exception(
                f"Recv Transport not created for Local Peer: {self.peer_id}"
            )

        return self.__recv_transport

    @property
    def producers(self) -> Dict[str, Producer]:
        """
        Get the Producers of the Local Peer, which handles the track which is used to send the Media ( Audio, Video, Data )
        """
        if self.__send_transport is None:
            return {}

        return self.send_transport._producers

    @property
    def consumers(self) -> Dict[str, Consumer]:
        """
        Get the Consumers of the Local Peer, which handles the track to receive the Media ( Audio, Video, Data )
        """
        if self.__recv_transport is None:
            return {}

        return self.recv_transport._consumers

    @property
    def labels_to_producer_ids(self) -> Dict[str, str]:
        """
        Get the Mapping of Labels to Producer Ids
        """
        return self.__labels_to_producer_id

    @property
    def turn_servers(self) -> List[RTCIceServer]:
        """
        Get the Turn Servers Information
        """
        return self.__turn_servers

    @property
    def auto_consume(self) -> bool:
        """
        Consume Media of Remote Peers Automatically
        """
        return self.__auto_consume

    def get_producer(
        self, producer_id: Optional[str] = None, label: Optional[str] = None
    ) -> Union[Producer, None]:
        """
        Get the Producer of the Local Peer, which handles the track to send the Media ( Audio, Video, Data )

        - If `producer_id` is provided, then it will return the Producer with the given `producer_id`.
        - If `label` is provided, then it will return the Producer with the given `label`.
        - If both `producer_id` and `label` are provided, then it will return the Producer with the given `producer_id` and `label`.

        Args:
            producer_id: str: Producer Id of the Producer
            label: str: Label of the Producer

        Returns:
            Producer: Producer of the Local Peer

        Raises:
            Exception: If Producer Id or Label are not provided

        """
        if self.__send_transport is None:
            return None

        if producer_id is None or label is None:
            raise Exception("Producer Id or Label is required to get the Producer")

        if label:
            label_producer_id = self.__labels_to_producer_id.get(label)

            if label_producer_id is None:
                return None

            if producer_id and producer_id != label_producer_id:
                return None

            return self.__send_transport._producers.get(producer_id)

        return self.__send_transport._producers.get(producer_id)

    def get_consumer(
        self,
        consumer_id: Optional[str] = None,
        label: Optional[str] = None,
        peer_id: Optional[str] = None,
    ) -> Union[Consumer, None]:
        """
        Get the Consumer of the Remote Peer, which handles the track to recieve the Media ( Audio, Video, Data )

        - If `consumer_id` is provided, then it will return the Consumer with the given `consumer_id`.
        - If `label` and 'peer_id' is provided, then it will return the Consumer from 'peer_id' with the given `label`.

        Args:
            consumer_id: str: Consumer Id of the Consumer
            label: str: Label of the Consumer

        Returns:
            Consumer: Consumer of the Local Peer

        Raises:
            Exception: If Consumer Id or (Label and Peer ID) are not provided
        """
        if self.__recv_transport is None:
            return None

        if consumer_id is None or (label is None and peer_id is None):
            raise Exception("Consumer Id or Label is required to get the Consumer")

        if consumer_id:
            return self.__recv_transport._consumers.get(consumer_id)

        if label and peer_id:
            remote_peer = self.remote_peers.get(peer_id)

            if remote_peer is None:
                return None

            producer = remote_peer.label_to_producers.get(label)

            if producer is None:
                return None

            consumer_id = self.__remote_producer_id_to_consumer_id.get(
                producer.producer_id
            )

            if consumer_id is None:
                return None
            return self.__recv_transport._consumers.get(consumer_id)

        return None

    async def close_consumer(self, label: str, peer_id: str) -> bool:
        if self.__recv_transport is None:
            return False

        consumer: Optional[Consumer] = None

        remote_peer = self.remote_peers.get(peer_id)

        if remote_peer is None:
            return False

        producer = remote_peer.label_to_producers.get(label)

        if producer is None:
            return False

        consumer_id = self.__remote_producer_id_to_consumer_id.get(producer.producer_id)

        if consumer_id is None:
            return False
        consumer = self.__recv_transport._consumers.get(consumer_id)

        if consumer is None:
            return False

        remote_peer.remove_producer(label)
        self.__remote_producer_id_to_consumer_id.pop(producer.producer_id)
        await consumer.close()

        return True

    async def send_volatile_data(self, payload: str, label: str) -> bool:
        """
        Send Volatile Data to the Remote Peer
        """
        try:
            if payload.__len__() > 1024:  # 1KB
                logger.error("Payload size is too large")
                return False

            if self.room.bot:
                peer_id = self.peer_id
                data = VolatileDataMessage(
                    from_peer_id=peer_id, to="*", payload=payload, label=label
                )
                return await self.room.bot.send_data(data)

            return False
        except Exception as e:
            logger.error(f"Error sending volatile data: {e}")
            return False

    async def produce(self, options: ProduceOptions) -> Producer:
        """
        Produce the Media ( Audio, VidCARV Premium: This subscription model requires you to pay for your node operations, allowing you to retain your full rewards. Additionally, you can enable users to delegate to your node, offering flexibility in setting the commission rate you wish to receive from license holders who delegate to you.
        """
        operation_id = f"produce_{options.label}"

        try:
            task = self.__async_manager.get_operation(operation_id)

            if task:
                logger.info(
                    f"Pending Produce Operation found for label {options.label}, waiting for it to complete, this might be due to memory leak in your code."
                )

                await self.__async_manager.wait_for_operation(operation_id=operation_id)

                producer = self.get_producer(label=options.label)

                if producer is None:
                    raise Exception(
                        f"Producer not found for given label: {options.label}"
                    )

                return producer

            if not self.device._canProduceByKind.get(options.track.kind):
                raise Exception(
                    f"Cannot produce {options.track.kind} for Local Peer: {self.peer_id}"
                )

            transport = await self.__create_transport("send")

            self.send_transport._producers

            self.__async_manager.create_operation(operation_id=operation_id)

            logger.info(f"Producing Media for Local Peer: {self.peer_id}")

            producer = await transport.produce(
                track=options.track, appData={"label": options.label}
            )

            self.__labels_to_producer_id.update({options.label: producer.id})

            logger.info(f"Produce() | Result: {producer.id}")

            self.emit(LocalPeerEvents.ProduceSuccess, producer)

            return producer

        except Exception as e:
            logger.error(f"Error while producing Media: {e}")

            self.__async_manager.resolve_operation(operation_id=operation_id, error=e)
            raise

    async def consume(self, options: ConsumeOptions) -> Consumer:
        """
        Consume the Media ( Audio, Video, Data ) from the Room
        """
        logger.info(f"Consume Media Request for Local Peer: {self.peer_id}, {options}")

        operation_id = self.__async_manager.operation_id(
            OperationsType.CONSUME, options.producer_id
        )

        try:
            remote_peer = self.remote_peers.get(options.producer_peer_id)

            if remote_peer is None:
                raise Exception(
                    f"Remote Peer not found with PeerId: {options.producer_peer_id}"
                )

            consumer_id = self.__remote_producer_id_to_consumer_id.get(
                options.producer_id
            )

            if consumer_id and self.__recv_transport:
                consumer = self.__recv_transport._consumers.get(consumer_id)

                if consumer is None:
                    raise Exception(
                        f"Consumer not found for given consumer_id: {consumer_id}, This should never happen"
                    )

                return consumer

            pending_task = self.__async_manager.get_operation(operation_id)

            if pending_task:
                await self.__async_manager.wait_for_operation(operation_id=operation_id)

                consumer_id = self.__remote_producer_id_to_consumer_id.get(
                    options.producer_id
                )

                if consumer_id is None:
                    raise Exception(
                        f"Consumer not found for given producer_id: {options.producer_id}"
                    )

                consumer = self.recv_transport._consumers.get(consumer_id)

                if consumer is None:
                    raise Exception(
                        f"Consumer not found for given consumer_id: {consumer_id}"
                    )

                return consumer

            self.__async_manager.create_operation(
                operation_id=operation_id,
            )

            logger.info("Creating Recv Transpoort for Remote Peer")

            await self.__create_transport("recv")

            logger.info(f"Consuming Media for Local Peer: {self.peer_id}")

            await self.socket.request(
                SocketRequestEvents.Consume,
                Request.Consume(
                    producerPeerId=options.producer_peer_id,
                    producerId=options.producer_id,
                    appData={},
                ),
            )

            label = await self.__async_manager.wait_for_operation(
                operation_id=operation_id
            )

            if label is None or label is str:
                raise Exception(
                    "Label not found after consumer operation resolved, This should never happen"
                )

            consumer_id = self.__remote_producer_id_to_consumer_id.get(
                options.producer_id
            )

            if consumer_id is None:
                raise Exception(
                    f"Consumer not found for given producer_id: {options.producer_id}, This should never happen"
                )

            consumer = self.recv_transport._consumers.get(consumer_id)

            if consumer is None:
                raise Exception(
                    f"Consumer not found for given consumer_id: {consumer_id}, This should never happen"
                )

            remote_peer._update_producer(
                label=label, paused=consumer.paused, consuming=True
            )

            self.emit(LocalPeerEvents.NewConsumer, consumer)
            self.room.emit(RoomEvents.NewConsumerAdded, RoomEventsData.NewConsumerAdded(
                consumer=consumer,
                consumer_id=consumer.id,
                kind=consumer.kind,
                label=label,
            ))

            return consumer

        except Exception as e:
            logger.error(f"Error while consuming Media: {e}")

            self.__async_manager.resolve_operation(operation_id=operation_id, error=e)

            self.emit(LocalPeerEvents.ConsumeError, e)

            raise

    def send_data(self, data: SendDataOptions) -> SendDataResult:
        """
        Send Data to the Room
        """
        try:
            if len(data.payload) > MAX_DATA_MESSAGE_SIZE:
                logger.error("❌ Data message exceeds 1kb in size")
                return SendDataResult(
                    success=False, error="Data message exceeds 1kb in size"
                )

            parsed_to = ["*"] if data.to == "*" else data.to

            self.socket.emit(
                SocketRequestEvents.SendData,
                {"to": parsed_to, "payload": data.payload, "label": data.label},
            )

            return SendDataResult(success=True, error=None)

        except Exception as error:
            logger.error("❌ Error Sending Data")
            logger.error(error)
            return SendDataResult(success=False, error="Socket Message Failed")

    async def __activate_volatile_messaging(self) -> bool:
        """
        Activate the Volatile Messaging
        """
        try:
            logger.info("Activating Volatile Messaging")

            task = self.__async_manager.get_operation("volatile_messaging")

            if task:
                logger.info("Pending Enable Volataile Messaging Task Found")

                await self.__async_manager.wait_for_operation("volatile_messaging")

                return True

            if self.room.bot is not None:
                botDataConsumer = self.room.bot.bot_data_consumer

                if botDataConsumer:
                    return True

            async def task_fn():
                if not self.__recv_transport:
                    await self.__create_transport("recv")

                if not self.__send_transport:
                    await self.__create_transport("send")

                await self.__create_data_producer(
                    DataProducerOptions(
                        label="bot",
                        maxRetransmits=3,
                        ordered=False,
                        maxPacketLifeTime=None,
                    )
                )

                self.__async_manager.resolve_operation("volatile_messaging")

            task = self.__async_manager.create_operation("volatile_messaging")

            await task_fn()

            await task.future

            return True

        except Exception as e:
            logger.error(f"Error while activating Volatile Messaging: {e}")
            return False

    async def __create_data_producer(self, data_producer_options: DataProducerOptions):
        try:
            producerId = self.labels_to_producer_ids.get(
                f"data-{data_producer_options.label}"
            )

            if producerId is not None:
                dataProducer = self.send_transport._dataProducers.get(producerId)
                if dataProducer is not None:
                    return dataProducer

            logger.info(f"Creating Data Producer for Label: {data_producer_options}")
            operation_id = f"produce_data_{data_producer_options.label}"

            self.__async_manager.create_operation(operation_id=operation_id)

            dataProducer = await self.send_transport.produceData(
                label=data_producer_options.label,
                maxRetransmits=data_producer_options.maxRetransmits,
                ordered=data_producer_options.ordered,
                protocol="udp",
            )

            logger.info(
                f"Data Producer Created for Label: {data_producer_options.label}"
            )

            self.labels_to_producer_ids[f"data-{data_producer_options.label}"] = (
                dataProducer.id
            )

            logger.info(
                f"set label for data producer: data-{data_producer_options.label} with id: {dataProducer.id}"
            )
            # print all key values of labels_to_producer_ids
            for key, value in self.labels_to_producer_ids.items():
                print(key, value)

            return dataProducer
        except Exception as e:
            logger.error(f"Error while creating Data Producer: {e}")

    async def __create_data_consumer(self, data_consumer_options: DataConsumerOptions):
        try:
            dataConsumer = self.recv_transport._dataConsumers.get(
                data_consumer_options.label
            )

            if dataConsumer is not None:
                return dataConsumer

            dataConsumer = await self.recv_transport.consumeData(
                id=data_consumer_options.id,
                dataProducerId=data_consumer_options.dataProducerId,
                label=data_consumer_options.label,
                sctpStreamParameters=data_consumer_options.sctpStreamParameters,
                protocol=data_consumer_options.protocol,
                appData={},
            )

            return dataConsumer
        except Exception as e:
            logger.error(f"Error while creating Data Consumer: {e}")
            raise

    def __handle_socket_events(self):
        """
        Handle the Observer Events, which are emitted from the Observer
        and then handled accordingly
        """
        if self.__socket is None:
            raise ValueError(
                "Socket is not created, make sure to create the Socket before subscribing to the events"
            )

        @self.socket.on("reconnected")
        async def on_reconnected():
            try:
                logger.info("On recconnected")
                if not self.joined:
                    logger.info(f"Local Peer: {self.peer_id} Reconnecting")

                    if self.room.room_id and self.room.state == "connecting":
                        await self.room.connect()
                    return

                logger.info("Local Peer Reconnected, Syncing Meeting States")

                local_producer_ids: List[str] = []
                if self.send_transport is not None:
                    for producerIds in self.send_transport._producers.keys():
                        local_producer_ids.append(producerIds)

                await self.socket.request(
                    SocketRequestEvents.SyncMeetingState,
                    Request.SyncMeetingState(localProducerIds=local_producer_ids),
                )

                if self.send_transport:
                    await self.socket.request(
                        SocketRequestEvents.RestartTransportIce,
                        Request.RestartTransportIce(
                            transportId=self.send_transport.id, transportType="send"
                        ),
                    )
                if self.recv_transport:
                    await self.socket.request(
                        SocketRequestEvents.RestartTransportIce,
                        Request.RestartTransportIce(
                            transportId=self.recv_transport.id, transportType="recv"
                        ),
                    )

            except Exception as e:
                logger.error(f"Error while reconnecting: {e}")

        @self.socket.on(SocketResponseEvents.ConnectRoomResponse)
        async def on_connect_room_response(data: Response.ConnectRoomResponse):
            try:
                logger.info("Connect Room Response Recieved, Creating Device")

                # Create a Device for the Local Peer
                self.__device = Device(
                    handlerFactory=AiortcHandler.createFactory(),
                )

                parsed_router_rtp_capabilties = parse_router_rtp_capabilities(
                    data.routerRTPCapabilities
                )

                await self.__device.load(
                    routerRtpCapabilities=parsed_router_rtp_capabilties
                )

                if data.turnServers:
                    for server in data.turnServers:
                        turn_server = RTCIceServer(
                            urls=server.urls,
                            username=server.username,
                            credential=server.credential,
                        )

                        self.__turn_servers.append(turn_server)

                    logger.info(f"Setting Turn Servers done: {self.__turn_servers}")

                remote_producers = self.room._update_room_info(data.roomInfo)

                self.__joined.set_result(True)

                asyncio.create_task(
                    self.consume_remote_producers(remote_producers),
                    name="consume_remote_producers",
                )

                logger.info(f"Local Peer Joined Room: {self.peer_id}")

            except Exception as e:
                logger.error(f"Error while creating Device: {e}")

                self.__joined.set_exception(e)

        @self.socket.on(SocketResponseEvents.CreateTransportOnClient)
        async def on_create_transport(data: Response.CreateTransportOnClient):
            operation_id = f"create_transport_{data.transportType}"

            try:
                task = self.__async_manager.get_operation(operation_id)

                if task is None:
                    raise Exception(
                        f"Operation with id {operation_id} not found, This should never happen"
                    )

                logger.info("Create Transport Event Recieved, Creating Transport")

                parsed_sdp_info = parse_sdp_info(data.transportSDPInfo)

                setattr(parse_sdp_info, "iceServers", self.__turn_servers)

                def create_send_transport() -> Transport:
                    ice_candidates = cast(
                        List[IceCandidate], parsed_sdp_info.iceCandidates
                    )

                    return self.device.createSendTransport(
                        id=data.transportSDPInfo.id,
                        iceCandidates=ice_candidates,
                        dtlsParameters=parsed_sdp_info.dtlsParameters,
                        iceParameters=parsed_sdp_info.iceParameters,
                        iceServers=self.__turn_servers,
                        sctpParameters=parsed_sdp_info.sctpParameters,
                    )

                def create_recv_transport() -> Transport:
                    return self.device.createRecvTransport(
                        id=data.transportSDPInfo.id,
                        iceCandidates=parsed_sdp_info.iceCandidates,
                        dtlsParameters=parsed_sdp_info.dtlsParameters,
                        iceParameters=parsed_sdp_info.iceParameters,
                        iceServers=self.__turn_servers,
                        sctpParameters=parsed_sdp_info.sctpParameters,
                    )

                transport: Transport = (
                    create_send_transport()
                    if data.transportType == "send"
                    else create_recv_transport()
                )

                @transport.on("connect")
                async def on_connect(dtlsParameters: DtlsParameters):
                    try:
                        logger.info(f"Transport Connected: {dtlsParameters}")

                        parsed_dtls_parameters = parse_to_proto_dtls(dtlsParameters)

                        operation_id = self.__async_manager.operation_id(
                            OperationsType.CONNECT_TRANSPORT, data.transportType
                        )

                        task = self.__async_manager.create_operation(operation_id)

                        await self.socket.request(
                            SocketRequestEvents.ConnectTransport,
                            Request.ConnectTransport(
                                dtlsParameters=parsed_dtls_parameters,
                                transportType=data.transportType,
                            ),
                        )

                        await task.future

                    except Exception as e:
                        logger.error(f"Error while connecting Transport: {e}")

                        raise

                @transport.on("produce")
                async def on_produce(
                    kind: str, rtpParameters: RtpParameters, appData: Dict[str, str]
                ):
                    operation_id = f"produce_{appData.get('label')}"

                    try:
                        label = appData.get("label")

                        logger.info(f"Produce Event Recieved: {kind}, Label: {label}")

                        task = self.__async_manager.get_operation(operation_id)

                        if task is None:
                            raise Exception(
                                f"Pending Produce Operation found for label {label}, This should never happen"
                            )

                        if label is None:
                            raise Exception("Label not found in appData")

                        parsed_rtp_parameters = parse_to_proto_rtp_parameters(
                            rtpParameters
                        )

                        parsed_app_data = parse_to_proto_app_data(appData)

                        await self.socket.request(
                            SocketRequestEvents.Produce,
                            Request.Produce(
                                kind=kind,
                                label=label,
                                rtpParameters=parsed_rtp_parameters,
                                appData=parsed_app_data,
                                paused=False,
                            ),
                        )

                        if task is None:
                            raise Exception(
                                f"Operation with id {operation_id} not found, This should never happen"
                            )

                        await task.future

                        return task.future.result()

                    except Exception as e:
                        logger.error(f"Error while producing Media: {e}")

                        self.__async_manager.resolve_operation(
                            operation_id=operation_id, error=e
                        )

                @transport.on("connectionstatechange")
                async def on_connection_state_change(state: str):
                    logger.info(f"Transport Connection State Changed: {state}")
                    pass

                @transport.on("producedata")
                async def on_produce_data(
                    label: str,
                    protocol: str,
                    appData: Dict[str, str],
                    sctpStreamParameters: SctpStreamParameters,
                ):
                    if data.transportType == "recv":
                        return
                    try:
                        operation_id = f"produce_data_{label}"

                        task = self.__async_manager.get_operation(operation_id)

                        if task is None:
                            raise Exception(
                                f"Pending Produce Operation found for label {label}, This should never happen"
                            )

                        if label is None:
                            raise Exception("Label not found in appData")

                        logger.info(f"sctpStreamParameters: {sctpStreamParameters}")

                        protoSctpParams = parse_to_proto_sctp_parameters(
                            sctpStreamParameters
                        )

                        await self.socket.request(
                            SocketRequestEvents.ProduceData,
                            Request.ProduceData(
                                transportId=transport.id,
                                sctpStreamParameters=protoSctpParams,
                                label=label,
                                protocol=protocol,
                                appData=appData,
                            ),
                        )
                        if task is None:
                            raise Exception(
                                f"Operation with id {operation_id} not found, This should never happen"
                            )

                        await task.future

                        logger.info(f"future data received {task.future.result()}")

                        return task.future.result()

                    except Exception as e:
                        logger.error(f"Error while producing Data: {e}")

                if data.transportType == "send":
                    self.__send_transport = transport

                elif data.transportType == "recv":
                    self.__recv_transport = transport

                logger.info(f"Transport Created for Local Peer: {self.peer_id}")

                self.__async_manager.resolve_operation(
                    operation_id=operation_id, result=True
                )

            except Exception as e:
                logger.error(f"Error while creating Transport: {e}")

                self.__async_manager.resolve_operation(
                    operation_id=operation_id, error=e
                )

        @self.socket.on(SocketResponseEvents.ConnectTransportResponse)
        async def on_connect_transport(data: Response.ConnectTransportResponse):
            try:
                logger.info("Connect Transport Event Recieved, Connecting Transport")

                operation_id = self.__async_manager.operation_id(
                    OperationsType.CONNECT_TRANSPORT, data.transportType
                )

                task = self.__async_manager.get_operation(operation_id)

                if task is None:
                    raise Exception(
                        f"Operation with id {operation_id} not found, This should never happen"
                    )

                self.__async_manager.resolve_operation(operation_id, result=True)

                logger.info(f"Transport Connected for Local Peer: {self.peer_id}")

            except Exception as e:
                logger.error(f"Error while connecting Transport: {e}")
                raise

        @self.socket.on(SocketResponseEvents.ProduceResponse)
        async def on_produce_response(data: Response.ProduceResponse):
            try:
                # Wait for the Local Peer to join the Room
                await self.__joined

                logger.info("Produce Response Recieved, Producing Media")

                if data.peerId == self.peer_id:
                    self.__async_manager.resolve_operation(
                        operation_id=f"produce_{data.label}", result=data.producerId
                    )

                else:
                    remote_peer = self.remote_peers.get(data.peerId)

                    if remote_peer is None:
                        raise ValueError(
                            f"Remote Peer not found with PeerId: {data.peerId}"
                        )

                    producer = RemotePeerProducer(
                        consuming=False,
                        label=data.label,
                        paused=True,
                        peer_id=data.peerId,
                        producer_id=data.producerId,
                    )

                    remote_peer._add_producer(producer)

                    if self.__auto_consume:
                        try:
                            await self.consume(
                                ConsumeOptions(
                                    producer_peer_id=data.peerId,
                                    producer_id=data.producerId,
                                )
                            )
                        except Exception as e:
                            logger.error(f"Error while consuming Media: {e}")

            except Exception as e:
                logger.error(f"Error while producing Media: {e}")

        @self.socket.on(SocketResponseEvents.ConsumeResponse)
        async def on_consume_response(data: Response.ConsumeResponse):
            operation_id = self.__async_manager.operation_id(
                OperationsType.CONSUME, data.producerId
            )

            try:
                logger.info("Consume Response Recieved, Consuming Media")

                task = self.__async_manager.get_operation(operation_id)

                if task is None:
                    raise Exception(
                        f"Operation with id {operation_id} not found, This should never happen"
                    )

                remote_peer = self.remote_peers.get(data.producerPeerId)

                if remote_peer is None:
                    raise ValueError(
                        f"Remote Peer not found with PeerId: {data.producerPeerId}"
                    )

                remote_producer = remote_peer.get_producer(label=data.label)

                if remote_producer is None:
                    raise ValueError(
                        f"Remote Peer with PeerId: {data.producerPeerId} is not producing the label: {data.label}"
                    )

                parsed_rtp_parameters = parse_from_proto_rtp_parameters(
                    data.rtpParameters
                )

                kind: MediaKind = "audio" if data.kind == "audio" else "video"

                consumer = await self.recv_transport.consume(
                    id=data.consumerId,
                    producerId=data.producerId,
                    kind=kind,
                    rtpParameters=parsed_rtp_parameters,
                    appData={
                        "peerId": data.producerPeerId,
                        "label": data.label,
                        "producerPaused": data.producerPaused,
                    },
                )

                if remote_producer.paused:
                    consumer._paused = True

                await self.socket.request(
                    SocketRequestEvents.ResumeConsumer,
                    Request.ResumeConsumer(
                        consumerId=data.consumerId, producerPeerId=data.producerPeerId
                    ),
                )

                self.__remote_producer_id_to_consumer_id.update(
                    {data.producerId: consumer.id}
                )

                self.__async_manager.resolve_operation(
                    operation_id=operation_id,
                    result=data.label,
                )

                logger.info(f"Media Consumed for Local Peer: {self.peer_id}")

            except Exception as e:
                logger.error(f"Error while consuming Media: {e}")

                self.__async_manager.resolve_operation(
                    operation_id=operation_id,
                    error=e,
                )

        @self.socket.on(SocketResponseEvents.RestartTransportIceResponse)
        async def on_restart_transport_ice(data: Response.RestartTransportIceResponse):
            try:
                transport = (
                    self.__send_transport
                    if data.transportType == "send"
                    else self.__recv_transport
                )

                ice_parameters = parse_ice_parameters(data.iceParameters)

                if transport:
                    await transport.restartIce(ice_parameters)
                    logger.info(f"ICE Restarted for Local Peer: {self.peer_id}")
                    self.emit(LocalPeerEvents.IceTransportRestarted, data.transportType)

            except Exception as e:
                logger.error(f"Error while restarting Transport ICE: {e}")
                raise

        @self.socket.on(SocketResponseEvents.ConsumeDataResponse)
        async def on_consume_data_response(data: Response.ConsumeDataResponse):
            try:
                logger.info("Consume Data Response Recieved, Producing Data")

                self.__async_manager.resolve_operation(
                    operation_id=f"produce_data_{data.label}",
                    result=data.dataProducerId,
                )

                if data.label == "bot":
                    producerId = self.labels_to_producer_ids.get(f"data-{data.label}")

                    if producerId is None:
                        return

                    dataProducer = self.send_transport._dataProducers.get(producerId)

                    sctpStreamParameters = parse_to_sctp_parameters(
                        data.sctpStreamParameters
                    )

                    dataConsumer = await self.__create_data_consumer(
                        DataConsumerOptions(
                            id=data.id,
                            dataProducerId=data.dataProducerId,
                            peerId=data.peerId,
                            label=data.label,
                            protocol=data.protocol,
                            sctpStreamParameters=sctpStreamParameters,
                            appData={},
                        )
                    )

                    logger.info(f"Bot Data Consumer Created {dataConsumer}")
                    self.room.bot = Bot(
                        options=BotOptions(
                            dataConsumer=dataConsumer, dataProducer=dataProducer
                        )
                    )

                    self.__async_manager.resolve_operation("volatile_messaging")

            except Exception as e:
                logger.error(f"Error while producing Data: {e}")

        @self.socket.on(SocketResponseEvents.ProduceDataResponse)
        async def on_produce_data_response(data: Response.ProduceDataResponse):
            try:
                logger.info("Produce Data Response Recieved, Producing Data")

                self.__async_manager.resolve_operation(
                    operation_id=f"produce_data_{data.label}",
                    result=data.dataProducerId,
                )

                task = self.__async_manager.get_operation("volatile_messaging")

                if task is not None:
                    await self.__async_manager.wait_for_operation("volatile_messaging")

                if data.label == "bot":
                    producerId = self.labels_to_producer_ids.get(f"data-{data.label}")

                    if producerId is None:
                        logger.error("ProducerId not found for Bot")
                        return

                    dataProducer = self.send_transport._dataProducers.get(producerId)

                    logger.info(f"Data Producer Created {dataProducer}")

                    sctpStreamParameters = parse_to_sctp_parameters(
                        data.sctpStreamParameters
                    )

                    dataConsumer = await self.__create_data_consumer(
                        DataConsumerOptions(
                            id=data.id,
                            dataProducerId=data.dataProducerId,
                            peerId=data.peerId,
                            label=data.label,
                            protocol=data.protocol,
                            sctpStreamParameters=sctpStreamParameters,
                            appData={},
                        )
                    )

                    logger.info(f"Bot Data Consumer Created {dataConsumer}")
                    self.room.bot = Bot(
                        options=BotOptions(
                            dataConsumer=dataConsumer, dataProducer=dataProducer
                        )
                    )

                    self.__async_manager.resolve_operation("volatile_messaging")

            except Exception as e:
                logger.error(f"Error while producing Data: {e}")

        @self.socket.on(SocketResponseEvents.CloseProducerSuccess)
        async def on_close_producer_success(data: Response.CloseProducerSuccess):
            try:
                logger.info("Close Producer Success Event Recieved, Closing Producer")

                if self.peer_id == data.peerId:
                    return

                await self.close_consumer(peer_id=data.peerId, label=data.label)
            except Exception as e:
                logger.error(f"Error while closing Producer: {e}")

        @self.socket.on(SocketResponseEvents.SyncMeetingStateResponse)
        async def on_sync_meeting_state(data: Response.SyncMeetingStateResponse):
            try:
                logger.info("✅ Client recovered after reconnecting", data)

                latest_peers = data.roomInfo.peers
                latest_peers_set = set(
                    latest_peer.peerId for latest_peer in latest_peers
                )

                for peer_id, peer in list(self.remote_peers.items()):
                    if peer_id not in latest_peers_set:
                        for label in peer.labels():
                            try:
                                await self.close_consumer(peer_id=peer_id, label=label)
                            except Exception:
                                logger.error("Failed to close consumer in SyncMeeting")

                        peer.close()
                        del self.remote_peers[peer_id]

                        self.room.emit(
                            "peer-left",
                            {
                                "peerId": peer_id,
                                "metadata": peer.metadata,
                                "role": peer.role,
                            },
                        )
                        continue

                    # Handle closing of already closed streams of remote peer
                    latest_peer_info = next(
                        (p for p in latest_peers if p.peerId == peer_id), None
                    )
                    if not latest_peer_info:
                        continue

                    new_producer_set = set(p.label for p in latest_peer_info.producers)

                    for label in peer.labels():
                        if label not in new_producer_set:
                            await self.close_consumer(peer_id=peer_id, label=label)

                    current_producer_set = set(peer.producer_ids())

                    for producer in latest_peer_info.producers:
                        if producer.id not in current_producer_set:
                            remote_producer = RemotePeerProducer(
                                consuming=False,
                                label=producer.label,
                                paused=True,
                                peer_id=peer_id,
                                producer_id=producer.id,
                            )

                            peer._add_producer(remote_producer)
                            if self.__auto_consume:
                                try:
                                    await self.consume(
                                        ConsumeOptions(
                                            producer_peer_id=peer_id,
                                            producer_id=producer.id,
                                        )
                                    )
                                except Exception as e:
                                    logger.error(
                                        f"Error while consuming Media during SyncMeeting: {e}"
                                    )
                        else:
                            consumer = self.get_consumer(peer_id, producer.label)
                            if producer.paused:
                                if consumer:
                                    consumer.pause()

                                peer.emit(
                                    "stream-paused",
                                    {
                                        "label": producer.label,
                                        "peerId": peer_id,
                                        "producerId": producer.id,
                                    },
                                )

                            elif consumer:
                                consumer.resume()
                                peer.emit(
                                    "stream-playable",
                                    {"consumer": consumer, "label": producer.label},
                                )

                # Handle new peers
                filtered_peers = (
                    p
                    for p in latest_peers
                    if p.peerId not in self.remote_peers and p.peerId != self.peer_id
                )

                for latest_peer in filtered_peers:
                    remote_peer = RemotePeer(
                        RemotePeerData(
                            peer_id=latest_peer.peerId,
                            role=latest_peer.role,
                            metadata=latest_peer.metadata,
                        ),
                    )

                    self.remote_peers[latest_peer.peerId] = remote_peer

                    for producer in latest_peer.producers:
                        remote_producer = RemotePeerProducer(
                            consuming=False,
                            label=producer.label,
                            paused=producer.paused,
                            peer_id=latest_peer.peerId,
                            producer_id=producer.id,
                        )

                        remote_peer._add_producer(remote_producer)

                        if self.__auto_consume:
                            try:
                                await self.consume(
                                    ConsumeOptions(
                                        producer_peer_id=latest_peer.peerId,
                                        producer_id=producer.id,
                                    )
                                )
                            except Exception as e:
                                logger.error(f"Error while consuming Media: {e}")

                    self.room.emit("new-peer-joined", {"peer": remote_peer})

            except Exception as error:
                logger.error("❌ Error Syncing Meeting State, Can't Recover")
                logger.error(error)

    async def __create_transport(
        self, transport_type: Literal["send", "recv"]
    ) -> Transport:
        """
        Create a Transport for the Local Peer, if transport already exists, return the existing transport
        """
        logger.info(f"Creating Transport Type: {transport_type}")

        operation_id = f"create_transport_{transport_type}"

        try:
            if self.__device is None:
                raise Exception(f"Device not created for Local Peer: {self.peer_id}")

            if transport_type == "send" and self.__send_transport:
                return self.__send_transport

            if transport_type == "recv" and self.__recv_transport:
                return self.__recv_transport

            pending_task = self.__async_manager.get_operation(operation_id)

            if pending_task:
                await pending_task.future

                transport = (
                    self.__send_transport
                    if transport_type == "send"
                    else self.__recv_transport
                )

                if transport is None:
                    raise Exception(
                        f"Transport not created for Local Peer: {self.peer_id}"
                    )

                return transport

            sctp_capabilities = self.device.sctpCapabilities

            if sctp_capabilities is not None:
                sctp_capabilities = parse_to_proto_sctp_capabilities(sctp_capabilities)

            create_transport = Request.CreateTransport(
                transportType=transport_type, sctpCapabilities=sctp_capabilities
            )

            logger.info(f"Creating Transport for Local Peer: {self.peer_id}")

            task = self.__async_manager.create_operation(
                operation_id=operation_id,
            )

            await self.socket.request(
                SocketRequestEvents.CreateTransport, create_transport
            )

            logger.info("Waiting for Transport Creation to complete")

            await task.future

            logger.info("Transport Creation Completed")

            transport = (
                self.__send_transport
                if transport_type == "send"
                else self.__recv_transport
            )

            if transport is None:
                raise Exception(f"Transport not created for Local Peer: {self.peer_id}")

            async def __connection_state_change(state: ConnectionState):
                try:
                    logger.debug(
                        f"🔔 {transport.direction} Transport Connection State Changed, state: {state}"
                    )

                    async def handle_connected():
                        logger.debug(f"🔔 {transport.direction} Transport Connected")

                    async def handle_disconnected():
                        debounce = (
                            self._ice_restart_debounce.send
                            if transport.direction == "send"
                            else self._ice_restart_debounce.recv
                        )

                        if debounce:
                            return

                        debounce = True

                        await self.__socket.request(
                            SocketRequestEvents.RestartTransportIce,
                            RestartTransportIce(
                                transportId=transport.id,
                                transportType=transport.direction,
                            ),
                        )

                        await asyncio.sleep(3)

                        debounce = False

                        logger.debug(f"🔔 {transport.direction} Transport Disconnected")

                    async def handle_failed():
                        logger.debug(f"🔔 {transport.direction} Transport Failed")

                    async def handle_connecting():
                        logger.debug(f"🔔 {transport.direction} Transport Connecting")

                    async def handle_closed():
                        logger.debug(f"🔔 {transport.direction} Transport Closed")

                    async def handle_new():
                        logger.debug(f"🔔 {transport.direction} Transport New")

                    # Map each state to its handler function
                    handler: dict[str, Callable[[], Any]] = {
                        "connected": handle_connected,
                        "disconnected": handle_disconnected,
                        "failed": handle_failed,
                        "connecting": handle_connecting,
                        "closed": handle_closed,
                        "new": handle_new,
                    }

                    fn = handler.get(state)

                    if fn is None:
                        raise Exception(f"Handler not found for state: {state}")

                    await fn()

                except Exception as err:
                    logger.error(f"❌ Error in connectionStateChangeHandler: {err}")

            transport.on("connectionstatechange", __connection_state_change)

            return transport

        except Exception as e:
            logger.info("Error Is Here2")
            logger.error(f"Error while creating Transport: {e}")

            self.__async_manager.resolve_operation(operation_id=operation_id, error=e)

            raise e

    async def consume_remote_producers(
        self, remote_producers: List[RemotePeerProducer]
    ):
        """
        Consume the Remote Producer Ids
        """
        try:
            if not self.__auto_consume:
                return

            if not remote_producers:
                return

            tasks = await asyncio.gather(
                *[
                    self.consume(
                        ConsumeOptions(
                            producer_id=producer.producer_id,
                            producer_peer_id=producer.peer_id,
                        )
                    )
                    for producer in remote_producers
                ],
                return_exceptions=False,
            )

            errorTasks = [task for task in tasks if isinstance(task, Exception)]

            if errorTasks:
                logger.error(f"Some Remote Producer Cannot be consumed: {errorTasks}")

        except Exception as e:
            logger.error(f"Error while consuming Remote Producers: {e}")

            raise

    async def __close_remote_peer_consumer(self, peer_id: str, label: str):
        """
        Close the Consumer of the Remote Peer
        """
        try:
            consumer = self.get_consumer(peer_id, label)

            if consumer is None:
                return

            await consumer.close()

            logger.info(f"Consumer Closed for Remote Peer: {peer_id}, Label: {label}")

        except Exception as e:
            logger.error(f"Error while closing Consumer: {e}")

            raise
