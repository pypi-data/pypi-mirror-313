from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class WireMaterialKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[WireMaterialKind]
    aaac: _ClassVar[WireMaterialKind]
    acsr: _ClassVar[WireMaterialKind]
    acsrAz: _ClassVar[WireMaterialKind]
    aluminum: _ClassVar[WireMaterialKind]
    aluminumAlloy: _ClassVar[WireMaterialKind]
    aluminumAlloySteel: _ClassVar[WireMaterialKind]
    aluminumSteel: _ClassVar[WireMaterialKind]
    copper: _ClassVar[WireMaterialKind]
    copperCadmium: _ClassVar[WireMaterialKind]
    other: _ClassVar[WireMaterialKind]
    steel: _ClassVar[WireMaterialKind]
UNKNOWN: WireMaterialKind
aaac: WireMaterialKind
acsr: WireMaterialKind
acsrAz: WireMaterialKind
aluminum: WireMaterialKind
aluminumAlloy: WireMaterialKind
aluminumAlloySteel: WireMaterialKind
aluminumSteel: WireMaterialKind
copper: WireMaterialKind
copperCadmium: WireMaterialKind
other: WireMaterialKind
steel: WireMaterialKind
