from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class Account(_message.Message):
    __slots__ = ('api_key', 'email', 'full_name', 'enabled', 'username', 'is_admin', 'nessie_host', 'runners')
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    IS_ADMIN_FIELD_NUMBER: _ClassVar[int]
    NESSIE_HOST_FIELD_NUMBER: _ClassVar[int]
    RUNNERS_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    email: str
    full_name: str
    enabled: bool
    username: str
    is_admin: bool
    nessie_host: str
    runners: str
    def __init__(
        self,
        api_key: _Optional[str] = ...,
        email: _Optional[str] = ...,
        full_name: _Optional[str] = ...,
        enabled: bool = ...,
        username: _Optional[str] = ...,
        is_admin: bool = ...,
        nessie_host: _Optional[str] = ...,
        runners: _Optional[str] = ...,
    ) -> None: ...

class SyncAlphaAccountsRequest(_message.Message):
    __slots__ = ('accounts', 'magic_token')
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    MAGIC_TOKEN_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[Account]
    magic_token: str
    def __init__(
        self,
        accounts: _Optional[_Iterable[_Union[Account, _Mapping]]] = ...,
        magic_token: _Optional[str] = ...,
    ) -> None: ...

class SyncAlphaAccountsResponse(_message.Message):
    __slots__ = ('error',)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: str
    def __init__(self, error: _Optional[str] = ...) -> None: ...
