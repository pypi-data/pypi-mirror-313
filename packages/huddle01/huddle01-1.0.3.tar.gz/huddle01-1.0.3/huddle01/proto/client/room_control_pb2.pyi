from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProduceSources(_message.Message):
    __slots__ = ("mic", "cam", "screen")
    MIC_FIELD_NUMBER: _ClassVar[int]
    CAM_FIELD_NUMBER: _ClassVar[int]
    SCREEN_FIELD_NUMBER: _ClassVar[int]
    mic: bool
    cam: bool
    screen: bool
    def __init__(self, mic: bool = ..., cam: bool = ..., screen: bool = ...) -> None: ...

class RoomControlType(_message.Message):
    __slots__ = ("type", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: str
    value: bool
    def __init__(self, type: _Optional[str] = ..., value: bool = ...) -> None: ...

class ProduceSourcesControl(_message.Message):
    __slots__ = ("type", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: str
    value: ProduceSources
    def __init__(self, type: _Optional[str] = ..., value: _Optional[_Union[ProduceSources, _Mapping]] = ...) -> None: ...
