from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class SynchronousMachineKind(_message.Message):
    __slots__ = []
    class Enum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        UNKNOWN: _ClassVar[SynchronousMachineKind.Enum]
        generator: _ClassVar[SynchronousMachineKind.Enum]
        condenser: _ClassVar[SynchronousMachineKind.Enum]
        generatorOrCondenser: _ClassVar[SynchronousMachineKind.Enum]
        motor: _ClassVar[SynchronousMachineKind.Enum]
        generatorOrMotor: _ClassVar[SynchronousMachineKind.Enum]
        motorOrCondenser: _ClassVar[SynchronousMachineKind.Enum]
        generatorOrCondenserOrMotor: _ClassVar[SynchronousMachineKind.Enum]
    UNKNOWN: SynchronousMachineKind.Enum
    generator: SynchronousMachineKind.Enum
    condenser: SynchronousMachineKind.Enum
    generatorOrCondenser: SynchronousMachineKind.Enum
    motor: SynchronousMachineKind.Enum
    generatorOrMotor: SynchronousMachineKind.Enum
    motorOrCondenser: SynchronousMachineKind.Enum
    generatorOrCondenserOrMotor: SynchronousMachineKind.Enum
    def __init__(self) -> None: ...
