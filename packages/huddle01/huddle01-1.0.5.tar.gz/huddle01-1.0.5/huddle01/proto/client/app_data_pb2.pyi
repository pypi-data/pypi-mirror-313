from typing import (
    ClassVar as _ClassVar,
)
from typing import (
    Mapping as _Mapping,
)
from typing import (
    Optional as _Optional,
)
from typing import (
    Union as _Union,
)

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Value(_message.Message):
    __slots__ = ("string_value", "int_value", "float_value")
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    string_value: str
    int_value: int
    float_value: float
    def __init__(
        self,
        string_value: _Optional[str] = ...,
        int_value: _Optional[int] = ...,
        float_value: _Optional[float] = ...,
    ) -> None: ...

class AppData(_message.Message):
    __slots__ = ("appData",)
    class AppDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Value
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[Value, _Mapping]] = ...,
        ) -> None: ...

    APPDATA_FIELD_NUMBER: _ClassVar[int]
    appData: _containers.MessageMap[str, Value]
    def __init__(self, appData: _Optional[_Mapping[str, Value]] = ...) -> None: ...
