"""
Type annotations for health service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/type_defs/)

Usage::

    ```python
    from mypy_boto3_health.type_defs import AccountEntityAggregateTypeDef

    data: AccountEntityAggregateTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    EntityStatusCodeType,
    EventScopeCodeType,
    EventStatusCodeType,
    EventTypeCategoryType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountEntityAggregateTypeDef",
    "AffectedEntityTypeDef",
    "DateTimeRangeTypeDef",
    "DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef",
    "DescribeAffectedAccountsForOrganizationRequestRequestTypeDef",
    "DescribeAffectedAccountsForOrganizationResponseTypeDef",
    "DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef",
    "DescribeAffectedEntitiesForOrganizationRequestRequestTypeDef",
    "DescribeAffectedEntitiesForOrganizationResponseTypeDef",
    "DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef",
    "DescribeAffectedEntitiesRequestRequestTypeDef",
    "DescribeAffectedEntitiesResponseTypeDef",
    "DescribeEntityAggregatesForOrganizationRequestRequestTypeDef",
    "DescribeEntityAggregatesForOrganizationResponseTypeDef",
    "DescribeEntityAggregatesRequestRequestTypeDef",
    "DescribeEntityAggregatesResponseTypeDef",
    "DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef",
    "DescribeEventAggregatesRequestRequestTypeDef",
    "DescribeEventAggregatesResponseTypeDef",
    "DescribeEventDetailsForOrganizationRequestRequestTypeDef",
    "DescribeEventDetailsForOrganizationResponseTypeDef",
    "DescribeEventDetailsRequestRequestTypeDef",
    "DescribeEventDetailsResponseTypeDef",
    "DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef",
    "DescribeEventTypesRequestRequestTypeDef",
    "DescribeEventTypesResponseTypeDef",
    "DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef",
    "DescribeEventsForOrganizationRequestRequestTypeDef",
    "DescribeEventsForOrganizationResponseTypeDef",
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    "DescribeEventsRequestRequestTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeHealthServiceStatusForOrganizationResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EntityAccountFilterTypeDef",
    "EntityAggregateTypeDef",
    "EntityFilterTypeDef",
    "EventAccountFilterTypeDef",
    "EventAggregateTypeDef",
    "EventDescriptionTypeDef",
    "EventDetailsErrorItemTypeDef",
    "EventDetailsTypeDef",
    "EventFilterTypeDef",
    "EventTypeDef",
    "EventTypeFilterTypeDef",
    "EventTypeTypeDef",
    "OrganizationAffectedEntitiesErrorItemTypeDef",
    "OrganizationEntityAggregateTypeDef",
    "OrganizationEventDetailsErrorItemTypeDef",
    "OrganizationEventDetailsTypeDef",
    "OrganizationEventFilterTypeDef",
    "OrganizationEventTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TimestampTypeDef",
)

class AccountEntityAggregateTypeDef(TypedDict):
    accountId: NotRequired[str]
    count: NotRequired[int]
    statuses: NotRequired[Dict[EntityStatusCodeType, int]]

class AffectedEntityTypeDef(TypedDict):
    entityArn: NotRequired[str]
    eventArn: NotRequired[str]
    entityValue: NotRequired[str]
    entityUrl: NotRequired[str]
    awsAccountId: NotRequired[str]
    lastUpdatedTime: NotRequired[datetime]
    statusCode: NotRequired[EntityStatusCodeType]
    tags: NotRequired[Dict[str, str]]
    entityMetadata: NotRequired[Dict[str, str]]

TimestampTypeDef = Union[datetime, str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeAffectedAccountsForOrganizationRequestRequestTypeDef(TypedDict):
    eventArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class EntityAccountFilterTypeDef(TypedDict):
    eventArn: str
    awsAccountId: NotRequired[str]
    statusCodes: NotRequired[Sequence[EntityStatusCodeType]]

class EventAccountFilterTypeDef(TypedDict):
    eventArn: str
    awsAccountId: NotRequired[str]

class OrganizationAffectedEntitiesErrorItemTypeDef(TypedDict):
    awsAccountId: NotRequired[str]
    eventArn: NotRequired[str]
    errorName: NotRequired[str]
    errorMessage: NotRequired[str]

class DescribeEntityAggregatesForOrganizationRequestRequestTypeDef(TypedDict):
    eventArns: Sequence[str]
    awsAccountIds: NotRequired[Sequence[str]]

class DescribeEntityAggregatesRequestRequestTypeDef(TypedDict):
    eventArns: NotRequired[Sequence[str]]

class EntityAggregateTypeDef(TypedDict):
    eventArn: NotRequired[str]
    count: NotRequired[int]
    statuses: NotRequired[Dict[EntityStatusCodeType, int]]

class EventAggregateTypeDef(TypedDict):
    aggregateValue: NotRequired[str]
    count: NotRequired[int]

class OrganizationEventDetailsErrorItemTypeDef(TypedDict):
    awsAccountId: NotRequired[str]
    eventArn: NotRequired[str]
    errorName: NotRequired[str]
    errorMessage: NotRequired[str]

class DescribeEventDetailsRequestRequestTypeDef(TypedDict):
    eventArns: Sequence[str]
    locale: NotRequired[str]

class EventDetailsErrorItemTypeDef(TypedDict):
    eventArn: NotRequired[str]
    errorName: NotRequired[str]
    errorMessage: NotRequired[str]

class EventTypeFilterTypeDef(TypedDict):
    eventTypeCodes: NotRequired[Sequence[str]]
    services: NotRequired[Sequence[str]]
    eventTypeCategories: NotRequired[Sequence[EventTypeCategoryType]]

class EventTypeTypeDef(TypedDict):
    service: NotRequired[str]
    code: NotRequired[str]
    category: NotRequired[EventTypeCategoryType]

class OrganizationEventTypeDef(TypedDict):
    arn: NotRequired[str]
    service: NotRequired[str]
    eventTypeCode: NotRequired[str]
    eventTypeCategory: NotRequired[EventTypeCategoryType]
    eventScopeCode: NotRequired[EventScopeCodeType]
    region: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    lastUpdatedTime: NotRequired[datetime]
    statusCode: NotRequired[EventStatusCodeType]

class EventTypeDef(TypedDict):
    arn: NotRequired[str]
    service: NotRequired[str]
    eventTypeCode: NotRequired[str]
    eventTypeCategory: NotRequired[EventTypeCategoryType]
    region: NotRequired[str]
    availabilityZone: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    lastUpdatedTime: NotRequired[datetime]
    statusCode: NotRequired[EventStatusCodeType]
    eventScopeCode: NotRequired[EventScopeCodeType]

class EventDescriptionTypeDef(TypedDict):
    latestDescription: NotRequired[str]

class OrganizationEntityAggregateTypeDef(TypedDict):
    eventArn: NotRequired[str]
    count: NotRequired[int]
    statuses: NotRequired[Dict[EntityStatusCodeType, int]]
    accounts: NotRequired[List[AccountEntityAggregateTypeDef]]

DateTimeRangeTypeDef = TypedDict(
    "DateTimeRangeTypeDef",
    {
        "from": NotRequired[TimestampTypeDef],
        "to": NotRequired[TimestampTypeDef],
    },
)

class DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef(
    TypedDict
):
    eventArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeAffectedAccountsForOrganizationResponseTypeDef(TypedDict):
    affectedAccounts: List[str]
    eventScopeCode: EventScopeCodeType
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeAffectedEntitiesResponseTypeDef(TypedDict):
    entities: List[AffectedEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeHealthServiceStatusForOrganizationResponseTypeDef(TypedDict):
    healthServiceAccessStatusForOrganization: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef(
    TypedDict
):
    organizationEntityFilters: NotRequired[Sequence[EventAccountFilterTypeDef]]
    locale: NotRequired[str]
    organizationEntityAccountFilters: NotRequired[Sequence[EntityAccountFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeAffectedEntitiesForOrganizationRequestRequestTypeDef(TypedDict):
    organizationEntityFilters: NotRequired[Sequence[EventAccountFilterTypeDef]]
    locale: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    organizationEntityAccountFilters: NotRequired[Sequence[EntityAccountFilterTypeDef]]

class DescribeEventDetailsForOrganizationRequestRequestTypeDef(TypedDict):
    organizationEventDetailFilters: Sequence[EventAccountFilterTypeDef]
    locale: NotRequired[str]

class DescribeAffectedEntitiesForOrganizationResponseTypeDef(TypedDict):
    entities: List[AffectedEntityTypeDef]
    failedSet: List[OrganizationAffectedEntitiesErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeEntityAggregatesResponseTypeDef(TypedDict):
    entityAggregates: List[EntityAggregateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEventAggregatesResponseTypeDef(TypedDict):
    eventAggregates: List[EventAggregateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef = TypedDict(
    "DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef",
    {
        "filter": NotRequired[EventTypeFilterTypeDef],
        "locale": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeEventTypesRequestRequestTypeDef = TypedDict(
    "DescribeEventTypesRequestRequestTypeDef",
    {
        "filter": NotRequired[EventTypeFilterTypeDef],
        "locale": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class DescribeEventTypesResponseTypeDef(TypedDict):
    eventTypes: List[EventTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeEventsForOrganizationResponseTypeDef(TypedDict):
    events: List[OrganizationEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeEventsResponseTypeDef(TypedDict):
    events: List[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EventDetailsTypeDef(TypedDict):
    event: NotRequired[EventTypeDef]
    eventDescription: NotRequired[EventDescriptionTypeDef]
    eventMetadata: NotRequired[Dict[str, str]]

class OrganizationEventDetailsTypeDef(TypedDict):
    awsAccountId: NotRequired[str]
    event: NotRequired[EventTypeDef]
    eventDescription: NotRequired[EventDescriptionTypeDef]
    eventMetadata: NotRequired[Dict[str, str]]

class DescribeEntityAggregatesForOrganizationResponseTypeDef(TypedDict):
    organizationEntityAggregates: List[OrganizationEntityAggregateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class EntityFilterTypeDef(TypedDict):
    eventArns: Sequence[str]
    entityArns: NotRequired[Sequence[str]]
    entityValues: NotRequired[Sequence[str]]
    lastUpdatedTimes: NotRequired[Sequence[DateTimeRangeTypeDef]]
    tags: NotRequired[Sequence[Mapping[str, str]]]
    statusCodes: NotRequired[Sequence[EntityStatusCodeType]]

class EventFilterTypeDef(TypedDict):
    eventArns: NotRequired[Sequence[str]]
    eventTypeCodes: NotRequired[Sequence[str]]
    services: NotRequired[Sequence[str]]
    regions: NotRequired[Sequence[str]]
    availabilityZones: NotRequired[Sequence[str]]
    startTimes: NotRequired[Sequence[DateTimeRangeTypeDef]]
    endTimes: NotRequired[Sequence[DateTimeRangeTypeDef]]
    lastUpdatedTimes: NotRequired[Sequence[DateTimeRangeTypeDef]]
    entityArns: NotRequired[Sequence[str]]
    entityValues: NotRequired[Sequence[str]]
    eventTypeCategories: NotRequired[Sequence[EventTypeCategoryType]]
    tags: NotRequired[Sequence[Mapping[str, str]]]
    eventStatusCodes: NotRequired[Sequence[EventStatusCodeType]]

class OrganizationEventFilterTypeDef(TypedDict):
    eventTypeCodes: NotRequired[Sequence[str]]
    awsAccountIds: NotRequired[Sequence[str]]
    services: NotRequired[Sequence[str]]
    regions: NotRequired[Sequence[str]]
    startTime: NotRequired[DateTimeRangeTypeDef]
    endTime: NotRequired[DateTimeRangeTypeDef]
    lastUpdatedTime: NotRequired[DateTimeRangeTypeDef]
    entityArns: NotRequired[Sequence[str]]
    entityValues: NotRequired[Sequence[str]]
    eventTypeCategories: NotRequired[Sequence[EventTypeCategoryType]]
    eventStatusCodes: NotRequired[Sequence[EventStatusCodeType]]

class DescribeEventDetailsResponseTypeDef(TypedDict):
    successfulSet: List[EventDetailsTypeDef]
    failedSet: List[EventDetailsErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEventDetailsForOrganizationResponseTypeDef(TypedDict):
    successfulSet: List[OrganizationEventDetailsTypeDef]
    failedSet: List[OrganizationEventDetailsErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef = TypedDict(
    "DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef",
    {
        "filter": EntityFilterTypeDef,
        "locale": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeAffectedEntitiesRequestRequestTypeDef = TypedDict(
    "DescribeAffectedEntitiesRequestRequestTypeDef",
    {
        "filter": EntityFilterTypeDef,
        "locale": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef = TypedDict(
    "DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef",
    {
        "aggregateField": Literal["eventTypeCategory"],
        "filter": NotRequired[EventFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeEventAggregatesRequestRequestTypeDef = TypedDict(
    "DescribeEventAggregatesRequestRequestTypeDef",
    {
        "aggregateField": Literal["eventTypeCategory"],
        "filter": NotRequired[EventFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
DescribeEventsRequestDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    {
        "filter": NotRequired[EventFilterTypeDef],
        "locale": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeEventsRequestRequestTypeDef = TypedDict(
    "DescribeEventsRequestRequestTypeDef",
    {
        "filter": NotRequired[EventFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "locale": NotRequired[str],
    },
)
DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef = TypedDict(
    "DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef",
    {
        "filter": NotRequired[OrganizationEventFilterTypeDef],
        "locale": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeEventsForOrganizationRequestRequestTypeDef = TypedDict(
    "DescribeEventsForOrganizationRequestRequestTypeDef",
    {
        "filter": NotRequired[OrganizationEventFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "locale": NotRequired[str],
    },
)
