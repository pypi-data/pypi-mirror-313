from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class PotentialTransformerKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[PotentialTransformerKind]
    inductive: _ClassVar[PotentialTransformerKind]
    capacitiveCoupling: _ClassVar[PotentialTransformerKind]
UNKNOWN: PotentialTransformerKind
inductive: PotentialTransformerKind
capacitiveCoupling: PotentialTransformerKind
