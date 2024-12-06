from bauplan._bpln_proto.commander.service.v2 import common_pb2 as _common_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_STATUS_UNSPECIFIED: _ClassVar[JobStatus]
    JOB_STATUS_PENDING: _ClassVar[JobStatus]
    JOB_STATUS_RUNNING: _ClassVar[JobStatus]
    JOB_STATUS_COMPLETED: _ClassVar[JobStatus]
    JOB_STATUS_FAILED: _ClassVar[JobStatus]
    JOB_STATUS_CANCELED: _ClassVar[JobStatus]

JOB_STATUS_UNSPECIFIED: JobStatus
JOB_STATUS_PENDING: JobStatus
JOB_STATUS_RUNNING: JobStatus
JOB_STATUS_COMPLETED: JobStatus
JOB_STATUS_FAILED: JobStatus
JOB_STATUS_CANCELED: JobStatus

class RunnerAction(_message.Message):
    __slots__ = ('job_id', 'action', 'job_request', 'trace_id', 'parent_span_id', 'job_args')
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACTION_UNSPECIFIED: _ClassVar[RunnerAction.Action]
        ACTION_START: _ClassVar[RunnerAction.Action]
        ACTION_CANCEL: _ClassVar[RunnerAction.Action]
        ACTION_UPLOAD: _ClassVar[RunnerAction.Action]
        ACTION_QUERY: _ClassVar[RunnerAction.Action]

    ACTION_UNSPECIFIED: RunnerAction.Action
    ACTION_START: RunnerAction.Action
    ACTION_CANCEL: RunnerAction.Action
    ACTION_UPLOAD: RunnerAction.Action
    ACTION_QUERY: RunnerAction.Action
    class JobArgsEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    JOB_REQUEST_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ARGS_FIELD_NUMBER: _ClassVar[int]
    job_id: _common_pb2.JobId
    action: RunnerAction.Action
    job_request: JobRequest
    trace_id: str
    parent_span_id: str
    job_args: _containers.ScalarMap[str, str]
    def __init__(
        self,
        job_id: _Optional[_Union[_common_pb2.JobId, _Mapping]] = ...,
        action: _Optional[_Union[RunnerAction.Action, str]] = ...,
        job_request: _Optional[_Union[JobRequest, _Mapping]] = ...,
        trace_id: _Optional[str] = ...,
        parent_span_id: _Optional[str] = ...,
        job_args: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class JobRequest(_message.Message):
    __slots__ = (
        'detach',
        'args',
        'status',
        'scheduled_runner_id',
        'physical_plan_v2',
        'scheduling_error',
        'user',
        'created_at',
        'finished_at',
        'read_branch',
        'write_branch',
        'tags',
    )
    class ArgsEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class TagsEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    DETACH_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_RUNNER_ID_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_PLAN_V2_FIELD_NUMBER: _ClassVar[int]
    SCHEDULING_ERROR_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    READ_BRANCH_FIELD_NUMBER: _ClassVar[int]
    WRITE_BRANCH_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    detach: bool
    args: _containers.ScalarMap[str, str]
    status: JobStatus
    scheduled_runner_id: str
    physical_plan_v2: bytes
    scheduling_error: str
    user: str
    created_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    read_branch: str
    write_branch: str
    tags: _containers.ScalarMap[str, str]
    def __init__(
        self,
        detach: bool = ...,
        args: _Optional[_Mapping[str, str]] = ...,
        status: _Optional[_Union[JobStatus, str]] = ...,
        scheduled_runner_id: _Optional[str] = ...,
        physical_plan_v2: _Optional[bytes] = ...,
        scheduling_error: _Optional[str] = ...,
        user: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        read_branch: _Optional[str] = ...,
        write_branch: _Optional[str] = ...,
        tags: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class TriggerRunRequest(_message.Message):
    __slots__ = (
        'zip_file',
        'module_version',
        'client_hostname',
        'args',
        'is_flight_query',
        'query_for_flight',
        'run_id',
        'cache',
        'namespace',
    )
    class ArgsEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ZIP_FILE_FIELD_NUMBER: _ClassVar[int]
    MODULE_VERSION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    IS_FLIGHT_QUERY_FIELD_NUMBER: _ClassVar[int]
    QUERY_FOR_FLIGHT_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    CACHE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    zip_file: bytes
    module_version: str
    client_hostname: str
    args: _containers.ScalarMap[str, str]
    is_flight_query: bool
    query_for_flight: str
    run_id: str
    cache: bool
    namespace: str
    def __init__(
        self,
        zip_file: _Optional[bytes] = ...,
        module_version: _Optional[str] = ...,
        client_hostname: _Optional[str] = ...,
        args: _Optional[_Mapping[str, str]] = ...,
        is_flight_query: bool = ...,
        query_for_flight: _Optional[str] = ...,
        run_id: _Optional[str] = ...,
        cache: bool = ...,
        namespace: _Optional[str] = ...,
    ) -> None: ...
