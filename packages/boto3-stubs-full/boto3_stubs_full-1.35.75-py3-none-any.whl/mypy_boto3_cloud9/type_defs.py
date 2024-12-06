"""
Type annotations for cloud9 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloud9.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ConnectionTypeType,
    EnvironmentLifecycleStatusType,
    EnvironmentStatusType,
    EnvironmentTypeType,
    ManagedCredentialsActionType,
    ManagedCredentialsStatusType,
    MemberPermissionsType,
    PermissionsType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CreateEnvironmentEC2RequestRequestTypeDef",
    "CreateEnvironmentEC2ResultTypeDef",
    "CreateEnvironmentMembershipRequestRequestTypeDef",
    "CreateEnvironmentMembershipResultTypeDef",
    "DeleteEnvironmentMembershipRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DescribeEnvironmentMembershipsRequestDescribeEnvironmentMembershipsPaginateTypeDef",
    "DescribeEnvironmentMembershipsRequestRequestTypeDef",
    "DescribeEnvironmentMembershipsResultTypeDef",
    "DescribeEnvironmentStatusRequestRequestTypeDef",
    "DescribeEnvironmentStatusResultTypeDef",
    "DescribeEnvironmentsRequestRequestTypeDef",
    "DescribeEnvironmentsResultTypeDef",
    "EnvironmentLifecycleTypeDef",
    "EnvironmentMemberTypeDef",
    "EnvironmentTypeDef",
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListEnvironmentsResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateEnvironmentMembershipRequestRequestTypeDef",
    "UpdateEnvironmentMembershipResultTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
)


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateEnvironmentMembershipRequestRequestTypeDef(TypedDict):
    environmentId: str
    userArn: str
    permissions: MemberPermissionsType


class EnvironmentMemberTypeDef(TypedDict):
    permissions: PermissionsType
    userId: str
    userArn: str
    environmentId: str
    lastAccess: NotRequired[datetime]


class DeleteEnvironmentMembershipRequestRequestTypeDef(TypedDict):
    environmentId: str
    userArn: str


class DeleteEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeEnvironmentMembershipsRequestRequestTypeDef(TypedDict):
    userArn: NotRequired[str]
    environmentId: NotRequired[str]
    permissions: NotRequired[Sequence[PermissionsType]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class DescribeEnvironmentStatusRequestRequestTypeDef(TypedDict):
    environmentId: str


class DescribeEnvironmentsRequestRequestTypeDef(TypedDict):
    environmentIds: Sequence[str]


class EnvironmentLifecycleTypeDef(TypedDict):
    status: NotRequired[EnvironmentLifecycleStatusType]
    reason: NotRequired[str]
    failureResource: NotRequired[str]


class ListEnvironmentsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateEnvironmentMembershipRequestRequestTypeDef(TypedDict):
    environmentId: str
    userArn: str
    permissions: MemberPermissionsType


class UpdateEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str
    name: NotRequired[str]
    description: NotRequired[str]
    managedCredentialsAction: NotRequired[ManagedCredentialsActionType]


class CreateEnvironmentEC2RequestRequestTypeDef(TypedDict):
    name: str
    instanceType: str
    imageId: str
    description: NotRequired[str]
    clientRequestToken: NotRequired[str]
    subnetId: NotRequired[str]
    automaticStopTimeMinutes: NotRequired[int]
    ownerArn: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    connectionType: NotRequired[ConnectionTypeType]
    dryRun: NotRequired[bool]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateEnvironmentEC2ResultTypeDef(TypedDict):
    environmentId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEnvironmentStatusResultTypeDef(TypedDict):
    status: EnvironmentStatusType
    message: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListEnvironmentsResultTypeDef(TypedDict):
    environmentIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEnvironmentMembershipResultTypeDef(TypedDict):
    membership: EnvironmentMemberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEnvironmentMembershipsResultTypeDef(TypedDict):
    memberships: List[EnvironmentMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateEnvironmentMembershipResultTypeDef(TypedDict):
    membership: EnvironmentMemberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEnvironmentMembershipsRequestDescribeEnvironmentMembershipsPaginateTypeDef(TypedDict):
    userArn: NotRequired[str]
    environmentId: NotRequired[str]
    permissions: NotRequired[Sequence[PermissionsType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentsRequestListEnvironmentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "type": EnvironmentTypeType,
        "arn": str,
        "ownerArn": str,
        "id": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "connectionType": NotRequired[ConnectionTypeType],
        "lifecycle": NotRequired[EnvironmentLifecycleTypeDef],
        "managedCredentialsStatus": NotRequired[ManagedCredentialsStatusType],
    },
)


class DescribeEnvironmentsResultTypeDef(TypedDict):
    environments: List[EnvironmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
