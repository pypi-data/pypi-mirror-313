"""
Type annotations for security-ir service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_security_ir/type_defs/)

Usage::

    ```python
    from mypy_boto3_security_ir.type_defs import BatchGetMemberAccountDetailsRequestRequestTypeDef

    data: BatchGetMemberAccountDetailsRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AwsRegionType,
    CaseAttachmentStatusType,
    CaseStatusType,
    ClosureCodeType,
    CustomerTypeType,
    EngagementTypeType,
    MembershipAccountRelationshipStatusType,
    MembershipStatusType,
    PendingActionType,
    ResolverTypeType,
    SelfManagedCaseStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "BatchGetMemberAccountDetailsRequestRequestTypeDef",
    "BatchGetMemberAccountDetailsResponseTypeDef",
    "CancelMembershipRequestRequestTypeDef",
    "CancelMembershipResponseTypeDef",
    "CaseAttachmentAttributesTypeDef",
    "CaseEditItemTypeDef",
    "CloseCaseRequestRequestTypeDef",
    "CloseCaseResponseTypeDef",
    "CreateCaseCommentRequestRequestTypeDef",
    "CreateCaseCommentResponseTypeDef",
    "CreateCaseRequestRequestTypeDef",
    "CreateCaseResponseTypeDef",
    "CreateMembershipRequestRequestTypeDef",
    "CreateMembershipResponseTypeDef",
    "GetCaseAttachmentDownloadUrlRequestRequestTypeDef",
    "GetCaseAttachmentDownloadUrlResponseTypeDef",
    "GetCaseAttachmentUploadUrlRequestRequestTypeDef",
    "GetCaseAttachmentUploadUrlResponseTypeDef",
    "GetCaseRequestRequestTypeDef",
    "GetCaseResponseTypeDef",
    "GetMembershipAccountDetailErrorTypeDef",
    "GetMembershipAccountDetailItemTypeDef",
    "GetMembershipRequestRequestTypeDef",
    "GetMembershipResponseTypeDef",
    "ImpactedAwsRegionTypeDef",
    "IncidentResponderTypeDef",
    "ListCaseEditsRequestListCaseEditsPaginateTypeDef",
    "ListCaseEditsRequestRequestTypeDef",
    "ListCaseEditsResponseTypeDef",
    "ListCasesItemTypeDef",
    "ListCasesRequestListCasesPaginateTypeDef",
    "ListCasesRequestRequestTypeDef",
    "ListCasesResponseTypeDef",
    "ListCommentsItemTypeDef",
    "ListCommentsRequestListCommentsPaginateTypeDef",
    "ListCommentsRequestRequestTypeDef",
    "ListCommentsResponseTypeDef",
    "ListMembershipItemTypeDef",
    "ListMembershipsRequestListMembershipsPaginateTypeDef",
    "ListMembershipsRequestRequestTypeDef",
    "ListMembershipsResponseTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "OptInFeatureTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputRequestTypeDef",
    "ThreatActorIpTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateCaseCommentRequestRequestTypeDef",
    "UpdateCaseCommentResponseTypeDef",
    "UpdateCaseRequestRequestTypeDef",
    "UpdateCaseStatusRequestRequestTypeDef",
    "UpdateCaseStatusResponseTypeDef",
    "UpdateMembershipRequestRequestTypeDef",
    "UpdateResolverTypeRequestRequestTypeDef",
    "UpdateResolverTypeResponseTypeDef",
    "WatcherTypeDef",
)


class BatchGetMemberAccountDetailsRequestRequestTypeDef(TypedDict):
    membershipId: str
    accountIds: Sequence[str]


class GetMembershipAccountDetailErrorTypeDef(TypedDict):
    accountId: str
    error: str
    message: str


class GetMembershipAccountDetailItemTypeDef(TypedDict):
    accountId: NotRequired[str]
    relationshipStatus: NotRequired[MembershipAccountRelationshipStatusType]
    relationshipType: NotRequired[Literal["Organization"]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CancelMembershipRequestRequestTypeDef(TypedDict):
    membershipId: str


class CaseAttachmentAttributesTypeDef(TypedDict):
    attachmentId: str
    fileName: str
    attachmentStatus: CaseAttachmentStatusType
    creator: str
    createdDate: datetime


class CaseEditItemTypeDef(TypedDict):
    eventTimestamp: NotRequired[datetime]
    principal: NotRequired[str]
    action: NotRequired[str]
    message: NotRequired[str]


class CloseCaseRequestRequestTypeDef(TypedDict):
    caseId: str


class CreateCaseCommentRequestRequestTypeDef(TypedDict):
    caseId: str
    body: str
    clientToken: NotRequired[str]


class ImpactedAwsRegionTypeDef(TypedDict):
    region: AwsRegionType


class ThreatActorIpTypeDef(TypedDict):
    ipAddress: str
    userAgent: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class WatcherTypeDef(TypedDict):
    email: str
    name: NotRequired[str]
    jobTitle: NotRequired[str]


class IncidentResponderTypeDef(TypedDict):
    name: str
    jobTitle: str
    email: str


class OptInFeatureTypeDef(TypedDict):
    featureName: Literal["Triage"]
    isEnabled: bool


class GetCaseAttachmentDownloadUrlRequestRequestTypeDef(TypedDict):
    caseId: str
    attachmentId: str


class GetCaseAttachmentUploadUrlRequestRequestTypeDef(TypedDict):
    caseId: str
    fileName: str
    contentLength: int
    clientToken: NotRequired[str]


class GetCaseRequestRequestTypeDef(TypedDict):
    caseId: str


class GetMembershipRequestRequestTypeDef(TypedDict):
    membershipId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListCaseEditsRequestRequestTypeDef(TypedDict):
    caseId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListCasesItemTypeDef(TypedDict):
    caseId: str
    lastUpdatedDate: NotRequired[datetime]
    title: NotRequired[str]
    caseArn: NotRequired[str]
    engagementType: NotRequired[EngagementTypeType]
    caseStatus: NotRequired[CaseStatusType]
    createdDate: NotRequired[datetime]
    closedDate: NotRequired[datetime]
    resolverType: NotRequired[ResolverTypeType]
    pendingAction: NotRequired[PendingActionType]


class ListCasesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListCommentsItemTypeDef(TypedDict):
    commentId: str
    createdDate: NotRequired[datetime]
    lastUpdatedDate: NotRequired[datetime]
    creator: NotRequired[str]
    lastUpdatedBy: NotRequired[str]
    body: NotRequired[str]


class ListCommentsRequestRequestTypeDef(TypedDict):
    caseId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListMembershipItemTypeDef(TypedDict):
    membershipId: str
    accountId: NotRequired[str]
    region: NotRequired[AwsRegionType]
    membershipArn: NotRequired[str]
    membershipStatus: NotRequired[MembershipStatusType]


class ListMembershipsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateCaseCommentRequestRequestTypeDef(TypedDict):
    caseId: str
    commentId: str
    body: str


class UpdateCaseStatusRequestRequestTypeDef(TypedDict):
    caseId: str
    caseStatus: SelfManagedCaseStatusType


class UpdateResolverTypeRequestRequestTypeDef(TypedDict):
    caseId: str
    resolverType: ResolverTypeType


class BatchGetMemberAccountDetailsResponseTypeDef(TypedDict):
    items: List[GetMembershipAccountDetailItemTypeDef]
    errors: List[GetMembershipAccountDetailErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CancelMembershipResponseTypeDef(TypedDict):
    membershipId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CloseCaseResponseTypeDef(TypedDict):
    caseStatus: CaseStatusType
    closedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCaseCommentResponseTypeDef(TypedDict):
    commentId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCaseResponseTypeDef(TypedDict):
    caseId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMembershipResponseTypeDef(TypedDict):
    membershipId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCaseAttachmentDownloadUrlResponseTypeDef(TypedDict):
    attachmentPresignedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCaseAttachmentUploadUrlResponseTypeDef(TypedDict):
    attachmentPresignedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCaseCommentResponseTypeDef(TypedDict):
    commentId: str
    body: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCaseStatusResponseTypeDef(TypedDict):
    caseStatus: SelfManagedCaseStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateResolverTypeResponseTypeDef(TypedDict):
    caseId: str
    caseStatus: CaseStatusType
    resolverType: ResolverTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class ListCaseEditsResponseTypeDef(TypedDict):
    items: List[CaseEditItemTypeDef]
    total: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateCaseRequestRequestTypeDef(TypedDict):
    resolverType: ResolverTypeType
    title: str
    description: str
    engagementType: EngagementTypeType
    reportedIncidentStartDate: TimestampTypeDef
    impactedAccounts: Sequence[str]
    watchers: Sequence[WatcherTypeDef]
    clientToken: NotRequired[str]
    threatActorIpAddresses: NotRequired[Sequence[ThreatActorIpTypeDef]]
    impactedServices: NotRequired[Sequence[str]]
    impactedAwsRegions: NotRequired[Sequence[ImpactedAwsRegionTypeDef]]
    tags: NotRequired[Mapping[str, str]]


class GetCaseResponseTypeDef(TypedDict):
    title: str
    caseArn: str
    description: str
    caseStatus: CaseStatusType
    engagementType: EngagementTypeType
    reportedIncidentStartDate: datetime
    actualIncidentStartDate: datetime
    impactedAwsRegions: List[ImpactedAwsRegionTypeDef]
    threatActorIpAddresses: List[ThreatActorIpTypeDef]
    pendingAction: PendingActionType
    impactedAccounts: List[str]
    watchers: List[WatcherTypeDef]
    createdDate: datetime
    lastUpdatedDate: datetime
    closureCode: ClosureCodeType
    resolverType: ResolverTypeType
    impactedServices: List[str]
    caseAttachments: List[CaseAttachmentAttributesTypeDef]
    closedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCaseRequestRequestTypeDef(TypedDict):
    caseId: str
    title: NotRequired[str]
    description: NotRequired[str]
    reportedIncidentStartDate: NotRequired[TimestampTypeDef]
    actualIncidentStartDate: NotRequired[TimestampTypeDef]
    engagementType: NotRequired[EngagementTypeType]
    watchersToAdd: NotRequired[Sequence[WatcherTypeDef]]
    watchersToDelete: NotRequired[Sequence[WatcherTypeDef]]
    threatActorIpAddressesToAdd: NotRequired[Sequence[ThreatActorIpTypeDef]]
    threatActorIpAddressesToDelete: NotRequired[Sequence[ThreatActorIpTypeDef]]
    impactedServicesToAdd: NotRequired[Sequence[str]]
    impactedServicesToDelete: NotRequired[Sequence[str]]
    impactedAwsRegionsToAdd: NotRequired[Sequence[ImpactedAwsRegionTypeDef]]
    impactedAwsRegionsToDelete: NotRequired[Sequence[ImpactedAwsRegionTypeDef]]
    impactedAccountsToAdd: NotRequired[Sequence[str]]
    impactedAccountsToDelete: NotRequired[Sequence[str]]


class CreateMembershipRequestRequestTypeDef(TypedDict):
    membershipName: str
    incidentResponseTeam: Sequence[IncidentResponderTypeDef]
    clientToken: NotRequired[str]
    optInFeatures: NotRequired[Sequence[OptInFeatureTypeDef]]
    tags: NotRequired[Mapping[str, str]]


class GetMembershipResponseTypeDef(TypedDict):
    membershipId: str
    accountId: str
    region: AwsRegionType
    membershipName: str
    membershipArn: str
    membershipStatus: MembershipStatusType
    membershipActivationTimestamp: datetime
    membershipDeactivationTimestamp: datetime
    customerType: CustomerTypeType
    numberOfAccountsCovered: int
    incidentResponseTeam: List[IncidentResponderTypeDef]
    optInFeatures: List[OptInFeatureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMembershipRequestRequestTypeDef(TypedDict):
    membershipId: str
    membershipName: NotRequired[str]
    incidentResponseTeam: NotRequired[Sequence[IncidentResponderTypeDef]]
    optInFeatures: NotRequired[Sequence[OptInFeatureTypeDef]]


class ListCaseEditsRequestListCaseEditsPaginateTypeDef(TypedDict):
    caseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCasesRequestListCasesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCommentsRequestListCommentsPaginateTypeDef(TypedDict):
    caseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMembershipsRequestListMembershipsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCasesResponseTypeDef(TypedDict):
    items: List[ListCasesItemTypeDef]
    total: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListCommentsResponseTypeDef(TypedDict):
    items: List[ListCommentsItemTypeDef]
    total: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMembershipsResponseTypeDef(TypedDict):
    items: List[ListMembershipItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
