from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TransformerFunctionKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    other: _ClassVar[TransformerFunctionKind]
    voltageRegulator: _ClassVar[TransformerFunctionKind]
    distributionTransformer: _ClassVar[TransformerFunctionKind]
    isolationTransformer: _ClassVar[TransformerFunctionKind]
    autotransformer: _ClassVar[TransformerFunctionKind]
    powerTransformer: _ClassVar[TransformerFunctionKind]
    secondaryTransformer: _ClassVar[TransformerFunctionKind]
other: TransformerFunctionKind
voltageRegulator: TransformerFunctionKind
distributionTransformer: TransformerFunctionKind
isolationTransformer: TransformerFunctionKind
autotransformer: TransformerFunctionKind
powerTransformer: TransformerFunctionKind
secondaryTransformer: TransformerFunctionKind
