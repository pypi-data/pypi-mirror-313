from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class WindingConnection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN_WINDING: _ClassVar[WindingConnection]
    D: _ClassVar[WindingConnection]
    Y: _ClassVar[WindingConnection]
    Z: _ClassVar[WindingConnection]
    Yn: _ClassVar[WindingConnection]
    Zn: _ClassVar[WindingConnection]
    A: _ClassVar[WindingConnection]
    I: _ClassVar[WindingConnection]
UNKNOWN_WINDING: WindingConnection
D: WindingConnection
Y: WindingConnection
Z: WindingConnection
Yn: WindingConnection
Zn: WindingConnection
A: WindingConnection
I: WindingConnection
