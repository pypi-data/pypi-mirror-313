from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoNumSctpStreams(_message.Message):
    __slots__ = ("OS", "MIS")
    OS_FIELD_NUMBER: _ClassVar[int]
    MIS_FIELD_NUMBER: _ClassVar[int]
    OS: int
    MIS: int
    def __init__(self, OS: _Optional[int] = ..., MIS: _Optional[int] = ...) -> None: ...

class ProtoSctpCapabilities(_message.Message):
    __slots__ = ("numStreams",)
    NUMSTREAMS_FIELD_NUMBER: _ClassVar[int]
    numStreams: ProtoNumSctpStreams
    def __init__(self, numStreams: _Optional[_Union[ProtoNumSctpStreams, _Mapping]] = ...) -> None: ...
