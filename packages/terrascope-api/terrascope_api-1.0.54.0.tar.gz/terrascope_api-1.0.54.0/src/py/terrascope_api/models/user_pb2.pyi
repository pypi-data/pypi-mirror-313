import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("status_code", "jwt_token")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    JWT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    jwt_token: str
    def __init__(self, status_code: _Optional[int] = ..., jwt_token: _Optional[str] = ...) -> None: ...

class UserChangePasswordRequest(_message.Message):
    __slots__ = ("old_password", "new_password")
    OLD_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    old_password: str
    new_password: str
    def __init__(self, old_password: _Optional[str] = ..., new_password: _Optional[str] = ...) -> None: ...

class UserChangePasswordResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserGenerateTempPasswordRequest(_message.Message):
    __slots__ = ("user_email",)
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    user_email: str
    def __init__(self, user_email: _Optional[str] = ...) -> None: ...

class UserGenerateTempPasswordResponse(_message.Message):
    __slots__ = ("status_code", "new_password")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    new_password: str
    def __init__(self, status_code: _Optional[int] = ..., new_password: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name", "email", "user_collection_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    email: str
    user_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., user_collection_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UserCreateRequest(_message.Message):
    __slots__ = ("name", "email", "user_collection_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    user_collection_id: str
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., user_collection_id: _Optional[str] = ...) -> None: ...

class UserCreateResponse(_message.Message):
    __slots__ = ("status_code", "user")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    user: User
    def __init__(self, status_code: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UserUpdateRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UserUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserDeleteRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class UserDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserGetRequest(_message.Message):
    __slots__ = ("ids", "emails")
    IDS_FIELD_NUMBER: _ClassVar[int]
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    emails: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., emails: _Optional[_Iterable[str]] = ...) -> None: ...

class UserGetResponse(_message.Message):
    __slots__ = ("status_code", "users")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, status_code: _Optional[int] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class UserListRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class UserListResponse(_message.Message):
    __slots__ = ("status_code", "users")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, status_code: _Optional[int] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class KeyValuePair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class UserPropertiesGetRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UserPropertiesGetResponse(_message.Message):
    __slots__ = ("status_code", "properties")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    properties: _containers.RepeatedCompositeFieldContainer[KeyValuePair]
    def __init__(self, status_code: _Optional[int] = ..., properties: _Optional[_Iterable[_Union[KeyValuePair, _Mapping]]] = ...) -> None: ...

class UserPropertiesUpdateRequest(_message.Message):
    __slots__ = ("properties", "replace_all")
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    REPLACE_ALL_FIELD_NUMBER: _ClassVar[int]
    properties: _containers.RepeatedCompositeFieldContainer[KeyValuePair]
    replace_all: bool
    def __init__(self, properties: _Optional[_Iterable[_Union[KeyValuePair, _Mapping]]] = ..., replace_all: bool = ...) -> None: ...

class UserPropertiesUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserPublicKeyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UserPublicKeyResponse(_message.Message):
    __slots__ = ("status_code", "key_pem")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    KEY_PEM_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    key_pem: str
    def __init__(self, status_code: _Optional[int] = ..., key_pem: _Optional[str] = ...) -> None: ...
