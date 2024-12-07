from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class RegulatingControlModeKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN_CONTROL_MODE: _ClassVar[RegulatingControlModeKind]
    voltage: _ClassVar[RegulatingControlModeKind]
    activePower: _ClassVar[RegulatingControlModeKind]
    reactivePower: _ClassVar[RegulatingControlModeKind]
    currentFlow: _ClassVar[RegulatingControlModeKind]
    admittance: _ClassVar[RegulatingControlModeKind]
    timeScheduled: _ClassVar[RegulatingControlModeKind]
    temperature: _ClassVar[RegulatingControlModeKind]
    powerFactor: _ClassVar[RegulatingControlModeKind]
UNKNOWN_CONTROL_MODE: RegulatingControlModeKind
voltage: RegulatingControlModeKind
activePower: RegulatingControlModeKind
reactivePower: RegulatingControlModeKind
currentFlow: RegulatingControlModeKind
admittance: RegulatingControlModeKind
timeScheduled: RegulatingControlModeKind
temperature: RegulatingControlModeKind
powerFactor: RegulatingControlModeKind
