"""
Type annotations for shield service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/type_defs/)

Usage::

    ```python
    from mypy_boto3_shield.type_defs import ResponseActionOutputTypeDef

    data: ResponseActionOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ApplicationLayerAutomaticResponseStatusType,
    AttackLayerType,
    AttackPropertyIdentifierType,
    AutoRenewType,
    ProactiveEngagementStatusType,
    ProtectedResourceTypeType,
    ProtectionGroupAggregationType,
    ProtectionGroupPatternType,
    SubResourceTypeType,
    SubscriptionStateType,
    UnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ApplicationLayerAutomaticResponseConfigurationTypeDef",
    "AssociateDRTLogBucketRequestRequestTypeDef",
    "AssociateDRTRoleRequestRequestTypeDef",
    "AssociateHealthCheckRequestRequestTypeDef",
    "AssociateProactiveEngagementDetailsRequestRequestTypeDef",
    "AttackDetailTypeDef",
    "AttackPropertyTypeDef",
    "AttackStatisticsDataItemTypeDef",
    "AttackSummaryTypeDef",
    "AttackVectorDescriptionTypeDef",
    "AttackVolumeStatisticsTypeDef",
    "AttackVolumeTypeDef",
    "ContributorTypeDef",
    "CreateProtectionGroupRequestRequestTypeDef",
    "CreateProtectionRequestRequestTypeDef",
    "CreateProtectionResponseTypeDef",
    "DeleteProtectionGroupRequestRequestTypeDef",
    "DeleteProtectionRequestRequestTypeDef",
    "DescribeAttackRequestRequestTypeDef",
    "DescribeAttackResponseTypeDef",
    "DescribeAttackStatisticsResponseTypeDef",
    "DescribeDRTAccessResponseTypeDef",
    "DescribeEmergencyContactSettingsResponseTypeDef",
    "DescribeProtectionGroupRequestRequestTypeDef",
    "DescribeProtectionGroupResponseTypeDef",
    "DescribeProtectionRequestRequestTypeDef",
    "DescribeProtectionResponseTypeDef",
    "DescribeSubscriptionResponseTypeDef",
    "DisableApplicationLayerAutomaticResponseRequestRequestTypeDef",
    "DisassociateDRTLogBucketRequestRequestTypeDef",
    "DisassociateHealthCheckRequestRequestTypeDef",
    "EmergencyContactTypeDef",
    "EnableApplicationLayerAutomaticResponseRequestRequestTypeDef",
    "GetSubscriptionStateResponseTypeDef",
    "InclusionProtectionFiltersTypeDef",
    "InclusionProtectionGroupFiltersTypeDef",
    "LimitTypeDef",
    "ListAttacksRequestListAttacksPaginateTypeDef",
    "ListAttacksRequestRequestTypeDef",
    "ListAttacksResponseTypeDef",
    "ListProtectionGroupsRequestRequestTypeDef",
    "ListProtectionGroupsResponseTypeDef",
    "ListProtectionsRequestListProtectionsPaginateTypeDef",
    "ListProtectionsRequestRequestTypeDef",
    "ListProtectionsResponseTypeDef",
    "ListResourcesInProtectionGroupRequestRequestTypeDef",
    "ListResourcesInProtectionGroupResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MitigationTypeDef",
    "PaginatorConfigTypeDef",
    "ProtectionGroupArbitraryPatternLimitsTypeDef",
    "ProtectionGroupLimitsTypeDef",
    "ProtectionGroupPatternTypeLimitsTypeDef",
    "ProtectionGroupTypeDef",
    "ProtectionLimitsTypeDef",
    "ProtectionTypeDef",
    "ResponseActionOutputTypeDef",
    "ResponseActionTypeDef",
    "ResponseMetadataTypeDef",
    "SubResourceSummaryTypeDef",
    "SubscriptionLimitsTypeDef",
    "SubscriptionTypeDef",
    "SummarizedAttackVectorTypeDef",
    "SummarizedCounterTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimeRangeOutputTypeDef",
    "TimeRangeTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationLayerAutomaticResponseRequestRequestTypeDef",
    "UpdateEmergencyContactSettingsRequestRequestTypeDef",
    "UpdateProtectionGroupRequestRequestTypeDef",
    "UpdateSubscriptionRequestRequestTypeDef",
)


class ResponseActionOutputTypeDef(TypedDict):
    Block: NotRequired[Dict[str, Any]]
    Count: NotRequired[Dict[str, Any]]


class AssociateDRTLogBucketRequestRequestTypeDef(TypedDict):
    LogBucket: str


class AssociateDRTRoleRequestRequestTypeDef(TypedDict):
    RoleArn: str


class AssociateHealthCheckRequestRequestTypeDef(TypedDict):
    ProtectionId: str
    HealthCheckArn: str


class EmergencyContactTypeDef(TypedDict):
    EmailAddress: str
    PhoneNumber: NotRequired[str]
    ContactNotes: NotRequired[str]


class MitigationTypeDef(TypedDict):
    MitigationName: NotRequired[str]


class SummarizedCounterTypeDef(TypedDict):
    Name: NotRequired[str]
    Max: NotRequired[float]
    Average: NotRequired[float]
    Sum: NotRequired[float]
    N: NotRequired[int]
    Unit: NotRequired[str]


class ContributorTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[int]


class AttackVectorDescriptionTypeDef(TypedDict):
    VectorType: str


class AttackVolumeStatisticsTypeDef(TypedDict):
    Max: float


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteProtectionGroupRequestRequestTypeDef(TypedDict):
    ProtectionGroupId: str


class DeleteProtectionRequestRequestTypeDef(TypedDict):
    ProtectionId: str


class DescribeAttackRequestRequestTypeDef(TypedDict):
    AttackId: str


class TimeRangeOutputTypeDef(TypedDict):
    FromInclusive: NotRequired[datetime]
    ToExclusive: NotRequired[datetime]


class DescribeProtectionGroupRequestRequestTypeDef(TypedDict):
    ProtectionGroupId: str


class ProtectionGroupTypeDef(TypedDict):
    ProtectionGroupId: str
    Aggregation: ProtectionGroupAggregationType
    Pattern: ProtectionGroupPatternType
    Members: List[str]
    ResourceType: NotRequired[ProtectedResourceTypeType]
    ProtectionGroupArn: NotRequired[str]


class DescribeProtectionRequestRequestTypeDef(TypedDict):
    ProtectionId: NotRequired[str]
    ResourceArn: NotRequired[str]


class DisableApplicationLayerAutomaticResponseRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class DisassociateDRTLogBucketRequestRequestTypeDef(TypedDict):
    LogBucket: str


class DisassociateHealthCheckRequestRequestTypeDef(TypedDict):
    ProtectionId: str
    HealthCheckArn: str


class ResponseActionTypeDef(TypedDict):
    Block: NotRequired[Mapping[str, Any]]
    Count: NotRequired[Mapping[str, Any]]


class InclusionProtectionFiltersTypeDef(TypedDict):
    ResourceArns: NotRequired[Sequence[str]]
    ProtectionNames: NotRequired[Sequence[str]]
    ResourceTypes: NotRequired[Sequence[ProtectedResourceTypeType]]


class InclusionProtectionGroupFiltersTypeDef(TypedDict):
    ProtectionGroupIds: NotRequired[Sequence[str]]
    Patterns: NotRequired[Sequence[ProtectionGroupPatternType]]
    ResourceTypes: NotRequired[Sequence[ProtectedResourceTypeType]]
    Aggregations: NotRequired[Sequence[ProtectionGroupAggregationType]]


LimitTypeDef = TypedDict(
    "LimitTypeDef",
    {
        "Type": NotRequired[str],
        "Max": NotRequired[int],
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListResourcesInProtectionGroupRequestRequestTypeDef(TypedDict):
    ProtectionGroupId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class ProtectionGroupArbitraryPatternLimitsTypeDef(TypedDict):
    MaxMembers: int


TimestampTypeDef = Union[datetime, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateProtectionGroupRequestRequestTypeDef(TypedDict):
    ProtectionGroupId: str
    Aggregation: ProtectionGroupAggregationType
    Pattern: ProtectionGroupPatternType
    ResourceType: NotRequired[ProtectedResourceTypeType]
    Members: NotRequired[Sequence[str]]


class UpdateSubscriptionRequestRequestTypeDef(TypedDict):
    AutoRenew: NotRequired[AutoRenewType]


class ApplicationLayerAutomaticResponseConfigurationTypeDef(TypedDict):
    Status: ApplicationLayerAutomaticResponseStatusType
    Action: ResponseActionOutputTypeDef


class AssociateProactiveEngagementDetailsRequestRequestTypeDef(TypedDict):
    EmergencyContactList: Sequence[EmergencyContactTypeDef]


class UpdateEmergencyContactSettingsRequestRequestTypeDef(TypedDict):
    EmergencyContactList: NotRequired[Sequence[EmergencyContactTypeDef]]


class SummarizedAttackVectorTypeDef(TypedDict):
    VectorType: str
    VectorCounters: NotRequired[List[SummarizedCounterTypeDef]]


class AttackPropertyTypeDef(TypedDict):
    AttackLayer: NotRequired[AttackLayerType]
    AttackPropertyIdentifier: NotRequired[AttackPropertyIdentifierType]
    TopContributors: NotRequired[List[ContributorTypeDef]]
    Unit: NotRequired[UnitType]
    Total: NotRequired[int]


class AttackSummaryTypeDef(TypedDict):
    AttackId: NotRequired[str]
    ResourceArn: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    AttackVectors: NotRequired[List[AttackVectorDescriptionTypeDef]]


class AttackVolumeTypeDef(TypedDict):
    BitsPerSecond: NotRequired[AttackVolumeStatisticsTypeDef]
    PacketsPerSecond: NotRequired[AttackVolumeStatisticsTypeDef]
    RequestsPerSecond: NotRequired[AttackVolumeStatisticsTypeDef]


class CreateProtectionGroupRequestRequestTypeDef(TypedDict):
    ProtectionGroupId: str
    Aggregation: ProtectionGroupAggregationType
    Pattern: ProtectionGroupPatternType
    ResourceType: NotRequired[ProtectedResourceTypeType]
    Members: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateProtectionRequestRequestTypeDef(TypedDict):
    Name: str
    ResourceArn: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateProtectionResponseTypeDef(TypedDict):
    ProtectionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDRTAccessResponseTypeDef(TypedDict):
    RoleArn: str
    LogBucketList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEmergencyContactSettingsResponseTypeDef(TypedDict):
    EmergencyContactList: List[EmergencyContactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetSubscriptionStateResponseTypeDef(TypedDict):
    SubscriptionState: SubscriptionStateType
    ResponseMetadata: ResponseMetadataTypeDef


class ListResourcesInProtectionGroupResponseTypeDef(TypedDict):
    ResourceArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProtectionGroupResponseTypeDef(TypedDict):
    ProtectionGroup: ProtectionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListProtectionGroupsResponseTypeDef(TypedDict):
    ProtectionGroups: List[ProtectionGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EnableApplicationLayerAutomaticResponseRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Action: ResponseActionTypeDef


class UpdateApplicationLayerAutomaticResponseRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Action: ResponseActionTypeDef


class ListProtectionsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    InclusionFilters: NotRequired[InclusionProtectionFiltersTypeDef]


class ListProtectionGroupsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    InclusionFilters: NotRequired[InclusionProtectionGroupFiltersTypeDef]


class ProtectionLimitsTypeDef(TypedDict):
    ProtectedResourceTypeLimits: List[LimitTypeDef]


class ListProtectionsRequestListProtectionsPaginateTypeDef(TypedDict):
    InclusionFilters: NotRequired[InclusionProtectionFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ProtectionGroupPatternTypeLimitsTypeDef(TypedDict):
    ArbitraryPatternLimits: ProtectionGroupArbitraryPatternLimitsTypeDef


class TimeRangeTypeDef(TypedDict):
    FromInclusive: NotRequired[TimestampTypeDef]
    ToExclusive: NotRequired[TimestampTypeDef]


class ProtectionTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    ResourceArn: NotRequired[str]
    HealthCheckIds: NotRequired[List[str]]
    ProtectionArn: NotRequired[str]
    ApplicationLayerAutomaticResponseConfiguration: NotRequired[
        ApplicationLayerAutomaticResponseConfigurationTypeDef
    ]


SubResourceSummaryTypeDef = TypedDict(
    "SubResourceSummaryTypeDef",
    {
        "Type": NotRequired[SubResourceTypeType],
        "Id": NotRequired[str],
        "AttackVectors": NotRequired[List[SummarizedAttackVectorTypeDef]],
        "Counters": NotRequired[List[SummarizedCounterTypeDef]],
    },
)


class ListAttacksResponseTypeDef(TypedDict):
    AttackSummaries: List[AttackSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AttackStatisticsDataItemTypeDef(TypedDict):
    AttackCount: int
    AttackVolume: NotRequired[AttackVolumeTypeDef]


class ProtectionGroupLimitsTypeDef(TypedDict):
    MaxProtectionGroups: int
    PatternTypeLimits: ProtectionGroupPatternTypeLimitsTypeDef


class ListAttacksRequestListAttacksPaginateTypeDef(TypedDict):
    ResourceArns: NotRequired[Sequence[str]]
    StartTime: NotRequired[TimeRangeTypeDef]
    EndTime: NotRequired[TimeRangeTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAttacksRequestRequestTypeDef(TypedDict):
    ResourceArns: NotRequired[Sequence[str]]
    StartTime: NotRequired[TimeRangeTypeDef]
    EndTime: NotRequired[TimeRangeTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeProtectionResponseTypeDef(TypedDict):
    Protection: ProtectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListProtectionsResponseTypeDef(TypedDict):
    Protections: List[ProtectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AttackDetailTypeDef(TypedDict):
    AttackId: NotRequired[str]
    ResourceArn: NotRequired[str]
    SubResources: NotRequired[List[SubResourceSummaryTypeDef]]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    AttackCounters: NotRequired[List[SummarizedCounterTypeDef]]
    AttackProperties: NotRequired[List[AttackPropertyTypeDef]]
    Mitigations: NotRequired[List[MitigationTypeDef]]


class DescribeAttackStatisticsResponseTypeDef(TypedDict):
    TimeRange: TimeRangeOutputTypeDef
    DataItems: List[AttackStatisticsDataItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SubscriptionLimitsTypeDef(TypedDict):
    ProtectionLimits: ProtectionLimitsTypeDef
    ProtectionGroupLimits: ProtectionGroupLimitsTypeDef


class DescribeAttackResponseTypeDef(TypedDict):
    Attack: AttackDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SubscriptionTypeDef(TypedDict):
    SubscriptionLimits: SubscriptionLimitsTypeDef
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    TimeCommitmentInSeconds: NotRequired[int]
    AutoRenew: NotRequired[AutoRenewType]
    Limits: NotRequired[List[LimitTypeDef]]
    ProactiveEngagementStatus: NotRequired[ProactiveEngagementStatusType]
    SubscriptionArn: NotRequired[str]


class DescribeSubscriptionResponseTypeDef(TypedDict):
    Subscription: SubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
