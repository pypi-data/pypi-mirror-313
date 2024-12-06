"""
Type annotations for ssm-incidents service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm_incidents.type_defs import AddRegionActionTypeDef

    data: AddRegionActionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    IncidentRecordStatusType,
    ItemTypeType,
    RegionStatusType,
    ReplicationSetStatusType,
    SortOrderType,
    SsmTargetAccountType,
    VariableTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActionOutputTypeDef",
    "ActionTypeDef",
    "ActionUnionTypeDef",
    "AddRegionActionTypeDef",
    "AttributeValueListTypeDef",
    "AutomationExecutionTypeDef",
    "BatchGetIncidentFindingsErrorTypeDef",
    "BatchGetIncidentFindingsInputRequestTypeDef",
    "BatchGetIncidentFindingsOutputTypeDef",
    "ChatChannelOutputTypeDef",
    "ChatChannelTypeDef",
    "CloudFormationStackUpdateTypeDef",
    "CodeDeployDeploymentTypeDef",
    "ConditionTypeDef",
    "CreateReplicationSetInputRequestTypeDef",
    "CreateReplicationSetOutputTypeDef",
    "CreateResponsePlanInputRequestTypeDef",
    "CreateResponsePlanOutputTypeDef",
    "CreateTimelineEventInputRequestTypeDef",
    "CreateTimelineEventOutputTypeDef",
    "DeleteIncidentRecordInputRequestTypeDef",
    "DeleteRegionActionTypeDef",
    "DeleteReplicationSetInputRequestTypeDef",
    "DeleteResourcePolicyInputRequestTypeDef",
    "DeleteResponsePlanInputRequestTypeDef",
    "DeleteTimelineEventInputRequestTypeDef",
    "DynamicSsmParameterValueTypeDef",
    "EventReferenceTypeDef",
    "EventSummaryTypeDef",
    "FilterTypeDef",
    "FindingDetailsTypeDef",
    "FindingSummaryTypeDef",
    "FindingTypeDef",
    "GetIncidentRecordInputRequestTypeDef",
    "GetIncidentRecordOutputTypeDef",
    "GetReplicationSetInputRequestTypeDef",
    "GetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef",
    "GetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef",
    "GetReplicationSetOutputTypeDef",
    "GetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef",
    "GetResourcePoliciesInputRequestTypeDef",
    "GetResourcePoliciesOutputTypeDef",
    "GetResponsePlanInputRequestTypeDef",
    "GetResponsePlanOutputTypeDef",
    "GetTimelineEventInputRequestTypeDef",
    "GetTimelineEventOutputTypeDef",
    "IncidentRecordSourceTypeDef",
    "IncidentRecordSummaryTypeDef",
    "IncidentRecordTypeDef",
    "IncidentTemplateOutputTypeDef",
    "IncidentTemplateTypeDef",
    "IntegrationTypeDef",
    "ItemIdentifierTypeDef",
    "ItemValueTypeDef",
    "ListIncidentFindingsInputListIncidentFindingsPaginateTypeDef",
    "ListIncidentFindingsInputRequestTypeDef",
    "ListIncidentFindingsOutputTypeDef",
    "ListIncidentRecordsInputListIncidentRecordsPaginateTypeDef",
    "ListIncidentRecordsInputRequestTypeDef",
    "ListIncidentRecordsOutputTypeDef",
    "ListRelatedItemsInputListRelatedItemsPaginateTypeDef",
    "ListRelatedItemsInputRequestTypeDef",
    "ListRelatedItemsOutputTypeDef",
    "ListReplicationSetsInputListReplicationSetsPaginateTypeDef",
    "ListReplicationSetsInputRequestTypeDef",
    "ListReplicationSetsOutputTypeDef",
    "ListResponsePlansInputListResponsePlansPaginateTypeDef",
    "ListResponsePlansInputRequestTypeDef",
    "ListResponsePlansOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTimelineEventsInputListTimelineEventsPaginateTypeDef",
    "ListTimelineEventsInputRequestTypeDef",
    "ListTimelineEventsOutputTypeDef",
    "NotificationTargetItemTypeDef",
    "PagerDutyConfigurationTypeDef",
    "PagerDutyIncidentConfigurationTypeDef",
    "PagerDutyIncidentDetailTypeDef",
    "PaginatorConfigTypeDef",
    "PutResourcePolicyInputRequestTypeDef",
    "PutResourcePolicyOutputTypeDef",
    "RegionInfoTypeDef",
    "RegionMapInputValueTypeDef",
    "RelatedItemTypeDef",
    "RelatedItemsUpdateTypeDef",
    "ReplicationSetTypeDef",
    "ResourcePolicyTypeDef",
    "ResponseMetadataTypeDef",
    "ResponsePlanSummaryTypeDef",
    "SsmAutomationOutputTypeDef",
    "SsmAutomationTypeDef",
    "SsmAutomationUnionTypeDef",
    "StartIncidentInputRequestTypeDef",
    "StartIncidentOutputTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimelineEventTypeDef",
    "TimestampTypeDef",
    "TriggerDetailsTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDeletionProtectionInputRequestTypeDef",
    "UpdateIncidentRecordInputRequestTypeDef",
    "UpdateRelatedItemsInputRequestTypeDef",
    "UpdateReplicationSetActionTypeDef",
    "UpdateReplicationSetInputRequestTypeDef",
    "UpdateResponsePlanInputRequestTypeDef",
    "UpdateTimelineEventInputRequestTypeDef",
    "WaiterConfigTypeDef",
)


class AddRegionActionTypeDef(TypedDict):
    regionName: str
    sseKmsKeyId: NotRequired[str]


class AttributeValueListTypeDef(TypedDict):
    integerValues: NotRequired[Sequence[int]]
    stringValues: NotRequired[Sequence[str]]


class AutomationExecutionTypeDef(TypedDict):
    ssmExecutionArn: NotRequired[str]


class BatchGetIncidentFindingsErrorTypeDef(TypedDict):
    code: str
    findingId: str
    message: str


class BatchGetIncidentFindingsInputRequestTypeDef(TypedDict):
    findingIds: Sequence[str]
    incidentRecordArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ChatChannelOutputTypeDef(TypedDict):
    chatbotSns: NotRequired[List[str]]
    empty: NotRequired[Dict[str, Any]]


class ChatChannelTypeDef(TypedDict):
    chatbotSns: NotRequired[Sequence[str]]
    empty: NotRequired[Mapping[str, Any]]


class CloudFormationStackUpdateTypeDef(TypedDict):
    stackArn: str
    startTime: datetime
    endTime: NotRequired[datetime]


class CodeDeployDeploymentTypeDef(TypedDict):
    deploymentGroupArn: str
    deploymentId: str
    startTime: datetime
    endTime: NotRequired[datetime]


TimestampTypeDef = Union[datetime, str]


class RegionMapInputValueTypeDef(TypedDict):
    sseKmsKeyId: NotRequired[str]


class EventReferenceTypeDef(TypedDict):
    relatedItemId: NotRequired[str]
    resource: NotRequired[str]


class DeleteIncidentRecordInputRequestTypeDef(TypedDict):
    arn: str


class DeleteRegionActionTypeDef(TypedDict):
    regionName: str


class DeleteReplicationSetInputRequestTypeDef(TypedDict):
    arn: str


class DeleteResourcePolicyInputRequestTypeDef(TypedDict):
    policyId: str
    resourceArn: str


class DeleteResponsePlanInputRequestTypeDef(TypedDict):
    arn: str


class DeleteTimelineEventInputRequestTypeDef(TypedDict):
    eventId: str
    incidentRecordArn: str


class DynamicSsmParameterValueTypeDef(TypedDict):
    variable: NotRequired[VariableTypeType]


FindingSummaryTypeDef = TypedDict(
    "FindingSummaryTypeDef",
    {
        "id": str,
        "lastModifiedTime": datetime,
    },
)


class GetIncidentRecordInputRequestTypeDef(TypedDict):
    arn: str


class GetReplicationSetInputRequestTypeDef(TypedDict):
    arn: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetResourcePoliciesInputRequestTypeDef(TypedDict):
    resourceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ResourcePolicyTypeDef(TypedDict):
    policyDocument: str
    policyId: str
    ramResourceShareRegion: str


class GetResponsePlanInputRequestTypeDef(TypedDict):
    arn: str


class GetTimelineEventInputRequestTypeDef(TypedDict):
    eventId: str
    incidentRecordArn: str


class IncidentRecordSourceTypeDef(TypedDict):
    createdBy: str
    source: str
    invokedBy: NotRequired[str]
    resourceArn: NotRequired[str]


class NotificationTargetItemTypeDef(TypedDict):
    snsTopicArn: NotRequired[str]


PagerDutyIncidentDetailTypeDef = TypedDict(
    "PagerDutyIncidentDetailTypeDef",
    {
        "id": str,
        "autoResolve": NotRequired[bool],
        "secretId": NotRequired[str],
    },
)


class ListIncidentFindingsInputRequestTypeDef(TypedDict):
    incidentRecordArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListRelatedItemsInputRequestTypeDef(TypedDict):
    incidentRecordArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListReplicationSetsInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListResponsePlansInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ResponsePlanSummaryTypeDef(TypedDict):
    arn: str
    name: str
    displayName: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class PagerDutyIncidentConfigurationTypeDef(TypedDict):
    serviceId: str


class PutResourcePolicyInputRequestTypeDef(TypedDict):
    policy: str
    resourceArn: str


class RegionInfoTypeDef(TypedDict):
    status: RegionStatusType
    statusUpdateDateTime: datetime
    sseKmsKeyId: NotRequired[str]
    statusMessage: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateDeletionProtectionInputRequestTypeDef(TypedDict):
    arn: str
    deletionProtected: bool
    clientToken: NotRequired[str]


class CreateReplicationSetOutputTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateResponsePlanOutputTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTimelineEventOutputTypeDef(TypedDict):
    eventId: str
    incidentRecordArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListReplicationSetsOutputTypeDef(TypedDict):
    replicationSetArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourcePolicyOutputTypeDef(TypedDict):
    policyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartIncidentOutputTypeDef(TypedDict):
    incidentRecordArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class FindingDetailsTypeDef(TypedDict):
    cloudFormationStackUpdate: NotRequired[CloudFormationStackUpdateTypeDef]
    codeDeployDeployment: NotRequired[CodeDeployDeploymentTypeDef]


class ConditionTypeDef(TypedDict):
    after: NotRequired[TimestampTypeDef]
    before: NotRequired[TimestampTypeDef]
    equals: NotRequired[AttributeValueListTypeDef]


class TriggerDetailsTypeDef(TypedDict):
    source: str
    timestamp: TimestampTypeDef
    rawData: NotRequired[str]
    triggerArn: NotRequired[str]


class CreateReplicationSetInputRequestTypeDef(TypedDict):
    regions: Mapping[str, RegionMapInputValueTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateTimelineEventInputRequestTypeDef(TypedDict):
    eventData: str
    eventTime: TimestampTypeDef
    eventType: str
    incidentRecordArn: str
    clientToken: NotRequired[str]
    eventReferences: NotRequired[Sequence[EventReferenceTypeDef]]


class EventSummaryTypeDef(TypedDict):
    eventId: str
    eventTime: datetime
    eventType: str
    eventUpdatedTime: datetime
    incidentRecordArn: str
    eventReferences: NotRequired[List[EventReferenceTypeDef]]


class TimelineEventTypeDef(TypedDict):
    eventData: str
    eventId: str
    eventTime: datetime
    eventType: str
    eventUpdatedTime: datetime
    incidentRecordArn: str
    eventReferences: NotRequired[List[EventReferenceTypeDef]]


class UpdateTimelineEventInputRequestTypeDef(TypedDict):
    eventId: str
    incidentRecordArn: str
    clientToken: NotRequired[str]
    eventData: NotRequired[str]
    eventReferences: NotRequired[Sequence[EventReferenceTypeDef]]
    eventTime: NotRequired[TimestampTypeDef]
    eventType: NotRequired[str]


class UpdateReplicationSetActionTypeDef(TypedDict):
    addRegionAction: NotRequired[AddRegionActionTypeDef]
    deleteRegionAction: NotRequired[DeleteRegionActionTypeDef]


class SsmAutomationOutputTypeDef(TypedDict):
    documentName: str
    roleArn: str
    documentVersion: NotRequired[str]
    dynamicParameters: NotRequired[Dict[str, DynamicSsmParameterValueTypeDef]]
    parameters: NotRequired[Dict[str, List[str]]]
    targetAccount: NotRequired[SsmTargetAccountType]


class SsmAutomationTypeDef(TypedDict):
    documentName: str
    roleArn: str
    documentVersion: NotRequired[str]
    dynamicParameters: NotRequired[Mapping[str, DynamicSsmParameterValueTypeDef]]
    parameters: NotRequired[Mapping[str, Sequence[str]]]
    targetAccount: NotRequired[SsmTargetAccountType]


class ListIncidentFindingsOutputTypeDef(TypedDict):
    findings: List[FindingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef(TypedDict):
    arn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef(TypedDict):
    arn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIncidentFindingsInputListIncidentFindingsPaginateTypeDef(TypedDict):
    incidentRecordArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRelatedItemsInputListRelatedItemsPaginateTypeDef(TypedDict):
    incidentRecordArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListReplicationSetsInputListReplicationSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResponsePlansInputListResponsePlansPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetResourcePoliciesOutputTypeDef(TypedDict):
    resourcePolicies: List[ResourcePolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class IncidentRecordSummaryTypeDef(TypedDict):
    arn: str
    creationTime: datetime
    impact: int
    incidentRecordSource: IncidentRecordSourceTypeDef
    status: IncidentRecordStatusType
    title: str
    resolvedTime: NotRequired[datetime]


class IncidentRecordTypeDef(TypedDict):
    arn: str
    creationTime: datetime
    dedupeString: str
    impact: int
    incidentRecordSource: IncidentRecordSourceTypeDef
    lastModifiedBy: str
    lastModifiedTime: datetime
    status: IncidentRecordStatusType
    title: str
    automationExecutions: NotRequired[List[AutomationExecutionTypeDef]]
    chatChannel: NotRequired[ChatChannelOutputTypeDef]
    notificationTargets: NotRequired[List[NotificationTargetItemTypeDef]]
    resolvedTime: NotRequired[datetime]
    summary: NotRequired[str]


class IncidentTemplateOutputTypeDef(TypedDict):
    impact: int
    title: str
    dedupeString: NotRequired[str]
    incidentTags: NotRequired[Dict[str, str]]
    notificationTargets: NotRequired[List[NotificationTargetItemTypeDef]]
    summary: NotRequired[str]


class IncidentTemplateTypeDef(TypedDict):
    impact: int
    title: str
    dedupeString: NotRequired[str]
    incidentTags: NotRequired[Mapping[str, str]]
    notificationTargets: NotRequired[Sequence[NotificationTargetItemTypeDef]]
    summary: NotRequired[str]


class UpdateIncidentRecordInputRequestTypeDef(TypedDict):
    arn: str
    chatChannel: NotRequired[ChatChannelTypeDef]
    clientToken: NotRequired[str]
    impact: NotRequired[int]
    notificationTargets: NotRequired[Sequence[NotificationTargetItemTypeDef]]
    status: NotRequired[IncidentRecordStatusType]
    summary: NotRequired[str]
    title: NotRequired[str]


class ItemValueTypeDef(TypedDict):
    arn: NotRequired[str]
    metricDefinition: NotRequired[str]
    pagerDutyIncidentDetail: NotRequired[PagerDutyIncidentDetailTypeDef]
    url: NotRequired[str]


class ListResponsePlansOutputTypeDef(TypedDict):
    responsePlanSummaries: List[ResponsePlanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PagerDutyConfigurationTypeDef(TypedDict):
    name: str
    pagerDutyIncidentConfiguration: PagerDutyIncidentConfigurationTypeDef
    secretId: str


class ReplicationSetTypeDef(TypedDict):
    createdBy: str
    createdTime: datetime
    deletionProtected: bool
    lastModifiedBy: str
    lastModifiedTime: datetime
    regionMap: Dict[str, RegionInfoTypeDef]
    status: ReplicationSetStatusType
    arn: NotRequired[str]


FindingTypeDef = TypedDict(
    "FindingTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "lastModifiedTime": datetime,
        "details": NotRequired[FindingDetailsTypeDef],
    },
)


class FilterTypeDef(TypedDict):
    condition: ConditionTypeDef
    key: str


class ListTimelineEventsOutputTypeDef(TypedDict):
    eventSummaries: List[EventSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetTimelineEventOutputTypeDef(TypedDict):
    event: TimelineEventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateReplicationSetInputRequestTypeDef(TypedDict):
    actions: Sequence[UpdateReplicationSetActionTypeDef]
    arn: str
    clientToken: NotRequired[str]


class ActionOutputTypeDef(TypedDict):
    ssmAutomation: NotRequired[SsmAutomationOutputTypeDef]


SsmAutomationUnionTypeDef = Union[SsmAutomationTypeDef, SsmAutomationOutputTypeDef]


class ListIncidentRecordsOutputTypeDef(TypedDict):
    incidentRecordSummaries: List[IncidentRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetIncidentRecordOutputTypeDef(TypedDict):
    incidentRecord: IncidentRecordTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ItemIdentifierTypeDef = TypedDict(
    "ItemIdentifierTypeDef",
    {
        "type": ItemTypeType,
        "value": ItemValueTypeDef,
    },
)


class IntegrationTypeDef(TypedDict):
    pagerDutyConfiguration: NotRequired[PagerDutyConfigurationTypeDef]


class GetReplicationSetOutputTypeDef(TypedDict):
    replicationSet: ReplicationSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetIncidentFindingsOutputTypeDef(TypedDict):
    errors: List[BatchGetIncidentFindingsErrorTypeDef]
    findings: List[FindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListIncidentRecordsInputListIncidentRecordsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIncidentRecordsInputRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTimelineEventsInputListTimelineEventsPaginateTypeDef(TypedDict):
    incidentRecordArn: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    sortBy: NotRequired[Literal["EVENT_TIME"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTimelineEventsInputRequestTypeDef(TypedDict):
    incidentRecordArn: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["EVENT_TIME"]]
    sortOrder: NotRequired[SortOrderType]


class ActionTypeDef(TypedDict):
    ssmAutomation: NotRequired[SsmAutomationUnionTypeDef]


class RelatedItemTypeDef(TypedDict):
    identifier: ItemIdentifierTypeDef
    generatedId: NotRequired[str]
    title: NotRequired[str]


class GetResponsePlanOutputTypeDef(TypedDict):
    actions: List[ActionOutputTypeDef]
    arn: str
    chatChannel: ChatChannelOutputTypeDef
    displayName: str
    engagements: List[str]
    incidentTemplate: IncidentTemplateOutputTypeDef
    integrations: List[IntegrationTypeDef]
    name: str
    ResponseMetadata: ResponseMetadataTypeDef


ActionUnionTypeDef = Union[ActionTypeDef, ActionOutputTypeDef]


class UpdateResponsePlanInputRequestTypeDef(TypedDict):
    arn: str
    actions: NotRequired[Sequence[ActionTypeDef]]
    chatChannel: NotRequired[ChatChannelTypeDef]
    clientToken: NotRequired[str]
    displayName: NotRequired[str]
    engagements: NotRequired[Sequence[str]]
    incidentTemplateDedupeString: NotRequired[str]
    incidentTemplateImpact: NotRequired[int]
    incidentTemplateNotificationTargets: NotRequired[Sequence[NotificationTargetItemTypeDef]]
    incidentTemplateSummary: NotRequired[str]
    incidentTemplateTags: NotRequired[Mapping[str, str]]
    incidentTemplateTitle: NotRequired[str]
    integrations: NotRequired[Sequence[IntegrationTypeDef]]


class ListRelatedItemsOutputTypeDef(TypedDict):
    relatedItems: List[RelatedItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RelatedItemsUpdateTypeDef(TypedDict):
    itemToAdd: NotRequired[RelatedItemTypeDef]
    itemToRemove: NotRequired[ItemIdentifierTypeDef]


class StartIncidentInputRequestTypeDef(TypedDict):
    responsePlanArn: str
    clientToken: NotRequired[str]
    impact: NotRequired[int]
    relatedItems: NotRequired[Sequence[RelatedItemTypeDef]]
    title: NotRequired[str]
    triggerDetails: NotRequired[TriggerDetailsTypeDef]


class CreateResponsePlanInputRequestTypeDef(TypedDict):
    incidentTemplate: IncidentTemplateTypeDef
    name: str
    actions: NotRequired[Sequence[ActionUnionTypeDef]]
    chatChannel: NotRequired[ChatChannelTypeDef]
    clientToken: NotRequired[str]
    displayName: NotRequired[str]
    engagements: NotRequired[Sequence[str]]
    integrations: NotRequired[Sequence[IntegrationTypeDef]]
    tags: NotRequired[Mapping[str, str]]


class UpdateRelatedItemsInputRequestTypeDef(TypedDict):
    incidentRecordArn: str
    relatedItemsUpdate: RelatedItemsUpdateTypeDef
    clientToken: NotRequired[str]
