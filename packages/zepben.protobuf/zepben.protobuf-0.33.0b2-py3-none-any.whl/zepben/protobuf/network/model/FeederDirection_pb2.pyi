from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class FeederDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NONE: _ClassVar[FeederDirection]
    UPSTREAM: _ClassVar[FeederDirection]
    DOWNSTREAM: _ClassVar[FeederDirection]
    BOTH: _ClassVar[FeederDirection]
NONE: FeederDirection
UPSTREAM: FeederDirection
DOWNSTREAM: FeederDirection
BOTH: FeederDirection
