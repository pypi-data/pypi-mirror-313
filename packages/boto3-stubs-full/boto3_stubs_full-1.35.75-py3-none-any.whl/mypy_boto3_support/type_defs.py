"""
Type annotations for support service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/type_defs/)

Usage::

    ```python
    from mypy_boto3_support.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AddAttachmentsToSetRequestRequestTypeDef",
    "AddAttachmentsToSetResponseTypeDef",
    "AddCommunicationToCaseRequestRequestTypeDef",
    "AddCommunicationToCaseResponseTypeDef",
    "AttachmentDetailsTypeDef",
    "AttachmentOutputTypeDef",
    "AttachmentTypeDef",
    "AttachmentUnionTypeDef",
    "BlobTypeDef",
    "CaseDetailsTypeDef",
    "CategoryTypeDef",
    "CommunicationTypeDef",
    "CommunicationTypeOptionsTypeDef",
    "CreateCaseRequestRequestTypeDef",
    "CreateCaseResponseTypeDef",
    "DateIntervalTypeDef",
    "DescribeAttachmentRequestRequestTypeDef",
    "DescribeAttachmentResponseTypeDef",
    "DescribeCasesRequestDescribeCasesPaginateTypeDef",
    "DescribeCasesRequestRequestTypeDef",
    "DescribeCasesResponseTypeDef",
    "DescribeCommunicationsRequestDescribeCommunicationsPaginateTypeDef",
    "DescribeCommunicationsRequestRequestTypeDef",
    "DescribeCommunicationsResponseTypeDef",
    "DescribeCreateCaseOptionsRequestRequestTypeDef",
    "DescribeCreateCaseOptionsResponseTypeDef",
    "DescribeServicesRequestRequestTypeDef",
    "DescribeServicesResponseTypeDef",
    "DescribeSeverityLevelsRequestRequestTypeDef",
    "DescribeSeverityLevelsResponseTypeDef",
    "DescribeSupportedLanguagesRequestRequestTypeDef",
    "DescribeSupportedLanguagesResponseTypeDef",
    "DescribeTrustedAdvisorCheckRefreshStatusesRequestRequestTypeDef",
    "DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef",
    "DescribeTrustedAdvisorCheckResultRequestRequestTypeDef",
    "DescribeTrustedAdvisorCheckResultResponseTypeDef",
    "DescribeTrustedAdvisorCheckSummariesRequestRequestTypeDef",
    "DescribeTrustedAdvisorCheckSummariesResponseTypeDef",
    "DescribeTrustedAdvisorChecksRequestRequestTypeDef",
    "DescribeTrustedAdvisorChecksResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RecentCaseCommunicationsTypeDef",
    "RefreshTrustedAdvisorCheckRequestRequestTypeDef",
    "RefreshTrustedAdvisorCheckResponseTypeDef",
    "ResolveCaseRequestRequestTypeDef",
    "ResolveCaseResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceTypeDef",
    "SeverityLevelTypeDef",
    "SupportedHourTypeDef",
    "SupportedLanguageTypeDef",
    "TrustedAdvisorCategorySpecificSummaryTypeDef",
    "TrustedAdvisorCheckDescriptionTypeDef",
    "TrustedAdvisorCheckRefreshStatusTypeDef",
    "TrustedAdvisorCheckResultTypeDef",
    "TrustedAdvisorCheckSummaryTypeDef",
    "TrustedAdvisorCostOptimizingSummaryTypeDef",
    "TrustedAdvisorResourceDetailTypeDef",
    "TrustedAdvisorResourcesSummaryTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddCommunicationToCaseRequestRequestTypeDef(TypedDict):
    communicationBody: str
    caseId: NotRequired[str]
    ccEmailAddresses: NotRequired[Sequence[str]]
    attachmentSetId: NotRequired[str]


class AttachmentDetailsTypeDef(TypedDict):
    attachmentId: NotRequired[str]
    fileName: NotRequired[str]


class AttachmentOutputTypeDef(TypedDict):
    fileName: NotRequired[str]
    data: NotRequired[bytes]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CategoryTypeDef(TypedDict):
    code: NotRequired[str]
    name: NotRequired[str]


class DateIntervalTypeDef(TypedDict):
    startDateTime: NotRequired[str]
    endDateTime: NotRequired[str]


class SupportedHourTypeDef(TypedDict):
    startTime: NotRequired[str]
    endTime: NotRequired[str]


class CreateCaseRequestRequestTypeDef(TypedDict):
    subject: str
    communicationBody: str
    serviceCode: NotRequired[str]
    severityCode: NotRequired[str]
    categoryCode: NotRequired[str]
    ccEmailAddresses: NotRequired[Sequence[str]]
    language: NotRequired[str]
    issueType: NotRequired[str]
    attachmentSetId: NotRequired[str]


class DescribeAttachmentRequestRequestTypeDef(TypedDict):
    attachmentId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeCasesRequestRequestTypeDef(TypedDict):
    caseIdList: NotRequired[Sequence[str]]
    displayId: NotRequired[str]
    afterTime: NotRequired[str]
    beforeTime: NotRequired[str]
    includeResolvedCases: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    language: NotRequired[str]
    includeCommunications: NotRequired[bool]


class DescribeCommunicationsRequestRequestTypeDef(TypedDict):
    caseId: str
    beforeTime: NotRequired[str]
    afterTime: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class DescribeCreateCaseOptionsRequestRequestTypeDef(TypedDict):
    issueType: str
    serviceCode: str
    language: str
    categoryCode: str


class DescribeServicesRequestRequestTypeDef(TypedDict):
    serviceCodeList: NotRequired[Sequence[str]]
    language: NotRequired[str]


class DescribeSeverityLevelsRequestRequestTypeDef(TypedDict):
    language: NotRequired[str]


class SeverityLevelTypeDef(TypedDict):
    code: NotRequired[str]
    name: NotRequired[str]


class DescribeSupportedLanguagesRequestRequestTypeDef(TypedDict):
    issueType: str
    serviceCode: str
    categoryCode: str


class SupportedLanguageTypeDef(TypedDict):
    code: NotRequired[str]
    language: NotRequired[str]
    display: NotRequired[str]


class DescribeTrustedAdvisorCheckRefreshStatusesRequestRequestTypeDef(TypedDict):
    checkIds: Sequence[str]


class TrustedAdvisorCheckRefreshStatusTypeDef(TypedDict):
    checkId: str
    status: str
    millisUntilNextRefreshable: int


class DescribeTrustedAdvisorCheckResultRequestRequestTypeDef(TypedDict):
    checkId: str
    language: NotRequired[str]


class DescribeTrustedAdvisorCheckSummariesRequestRequestTypeDef(TypedDict):
    checkIds: Sequence[str]


class DescribeTrustedAdvisorChecksRequestRequestTypeDef(TypedDict):
    language: str


TrustedAdvisorCheckDescriptionTypeDef = TypedDict(
    "TrustedAdvisorCheckDescriptionTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "category": str,
        "metadata": List[str],
    },
)


class RefreshTrustedAdvisorCheckRequestRequestTypeDef(TypedDict):
    checkId: str


class ResolveCaseRequestRequestTypeDef(TypedDict):
    caseId: NotRequired[str]


class TrustedAdvisorCostOptimizingSummaryTypeDef(TypedDict):
    estimatedMonthlySavings: float
    estimatedPercentMonthlySavings: float


class TrustedAdvisorResourceDetailTypeDef(TypedDict):
    status: str
    resourceId: str
    metadata: List[str]
    region: NotRequired[str]
    isSuppressed: NotRequired[bool]


class TrustedAdvisorResourcesSummaryTypeDef(TypedDict):
    resourcesProcessed: int
    resourcesFlagged: int
    resourcesIgnored: int
    resourcesSuppressed: int


class AddAttachmentsToSetResponseTypeDef(TypedDict):
    attachmentSetId: str
    expiryTime: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddCommunicationToCaseResponseTypeDef(TypedDict):
    result: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCaseResponseTypeDef(TypedDict):
    caseId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResolveCaseResponseTypeDef(TypedDict):
    initialCaseStatus: str
    finalCaseStatus: str
    ResponseMetadata: ResponseMetadataTypeDef


class CommunicationTypeDef(TypedDict):
    caseId: NotRequired[str]
    body: NotRequired[str]
    submittedBy: NotRequired[str]
    timeCreated: NotRequired[str]
    attachmentSet: NotRequired[List[AttachmentDetailsTypeDef]]


class DescribeAttachmentResponseTypeDef(TypedDict):
    attachment: AttachmentOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AttachmentTypeDef(TypedDict):
    fileName: NotRequired[str]
    data: NotRequired[BlobTypeDef]


class ServiceTypeDef(TypedDict):
    code: NotRequired[str]
    name: NotRequired[str]
    categories: NotRequired[List[CategoryTypeDef]]


CommunicationTypeOptionsTypeDef = TypedDict(
    "CommunicationTypeOptionsTypeDef",
    {
        "type": NotRequired[str],
        "supportedHours": NotRequired[List[SupportedHourTypeDef]],
        "datesWithoutSupport": NotRequired[List[DateIntervalTypeDef]],
    },
)


class DescribeCasesRequestDescribeCasesPaginateTypeDef(TypedDict):
    caseIdList: NotRequired[Sequence[str]]
    displayId: NotRequired[str]
    afterTime: NotRequired[str]
    beforeTime: NotRequired[str]
    includeResolvedCases: NotRequired[bool]
    language: NotRequired[str]
    includeCommunications: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCommunicationsRequestDescribeCommunicationsPaginateTypeDef(TypedDict):
    caseId: str
    beforeTime: NotRequired[str]
    afterTime: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSeverityLevelsResponseTypeDef(TypedDict):
    severityLevels: List[SeverityLevelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSupportedLanguagesResponseTypeDef(TypedDict):
    supportedLanguages: List[SupportedLanguageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef(TypedDict):
    statuses: List[TrustedAdvisorCheckRefreshStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RefreshTrustedAdvisorCheckResponseTypeDef(TypedDict):
    status: TrustedAdvisorCheckRefreshStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrustedAdvisorChecksResponseTypeDef(TypedDict):
    checks: List[TrustedAdvisorCheckDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TrustedAdvisorCategorySpecificSummaryTypeDef(TypedDict):
    costOptimizing: NotRequired[TrustedAdvisorCostOptimizingSummaryTypeDef]


class DescribeCommunicationsResponseTypeDef(TypedDict):
    communications: List[CommunicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RecentCaseCommunicationsTypeDef(TypedDict):
    communications: NotRequired[List[CommunicationTypeDef]]
    nextToken: NotRequired[str]


AttachmentUnionTypeDef = Union[AttachmentTypeDef, AttachmentOutputTypeDef]


class DescribeServicesResponseTypeDef(TypedDict):
    services: List[ServiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCreateCaseOptionsResponseTypeDef(TypedDict):
    languageAvailability: str
    communicationTypes: List[CommunicationTypeOptionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TrustedAdvisorCheckResultTypeDef(TypedDict):
    checkId: str
    timestamp: str
    status: str
    resourcesSummary: TrustedAdvisorResourcesSummaryTypeDef
    categorySpecificSummary: TrustedAdvisorCategorySpecificSummaryTypeDef
    flaggedResources: List[TrustedAdvisorResourceDetailTypeDef]


class TrustedAdvisorCheckSummaryTypeDef(TypedDict):
    checkId: str
    timestamp: str
    status: str
    resourcesSummary: TrustedAdvisorResourcesSummaryTypeDef
    categorySpecificSummary: TrustedAdvisorCategorySpecificSummaryTypeDef
    hasFlaggedResources: NotRequired[bool]


class CaseDetailsTypeDef(TypedDict):
    caseId: NotRequired[str]
    displayId: NotRequired[str]
    subject: NotRequired[str]
    status: NotRequired[str]
    serviceCode: NotRequired[str]
    categoryCode: NotRequired[str]
    severityCode: NotRequired[str]
    submittedBy: NotRequired[str]
    timeCreated: NotRequired[str]
    recentCommunications: NotRequired[RecentCaseCommunicationsTypeDef]
    ccEmailAddresses: NotRequired[List[str]]
    language: NotRequired[str]


class AddAttachmentsToSetRequestRequestTypeDef(TypedDict):
    attachments: Sequence[AttachmentUnionTypeDef]
    attachmentSetId: NotRequired[str]


class DescribeTrustedAdvisorCheckResultResponseTypeDef(TypedDict):
    result: TrustedAdvisorCheckResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrustedAdvisorCheckSummariesResponseTypeDef(TypedDict):
    summaries: List[TrustedAdvisorCheckSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCasesResponseTypeDef(TypedDict):
    cases: List[CaseDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
