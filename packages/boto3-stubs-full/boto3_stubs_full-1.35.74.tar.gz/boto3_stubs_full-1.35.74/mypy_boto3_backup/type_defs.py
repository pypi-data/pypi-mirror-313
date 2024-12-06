"""
Type annotations for backup service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/type_defs/)

Usage::

    ```python
    from mypy_boto3_backup.type_defs import AdvancedBackupSettingOutputTypeDef

    data: AdvancedBackupSettingOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AggregationPeriodType,
    BackupJobStateType,
    BackupJobStatusType,
    BackupVaultEventType,
    CopyJobStateType,
    CopyJobStatusType,
    LegalHoldStatusType,
    RecoveryPointStatusType,
    RestoreDeletionStatusType,
    RestoreJobStateType,
    RestoreJobStatusType,
    RestoreTestingRecoveryPointSelectionAlgorithmType,
    RestoreTestingRecoveryPointTypeType,
    RestoreValidationStatusType,
    StorageClassType,
    VaultStateType,
    VaultTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AdvancedBackupSettingOutputTypeDef",
    "AdvancedBackupSettingTypeDef",
    "AdvancedBackupSettingUnionTypeDef",
    "BackupJobSummaryTypeDef",
    "BackupJobTypeDef",
    "BackupPlanInputTypeDef",
    "BackupPlanTemplatesListMemberTypeDef",
    "BackupPlanTypeDef",
    "BackupPlansListMemberTypeDef",
    "BackupRuleInputTypeDef",
    "BackupRuleTypeDef",
    "BackupSelectionOutputTypeDef",
    "BackupSelectionTypeDef",
    "BackupSelectionsListMemberTypeDef",
    "BackupVaultListMemberTypeDef",
    "CalculatedLifecycleTypeDef",
    "CancelLegalHoldInputRequestTypeDef",
    "ConditionParameterTypeDef",
    "ConditionTypeDef",
    "ConditionsOutputTypeDef",
    "ConditionsTypeDef",
    "ConditionsUnionTypeDef",
    "ControlInputParameterTypeDef",
    "ControlScopeOutputTypeDef",
    "ControlScopeTypeDef",
    "ControlScopeUnionTypeDef",
    "CopyActionTypeDef",
    "CopyJobSummaryTypeDef",
    "CopyJobTypeDef",
    "CreateBackupPlanInputRequestTypeDef",
    "CreateBackupPlanOutputTypeDef",
    "CreateBackupSelectionInputRequestTypeDef",
    "CreateBackupSelectionOutputTypeDef",
    "CreateBackupVaultInputRequestTypeDef",
    "CreateBackupVaultOutputTypeDef",
    "CreateFrameworkInputRequestTypeDef",
    "CreateFrameworkOutputTypeDef",
    "CreateLegalHoldInputRequestTypeDef",
    "CreateLegalHoldOutputTypeDef",
    "CreateLogicallyAirGappedBackupVaultInputRequestTypeDef",
    "CreateLogicallyAirGappedBackupVaultOutputTypeDef",
    "CreateReportPlanInputRequestTypeDef",
    "CreateReportPlanOutputTypeDef",
    "CreateRestoreTestingPlanInputRequestTypeDef",
    "CreateRestoreTestingPlanOutputTypeDef",
    "CreateRestoreTestingSelectionInputRequestTypeDef",
    "CreateRestoreTestingSelectionOutputTypeDef",
    "DateRangeOutputTypeDef",
    "DateRangeTypeDef",
    "DateRangeUnionTypeDef",
    "DeleteBackupPlanInputRequestTypeDef",
    "DeleteBackupPlanOutputTypeDef",
    "DeleteBackupSelectionInputRequestTypeDef",
    "DeleteBackupVaultAccessPolicyInputRequestTypeDef",
    "DeleteBackupVaultInputRequestTypeDef",
    "DeleteBackupVaultLockConfigurationInputRequestTypeDef",
    "DeleteBackupVaultNotificationsInputRequestTypeDef",
    "DeleteFrameworkInputRequestTypeDef",
    "DeleteRecoveryPointInputRequestTypeDef",
    "DeleteReportPlanInputRequestTypeDef",
    "DeleteRestoreTestingPlanInputRequestTypeDef",
    "DeleteRestoreTestingSelectionInputRequestTypeDef",
    "DescribeBackupJobInputRequestTypeDef",
    "DescribeBackupJobOutputTypeDef",
    "DescribeBackupVaultInputRequestTypeDef",
    "DescribeBackupVaultOutputTypeDef",
    "DescribeCopyJobInputRequestTypeDef",
    "DescribeCopyJobOutputTypeDef",
    "DescribeFrameworkInputRequestTypeDef",
    "DescribeFrameworkOutputTypeDef",
    "DescribeGlobalSettingsOutputTypeDef",
    "DescribeProtectedResourceInputRequestTypeDef",
    "DescribeProtectedResourceOutputTypeDef",
    "DescribeRecoveryPointInputRequestTypeDef",
    "DescribeRecoveryPointOutputTypeDef",
    "DescribeRegionSettingsOutputTypeDef",
    "DescribeReportJobInputRequestTypeDef",
    "DescribeReportJobOutputTypeDef",
    "DescribeReportPlanInputRequestTypeDef",
    "DescribeReportPlanOutputTypeDef",
    "DescribeRestoreJobInputRequestTypeDef",
    "DescribeRestoreJobOutputTypeDef",
    "DisassociateRecoveryPointFromParentInputRequestTypeDef",
    "DisassociateRecoveryPointInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportBackupPlanTemplateInputRequestTypeDef",
    "ExportBackupPlanTemplateOutputTypeDef",
    "FrameworkControlOutputTypeDef",
    "FrameworkControlTypeDef",
    "FrameworkControlUnionTypeDef",
    "FrameworkTypeDef",
    "GetBackupPlanFromJSONInputRequestTypeDef",
    "GetBackupPlanFromJSONOutputTypeDef",
    "GetBackupPlanFromTemplateInputRequestTypeDef",
    "GetBackupPlanFromTemplateOutputTypeDef",
    "GetBackupPlanInputRequestTypeDef",
    "GetBackupPlanOutputTypeDef",
    "GetBackupSelectionInputRequestTypeDef",
    "GetBackupSelectionOutputTypeDef",
    "GetBackupVaultAccessPolicyInputRequestTypeDef",
    "GetBackupVaultAccessPolicyOutputTypeDef",
    "GetBackupVaultNotificationsInputRequestTypeDef",
    "GetBackupVaultNotificationsOutputTypeDef",
    "GetLegalHoldInputRequestTypeDef",
    "GetLegalHoldOutputTypeDef",
    "GetRecoveryPointRestoreMetadataInputRequestTypeDef",
    "GetRecoveryPointRestoreMetadataOutputTypeDef",
    "GetRestoreJobMetadataInputRequestTypeDef",
    "GetRestoreJobMetadataOutputTypeDef",
    "GetRestoreTestingInferredMetadataInputRequestTypeDef",
    "GetRestoreTestingInferredMetadataOutputTypeDef",
    "GetRestoreTestingPlanInputRequestTypeDef",
    "GetRestoreTestingPlanOutputTypeDef",
    "GetRestoreTestingSelectionInputRequestTypeDef",
    "GetRestoreTestingSelectionOutputTypeDef",
    "GetSupportedResourceTypesOutputTypeDef",
    "KeyValueTypeDef",
    "LegalHoldTypeDef",
    "LifecycleTypeDef",
    "ListBackupJobSummariesInputRequestTypeDef",
    "ListBackupJobSummariesOutputTypeDef",
    "ListBackupJobsInputListBackupJobsPaginateTypeDef",
    "ListBackupJobsInputRequestTypeDef",
    "ListBackupJobsOutputTypeDef",
    "ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef",
    "ListBackupPlanTemplatesInputRequestTypeDef",
    "ListBackupPlanTemplatesOutputTypeDef",
    "ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef",
    "ListBackupPlanVersionsInputRequestTypeDef",
    "ListBackupPlanVersionsOutputTypeDef",
    "ListBackupPlansInputListBackupPlansPaginateTypeDef",
    "ListBackupPlansInputRequestTypeDef",
    "ListBackupPlansOutputTypeDef",
    "ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef",
    "ListBackupSelectionsInputRequestTypeDef",
    "ListBackupSelectionsOutputTypeDef",
    "ListBackupVaultsInputListBackupVaultsPaginateTypeDef",
    "ListBackupVaultsInputRequestTypeDef",
    "ListBackupVaultsOutputTypeDef",
    "ListCopyJobSummariesInputRequestTypeDef",
    "ListCopyJobSummariesOutputTypeDef",
    "ListCopyJobsInputListCopyJobsPaginateTypeDef",
    "ListCopyJobsInputRequestTypeDef",
    "ListCopyJobsOutputTypeDef",
    "ListFrameworksInputRequestTypeDef",
    "ListFrameworksOutputTypeDef",
    "ListLegalHoldsInputListLegalHoldsPaginateTypeDef",
    "ListLegalHoldsInputRequestTypeDef",
    "ListLegalHoldsOutputTypeDef",
    "ListProtectedResourcesByBackupVaultInputListProtectedResourcesByBackupVaultPaginateTypeDef",
    "ListProtectedResourcesByBackupVaultInputRequestTypeDef",
    "ListProtectedResourcesByBackupVaultOutputTypeDef",
    "ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef",
    "ListProtectedResourcesInputRequestTypeDef",
    "ListProtectedResourcesOutputTypeDef",
    "ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef",
    "ListRecoveryPointsByBackupVaultInputRequestTypeDef",
    "ListRecoveryPointsByBackupVaultOutputTypeDef",
    "ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef",
    "ListRecoveryPointsByLegalHoldInputRequestTypeDef",
    "ListRecoveryPointsByLegalHoldOutputTypeDef",
    "ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef",
    "ListRecoveryPointsByResourceInputRequestTypeDef",
    "ListRecoveryPointsByResourceOutputTypeDef",
    "ListReportJobsInputRequestTypeDef",
    "ListReportJobsOutputTypeDef",
    "ListReportPlansInputRequestTypeDef",
    "ListReportPlansOutputTypeDef",
    "ListRestoreJobSummariesInputRequestTypeDef",
    "ListRestoreJobSummariesOutputTypeDef",
    "ListRestoreJobsByProtectedResourceInputListRestoreJobsByProtectedResourcePaginateTypeDef",
    "ListRestoreJobsByProtectedResourceInputRequestTypeDef",
    "ListRestoreJobsByProtectedResourceOutputTypeDef",
    "ListRestoreJobsInputListRestoreJobsPaginateTypeDef",
    "ListRestoreJobsInputRequestTypeDef",
    "ListRestoreJobsOutputTypeDef",
    "ListRestoreTestingPlansInputListRestoreTestingPlansPaginateTypeDef",
    "ListRestoreTestingPlansInputRequestTypeDef",
    "ListRestoreTestingPlansOutputTypeDef",
    "ListRestoreTestingSelectionsInputListRestoreTestingSelectionsPaginateTypeDef",
    "ListRestoreTestingSelectionsInputRequestTypeDef",
    "ListRestoreTestingSelectionsOutputTypeDef",
    "ListTagsInputRequestTypeDef",
    "ListTagsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ProtectedResourceConditionsOutputTypeDef",
    "ProtectedResourceConditionsTypeDef",
    "ProtectedResourceConditionsUnionTypeDef",
    "ProtectedResourceTypeDef",
    "PutBackupVaultAccessPolicyInputRequestTypeDef",
    "PutBackupVaultLockConfigurationInputRequestTypeDef",
    "PutBackupVaultNotificationsInputRequestTypeDef",
    "PutRestoreValidationResultInputRequestTypeDef",
    "RecoveryPointByBackupVaultTypeDef",
    "RecoveryPointByResourceTypeDef",
    "RecoveryPointCreatorTypeDef",
    "RecoveryPointMemberTypeDef",
    "RecoveryPointSelectionOutputTypeDef",
    "RecoveryPointSelectionTypeDef",
    "ReportDeliveryChannelOutputTypeDef",
    "ReportDeliveryChannelTypeDef",
    "ReportDestinationTypeDef",
    "ReportJobTypeDef",
    "ReportPlanTypeDef",
    "ReportSettingOutputTypeDef",
    "ReportSettingTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreJobCreatorTypeDef",
    "RestoreJobSummaryTypeDef",
    "RestoreJobsListMemberTypeDef",
    "RestoreTestingPlanForCreateTypeDef",
    "RestoreTestingPlanForGetTypeDef",
    "RestoreTestingPlanForListTypeDef",
    "RestoreTestingPlanForUpdateTypeDef",
    "RestoreTestingRecoveryPointSelectionOutputTypeDef",
    "RestoreTestingRecoveryPointSelectionTypeDef",
    "RestoreTestingRecoveryPointSelectionUnionTypeDef",
    "RestoreTestingSelectionForCreateTypeDef",
    "RestoreTestingSelectionForGetTypeDef",
    "RestoreTestingSelectionForListTypeDef",
    "RestoreTestingSelectionForUpdateTypeDef",
    "StartBackupJobInputRequestTypeDef",
    "StartBackupJobOutputTypeDef",
    "StartCopyJobInputRequestTypeDef",
    "StartCopyJobOutputTypeDef",
    "StartReportJobInputRequestTypeDef",
    "StartReportJobOutputTypeDef",
    "StartRestoreJobInputRequestTypeDef",
    "StartRestoreJobOutputTypeDef",
    "StopBackupJobInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateBackupPlanInputRequestTypeDef",
    "UpdateBackupPlanOutputTypeDef",
    "UpdateFrameworkInputRequestTypeDef",
    "UpdateFrameworkOutputTypeDef",
    "UpdateGlobalSettingsInputRequestTypeDef",
    "UpdateRecoveryPointLifecycleInputRequestTypeDef",
    "UpdateRecoveryPointLifecycleOutputTypeDef",
    "UpdateRegionSettingsInputRequestTypeDef",
    "UpdateReportPlanInputRequestTypeDef",
    "UpdateReportPlanOutputTypeDef",
    "UpdateRestoreTestingPlanInputRequestTypeDef",
    "UpdateRestoreTestingPlanOutputTypeDef",
    "UpdateRestoreTestingSelectionInputRequestTypeDef",
    "UpdateRestoreTestingSelectionOutputTypeDef",
)


class AdvancedBackupSettingOutputTypeDef(TypedDict):
    ResourceType: NotRequired[str]
    BackupOptions: NotRequired[Dict[str, str]]


class AdvancedBackupSettingTypeDef(TypedDict):
    ResourceType: NotRequired[str]
    BackupOptions: NotRequired[Mapping[str, str]]


class BackupJobSummaryTypeDef(TypedDict):
    Region: NotRequired[str]
    AccountId: NotRequired[str]
    State: NotRequired[BackupJobStatusType]
    ResourceType: NotRequired[str]
    MessageCategory: NotRequired[str]
    Count: NotRequired[int]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class RecoveryPointCreatorTypeDef(TypedDict):
    BackupPlanId: NotRequired[str]
    BackupPlanArn: NotRequired[str]
    BackupPlanVersion: NotRequired[str]
    BackupRuleId: NotRequired[str]


class BackupPlanTemplatesListMemberTypeDef(TypedDict):
    BackupPlanTemplateId: NotRequired[str]
    BackupPlanTemplateName: NotRequired[str]


class LifecycleTypeDef(TypedDict):
    MoveToColdStorageAfterDays: NotRequired[int]
    DeleteAfterDays: NotRequired[int]
    OptInToArchiveForSupportedResources: NotRequired[bool]


class ConditionTypeDef(TypedDict):
    ConditionType: Literal["STRINGEQUALS"]
    ConditionKey: str
    ConditionValue: str


class BackupSelectionsListMemberTypeDef(TypedDict):
    SelectionId: NotRequired[str]
    SelectionName: NotRequired[str]
    BackupPlanId: NotRequired[str]
    CreationDate: NotRequired[datetime]
    CreatorRequestId: NotRequired[str]
    IamRoleArn: NotRequired[str]


class BackupVaultListMemberTypeDef(TypedDict):
    BackupVaultName: NotRequired[str]
    BackupVaultArn: NotRequired[str]
    VaultType: NotRequired[VaultTypeType]
    VaultState: NotRequired[VaultStateType]
    CreationDate: NotRequired[datetime]
    EncryptionKeyArn: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    NumberOfRecoveryPoints: NotRequired[int]
    Locked: NotRequired[bool]
    MinRetentionDays: NotRequired[int]
    MaxRetentionDays: NotRequired[int]
    LockDate: NotRequired[datetime]


class CalculatedLifecycleTypeDef(TypedDict):
    MoveToColdStorageAt: NotRequired[datetime]
    DeleteAt: NotRequired[datetime]


class CancelLegalHoldInputRequestTypeDef(TypedDict):
    LegalHoldId: str
    CancelDescription: str
    RetainRecordInDays: NotRequired[int]


class ConditionParameterTypeDef(TypedDict):
    ConditionKey: NotRequired[str]
    ConditionValue: NotRequired[str]


class ControlInputParameterTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterValue: NotRequired[str]


class ControlScopeOutputTypeDef(TypedDict):
    ComplianceResourceIds: NotRequired[List[str]]
    ComplianceResourceTypes: NotRequired[List[str]]
    Tags: NotRequired[Dict[str, str]]


class ControlScopeTypeDef(TypedDict):
    ComplianceResourceIds: NotRequired[Sequence[str]]
    ComplianceResourceTypes: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]


class CopyJobSummaryTypeDef(TypedDict):
    Region: NotRequired[str]
    AccountId: NotRequired[str]
    State: NotRequired[CopyJobStatusType]
    ResourceType: NotRequired[str]
    MessageCategory: NotRequired[str]
    Count: NotRequired[int]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateBackupVaultInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultTags: NotRequired[Mapping[str, str]]
    EncryptionKeyArn: NotRequired[str]
    CreatorRequestId: NotRequired[str]


class CreateLogicallyAirGappedBackupVaultInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    MinRetentionDays: int
    MaxRetentionDays: int
    BackupVaultTags: NotRequired[Mapping[str, str]]
    CreatorRequestId: NotRequired[str]


class ReportDeliveryChannelTypeDef(TypedDict):
    S3BucketName: str
    S3KeyPrefix: NotRequired[str]
    Formats: NotRequired[Sequence[str]]


class ReportSettingTypeDef(TypedDict):
    ReportTemplate: str
    FrameworkArns: NotRequired[Sequence[str]]
    NumberOfFrameworks: NotRequired[int]
    Accounts: NotRequired[Sequence[str]]
    OrganizationUnits: NotRequired[Sequence[str]]
    Regions: NotRequired[Sequence[str]]


class DateRangeOutputTypeDef(TypedDict):
    FromDate: datetime
    ToDate: datetime


TimestampTypeDef = Union[datetime, str]


class DeleteBackupPlanInputRequestTypeDef(TypedDict):
    BackupPlanId: str


class DeleteBackupSelectionInputRequestTypeDef(TypedDict):
    BackupPlanId: str
    SelectionId: str


class DeleteBackupVaultAccessPolicyInputRequestTypeDef(TypedDict):
    BackupVaultName: str


class DeleteBackupVaultInputRequestTypeDef(TypedDict):
    BackupVaultName: str


class DeleteBackupVaultLockConfigurationInputRequestTypeDef(TypedDict):
    BackupVaultName: str


class DeleteBackupVaultNotificationsInputRequestTypeDef(TypedDict):
    BackupVaultName: str


class DeleteFrameworkInputRequestTypeDef(TypedDict):
    FrameworkName: str


class DeleteRecoveryPointInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    RecoveryPointArn: str


class DeleteReportPlanInputRequestTypeDef(TypedDict):
    ReportPlanName: str


class DeleteRestoreTestingPlanInputRequestTypeDef(TypedDict):
    RestoreTestingPlanName: str


class DeleteRestoreTestingSelectionInputRequestTypeDef(TypedDict):
    RestoreTestingPlanName: str
    RestoreTestingSelectionName: str


class DescribeBackupJobInputRequestTypeDef(TypedDict):
    BackupJobId: str


class DescribeBackupVaultInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultAccountId: NotRequired[str]


class DescribeCopyJobInputRequestTypeDef(TypedDict):
    CopyJobId: str


class DescribeFrameworkInputRequestTypeDef(TypedDict):
    FrameworkName: str


class DescribeProtectedResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str


class DescribeRecoveryPointInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    RecoveryPointArn: str
    BackupVaultAccountId: NotRequired[str]


class DescribeReportJobInputRequestTypeDef(TypedDict):
    ReportJobId: str


class DescribeReportPlanInputRequestTypeDef(TypedDict):
    ReportPlanName: str


class DescribeRestoreJobInputRequestTypeDef(TypedDict):
    RestoreJobId: str


class RestoreJobCreatorTypeDef(TypedDict):
    RestoreTestingPlanArn: NotRequired[str]


class DisassociateRecoveryPointFromParentInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    RecoveryPointArn: str


class DisassociateRecoveryPointInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    RecoveryPointArn: str


class ExportBackupPlanTemplateInputRequestTypeDef(TypedDict):
    BackupPlanId: str


class FrameworkTypeDef(TypedDict):
    FrameworkName: NotRequired[str]
    FrameworkArn: NotRequired[str]
    FrameworkDescription: NotRequired[str]
    NumberOfControls: NotRequired[int]
    CreationTime: NotRequired[datetime]
    DeploymentStatus: NotRequired[str]


class GetBackupPlanFromJSONInputRequestTypeDef(TypedDict):
    BackupPlanTemplateJson: str


class GetBackupPlanFromTemplateInputRequestTypeDef(TypedDict):
    BackupPlanTemplateId: str


class GetBackupPlanInputRequestTypeDef(TypedDict):
    BackupPlanId: str
    VersionId: NotRequired[str]


class GetBackupSelectionInputRequestTypeDef(TypedDict):
    BackupPlanId: str
    SelectionId: str


class GetBackupVaultAccessPolicyInputRequestTypeDef(TypedDict):
    BackupVaultName: str


class GetBackupVaultNotificationsInputRequestTypeDef(TypedDict):
    BackupVaultName: str


class GetLegalHoldInputRequestTypeDef(TypedDict):
    LegalHoldId: str


class GetRecoveryPointRestoreMetadataInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    RecoveryPointArn: str
    BackupVaultAccountId: NotRequired[str]


class GetRestoreJobMetadataInputRequestTypeDef(TypedDict):
    RestoreJobId: str


class GetRestoreTestingInferredMetadataInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    RecoveryPointArn: str
    BackupVaultAccountId: NotRequired[str]


class GetRestoreTestingPlanInputRequestTypeDef(TypedDict):
    RestoreTestingPlanName: str


class GetRestoreTestingSelectionInputRequestTypeDef(TypedDict):
    RestoreTestingPlanName: str
    RestoreTestingSelectionName: str


class KeyValueTypeDef(TypedDict):
    Key: str
    Value: str


class LegalHoldTypeDef(TypedDict):
    Title: NotRequired[str]
    Status: NotRequired[LegalHoldStatusType]
    Description: NotRequired[str]
    LegalHoldId: NotRequired[str]
    LegalHoldArn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    CancellationDate: NotRequired[datetime]


class ListBackupJobSummariesInputRequestTypeDef(TypedDict):
    AccountId: NotRequired[str]
    State: NotRequired[BackupJobStatusType]
    ResourceType: NotRequired[str]
    MessageCategory: NotRequired[str]
    AggregationPeriod: NotRequired[AggregationPeriodType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListBackupPlanTemplatesInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListBackupPlanVersionsInputRequestTypeDef(TypedDict):
    BackupPlanId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListBackupPlansInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IncludeDeleted: NotRequired[bool]


class ListBackupSelectionsInputRequestTypeDef(TypedDict):
    BackupPlanId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListBackupVaultsInputRequestTypeDef(TypedDict):
    ByVaultType: NotRequired[VaultTypeType]
    ByShared: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListCopyJobSummariesInputRequestTypeDef(TypedDict):
    AccountId: NotRequired[str]
    State: NotRequired[CopyJobStatusType]
    ResourceType: NotRequired[str]
    MessageCategory: NotRequired[str]
    AggregationPeriod: NotRequired[AggregationPeriodType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFrameworksInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListLegalHoldsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProtectedResourcesByBackupVaultInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultAccountId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ProtectedResourceTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]
    LastBackupTime: NotRequired[datetime]
    ResourceName: NotRequired[str]
    LastBackupVaultArn: NotRequired[str]
    LastRecoveryPointArn: NotRequired[str]


class ListProtectedResourcesInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListRecoveryPointsByLegalHoldInputRequestTypeDef(TypedDict):
    LegalHoldId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class RecoveryPointMemberTypeDef(TypedDict):
    RecoveryPointArn: NotRequired[str]
    ResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]
    BackupVaultName: NotRequired[str]


class ListRecoveryPointsByResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ManagedByAWSBackupOnly: NotRequired[bool]


class RecoveryPointByResourceTypeDef(TypedDict):
    RecoveryPointArn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    Status: NotRequired[RecoveryPointStatusType]
    StatusMessage: NotRequired[str]
    EncryptionKeyArn: NotRequired[str]
    BackupSizeBytes: NotRequired[int]
    BackupVaultName: NotRequired[str]
    IsParent: NotRequired[bool]
    ParentRecoveryPointArn: NotRequired[str]
    ResourceName: NotRequired[str]
    VaultType: NotRequired[VaultTypeType]


class ListReportPlansInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListRestoreJobSummariesInputRequestTypeDef(TypedDict):
    AccountId: NotRequired[str]
    State: NotRequired[RestoreJobStateType]
    ResourceType: NotRequired[str]
    AggregationPeriod: NotRequired[AggregationPeriodType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RestoreJobSummaryTypeDef(TypedDict):
    Region: NotRequired[str]
    AccountId: NotRequired[str]
    State: NotRequired[RestoreJobStateType]
    ResourceType: NotRequired[str]
    Count: NotRequired[int]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class ListRestoreTestingPlansInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RestoreTestingPlanForListTypeDef(TypedDict):
    CreationTime: datetime
    RestoreTestingPlanArn: str
    RestoreTestingPlanName: str
    ScheduleExpression: str
    LastExecutionTime: NotRequired[datetime]
    LastUpdateTime: NotRequired[datetime]
    ScheduleExpressionTimezone: NotRequired[str]
    StartWindowHours: NotRequired[int]


class ListRestoreTestingSelectionsInputRequestTypeDef(TypedDict):
    RestoreTestingPlanName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RestoreTestingSelectionForListTypeDef(TypedDict):
    CreationTime: datetime
    IamRoleArn: str
    ProtectedResourceType: str
    RestoreTestingPlanName: str
    RestoreTestingSelectionName: str
    ValidationWindowHours: NotRequired[int]


class ListTagsInputRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PutBackupVaultAccessPolicyInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    Policy: NotRequired[str]


class PutBackupVaultLockConfigurationInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    MinRetentionDays: NotRequired[int]
    MaxRetentionDays: NotRequired[int]
    ChangeableForDays: NotRequired[int]


class PutBackupVaultNotificationsInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    SNSTopicArn: str
    BackupVaultEvents: Sequence[BackupVaultEventType]


class PutRestoreValidationResultInputRequestTypeDef(TypedDict):
    RestoreJobId: str
    ValidationStatus: RestoreValidationStatusType
    ValidationStatusMessage: NotRequired[str]


class ReportDeliveryChannelOutputTypeDef(TypedDict):
    S3BucketName: str
    S3KeyPrefix: NotRequired[str]
    Formats: NotRequired[List[str]]


class ReportDestinationTypeDef(TypedDict):
    S3BucketName: NotRequired[str]
    S3Keys: NotRequired[List[str]]


class ReportSettingOutputTypeDef(TypedDict):
    ReportTemplate: str
    FrameworkArns: NotRequired[List[str]]
    NumberOfFrameworks: NotRequired[int]
    Accounts: NotRequired[List[str]]
    OrganizationUnits: NotRequired[List[str]]
    Regions: NotRequired[List[str]]


class RestoreTestingRecoveryPointSelectionOutputTypeDef(TypedDict):
    Algorithm: NotRequired[RestoreTestingRecoveryPointSelectionAlgorithmType]
    ExcludeVaults: NotRequired[List[str]]
    IncludeVaults: NotRequired[List[str]]
    RecoveryPointTypes: NotRequired[List[RestoreTestingRecoveryPointTypeType]]
    SelectionWindowDays: NotRequired[int]


class RestoreTestingRecoveryPointSelectionTypeDef(TypedDict):
    Algorithm: NotRequired[RestoreTestingRecoveryPointSelectionAlgorithmType]
    ExcludeVaults: NotRequired[Sequence[str]]
    IncludeVaults: NotRequired[Sequence[str]]
    RecoveryPointTypes: NotRequired[Sequence[RestoreTestingRecoveryPointTypeType]]
    SelectionWindowDays: NotRequired[int]


class StartReportJobInputRequestTypeDef(TypedDict):
    ReportPlanName: str
    IdempotencyToken: NotRequired[str]


class StartRestoreJobInputRequestTypeDef(TypedDict):
    RecoveryPointArn: str
    Metadata: Mapping[str, str]
    IamRoleArn: NotRequired[str]
    IdempotencyToken: NotRequired[str]
    ResourceType: NotRequired[str]
    CopySourceTagsToRestoredResource: NotRequired[bool]


class StopBackupJobInputRequestTypeDef(TypedDict):
    BackupJobId: str


class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeyList: Sequence[str]


class UpdateGlobalSettingsInputRequestTypeDef(TypedDict):
    GlobalSettings: NotRequired[Mapping[str, str]]


class UpdateRegionSettingsInputRequestTypeDef(TypedDict):
    ResourceTypeOptInPreference: NotRequired[Mapping[str, bool]]
    ResourceTypeManagementPreference: NotRequired[Mapping[str, bool]]


class BackupPlansListMemberTypeDef(TypedDict):
    BackupPlanArn: NotRequired[str]
    BackupPlanId: NotRequired[str]
    CreationDate: NotRequired[datetime]
    DeletionDate: NotRequired[datetime]
    VersionId: NotRequired[str]
    BackupPlanName: NotRequired[str]
    CreatorRequestId: NotRequired[str]
    LastExecutionDate: NotRequired[datetime]
    AdvancedBackupSettings: NotRequired[List[AdvancedBackupSettingOutputTypeDef]]


AdvancedBackupSettingUnionTypeDef = Union[
    AdvancedBackupSettingTypeDef, AdvancedBackupSettingOutputTypeDef
]


class BackupJobTypeDef(TypedDict):
    AccountId: NotRequired[str]
    BackupJobId: NotRequired[str]
    BackupVaultName: NotRequired[str]
    BackupVaultArn: NotRequired[str]
    RecoveryPointArn: NotRequired[str]
    ResourceArn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    CompletionDate: NotRequired[datetime]
    State: NotRequired[BackupJobStateType]
    StatusMessage: NotRequired[str]
    PercentDone: NotRequired[str]
    BackupSizeInBytes: NotRequired[int]
    IamRoleArn: NotRequired[str]
    CreatedBy: NotRequired[RecoveryPointCreatorTypeDef]
    ExpectedCompletionDate: NotRequired[datetime]
    StartBy: NotRequired[datetime]
    ResourceType: NotRequired[str]
    BytesTransferred: NotRequired[int]
    BackupOptions: NotRequired[Dict[str, str]]
    BackupType: NotRequired[str]
    ParentJobId: NotRequired[str]
    IsParent: NotRequired[bool]
    ResourceName: NotRequired[str]
    InitiationDate: NotRequired[datetime]
    MessageCategory: NotRequired[str]


class CopyJobTypeDef(TypedDict):
    AccountId: NotRequired[str]
    CopyJobId: NotRequired[str]
    SourceBackupVaultArn: NotRequired[str]
    SourceRecoveryPointArn: NotRequired[str]
    DestinationBackupVaultArn: NotRequired[str]
    DestinationRecoveryPointArn: NotRequired[str]
    ResourceArn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    CompletionDate: NotRequired[datetime]
    State: NotRequired[CopyJobStateType]
    StatusMessage: NotRequired[str]
    BackupSizeInBytes: NotRequired[int]
    IamRoleArn: NotRequired[str]
    CreatedBy: NotRequired[RecoveryPointCreatorTypeDef]
    ResourceType: NotRequired[str]
    ParentJobId: NotRequired[str]
    IsParent: NotRequired[bool]
    CompositeMemberIdentifier: NotRequired[str]
    NumberOfChildJobs: NotRequired[int]
    ChildJobsInState: NotRequired[Dict[CopyJobStateType, int]]
    ResourceName: NotRequired[str]
    MessageCategory: NotRequired[str]


class CopyActionTypeDef(TypedDict):
    DestinationBackupVaultArn: str
    Lifecycle: NotRequired[LifecycleTypeDef]


class StartBackupJobInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    ResourceArn: str
    IamRoleArn: str
    IdempotencyToken: NotRequired[str]
    StartWindowMinutes: NotRequired[int]
    CompleteWindowMinutes: NotRequired[int]
    Lifecycle: NotRequired[LifecycleTypeDef]
    RecoveryPointTags: NotRequired[Mapping[str, str]]
    BackupOptions: NotRequired[Mapping[str, str]]


class StartCopyJobInputRequestTypeDef(TypedDict):
    RecoveryPointArn: str
    SourceBackupVaultName: str
    DestinationBackupVaultArn: str
    IamRoleArn: str
    IdempotencyToken: NotRequired[str]
    Lifecycle: NotRequired[LifecycleTypeDef]


class UpdateRecoveryPointLifecycleInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    RecoveryPointArn: str
    Lifecycle: NotRequired[LifecycleTypeDef]


class RecoveryPointByBackupVaultTypeDef(TypedDict):
    RecoveryPointArn: NotRequired[str]
    BackupVaultName: NotRequired[str]
    BackupVaultArn: NotRequired[str]
    SourceBackupVaultArn: NotRequired[str]
    ResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]
    CreatedBy: NotRequired[RecoveryPointCreatorTypeDef]
    IamRoleArn: NotRequired[str]
    Status: NotRequired[RecoveryPointStatusType]
    StatusMessage: NotRequired[str]
    CreationDate: NotRequired[datetime]
    CompletionDate: NotRequired[datetime]
    BackupSizeInBytes: NotRequired[int]
    CalculatedLifecycle: NotRequired[CalculatedLifecycleTypeDef]
    Lifecycle: NotRequired[LifecycleTypeDef]
    EncryptionKeyArn: NotRequired[str]
    IsEncrypted: NotRequired[bool]
    LastRestoreTime: NotRequired[datetime]
    ParentRecoveryPointArn: NotRequired[str]
    CompositeMemberIdentifier: NotRequired[str]
    IsParent: NotRequired[bool]
    ResourceName: NotRequired[str]
    VaultType: NotRequired[VaultTypeType]


class ConditionsOutputTypeDef(TypedDict):
    StringEquals: NotRequired[List[ConditionParameterTypeDef]]
    StringNotEquals: NotRequired[List[ConditionParameterTypeDef]]
    StringLike: NotRequired[List[ConditionParameterTypeDef]]
    StringNotLike: NotRequired[List[ConditionParameterTypeDef]]


class ConditionsTypeDef(TypedDict):
    StringEquals: NotRequired[Sequence[ConditionParameterTypeDef]]
    StringNotEquals: NotRequired[Sequence[ConditionParameterTypeDef]]
    StringLike: NotRequired[Sequence[ConditionParameterTypeDef]]
    StringNotLike: NotRequired[Sequence[ConditionParameterTypeDef]]


class FrameworkControlOutputTypeDef(TypedDict):
    ControlName: str
    ControlInputParameters: NotRequired[List[ControlInputParameterTypeDef]]
    ControlScope: NotRequired[ControlScopeOutputTypeDef]


ControlScopeUnionTypeDef = Union[ControlScopeTypeDef, ControlScopeOutputTypeDef]


class CreateBackupPlanOutputTypeDef(TypedDict):
    BackupPlanId: str
    BackupPlanArn: str
    CreationDate: datetime
    VersionId: str
    AdvancedBackupSettings: List[AdvancedBackupSettingOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBackupSelectionOutputTypeDef(TypedDict):
    SelectionId: str
    BackupPlanId: str
    CreationDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBackupVaultOutputTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultArn: str
    CreationDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFrameworkOutputTypeDef(TypedDict):
    FrameworkName: str
    FrameworkArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLogicallyAirGappedBackupVaultOutputTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultArn: str
    CreationDate: datetime
    VaultState: VaultStateType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReportPlanOutputTypeDef(TypedDict):
    ReportPlanName: str
    ReportPlanArn: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRestoreTestingPlanOutputTypeDef(TypedDict):
    CreationTime: datetime
    RestoreTestingPlanArn: str
    RestoreTestingPlanName: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRestoreTestingSelectionOutputTypeDef(TypedDict):
    CreationTime: datetime
    RestoreTestingPlanArn: str
    RestoreTestingPlanName: str
    RestoreTestingSelectionName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBackupPlanOutputTypeDef(TypedDict):
    BackupPlanId: str
    BackupPlanArn: str
    DeletionDate: datetime
    VersionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBackupJobOutputTypeDef(TypedDict):
    AccountId: str
    BackupJobId: str
    BackupVaultName: str
    BackupVaultArn: str
    RecoveryPointArn: str
    ResourceArn: str
    CreationDate: datetime
    CompletionDate: datetime
    State: BackupJobStateType
    StatusMessage: str
    PercentDone: str
    BackupSizeInBytes: int
    IamRoleArn: str
    CreatedBy: RecoveryPointCreatorTypeDef
    ResourceType: str
    BytesTransferred: int
    ExpectedCompletionDate: datetime
    StartBy: datetime
    BackupOptions: Dict[str, str]
    BackupType: str
    ParentJobId: str
    IsParent: bool
    NumberOfChildJobs: int
    ChildJobsInState: Dict[BackupJobStateType, int]
    ResourceName: str
    InitiationDate: datetime
    MessageCategory: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBackupVaultOutputTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultArn: str
    VaultType: VaultTypeType
    VaultState: VaultStateType
    EncryptionKeyArn: str
    CreationDate: datetime
    CreatorRequestId: str
    NumberOfRecoveryPoints: int
    Locked: bool
    MinRetentionDays: int
    MaxRetentionDays: int
    LockDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGlobalSettingsOutputTypeDef(TypedDict):
    GlobalSettings: Dict[str, str]
    LastUpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProtectedResourceOutputTypeDef(TypedDict):
    ResourceArn: str
    ResourceType: str
    LastBackupTime: datetime
    ResourceName: str
    LastBackupVaultArn: str
    LastRecoveryPointArn: str
    LatestRestoreExecutionTimeMinutes: int
    LatestRestoreJobCreationDate: datetime
    LatestRestoreRecoveryPointCreationDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRecoveryPointOutputTypeDef(TypedDict):
    RecoveryPointArn: str
    BackupVaultName: str
    BackupVaultArn: str
    SourceBackupVaultArn: str
    ResourceArn: str
    ResourceType: str
    CreatedBy: RecoveryPointCreatorTypeDef
    IamRoleArn: str
    Status: RecoveryPointStatusType
    StatusMessage: str
    CreationDate: datetime
    CompletionDate: datetime
    BackupSizeInBytes: int
    CalculatedLifecycle: CalculatedLifecycleTypeDef
    Lifecycle: LifecycleTypeDef
    EncryptionKeyArn: str
    IsEncrypted: bool
    StorageClass: StorageClassType
    LastRestoreTime: datetime
    ParentRecoveryPointArn: str
    CompositeMemberIdentifier: str
    IsParent: bool
    ResourceName: str
    VaultType: VaultTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRegionSettingsOutputTypeDef(TypedDict):
    ResourceTypeOptInPreference: Dict[str, bool]
    ResourceTypeManagementPreference: Dict[str, bool]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExportBackupPlanTemplateOutputTypeDef(TypedDict):
    BackupPlanTemplateJson: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetBackupVaultAccessPolicyOutputTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultArn: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetBackupVaultNotificationsOutputTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultArn: str
    SNSTopicArn: str
    BackupVaultEvents: List[BackupVaultEventType]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRecoveryPointRestoreMetadataOutputTypeDef(TypedDict):
    BackupVaultArn: str
    RecoveryPointArn: str
    RestoreMetadata: Dict[str, str]
    ResourceType: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRestoreJobMetadataOutputTypeDef(TypedDict):
    RestoreJobId: str
    Metadata: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRestoreTestingInferredMetadataOutputTypeDef(TypedDict):
    InferredMetadata: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetSupportedResourceTypesOutputTypeDef(TypedDict):
    ResourceTypes: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBackupJobSummariesOutputTypeDef(TypedDict):
    BackupJobSummaries: List[BackupJobSummaryTypeDef]
    AggregationPeriod: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBackupPlanTemplatesOutputTypeDef(TypedDict):
    BackupPlanTemplatesList: List[BackupPlanTemplatesListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBackupSelectionsOutputTypeDef(TypedDict):
    BackupSelectionsList: List[BackupSelectionsListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBackupVaultsOutputTypeDef(TypedDict):
    BackupVaultList: List[BackupVaultListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCopyJobSummariesOutputTypeDef(TypedDict):
    CopyJobSummaries: List[CopyJobSummaryTypeDef]
    AggregationPeriod: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartBackupJobOutputTypeDef(TypedDict):
    BackupJobId: str
    RecoveryPointArn: str
    CreationDate: datetime
    IsParent: bool
    ResponseMetadata: ResponseMetadataTypeDef


class StartCopyJobOutputTypeDef(TypedDict):
    CopyJobId: str
    CreationDate: datetime
    IsParent: bool
    ResponseMetadata: ResponseMetadataTypeDef


class StartReportJobOutputTypeDef(TypedDict):
    ReportJobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartRestoreJobOutputTypeDef(TypedDict):
    RestoreJobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBackupPlanOutputTypeDef(TypedDict):
    BackupPlanId: str
    BackupPlanArn: str
    CreationDate: datetime
    VersionId: str
    AdvancedBackupSettings: List[AdvancedBackupSettingOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFrameworkOutputTypeDef(TypedDict):
    FrameworkName: str
    FrameworkArn: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRecoveryPointLifecycleOutputTypeDef(TypedDict):
    BackupVaultArn: str
    RecoveryPointArn: str
    Lifecycle: LifecycleTypeDef
    CalculatedLifecycle: CalculatedLifecycleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateReportPlanOutputTypeDef(TypedDict):
    ReportPlanName: str
    ReportPlanArn: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRestoreTestingPlanOutputTypeDef(TypedDict):
    CreationTime: datetime
    RestoreTestingPlanArn: str
    RestoreTestingPlanName: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRestoreTestingSelectionOutputTypeDef(TypedDict):
    CreationTime: datetime
    RestoreTestingPlanArn: str
    RestoreTestingPlanName: str
    RestoreTestingSelectionName: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReportPlanInputRequestTypeDef(TypedDict):
    ReportPlanName: str
    ReportDeliveryChannel: ReportDeliveryChannelTypeDef
    ReportSetting: ReportSettingTypeDef
    ReportPlanDescription: NotRequired[str]
    ReportPlanTags: NotRequired[Mapping[str, str]]
    IdempotencyToken: NotRequired[str]


class UpdateReportPlanInputRequestTypeDef(TypedDict):
    ReportPlanName: str
    ReportPlanDescription: NotRequired[str]
    ReportDeliveryChannel: NotRequired[ReportDeliveryChannelTypeDef]
    ReportSetting: NotRequired[ReportSettingTypeDef]
    IdempotencyToken: NotRequired[str]


class RecoveryPointSelectionOutputTypeDef(TypedDict):
    VaultNames: NotRequired[List[str]]
    ResourceIdentifiers: NotRequired[List[str]]
    DateRange: NotRequired[DateRangeOutputTypeDef]


class DateRangeTypeDef(TypedDict):
    FromDate: TimestampTypeDef
    ToDate: TimestampTypeDef


class ListBackupJobsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ByResourceArn: NotRequired[str]
    ByState: NotRequired[BackupJobStateType]
    ByBackupVaultName: NotRequired[str]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByResourceType: NotRequired[str]
    ByAccountId: NotRequired[str]
    ByCompleteAfter: NotRequired[TimestampTypeDef]
    ByCompleteBefore: NotRequired[TimestampTypeDef]
    ByParentJobId: NotRequired[str]
    ByMessageCategory: NotRequired[str]


class ListCopyJobsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ByResourceArn: NotRequired[str]
    ByState: NotRequired[CopyJobStateType]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByResourceType: NotRequired[str]
    ByDestinationVaultArn: NotRequired[str]
    ByAccountId: NotRequired[str]
    ByCompleteBefore: NotRequired[TimestampTypeDef]
    ByCompleteAfter: NotRequired[TimestampTypeDef]
    ByParentJobId: NotRequired[str]
    ByMessageCategory: NotRequired[str]


class ListRecoveryPointsByBackupVaultInputRequestTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultAccountId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ByResourceArn: NotRequired[str]
    ByResourceType: NotRequired[str]
    ByBackupPlanId: NotRequired[str]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByParentRecoveryPointArn: NotRequired[str]


class ListReportJobsInputRequestTypeDef(TypedDict):
    ByReportPlanName: NotRequired[str]
    ByCreationBefore: NotRequired[TimestampTypeDef]
    ByCreationAfter: NotRequired[TimestampTypeDef]
    ByStatus: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListRestoreJobsByProtectedResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    ByStatus: NotRequired[RestoreJobStatusType]
    ByRecoveryPointCreationDateAfter: NotRequired[TimestampTypeDef]
    ByRecoveryPointCreationDateBefore: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListRestoreJobsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ByAccountId: NotRequired[str]
    ByResourceType: NotRequired[str]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByStatus: NotRequired[RestoreJobStatusType]
    ByCompleteBefore: NotRequired[TimestampTypeDef]
    ByCompleteAfter: NotRequired[TimestampTypeDef]
    ByRestoreTestingPlanArn: NotRequired[str]


class DescribeRestoreJobOutputTypeDef(TypedDict):
    AccountId: str
    RestoreJobId: str
    RecoveryPointArn: str
    CreationDate: datetime
    CompletionDate: datetime
    Status: RestoreJobStatusType
    StatusMessage: str
    PercentDone: str
    BackupSizeInBytes: int
    IamRoleArn: str
    ExpectedCompletionTimeMinutes: int
    CreatedResourceArn: str
    ResourceType: str
    RecoveryPointCreationDate: datetime
    CreatedBy: RestoreJobCreatorTypeDef
    ValidationStatus: RestoreValidationStatusType
    ValidationStatusMessage: str
    DeletionStatus: RestoreDeletionStatusType
    DeletionStatusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreJobsListMemberTypeDef(TypedDict):
    AccountId: NotRequired[str]
    RestoreJobId: NotRequired[str]
    RecoveryPointArn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    CompletionDate: NotRequired[datetime]
    Status: NotRequired[RestoreJobStatusType]
    StatusMessage: NotRequired[str]
    PercentDone: NotRequired[str]
    BackupSizeInBytes: NotRequired[int]
    IamRoleArn: NotRequired[str]
    ExpectedCompletionTimeMinutes: NotRequired[int]
    CreatedResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]
    RecoveryPointCreationDate: NotRequired[datetime]
    CreatedBy: NotRequired[RestoreJobCreatorTypeDef]
    ValidationStatus: NotRequired[RestoreValidationStatusType]
    ValidationStatusMessage: NotRequired[str]
    DeletionStatus: NotRequired[RestoreDeletionStatusType]
    DeletionStatusMessage: NotRequired[str]


class ListFrameworksOutputTypeDef(TypedDict):
    Frameworks: List[FrameworkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ProtectedResourceConditionsOutputTypeDef(TypedDict):
    StringEquals: NotRequired[List[KeyValueTypeDef]]
    StringNotEquals: NotRequired[List[KeyValueTypeDef]]


class ProtectedResourceConditionsTypeDef(TypedDict):
    StringEquals: NotRequired[Sequence[KeyValueTypeDef]]
    StringNotEquals: NotRequired[Sequence[KeyValueTypeDef]]


class ListLegalHoldsOutputTypeDef(TypedDict):
    LegalHolds: List[LegalHoldTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBackupJobsInputListBackupJobsPaginateTypeDef(TypedDict):
    ByResourceArn: NotRequired[str]
    ByState: NotRequired[BackupJobStateType]
    ByBackupVaultName: NotRequired[str]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByResourceType: NotRequired[str]
    ByAccountId: NotRequired[str]
    ByCompleteAfter: NotRequired[TimestampTypeDef]
    ByCompleteBefore: NotRequired[TimestampTypeDef]
    ByParentJobId: NotRequired[str]
    ByMessageCategory: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef(TypedDict):
    BackupPlanId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBackupPlansInputListBackupPlansPaginateTypeDef(TypedDict):
    IncludeDeleted: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef(TypedDict):
    BackupPlanId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBackupVaultsInputListBackupVaultsPaginateTypeDef(TypedDict):
    ByVaultType: NotRequired[VaultTypeType]
    ByShared: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCopyJobsInputListCopyJobsPaginateTypeDef(TypedDict):
    ByResourceArn: NotRequired[str]
    ByState: NotRequired[CopyJobStateType]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByResourceType: NotRequired[str]
    ByDestinationVaultArn: NotRequired[str]
    ByAccountId: NotRequired[str]
    ByCompleteBefore: NotRequired[TimestampTypeDef]
    ByCompleteAfter: NotRequired[TimestampTypeDef]
    ByParentJobId: NotRequired[str]
    ByMessageCategory: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLegalHoldsInputListLegalHoldsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProtectedResourcesByBackupVaultInputListProtectedResourcesByBackupVaultPaginateTypeDef(
    TypedDict
):
    BackupVaultName: str
    BackupVaultAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef(TypedDict):
    BackupVaultName: str
    BackupVaultAccountId: NotRequired[str]
    ByResourceArn: NotRequired[str]
    ByResourceType: NotRequired[str]
    ByBackupPlanId: NotRequired[str]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByParentRecoveryPointArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef(TypedDict):
    LegalHoldId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef(TypedDict):
    ResourceArn: str
    ManagedByAWSBackupOnly: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRestoreJobsByProtectedResourceInputListRestoreJobsByProtectedResourcePaginateTypeDef(
    TypedDict
):
    ResourceArn: str
    ByStatus: NotRequired[RestoreJobStatusType]
    ByRecoveryPointCreationDateAfter: NotRequired[TimestampTypeDef]
    ByRecoveryPointCreationDateBefore: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRestoreJobsInputListRestoreJobsPaginateTypeDef(TypedDict):
    ByAccountId: NotRequired[str]
    ByResourceType: NotRequired[str]
    ByCreatedBefore: NotRequired[TimestampTypeDef]
    ByCreatedAfter: NotRequired[TimestampTypeDef]
    ByStatus: NotRequired[RestoreJobStatusType]
    ByCompleteBefore: NotRequired[TimestampTypeDef]
    ByCompleteAfter: NotRequired[TimestampTypeDef]
    ByRestoreTestingPlanArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRestoreTestingPlansInputListRestoreTestingPlansPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRestoreTestingSelectionsInputListRestoreTestingSelectionsPaginateTypeDef(TypedDict):
    RestoreTestingPlanName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProtectedResourcesByBackupVaultOutputTypeDef(TypedDict):
    Results: List[ProtectedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProtectedResourcesOutputTypeDef(TypedDict):
    Results: List[ProtectedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRecoveryPointsByLegalHoldOutputTypeDef(TypedDict):
    RecoveryPoints: List[RecoveryPointMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRecoveryPointsByResourceOutputTypeDef(TypedDict):
    RecoveryPoints: List[RecoveryPointByResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRestoreJobSummariesOutputTypeDef(TypedDict):
    RestoreJobSummaries: List[RestoreJobSummaryTypeDef]
    AggregationPeriod: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRestoreTestingPlansOutputTypeDef(TypedDict):
    RestoreTestingPlans: List[RestoreTestingPlanForListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRestoreTestingSelectionsOutputTypeDef(TypedDict):
    RestoreTestingSelections: List[RestoreTestingSelectionForListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ReportJobTypeDef(TypedDict):
    ReportJobId: NotRequired[str]
    ReportPlanArn: NotRequired[str]
    ReportTemplate: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    ReportDestination: NotRequired[ReportDestinationTypeDef]


class ReportPlanTypeDef(TypedDict):
    ReportPlanArn: NotRequired[str]
    ReportPlanName: NotRequired[str]
    ReportPlanDescription: NotRequired[str]
    ReportSetting: NotRequired[ReportSettingOutputTypeDef]
    ReportDeliveryChannel: NotRequired[ReportDeliveryChannelOutputTypeDef]
    DeploymentStatus: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastAttemptedExecutionTime: NotRequired[datetime]
    LastSuccessfulExecutionTime: NotRequired[datetime]


class RestoreTestingPlanForGetTypeDef(TypedDict):
    CreationTime: datetime
    RecoveryPointSelection: RestoreTestingRecoveryPointSelectionOutputTypeDef
    RestoreTestingPlanArn: str
    RestoreTestingPlanName: str
    ScheduleExpression: str
    CreatorRequestId: NotRequired[str]
    LastExecutionTime: NotRequired[datetime]
    LastUpdateTime: NotRequired[datetime]
    ScheduleExpressionTimezone: NotRequired[str]
    StartWindowHours: NotRequired[int]


RestoreTestingRecoveryPointSelectionUnionTypeDef = Union[
    RestoreTestingRecoveryPointSelectionTypeDef, RestoreTestingRecoveryPointSelectionOutputTypeDef
]


class ListBackupPlanVersionsOutputTypeDef(TypedDict):
    BackupPlanVersionsList: List[BackupPlansListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBackupPlansOutputTypeDef(TypedDict):
    BackupPlansList: List[BackupPlansListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBackupJobsOutputTypeDef(TypedDict):
    BackupJobs: List[BackupJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeCopyJobOutputTypeDef(TypedDict):
    CopyJob: CopyJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCopyJobsOutputTypeDef(TypedDict):
    CopyJobs: List[CopyJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BackupRuleInputTypeDef(TypedDict):
    RuleName: str
    TargetBackupVaultName: str
    ScheduleExpression: NotRequired[str]
    StartWindowMinutes: NotRequired[int]
    CompletionWindowMinutes: NotRequired[int]
    Lifecycle: NotRequired[LifecycleTypeDef]
    RecoveryPointTags: NotRequired[Mapping[str, str]]
    CopyActions: NotRequired[Sequence[CopyActionTypeDef]]
    EnableContinuousBackup: NotRequired[bool]
    ScheduleExpressionTimezone: NotRequired[str]


class BackupRuleTypeDef(TypedDict):
    RuleName: str
    TargetBackupVaultName: str
    ScheduleExpression: NotRequired[str]
    StartWindowMinutes: NotRequired[int]
    CompletionWindowMinutes: NotRequired[int]
    Lifecycle: NotRequired[LifecycleTypeDef]
    RecoveryPointTags: NotRequired[Dict[str, str]]
    RuleId: NotRequired[str]
    CopyActions: NotRequired[List[CopyActionTypeDef]]
    EnableContinuousBackup: NotRequired[bool]
    ScheduleExpressionTimezone: NotRequired[str]


class ListRecoveryPointsByBackupVaultOutputTypeDef(TypedDict):
    RecoveryPoints: List[RecoveryPointByBackupVaultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BackupSelectionOutputTypeDef(TypedDict):
    SelectionName: str
    IamRoleArn: str
    Resources: NotRequired[List[str]]
    ListOfTags: NotRequired[List[ConditionTypeDef]]
    NotResources: NotRequired[List[str]]
    Conditions: NotRequired[ConditionsOutputTypeDef]


ConditionsUnionTypeDef = Union[ConditionsTypeDef, ConditionsOutputTypeDef]


class DescribeFrameworkOutputTypeDef(TypedDict):
    FrameworkName: str
    FrameworkArn: str
    FrameworkDescription: str
    FrameworkControls: List[FrameworkControlOutputTypeDef]
    CreationTime: datetime
    DeploymentStatus: str
    FrameworkStatus: str
    IdempotencyToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class FrameworkControlTypeDef(TypedDict):
    ControlName: str
    ControlInputParameters: NotRequired[Sequence[ControlInputParameterTypeDef]]
    ControlScope: NotRequired[ControlScopeUnionTypeDef]


class CreateLegalHoldOutputTypeDef(TypedDict):
    Title: str
    Status: LegalHoldStatusType
    Description: str
    LegalHoldId: str
    LegalHoldArn: str
    CreationDate: datetime
    RecoveryPointSelection: RecoveryPointSelectionOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetLegalHoldOutputTypeDef(TypedDict):
    Title: str
    Status: LegalHoldStatusType
    Description: str
    CancelDescription: str
    LegalHoldId: str
    LegalHoldArn: str
    CreationDate: datetime
    CancellationDate: datetime
    RetainRecordUntil: datetime
    RecoveryPointSelection: RecoveryPointSelectionOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DateRangeUnionTypeDef = Union[DateRangeTypeDef, DateRangeOutputTypeDef]


class ListRestoreJobsByProtectedResourceOutputTypeDef(TypedDict):
    RestoreJobs: List[RestoreJobsListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRestoreJobsOutputTypeDef(TypedDict):
    RestoreJobs: List[RestoreJobsListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RestoreTestingSelectionForGetTypeDef(TypedDict):
    CreationTime: datetime
    IamRoleArn: str
    ProtectedResourceType: str
    RestoreTestingPlanName: str
    RestoreTestingSelectionName: str
    CreatorRequestId: NotRequired[str]
    ProtectedResourceArns: NotRequired[List[str]]
    ProtectedResourceConditions: NotRequired[ProtectedResourceConditionsOutputTypeDef]
    RestoreMetadataOverrides: NotRequired[Dict[str, str]]
    ValidationWindowHours: NotRequired[int]


ProtectedResourceConditionsUnionTypeDef = Union[
    ProtectedResourceConditionsTypeDef, ProtectedResourceConditionsOutputTypeDef
]


class DescribeReportJobOutputTypeDef(TypedDict):
    ReportJob: ReportJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListReportJobsOutputTypeDef(TypedDict):
    ReportJobs: List[ReportJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeReportPlanOutputTypeDef(TypedDict):
    ReportPlan: ReportPlanTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListReportPlansOutputTypeDef(TypedDict):
    ReportPlans: List[ReportPlanTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetRestoreTestingPlanOutputTypeDef(TypedDict):
    RestoreTestingPlan: RestoreTestingPlanForGetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreTestingPlanForCreateTypeDef(TypedDict):
    RecoveryPointSelection: RestoreTestingRecoveryPointSelectionUnionTypeDef
    RestoreTestingPlanName: str
    ScheduleExpression: str
    ScheduleExpressionTimezone: NotRequired[str]
    StartWindowHours: NotRequired[int]


class RestoreTestingPlanForUpdateTypeDef(TypedDict):
    RecoveryPointSelection: NotRequired[RestoreTestingRecoveryPointSelectionUnionTypeDef]
    ScheduleExpression: NotRequired[str]
    ScheduleExpressionTimezone: NotRequired[str]
    StartWindowHours: NotRequired[int]


class BackupPlanInputTypeDef(TypedDict):
    BackupPlanName: str
    Rules: Sequence[BackupRuleInputTypeDef]
    AdvancedBackupSettings: NotRequired[Sequence[AdvancedBackupSettingUnionTypeDef]]


class BackupPlanTypeDef(TypedDict):
    BackupPlanName: str
    Rules: List[BackupRuleTypeDef]
    AdvancedBackupSettings: NotRequired[List[AdvancedBackupSettingOutputTypeDef]]


class GetBackupSelectionOutputTypeDef(TypedDict):
    BackupSelection: BackupSelectionOutputTypeDef
    SelectionId: str
    BackupPlanId: str
    CreationDate: datetime
    CreatorRequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class BackupSelectionTypeDef(TypedDict):
    SelectionName: str
    IamRoleArn: str
    Resources: NotRequired[Sequence[str]]
    ListOfTags: NotRequired[Sequence[ConditionTypeDef]]
    NotResources: NotRequired[Sequence[str]]
    Conditions: NotRequired[ConditionsUnionTypeDef]


FrameworkControlUnionTypeDef = Union[FrameworkControlTypeDef, FrameworkControlOutputTypeDef]


class UpdateFrameworkInputRequestTypeDef(TypedDict):
    FrameworkName: str
    FrameworkDescription: NotRequired[str]
    FrameworkControls: NotRequired[Sequence[FrameworkControlTypeDef]]
    IdempotencyToken: NotRequired[str]


class RecoveryPointSelectionTypeDef(TypedDict):
    VaultNames: NotRequired[Sequence[str]]
    ResourceIdentifiers: NotRequired[Sequence[str]]
    DateRange: NotRequired[DateRangeUnionTypeDef]


class GetRestoreTestingSelectionOutputTypeDef(TypedDict):
    RestoreTestingSelection: RestoreTestingSelectionForGetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreTestingSelectionForCreateTypeDef(TypedDict):
    IamRoleArn: str
    ProtectedResourceType: str
    RestoreTestingSelectionName: str
    ProtectedResourceArns: NotRequired[Sequence[str]]
    ProtectedResourceConditions: NotRequired[ProtectedResourceConditionsUnionTypeDef]
    RestoreMetadataOverrides: NotRequired[Mapping[str, str]]
    ValidationWindowHours: NotRequired[int]


class RestoreTestingSelectionForUpdateTypeDef(TypedDict):
    IamRoleArn: NotRequired[str]
    ProtectedResourceArns: NotRequired[Sequence[str]]
    ProtectedResourceConditions: NotRequired[ProtectedResourceConditionsUnionTypeDef]
    RestoreMetadataOverrides: NotRequired[Mapping[str, str]]
    ValidationWindowHours: NotRequired[int]


class CreateRestoreTestingPlanInputRequestTypeDef(TypedDict):
    RestoreTestingPlan: RestoreTestingPlanForCreateTypeDef
    CreatorRequestId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class UpdateRestoreTestingPlanInputRequestTypeDef(TypedDict):
    RestoreTestingPlan: RestoreTestingPlanForUpdateTypeDef
    RestoreTestingPlanName: str


class CreateBackupPlanInputRequestTypeDef(TypedDict):
    BackupPlan: BackupPlanInputTypeDef
    BackupPlanTags: NotRequired[Mapping[str, str]]
    CreatorRequestId: NotRequired[str]


class UpdateBackupPlanInputRequestTypeDef(TypedDict):
    BackupPlanId: str
    BackupPlan: BackupPlanInputTypeDef


class GetBackupPlanFromJSONOutputTypeDef(TypedDict):
    BackupPlan: BackupPlanTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBackupPlanFromTemplateOutputTypeDef(TypedDict):
    BackupPlanDocument: BackupPlanTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBackupPlanOutputTypeDef(TypedDict):
    BackupPlan: BackupPlanTypeDef
    BackupPlanId: str
    BackupPlanArn: str
    VersionId: str
    CreatorRequestId: str
    CreationDate: datetime
    DeletionDate: datetime
    LastExecutionDate: datetime
    AdvancedBackupSettings: List[AdvancedBackupSettingOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBackupSelectionInputRequestTypeDef(TypedDict):
    BackupPlanId: str
    BackupSelection: BackupSelectionTypeDef
    CreatorRequestId: NotRequired[str]


class CreateFrameworkInputRequestTypeDef(TypedDict):
    FrameworkName: str
    FrameworkControls: Sequence[FrameworkControlUnionTypeDef]
    FrameworkDescription: NotRequired[str]
    IdempotencyToken: NotRequired[str]
    FrameworkTags: NotRequired[Mapping[str, str]]


class CreateLegalHoldInputRequestTypeDef(TypedDict):
    Title: str
    Description: str
    IdempotencyToken: NotRequired[str]
    RecoveryPointSelection: NotRequired[RecoveryPointSelectionTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class CreateRestoreTestingSelectionInputRequestTypeDef(TypedDict):
    RestoreTestingPlanName: str
    RestoreTestingSelection: RestoreTestingSelectionForCreateTypeDef
    CreatorRequestId: NotRequired[str]


class UpdateRestoreTestingSelectionInputRequestTypeDef(TypedDict):
    RestoreTestingPlanName: str
    RestoreTestingSelection: RestoreTestingSelectionForUpdateTypeDef
    RestoreTestingSelectionName: str
