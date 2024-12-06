from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class BatteryStateKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[BatteryStateKind]
    discharging: _ClassVar[BatteryStateKind]
    full: _ClassVar[BatteryStateKind]
    waiting: _ClassVar[BatteryStateKind]
    charging: _ClassVar[BatteryStateKind]
    empty: _ClassVar[BatteryStateKind]
UNKNOWN: BatteryStateKind
discharging: BatteryStateKind
full: BatteryStateKind
waiting: BatteryStateKind
charging: BatteryStateKind
empty: BatteryStateKind
