from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    INFO: _ClassVar[LogLevel]
    WARN: _ClassVar[LogLevel]
    ERROR: _ClassVar[LogLevel]
    DEBUG: _ClassVar[LogLevel]

class LogSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MODEL_GENERATOR: _ClassVar[LogSource]
    MODEL_EXECUTOR: _ClassVar[LogSource]
    RESULT_PROCESSOR: _ClassVar[LogSource]
INFO: LogLevel
WARN: LogLevel
ERROR: LogLevel
DEBUG: LogLevel
MODEL_GENERATOR: LogSource
MODEL_EXECUTOR: LogSource
RESULT_PROCESSOR: LogSource

class LogMessage(_message.Message):
    __slots__ = ["workPackageId", "scenario", "yearNull", "yearSet", "feeder", "timeStepNull", "timeStepSet", "timestamp", "severity", "message", "source"]
    WORKPACKAGEID_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_FIELD_NUMBER: _ClassVar[int]
    YEARNULL_FIELD_NUMBER: _ClassVar[int]
    YEARSET_FIELD_NUMBER: _ClassVar[int]
    FEEDER_FIELD_NUMBER: _ClassVar[int]
    TIMESTEPNULL_FIELD_NUMBER: _ClassVar[int]
    TIMESTEPSET_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    workPackageId: str
    scenario: str
    yearNull: _struct_pb2.NullValue
    yearSet: int
    feeder: str
    timeStepNull: _struct_pb2.NullValue
    timeStepSet: _timestamp_pb2.Timestamp
    timestamp: _timestamp_pb2.Timestamp
    severity: LogLevel
    message: str
    source: LogSource
    def __init__(self, workPackageId: _Optional[str] = ..., scenario: _Optional[str] = ..., yearNull: _Optional[_Union[_struct_pb2.NullValue, str]] = ..., yearSet: _Optional[int] = ..., feeder: _Optional[str] = ..., timeStepNull: _Optional[_Union[_struct_pb2.NullValue, str]] = ..., timeStepSet: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., severity: _Optional[_Union[LogLevel, str]] = ..., message: _Optional[str] = ..., source: _Optional[_Union[LogSource, str]] = ...) -> None: ...
