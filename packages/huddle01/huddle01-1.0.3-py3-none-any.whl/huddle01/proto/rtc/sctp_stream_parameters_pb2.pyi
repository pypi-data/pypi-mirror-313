from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoSctpStreamParameters(_message.Message):
    __slots__ = ("streamId", "ordered", "maxPacketLifeTime", "maxRetransmits")
    STREAMID_FIELD_NUMBER: _ClassVar[int]
    ORDERED_FIELD_NUMBER: _ClassVar[int]
    MAXPACKETLIFETIME_FIELD_NUMBER: _ClassVar[int]
    MAXRETRANSMITS_FIELD_NUMBER: _ClassVar[int]
    streamId: int
    ordered: bool
    maxPacketLifeTime: int
    maxRetransmits: int
    def __init__(self, streamId: _Optional[int] = ..., ordered: bool = ..., maxPacketLifeTime: _Optional[int] = ..., maxRetransmits: _Optional[int] = ...) -> None: ...
