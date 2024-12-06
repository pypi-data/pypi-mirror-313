from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class StreetlightLampKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[StreetlightLampKind]
    HIGH_PRESSURE_SODIUM: _ClassVar[StreetlightLampKind]
    MERCURY_VAPOR: _ClassVar[StreetlightLampKind]
    METAL_HALIDE: _ClassVar[StreetlightLampKind]
    OTHER: _ClassVar[StreetlightLampKind]
UNKNOWN: StreetlightLampKind
HIGH_PRESSURE_SODIUM: StreetlightLampKind
MERCURY_VAPOR: StreetlightLampKind
METAL_HALIDE: StreetlightLampKind
OTHER: StreetlightLampKind
