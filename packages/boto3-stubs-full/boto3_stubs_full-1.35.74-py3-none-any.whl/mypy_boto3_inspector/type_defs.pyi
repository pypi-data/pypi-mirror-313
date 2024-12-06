"""
Type annotations for inspector service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/type_defs/)

Usage::

    ```python
    from mypy_boto3_inspector.type_defs import AttributeTypeDef

    data: AttributeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AgentHealthCodeType,
    AgentHealthType,
    AssessmentRunNotificationSnsStatusCodeType,
    AssessmentRunStateType,
    FailedItemErrorCodeType,
    InspectorEventType,
    PreviewStatusType,
    ReportFileFormatType,
    ReportStatusType,
    ReportTypeType,
    ScopeTypeType,
    SeverityType,
    StopActionType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddAttributesToFindingsRequestRequestTypeDef",
    "AddAttributesToFindingsResponseTypeDef",
    "AgentFilterTypeDef",
    "AgentPreviewTypeDef",
    "AssessmentRunAgentTypeDef",
    "AssessmentRunFilterTypeDef",
    "AssessmentRunNotificationTypeDef",
    "AssessmentRunStateChangeTypeDef",
    "AssessmentRunTypeDef",
    "AssessmentTargetFilterTypeDef",
    "AssessmentTargetTypeDef",
    "AssessmentTemplateFilterTypeDef",
    "AssessmentTemplateTypeDef",
    "AssetAttributesTypeDef",
    "AttributeTypeDef",
    "CreateAssessmentTargetRequestRequestTypeDef",
    "CreateAssessmentTargetResponseTypeDef",
    "CreateAssessmentTemplateRequestRequestTypeDef",
    "CreateAssessmentTemplateResponseTypeDef",
    "CreateExclusionsPreviewRequestRequestTypeDef",
    "CreateExclusionsPreviewResponseTypeDef",
    "CreateResourceGroupRequestRequestTypeDef",
    "CreateResourceGroupResponseTypeDef",
    "DeleteAssessmentRunRequestRequestTypeDef",
    "DeleteAssessmentTargetRequestRequestTypeDef",
    "DeleteAssessmentTemplateRequestRequestTypeDef",
    "DescribeAssessmentRunsRequestRequestTypeDef",
    "DescribeAssessmentRunsResponseTypeDef",
    "DescribeAssessmentTargetsRequestRequestTypeDef",
    "DescribeAssessmentTargetsResponseTypeDef",
    "DescribeAssessmentTemplatesRequestRequestTypeDef",
    "DescribeAssessmentTemplatesResponseTypeDef",
    "DescribeCrossAccountAccessRoleResponseTypeDef",
    "DescribeExclusionsRequestRequestTypeDef",
    "DescribeExclusionsResponseTypeDef",
    "DescribeFindingsRequestRequestTypeDef",
    "DescribeFindingsResponseTypeDef",
    "DescribeResourceGroupsRequestRequestTypeDef",
    "DescribeResourceGroupsResponseTypeDef",
    "DescribeRulesPackagesRequestRequestTypeDef",
    "DescribeRulesPackagesResponseTypeDef",
    "DurationRangeTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventSubscriptionTypeDef",
    "ExclusionPreviewTypeDef",
    "ExclusionTypeDef",
    "FailedItemDetailsTypeDef",
    "FindingFilterTypeDef",
    "FindingTypeDef",
    "GetAssessmentReportRequestRequestTypeDef",
    "GetAssessmentReportResponseTypeDef",
    "GetExclusionsPreviewRequestRequestTypeDef",
    "GetExclusionsPreviewResponseTypeDef",
    "GetTelemetryMetadataRequestRequestTypeDef",
    "GetTelemetryMetadataResponseTypeDef",
    "InspectorServiceAttributesTypeDef",
    "ListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef",
    "ListAssessmentRunAgentsRequestRequestTypeDef",
    "ListAssessmentRunAgentsResponseTypeDef",
    "ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef",
    "ListAssessmentRunsRequestRequestTypeDef",
    "ListAssessmentRunsResponseTypeDef",
    "ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef",
    "ListAssessmentTargetsRequestRequestTypeDef",
    "ListAssessmentTargetsResponseTypeDef",
    "ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef",
    "ListAssessmentTemplatesRequestRequestTypeDef",
    "ListAssessmentTemplatesResponseTypeDef",
    "ListEventSubscriptionsRequestListEventSubscriptionsPaginateTypeDef",
    "ListEventSubscriptionsRequestRequestTypeDef",
    "ListEventSubscriptionsResponseTypeDef",
    "ListExclusionsRequestListExclusionsPaginateTypeDef",
    "ListExclusionsRequestRequestTypeDef",
    "ListExclusionsResponseTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "ListFindingsResponseTypeDef",
    "ListRulesPackagesRequestListRulesPackagesPaginateTypeDef",
    "ListRulesPackagesRequestRequestTypeDef",
    "ListRulesPackagesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "PreviewAgentsRequestPreviewAgentsPaginateTypeDef",
    "PreviewAgentsRequestRequestTypeDef",
    "PreviewAgentsResponseTypeDef",
    "PrivateIpTypeDef",
    "RegisterCrossAccountAccessRoleRequestRequestTypeDef",
    "RemoveAttributesFromFindingsRequestRequestTypeDef",
    "RemoveAttributesFromFindingsResponseTypeDef",
    "ResourceGroupTagTypeDef",
    "ResourceGroupTypeDef",
    "ResponseMetadataTypeDef",
    "RulesPackageTypeDef",
    "ScopeTypeDef",
    "SecurityGroupTypeDef",
    "SetTagsForResourceRequestRequestTypeDef",
    "StartAssessmentRunRequestRequestTypeDef",
    "StartAssessmentRunResponseTypeDef",
    "StopAssessmentRunRequestRequestTypeDef",
    "SubscribeToEventRequestRequestTypeDef",
    "SubscriptionTypeDef",
    "TagTypeDef",
    "TelemetryMetadataTypeDef",
    "TimestampRangeTypeDef",
    "TimestampTypeDef",
    "UnsubscribeFromEventRequestRequestTypeDef",
    "UpdateAssessmentTargetRequestRequestTypeDef",
)

class AttributeTypeDef(TypedDict):
    key: str
    value: NotRequired[str]

class FailedItemDetailsTypeDef(TypedDict):
    failureCode: FailedItemErrorCodeType
    retryable: bool

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AgentFilterTypeDef(TypedDict):
    agentHealths: Sequence[AgentHealthType]
    agentHealthCodes: Sequence[AgentHealthCodeType]

class AgentPreviewTypeDef(TypedDict):
    agentId: str
    hostname: NotRequired[str]
    autoScalingGroup: NotRequired[str]
    agentHealth: NotRequired[AgentHealthType]
    agentVersion: NotRequired[str]
    operatingSystem: NotRequired[str]
    kernelVersion: NotRequired[str]
    ipv4Address: NotRequired[str]

class TelemetryMetadataTypeDef(TypedDict):
    messageType: str
    count: int
    dataSize: NotRequired[int]

class DurationRangeTypeDef(TypedDict):
    minSeconds: NotRequired[int]
    maxSeconds: NotRequired[int]

class AssessmentRunNotificationTypeDef(TypedDict):
    date: datetime
    event: InspectorEventType
    error: bool
    message: NotRequired[str]
    snsTopicArn: NotRequired[str]
    snsPublishStatusCode: NotRequired[AssessmentRunNotificationSnsStatusCodeType]

class AssessmentRunStateChangeTypeDef(TypedDict):
    stateChangedAt: datetime
    state: AssessmentRunStateType

class AssessmentTargetFilterTypeDef(TypedDict):
    assessmentTargetNamePattern: NotRequired[str]

class AssessmentTargetTypeDef(TypedDict):
    arn: str
    name: str
    createdAt: datetime
    updatedAt: datetime
    resourceGroupArn: NotRequired[str]

class TagTypeDef(TypedDict):
    key: str
    value: NotRequired[str]

class CreateAssessmentTargetRequestRequestTypeDef(TypedDict):
    assessmentTargetName: str
    resourceGroupArn: NotRequired[str]

class CreateExclusionsPreviewRequestRequestTypeDef(TypedDict):
    assessmentTemplateArn: str

class ResourceGroupTagTypeDef(TypedDict):
    key: str
    value: NotRequired[str]

class DeleteAssessmentRunRequestRequestTypeDef(TypedDict):
    assessmentRunArn: str

class DeleteAssessmentTargetRequestRequestTypeDef(TypedDict):
    assessmentTargetArn: str

class DeleteAssessmentTemplateRequestRequestTypeDef(TypedDict):
    assessmentTemplateArn: str

class DescribeAssessmentRunsRequestRequestTypeDef(TypedDict):
    assessmentRunArns: Sequence[str]

class DescribeAssessmentTargetsRequestRequestTypeDef(TypedDict):
    assessmentTargetArns: Sequence[str]

class DescribeAssessmentTemplatesRequestRequestTypeDef(TypedDict):
    assessmentTemplateArns: Sequence[str]

class DescribeExclusionsRequestRequestTypeDef(TypedDict):
    exclusionArns: Sequence[str]
    locale: NotRequired[Literal["EN_US"]]

class DescribeFindingsRequestRequestTypeDef(TypedDict):
    findingArns: Sequence[str]
    locale: NotRequired[Literal["EN_US"]]

class DescribeResourceGroupsRequestRequestTypeDef(TypedDict):
    resourceGroupArns: Sequence[str]

class DescribeRulesPackagesRequestRequestTypeDef(TypedDict):
    rulesPackageArns: Sequence[str]
    locale: NotRequired[Literal["EN_US"]]

class RulesPackageTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    provider: str
    description: NotRequired[str]

class EventSubscriptionTypeDef(TypedDict):
    event: InspectorEventType
    subscribedAt: datetime

class ScopeTypeDef(TypedDict):
    key: NotRequired[ScopeTypeType]
    value: NotRequired[str]

class InspectorServiceAttributesTypeDef(TypedDict):
    schemaVersion: int
    assessmentRunArn: NotRequired[str]
    rulesPackageArn: NotRequired[str]

class GetAssessmentReportRequestRequestTypeDef(TypedDict):
    assessmentRunArn: str
    reportFileFormat: ReportFileFormatType
    reportType: ReportTypeType

class GetExclusionsPreviewRequestRequestTypeDef(TypedDict):
    assessmentTemplateArn: str
    previewToken: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    locale: NotRequired[Literal["EN_US"]]

class GetTelemetryMetadataRequestRequestTypeDef(TypedDict):
    assessmentRunArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListEventSubscriptionsRequestRequestTypeDef(TypedDict):
    resourceArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListExclusionsRequestRequestTypeDef(TypedDict):
    assessmentRunArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListRulesPackagesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class PrivateIpTypeDef(TypedDict):
    privateDnsName: NotRequired[str]
    privateIpAddress: NotRequired[str]

class SecurityGroupTypeDef(TypedDict):
    groupName: NotRequired[str]
    groupId: NotRequired[str]

class PreviewAgentsRequestRequestTypeDef(TypedDict):
    previewAgentsArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class RegisterCrossAccountAccessRoleRequestRequestTypeDef(TypedDict):
    roleArn: str

class RemoveAttributesFromFindingsRequestRequestTypeDef(TypedDict):
    findingArns: Sequence[str]
    attributeKeys: Sequence[str]

class StartAssessmentRunRequestRequestTypeDef(TypedDict):
    assessmentTemplateArn: str
    assessmentRunName: NotRequired[str]

class StopAssessmentRunRequestRequestTypeDef(TypedDict):
    assessmentRunArn: str
    stopAction: NotRequired[StopActionType]

class SubscribeToEventRequestRequestTypeDef(TypedDict):
    resourceArn: str
    event: InspectorEventType
    topicArn: str

TimestampTypeDef = Union[datetime, str]

class UnsubscribeFromEventRequestRequestTypeDef(TypedDict):
    resourceArn: str
    event: InspectorEventType
    topicArn: str

class UpdateAssessmentTargetRequestRequestTypeDef(TypedDict):
    assessmentTargetArn: str
    assessmentTargetName: str
    resourceGroupArn: NotRequired[str]

class AddAttributesToFindingsRequestRequestTypeDef(TypedDict):
    findingArns: Sequence[str]
    attributes: Sequence[AttributeTypeDef]

class AssessmentTemplateTypeDef(TypedDict):
    arn: str
    name: str
    assessmentTargetArn: str
    durationInSeconds: int
    rulesPackageArns: List[str]
    userAttributesForFindings: List[AttributeTypeDef]
    assessmentRunCount: int
    createdAt: datetime
    lastAssessmentRunArn: NotRequired[str]

class CreateAssessmentTemplateRequestRequestTypeDef(TypedDict):
    assessmentTargetArn: str
    assessmentTemplateName: str
    durationInSeconds: int
    rulesPackageArns: Sequence[str]
    userAttributesForFindings: NotRequired[Sequence[AttributeTypeDef]]

class AddAttributesToFindingsResponseTypeDef(TypedDict):
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAssessmentTargetResponseTypeDef(TypedDict):
    assessmentTargetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAssessmentTemplateResponseTypeDef(TypedDict):
    assessmentTemplateArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateExclusionsPreviewResponseTypeDef(TypedDict):
    previewToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourceGroupResponseTypeDef(TypedDict):
    resourceGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCrossAccountAccessRoleResponseTypeDef(TypedDict):
    roleArn: str
    valid: bool
    registeredAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAssessmentReportResponseTypeDef(TypedDict):
    status: ReportStatusType
    url: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssessmentRunsResponseTypeDef(TypedDict):
    assessmentRunArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssessmentTargetsResponseTypeDef(TypedDict):
    assessmentTargetArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssessmentTemplatesResponseTypeDef(TypedDict):
    assessmentTemplateArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListExclusionsResponseTypeDef(TypedDict):
    exclusionArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFindingsResponseTypeDef(TypedDict):
    findingArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRulesPackagesResponseTypeDef(TypedDict):
    rulesPackageArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RemoveAttributesFromFindingsResponseTypeDef(TypedDict):
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartAssessmentRunResponseTypeDef(TypedDict):
    assessmentRunArn: str
    ResponseMetadata: ResponseMetadataTypeDef

ListAssessmentRunAgentsRequestRequestTypeDef = TypedDict(
    "ListAssessmentRunAgentsRequestRequestTypeDef",
    {
        "assessmentRunArn": str,
        "filter": NotRequired[AgentFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class PreviewAgentsResponseTypeDef(TypedDict):
    agentPreviews: List[AgentPreviewTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AssessmentRunAgentTypeDef(TypedDict):
    agentId: str
    assessmentRunArn: str
    agentHealth: AgentHealthType
    agentHealthCode: AgentHealthCodeType
    telemetryMetadata: List[TelemetryMetadataTypeDef]
    agentHealthDetails: NotRequired[str]
    autoScalingGroup: NotRequired[str]

class GetTelemetryMetadataResponseTypeDef(TypedDict):
    telemetryMetadata: List[TelemetryMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AssessmentTemplateFilterTypeDef(TypedDict):
    namePattern: NotRequired[str]
    durationRange: NotRequired[DurationRangeTypeDef]
    rulesPackageArns: NotRequired[Sequence[str]]

class AssessmentRunTypeDef(TypedDict):
    arn: str
    name: str
    assessmentTemplateArn: str
    state: AssessmentRunStateType
    durationInSeconds: int
    rulesPackageArns: List[str]
    userAttributesForFindings: List[AttributeTypeDef]
    createdAt: datetime
    stateChangedAt: datetime
    dataCollected: bool
    stateChanges: List[AssessmentRunStateChangeTypeDef]
    notifications: List[AssessmentRunNotificationTypeDef]
    findingCounts: Dict[SeverityType, int]
    startedAt: NotRequired[datetime]
    completedAt: NotRequired[datetime]

ListAssessmentTargetsRequestRequestTypeDef = TypedDict(
    "ListAssessmentTargetsRequestRequestTypeDef",
    {
        "filter": NotRequired[AssessmentTargetFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class DescribeAssessmentTargetsResponseTypeDef(TypedDict):
    assessmentTargets: List[AssessmentTargetTypeDef]
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SetTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateResourceGroupRequestRequestTypeDef(TypedDict):
    resourceGroupTags: Sequence[ResourceGroupTagTypeDef]

class ResourceGroupTypeDef(TypedDict):
    arn: str
    tags: List[ResourceGroupTagTypeDef]
    createdAt: datetime

class DescribeRulesPackagesResponseTypeDef(TypedDict):
    rulesPackages: List[RulesPackageTypeDef]
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SubscriptionTypeDef(TypedDict):
    resourceArn: str
    topicArn: str
    eventSubscriptions: List[EventSubscriptionTypeDef]

class ExclusionPreviewTypeDef(TypedDict):
    title: str
    description: str
    recommendation: str
    scopes: List[ScopeTypeDef]
    attributes: NotRequired[List[AttributeTypeDef]]

class ExclusionTypeDef(TypedDict):
    arn: str
    title: str
    description: str
    recommendation: str
    scopes: List[ScopeTypeDef]
    attributes: NotRequired[List[AttributeTypeDef]]

ListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef = TypedDict(
    "ListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef",
    {
        "assessmentRunArn": str,
        "filter": NotRequired[AgentFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef = TypedDict(
    "ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef",
    {
        "filter": NotRequired[AssessmentTargetFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListEventSubscriptionsRequestListEventSubscriptionsPaginateTypeDef(TypedDict):
    resourceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListExclusionsRequestListExclusionsPaginateTypeDef(TypedDict):
    assessmentRunArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesPackagesRequestListRulesPackagesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class PreviewAgentsRequestPreviewAgentsPaginateTypeDef(TypedDict):
    previewAgentsArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class NetworkInterfaceTypeDef(TypedDict):
    networkInterfaceId: NotRequired[str]
    subnetId: NotRequired[str]
    vpcId: NotRequired[str]
    privateDnsName: NotRequired[str]
    privateIpAddress: NotRequired[str]
    privateIpAddresses: NotRequired[List[PrivateIpTypeDef]]
    publicDnsName: NotRequired[str]
    publicIp: NotRequired[str]
    ipv6Addresses: NotRequired[List[str]]
    securityGroups: NotRequired[List[SecurityGroupTypeDef]]

class TimestampRangeTypeDef(TypedDict):
    beginDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]

class DescribeAssessmentTemplatesResponseTypeDef(TypedDict):
    assessmentTemplates: List[AssessmentTemplateTypeDef]
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssessmentRunAgentsResponseTypeDef(TypedDict):
    assessmentRunAgents: List[AssessmentRunAgentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef = TypedDict(
    "ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef",
    {
        "assessmentTargetArns": NotRequired[Sequence[str]],
        "filter": NotRequired[AssessmentTemplateFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAssessmentTemplatesRequestRequestTypeDef = TypedDict(
    "ListAssessmentTemplatesRequestRequestTypeDef",
    {
        "assessmentTargetArns": NotRequired[Sequence[str]],
        "filter": NotRequired[AssessmentTemplateFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class DescribeAssessmentRunsResponseTypeDef(TypedDict):
    assessmentRuns: List[AssessmentRunTypeDef]
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeResourceGroupsResponseTypeDef(TypedDict):
    resourceGroups: List[ResourceGroupTypeDef]
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListEventSubscriptionsResponseTypeDef(TypedDict):
    subscriptions: List[SubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetExclusionsPreviewResponseTypeDef(TypedDict):
    previewStatus: PreviewStatusType
    exclusionPreviews: List[ExclusionPreviewTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeExclusionsResponseTypeDef(TypedDict):
    exclusions: Dict[str, ExclusionTypeDef]
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AssetAttributesTypeDef(TypedDict):
    schemaVersion: int
    agentId: NotRequired[str]
    autoScalingGroup: NotRequired[str]
    amiId: NotRequired[str]
    hostname: NotRequired[str]
    ipv4Addresses: NotRequired[List[str]]
    tags: NotRequired[List[TagTypeDef]]
    networkInterfaces: NotRequired[List[NetworkInterfaceTypeDef]]

class AssessmentRunFilterTypeDef(TypedDict):
    namePattern: NotRequired[str]
    states: NotRequired[Sequence[AssessmentRunStateType]]
    durationRange: NotRequired[DurationRangeTypeDef]
    rulesPackageArns: NotRequired[Sequence[str]]
    startTimeRange: NotRequired[TimestampRangeTypeDef]
    completionTimeRange: NotRequired[TimestampRangeTypeDef]
    stateChangeTimeRange: NotRequired[TimestampRangeTypeDef]

class FindingFilterTypeDef(TypedDict):
    agentIds: NotRequired[Sequence[str]]
    autoScalingGroups: NotRequired[Sequence[str]]
    ruleNames: NotRequired[Sequence[str]]
    severities: NotRequired[Sequence[SeverityType]]
    rulesPackageArns: NotRequired[Sequence[str]]
    attributes: NotRequired[Sequence[AttributeTypeDef]]
    userAttributes: NotRequired[Sequence[AttributeTypeDef]]
    creationTimeRange: NotRequired[TimestampRangeTypeDef]

FindingTypeDef = TypedDict(
    "FindingTypeDef",
    {
        "arn": str,
        "attributes": List[AttributeTypeDef],
        "userAttributes": List[AttributeTypeDef],
        "createdAt": datetime,
        "updatedAt": datetime,
        "schemaVersion": NotRequired[int],
        "service": NotRequired[str],
        "serviceAttributes": NotRequired[InspectorServiceAttributesTypeDef],
        "assetType": NotRequired[Literal["ec2-instance"]],
        "assetAttributes": NotRequired[AssetAttributesTypeDef],
        "id": NotRequired[str],
        "title": NotRequired[str],
        "description": NotRequired[str],
        "recommendation": NotRequired[str],
        "severity": NotRequired[SeverityType],
        "numericSeverity": NotRequired[float],
        "confidence": NotRequired[int],
        "indicatorOfCompromise": NotRequired[bool],
    },
)
ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef = TypedDict(
    "ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef",
    {
        "assessmentTemplateArns": NotRequired[Sequence[str]],
        "filter": NotRequired[AssessmentRunFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAssessmentRunsRequestRequestTypeDef = TypedDict(
    "ListAssessmentRunsRequestRequestTypeDef",
    {
        "assessmentTemplateArns": NotRequired[Sequence[str]],
        "filter": NotRequired[AssessmentRunFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "ListFindingsRequestListFindingsPaginateTypeDef",
    {
        "assessmentRunArns": NotRequired[Sequence[str]],
        "filter": NotRequired[FindingFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFindingsRequestRequestTypeDef = TypedDict(
    "ListFindingsRequestRequestTypeDef",
    {
        "assessmentRunArns": NotRequired[Sequence[str]],
        "filter": NotRequired[FindingFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class DescribeFindingsResponseTypeDef(TypedDict):
    findings: List[FindingTypeDef]
    failedItems: Dict[str, FailedItemDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
