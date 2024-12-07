from typing import List, Optional

from aiortc import MediaStreamTrack
from pydantic import BaseModel, Field
from pymediasoup.handlers.aiortc_handler import SctpStreamParameters


class LocalPeerEvents(str):
    ProduceSuccess = "produce_success"
    IceTransportRestarted = "ice_transport_restarted"
    NewConsumer = "new_consumer"
    ConsumeError = "consume_error"


class ProduceOptions(BaseModel):
    label: str = Field(description="Label of the Producer")
    track: MediaStreamTrack

    class Config:
        arbitrary_types_allowed = True


class ConsumeOptions(BaseModel):
    producer_peer_id: str = Field(description="Peer Id of the Producer")
    producer_id: str = Field(description="Id of the Producer")


class SendDataOptions(BaseModel):
    to: List[str] = Field(description="Array of Peer Ids to send data to")
    payload: str = Field(description="Payload to send")
    label: Optional[str] = Field(description="Label of payload")


class DataProducerOptions(BaseModel):
    label: str = Field(description="Label of the Data Producer")
    ordered: Optional[bool]
    maxRetransmits: Optional[int]
    maxPacketLifeTime: Optional[int]

    class Config:
        arbitrary_types_allowed = True


class DataConsumerOptions(BaseModel):
    id: str
    dataProducerId: str
    sctpStreamParameters: SctpStreamParameters
    label: str
    protocol: Optional[str]
    appData: dict
    peerId: str

    class Config:
        arbitrary_types_allowed = True


class IceRestartDebounce(BaseModel):
    send: bool = Field(description="Send Ice Restart")
    recv: bool = Field(description="Receive Ice Restart")


class SendDataResult(BaseModel):
    success: bool
    error: Optional[str]
