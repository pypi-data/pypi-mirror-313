"""
Type annotations for macie2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie2/type_defs/)

Usage::

    ```python
    from mypy_boto3_macie2.type_defs import AcceptInvitationRequestRequestTypeDef

    data: AcceptInvitationRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AdminStatusType,
    AllowListStatusCodeType,
    AllowsUnencryptedObjectUploadsType,
    AutoEnableModeType,
    AutomatedDiscoveryAccountStatusType,
    AutomatedDiscoveryAccountUpdateErrorCodeType,
    AutomatedDiscoveryMonitoringStatusType,
    AutomatedDiscoveryStatusType,
    AvailabilityCodeType,
    ClassificationScopeUpdateOperationType,
    DataIdentifierSeverityType,
    DataIdentifierTypeType,
    DayOfWeekType,
    EffectivePermissionType,
    EncryptionTypeType,
    ErrorCodeType,
    FindingCategoryType,
    FindingPublishingFrequencyType,
    FindingsFilterActionType,
    FindingStatisticsSortAttributeNameType,
    FindingTypeType,
    GroupByType,
    IsDefinedInJobType,
    IsMonitoredByJobType,
    JobComparatorType,
    JobStatusType,
    JobTypeType,
    LastRunErrorStatusCodeType,
    ListJobsFilterKeyType,
    ListJobsSortAttributeNameType,
    MacieStatusType,
    ManagedDataIdentifierSelectorType,
    OrderByType,
    OriginTypeType,
    RelationshipStatusType,
    RetrievalModeType,
    RevealRequestStatusType,
    RevealStatusType,
    ScopeFilterKeyType,
    SearchResourcesComparatorType,
    SearchResourcesSimpleCriterionKeyType,
    SearchResourcesSortAttributeNameType,
    SensitiveDataItemCategoryType,
    SeverityDescriptionType,
    SharedAccessType,
    SimpleCriterionKeyForJobType,
    StorageClassType,
    TimeRangeType,
    TypeType,
    UnavailabilityReasonCodeType,
    UsageStatisticsFilterComparatorType,
    UsageStatisticsFilterKeyType,
    UsageStatisticsSortKeyType,
    UsageTypeType,
    UserIdentityTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptInvitationRequestRequestTypeDef",
    "AccessControlListTypeDef",
    "AccountDetailTypeDef",
    "AccountLevelPermissionsTypeDef",
    "AdminAccountTypeDef",
    "AllowListCriteriaTypeDef",
    "AllowListStatusTypeDef",
    "AllowListSummaryTypeDef",
    "ApiCallDetailsTypeDef",
    "AssumedRoleTypeDef",
    "AutomatedDiscoveryAccountTypeDef",
    "AutomatedDiscoveryAccountUpdateErrorTypeDef",
    "AutomatedDiscoveryAccountUpdateTypeDef",
    "AwsAccountTypeDef",
    "AwsServiceTypeDef",
    "BatchGetCustomDataIdentifierSummaryTypeDef",
    "BatchGetCustomDataIdentifiersRequestRequestTypeDef",
    "BatchGetCustomDataIdentifiersResponseTypeDef",
    "BatchUpdateAutomatedDiscoveryAccountsRequestRequestTypeDef",
    "BatchUpdateAutomatedDiscoveryAccountsResponseTypeDef",
    "BlockPublicAccessTypeDef",
    "BucketCountByEffectivePermissionTypeDef",
    "BucketCountByEncryptionTypeTypeDef",
    "BucketCountBySharedAccessTypeTypeDef",
    "BucketCountPolicyAllowsUnencryptedObjectUploadsTypeDef",
    "BucketCriteriaAdditionalPropertiesTypeDef",
    "BucketLevelPermissionsTypeDef",
    "BucketMetadataTypeDef",
    "BucketPermissionConfigurationTypeDef",
    "BucketPolicyTypeDef",
    "BucketPublicAccessTypeDef",
    "BucketServerSideEncryptionTypeDef",
    "BucketSortCriteriaTypeDef",
    "BucketStatisticsBySensitivityTypeDef",
    "CellTypeDef",
    "ClassificationDetailsTypeDef",
    "ClassificationExportConfigurationTypeDef",
    "ClassificationResultStatusTypeDef",
    "ClassificationResultTypeDef",
    "ClassificationScopeSummaryTypeDef",
    "CreateAllowListRequestRequestTypeDef",
    "CreateAllowListResponseTypeDef",
    "CreateClassificationJobRequestRequestTypeDef",
    "CreateClassificationJobResponseTypeDef",
    "CreateCustomDataIdentifierRequestRequestTypeDef",
    "CreateCustomDataIdentifierResponseTypeDef",
    "CreateFindingsFilterRequestRequestTypeDef",
    "CreateFindingsFilterResponseTypeDef",
    "CreateInvitationsRequestRequestTypeDef",
    "CreateInvitationsResponseTypeDef",
    "CreateMemberRequestRequestTypeDef",
    "CreateMemberResponseTypeDef",
    "CreateSampleFindingsRequestRequestTypeDef",
    "CriteriaBlockForJobOutputTypeDef",
    "CriteriaBlockForJobTypeDef",
    "CriteriaBlockForJobUnionTypeDef",
    "CriteriaForJobOutputTypeDef",
    "CriteriaForJobTypeDef",
    "CriteriaForJobUnionTypeDef",
    "CriterionAdditionalPropertiesOutputTypeDef",
    "CriterionAdditionalPropertiesTypeDef",
    "CriterionAdditionalPropertiesUnionTypeDef",
    "CustomDataIdentifierSummaryTypeDef",
    "CustomDataIdentifiersTypeDef",
    "CustomDetectionTypeDef",
    "DeclineInvitationsRequestRequestTypeDef",
    "DeclineInvitationsResponseTypeDef",
    "DefaultDetectionTypeDef",
    "DeleteAllowListRequestRequestTypeDef",
    "DeleteCustomDataIdentifierRequestRequestTypeDef",
    "DeleteFindingsFilterRequestRequestTypeDef",
    "DeleteInvitationsRequestRequestTypeDef",
    "DeleteInvitationsResponseTypeDef",
    "DeleteMemberRequestRequestTypeDef",
    "DescribeBucketsRequestDescribeBucketsPaginateTypeDef",
    "DescribeBucketsRequestRequestTypeDef",
    "DescribeBucketsResponseTypeDef",
    "DescribeClassificationJobRequestRequestTypeDef",
    "DescribeClassificationJobResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "DetectedDataDetailsTypeDef",
    "DetectionTypeDef",
    "DisableOrganizationAdminAccountRequestRequestTypeDef",
    "DisassociateMemberRequestRequestTypeDef",
    "DomainDetailsTypeDef",
    "EnableMacieRequestRequestTypeDef",
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    "FederatedUserTypeDef",
    "FindingActionTypeDef",
    "FindingActorTypeDef",
    "FindingCriteriaOutputTypeDef",
    "FindingCriteriaTypeDef",
    "FindingStatisticsSortCriteriaTypeDef",
    "FindingTypeDef",
    "FindingsFilterListItemTypeDef",
    "GetAdministratorAccountResponseTypeDef",
    "GetAllowListRequestRequestTypeDef",
    "GetAllowListResponseTypeDef",
    "GetAutomatedDiscoveryConfigurationResponseTypeDef",
    "GetBucketStatisticsRequestRequestTypeDef",
    "GetBucketStatisticsResponseTypeDef",
    "GetClassificationExportConfigurationResponseTypeDef",
    "GetClassificationScopeRequestRequestTypeDef",
    "GetClassificationScopeResponseTypeDef",
    "GetCustomDataIdentifierRequestRequestTypeDef",
    "GetCustomDataIdentifierResponseTypeDef",
    "GetFindingStatisticsRequestRequestTypeDef",
    "GetFindingStatisticsResponseTypeDef",
    "GetFindingsFilterRequestRequestTypeDef",
    "GetFindingsFilterResponseTypeDef",
    "GetFindingsPublicationConfigurationResponseTypeDef",
    "GetFindingsRequestRequestTypeDef",
    "GetFindingsResponseTypeDef",
    "GetInvitationsCountResponseTypeDef",
    "GetMacieSessionResponseTypeDef",
    "GetMasterAccountResponseTypeDef",
    "GetMemberRequestRequestTypeDef",
    "GetMemberResponseTypeDef",
    "GetResourceProfileRequestRequestTypeDef",
    "GetResourceProfileResponseTypeDef",
    "GetRevealConfigurationResponseTypeDef",
    "GetSensitiveDataOccurrencesAvailabilityRequestRequestTypeDef",
    "GetSensitiveDataOccurrencesAvailabilityResponseTypeDef",
    "GetSensitiveDataOccurrencesRequestFindingRevealedWaitTypeDef",
    "GetSensitiveDataOccurrencesRequestRequestTypeDef",
    "GetSensitiveDataOccurrencesResponseTypeDef",
    "GetSensitivityInspectionTemplateRequestRequestTypeDef",
    "GetSensitivityInspectionTemplateResponseTypeDef",
    "GetUsageStatisticsRequestGetUsageStatisticsPaginateTypeDef",
    "GetUsageStatisticsRequestRequestTypeDef",
    "GetUsageStatisticsResponseTypeDef",
    "GetUsageTotalsRequestRequestTypeDef",
    "GetUsageTotalsResponseTypeDef",
    "GroupCountTypeDef",
    "IamUserTypeDef",
    "InvitationTypeDef",
    "IpAddressDetailsTypeDef",
    "IpCityTypeDef",
    "IpCountryTypeDef",
    "IpGeoLocationTypeDef",
    "IpOwnerTypeDef",
    "JobDetailsTypeDef",
    "JobScheduleFrequencyOutputTypeDef",
    "JobScheduleFrequencyTypeDef",
    "JobScopeTermOutputTypeDef",
    "JobScopeTermTypeDef",
    "JobScopeTermUnionTypeDef",
    "JobScopingBlockOutputTypeDef",
    "JobScopingBlockTypeDef",
    "JobScopingBlockUnionTypeDef",
    "JobSummaryTypeDef",
    "KeyValuePairTypeDef",
    "LastRunErrorStatusTypeDef",
    "ListAllowListsRequestListAllowListsPaginateTypeDef",
    "ListAllowListsRequestRequestTypeDef",
    "ListAllowListsResponseTypeDef",
    "ListAutomatedDiscoveryAccountsRequestListAutomatedDiscoveryAccountsPaginateTypeDef",
    "ListAutomatedDiscoveryAccountsRequestRequestTypeDef",
    "ListAutomatedDiscoveryAccountsResponseTypeDef",
    "ListClassificationJobsRequestListClassificationJobsPaginateTypeDef",
    "ListClassificationJobsRequestRequestTypeDef",
    "ListClassificationJobsResponseTypeDef",
    "ListClassificationScopesRequestListClassificationScopesPaginateTypeDef",
    "ListClassificationScopesRequestRequestTypeDef",
    "ListClassificationScopesResponseTypeDef",
    "ListCustomDataIdentifiersRequestListCustomDataIdentifiersPaginateTypeDef",
    "ListCustomDataIdentifiersRequestRequestTypeDef",
    "ListCustomDataIdentifiersResponseTypeDef",
    "ListFindingsFiltersRequestListFindingsFiltersPaginateTypeDef",
    "ListFindingsFiltersRequestRequestTypeDef",
    "ListFindingsFiltersResponseTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "ListFindingsResponseTypeDef",
    "ListInvitationsRequestListInvitationsPaginateTypeDef",
    "ListInvitationsRequestRequestTypeDef",
    "ListInvitationsResponseTypeDef",
    "ListJobsFilterCriteriaTypeDef",
    "ListJobsFilterTermTypeDef",
    "ListJobsSortCriteriaTypeDef",
    "ListManagedDataIdentifiersRequestListManagedDataIdentifiersPaginateTypeDef",
    "ListManagedDataIdentifiersRequestRequestTypeDef",
    "ListManagedDataIdentifiersResponseTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListMembersResponseTypeDef",
    "ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef",
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    "ListOrganizationAdminAccountsResponseTypeDef",
    "ListResourceProfileArtifactsRequestListResourceProfileArtifactsPaginateTypeDef",
    "ListResourceProfileArtifactsRequestRequestTypeDef",
    "ListResourceProfileArtifactsResponseTypeDef",
    "ListResourceProfileDetectionsRequestListResourceProfileDetectionsPaginateTypeDef",
    "ListResourceProfileDetectionsRequestRequestTypeDef",
    "ListResourceProfileDetectionsResponseTypeDef",
    "ListSensitivityInspectionTemplatesRequestListSensitivityInspectionTemplatesPaginateTypeDef",
    "ListSensitivityInspectionTemplatesRequestRequestTypeDef",
    "ListSensitivityInspectionTemplatesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ManagedDataIdentifierSummaryTypeDef",
    "MatchingBucketTypeDef",
    "MatchingResourceTypeDef",
    "MemberTypeDef",
    "MonthlyScheduleTypeDef",
    "ObjectCountByEncryptionTypeTypeDef",
    "ObjectLevelStatisticsTypeDef",
    "OccurrencesTypeDef",
    "PageTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyDetailsTypeDef",
    "PutClassificationExportConfigurationRequestRequestTypeDef",
    "PutClassificationExportConfigurationResponseTypeDef",
    "PutFindingsPublicationConfigurationRequestRequestTypeDef",
    "RangeTypeDef",
    "RecordTypeDef",
    "ReplicationDetailsTypeDef",
    "ResourceProfileArtifactTypeDef",
    "ResourceStatisticsTypeDef",
    "ResourcesAffectedTypeDef",
    "ResponseMetadataTypeDef",
    "RetrievalConfigurationTypeDef",
    "RevealConfigurationTypeDef",
    "S3BucketCriteriaForJobOutputTypeDef",
    "S3BucketCriteriaForJobTypeDef",
    "S3BucketCriteriaForJobUnionTypeDef",
    "S3BucketDefinitionForJobOutputTypeDef",
    "S3BucketDefinitionForJobTypeDef",
    "S3BucketDefinitionForJobUnionTypeDef",
    "S3BucketOwnerTypeDef",
    "S3BucketTypeDef",
    "S3ClassificationScopeExclusionTypeDef",
    "S3ClassificationScopeExclusionUpdateTypeDef",
    "S3ClassificationScopeTypeDef",
    "S3ClassificationScopeUpdateTypeDef",
    "S3DestinationTypeDef",
    "S3JobDefinitionOutputTypeDef",
    "S3JobDefinitionTypeDef",
    "S3ObjectTypeDef",
    "S3WordsListTypeDef",
    "ScopingOutputTypeDef",
    "ScopingTypeDef",
    "ScopingUnionTypeDef",
    "SearchResourcesBucketCriteriaTypeDef",
    "SearchResourcesCriteriaBlockTypeDef",
    "SearchResourcesCriteriaTypeDef",
    "SearchResourcesRequestRequestTypeDef",
    "SearchResourcesRequestSearchResourcesPaginateTypeDef",
    "SearchResourcesResponseTypeDef",
    "SearchResourcesSimpleCriterionTypeDef",
    "SearchResourcesSortCriteriaTypeDef",
    "SearchResourcesTagCriterionPairTypeDef",
    "SearchResourcesTagCriterionTypeDef",
    "SecurityHubConfigurationTypeDef",
    "SensitiveDataItemTypeDef",
    "SensitivityAggregationsTypeDef",
    "SensitivityInspectionTemplateExcludesOutputTypeDef",
    "SensitivityInspectionTemplateExcludesTypeDef",
    "SensitivityInspectionTemplateIncludesOutputTypeDef",
    "SensitivityInspectionTemplateIncludesTypeDef",
    "SensitivityInspectionTemplatesEntryTypeDef",
    "ServerSideEncryptionTypeDef",
    "ServiceLimitTypeDef",
    "SessionContextAttributesTypeDef",
    "SessionContextTypeDef",
    "SessionIssuerTypeDef",
    "SeverityLevelTypeDef",
    "SeverityTypeDef",
    "SimpleCriterionForJobOutputTypeDef",
    "SimpleCriterionForJobTypeDef",
    "SimpleCriterionForJobUnionTypeDef",
    "SimpleScopeTermOutputTypeDef",
    "SimpleScopeTermTypeDef",
    "SimpleScopeTermUnionTypeDef",
    "SortCriteriaTypeDef",
    "StatisticsTypeDef",
    "SuppressDataIdentifierTypeDef",
    "TagCriterionForJobOutputTypeDef",
    "TagCriterionForJobTypeDef",
    "TagCriterionForJobUnionTypeDef",
    "TagCriterionPairForJobTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagScopeTermOutputTypeDef",
    "TagScopeTermTypeDef",
    "TagScopeTermUnionTypeDef",
    "TagValuePairTypeDef",
    "TestCustomDataIdentifierRequestRequestTypeDef",
    "TestCustomDataIdentifierResponseTypeDef",
    "UnprocessedAccountTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAllowListRequestRequestTypeDef",
    "UpdateAllowListResponseTypeDef",
    "UpdateAutomatedDiscoveryConfigurationRequestRequestTypeDef",
    "UpdateClassificationJobRequestRequestTypeDef",
    "UpdateClassificationScopeRequestRequestTypeDef",
    "UpdateFindingsFilterRequestRequestTypeDef",
    "UpdateFindingsFilterResponseTypeDef",
    "UpdateMacieSessionRequestRequestTypeDef",
    "UpdateMemberSessionRequestRequestTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "UpdateResourceProfileDetectionsRequestRequestTypeDef",
    "UpdateResourceProfileRequestRequestTypeDef",
    "UpdateRetrievalConfigurationTypeDef",
    "UpdateRevealConfigurationRequestRequestTypeDef",
    "UpdateRevealConfigurationResponseTypeDef",
    "UpdateSensitivityInspectionTemplateRequestRequestTypeDef",
    "UsageByAccountTypeDef",
    "UsageRecordTypeDef",
    "UsageStatisticsFilterTypeDef",
    "UsageStatisticsSortByTypeDef",
    "UsageTotalTypeDef",
    "UserIdentityRootTypeDef",
    "UserIdentityTypeDef",
    "UserPausedDetailsTypeDef",
    "WaiterConfigTypeDef",
    "WeeklyScheduleTypeDef",
)

class AcceptInvitationRequestRequestTypeDef(TypedDict):
    invitationId: str
    administratorAccountId: NotRequired[str]
    masterAccount: NotRequired[str]

class AccessControlListTypeDef(TypedDict):
    allowsPublicReadAccess: NotRequired[bool]
    allowsPublicWriteAccess: NotRequired[bool]

class AccountDetailTypeDef(TypedDict):
    accountId: str
    email: str

class BlockPublicAccessTypeDef(TypedDict):
    blockPublicAcls: NotRequired[bool]
    blockPublicPolicy: NotRequired[bool]
    ignorePublicAcls: NotRequired[bool]
    restrictPublicBuckets: NotRequired[bool]

class AdminAccountTypeDef(TypedDict):
    accountId: NotRequired[str]
    status: NotRequired[AdminStatusType]

class S3WordsListTypeDef(TypedDict):
    bucketName: str
    objectKey: str

class AllowListStatusTypeDef(TypedDict):
    code: AllowListStatusCodeType
    description: NotRequired[str]

AllowListSummaryTypeDef = TypedDict(
    "AllowListSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "updatedAt": NotRequired[datetime],
    },
)

class ApiCallDetailsTypeDef(TypedDict):
    api: NotRequired[str]
    apiServiceName: NotRequired[str]
    firstSeen: NotRequired[datetime]
    lastSeen: NotRequired[datetime]

class AutomatedDiscoveryAccountTypeDef(TypedDict):
    accountId: NotRequired[str]
    status: NotRequired[AutomatedDiscoveryAccountStatusType]

class AutomatedDiscoveryAccountUpdateErrorTypeDef(TypedDict):
    accountId: NotRequired[str]
    errorCode: NotRequired[AutomatedDiscoveryAccountUpdateErrorCodeType]

class AutomatedDiscoveryAccountUpdateTypeDef(TypedDict):
    accountId: NotRequired[str]
    status: NotRequired[AutomatedDiscoveryAccountStatusType]

class AwsAccountTypeDef(TypedDict):
    accountId: NotRequired[str]
    principalId: NotRequired[str]

class AwsServiceTypeDef(TypedDict):
    invokedBy: NotRequired[str]

BatchGetCustomDataIdentifierSummaryTypeDef = TypedDict(
    "BatchGetCustomDataIdentifierSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "deleted": NotRequired[bool],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class BatchGetCustomDataIdentifiersRequestRequestTypeDef(TypedDict):
    ids: NotRequired[Sequence[str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BucketCountByEffectivePermissionTypeDef(TypedDict):
    publiclyAccessible: NotRequired[int]
    publiclyReadable: NotRequired[int]
    publiclyWritable: NotRequired[int]
    unknown: NotRequired[int]

class BucketCountByEncryptionTypeTypeDef(TypedDict):
    kmsManaged: NotRequired[int]
    s3Managed: NotRequired[int]
    unencrypted: NotRequired[int]
    unknown: NotRequired[int]

class BucketCountBySharedAccessTypeTypeDef(TypedDict):
    external: NotRequired[int]
    internal: NotRequired[int]
    notShared: NotRequired[int]
    unknown: NotRequired[int]

class BucketCountPolicyAllowsUnencryptedObjectUploadsTypeDef(TypedDict):
    allowsUnencryptedObjectUploads: NotRequired[int]
    deniesUnencryptedObjectUploads: NotRequired[int]
    unknown: NotRequired[int]

class BucketCriteriaAdditionalPropertiesTypeDef(TypedDict):
    eq: NotRequired[Sequence[str]]
    gt: NotRequired[int]
    gte: NotRequired[int]
    lt: NotRequired[int]
    lte: NotRequired[int]
    neq: NotRequired[Sequence[str]]
    prefix: NotRequired[str]

class BucketPolicyTypeDef(TypedDict):
    allowsPublicReadAccess: NotRequired[bool]
    allowsPublicWriteAccess: NotRequired[bool]

BucketServerSideEncryptionTypeDef = TypedDict(
    "BucketServerSideEncryptionTypeDef",
    {
        "kmsMasterKeyId": NotRequired[str],
        "type": NotRequired[TypeType],
    },
)

class JobDetailsTypeDef(TypedDict):
    isDefinedInJob: NotRequired[IsDefinedInJobType]
    isMonitoredByJob: NotRequired[IsMonitoredByJobType]
    lastJobId: NotRequired[str]
    lastJobRunTime: NotRequired[datetime]

class KeyValuePairTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class ObjectCountByEncryptionTypeTypeDef(TypedDict):
    customerManaged: NotRequired[int]
    kmsManaged: NotRequired[int]
    s3Managed: NotRequired[int]
    unencrypted: NotRequired[int]
    unknown: NotRequired[int]

class ObjectLevelStatisticsTypeDef(TypedDict):
    fileType: NotRequired[int]
    storageClass: NotRequired[int]
    total: NotRequired[int]

class ReplicationDetailsTypeDef(TypedDict):
    replicated: NotRequired[bool]
    replicatedExternally: NotRequired[bool]
    replicationAccounts: NotRequired[List[str]]

class BucketSortCriteriaTypeDef(TypedDict):
    attributeName: NotRequired[str]
    orderBy: NotRequired[OrderByType]

class SensitivityAggregationsTypeDef(TypedDict):
    classifiableSizeInBytes: NotRequired[int]
    publiclyAccessibleCount: NotRequired[int]
    totalCount: NotRequired[int]
    totalSizeInBytes: NotRequired[int]

class CellTypeDef(TypedDict):
    cellReference: NotRequired[str]
    column: NotRequired[int]
    columnName: NotRequired[str]
    row: NotRequired[int]

class S3DestinationTypeDef(TypedDict):
    bucketName: str
    kmsKeyArn: str
    keyPrefix: NotRequired[str]

class ClassificationResultStatusTypeDef(TypedDict):
    code: NotRequired[str]
    reason: NotRequired[str]

ClassificationScopeSummaryTypeDef = TypedDict(
    "ClassificationScopeSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class SeverityLevelTypeDef(TypedDict):
    occurrencesThreshold: int
    severity: DataIdentifierSeverityType

class CreateInvitationsRequestRequestTypeDef(TypedDict):
    accountIds: Sequence[str]
    disableEmailNotification: NotRequired[bool]
    message: NotRequired[str]

class UnprocessedAccountTypeDef(TypedDict):
    accountId: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]
    errorMessage: NotRequired[str]

class CreateSampleFindingsRequestRequestTypeDef(TypedDict):
    findingTypes: NotRequired[Sequence[FindingTypeType]]

class SimpleCriterionForJobOutputTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    key: NotRequired[SimpleCriterionKeyForJobType]
    values: NotRequired[List[str]]

class CriterionAdditionalPropertiesOutputTypeDef(TypedDict):
    eq: NotRequired[List[str]]
    eqExactMatch: NotRequired[List[str]]
    gt: NotRequired[int]
    gte: NotRequired[int]
    lt: NotRequired[int]
    lte: NotRequired[int]
    neq: NotRequired[List[str]]

class CriterionAdditionalPropertiesTypeDef(TypedDict):
    eq: NotRequired[Sequence[str]]
    eqExactMatch: NotRequired[Sequence[str]]
    gt: NotRequired[int]
    gte: NotRequired[int]
    lt: NotRequired[int]
    lte: NotRequired[int]
    neq: NotRequired[Sequence[str]]

CustomDataIdentifierSummaryTypeDef = TypedDict(
    "CustomDataIdentifierSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class DeclineInvitationsRequestRequestTypeDef(TypedDict):
    accountIds: Sequence[str]

DeleteAllowListRequestRequestTypeDef = TypedDict(
    "DeleteAllowListRequestRequestTypeDef",
    {
        "id": str,
        "ignoreJobChecks": NotRequired[str],
    },
)
DeleteCustomDataIdentifierRequestRequestTypeDef = TypedDict(
    "DeleteCustomDataIdentifierRequestRequestTypeDef",
    {
        "id": str,
    },
)
DeleteFindingsFilterRequestRequestTypeDef = TypedDict(
    "DeleteFindingsFilterRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DeleteInvitationsRequestRequestTypeDef(TypedDict):
    accountIds: Sequence[str]

DeleteMemberRequestRequestTypeDef = TypedDict(
    "DeleteMemberRequestRequestTypeDef",
    {
        "id": str,
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeClassificationJobRequestRequestTypeDef(TypedDict):
    jobId: str

class LastRunErrorStatusTypeDef(TypedDict):
    code: NotRequired[LastRunErrorStatusCodeType]

class StatisticsTypeDef(TypedDict):
    approximateNumberOfObjectsToProcess: NotRequired[float]
    numberOfRuns: NotRequired[float]

class UserPausedDetailsTypeDef(TypedDict):
    jobExpiresAt: NotRequired[datetime]
    jobImminentExpirationHealthEventArn: NotRequired[str]
    jobPausedAt: NotRequired[datetime]

class DetectedDataDetailsTypeDef(TypedDict):
    value: str

DetectionTypeDef = TypedDict(
    "DetectionTypeDef",
    {
        "arn": NotRequired[str],
        "count": NotRequired[int],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "suppressed": NotRequired[bool],
        "type": NotRequired[DataIdentifierTypeType],
    },
)

class DisableOrganizationAdminAccountRequestRequestTypeDef(TypedDict):
    adminAccountId: str

DisassociateMemberRequestRequestTypeDef = TypedDict(
    "DisassociateMemberRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DomainDetailsTypeDef(TypedDict):
    domainName: NotRequired[str]

class EnableMacieRequestRequestTypeDef(TypedDict):
    clientToken: NotRequired[str]
    findingPublishingFrequency: NotRequired[FindingPublishingFrequencyType]
    status: NotRequired[MacieStatusType]

class EnableOrganizationAdminAccountRequestRequestTypeDef(TypedDict):
    adminAccountId: str
    clientToken: NotRequired[str]

class FindingStatisticsSortCriteriaTypeDef(TypedDict):
    attributeName: NotRequired[FindingStatisticsSortAttributeNameType]
    orderBy: NotRequired[OrderByType]

class SeverityTypeDef(TypedDict):
    description: NotRequired[SeverityDescriptionType]
    score: NotRequired[int]

FindingsFilterListItemTypeDef = TypedDict(
    "FindingsFilterListItemTypeDef",
    {
        "action": NotRequired[FindingsFilterActionType],
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)

class InvitationTypeDef(TypedDict):
    accountId: NotRequired[str]
    invitationId: NotRequired[str]
    invitedAt: NotRequired[datetime]
    relationshipStatus: NotRequired[RelationshipStatusType]

GetAllowListRequestRequestTypeDef = TypedDict(
    "GetAllowListRequestRequestTypeDef",
    {
        "id": str,
    },
)

class GetBucketStatisticsRequestRequestTypeDef(TypedDict):
    accountId: NotRequired[str]

GetClassificationScopeRequestRequestTypeDef = TypedDict(
    "GetClassificationScopeRequestRequestTypeDef",
    {
        "id": str,
    },
)
GetCustomDataIdentifierRequestRequestTypeDef = TypedDict(
    "GetCustomDataIdentifierRequestRequestTypeDef",
    {
        "id": str,
    },
)

class GroupCountTypeDef(TypedDict):
    count: NotRequired[int]
    groupKey: NotRequired[str]

GetFindingsFilterRequestRequestTypeDef = TypedDict(
    "GetFindingsFilterRequestRequestTypeDef",
    {
        "id": str,
    },
)

class SecurityHubConfigurationTypeDef(TypedDict):
    publishClassificationFindings: bool
    publishPolicyFindings: bool

class SortCriteriaTypeDef(TypedDict):
    attributeName: NotRequired[str]
    orderBy: NotRequired[OrderByType]

GetMemberRequestRequestTypeDef = TypedDict(
    "GetMemberRequestRequestTypeDef",
    {
        "id": str,
    },
)

class GetResourceProfileRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ResourceStatisticsTypeDef(TypedDict):
    totalBytesClassified: NotRequired[int]
    totalDetections: NotRequired[int]
    totalDetectionsSuppressed: NotRequired[int]
    totalItemsClassified: NotRequired[int]
    totalItemsSensitive: NotRequired[int]
    totalItemsSkipped: NotRequired[int]
    totalItemsSkippedInvalidEncryption: NotRequired[int]
    totalItemsSkippedInvalidKms: NotRequired[int]
    totalItemsSkippedPermissionDenied: NotRequired[int]

class RetrievalConfigurationTypeDef(TypedDict):
    retrievalMode: RetrievalModeType
    externalId: NotRequired[str]
    roleName: NotRequired[str]

class RevealConfigurationTypeDef(TypedDict):
    status: RevealStatusType
    kmsKeyId: NotRequired[str]

class GetSensitiveDataOccurrencesAvailabilityRequestRequestTypeDef(TypedDict):
    findingId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetSensitiveDataOccurrencesRequestRequestTypeDef(TypedDict):
    findingId: str

GetSensitivityInspectionTemplateRequestRequestTypeDef = TypedDict(
    "GetSensitivityInspectionTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

class SensitivityInspectionTemplateExcludesOutputTypeDef(TypedDict):
    managedDataIdentifierIds: NotRequired[List[str]]

class SensitivityInspectionTemplateIncludesOutputTypeDef(TypedDict):
    allowListIds: NotRequired[List[str]]
    customDataIdentifierIds: NotRequired[List[str]]
    managedDataIdentifierIds: NotRequired[List[str]]

class UsageStatisticsFilterTypeDef(TypedDict):
    comparator: NotRequired[UsageStatisticsFilterComparatorType]
    key: NotRequired[UsageStatisticsFilterKeyType]
    values: NotRequired[Sequence[str]]

class UsageStatisticsSortByTypeDef(TypedDict):
    key: NotRequired[UsageStatisticsSortKeyType]
    orderBy: NotRequired[OrderByType]

class GetUsageTotalsRequestRequestTypeDef(TypedDict):
    timeRange: NotRequired[str]

UsageTotalTypeDef = TypedDict(
    "UsageTotalTypeDef",
    {
        "currency": NotRequired[Literal["USD"]],
        "estimatedCost": NotRequired[str],
        "type": NotRequired[UsageTypeType],
    },
)

class IamUserTypeDef(TypedDict):
    accountId: NotRequired[str]
    arn: NotRequired[str]
    principalId: NotRequired[str]
    userName: NotRequired[str]

class IpCityTypeDef(TypedDict):
    name: NotRequired[str]

class IpCountryTypeDef(TypedDict):
    code: NotRequired[str]
    name: NotRequired[str]

class IpGeoLocationTypeDef(TypedDict):
    lat: NotRequired[float]
    lon: NotRequired[float]

class IpOwnerTypeDef(TypedDict):
    asn: NotRequired[str]
    asnOrg: NotRequired[str]
    isp: NotRequired[str]
    org: NotRequired[str]

class MonthlyScheduleTypeDef(TypedDict):
    dayOfMonth: NotRequired[int]

class WeeklyScheduleTypeDef(TypedDict):
    dayOfWeek: NotRequired[DayOfWeekType]

class SimpleScopeTermOutputTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    key: NotRequired[ScopeFilterKeyType]
    values: NotRequired[List[str]]

class S3BucketDefinitionForJobOutputTypeDef(TypedDict):
    accountId: str
    buckets: List[str]

class ListAllowListsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAutomatedDiscoveryAccountsRequestRequestTypeDef(TypedDict):
    accountIds: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListJobsSortCriteriaTypeDef(TypedDict):
    attributeName: NotRequired[ListJobsSortAttributeNameType]
    orderBy: NotRequired[OrderByType]

class ListClassificationScopesRequestRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]

class ListCustomDataIdentifiersRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListFindingsFiltersRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListInvitationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListJobsFilterTermTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    key: NotRequired[ListJobsFilterKeyType]
    values: NotRequired[Sequence[str]]

class ListManagedDataIdentifiersRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]

ManagedDataIdentifierSummaryTypeDef = TypedDict(
    "ManagedDataIdentifierSummaryTypeDef",
    {
        "category": NotRequired[SensitiveDataItemCategoryType],
        "id": NotRequired[str],
    },
)

class ListMembersRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    onlyAssociated: NotRequired[str]

class MemberTypeDef(TypedDict):
    accountId: NotRequired[str]
    administratorAccountId: NotRequired[str]
    arn: NotRequired[str]
    email: NotRequired[str]
    invitedAt: NotRequired[datetime]
    masterAccountId: NotRequired[str]
    relationshipStatus: NotRequired[RelationshipStatusType]
    tags: NotRequired[Dict[str, str]]
    updatedAt: NotRequired[datetime]

class ListOrganizationAdminAccountsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListResourceProfileArtifactsRequestRequestTypeDef(TypedDict):
    resourceArn: str
    nextToken: NotRequired[str]

class ResourceProfileArtifactTypeDef(TypedDict):
    arn: str
    classificationResultStatus: str
    sensitive: NotRequired[bool]

class ListResourceProfileDetectionsRequestRequestTypeDef(TypedDict):
    resourceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSensitivityInspectionTemplatesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

SensitivityInspectionTemplatesEntryTypeDef = TypedDict(
    "SensitivityInspectionTemplatesEntryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class RangeTypeDef(TypedDict):
    end: NotRequired[int]
    start: NotRequired[int]
    startColumn: NotRequired[int]

class RecordTypeDef(TypedDict):
    jsonPath: NotRequired[str]
    recordIndex: NotRequired[int]

class S3BucketDefinitionForJobTypeDef(TypedDict):
    accountId: str
    buckets: Sequence[str]

S3BucketOwnerTypeDef = TypedDict(
    "S3BucketOwnerTypeDef",
    {
        "displayName": NotRequired[str],
        "id": NotRequired[str],
    },
)

class ServerSideEncryptionTypeDef(TypedDict):
    encryptionType: NotRequired[EncryptionTypeType]
    kmsMasterKeyId: NotRequired[str]

class S3ClassificationScopeExclusionTypeDef(TypedDict):
    bucketNames: List[str]

class S3ClassificationScopeExclusionUpdateTypeDef(TypedDict):
    bucketNames: Sequence[str]
    operation: ClassificationScopeUpdateOperationType

class SearchResourcesSimpleCriterionTypeDef(TypedDict):
    comparator: NotRequired[SearchResourcesComparatorType]
    key: NotRequired[SearchResourcesSimpleCriterionKeyType]
    values: NotRequired[Sequence[str]]

class SearchResourcesSortCriteriaTypeDef(TypedDict):
    attributeName: NotRequired[SearchResourcesSortAttributeNameType]
    orderBy: NotRequired[OrderByType]

class SearchResourcesTagCriterionPairTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class SensitivityInspectionTemplateExcludesTypeDef(TypedDict):
    managedDataIdentifierIds: NotRequired[Sequence[str]]

class SensitivityInspectionTemplateIncludesTypeDef(TypedDict):
    allowListIds: NotRequired[Sequence[str]]
    customDataIdentifierIds: NotRequired[Sequence[str]]
    managedDataIdentifierIds: NotRequired[Sequence[str]]

class ServiceLimitTypeDef(TypedDict):
    isServiceLimited: NotRequired[bool]
    unit: NotRequired[Literal["TERABYTES"]]
    value: NotRequired[int]

class SessionContextAttributesTypeDef(TypedDict):
    creationDate: NotRequired[datetime]
    mfaAuthenticated: NotRequired[bool]

SessionIssuerTypeDef = TypedDict(
    "SessionIssuerTypeDef",
    {
        "accountId": NotRequired[str],
        "arn": NotRequired[str],
        "principalId": NotRequired[str],
        "type": NotRequired[str],
        "userName": NotRequired[str],
    },
)

class SimpleCriterionForJobTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    key: NotRequired[SimpleCriterionKeyForJobType]
    values: NotRequired[Sequence[str]]

class SimpleScopeTermTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    key: NotRequired[ScopeFilterKeyType]
    values: NotRequired[Sequence[str]]

SuppressDataIdentifierTypeDef = TypedDict(
    "SuppressDataIdentifierTypeDef",
    {
        "id": NotRequired[str],
        "type": NotRequired[DataIdentifierTypeType],
    },
)

class TagCriterionPairForJobTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TagValuePairTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class TestCustomDataIdentifierRequestRequestTypeDef(TypedDict):
    regex: str
    sampleText: str
    ignoreWords: NotRequired[Sequence[str]]
    keywords: NotRequired[Sequence[str]]
    maximumMatchDistance: NotRequired[int]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAutomatedDiscoveryConfigurationRequestRequestTypeDef(TypedDict):
    status: AutomatedDiscoveryStatusType
    autoEnableOrganizationMembers: NotRequired[AutoEnableModeType]

class UpdateClassificationJobRequestRequestTypeDef(TypedDict):
    jobId: str
    jobStatus: JobStatusType

class UpdateMacieSessionRequestRequestTypeDef(TypedDict):
    findingPublishingFrequency: NotRequired[FindingPublishingFrequencyType]
    status: NotRequired[MacieStatusType]

UpdateMemberSessionRequestRequestTypeDef = TypedDict(
    "UpdateMemberSessionRequestRequestTypeDef",
    {
        "id": str,
        "status": MacieStatusType,
    },
)

class UpdateOrganizationConfigurationRequestRequestTypeDef(TypedDict):
    autoEnable: bool

class UpdateResourceProfileRequestRequestTypeDef(TypedDict):
    resourceArn: str
    sensitivityScoreOverride: NotRequired[int]

class UpdateRetrievalConfigurationTypeDef(TypedDict):
    retrievalMode: RetrievalModeType
    roleName: NotRequired[str]

class UserIdentityRootTypeDef(TypedDict):
    accountId: NotRequired[str]
    arn: NotRequired[str]
    principalId: NotRequired[str]

class CreateMemberRequestRequestTypeDef(TypedDict):
    account: AccountDetailTypeDef
    tags: NotRequired[Mapping[str, str]]

class AccountLevelPermissionsTypeDef(TypedDict):
    blockPublicAccess: NotRequired[BlockPublicAccessTypeDef]

class AllowListCriteriaTypeDef(TypedDict):
    regex: NotRequired[str]
    s3WordsList: NotRequired[S3WordsListTypeDef]

class FindingActionTypeDef(TypedDict):
    actionType: NotRequired[Literal["AWS_API_CALL"]]
    apiCallDetails: NotRequired[ApiCallDetailsTypeDef]

class BatchUpdateAutomatedDiscoveryAccountsRequestRequestTypeDef(TypedDict):
    accounts: NotRequired[Sequence[AutomatedDiscoveryAccountUpdateTypeDef]]

class BatchGetCustomDataIdentifiersResponseTypeDef(TypedDict):
    customDataIdentifiers: List[BatchGetCustomDataIdentifierSummaryTypeDef]
    notFoundIdentifierIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateAutomatedDiscoveryAccountsResponseTypeDef(TypedDict):
    errors: List[AutomatedDiscoveryAccountUpdateErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

CreateAllowListResponseTypeDef = TypedDict(
    "CreateAllowListResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateClassificationJobResponseTypeDef(TypedDict):
    jobArn: str
    jobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCustomDataIdentifierResponseTypeDef(TypedDict):
    customDataIdentifierId: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateFindingsFilterResponseTypeDef = TypedDict(
    "CreateFindingsFilterResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateMemberResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeOrganizationConfigurationResponseTypeDef(TypedDict):
    autoEnable: bool
    maxAccountLimitReached: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetAutomatedDiscoveryConfigurationResponseTypeDef(TypedDict):
    autoEnableOrganizationMembers: AutoEnableModeType
    classificationScopeId: str
    disabledAt: datetime
    firstEnabledAt: datetime
    lastUpdatedAt: datetime
    sensitivityInspectionTemplateId: str
    status: AutomatedDiscoveryStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetInvitationsCountResponseTypeDef(TypedDict):
    invitationsCount: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetMacieSessionResponseTypeDef(TypedDict):
    createdAt: datetime
    findingPublishingFrequency: FindingPublishingFrequencyType
    serviceRole: str
    status: MacieStatusType
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetMemberResponseTypeDef(TypedDict):
    accountId: str
    administratorAccountId: str
    arn: str
    email: str
    invitedAt: datetime
    masterAccountId: str
    relationshipStatus: RelationshipStatusType
    tags: Dict[str, str]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetSensitiveDataOccurrencesAvailabilityResponseTypeDef(TypedDict):
    code: AvailabilityCodeType
    reasons: List[UnavailabilityReasonCodeType]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAllowListsResponseTypeDef(TypedDict):
    allowLists: List[AllowListSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAutomatedDiscoveryAccountsResponseTypeDef(TypedDict):
    items: List[AutomatedDiscoveryAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFindingsResponseTypeDef(TypedDict):
    findingIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListOrganizationAdminAccountsResponseTypeDef(TypedDict):
    adminAccounts: List[AdminAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class TestCustomDataIdentifierResponseTypeDef(TypedDict):
    matchCount: int
    ResponseMetadata: ResponseMetadataTypeDef

UpdateAllowListResponseTypeDef = TypedDict(
    "UpdateAllowListResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFindingsFilterResponseTypeDef = TypedDict(
    "UpdateFindingsFilterResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class BucketLevelPermissionsTypeDef(TypedDict):
    accessControlList: NotRequired[AccessControlListTypeDef]
    blockPublicAccess: NotRequired[BlockPublicAccessTypeDef]
    bucketPolicy: NotRequired[BucketPolicyTypeDef]

class MatchingBucketTypeDef(TypedDict):
    accountId: NotRequired[str]
    automatedDiscoveryMonitoringStatus: NotRequired[AutomatedDiscoveryMonitoringStatusType]
    bucketName: NotRequired[str]
    classifiableObjectCount: NotRequired[int]
    classifiableSizeInBytes: NotRequired[int]
    errorCode: NotRequired[Literal["ACCESS_DENIED"]]
    errorMessage: NotRequired[str]
    jobDetails: NotRequired[JobDetailsTypeDef]
    lastAutomatedDiscoveryTime: NotRequired[datetime]
    objectCount: NotRequired[int]
    objectCountByEncryptionType: NotRequired[ObjectCountByEncryptionTypeTypeDef]
    sensitivityScore: NotRequired[int]
    sizeInBytes: NotRequired[int]
    sizeInBytesCompressed: NotRequired[int]
    unclassifiableObjectCount: NotRequired[ObjectLevelStatisticsTypeDef]
    unclassifiableObjectSizeInBytes: NotRequired[ObjectLevelStatisticsTypeDef]

class DescribeBucketsRequestRequestTypeDef(TypedDict):
    criteria: NotRequired[Mapping[str, BucketCriteriaAdditionalPropertiesTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortCriteria: NotRequired[BucketSortCriteriaTypeDef]

class BucketStatisticsBySensitivityTypeDef(TypedDict):
    classificationError: NotRequired[SensitivityAggregationsTypeDef]
    notClassified: NotRequired[SensitivityAggregationsTypeDef]
    notSensitive: NotRequired[SensitivityAggregationsTypeDef]
    sensitive: NotRequired[SensitivityAggregationsTypeDef]

class ClassificationExportConfigurationTypeDef(TypedDict):
    s3Destination: NotRequired[S3DestinationTypeDef]

class ListClassificationScopesResponseTypeDef(TypedDict):
    classificationScopes: List[ClassificationScopeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateCustomDataIdentifierRequestRequestTypeDef(TypedDict):
    name: str
    regex: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    ignoreWords: NotRequired[Sequence[str]]
    keywords: NotRequired[Sequence[str]]
    maximumMatchDistance: NotRequired[int]
    severityLevels: NotRequired[Sequence[SeverityLevelTypeDef]]
    tags: NotRequired[Mapping[str, str]]

GetCustomDataIdentifierResponseTypeDef = TypedDict(
    "GetCustomDataIdentifierResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deleted": bool,
        "description": str,
        "id": str,
        "ignoreWords": List[str],
        "keywords": List[str],
        "maximumMatchDistance": int,
        "name": str,
        "regex": str,
        "severityLevels": List[SeverityLevelTypeDef],
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateInvitationsResponseTypeDef(TypedDict):
    unprocessedAccounts: List[UnprocessedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeclineInvitationsResponseTypeDef(TypedDict):
    unprocessedAccounts: List[UnprocessedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInvitationsResponseTypeDef(TypedDict):
    unprocessedAccounts: List[UnprocessedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class FindingCriteriaOutputTypeDef(TypedDict):
    criterion: NotRequired[Dict[str, CriterionAdditionalPropertiesOutputTypeDef]]

CriterionAdditionalPropertiesUnionTypeDef = Union[
    CriterionAdditionalPropertiesTypeDef, CriterionAdditionalPropertiesOutputTypeDef
]

class ListCustomDataIdentifiersResponseTypeDef(TypedDict):
    items: List[CustomDataIdentifierSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeBucketsRequestDescribeBucketsPaginateTypeDef(TypedDict):
    criteria: NotRequired[Mapping[str, BucketCriteriaAdditionalPropertiesTypeDef]]
    sortCriteria: NotRequired[BucketSortCriteriaTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAllowListsRequestListAllowListsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAutomatedDiscoveryAccountsRequestListAutomatedDiscoveryAccountsPaginateTypeDef(TypedDict):
    accountIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClassificationScopesRequestListClassificationScopesPaginateTypeDef(TypedDict):
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomDataIdentifiersRequestListCustomDataIdentifiersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFindingsFiltersRequestListFindingsFiltersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInvitationsRequestListInvitationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListManagedDataIdentifiersRequestListManagedDataIdentifiersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMembersRequestListMembersPaginateTypeDef(TypedDict):
    onlyAssociated: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceProfileArtifactsRequestListResourceProfileArtifactsPaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceProfileDetectionsRequestListResourceProfileDetectionsPaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSensitivityInspectionTemplatesRequestListSensitivityInspectionTemplatesPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetSensitiveDataOccurrencesResponseTypeDef(TypedDict):
    error: str
    sensitiveDataOccurrences: Dict[str, List[DetectedDataDetailsTypeDef]]
    status: RevealRequestStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourceProfileDetectionsResponseTypeDef(TypedDict):
    detections: List[DetectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFindingsFiltersResponseTypeDef(TypedDict):
    findingsFilterListItems: List[FindingsFilterListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetAdministratorAccountResponseTypeDef(TypedDict):
    administrator: InvitationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMasterAccountResponseTypeDef(TypedDict):
    master: InvitationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListInvitationsResponseTypeDef(TypedDict):
    invitations: List[InvitationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetFindingStatisticsResponseTypeDef(TypedDict):
    countsByGroup: List[GroupCountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetFindingsPublicationConfigurationResponseTypeDef(TypedDict):
    securityHubConfiguration: SecurityHubConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutFindingsPublicationConfigurationRequestRequestTypeDef(TypedDict):
    clientToken: NotRequired[str]
    securityHubConfiguration: NotRequired[SecurityHubConfigurationTypeDef]

class GetFindingsRequestRequestTypeDef(TypedDict):
    findingIds: Sequence[str]
    sortCriteria: NotRequired[SortCriteriaTypeDef]

class GetResourceProfileResponseTypeDef(TypedDict):
    profileUpdatedAt: datetime
    sensitivityScore: int
    sensitivityScoreOverridden: bool
    statistics: ResourceStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRevealConfigurationResponseTypeDef(TypedDict):
    configuration: RevealConfigurationTypeDef
    retrievalConfiguration: RetrievalConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRevealConfigurationResponseTypeDef(TypedDict):
    configuration: RevealConfigurationTypeDef
    retrievalConfiguration: RetrievalConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSensitiveDataOccurrencesRequestFindingRevealedWaitTypeDef(TypedDict):
    findingId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetSensitivityInspectionTemplateResponseTypeDef(TypedDict):
    description: str
    excludes: SensitivityInspectionTemplateExcludesOutputTypeDef
    includes: SensitivityInspectionTemplateIncludesOutputTypeDef
    name: str
    sensitivityInspectionTemplateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetUsageStatisticsRequestGetUsageStatisticsPaginateTypeDef(TypedDict):
    filterBy: NotRequired[Sequence[UsageStatisticsFilterTypeDef]]
    sortBy: NotRequired[UsageStatisticsSortByTypeDef]
    timeRange: NotRequired[TimeRangeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetUsageStatisticsRequestRequestTypeDef(TypedDict):
    filterBy: NotRequired[Sequence[UsageStatisticsFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[UsageStatisticsSortByTypeDef]
    timeRange: NotRequired[TimeRangeType]

class GetUsageTotalsResponseTypeDef(TypedDict):
    timeRange: TimeRangeType
    usageTotals: List[UsageTotalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class IpAddressDetailsTypeDef(TypedDict):
    ipAddressV4: NotRequired[str]
    ipCity: NotRequired[IpCityTypeDef]
    ipCountry: NotRequired[IpCountryTypeDef]
    ipGeoLocation: NotRequired[IpGeoLocationTypeDef]
    ipOwner: NotRequired[IpOwnerTypeDef]

class JobScheduleFrequencyOutputTypeDef(TypedDict):
    dailySchedule: NotRequired[Dict[str, Any]]
    monthlySchedule: NotRequired[MonthlyScheduleTypeDef]
    weeklySchedule: NotRequired[WeeklyScheduleTypeDef]

class JobScheduleFrequencyTypeDef(TypedDict):
    dailySchedule: NotRequired[Mapping[str, Any]]
    monthlySchedule: NotRequired[MonthlyScheduleTypeDef]
    weeklySchedule: NotRequired[WeeklyScheduleTypeDef]

class ListJobsFilterCriteriaTypeDef(TypedDict):
    excludes: NotRequired[Sequence[ListJobsFilterTermTypeDef]]
    includes: NotRequired[Sequence[ListJobsFilterTermTypeDef]]

class ListManagedDataIdentifiersResponseTypeDef(TypedDict):
    items: List[ManagedDataIdentifierSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMembersResponseTypeDef(TypedDict):
    members: List[MemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListResourceProfileArtifactsResponseTypeDef(TypedDict):
    artifacts: List[ResourceProfileArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSensitivityInspectionTemplatesResponseTypeDef(TypedDict):
    sensitivityInspectionTemplates: List[SensitivityInspectionTemplatesEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PageTypeDef(TypedDict):
    lineRange: NotRequired[RangeTypeDef]
    offsetRange: NotRequired[RangeTypeDef]
    pageNumber: NotRequired[int]

S3BucketDefinitionForJobUnionTypeDef = Union[
    S3BucketDefinitionForJobTypeDef, S3BucketDefinitionForJobOutputTypeDef
]

class S3ObjectTypeDef(TypedDict):
    bucketArn: NotRequired[str]
    eTag: NotRequired[str]
    extension: NotRequired[str]
    key: NotRequired[str]
    lastModified: NotRequired[datetime]
    path: NotRequired[str]
    publicAccess: NotRequired[bool]
    serverSideEncryption: NotRequired[ServerSideEncryptionTypeDef]
    size: NotRequired[int]
    storageClass: NotRequired[StorageClassType]
    tags: NotRequired[List[KeyValuePairTypeDef]]
    versionId: NotRequired[str]

class S3ClassificationScopeTypeDef(TypedDict):
    excludes: S3ClassificationScopeExclusionTypeDef

class S3ClassificationScopeUpdateTypeDef(TypedDict):
    excludes: S3ClassificationScopeExclusionUpdateTypeDef

class SearchResourcesTagCriterionTypeDef(TypedDict):
    comparator: NotRequired[SearchResourcesComparatorType]
    tagValues: NotRequired[Sequence[SearchResourcesTagCriterionPairTypeDef]]

UpdateSensitivityInspectionTemplateRequestRequestTypeDef = TypedDict(
    "UpdateSensitivityInspectionTemplateRequestRequestTypeDef",
    {
        "id": str,
        "description": NotRequired[str],
        "excludes": NotRequired[SensitivityInspectionTemplateExcludesTypeDef],
        "includes": NotRequired[SensitivityInspectionTemplateIncludesTypeDef],
    },
)
UsageByAccountTypeDef = TypedDict(
    "UsageByAccountTypeDef",
    {
        "currency": NotRequired[Literal["USD"]],
        "estimatedCost": NotRequired[str],
        "serviceLimit": NotRequired[ServiceLimitTypeDef],
        "type": NotRequired[UsageTypeType],
    },
)

class SessionContextTypeDef(TypedDict):
    attributes: NotRequired[SessionContextAttributesTypeDef]
    sessionIssuer: NotRequired[SessionIssuerTypeDef]

SimpleCriterionForJobUnionTypeDef = Union[
    SimpleCriterionForJobTypeDef, SimpleCriterionForJobOutputTypeDef
]
SimpleScopeTermUnionTypeDef = Union[SimpleScopeTermTypeDef, SimpleScopeTermOutputTypeDef]

class UpdateResourceProfileDetectionsRequestRequestTypeDef(TypedDict):
    resourceArn: str
    suppressDataIdentifiers: NotRequired[Sequence[SuppressDataIdentifierTypeDef]]

class TagCriterionForJobOutputTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    tagValues: NotRequired[List[TagCriterionPairForJobTypeDef]]

class TagCriterionForJobTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    tagValues: NotRequired[Sequence[TagCriterionPairForJobTypeDef]]

class TagScopeTermOutputTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    key: NotRequired[str]
    tagValues: NotRequired[List[TagValuePairTypeDef]]
    target: NotRequired[Literal["S3_OBJECT"]]

class TagScopeTermTypeDef(TypedDict):
    comparator: NotRequired[JobComparatorType]
    key: NotRequired[str]
    tagValues: NotRequired[Sequence[TagValuePairTypeDef]]
    target: NotRequired[Literal["S3_OBJECT"]]

class UpdateRevealConfigurationRequestRequestTypeDef(TypedDict):
    configuration: RevealConfigurationTypeDef
    retrievalConfiguration: NotRequired[UpdateRetrievalConfigurationTypeDef]

class CreateAllowListRequestRequestTypeDef(TypedDict):
    clientToken: str
    criteria: AllowListCriteriaTypeDef
    name: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

GetAllowListResponseTypeDef = TypedDict(
    "GetAllowListResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "criteria": AllowListCriteriaTypeDef,
        "description": str,
        "id": str,
        "name": str,
        "status": AllowListStatusTypeDef,
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAllowListRequestRequestTypeDef = TypedDict(
    "UpdateAllowListRequestRequestTypeDef",
    {
        "criteria": AllowListCriteriaTypeDef,
        "id": str,
        "name": str,
        "description": NotRequired[str],
    },
)

class BucketPermissionConfigurationTypeDef(TypedDict):
    accountLevelPermissions: NotRequired[AccountLevelPermissionsTypeDef]
    bucketLevelPermissions: NotRequired[BucketLevelPermissionsTypeDef]

class MatchingResourceTypeDef(TypedDict):
    matchingBucket: NotRequired[MatchingBucketTypeDef]

class GetBucketStatisticsResponseTypeDef(TypedDict):
    bucketCount: int
    bucketCountByEffectivePermission: BucketCountByEffectivePermissionTypeDef
    bucketCountByEncryptionType: BucketCountByEncryptionTypeTypeDef
    bucketCountByObjectEncryptionRequirement: BucketCountPolicyAllowsUnencryptedObjectUploadsTypeDef
    bucketCountBySharedAccessType: BucketCountBySharedAccessTypeTypeDef
    bucketStatisticsBySensitivity: BucketStatisticsBySensitivityTypeDef
    classifiableObjectCount: int
    classifiableSizeInBytes: int
    lastUpdated: datetime
    objectCount: int
    sizeInBytes: int
    sizeInBytesCompressed: int
    unclassifiableObjectCount: ObjectLevelStatisticsTypeDef
    unclassifiableObjectSizeInBytes: ObjectLevelStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetClassificationExportConfigurationResponseTypeDef(TypedDict):
    configuration: ClassificationExportConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutClassificationExportConfigurationRequestRequestTypeDef(TypedDict):
    configuration: ClassificationExportConfigurationTypeDef

class PutClassificationExportConfigurationResponseTypeDef(TypedDict):
    configuration: ClassificationExportConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

GetFindingsFilterResponseTypeDef = TypedDict(
    "GetFindingsFilterResponseTypeDef",
    {
        "action": FindingsFilterActionType,
        "arn": str,
        "description": str,
        "findingCriteria": FindingCriteriaOutputTypeDef,
        "id": str,
        "name": str,
        "position": int,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class FindingCriteriaTypeDef(TypedDict):
    criterion: NotRequired[Mapping[str, CriterionAdditionalPropertiesUnionTypeDef]]

class ListClassificationJobsRequestListClassificationJobsPaginateTypeDef(TypedDict):
    filterCriteria: NotRequired[ListJobsFilterCriteriaTypeDef]
    sortCriteria: NotRequired[ListJobsSortCriteriaTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClassificationJobsRequestRequestTypeDef(TypedDict):
    filterCriteria: NotRequired[ListJobsFilterCriteriaTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortCriteria: NotRequired[ListJobsSortCriteriaTypeDef]

class OccurrencesTypeDef(TypedDict):
    cells: NotRequired[List[CellTypeDef]]
    lineRanges: NotRequired[List[RangeTypeDef]]
    offsetRanges: NotRequired[List[RangeTypeDef]]
    pages: NotRequired[List[PageTypeDef]]
    records: NotRequired[List[RecordTypeDef]]

GetClassificationScopeResponseTypeDef = TypedDict(
    "GetClassificationScopeResponseTypeDef",
    {
        "id": str,
        "name": str,
        "s3": S3ClassificationScopeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateClassificationScopeRequestRequestTypeDef = TypedDict(
    "UpdateClassificationScopeRequestRequestTypeDef",
    {
        "id": str,
        "s3": NotRequired[S3ClassificationScopeUpdateTypeDef],
    },
)

class SearchResourcesCriteriaTypeDef(TypedDict):
    simpleCriterion: NotRequired[SearchResourcesSimpleCriterionTypeDef]
    tagCriterion: NotRequired[SearchResourcesTagCriterionTypeDef]

class UsageRecordTypeDef(TypedDict):
    accountId: NotRequired[str]
    automatedDiscoveryFreeTrialStartDate: NotRequired[datetime]
    freeTrialStartDate: NotRequired[datetime]
    usage: NotRequired[List[UsageByAccountTypeDef]]

class AssumedRoleTypeDef(TypedDict):
    accessKeyId: NotRequired[str]
    accountId: NotRequired[str]
    arn: NotRequired[str]
    principalId: NotRequired[str]
    sessionContext: NotRequired[SessionContextTypeDef]

class FederatedUserTypeDef(TypedDict):
    accessKeyId: NotRequired[str]
    accountId: NotRequired[str]
    arn: NotRequired[str]
    principalId: NotRequired[str]
    sessionContext: NotRequired[SessionContextTypeDef]

class CriteriaForJobOutputTypeDef(TypedDict):
    simpleCriterion: NotRequired[SimpleCriterionForJobOutputTypeDef]
    tagCriterion: NotRequired[TagCriterionForJobOutputTypeDef]

TagCriterionForJobUnionTypeDef = Union[TagCriterionForJobTypeDef, TagCriterionForJobOutputTypeDef]

class JobScopeTermOutputTypeDef(TypedDict):
    simpleScopeTerm: NotRequired[SimpleScopeTermOutputTypeDef]
    tagScopeTerm: NotRequired[TagScopeTermOutputTypeDef]

TagScopeTermUnionTypeDef = Union[TagScopeTermTypeDef, TagScopeTermOutputTypeDef]

class BucketPublicAccessTypeDef(TypedDict):
    effectivePermission: NotRequired[EffectivePermissionType]
    permissionConfiguration: NotRequired[BucketPermissionConfigurationTypeDef]

class SearchResourcesResponseTypeDef(TypedDict):
    matchingResources: List[MatchingResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateFindingsFilterRequestRequestTypeDef(TypedDict):
    action: FindingsFilterActionType
    findingCriteria: FindingCriteriaTypeDef
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    position: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]

class GetFindingStatisticsRequestRequestTypeDef(TypedDict):
    groupBy: GroupByType
    findingCriteria: NotRequired[FindingCriteriaTypeDef]
    size: NotRequired[int]
    sortCriteria: NotRequired[FindingStatisticsSortCriteriaTypeDef]

class ListFindingsRequestListFindingsPaginateTypeDef(TypedDict):
    findingCriteria: NotRequired[FindingCriteriaTypeDef]
    sortCriteria: NotRequired[SortCriteriaTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFindingsRequestRequestTypeDef(TypedDict):
    findingCriteria: NotRequired[FindingCriteriaTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortCriteria: NotRequired[SortCriteriaTypeDef]

UpdateFindingsFilterRequestRequestTypeDef = TypedDict(
    "UpdateFindingsFilterRequestRequestTypeDef",
    {
        "id": str,
        "action": NotRequired[FindingsFilterActionType],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "findingCriteria": NotRequired[FindingCriteriaTypeDef],
        "name": NotRequired[str],
        "position": NotRequired[int],
    },
)

class CustomDetectionTypeDef(TypedDict):
    arn: NotRequired[str]
    count: NotRequired[int]
    name: NotRequired[str]
    occurrences: NotRequired[OccurrencesTypeDef]

DefaultDetectionTypeDef = TypedDict(
    "DefaultDetectionTypeDef",
    {
        "count": NotRequired[int],
        "occurrences": NotRequired[OccurrencesTypeDef],
        "type": NotRequired[str],
    },
)
SearchResourcesCriteriaBlockTypeDef = TypedDict(
    "SearchResourcesCriteriaBlockTypeDef",
    {
        "and": NotRequired[Sequence[SearchResourcesCriteriaTypeDef]],
    },
)

class GetUsageStatisticsResponseTypeDef(TypedDict):
    records: List[UsageRecordTypeDef]
    timeRange: TimeRangeType
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "assumedRole": NotRequired[AssumedRoleTypeDef],
        "awsAccount": NotRequired[AwsAccountTypeDef],
        "awsService": NotRequired[AwsServiceTypeDef],
        "federatedUser": NotRequired[FederatedUserTypeDef],
        "iamUser": NotRequired[IamUserTypeDef],
        "root": NotRequired[UserIdentityRootTypeDef],
        "type": NotRequired[UserIdentityTypeType],
    },
)
CriteriaBlockForJobOutputTypeDef = TypedDict(
    "CriteriaBlockForJobOutputTypeDef",
    {
        "and": NotRequired[List[CriteriaForJobOutputTypeDef]],
    },
)

class CriteriaForJobTypeDef(TypedDict):
    simpleCriterion: NotRequired[SimpleCriterionForJobUnionTypeDef]
    tagCriterion: NotRequired[TagCriterionForJobUnionTypeDef]

JobScopingBlockOutputTypeDef = TypedDict(
    "JobScopingBlockOutputTypeDef",
    {
        "and": NotRequired[List[JobScopeTermOutputTypeDef]],
    },
)

class JobScopeTermTypeDef(TypedDict):
    simpleScopeTerm: NotRequired[SimpleScopeTermUnionTypeDef]
    tagScopeTerm: NotRequired[TagScopeTermUnionTypeDef]

class BucketMetadataTypeDef(TypedDict):
    accountId: NotRequired[str]
    allowsUnencryptedObjectUploads: NotRequired[AllowsUnencryptedObjectUploadsType]
    automatedDiscoveryMonitoringStatus: NotRequired[AutomatedDiscoveryMonitoringStatusType]
    bucketArn: NotRequired[str]
    bucketCreatedAt: NotRequired[datetime]
    bucketName: NotRequired[str]
    classifiableObjectCount: NotRequired[int]
    classifiableSizeInBytes: NotRequired[int]
    errorCode: NotRequired[Literal["ACCESS_DENIED"]]
    errorMessage: NotRequired[str]
    jobDetails: NotRequired[JobDetailsTypeDef]
    lastAutomatedDiscoveryTime: NotRequired[datetime]
    lastUpdated: NotRequired[datetime]
    objectCount: NotRequired[int]
    objectCountByEncryptionType: NotRequired[ObjectCountByEncryptionTypeTypeDef]
    publicAccess: NotRequired[BucketPublicAccessTypeDef]
    region: NotRequired[str]
    replicationDetails: NotRequired[ReplicationDetailsTypeDef]
    sensitivityScore: NotRequired[int]
    serverSideEncryption: NotRequired[BucketServerSideEncryptionTypeDef]
    sharedAccess: NotRequired[SharedAccessType]
    sizeInBytes: NotRequired[int]
    sizeInBytesCompressed: NotRequired[int]
    tags: NotRequired[List[KeyValuePairTypeDef]]
    unclassifiableObjectCount: NotRequired[ObjectLevelStatisticsTypeDef]
    unclassifiableObjectSizeInBytes: NotRequired[ObjectLevelStatisticsTypeDef]
    versioning: NotRequired[bool]

class S3BucketTypeDef(TypedDict):
    allowsUnencryptedObjectUploads: NotRequired[AllowsUnencryptedObjectUploadsType]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    defaultServerSideEncryption: NotRequired[ServerSideEncryptionTypeDef]
    name: NotRequired[str]
    owner: NotRequired[S3BucketOwnerTypeDef]
    publicAccess: NotRequired[BucketPublicAccessTypeDef]
    tags: NotRequired[List[KeyValuePairTypeDef]]

class CustomDataIdentifiersTypeDef(TypedDict):
    detections: NotRequired[List[CustomDetectionTypeDef]]
    totalCount: NotRequired[int]

class SensitiveDataItemTypeDef(TypedDict):
    category: NotRequired[SensitiveDataItemCategoryType]
    detections: NotRequired[List[DefaultDetectionTypeDef]]
    totalCount: NotRequired[int]

class SearchResourcesBucketCriteriaTypeDef(TypedDict):
    excludes: NotRequired[SearchResourcesCriteriaBlockTypeDef]
    includes: NotRequired[SearchResourcesCriteriaBlockTypeDef]

class FindingActorTypeDef(TypedDict):
    domainDetails: NotRequired[DomainDetailsTypeDef]
    ipAddressDetails: NotRequired[IpAddressDetailsTypeDef]
    userIdentity: NotRequired[UserIdentityTypeDef]

class S3BucketCriteriaForJobOutputTypeDef(TypedDict):
    excludes: NotRequired[CriteriaBlockForJobOutputTypeDef]
    includes: NotRequired[CriteriaBlockForJobOutputTypeDef]

CriteriaForJobUnionTypeDef = Union[CriteriaForJobTypeDef, CriteriaForJobOutputTypeDef]

class ScopingOutputTypeDef(TypedDict):
    excludes: NotRequired[JobScopingBlockOutputTypeDef]
    includes: NotRequired[JobScopingBlockOutputTypeDef]

JobScopeTermUnionTypeDef = Union[JobScopeTermTypeDef, JobScopeTermOutputTypeDef]

class DescribeBucketsResponseTypeDef(TypedDict):
    buckets: List[BucketMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ResourcesAffectedTypeDef(TypedDict):
    s3Bucket: NotRequired[S3BucketTypeDef]
    s3Object: NotRequired[S3ObjectTypeDef]

class ClassificationResultTypeDef(TypedDict):
    additionalOccurrences: NotRequired[bool]
    customDataIdentifiers: NotRequired[CustomDataIdentifiersTypeDef]
    mimeType: NotRequired[str]
    sensitiveData: NotRequired[List[SensitiveDataItemTypeDef]]
    sizeClassified: NotRequired[int]
    status: NotRequired[ClassificationResultStatusTypeDef]

class SearchResourcesRequestRequestTypeDef(TypedDict):
    bucketCriteria: NotRequired[SearchResourcesBucketCriteriaTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortCriteria: NotRequired[SearchResourcesSortCriteriaTypeDef]

class SearchResourcesRequestSearchResourcesPaginateTypeDef(TypedDict):
    bucketCriteria: NotRequired[SearchResourcesBucketCriteriaTypeDef]
    sortCriteria: NotRequired[SearchResourcesSortCriteriaTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class PolicyDetailsTypeDef(TypedDict):
    action: NotRequired[FindingActionTypeDef]
    actor: NotRequired[FindingActorTypeDef]

class JobSummaryTypeDef(TypedDict):
    bucketCriteria: NotRequired[S3BucketCriteriaForJobOutputTypeDef]
    bucketDefinitions: NotRequired[List[S3BucketDefinitionForJobOutputTypeDef]]
    createdAt: NotRequired[datetime]
    jobId: NotRequired[str]
    jobStatus: NotRequired[JobStatusType]
    jobType: NotRequired[JobTypeType]
    lastRunErrorStatus: NotRequired[LastRunErrorStatusTypeDef]
    name: NotRequired[str]
    userPausedDetails: NotRequired[UserPausedDetailsTypeDef]

CriteriaBlockForJobTypeDef = TypedDict(
    "CriteriaBlockForJobTypeDef",
    {
        "and": NotRequired[Sequence[CriteriaForJobUnionTypeDef]],
    },
)

class S3JobDefinitionOutputTypeDef(TypedDict):
    bucketCriteria: NotRequired[S3BucketCriteriaForJobOutputTypeDef]
    bucketDefinitions: NotRequired[List[S3BucketDefinitionForJobOutputTypeDef]]
    scoping: NotRequired[ScopingOutputTypeDef]

JobScopingBlockTypeDef = TypedDict(
    "JobScopingBlockTypeDef",
    {
        "and": NotRequired[Sequence[JobScopeTermUnionTypeDef]],
    },
)

class ClassificationDetailsTypeDef(TypedDict):
    detailedResultsLocation: NotRequired[str]
    jobArn: NotRequired[str]
    jobId: NotRequired[str]
    originType: NotRequired[OriginTypeType]
    result: NotRequired[ClassificationResultTypeDef]

class ListClassificationJobsResponseTypeDef(TypedDict):
    items: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CriteriaBlockForJobUnionTypeDef = Union[
    CriteriaBlockForJobTypeDef, CriteriaBlockForJobOutputTypeDef
]

class DescribeClassificationJobResponseTypeDef(TypedDict):
    allowListIds: List[str]
    clientToken: str
    createdAt: datetime
    customDataIdentifierIds: List[str]
    description: str
    initialRun: bool
    jobArn: str
    jobId: str
    jobStatus: JobStatusType
    jobType: JobTypeType
    lastRunErrorStatus: LastRunErrorStatusTypeDef
    lastRunTime: datetime
    managedDataIdentifierIds: List[str]
    managedDataIdentifierSelector: ManagedDataIdentifierSelectorType
    name: str
    s3JobDefinition: S3JobDefinitionOutputTypeDef
    samplingPercentage: int
    scheduleFrequency: JobScheduleFrequencyOutputTypeDef
    statistics: StatisticsTypeDef
    tags: Dict[str, str]
    userPausedDetails: UserPausedDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

JobScopingBlockUnionTypeDef = Union[JobScopingBlockTypeDef, JobScopingBlockOutputTypeDef]
FindingTypeDef = TypedDict(
    "FindingTypeDef",
    {
        "accountId": NotRequired[str],
        "archived": NotRequired[bool],
        "category": NotRequired[FindingCategoryType],
        "classificationDetails": NotRequired[ClassificationDetailsTypeDef],
        "count": NotRequired[int],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "partition": NotRequired[str],
        "policyDetails": NotRequired[PolicyDetailsTypeDef],
        "region": NotRequired[str],
        "resourcesAffected": NotRequired[ResourcesAffectedTypeDef],
        "sample": NotRequired[bool],
        "schemaVersion": NotRequired[str],
        "severity": NotRequired[SeverityTypeDef],
        "title": NotRequired[str],
        "type": NotRequired[FindingTypeType],
        "updatedAt": NotRequired[datetime],
    },
)

class S3BucketCriteriaForJobTypeDef(TypedDict):
    excludes: NotRequired[CriteriaBlockForJobUnionTypeDef]
    includes: NotRequired[CriteriaBlockForJobUnionTypeDef]

class ScopingTypeDef(TypedDict):
    excludes: NotRequired[JobScopingBlockUnionTypeDef]
    includes: NotRequired[JobScopingBlockUnionTypeDef]

class GetFindingsResponseTypeDef(TypedDict):
    findings: List[FindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

S3BucketCriteriaForJobUnionTypeDef = Union[
    S3BucketCriteriaForJobTypeDef, S3BucketCriteriaForJobOutputTypeDef
]
ScopingUnionTypeDef = Union[ScopingTypeDef, ScopingOutputTypeDef]

class S3JobDefinitionTypeDef(TypedDict):
    bucketCriteria: NotRequired[S3BucketCriteriaForJobUnionTypeDef]
    bucketDefinitions: NotRequired[Sequence[S3BucketDefinitionForJobUnionTypeDef]]
    scoping: NotRequired[ScopingUnionTypeDef]

class CreateClassificationJobRequestRequestTypeDef(TypedDict):
    clientToken: str
    jobType: JobTypeType
    name: str
    s3JobDefinition: S3JobDefinitionTypeDef
    allowListIds: NotRequired[Sequence[str]]
    customDataIdentifierIds: NotRequired[Sequence[str]]
    description: NotRequired[str]
    initialRun: NotRequired[bool]
    managedDataIdentifierIds: NotRequired[Sequence[str]]
    managedDataIdentifierSelector: NotRequired[ManagedDataIdentifierSelectorType]
    samplingPercentage: NotRequired[int]
    scheduleFrequency: NotRequired[JobScheduleFrequencyTypeDef]
    tags: NotRequired[Mapping[str, str]]
