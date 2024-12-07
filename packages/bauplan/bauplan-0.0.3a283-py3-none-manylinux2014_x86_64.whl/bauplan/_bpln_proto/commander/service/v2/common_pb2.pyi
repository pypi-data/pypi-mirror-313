from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobRequestOptionalBool(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_REQUEST_OPTIONAL_BOOL_UNSPECIFIED: _ClassVar[JobRequestOptionalBool]
    JOB_REQUEST_OPTIONAL_BOOL_TRUE: _ClassVar[JobRequestOptionalBool]
    JOB_REQUEST_OPTIONAL_BOOL_FALSE: _ClassVar[JobRequestOptionalBool]

JOB_REQUEST_OPTIONAL_BOOL_UNSPECIFIED: JobRequestOptionalBool
JOB_REQUEST_OPTIONAL_BOOL_TRUE: JobRequestOptionalBool
JOB_REQUEST_OPTIONAL_BOOL_FALSE: JobRequestOptionalBool

class JobRequestCommon(_message.Message):
    __slots__ = ('module_version', 'hostname', 'args', 'debug')
    class ArgsEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    MODULE_VERSION_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    module_version: str
    hostname: str
    args: _containers.ScalarMap[str, str]
    debug: JobRequestOptionalBool
    def __init__(
        self,
        module_version: _Optional[str] = ...,
        hostname: _Optional[str] = ...,
        args: _Optional[_Mapping[str, str]] = ...,
        debug: _Optional[_Union[JobRequestOptionalBool, str]] = ...,
    ) -> None: ...

class JobResponseCommon(_message.Message):
    __slots__ = ('job_id', 'debug', 'args', 'username')
    class ArgsEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    debug: bool
    args: _containers.ScalarMap[str, str]
    username: str
    def __init__(
        self,
        job_id: _Optional[str] = ...,
        debug: bool = ...,
        args: _Optional[_Mapping[str, str]] = ...,
        username: _Optional[str] = ...,
    ) -> None: ...

class TriggerRunOpts(_message.Message):
    __slots__ = ('cache',)
    CACHE_FIELD_NUMBER: _ClassVar[int]
    cache: bool
    def __init__(self, cache: bool = ...) -> None: ...

class JobInfo(_message.Message):
    __slots__ = ('id', 'status', 'kind', 'user', 'created_at', 'finished_at', 'runner')
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    RUNNER_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    kind: str
    user: str
    created_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    runner: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        user: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        runner: _Optional[str] = ...,
    ) -> None: ...

class JobId(_message.Message):
    __slots__ = ('id', 'snapshot_uri', 'dag_graphviz', 'dag_ascii', 'scheduled_runner_id')
    ID_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_URI_FIELD_NUMBER: _ClassVar[int]
    DAG_GRAPHVIZ_FIELD_NUMBER: _ClassVar[int]
    DAG_ASCII_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_RUNNER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    snapshot_uri: str
    dag_graphviz: str
    dag_ascii: str
    scheduled_runner_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        snapshot_uri: _Optional[str] = ...,
        dag_graphviz: _Optional[str] = ...,
        dag_ascii: _Optional[str] = ...,
        scheduled_runner_id: _Optional[str] = ...,
    ) -> None: ...

class IntParameterValue(_message.Message):
    __slots__ = ('value',)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class FloatParameterValue(_message.Message):
    __slots__ = ('value',)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...

class BoolParameterValue(_message.Message):
    __slots__ = ('value',)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: bool = ...) -> None: ...

class StrParameterValue(_message.Message):
    __slots__ = ('value',)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class SecretParameterValue(_message.Message):
    __slots__ = ('value', 'key')
    VALUE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    value: str
    key: str
    def __init__(self, value: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class VaultParameterValue(_message.Message):
    __slots__ = ('value',)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class Parameter(_message.Message):
    __slots__ = ('name', 'int_value', 'float_value', 'bool_value', 'str_value', 'secret_value', 'vault_value')
    NAME_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    STR_VALUE_FIELD_NUMBER: _ClassVar[int]
    SECRET_VALUE_FIELD_NUMBER: _ClassVar[int]
    VAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    int_value: IntParameterValue
    float_value: FloatParameterValue
    bool_value: BoolParameterValue
    str_value: StrParameterValue
    secret_value: SecretParameterValue
    vault_value: VaultParameterValue
    def __init__(
        self,
        name: _Optional[str] = ...,
        int_value: _Optional[_Union[IntParameterValue, _Mapping]] = ...,
        float_value: _Optional[_Union[FloatParameterValue, _Mapping]] = ...,
        bool_value: _Optional[_Union[BoolParameterValue, _Mapping]] = ...,
        str_value: _Optional[_Union[StrParameterValue, _Mapping]] = ...,
        secret_value: _Optional[_Union[SecretParameterValue, _Mapping]] = ...,
        vault_value: _Optional[_Union[VaultParameterValue, _Mapping]] = ...,
    ) -> None: ...
