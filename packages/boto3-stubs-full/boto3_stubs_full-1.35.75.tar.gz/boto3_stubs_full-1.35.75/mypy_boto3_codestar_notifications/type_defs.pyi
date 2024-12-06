"""
Type annotations for codestar-notifications service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/type_defs/)

Usage::

    ```python
    from mypy_boto3_codestar_notifications.type_defs import TargetTypeDef

    data: TargetTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    DetailTypeType,
    ListEventTypesFilterNameType,
    ListNotificationRulesFilterNameType,
    ListTargetsFilterNameType,
    NotificationRuleStatusType,
    TargetStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateNotificationRuleRequestRequestTypeDef",
    "CreateNotificationRuleResultTypeDef",
    "DeleteNotificationRuleRequestRequestTypeDef",
    "DeleteNotificationRuleResultTypeDef",
    "DeleteTargetRequestRequestTypeDef",
    "DescribeNotificationRuleRequestRequestTypeDef",
    "DescribeNotificationRuleResultTypeDef",
    "EventTypeSummaryTypeDef",
    "ListEventTypesFilterTypeDef",
    "ListEventTypesRequestListEventTypesPaginateTypeDef",
    "ListEventTypesRequestRequestTypeDef",
    "ListEventTypesResultTypeDef",
    "ListNotificationRulesFilterTypeDef",
    "ListNotificationRulesRequestListNotificationRulesPaginateTypeDef",
    "ListNotificationRulesRequestRequestTypeDef",
    "ListNotificationRulesResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "ListTargetsFilterTypeDef",
    "ListTargetsRequestListTargetsPaginateTypeDef",
    "ListTargetsRequestRequestTypeDef",
    "ListTargetsResultTypeDef",
    "NotificationRuleSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SubscribeRequestRequestTypeDef",
    "SubscribeResultTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagResourceResultTypeDef",
    "TargetSummaryTypeDef",
    "TargetTypeDef",
    "UnsubscribeRequestRequestTypeDef",
    "UnsubscribeResultTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateNotificationRuleRequestRequestTypeDef",
)

class TargetTypeDef(TypedDict):
    TargetType: NotRequired[str]
    TargetAddress: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteNotificationRuleRequestRequestTypeDef(TypedDict):
    Arn: str

class DeleteTargetRequestRequestTypeDef(TypedDict):
    TargetAddress: str
    ForceUnsubscribeAll: NotRequired[bool]

class DescribeNotificationRuleRequestRequestTypeDef(TypedDict):
    Arn: str

EventTypeSummaryTypeDef = TypedDict(
    "EventTypeSummaryTypeDef",
    {
        "EventTypeId": NotRequired[str],
        "ServiceName": NotRequired[str],
        "EventTypeName": NotRequired[str],
        "ResourceType": NotRequired[str],
    },
)

class TargetSummaryTypeDef(TypedDict):
    TargetAddress: NotRequired[str]
    TargetType: NotRequired[str]
    TargetStatus: NotRequired[TargetStatusType]

class ListEventTypesFilterTypeDef(TypedDict):
    Name: ListEventTypesFilterNameType
    Value: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListNotificationRulesFilterTypeDef(TypedDict):
    Name: ListNotificationRulesFilterNameType
    Value: str

class NotificationRuleSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    Arn: str

class ListTargetsFilterTypeDef(TypedDict):
    Name: ListTargetsFilterNameType
    Value: str

class TagResourceRequestRequestTypeDef(TypedDict):
    Arn: str
    Tags: Mapping[str, str]

class UnsubscribeRequestRequestTypeDef(TypedDict):
    Arn: str
    TargetAddress: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    Arn: str
    TagKeys: Sequence[str]

class CreateNotificationRuleRequestRequestTypeDef(TypedDict):
    Name: str
    EventTypeIds: Sequence[str]
    Resource: str
    Targets: Sequence[TargetTypeDef]
    DetailType: DetailTypeType
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    Status: NotRequired[NotificationRuleStatusType]

class SubscribeRequestRequestTypeDef(TypedDict):
    Arn: str
    Target: TargetTypeDef
    ClientRequestToken: NotRequired[str]

class UpdateNotificationRuleRequestRequestTypeDef(TypedDict):
    Arn: str
    Name: NotRequired[str]
    Status: NotRequired[NotificationRuleStatusType]
    EventTypeIds: NotRequired[Sequence[str]]
    Targets: NotRequired[Sequence[TargetTypeDef]]
    DetailType: NotRequired[DetailTypeType]

class CreateNotificationRuleResultTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNotificationRuleResultTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResultTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SubscribeResultTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceResultTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UnsubscribeResultTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListEventTypesResultTypeDef(TypedDict):
    EventTypes: List[EventTypeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeNotificationRuleResultTypeDef(TypedDict):
    Arn: str
    Name: str
    EventTypes: List[EventTypeSummaryTypeDef]
    Resource: str
    Targets: List[TargetSummaryTypeDef]
    DetailType: DetailTypeType
    CreatedBy: str
    Status: NotificationRuleStatusType
    CreatedTimestamp: datetime
    LastModifiedTimestamp: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTargetsResultTypeDef(TypedDict):
    Targets: List[TargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEventTypesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListEventTypesFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEventTypesRequestListEventTypesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListEventTypesFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNotificationRulesRequestListNotificationRulesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListNotificationRulesFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNotificationRulesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListNotificationRulesFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListNotificationRulesResultTypeDef(TypedDict):
    NotificationRules: List[NotificationRuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTargetsRequestListTargetsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListTargetsFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTargetsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ListTargetsFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
