from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IncludedEnergizingContainers(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    EXCLUDE_ENERGIZING_CONTAINERS: _ClassVar[IncludedEnergizingContainers]
    INCLUDE_ENERGIZING_FEEDERS: _ClassVar[IncludedEnergizingContainers]
    INCLUDE_ENERGIZING_SUBSTATIONS: _ClassVar[IncludedEnergizingContainers]

class IncludedEnergizedContainers(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    EXCLUDE_ENERGIZED_CONTAINERS: _ClassVar[IncludedEnergizedContainers]
    INCLUDE_ENERGIZED_FEEDERS: _ClassVar[IncludedEnergizedContainers]
    INCLUDE_ENERGIZED_LV_FEEDERS: _ClassVar[IncludedEnergizedContainers]
EXCLUDE_ENERGIZING_CONTAINERS: IncludedEnergizingContainers
INCLUDE_ENERGIZING_FEEDERS: IncludedEnergizingContainers
INCLUDE_ENERGIZING_SUBSTATIONS: IncludedEnergizingContainers
EXCLUDE_ENERGIZED_CONTAINERS: IncludedEnergizedContainers
INCLUDE_ENERGIZED_FEEDERS: IncludedEnergizedContainers
INCLUDE_ENERGIZED_LV_FEEDERS: IncludedEnergizedContainers

class GetIdentifiedObjectsRequest(_message.Message):
    __slots__ = ["messageId", "mrids"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    MRIDS_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    mrids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, messageId: _Optional[int] = ..., mrids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetNetworkHierarchyRequest(_message.Message):
    __slots__ = ["messageId"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    def __init__(self, messageId: _Optional[int] = ...) -> None: ...

class GetEquipmentForContainersRequest(_message.Message):
    __slots__ = ["messageId", "mrids", "includeEnergizingContainers", "includeEnergizedContainers"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    MRIDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDEENERGIZINGCONTAINERS_FIELD_NUMBER: _ClassVar[int]
    INCLUDEENERGIZEDCONTAINERS_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    mrids: _containers.RepeatedScalarFieldContainer[str]
    includeEnergizingContainers: IncludedEnergizingContainers
    includeEnergizedContainers: IncludedEnergizedContainers
    def __init__(self, messageId: _Optional[int] = ..., mrids: _Optional[_Iterable[str]] = ..., includeEnergizingContainers: _Optional[_Union[IncludedEnergizingContainers, str]] = ..., includeEnergizedContainers: _Optional[_Union[IncludedEnergizedContainers, str]] = ...) -> None: ...

class GetCurrentEquipmentForFeederRequest(_message.Message):
    __slots__ = ["messageId", "mrid"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    MRID_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    mrid: str
    def __init__(self, messageId: _Optional[int] = ..., mrid: _Optional[str] = ...) -> None: ...

class GetEquipmentForRestrictionRequest(_message.Message):
    __slots__ = ["messageId", "mrid"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    MRID_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    mrid: str
    def __init__(self, messageId: _Optional[int] = ..., mrid: _Optional[str] = ...) -> None: ...

class GetTerminalsForNodeRequest(_message.Message):
    __slots__ = ["messageId", "mrid"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    MRID_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    mrid: str
    def __init__(self, messageId: _Optional[int] = ..., mrid: _Optional[str] = ...) -> None: ...
