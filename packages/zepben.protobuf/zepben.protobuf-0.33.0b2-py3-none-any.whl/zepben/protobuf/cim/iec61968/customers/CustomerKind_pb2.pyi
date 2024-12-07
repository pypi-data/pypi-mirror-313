from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class CustomerKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[CustomerKind]
    commercialIndustrial: _ClassVar[CustomerKind]
    energyServiceScheduler: _ClassVar[CustomerKind]
    energyServiceSupplier: _ClassVar[CustomerKind]
    enterprise: _ClassVar[CustomerKind]
    internalUse: _ClassVar[CustomerKind]
    other: _ClassVar[CustomerKind]
    pumpingLoad: _ClassVar[CustomerKind]
    regionalOperator: _ClassVar[CustomerKind]
    residential: _ClassVar[CustomerKind]
    residentialAndCommercial: _ClassVar[CustomerKind]
    residentialAndStreetlight: _ClassVar[CustomerKind]
    residentialFarmService: _ClassVar[CustomerKind]
    residentialStreetlightOthers: _ClassVar[CustomerKind]
    subsidiary: _ClassVar[CustomerKind]
    windMachine: _ClassVar[CustomerKind]
UNKNOWN: CustomerKind
commercialIndustrial: CustomerKind
energyServiceScheduler: CustomerKind
energyServiceSupplier: CustomerKind
enterprise: CustomerKind
internalUse: CustomerKind
other: CustomerKind
pumpingLoad: CustomerKind
regionalOperator: CustomerKind
residential: CustomerKind
residentialAndCommercial: CustomerKind
residentialAndStreetlight: CustomerKind
residentialFarmService: CustomerKind
residentialStreetlightOthers: CustomerKind
subsidiary: CustomerKind
windMachine: CustomerKind
