from typing import ClassVar as _ClassVar
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class Permissions(_message.Message):
    __slots__ = (
        "admin",
        "canConsume",
        "canProduce",
        "canProduceSources",
        "canSendData",
        "canRecvData",
        "canUpdateMetadata",
    )
    class ProduceSources(_message.Message):
        __slots__ = ("cam", "mic", "screen")
        CAM_FIELD_NUMBER: _ClassVar[int]
        MIC_FIELD_NUMBER: _ClassVar[int]
        SCREEN_FIELD_NUMBER: _ClassVar[int]
        cam: bool
        mic: bool
        screen: bool
        def __init__(
            self, cam: bool = ..., mic: bool = ..., screen: bool = ...
        ) -> None: ...

    ADMIN_FIELD_NUMBER: _ClassVar[int]
    CANCONSUME_FIELD_NUMBER: _ClassVar[int]
    CANPRODUCE_FIELD_NUMBER: _ClassVar[int]
    CANPRODUCESOURCES_FIELD_NUMBER: _ClassVar[int]
    CANSENDDATA_FIELD_NUMBER: _ClassVar[int]
    CANRECVDATA_FIELD_NUMBER: _ClassVar[int]
    CANUPDATEMETADATA_FIELD_NUMBER: _ClassVar[int]
    admin: bool
    canConsume: bool
    canProduce: bool
    canProduceSources: Permissions.ProduceSources
    canSendData: bool
    canRecvData: bool
    canUpdateMetadata: bool
    def __init__(
        self,
        admin: bool = ...,
        canConsume: bool = ...,
        canProduce: bool = ...,
        canProduceSources: _Optional[
            _Union[Permissions.ProduceSources, _Mapping]
        ] = ...,
        canSendData: bool = ...,
        canRecvData: bool = ...,
        canUpdateMetadata: bool = ...,
    ) -> None: ...
