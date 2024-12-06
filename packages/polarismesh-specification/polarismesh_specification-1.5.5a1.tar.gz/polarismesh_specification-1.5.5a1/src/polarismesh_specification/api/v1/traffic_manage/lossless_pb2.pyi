from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LosslessRule(_message.Message):
    __slots__ = ("id", "service", "namespace", "revision", "ctime", "mtime", "losslessOnline", "losslessOffline", "metadata", "editable", "deleteable")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    LOSSLESSONLINE_FIELD_NUMBER: _ClassVar[int]
    LOSSLESSOFFLINE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    EDITABLE_FIELD_NUMBER: _ClassVar[int]
    DELETEABLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    service: str
    namespace: str
    revision: str
    ctime: str
    mtime: str
    losslessOnline: LosslessOnline
    losslessOffline: LosslessOffline
    metadata: _containers.ScalarMap[str, str]
    editable: bool
    deleteable: bool
    def __init__(self, id: _Optional[str] = ..., service: _Optional[str] = ..., namespace: _Optional[str] = ..., revision: _Optional[str] = ..., ctime: _Optional[str] = ..., mtime: _Optional[str] = ..., losslessOnline: _Optional[_Union[LosslessOnline, _Mapping]] = ..., losslessOffline: _Optional[_Union[LosslessOffline, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., editable: bool = ..., deleteable: bool = ...) -> None: ...

class LosslessOnline(_message.Message):
    __slots__ = ("delayRegister", "warmup", "readiness")
    DELAYREGISTER_FIELD_NUMBER: _ClassVar[int]
    WARMUP_FIELD_NUMBER: _ClassVar[int]
    READINESS_FIELD_NUMBER: _ClassVar[int]
    delayRegister: DelayRegister
    warmup: Warmup
    readiness: Readiness
    def __init__(self, delayRegister: _Optional[_Union[DelayRegister, _Mapping]] = ..., warmup: _Optional[_Union[Warmup, _Mapping]] = ..., readiness: _Optional[_Union[Readiness, _Mapping]] = ...) -> None: ...

class DelayRegister(_message.Message):
    __slots__ = ("enable", "strategy", "intervalSecond", "healthCheckProtocol", "healthCheckMethod", "healthCheckPath", "healthCheckIntervalSecond")
    class DelayStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DELAY_BY_TIME: _ClassVar[DelayRegister.DelayStrategy]
        DELAY_BY_HEALTH_CHECK: _ClassVar[DelayRegister.DelayStrategy]
    DELAY_BY_TIME: DelayRegister.DelayStrategy
    DELAY_BY_HEALTH_CHECK: DelayRegister.DelayStrategy
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_FIELD_NUMBER: _ClassVar[int]
    INTERVALSECOND_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECKPROTOCOL_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECKMETHOD_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECKPATH_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECKINTERVALSECOND_FIELD_NUMBER: _ClassVar[int]
    enable: bool
    strategy: DelayRegister.DelayStrategy
    intervalSecond: int
    healthCheckProtocol: str
    healthCheckMethod: str
    healthCheckPath: str
    healthCheckIntervalSecond: str
    def __init__(self, enable: bool = ..., strategy: _Optional[_Union[DelayRegister.DelayStrategy, str]] = ..., intervalSecond: _Optional[int] = ..., healthCheckProtocol: _Optional[str] = ..., healthCheckMethod: _Optional[str] = ..., healthCheckPath: _Optional[str] = ..., healthCheckIntervalSecond: _Optional[str] = ...) -> None: ...

class Warmup(_message.Message):
    __slots__ = ("enable", "intervalSecond", "enableOverloadProtection", "overloadProtectionThreshold", "curvature")
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    INTERVALSECOND_FIELD_NUMBER: _ClassVar[int]
    ENABLEOVERLOADPROTECTION_FIELD_NUMBER: _ClassVar[int]
    OVERLOADPROTECTIONTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    CURVATURE_FIELD_NUMBER: _ClassVar[int]
    enable: bool
    intervalSecond: int
    enableOverloadProtection: bool
    overloadProtectionThreshold: int
    curvature: int
    def __init__(self, enable: bool = ..., intervalSecond: _Optional[int] = ..., enableOverloadProtection: bool = ..., overloadProtectionThreshold: _Optional[int] = ..., curvature: _Optional[int] = ...) -> None: ...

class Readiness(_message.Message):
    __slots__ = ("enable",)
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    enable: bool
    def __init__(self, enable: bool = ...) -> None: ...

class LosslessOffline(_message.Message):
    __slots__ = ("enable",)
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    enable: bool
    def __init__(self, enable: bool = ...) -> None: ...
