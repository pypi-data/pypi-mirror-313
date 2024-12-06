"""
Type annotations for resource-groups service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/type_defs/)

Usage::

    ```python
    from mypy_boto3_resource_groups.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    GroupConfigurationStatusType,
    GroupFilterNameType,
    GroupingStatusType,
    GroupingTypeType,
    GroupLifecycleEventsDesiredStatusType,
    GroupLifecycleEventsStatusType,
    ListGroupingStatusesFilterNameType,
    QueryErrorCodeType,
    QueryTypeType,
    TagSyncTaskStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountSettingsTypeDef",
    "CancelTagSyncTaskInputRequestTypeDef",
    "CreateGroupInputRequestTypeDef",
    "CreateGroupOutputTypeDef",
    "DeleteGroupInputRequestTypeDef",
    "DeleteGroupOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FailedResourceTypeDef",
    "GetAccountSettingsOutputTypeDef",
    "GetGroupConfigurationInputRequestTypeDef",
    "GetGroupConfigurationOutputTypeDef",
    "GetGroupInputRequestTypeDef",
    "GetGroupOutputTypeDef",
    "GetGroupQueryInputRequestTypeDef",
    "GetGroupQueryOutputTypeDef",
    "GetTagSyncTaskInputRequestTypeDef",
    "GetTagSyncTaskOutputTypeDef",
    "GetTagsInputRequestTypeDef",
    "GetTagsOutputTypeDef",
    "GroupConfigurationItemOutputTypeDef",
    "GroupConfigurationItemTypeDef",
    "GroupConfigurationItemUnionTypeDef",
    "GroupConfigurationParameterOutputTypeDef",
    "GroupConfigurationParameterTypeDef",
    "GroupConfigurationParameterUnionTypeDef",
    "GroupConfigurationTypeDef",
    "GroupFilterTypeDef",
    "GroupIdentifierTypeDef",
    "GroupQueryTypeDef",
    "GroupResourcesInputRequestTypeDef",
    "GroupResourcesOutputTypeDef",
    "GroupTypeDef",
    "GroupingStatusesItemTypeDef",
    "ListGroupResourcesInputListGroupResourcesPaginateTypeDef",
    "ListGroupResourcesInputRequestTypeDef",
    "ListGroupResourcesItemTypeDef",
    "ListGroupResourcesOutputTypeDef",
    "ListGroupingStatusesFilterTypeDef",
    "ListGroupingStatusesInputListGroupingStatusesPaginateTypeDef",
    "ListGroupingStatusesInputRequestTypeDef",
    "ListGroupingStatusesOutputTypeDef",
    "ListGroupsInputListGroupsPaginateTypeDef",
    "ListGroupsInputRequestTypeDef",
    "ListGroupsOutputTypeDef",
    "ListTagSyncTasksFilterTypeDef",
    "ListTagSyncTasksInputListTagSyncTasksPaginateTypeDef",
    "ListTagSyncTasksInputRequestTypeDef",
    "ListTagSyncTasksOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PendingResourceTypeDef",
    "PutGroupConfigurationInputRequestTypeDef",
    "QueryErrorTypeDef",
    "ResourceFilterTypeDef",
    "ResourceIdentifierTypeDef",
    "ResourceQueryTypeDef",
    "ResourceStatusTypeDef",
    "ResponseMetadataTypeDef",
    "SearchResourcesInputRequestTypeDef",
    "SearchResourcesInputSearchResourcesPaginateTypeDef",
    "SearchResourcesOutputTypeDef",
    "StartTagSyncTaskInputRequestTypeDef",
    "StartTagSyncTaskOutputTypeDef",
    "TagInputRequestTypeDef",
    "TagOutputTypeDef",
    "TagSyncTaskItemTypeDef",
    "UngroupResourcesInputRequestTypeDef",
    "UngroupResourcesOutputTypeDef",
    "UntagInputRequestTypeDef",
    "UntagOutputTypeDef",
    "UpdateAccountSettingsInputRequestTypeDef",
    "UpdateAccountSettingsOutputTypeDef",
    "UpdateGroupInputRequestTypeDef",
    "UpdateGroupOutputTypeDef",
    "UpdateGroupQueryInputRequestTypeDef",
    "UpdateGroupQueryOutputTypeDef",
)


class AccountSettingsTypeDef(TypedDict):
    GroupLifecycleEventsDesiredStatus: NotRequired[GroupLifecycleEventsDesiredStatusType]
    GroupLifecycleEventsStatus: NotRequired[GroupLifecycleEventsStatusType]
    GroupLifecycleEventsStatusMessage: NotRequired[str]


class CancelTagSyncTaskInputRequestTypeDef(TypedDict):
    TaskArn: str


ResourceQueryTypeDef = TypedDict(
    "ResourceQueryTypeDef",
    {
        "Type": QueryTypeType,
        "Query": str,
    },
)


class GroupTypeDef(TypedDict):
    GroupArn: str
    Name: str
    Description: NotRequired[str]
    Criticality: NotRequired[int]
    Owner: NotRequired[str]
    DisplayName: NotRequired[str]
    ApplicationTag: NotRequired[Dict[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteGroupInputRequestTypeDef(TypedDict):
    GroupName: NotRequired[str]
    Group: NotRequired[str]


class FailedResourceTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    ErrorMessage: NotRequired[str]
    ErrorCode: NotRequired[str]


class GetGroupConfigurationInputRequestTypeDef(TypedDict):
    Group: NotRequired[str]


class GetGroupInputRequestTypeDef(TypedDict):
    GroupName: NotRequired[str]
    Group: NotRequired[str]


class GetGroupQueryInputRequestTypeDef(TypedDict):
    GroupName: NotRequired[str]
    Group: NotRequired[str]


class GetTagSyncTaskInputRequestTypeDef(TypedDict):
    TaskArn: str


class GetTagsInputRequestTypeDef(TypedDict):
    Arn: str


class GroupConfigurationParameterOutputTypeDef(TypedDict):
    Name: str
    Values: NotRequired[List[str]]


class GroupConfigurationParameterTypeDef(TypedDict):
    Name: str
    Values: NotRequired[Sequence[str]]


class GroupFilterTypeDef(TypedDict):
    Name: GroupFilterNameType
    Values: Sequence[str]


class GroupIdentifierTypeDef(TypedDict):
    GroupName: NotRequired[str]
    GroupArn: NotRequired[str]
    Description: NotRequired[str]
    Criticality: NotRequired[int]
    Owner: NotRequired[str]
    DisplayName: NotRequired[str]


class GroupResourcesInputRequestTypeDef(TypedDict):
    Group: str
    ResourceArns: Sequence[str]


class PendingResourceTypeDef(TypedDict):
    ResourceArn: NotRequired[str]


class GroupingStatusesItemTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    Action: NotRequired[GroupingTypeType]
    Status: NotRequired[GroupingStatusType]
    ErrorMessage: NotRequired[str]
    ErrorCode: NotRequired[str]
    UpdatedAt: NotRequired[datetime]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ResourceFilterTypeDef(TypedDict):
    Name: Literal["resource-type"]
    Values: Sequence[str]


class ResourceIdentifierTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]


class ResourceStatusTypeDef(TypedDict):
    Name: NotRequired[Literal["PENDING"]]


class QueryErrorTypeDef(TypedDict):
    ErrorCode: NotRequired[QueryErrorCodeType]
    Message: NotRequired[str]


class ListGroupingStatusesFilterTypeDef(TypedDict):
    Name: ListGroupingStatusesFilterNameType
    Values: Sequence[str]


class ListTagSyncTasksFilterTypeDef(TypedDict):
    GroupArn: NotRequired[str]
    GroupName: NotRequired[str]


class TagSyncTaskItemTypeDef(TypedDict):
    GroupArn: NotRequired[str]
    GroupName: NotRequired[str]
    TaskArn: NotRequired[str]
    TagKey: NotRequired[str]
    TagValue: NotRequired[str]
    RoleArn: NotRequired[str]
    Status: NotRequired[TagSyncTaskStatusType]
    ErrorMessage: NotRequired[str]
    CreatedAt: NotRequired[datetime]


class StartTagSyncTaskInputRequestTypeDef(TypedDict):
    Group: str
    TagKey: str
    TagValue: str
    RoleArn: str


class TagInputRequestTypeDef(TypedDict):
    Arn: str
    Tags: Mapping[str, str]


class UngroupResourcesInputRequestTypeDef(TypedDict):
    Group: str
    ResourceArns: Sequence[str]


class UntagInputRequestTypeDef(TypedDict):
    Arn: str
    Keys: Sequence[str]


class UpdateAccountSettingsInputRequestTypeDef(TypedDict):
    GroupLifecycleEventsDesiredStatus: NotRequired[GroupLifecycleEventsDesiredStatusType]


class UpdateGroupInputRequestTypeDef(TypedDict):
    GroupName: NotRequired[str]
    Group: NotRequired[str]
    Description: NotRequired[str]
    Criticality: NotRequired[int]
    Owner: NotRequired[str]
    DisplayName: NotRequired[str]


class GroupQueryTypeDef(TypedDict):
    GroupName: str
    ResourceQuery: ResourceQueryTypeDef


class SearchResourcesInputRequestTypeDef(TypedDict):
    ResourceQuery: ResourceQueryTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class UpdateGroupQueryInputRequestTypeDef(TypedDict):
    ResourceQuery: ResourceQueryTypeDef
    GroupName: NotRequired[str]
    Group: NotRequired[str]


class DeleteGroupOutputTypeDef(TypedDict):
    Group: GroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccountSettingsOutputTypeDef(TypedDict):
    AccountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupOutputTypeDef(TypedDict):
    Group: GroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTagSyncTaskOutputTypeDef(TypedDict):
    GroupArn: str
    GroupName: str
    TaskArn: str
    TagKey: str
    TagValue: str
    RoleArn: str
    Status: TagSyncTaskStatusType
    ErrorMessage: str
    CreatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetTagsOutputTypeDef(TypedDict):
    Arn: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartTagSyncTaskOutputTypeDef(TypedDict):
    GroupArn: str
    GroupName: str
    TaskArn: str
    TagKey: str
    TagValue: str
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class TagOutputTypeDef(TypedDict):
    Arn: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UntagOutputTypeDef(TypedDict):
    Arn: str
    Keys: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountSettingsOutputTypeDef(TypedDict):
    AccountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGroupOutputTypeDef(TypedDict):
    Group: GroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


GroupConfigurationItemOutputTypeDef = TypedDict(
    "GroupConfigurationItemOutputTypeDef",
    {
        "Type": str,
        "Parameters": NotRequired[List[GroupConfigurationParameterOutputTypeDef]],
    },
)
GroupConfigurationParameterUnionTypeDef = Union[
    GroupConfigurationParameterTypeDef, GroupConfigurationParameterOutputTypeDef
]


class ListGroupsInputRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[GroupFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListGroupsOutputTypeDef(TypedDict):
    GroupIdentifiers: List[GroupIdentifierTypeDef]
    Groups: List[GroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GroupResourcesOutputTypeDef(TypedDict):
    Succeeded: List[str]
    Failed: List[FailedResourceTypeDef]
    Pending: List[PendingResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UngroupResourcesOutputTypeDef(TypedDict):
    Succeeded: List[str]
    Failed: List[FailedResourceTypeDef]
    Pending: List[PendingResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupingStatusesOutputTypeDef(TypedDict):
    Group: str
    GroupingStatuses: List[GroupingStatusesItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGroupsInputListGroupsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[GroupFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchResourcesInputSearchResourcesPaginateTypeDef(TypedDict):
    ResourceQuery: ResourceQueryTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupResourcesInputListGroupResourcesPaginateTypeDef(TypedDict):
    GroupName: NotRequired[str]
    Group: NotRequired[str]
    Filters: NotRequired[Sequence[ResourceFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupResourcesInputRequestTypeDef(TypedDict):
    GroupName: NotRequired[str]
    Group: NotRequired[str]
    Filters: NotRequired[Sequence[ResourceFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListGroupResourcesItemTypeDef(TypedDict):
    Identifier: NotRequired[ResourceIdentifierTypeDef]
    Status: NotRequired[ResourceStatusTypeDef]


class SearchResourcesOutputTypeDef(TypedDict):
    ResourceIdentifiers: List[ResourceIdentifierTypeDef]
    QueryErrors: List[QueryErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGroupingStatusesInputListGroupingStatusesPaginateTypeDef(TypedDict):
    Group: str
    Filters: NotRequired[Sequence[ListGroupingStatusesFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupingStatusesInputRequestTypeDef(TypedDict):
    Group: str
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[ListGroupingStatusesFilterTypeDef]]
    NextToken: NotRequired[str]


class ListTagSyncTasksInputListTagSyncTasksPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListTagSyncTasksFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagSyncTasksInputRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListTagSyncTasksFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagSyncTasksOutputTypeDef(TypedDict):
    TagSyncTasks: List[TagSyncTaskItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetGroupQueryOutputTypeDef(TypedDict):
    GroupQuery: GroupQueryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGroupQueryOutputTypeDef(TypedDict):
    GroupQuery: GroupQueryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GroupConfigurationTypeDef(TypedDict):
    Configuration: NotRequired[List[GroupConfigurationItemOutputTypeDef]]
    ProposedConfiguration: NotRequired[List[GroupConfigurationItemOutputTypeDef]]
    Status: NotRequired[GroupConfigurationStatusType]
    FailureReason: NotRequired[str]


GroupConfigurationItemTypeDef = TypedDict(
    "GroupConfigurationItemTypeDef",
    {
        "Type": str,
        "Parameters": NotRequired[Sequence[GroupConfigurationParameterUnionTypeDef]],
    },
)


class ListGroupResourcesOutputTypeDef(TypedDict):
    Resources: List[ListGroupResourcesItemTypeDef]
    ResourceIdentifiers: List[ResourceIdentifierTypeDef]
    QueryErrors: List[QueryErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateGroupOutputTypeDef(TypedDict):
    Group: GroupTypeDef
    ResourceQuery: ResourceQueryTypeDef
    Tags: Dict[str, str]
    GroupConfiguration: GroupConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupConfigurationOutputTypeDef(TypedDict):
    GroupConfiguration: GroupConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


GroupConfigurationItemUnionTypeDef = Union[
    GroupConfigurationItemTypeDef, GroupConfigurationItemOutputTypeDef
]


class PutGroupConfigurationInputRequestTypeDef(TypedDict):
    Group: NotRequired[str]
    Configuration: NotRequired[Sequence[GroupConfigurationItemTypeDef]]


class CreateGroupInputRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    ResourceQuery: NotRequired[ResourceQueryTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    Configuration: NotRequired[Sequence[GroupConfigurationItemUnionTypeDef]]
    Criticality: NotRequired[int]
    Owner: NotRequired[str]
    DisplayName: NotRequired[str]
