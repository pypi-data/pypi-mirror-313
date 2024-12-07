from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TransformerCoolingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN_COOLING_TYPE: _ClassVar[TransformerCoolingType]
    ONAN: _ClassVar[TransformerCoolingType]
    ONAF: _ClassVar[TransformerCoolingType]
    OFAF: _ClassVar[TransformerCoolingType]
    OFWF: _ClassVar[TransformerCoolingType]
    ODAF: _ClassVar[TransformerCoolingType]
    KNAN: _ClassVar[TransformerCoolingType]
    KNAF: _ClassVar[TransformerCoolingType]
    KFAF: _ClassVar[TransformerCoolingType]
    KFWF: _ClassVar[TransformerCoolingType]
    KDAF: _ClassVar[TransformerCoolingType]
UNKNOWN_COOLING_TYPE: TransformerCoolingType
ONAN: TransformerCoolingType
ONAF: TransformerCoolingType
OFAF: TransformerCoolingType
OFWF: TransformerCoolingType
ODAF: TransformerCoolingType
KNAN: TransformerCoolingType
KNAF: TransformerCoolingType
KFAF: TransformerCoolingType
KFWF: TransformerCoolingType
KDAF: TransformerCoolingType
