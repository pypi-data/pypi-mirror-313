import common_models_pb2 as _common_models_pb2
import user_pb2 as _user_pb2
import common_models_pb2 as _common_models_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination
from user_pb2 import LoginRequest as LoginRequest
from user_pb2 import LoginResponse as LoginResponse
from user_pb2 import UserChangePasswordRequest as UserChangePasswordRequest
from user_pb2 import UserChangePasswordResponse as UserChangePasswordResponse
from user_pb2 import UserGenerateTempPasswordRequest as UserGenerateTempPasswordRequest
from user_pb2 import UserGenerateTempPasswordResponse as UserGenerateTempPasswordResponse
from user_pb2 import User as User
from user_pb2 import UserCreateRequest as UserCreateRequest
from user_pb2 import UserCreateResponse as UserCreateResponse
from user_pb2 import UserUpdateRequest as UserUpdateRequest
from user_pb2 import UserUpdateResponse as UserUpdateResponse
from user_pb2 import UserDeleteRequest as UserDeleteRequest
from user_pb2 import UserDeleteResponse as UserDeleteResponse
from user_pb2 import UserGetRequest as UserGetRequest
from user_pb2 import UserGetResponse as UserGetResponse
from user_pb2 import UserListRequest as UserListRequest
from user_pb2 import UserListResponse as UserListResponse
from user_pb2 import KeyValuePair as KeyValuePair
from user_pb2 import UserPropertiesGetRequest as UserPropertiesGetRequest
from user_pb2 import UserPropertiesGetResponse as UserPropertiesGetResponse
from user_pb2 import UserPropertiesUpdateRequest as UserPropertiesUpdateRequest
from user_pb2 import UserPropertiesUpdateResponse as UserPropertiesUpdateResponse
from user_pb2 import UserPublicKeyRequest as UserPublicKeyRequest
from user_pb2 import UserPublicKeyResponse as UserPublicKeyResponse

DESCRIPTOR: _descriptor.FileDescriptor

class UserCollection(_message.Message):
    __slots__ = ("id", "name", "users")
    class WellKnownIds(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        USER_COLLECTION_UNKNOWN: _ClassVar[UserCollection.WellKnownIds]
        USER_COLLECTION_ID_PUBLIC: _ClassVar[UserCollection.WellKnownIds]
    USER_COLLECTION_UNKNOWN: UserCollection.WellKnownIds
    USER_COLLECTION_ID_PUBLIC: UserCollection.WellKnownIds
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    users: _containers.RepeatedCompositeFieldContainer[_user_pb2.User]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., users: _Optional[_Iterable[_Union[_user_pb2.User, _Mapping]]] = ...) -> None: ...

class UserCollectionCreateRequest(_message.Message):
    __slots__ = ("name", "parent_collection_ids")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARENT_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    parent_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., parent_collection_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UserCollectionCreateResponse(_message.Message):
    __slots__ = ("status_code", "collection")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    collection: UserCollection
    def __init__(self, status_code: _Optional[int] = ..., collection: _Optional[_Union[UserCollection, _Mapping]] = ...) -> None: ...

class UserCollectionGetRequest(_message.Message):
    __slots__ = ("collection", "include_users")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_USERS_FIELD_NUMBER: _ClassVar[int]
    collection: UserCollection
    include_users: bool
    def __init__(self, collection: _Optional[_Union[UserCollection, _Mapping]] = ..., include_users: bool = ...) -> None: ...

class UserCollectionGetResponse(_message.Message):
    __slots__ = ("status_code", "collection")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    collection: UserCollection
    def __init__(self, status_code: _Optional[int] = ..., collection: _Optional[_Union[UserCollection, _Mapping]] = ...) -> None: ...

class UserCollectionUpdateRequest(_message.Message):
    __slots__ = ("collection",)
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    collection: UserCollection
    def __init__(self, collection: _Optional[_Union[UserCollection, _Mapping]] = ...) -> None: ...

class UserCollectionUpdateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserCollectionDeleteRequest(_message.Message):
    __slots__ = ("collection_id",)
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    def __init__(self, collection_id: _Optional[str] = ...) -> None: ...

class UserCollectionDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserCollectionAddUserRequest(_message.Message):
    __slots__ = ("user_id", "collection_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    collection_id: str
    def __init__(self, user_id: _Optional[str] = ..., collection_id: _Optional[str] = ...) -> None: ...

class UserCollectionAddUserResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserCollectionRemoveUserRequest(_message.Message):
    __slots__ = ("user_id", "collection_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    collection_id: str
    def __init__(self, user_id: _Optional[str] = ..., collection_id: _Optional[str] = ...) -> None: ...

class UserCollectionRemoveUserResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class UserCollectionListRequest(_message.Message):
    __slots__ = ("parent_collection_id", "collection_type", "search_text", "max_search_depth", "include_users")
    class UserCollectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_USER_COLLECTION_TYPE: _ClassVar[UserCollectionListRequest.UserCollectionType]
        USER_COLLECTION_TYPE_ANY: _ClassVar[UserCollectionListRequest.UserCollectionType]
        USER_COLLECTION_TYPE_CUSTOMER: _ClassVar[UserCollectionListRequest.UserCollectionType]
        USER_COLLECTION_TYPE_DEPARTMENT: _ClassVar[UserCollectionListRequest.UserCollectionType]
        USER_COLLECTION_TYPE_USER: _ClassVar[UserCollectionListRequest.UserCollectionType]
        USER_COLLECTION_TYPE_ADMINS: _ClassVar[UserCollectionListRequest.UserCollectionType]
    UNKNOWN_USER_COLLECTION_TYPE: UserCollectionListRequest.UserCollectionType
    USER_COLLECTION_TYPE_ANY: UserCollectionListRequest.UserCollectionType
    USER_COLLECTION_TYPE_CUSTOMER: UserCollectionListRequest.UserCollectionType
    USER_COLLECTION_TYPE_DEPARTMENT: UserCollectionListRequest.UserCollectionType
    USER_COLLECTION_TYPE_USER: UserCollectionListRequest.UserCollectionType
    USER_COLLECTION_TYPE_ADMINS: UserCollectionListRequest.UserCollectionType
    PARENT_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    MAX_SEARCH_DEPTH_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_USERS_FIELD_NUMBER: _ClassVar[int]
    parent_collection_id: str
    collection_type: UserCollectionListRequest.UserCollectionType
    search_text: str
    max_search_depth: int
    include_users: bool
    def __init__(self, parent_collection_id: _Optional[str] = ..., collection_type: _Optional[_Union[UserCollectionListRequest.UserCollectionType, str]] = ..., search_text: _Optional[str] = ..., max_search_depth: _Optional[int] = ..., include_users: bool = ...) -> None: ...

class UserCollectionListResponse(_message.Message):
    __slots__ = ("status_code", "collections")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    collections: _containers.RepeatedCompositeFieldContainer[UserCollection]
    def __init__(self, status_code: _Optional[int] = ..., collections: _Optional[_Iterable[_Union[UserCollection, _Mapping]]] = ...) -> None: ...
