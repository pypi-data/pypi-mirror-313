from zepben.protobuf.cim.iec61970.base.wires import Conductor_pb2 as _Conductor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AcLineSegment(_message.Message):
    __slots__ = ["cd", "perLengthSequenceImpedanceMRID"]
    CD_FIELD_NUMBER: _ClassVar[int]
    PERLENGTHSEQUENCEIMPEDANCEMRID_FIELD_NUMBER: _ClassVar[int]
    cd: _Conductor_pb2.Conductor
    perLengthSequenceImpedanceMRID: str
    def __init__(self, cd: _Optional[_Union[_Conductor_pb2.Conductor, _Mapping]] = ..., perLengthSequenceImpedanceMRID: _Optional[str] = ...) -> None: ...
