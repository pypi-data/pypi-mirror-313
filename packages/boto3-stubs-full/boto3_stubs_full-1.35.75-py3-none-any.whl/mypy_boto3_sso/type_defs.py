"""
Type annotations for sso service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/type_defs/)

Usage::

    ```python
    from mypy_boto3_sso.type_defs import AccountInfoTypeDef

    data: AccountInfoTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccountInfoTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetRoleCredentialsRequestRequestTypeDef",
    "GetRoleCredentialsResponseTypeDef",
    "ListAccountRolesRequestListAccountRolesPaginateTypeDef",
    "ListAccountRolesRequestRequestTypeDef",
    "ListAccountRolesResponseTypeDef",
    "ListAccountsRequestListAccountsPaginateTypeDef",
    "ListAccountsRequestRequestTypeDef",
    "ListAccountsResponseTypeDef",
    "LogoutRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RoleCredentialsTypeDef",
    "RoleInfoTypeDef",
)


class AccountInfoTypeDef(TypedDict):
    accountId: NotRequired[str]
    accountName: NotRequired[str]
    emailAddress: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GetRoleCredentialsRequestRequestTypeDef(TypedDict):
    roleName: str
    accountId: str
    accessToken: str


class RoleCredentialsTypeDef(TypedDict):
    accessKeyId: NotRequired[str]
    secretAccessKey: NotRequired[str]
    sessionToken: NotRequired[str]
    expiration: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAccountRolesRequestRequestTypeDef(TypedDict):
    accessToken: str
    accountId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class RoleInfoTypeDef(TypedDict):
    roleName: NotRequired[str]
    accountId: NotRequired[str]


class ListAccountsRequestRequestTypeDef(TypedDict):
    accessToken: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class LogoutRequestRequestTypeDef(TypedDict):
    accessToken: str


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccountsResponseTypeDef(TypedDict):
    accountList: List[AccountInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetRoleCredentialsResponseTypeDef(TypedDict):
    roleCredentials: RoleCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccountRolesRequestListAccountRolesPaginateTypeDef(TypedDict):
    accessToken: str
    accountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccountsRequestListAccountsPaginateTypeDef(TypedDict):
    accessToken: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccountRolesResponseTypeDef(TypedDict):
    roleList: List[RoleInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
