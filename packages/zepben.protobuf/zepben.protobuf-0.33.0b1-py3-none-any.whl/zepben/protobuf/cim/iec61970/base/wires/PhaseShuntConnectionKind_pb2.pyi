from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class PhaseShuntConnectionKind(_message.Message):
    __slots__ = []
    class Enum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        UNKNOWN: _ClassVar[PhaseShuntConnectionKind.Enum]
        D: _ClassVar[PhaseShuntConnectionKind.Enum]
        Y: _ClassVar[PhaseShuntConnectionKind.Enum]
        Yn: _ClassVar[PhaseShuntConnectionKind.Enum]
        I: _ClassVar[PhaseShuntConnectionKind.Enum]
        G: _ClassVar[PhaseShuntConnectionKind.Enum]
    UNKNOWN: PhaseShuntConnectionKind.Enum
    D: PhaseShuntConnectionKind.Enum
    Y: PhaseShuntConnectionKind.Enum
    Yn: PhaseShuntConnectionKind.Enum
    I: PhaseShuntConnectionKind.Enum
    G: PhaseShuntConnectionKind.Enum
    def __init__(self) -> None: ...
