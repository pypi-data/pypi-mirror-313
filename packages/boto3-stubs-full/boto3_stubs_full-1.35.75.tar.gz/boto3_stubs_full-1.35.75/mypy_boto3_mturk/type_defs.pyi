"""
Type annotations for mturk service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/type_defs/)

Usage::

    ```python
    from mypy_boto3_mturk.type_defs import AcceptQualificationRequestRequestRequestTypeDef

    data: AcceptQualificationRequestRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AssignmentStatusType,
    ComparatorType,
    EventTypeType,
    HITAccessActionsType,
    HITReviewStatusType,
    HITStatusType,
    NotificationTransportType,
    NotifyWorkersFailureCodeType,
    QualificationStatusType,
    QualificationTypeStatusType,
    ReviewableHITStatusType,
    ReviewActionStatusType,
    ReviewPolicyLevelType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AcceptQualificationRequestRequestRequestTypeDef",
    "ApproveAssignmentRequestRequestTypeDef",
    "AssignmentTypeDef",
    "AssociateQualificationWithWorkerRequestRequestTypeDef",
    "BonusPaymentTypeDef",
    "CreateAdditionalAssignmentsForHITRequestRequestTypeDef",
    "CreateHITRequestRequestTypeDef",
    "CreateHITResponseTypeDef",
    "CreateHITTypeRequestRequestTypeDef",
    "CreateHITTypeResponseTypeDef",
    "CreateHITWithHITTypeRequestRequestTypeDef",
    "CreateHITWithHITTypeResponseTypeDef",
    "CreateQualificationTypeRequestRequestTypeDef",
    "CreateQualificationTypeResponseTypeDef",
    "CreateWorkerBlockRequestRequestTypeDef",
    "DeleteHITRequestRequestTypeDef",
    "DeleteQualificationTypeRequestRequestTypeDef",
    "DeleteWorkerBlockRequestRequestTypeDef",
    "DisassociateQualificationFromWorkerRequestRequestTypeDef",
    "GetAccountBalanceResponseTypeDef",
    "GetAssignmentRequestRequestTypeDef",
    "GetAssignmentResponseTypeDef",
    "GetFileUploadURLRequestRequestTypeDef",
    "GetFileUploadURLResponseTypeDef",
    "GetHITRequestRequestTypeDef",
    "GetHITResponseTypeDef",
    "GetQualificationScoreRequestRequestTypeDef",
    "GetQualificationScoreResponseTypeDef",
    "GetQualificationTypeRequestRequestTypeDef",
    "GetQualificationTypeResponseTypeDef",
    "HITLayoutParameterTypeDef",
    "HITTypeDef",
    "ListAssignmentsForHITRequestListAssignmentsForHITPaginateTypeDef",
    "ListAssignmentsForHITRequestRequestTypeDef",
    "ListAssignmentsForHITResponseTypeDef",
    "ListBonusPaymentsRequestListBonusPaymentsPaginateTypeDef",
    "ListBonusPaymentsRequestRequestTypeDef",
    "ListBonusPaymentsResponseTypeDef",
    "ListHITsForQualificationTypeRequestListHITsForQualificationTypePaginateTypeDef",
    "ListHITsForQualificationTypeRequestRequestTypeDef",
    "ListHITsForQualificationTypeResponseTypeDef",
    "ListHITsRequestListHITsPaginateTypeDef",
    "ListHITsRequestRequestTypeDef",
    "ListHITsResponseTypeDef",
    "ListQualificationRequestsRequestListQualificationRequestsPaginateTypeDef",
    "ListQualificationRequestsRequestRequestTypeDef",
    "ListQualificationRequestsResponseTypeDef",
    "ListQualificationTypesRequestListQualificationTypesPaginateTypeDef",
    "ListQualificationTypesRequestRequestTypeDef",
    "ListQualificationTypesResponseTypeDef",
    "ListReviewPolicyResultsForHITRequestRequestTypeDef",
    "ListReviewPolicyResultsForHITResponseTypeDef",
    "ListReviewableHITsRequestListReviewableHITsPaginateTypeDef",
    "ListReviewableHITsRequestRequestTypeDef",
    "ListReviewableHITsResponseTypeDef",
    "ListWorkerBlocksRequestListWorkerBlocksPaginateTypeDef",
    "ListWorkerBlocksRequestRequestTypeDef",
    "ListWorkerBlocksResponseTypeDef",
    "ListWorkersWithQualificationTypeRequestListWorkersWithQualificationTypePaginateTypeDef",
    "ListWorkersWithQualificationTypeRequestRequestTypeDef",
    "ListWorkersWithQualificationTypeResponseTypeDef",
    "LocaleTypeDef",
    "NotificationSpecificationTypeDef",
    "NotifyWorkersFailureStatusTypeDef",
    "NotifyWorkersRequestRequestTypeDef",
    "NotifyWorkersResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterMapEntryOutputTypeDef",
    "ParameterMapEntryTypeDef",
    "ParameterMapEntryUnionTypeDef",
    "PolicyParameterOutputTypeDef",
    "PolicyParameterTypeDef",
    "PolicyParameterUnionTypeDef",
    "QualificationRequestTypeDef",
    "QualificationRequirementOutputTypeDef",
    "QualificationRequirementTypeDef",
    "QualificationRequirementUnionTypeDef",
    "QualificationTypeDef",
    "QualificationTypeTypeDef",
    "RejectAssignmentRequestRequestTypeDef",
    "RejectQualificationRequestRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ReviewActionDetailTypeDef",
    "ReviewPolicyOutputTypeDef",
    "ReviewPolicyTypeDef",
    "ReviewReportTypeDef",
    "ReviewResultDetailTypeDef",
    "SendBonusRequestRequestTypeDef",
    "SendTestEventNotificationRequestRequestTypeDef",
    "TimestampTypeDef",
    "UpdateExpirationForHITRequestRequestTypeDef",
    "UpdateHITReviewStatusRequestRequestTypeDef",
    "UpdateHITTypeOfHITRequestRequestTypeDef",
    "UpdateNotificationSettingsRequestRequestTypeDef",
    "UpdateQualificationTypeRequestRequestTypeDef",
    "UpdateQualificationTypeResponseTypeDef",
    "WorkerBlockTypeDef",
)

class AcceptQualificationRequestRequestRequestTypeDef(TypedDict):
    QualificationRequestId: str
    IntegerValue: NotRequired[int]

class ApproveAssignmentRequestRequestTypeDef(TypedDict):
    AssignmentId: str
    RequesterFeedback: NotRequired[str]
    OverrideRejection: NotRequired[bool]

class AssignmentTypeDef(TypedDict):
    AssignmentId: NotRequired[str]
    WorkerId: NotRequired[str]
    HITId: NotRequired[str]
    AssignmentStatus: NotRequired[AssignmentStatusType]
    AutoApprovalTime: NotRequired[datetime]
    AcceptTime: NotRequired[datetime]
    SubmitTime: NotRequired[datetime]
    ApprovalTime: NotRequired[datetime]
    RejectionTime: NotRequired[datetime]
    Deadline: NotRequired[datetime]
    Answer: NotRequired[str]
    RequesterFeedback: NotRequired[str]

class AssociateQualificationWithWorkerRequestRequestTypeDef(TypedDict):
    QualificationTypeId: str
    WorkerId: str
    IntegerValue: NotRequired[int]
    SendNotification: NotRequired[bool]

class BonusPaymentTypeDef(TypedDict):
    WorkerId: NotRequired[str]
    BonusAmount: NotRequired[str]
    AssignmentId: NotRequired[str]
    Reason: NotRequired[str]
    GrantTime: NotRequired[datetime]

class CreateAdditionalAssignmentsForHITRequestRequestTypeDef(TypedDict):
    HITId: str
    NumberOfAdditionalAssignments: int
    UniqueRequestToken: NotRequired[str]

class HITLayoutParameterTypeDef(TypedDict):
    Name: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateQualificationTypeRequestRequestTypeDef(TypedDict):
    Name: str
    Description: str
    QualificationTypeStatus: QualificationTypeStatusType
    Keywords: NotRequired[str]
    RetryDelayInSeconds: NotRequired[int]
    Test: NotRequired[str]
    AnswerKey: NotRequired[str]
    TestDurationInSeconds: NotRequired[int]
    AutoGranted: NotRequired[bool]
    AutoGrantedValue: NotRequired[int]

class QualificationTypeTypeDef(TypedDict):
    QualificationTypeId: NotRequired[str]
    CreationTime: NotRequired[datetime]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Keywords: NotRequired[str]
    QualificationTypeStatus: NotRequired[QualificationTypeStatusType]
    Test: NotRequired[str]
    TestDurationInSeconds: NotRequired[int]
    AnswerKey: NotRequired[str]
    RetryDelayInSeconds: NotRequired[int]
    IsRequestable: NotRequired[bool]
    AutoGranted: NotRequired[bool]
    AutoGrantedValue: NotRequired[int]

class CreateWorkerBlockRequestRequestTypeDef(TypedDict):
    WorkerId: str
    Reason: str

class DeleteHITRequestRequestTypeDef(TypedDict):
    HITId: str

class DeleteQualificationTypeRequestRequestTypeDef(TypedDict):
    QualificationTypeId: str

class DeleteWorkerBlockRequestRequestTypeDef(TypedDict):
    WorkerId: str
    Reason: NotRequired[str]

class DisassociateQualificationFromWorkerRequestRequestTypeDef(TypedDict):
    WorkerId: str
    QualificationTypeId: str
    Reason: NotRequired[str]

class GetAssignmentRequestRequestTypeDef(TypedDict):
    AssignmentId: str

class GetFileUploadURLRequestRequestTypeDef(TypedDict):
    AssignmentId: str
    QuestionIdentifier: str

class GetHITRequestRequestTypeDef(TypedDict):
    HITId: str

class GetQualificationScoreRequestRequestTypeDef(TypedDict):
    QualificationTypeId: str
    WorkerId: str

class GetQualificationTypeRequestRequestTypeDef(TypedDict):
    QualificationTypeId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAssignmentsForHITRequestRequestTypeDef(TypedDict):
    HITId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    AssignmentStatuses: NotRequired[Sequence[AssignmentStatusType]]

class ListBonusPaymentsRequestRequestTypeDef(TypedDict):
    HITId: NotRequired[str]
    AssignmentId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListHITsForQualificationTypeRequestRequestTypeDef(TypedDict):
    QualificationTypeId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListHITsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListQualificationRequestsRequestRequestTypeDef(TypedDict):
    QualificationTypeId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class QualificationRequestTypeDef(TypedDict):
    QualificationRequestId: NotRequired[str]
    QualificationTypeId: NotRequired[str]
    WorkerId: NotRequired[str]
    Test: NotRequired[str]
    Answer: NotRequired[str]
    SubmitTime: NotRequired[datetime]

class ListQualificationTypesRequestRequestTypeDef(TypedDict):
    MustBeRequestable: bool
    Query: NotRequired[str]
    MustBeOwnedByCaller: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListReviewPolicyResultsForHITRequestRequestTypeDef(TypedDict):
    HITId: str
    PolicyLevels: NotRequired[Sequence[ReviewPolicyLevelType]]
    RetrieveActions: NotRequired[bool]
    RetrieveResults: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListReviewableHITsRequestRequestTypeDef(TypedDict):
    HITTypeId: NotRequired[str]
    Status: NotRequired[ReviewableHITStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListWorkerBlocksRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class WorkerBlockTypeDef(TypedDict):
    WorkerId: NotRequired[str]
    Reason: NotRequired[str]

class ListWorkersWithQualificationTypeRequestRequestTypeDef(TypedDict):
    QualificationTypeId: str
    Status: NotRequired[QualificationStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class LocaleTypeDef(TypedDict):
    Country: str
    Subdivision: NotRequired[str]

class NotificationSpecificationTypeDef(TypedDict):
    Destination: str
    Transport: NotificationTransportType
    Version: str
    EventTypes: Sequence[EventTypeType]

class NotifyWorkersFailureStatusTypeDef(TypedDict):
    NotifyWorkersFailureCode: NotRequired[NotifyWorkersFailureCodeType]
    NotifyWorkersFailureMessage: NotRequired[str]
    WorkerId: NotRequired[str]

class NotifyWorkersRequestRequestTypeDef(TypedDict):
    Subject: str
    MessageText: str
    WorkerIds: Sequence[str]

class ParameterMapEntryOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[List[str]]

class ParameterMapEntryTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]

class RejectAssignmentRequestRequestTypeDef(TypedDict):
    AssignmentId: str
    RequesterFeedback: str

class RejectQualificationRequestRequestRequestTypeDef(TypedDict):
    QualificationRequestId: str
    Reason: NotRequired[str]

class ReviewActionDetailTypeDef(TypedDict):
    ActionId: NotRequired[str]
    ActionName: NotRequired[str]
    TargetId: NotRequired[str]
    TargetType: NotRequired[str]
    Status: NotRequired[ReviewActionStatusType]
    CompleteTime: NotRequired[datetime]
    Result: NotRequired[str]
    ErrorCode: NotRequired[str]

class ReviewResultDetailTypeDef(TypedDict):
    ActionId: NotRequired[str]
    SubjectId: NotRequired[str]
    SubjectType: NotRequired[str]
    QuestionId: NotRequired[str]
    Key: NotRequired[str]
    Value: NotRequired[str]

class SendBonusRequestRequestTypeDef(TypedDict):
    WorkerId: str
    BonusAmount: str
    AssignmentId: str
    Reason: str
    UniqueRequestToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class UpdateHITReviewStatusRequestRequestTypeDef(TypedDict):
    HITId: str
    Revert: NotRequired[bool]

class UpdateHITTypeOfHITRequestRequestTypeDef(TypedDict):
    HITId: str
    HITTypeId: str

class UpdateQualificationTypeRequestRequestTypeDef(TypedDict):
    QualificationTypeId: str
    Description: NotRequired[str]
    QualificationTypeStatus: NotRequired[QualificationTypeStatusType]
    Test: NotRequired[str]
    AnswerKey: NotRequired[str]
    TestDurationInSeconds: NotRequired[int]
    RetryDelayInSeconds: NotRequired[int]
    AutoGranted: NotRequired[bool]
    AutoGrantedValue: NotRequired[int]

class CreateHITTypeResponseTypeDef(TypedDict):
    HITTypeId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAccountBalanceResponseTypeDef(TypedDict):
    AvailableBalance: str
    OnHoldBalance: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetFileUploadURLResponseTypeDef(TypedDict):
    FileUploadURL: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssignmentsForHITResponseTypeDef(TypedDict):
    NumResults: int
    Assignments: List[AssignmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListBonusPaymentsResponseTypeDef(TypedDict):
    NumResults: int
    BonusPayments: List[BonusPaymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateQualificationTypeResponseTypeDef(TypedDict):
    QualificationType: QualificationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetQualificationTypeResponseTypeDef(TypedDict):
    QualificationType: QualificationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListQualificationTypesResponseTypeDef(TypedDict):
    NumResults: int
    QualificationTypes: List[QualificationTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateQualificationTypeResponseTypeDef(TypedDict):
    QualificationType: QualificationTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssignmentsForHITRequestListAssignmentsForHITPaginateTypeDef(TypedDict):
    HITId: str
    AssignmentStatuses: NotRequired[Sequence[AssignmentStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBonusPaymentsRequestListBonusPaymentsPaginateTypeDef(TypedDict):
    HITId: NotRequired[str]
    AssignmentId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListHITsForQualificationTypeRequestListHITsForQualificationTypePaginateTypeDef(TypedDict):
    QualificationTypeId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListHITsRequestListHITsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQualificationRequestsRequestListQualificationRequestsPaginateTypeDef(TypedDict):
    QualificationTypeId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQualificationTypesRequestListQualificationTypesPaginateTypeDef(TypedDict):
    MustBeRequestable: bool
    Query: NotRequired[str]
    MustBeOwnedByCaller: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReviewableHITsRequestListReviewableHITsPaginateTypeDef(TypedDict):
    HITTypeId: NotRequired[str]
    Status: NotRequired[ReviewableHITStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkerBlocksRequestListWorkerBlocksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkersWithQualificationTypeRequestListWorkersWithQualificationTypePaginateTypeDef(
    TypedDict
):
    QualificationTypeId: str
    Status: NotRequired[QualificationStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQualificationRequestsResponseTypeDef(TypedDict):
    NumResults: int
    QualificationRequests: List[QualificationRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListWorkerBlocksResponseTypeDef(TypedDict):
    NumResults: int
    WorkerBlocks: List[WorkerBlockTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class QualificationRequirementOutputTypeDef(TypedDict):
    QualificationTypeId: str
    Comparator: ComparatorType
    IntegerValues: NotRequired[List[int]]
    LocaleValues: NotRequired[List[LocaleTypeDef]]
    RequiredToPreview: NotRequired[bool]
    ActionsGuarded: NotRequired[HITAccessActionsType]

class QualificationRequirementTypeDef(TypedDict):
    QualificationTypeId: str
    Comparator: ComparatorType
    IntegerValues: NotRequired[Sequence[int]]
    LocaleValues: NotRequired[Sequence[LocaleTypeDef]]
    RequiredToPreview: NotRequired[bool]
    ActionsGuarded: NotRequired[HITAccessActionsType]

class QualificationTypeDef(TypedDict):
    QualificationTypeId: NotRequired[str]
    WorkerId: NotRequired[str]
    GrantTime: NotRequired[datetime]
    IntegerValue: NotRequired[int]
    LocaleValue: NotRequired[LocaleTypeDef]
    Status: NotRequired[QualificationStatusType]

class SendTestEventNotificationRequestRequestTypeDef(TypedDict):
    Notification: NotificationSpecificationTypeDef
    TestEventType: EventTypeType

class UpdateNotificationSettingsRequestRequestTypeDef(TypedDict):
    HITTypeId: str
    Notification: NotRequired[NotificationSpecificationTypeDef]
    Active: NotRequired[bool]

class NotifyWorkersResponseTypeDef(TypedDict):
    NotifyWorkersFailureStatuses: List[NotifyWorkersFailureStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyParameterOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[List[str]]
    MapEntries: NotRequired[List[ParameterMapEntryOutputTypeDef]]

ParameterMapEntryUnionTypeDef = Union[ParameterMapEntryTypeDef, ParameterMapEntryOutputTypeDef]

class ReviewReportTypeDef(TypedDict):
    ReviewResults: NotRequired[List[ReviewResultDetailTypeDef]]
    ReviewActions: NotRequired[List[ReviewActionDetailTypeDef]]

class UpdateExpirationForHITRequestRequestTypeDef(TypedDict):
    HITId: str
    ExpireAt: TimestampTypeDef

class HITTypeDef(TypedDict):
    HITId: NotRequired[str]
    HITTypeId: NotRequired[str]
    HITGroupId: NotRequired[str]
    HITLayoutId: NotRequired[str]
    CreationTime: NotRequired[datetime]
    Title: NotRequired[str]
    Description: NotRequired[str]
    Question: NotRequired[str]
    Keywords: NotRequired[str]
    HITStatus: NotRequired[HITStatusType]
    MaxAssignments: NotRequired[int]
    Reward: NotRequired[str]
    AutoApprovalDelayInSeconds: NotRequired[int]
    Expiration: NotRequired[datetime]
    AssignmentDurationInSeconds: NotRequired[int]
    RequesterAnnotation: NotRequired[str]
    QualificationRequirements: NotRequired[List[QualificationRequirementOutputTypeDef]]
    HITReviewStatus: NotRequired[HITReviewStatusType]
    NumberOfAssignmentsPending: NotRequired[int]
    NumberOfAssignmentsAvailable: NotRequired[int]
    NumberOfAssignmentsCompleted: NotRequired[int]

class CreateHITTypeRequestRequestTypeDef(TypedDict):
    AssignmentDurationInSeconds: int
    Reward: str
    Title: str
    Description: str
    AutoApprovalDelayInSeconds: NotRequired[int]
    Keywords: NotRequired[str]
    QualificationRequirements: NotRequired[Sequence[QualificationRequirementTypeDef]]

QualificationRequirementUnionTypeDef = Union[
    QualificationRequirementTypeDef, QualificationRequirementOutputTypeDef
]

class GetQualificationScoreResponseTypeDef(TypedDict):
    Qualification: QualificationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListWorkersWithQualificationTypeResponseTypeDef(TypedDict):
    NumResults: int
    Qualifications: List[QualificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ReviewPolicyOutputTypeDef(TypedDict):
    PolicyName: str
    Parameters: NotRequired[List[PolicyParameterOutputTypeDef]]

class PolicyParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]
    MapEntries: NotRequired[Sequence[ParameterMapEntryUnionTypeDef]]

class CreateHITResponseTypeDef(TypedDict):
    HIT: HITTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateHITWithHITTypeResponseTypeDef(TypedDict):
    HIT: HITTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAssignmentResponseTypeDef(TypedDict):
    Assignment: AssignmentTypeDef
    HIT: HITTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetHITResponseTypeDef(TypedDict):
    HIT: HITTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListHITsForQualificationTypeResponseTypeDef(TypedDict):
    NumResults: int
    HITs: List[HITTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListHITsResponseTypeDef(TypedDict):
    NumResults: int
    HITs: List[HITTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListReviewableHITsResponseTypeDef(TypedDict):
    NumResults: int
    HITs: List[HITTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListReviewPolicyResultsForHITResponseTypeDef(TypedDict):
    HITId: str
    AssignmentReviewPolicy: ReviewPolicyOutputTypeDef
    HITReviewPolicy: ReviewPolicyOutputTypeDef
    AssignmentReviewReport: ReviewReportTypeDef
    HITReviewReport: ReviewReportTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

PolicyParameterUnionTypeDef = Union[PolicyParameterTypeDef, PolicyParameterOutputTypeDef]

class ReviewPolicyTypeDef(TypedDict):
    PolicyName: str
    Parameters: NotRequired[Sequence[PolicyParameterUnionTypeDef]]

class CreateHITRequestRequestTypeDef(TypedDict):
    LifetimeInSeconds: int
    AssignmentDurationInSeconds: int
    Reward: str
    Title: str
    Description: str
    MaxAssignments: NotRequired[int]
    AutoApprovalDelayInSeconds: NotRequired[int]
    Keywords: NotRequired[str]
    Question: NotRequired[str]
    RequesterAnnotation: NotRequired[str]
    QualificationRequirements: NotRequired[Sequence[QualificationRequirementUnionTypeDef]]
    UniqueRequestToken: NotRequired[str]
    AssignmentReviewPolicy: NotRequired[ReviewPolicyTypeDef]
    HITReviewPolicy: NotRequired[ReviewPolicyTypeDef]
    HITLayoutId: NotRequired[str]
    HITLayoutParameters: NotRequired[Sequence[HITLayoutParameterTypeDef]]

class CreateHITWithHITTypeRequestRequestTypeDef(TypedDict):
    HITTypeId: str
    LifetimeInSeconds: int
    MaxAssignments: NotRequired[int]
    Question: NotRequired[str]
    RequesterAnnotation: NotRequired[str]
    UniqueRequestToken: NotRequired[str]
    AssignmentReviewPolicy: NotRequired[ReviewPolicyTypeDef]
    HITReviewPolicy: NotRequired[ReviewPolicyTypeDef]
    HITLayoutId: NotRequired[str]
    HITLayoutParameters: NotRequired[Sequence[HITLayoutParameterTypeDef]]
