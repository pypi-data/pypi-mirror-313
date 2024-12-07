from typing import Dict, List, Optional

from pydantic import BaseModel

from .emitter import EnhancedEventEmitter
from .log import base_logger

logger = base_logger.getChild("RemotePeer")


class RemotePeerProducer(BaseModel):
    # PeerId of the Remote Peer which is producing the Producer
    peer_id: str

    # ProducerId of the Producer
    producer_id: str

    # Label of the Producer
    label: str

    # Producer Paused
    paused: bool = True

    # Consuming the Producer
    consuming: bool = False


class RemotePeerData(BaseModel):
    # PeerId is the unique identifier of the Peer which is the Remote User.
    peer_id: str

    # Metadata of the Peer
    metadata: Optional[str] = None

    # Role of the Peer
    role: Optional[str] = None

    # Remote Peer Producers, Dictionary of [ Label -> ProducerId ]
    label_to_producers: Dict[str, RemotePeerProducer] = {}


class RemotePeer(EnhancedEventEmitter):
    """
    Remote Peer, defines the Remote User connected to the same Room.
    """

    # PeerId is the unique identifier of the Peer which is the Remote User.
    peer_id: str

    # Metadata of the Peer
    metadata: Optional[str]

    # Role of the Peer
    role: Optional[str]

    # Producers of the Remote Peer, Dictionary of Labels to RemotePeerProducer
    label_to_producers: Dict[str, RemotePeerProducer]

    def __init__(self, data: RemotePeerData):
        # PeerId is the unique identifier of the Peer which is the Remote User.
        self.peer_id = data.peer_id

        # Metadata of the Peer
        self.metadata = data.metadata

        # Role of the Peer
        self.role = data.role

        # Producers of the Remote Peer, Dictionary of Labels to ProducerIds
        self.label_to_producers: Dict[str, RemotePeerProducer] = data.label_to_producers

    def __str__(self):
        return f"RemotePeer({self.peer_id})"

    def __repr__(self):
        return f"RemotePeer({self.peer_id})"

    def _update_producer(
        self,
        label: str,
        paused: Optional[bool] = None,
        consuming: Optional[bool] = None,
    ):
        """
        Update the Producer of the Remote Peer
        """
        producer = self.label_to_producers.get(label, None)

        if producer:
            if paused is not None:
                producer.paused = paused
            if consuming is not None:
                producer.consuming = consuming
        else:
            logger.warning(
                f"Producer with Label: {label} not found for Remote Peer: {self.peer_id}"
            )

    def _add_producer(self, producer: RemotePeerProducer):
        """
        Add the Producer to the Remote Peer
        """
        self.label_to_producers.update({producer.label: producer})

    def remove_producer(self, label: str):
        """
        Remove the Producer from the Remote Peer
        """
        self.label_to_producers.pop(label, None)

    def get_producer(
        self, label: Optional[str] = None, producer_id: Optional[str] = None
    ) -> Optional[RemotePeerProducer]:
        """
        Get the Producer of the Remote Peer, which the Local Peer can consume using the function `local_peer.consume`

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

        if label is None and producer_id is None:
            raise ValueError("Producer Id or Label is required to get the Producer")

        if label:
            producer = self.label_to_producers.get(label, None)

            if producer_id and producer and producer.producer_id != producer_id:
                return None

            return producer

        if producer_id:
            for producer in self.label_to_producers.values():
                if producer.producer_id == producer_id:
                    return producer

                return None

        return None

    def is_producing_label(self, label: str) -> bool:
        """
        Check if the Remote Peer is producing the given Label
        """
        return label in self.label_to_producers

    def labels(self) -> List[str]:
        """
        Get the Labels of the Remote Peer
        """
        return list(self.label_to_producers.keys())

    def producer_ids(self) -> List[str]:
        """
        Get the ProducerIds of the Remote Peer
        """
        return list(p.producer_id for p in self.label_to_producers.values())

    def close(self):
        """
        Close the Remote Peer
        """
        logger.info(f"Closing Remote Peer with PeerId: {self.peer_id}")
