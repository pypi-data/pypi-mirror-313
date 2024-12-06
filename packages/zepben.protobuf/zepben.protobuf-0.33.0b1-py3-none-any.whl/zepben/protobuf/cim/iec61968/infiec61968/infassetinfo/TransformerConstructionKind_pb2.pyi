from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TransformerConstructionKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    unknown: _ClassVar[TransformerConstructionKind]
    onePhase: _ClassVar[TransformerConstructionKind]
    threePhase: _ClassVar[TransformerConstructionKind]
    aerial: _ClassVar[TransformerConstructionKind]
    overhead: _ClassVar[TransformerConstructionKind]
    dryType: _ClassVar[TransformerConstructionKind]
    network: _ClassVar[TransformerConstructionKind]
    padmountDeadFront: _ClassVar[TransformerConstructionKind]
    padmountFeedThrough: _ClassVar[TransformerConstructionKind]
    padmountLiveFront: _ClassVar[TransformerConstructionKind]
    padmountLoopThrough: _ClassVar[TransformerConstructionKind]
    padmounted: _ClassVar[TransformerConstructionKind]
    subway: _ClassVar[TransformerConstructionKind]
    underground: _ClassVar[TransformerConstructionKind]
    vault: _ClassVar[TransformerConstructionKind]
    vaultThreePhase: _ClassVar[TransformerConstructionKind]
unknown: TransformerConstructionKind
onePhase: TransformerConstructionKind
threePhase: TransformerConstructionKind
aerial: TransformerConstructionKind
overhead: TransformerConstructionKind
dryType: TransformerConstructionKind
network: TransformerConstructionKind
padmountDeadFront: TransformerConstructionKind
padmountFeedThrough: TransformerConstructionKind
padmountLiveFront: TransformerConstructionKind
padmountLoopThrough: TransformerConstructionKind
padmounted: TransformerConstructionKind
subway: TransformerConstructionKind
underground: TransformerConstructionKind
vault: TransformerConstructionKind
vaultThreePhase: TransformerConstructionKind
