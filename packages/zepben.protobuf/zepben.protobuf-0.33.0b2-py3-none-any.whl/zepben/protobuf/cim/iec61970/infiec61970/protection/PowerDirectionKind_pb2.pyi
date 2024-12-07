from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class PowerDirectionKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN_DIRECTION: _ClassVar[PowerDirectionKind]
    UNDIRECTED: _ClassVar[PowerDirectionKind]
    FORWARD: _ClassVar[PowerDirectionKind]
    REVERSE: _ClassVar[PowerDirectionKind]
UNKNOWN_DIRECTION: PowerDirectionKind
UNDIRECTED: PowerDirectionKind
FORWARD: PowerDirectionKind
REVERSE: PowerDirectionKind
