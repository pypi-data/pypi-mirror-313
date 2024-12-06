"""
Type annotations for deadline service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/type_defs/)

Usage::

    ```python
    from mypy_boto3_deadline.type_defs import AcceleratorCountRangeTypeDef

    data: AcceleratorCountRangeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AcceleratorNameType,
    AutoScalingModeType,
    AutoScalingStatusType,
    BudgetActionTypeType,
    BudgetStatusType,
    ComparisonOperatorType,
    CompletedStatusType,
    CpuArchitectureTypeType,
    CreateJobTargetTaskRunStatusType,
    CustomerManagedFleetOperatingSystemFamilyType,
    DefaultQueueBudgetActionType,
    DependencyConsumerResolutionStatusType,
    Ec2MarketTypeType,
    EnvironmentTemplateTypeType,
    FileSystemLocationTypeType,
    FleetStatusType,
    JobAttachmentsFileSystemType,
    JobEntityErrorCodeType,
    JobLifecycleStatusType,
    JobTargetTaskRunStatusType,
    JobTemplateTypeType,
    LicenseEndpointStatusType,
    LogicalOperatorType,
    MembershipLevelType,
    PathFormatType,
    PeriodType,
    PrincipalTypeType,
    QueueBlockedReasonType,
    QueueFleetAssociationStatusType,
    QueueStatusType,
    RunAsType,
    ServiceManagedFleetOperatingSystemFamilyType,
    SessionActionStatusType,
    SessionLifecycleStatusType,
    SessionsStatisticsAggregationStatusType,
    SortOrderType,
    StepLifecycleStatusType,
    StepParameterTypeType,
    StepTargetTaskRunStatusType,
    StorageProfileOperatingSystemFamilyType,
    TaskRunStatusType,
    TaskTargetRunStatusType,
    UpdatedWorkerStatusType,
    UpdateQueueFleetAssociationStatusType,
    UsageGroupByFieldType,
    UsageStatisticType,
    UsageTypeType,
    WorkerStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceleratorCapabilitiesOutputTypeDef",
    "AcceleratorCapabilitiesTypeDef",
    "AcceleratorCapabilitiesUnionTypeDef",
    "AcceleratorCountRangeTypeDef",
    "AcceleratorSelectionTypeDef",
    "AcceleratorTotalMemoryMiBRangeTypeDef",
    "AssignedEnvironmentEnterSessionActionDefinitionTypeDef",
    "AssignedEnvironmentExitSessionActionDefinitionTypeDef",
    "AssignedSessionActionDefinitionTypeDef",
    "AssignedSessionActionTypeDef",
    "AssignedSessionTypeDef",
    "AssignedSyncInputJobAttachmentsSessionActionDefinitionTypeDef",
    "AssignedTaskRunSessionActionDefinitionTypeDef",
    "AssociateMemberToFarmRequestRequestTypeDef",
    "AssociateMemberToFleetRequestRequestTypeDef",
    "AssociateMemberToJobRequestRequestTypeDef",
    "AssociateMemberToQueueRequestRequestTypeDef",
    "AssumeFleetRoleForReadRequestRequestTypeDef",
    "AssumeFleetRoleForReadResponseTypeDef",
    "AssumeFleetRoleForWorkerRequestRequestTypeDef",
    "AssumeFleetRoleForWorkerResponseTypeDef",
    "AssumeQueueRoleForReadRequestRequestTypeDef",
    "AssumeQueueRoleForReadResponseTypeDef",
    "AssumeQueueRoleForUserRequestRequestTypeDef",
    "AssumeQueueRoleForUserResponseTypeDef",
    "AssumeQueueRoleForWorkerRequestRequestTypeDef",
    "AssumeQueueRoleForWorkerResponseTypeDef",
    "AttachmentsOutputTypeDef",
    "AttachmentsTypeDef",
    "AwsCredentialsTypeDef",
    "BatchGetJobEntityRequestRequestTypeDef",
    "BatchGetJobEntityResponseTypeDef",
    "BudgetActionToAddTypeDef",
    "BudgetActionToRemoveTypeDef",
    "BudgetScheduleOutputTypeDef",
    "BudgetScheduleTypeDef",
    "BudgetSummaryTypeDef",
    "ConsumedUsagesTypeDef",
    "CopyJobTemplateRequestRequestTypeDef",
    "CopyJobTemplateResponseTypeDef",
    "CreateBudgetRequestRequestTypeDef",
    "CreateBudgetResponseTypeDef",
    "CreateFarmRequestRequestTypeDef",
    "CreateFarmResponseTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "CreateFleetResponseTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobResponseTypeDef",
    "CreateLicenseEndpointRequestRequestTypeDef",
    "CreateLicenseEndpointResponseTypeDef",
    "CreateMonitorRequestRequestTypeDef",
    "CreateMonitorResponseTypeDef",
    "CreateQueueEnvironmentRequestRequestTypeDef",
    "CreateQueueEnvironmentResponseTypeDef",
    "CreateQueueFleetAssociationRequestRequestTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "CreateQueueResponseTypeDef",
    "CreateStorageProfileRequestRequestTypeDef",
    "CreateStorageProfileResponseTypeDef",
    "CreateWorkerRequestRequestTypeDef",
    "CreateWorkerResponseTypeDef",
    "CustomerManagedFleetConfigurationOutputTypeDef",
    "CustomerManagedFleetConfigurationTypeDef",
    "CustomerManagedFleetConfigurationUnionTypeDef",
    "CustomerManagedWorkerCapabilitiesOutputTypeDef",
    "CustomerManagedWorkerCapabilitiesTypeDef",
    "CustomerManagedWorkerCapabilitiesUnionTypeDef",
    "DateTimeFilterExpressionTypeDef",
    "DeleteBudgetRequestRequestTypeDef",
    "DeleteFarmRequestRequestTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DeleteLicenseEndpointRequestRequestTypeDef",
    "DeleteMeteredProductRequestRequestTypeDef",
    "DeleteMonitorRequestRequestTypeDef",
    "DeleteQueueEnvironmentRequestRequestTypeDef",
    "DeleteQueueFleetAssociationRequestRequestTypeDef",
    "DeleteQueueRequestRequestTypeDef",
    "DeleteStorageProfileRequestRequestTypeDef",
    "DeleteWorkerRequestRequestTypeDef",
    "DependencyCountsTypeDef",
    "DisassociateMemberFromFarmRequestRequestTypeDef",
    "DisassociateMemberFromFleetRequestRequestTypeDef",
    "DisassociateMemberFromJobRequestRequestTypeDef",
    "DisassociateMemberFromQueueRequestRequestTypeDef",
    "Ec2EbsVolumeTypeDef",
    "EnvironmentDetailsEntityTypeDef",
    "EnvironmentDetailsErrorTypeDef",
    "EnvironmentDetailsIdentifiersTypeDef",
    "EnvironmentEnterSessionActionDefinitionSummaryTypeDef",
    "EnvironmentEnterSessionActionDefinitionTypeDef",
    "EnvironmentExitSessionActionDefinitionSummaryTypeDef",
    "EnvironmentExitSessionActionDefinitionTypeDef",
    "FarmMemberTypeDef",
    "FarmSummaryTypeDef",
    "FieldSortExpressionTypeDef",
    "FileSystemLocationTypeDef",
    "FixedBudgetScheduleOutputTypeDef",
    "FixedBudgetScheduleTypeDef",
    "FixedBudgetScheduleUnionTypeDef",
    "FleetAmountCapabilityTypeDef",
    "FleetAttributeCapabilityOutputTypeDef",
    "FleetAttributeCapabilityTypeDef",
    "FleetAttributeCapabilityUnionTypeDef",
    "FleetCapabilitiesTypeDef",
    "FleetConfigurationOutputTypeDef",
    "FleetConfigurationTypeDef",
    "FleetMemberTypeDef",
    "FleetSummaryTypeDef",
    "GetBudgetRequestRequestTypeDef",
    "GetBudgetResponseTypeDef",
    "GetFarmRequestRequestTypeDef",
    "GetFarmResponseTypeDef",
    "GetFleetRequestFleetActiveWaitTypeDef",
    "GetFleetRequestRequestTypeDef",
    "GetFleetResponseTypeDef",
    "GetJobEntityErrorTypeDef",
    "GetJobRequestJobCreateCompleteWaitTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobResponseTypeDef",
    "GetLicenseEndpointRequestLicenseEndpointDeletedWaitTypeDef",
    "GetLicenseEndpointRequestLicenseEndpointValidWaitTypeDef",
    "GetLicenseEndpointRequestRequestTypeDef",
    "GetLicenseEndpointResponseTypeDef",
    "GetMonitorRequestRequestTypeDef",
    "GetMonitorResponseTypeDef",
    "GetQueueEnvironmentRequestRequestTypeDef",
    "GetQueueEnvironmentResponseTypeDef",
    "GetQueueFleetAssociationRequestQueueFleetAssociationStoppedWaitTypeDef",
    "GetQueueFleetAssociationRequestRequestTypeDef",
    "GetQueueFleetAssociationResponseTypeDef",
    "GetQueueRequestQueueSchedulingBlockedWaitTypeDef",
    "GetQueueRequestQueueSchedulingWaitTypeDef",
    "GetQueueRequestRequestTypeDef",
    "GetQueueResponseTypeDef",
    "GetSessionActionRequestRequestTypeDef",
    "GetSessionActionResponseTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef",
    "GetSessionsStatisticsAggregationRequestRequestTypeDef",
    "GetSessionsStatisticsAggregationResponseTypeDef",
    "GetStepRequestRequestTypeDef",
    "GetStepResponseTypeDef",
    "GetStorageProfileForQueueRequestRequestTypeDef",
    "GetStorageProfileForQueueResponseTypeDef",
    "GetStorageProfileRequestRequestTypeDef",
    "GetStorageProfileResponseTypeDef",
    "GetTaskRequestRequestTypeDef",
    "GetTaskResponseTypeDef",
    "GetWorkerRequestRequestTypeDef",
    "GetWorkerResponseTypeDef",
    "HostPropertiesRequestTypeDef",
    "HostPropertiesResponseTypeDef",
    "IpAddressesOutputTypeDef",
    "IpAddressesTypeDef",
    "IpAddressesUnionTypeDef",
    "JobAttachmentDetailsEntityTypeDef",
    "JobAttachmentDetailsErrorTypeDef",
    "JobAttachmentDetailsIdentifiersTypeDef",
    "JobAttachmentSettingsTypeDef",
    "JobDetailsEntityTypeDef",
    "JobDetailsErrorTypeDef",
    "JobDetailsIdentifiersTypeDef",
    "JobEntityIdentifiersUnionTypeDef",
    "JobEntityTypeDef",
    "JobMemberTypeDef",
    "JobParameterTypeDef",
    "JobRunAsUserTypeDef",
    "JobSearchSummaryTypeDef",
    "JobSummaryTypeDef",
    "LicenseEndpointSummaryTypeDef",
    "ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef",
    "ListAvailableMeteredProductsRequestRequestTypeDef",
    "ListAvailableMeteredProductsResponseTypeDef",
    "ListBudgetsRequestListBudgetsPaginateTypeDef",
    "ListBudgetsRequestRequestTypeDef",
    "ListBudgetsResponseTypeDef",
    "ListFarmMembersRequestListFarmMembersPaginateTypeDef",
    "ListFarmMembersRequestRequestTypeDef",
    "ListFarmMembersResponseTypeDef",
    "ListFarmsRequestListFarmsPaginateTypeDef",
    "ListFarmsRequestRequestTypeDef",
    "ListFarmsResponseTypeDef",
    "ListFleetMembersRequestListFleetMembersPaginateTypeDef",
    "ListFleetMembersRequestRequestTypeDef",
    "ListFleetMembersResponseTypeDef",
    "ListFleetsRequestListFleetsPaginateTypeDef",
    "ListFleetsRequestRequestTypeDef",
    "ListFleetsResponseTypeDef",
    "ListJobMembersRequestListJobMembersPaginateTypeDef",
    "ListJobMembersRequestRequestTypeDef",
    "ListJobMembersResponseTypeDef",
    "ListJobParameterDefinitionsRequestListJobParameterDefinitionsPaginateTypeDef",
    "ListJobParameterDefinitionsRequestRequestTypeDef",
    "ListJobParameterDefinitionsResponseTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListJobsResponseTypeDef",
    "ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef",
    "ListLicenseEndpointsRequestRequestTypeDef",
    "ListLicenseEndpointsResponseTypeDef",
    "ListMeteredProductsRequestListMeteredProductsPaginateTypeDef",
    "ListMeteredProductsRequestRequestTypeDef",
    "ListMeteredProductsResponseTypeDef",
    "ListMonitorsRequestListMonitorsPaginateTypeDef",
    "ListMonitorsRequestRequestTypeDef",
    "ListMonitorsResponseTypeDef",
    "ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef",
    "ListQueueEnvironmentsRequestRequestTypeDef",
    "ListQueueEnvironmentsResponseTypeDef",
    "ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef",
    "ListQueueFleetAssociationsRequestRequestTypeDef",
    "ListQueueFleetAssociationsResponseTypeDef",
    "ListQueueMembersRequestListQueueMembersPaginateTypeDef",
    "ListQueueMembersRequestRequestTypeDef",
    "ListQueueMembersResponseTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "ListQueuesResponseTypeDef",
    "ListSessionActionsRequestListSessionActionsPaginateTypeDef",
    "ListSessionActionsRequestRequestTypeDef",
    "ListSessionActionsResponseTypeDef",
    "ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef",
    "ListSessionsForWorkerRequestRequestTypeDef",
    "ListSessionsForWorkerResponseTypeDef",
    "ListSessionsRequestListSessionsPaginateTypeDef",
    "ListSessionsRequestRequestTypeDef",
    "ListSessionsResponseTypeDef",
    "ListStepConsumersRequestListStepConsumersPaginateTypeDef",
    "ListStepConsumersRequestRequestTypeDef",
    "ListStepConsumersResponseTypeDef",
    "ListStepDependenciesRequestListStepDependenciesPaginateTypeDef",
    "ListStepDependenciesRequestRequestTypeDef",
    "ListStepDependenciesResponseTypeDef",
    "ListStepsRequestListStepsPaginateTypeDef",
    "ListStepsRequestRequestTypeDef",
    "ListStepsResponseTypeDef",
    "ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef",
    "ListStorageProfilesForQueueRequestRequestTypeDef",
    "ListStorageProfilesForQueueResponseTypeDef",
    "ListStorageProfilesRequestListStorageProfilesPaginateTypeDef",
    "ListStorageProfilesRequestRequestTypeDef",
    "ListStorageProfilesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTasksRequestListTasksPaginateTypeDef",
    "ListTasksRequestRequestTypeDef",
    "ListTasksResponseTypeDef",
    "ListWorkersRequestListWorkersPaginateTypeDef",
    "ListWorkersRequestRequestTypeDef",
    "ListWorkersResponseTypeDef",
    "LogConfigurationTypeDef",
    "ManifestPropertiesOutputTypeDef",
    "ManifestPropertiesTypeDef",
    "ManifestPropertiesUnionTypeDef",
    "MemoryMiBRangeTypeDef",
    "MeteredProductSummaryTypeDef",
    "MonitorSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterFilterExpressionTypeDef",
    "ParameterSortExpressionTypeDef",
    "ParameterSpaceTypeDef",
    "PathMappingRuleTypeDef",
    "PosixUserTypeDef",
    "PutMeteredProductRequestRequestTypeDef",
    "QueueEnvironmentSummaryTypeDef",
    "QueueFleetAssociationSummaryTypeDef",
    "QueueMemberTypeDef",
    "QueueSummaryTypeDef",
    "ResponseBudgetActionTypeDef",
    "ResponseMetadataTypeDef",
    "S3LocationTypeDef",
    "SearchFilterExpressionTypeDef",
    "SearchGroupedFilterExpressionsTypeDef",
    "SearchJobsRequestRequestTypeDef",
    "SearchJobsResponseTypeDef",
    "SearchSortExpressionTypeDef",
    "SearchStepsRequestRequestTypeDef",
    "SearchStepsResponseTypeDef",
    "SearchTasksRequestRequestTypeDef",
    "SearchTasksResponseTypeDef",
    "SearchTermFilterExpressionTypeDef",
    "SearchWorkersRequestRequestTypeDef",
    "SearchWorkersResponseTypeDef",
    "ServiceManagedEc2FleetConfigurationOutputTypeDef",
    "ServiceManagedEc2FleetConfigurationTypeDef",
    "ServiceManagedEc2FleetConfigurationUnionTypeDef",
    "ServiceManagedEc2InstanceCapabilitiesOutputTypeDef",
    "ServiceManagedEc2InstanceCapabilitiesTypeDef",
    "ServiceManagedEc2InstanceCapabilitiesUnionTypeDef",
    "ServiceManagedEc2InstanceMarketOptionsTypeDef",
    "SessionActionDefinitionSummaryTypeDef",
    "SessionActionDefinitionTypeDef",
    "SessionActionSummaryTypeDef",
    "SessionSummaryTypeDef",
    "SessionsStatisticsResourcesTypeDef",
    "StartSessionsStatisticsAggregationRequestRequestTypeDef",
    "StartSessionsStatisticsAggregationResponseTypeDef",
    "StatisticsTypeDef",
    "StatsTypeDef",
    "StepAmountCapabilityTypeDef",
    "StepAttributeCapabilityTypeDef",
    "StepConsumerTypeDef",
    "StepDependencyTypeDef",
    "StepDetailsEntityTypeDef",
    "StepDetailsErrorTypeDef",
    "StepDetailsIdentifiersTypeDef",
    "StepParameterTypeDef",
    "StepRequiredCapabilitiesTypeDef",
    "StepSearchSummaryTypeDef",
    "StepSummaryTypeDef",
    "StorageProfileSummaryTypeDef",
    "StringFilterExpressionTypeDef",
    "SyncInputJobAttachmentsSessionActionDefinitionSummaryTypeDef",
    "SyncInputJobAttachmentsSessionActionDefinitionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TaskParameterValueTypeDef",
    "TaskRunSessionActionDefinitionSummaryTypeDef",
    "TaskRunSessionActionDefinitionTypeDef",
    "TaskSearchSummaryTypeDef",
    "TaskSummaryTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBudgetRequestRequestTypeDef",
    "UpdateFarmRequestRequestTypeDef",
    "UpdateFleetRequestRequestTypeDef",
    "UpdateJobRequestRequestTypeDef",
    "UpdateMonitorRequestRequestTypeDef",
    "UpdateQueueEnvironmentRequestRequestTypeDef",
    "UpdateQueueFleetAssociationRequestRequestTypeDef",
    "UpdateQueueRequestRequestTypeDef",
    "UpdateSessionRequestRequestTypeDef",
    "UpdateStepRequestRequestTypeDef",
    "UpdateStorageProfileRequestRequestTypeDef",
    "UpdateTaskRequestRequestTypeDef",
    "UpdateWorkerRequestRequestTypeDef",
    "UpdateWorkerResponseTypeDef",
    "UpdateWorkerScheduleRequestRequestTypeDef",
    "UpdateWorkerScheduleResponseTypeDef",
    "UpdatedSessionActionInfoTypeDef",
    "UsageTrackingResourceTypeDef",
    "UserJobsFirstTypeDef",
    "VCpuCountRangeTypeDef",
    "WaiterConfigTypeDef",
    "WindowsUserTypeDef",
    "WorkerAmountCapabilityTypeDef",
    "WorkerAttributeCapabilityTypeDef",
    "WorkerCapabilitiesTypeDef",
    "WorkerSearchSummaryTypeDef",
    "WorkerSessionSummaryTypeDef",
    "WorkerSummaryTypeDef",
)

AcceleratorCountRangeTypeDef = TypedDict(
    "AcceleratorCountRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)

class AcceleratorSelectionTypeDef(TypedDict):
    name: AcceleratorNameType
    runtime: NotRequired[str]

AcceleratorTotalMemoryMiBRangeTypeDef = TypedDict(
    "AcceleratorTotalMemoryMiBRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)

class AssignedEnvironmentEnterSessionActionDefinitionTypeDef(TypedDict):
    environmentId: str

class AssignedEnvironmentExitSessionActionDefinitionTypeDef(TypedDict):
    environmentId: str

class AssignedSyncInputJobAttachmentsSessionActionDefinitionTypeDef(TypedDict):
    stepId: NotRequired[str]

class LogConfigurationTypeDef(TypedDict):
    logDriver: str
    options: NotRequired[Dict[str, str]]
    parameters: NotRequired[Dict[str, str]]
    error: NotRequired[str]

TaskParameterValueTypeDef = TypedDict(
    "TaskParameterValueTypeDef",
    {
        "int": NotRequired[str],
        "float": NotRequired[str],
        "string": NotRequired[str],
        "path": NotRequired[str],
    },
)

class AssociateMemberToFarmRequestRequestTypeDef(TypedDict):
    farmId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class AssociateMemberToFleetRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class AssociateMemberToJobRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class AssociateMemberToQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class AssumeFleetRoleForReadRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str

class AwsCredentialsTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str
    expiration: datetime

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssumeFleetRoleForWorkerRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str

class AssumeQueueRoleForReadRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str

class AssumeQueueRoleForUserRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str

class AssumeQueueRoleForWorkerRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str
    queueId: str

class ManifestPropertiesOutputTypeDef(TypedDict):
    rootPath: str
    rootPathFormat: PathFormatType
    fileSystemLocationName: NotRequired[str]
    outputRelativeDirectories: NotRequired[List[str]]
    inputManifestPath: NotRequired[str]
    inputManifestHash: NotRequired[str]

BudgetActionToAddTypeDef = TypedDict(
    "BudgetActionToAddTypeDef",
    {
        "type": BudgetActionTypeType,
        "thresholdPercentage": float,
        "description": NotRequired[str],
    },
)
BudgetActionToRemoveTypeDef = TypedDict(
    "BudgetActionToRemoveTypeDef",
    {
        "type": BudgetActionTypeType,
        "thresholdPercentage": float,
    },
)

class FixedBudgetScheduleOutputTypeDef(TypedDict):
    startTime: datetime
    endTime: datetime

class ConsumedUsagesTypeDef(TypedDict):
    approximateDollarUsage: float

class UsageTrackingResourceTypeDef(TypedDict):
    queueId: NotRequired[str]

class S3LocationTypeDef(TypedDict):
    bucketName: str
    key: str

class CreateFarmRequestRequestTypeDef(TypedDict):
    displayName: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

JobParameterTypeDef = TypedDict(
    "JobParameterTypeDef",
    {
        "int": NotRequired[str],
        "float": NotRequired[str],
        "string": NotRequired[str],
        "path": NotRequired[str],
    },
)

class CreateLicenseEndpointRequestRequestTypeDef(TypedDict):
    vpcId: str
    subnetIds: Sequence[str]
    securityGroupIds: Sequence[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateMonitorRequestRequestTypeDef(TypedDict):
    displayName: str
    identityCenterInstanceArn: str
    subdomain: str
    roleArn: str
    clientToken: NotRequired[str]

class CreateQueueEnvironmentRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    priority: int
    templateType: EnvironmentTemplateTypeType
    template: str
    clientToken: NotRequired[str]

class CreateQueueFleetAssociationRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    fleetId: str

class JobAttachmentSettingsTypeDef(TypedDict):
    s3BucketName: str
    rootPrefix: str

FileSystemLocationTypeDef = TypedDict(
    "FileSystemLocationTypeDef",
    {
        "name": str,
        "path": str,
        "type": FileSystemLocationTypeType,
    },
)
FleetAmountCapabilityTypeDef = TypedDict(
    "FleetAmountCapabilityTypeDef",
    {
        "name": str,
        "min": float,
        "max": NotRequired[float],
    },
)

class FleetAttributeCapabilityOutputTypeDef(TypedDict):
    name: str
    values: List[str]

MemoryMiBRangeTypeDef = TypedDict(
    "MemoryMiBRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)
VCpuCountRangeTypeDef = TypedDict(
    "VCpuCountRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)
TimestampTypeDef = Union[datetime, str]

class DeleteBudgetRequestRequestTypeDef(TypedDict):
    farmId: str
    budgetId: str

class DeleteFarmRequestRequestTypeDef(TypedDict):
    farmId: str

class DeleteFleetRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    clientToken: NotRequired[str]

class DeleteLicenseEndpointRequestRequestTypeDef(TypedDict):
    licenseEndpointId: str

class DeleteMeteredProductRequestRequestTypeDef(TypedDict):
    licenseEndpointId: str
    productId: str

class DeleteMonitorRequestRequestTypeDef(TypedDict):
    monitorId: str

class DeleteQueueEnvironmentRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    queueEnvironmentId: str

class DeleteQueueFleetAssociationRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    fleetId: str

class DeleteQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str

class DeleteStorageProfileRequestRequestTypeDef(TypedDict):
    farmId: str
    storageProfileId: str

class DeleteWorkerRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str

class DependencyCountsTypeDef(TypedDict):
    dependenciesResolved: int
    dependenciesUnresolved: int
    consumersResolved: int
    consumersUnresolved: int

class DisassociateMemberFromFarmRequestRequestTypeDef(TypedDict):
    farmId: str
    principalId: str

class DisassociateMemberFromFleetRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    principalId: str

class DisassociateMemberFromJobRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    principalId: str

class DisassociateMemberFromQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    principalId: str

class Ec2EbsVolumeTypeDef(TypedDict):
    sizeGiB: NotRequired[int]
    iops: NotRequired[int]
    throughputMiB: NotRequired[int]

class EnvironmentDetailsEntityTypeDef(TypedDict):
    jobId: str
    environmentId: str
    schemaVersion: str
    template: Dict[str, Any]

class EnvironmentDetailsErrorTypeDef(TypedDict):
    jobId: str
    environmentId: str
    code: JobEntityErrorCodeType
    message: str

class EnvironmentDetailsIdentifiersTypeDef(TypedDict):
    jobId: str
    environmentId: str

class EnvironmentEnterSessionActionDefinitionSummaryTypeDef(TypedDict):
    environmentId: str

class EnvironmentEnterSessionActionDefinitionTypeDef(TypedDict):
    environmentId: str

class EnvironmentExitSessionActionDefinitionSummaryTypeDef(TypedDict):
    environmentId: str

class EnvironmentExitSessionActionDefinitionTypeDef(TypedDict):
    environmentId: str

class FarmMemberTypeDef(TypedDict):
    farmId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class FarmSummaryTypeDef(TypedDict):
    farmId: str
    displayName: str
    createdAt: datetime
    createdBy: str
    kmsKeyArn: NotRequired[str]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class FieldSortExpressionTypeDef(TypedDict):
    sortOrder: SortOrderType
    name: str

class FleetAttributeCapabilityTypeDef(TypedDict):
    name: str
    values: Sequence[str]

class FleetMemberTypeDef(TypedDict):
    farmId: str
    fleetId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class GetBudgetRequestRequestTypeDef(TypedDict):
    farmId: str
    budgetId: str

ResponseBudgetActionTypeDef = TypedDict(
    "ResponseBudgetActionTypeDef",
    {
        "type": BudgetActionTypeType,
        "thresholdPercentage": float,
        "description": NotRequired[str],
    },
)

class GetFarmRequestRequestTypeDef(TypedDict):
    farmId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetFleetRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str

class JobAttachmentDetailsErrorTypeDef(TypedDict):
    jobId: str
    code: JobEntityErrorCodeType
    message: str

class JobDetailsErrorTypeDef(TypedDict):
    jobId: str
    code: JobEntityErrorCodeType
    message: str

class StepDetailsErrorTypeDef(TypedDict):
    jobId: str
    stepId: str
    code: JobEntityErrorCodeType
    message: str

class GetJobRequestRequestTypeDef(TypedDict):
    farmId: str
    jobId: str
    queueId: str

class GetLicenseEndpointRequestRequestTypeDef(TypedDict):
    licenseEndpointId: str

class GetMonitorRequestRequestTypeDef(TypedDict):
    monitorId: str

class GetQueueEnvironmentRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    queueEnvironmentId: str

class GetQueueFleetAssociationRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    fleetId: str

class GetQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str

class GetSessionActionRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    sessionActionId: str

class GetSessionRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    sessionId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetSessionsStatisticsAggregationRequestRequestTypeDef(TypedDict):
    farmId: str
    aggregationId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class GetStepRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str

class GetStorageProfileForQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    storageProfileId: str

class GetStorageProfileRequestRequestTypeDef(TypedDict):
    farmId: str
    storageProfileId: str

class GetTaskRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    taskId: str

class GetWorkerRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str

class IpAddressesOutputTypeDef(TypedDict):
    ipV4Addresses: NotRequired[List[str]]
    ipV6Addresses: NotRequired[List[str]]

class IpAddressesTypeDef(TypedDict):
    ipV4Addresses: NotRequired[Sequence[str]]
    ipV6Addresses: NotRequired[Sequence[str]]

class JobAttachmentDetailsIdentifiersTypeDef(TypedDict):
    jobId: str

class PathMappingRuleTypeDef(TypedDict):
    sourcePathFormat: PathFormatType
    sourcePath: str
    destinationPath: str

class JobDetailsIdentifiersTypeDef(TypedDict):
    jobId: str

class StepDetailsIdentifiersTypeDef(TypedDict):
    jobId: str
    stepId: str

class StepDetailsEntityTypeDef(TypedDict):
    jobId: str
    stepId: str
    schemaVersion: str
    template: Dict[str, Any]
    dependencies: List[str]

class JobMemberTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class PosixUserTypeDef(TypedDict):
    user: str
    group: str

class WindowsUserTypeDef(TypedDict):
    user: str
    passwordArn: str

class JobSummaryTypeDef(TypedDict):
    jobId: str
    name: str
    lifecycleStatus: JobLifecycleStatusType
    lifecycleStatusMessage: str
    priority: int
    createdAt: datetime
    createdBy: str
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    taskRunStatus: NotRequired[TaskRunStatusType]
    targetTaskRunStatus: NotRequired[JobTargetTaskRunStatusType]
    taskRunStatusCounts: NotRequired[Dict[TaskRunStatusType, int]]
    maxFailedTasksCount: NotRequired[int]
    maxRetriesPerTask: NotRequired[int]
    sourceJobId: NotRequired[str]

class LicenseEndpointSummaryTypeDef(TypedDict):
    licenseEndpointId: NotRequired[str]
    status: NotRequired[LicenseEndpointStatusType]
    statusMessage: NotRequired[str]
    vpcId: NotRequired[str]

class ListAvailableMeteredProductsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class MeteredProductSummaryTypeDef(TypedDict):
    productId: str
    family: str
    vendor: str
    port: int

class ListBudgetsRequestRequestTypeDef(TypedDict):
    farmId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    status: NotRequired[BudgetStatusType]

class ListFarmMembersRequestRequestTypeDef(TypedDict):
    farmId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListFarmsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    principalId: NotRequired[str]
    maxResults: NotRequired[int]

class ListFleetMembersRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListFleetsRequestRequestTypeDef(TypedDict):
    farmId: str
    principalId: NotRequired[str]
    displayName: NotRequired[str]
    status: NotRequired[FleetStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListJobMembersRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListJobParameterDefinitionsRequestRequestTypeDef(TypedDict):
    farmId: str
    jobId: str
    queueId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListJobsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    principalId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListLicenseEndpointsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListMeteredProductsRequestRequestTypeDef(TypedDict):
    licenseEndpointId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListMonitorsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class MonitorSummaryTypeDef(TypedDict):
    monitorId: str
    displayName: str
    subdomain: str
    url: str
    roleArn: str
    identityCenterInstanceArn: str
    identityCenterApplicationArn: str
    createdAt: datetime
    createdBy: str
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class ListQueueEnvironmentsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class QueueEnvironmentSummaryTypeDef(TypedDict):
    queueEnvironmentId: str
    name: str
    priority: int

class ListQueueFleetAssociationsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: NotRequired[str]
    fleetId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class QueueFleetAssociationSummaryTypeDef(TypedDict):
    queueId: str
    fleetId: str
    status: QueueFleetAssociationStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class ListQueueMembersRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class QueueMemberTypeDef(TypedDict):
    farmId: str
    queueId: str
    principalId: str
    principalType: PrincipalTypeType
    identityStoreId: str
    membershipLevel: MembershipLevelType

class ListQueuesRequestRequestTypeDef(TypedDict):
    farmId: str
    principalId: NotRequired[str]
    status: NotRequired[QueueStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class QueueSummaryTypeDef(TypedDict):
    farmId: str
    queueId: str
    displayName: str
    status: QueueStatusType
    defaultBudgetAction: DefaultQueueBudgetActionType
    createdAt: datetime
    createdBy: str
    blockedReason: NotRequired[QueueBlockedReasonType]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class ListSessionActionsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    sessionId: NotRequired[str]
    taskId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListSessionsForWorkerRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class WorkerSessionSummaryTypeDef(TypedDict):
    sessionId: str
    queueId: str
    jobId: str
    startedAt: datetime
    lifecycleStatus: SessionLifecycleStatusType
    endedAt: NotRequired[datetime]
    targetLifecycleStatus: NotRequired[Literal["ENDED"]]

class ListSessionsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SessionSummaryTypeDef(TypedDict):
    sessionId: str
    fleetId: str
    workerId: str
    startedAt: datetime
    lifecycleStatus: SessionLifecycleStatusType
    endedAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    targetLifecycleStatus: NotRequired[Literal["ENDED"]]

class ListStepConsumersRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class StepConsumerTypeDef(TypedDict):
    stepId: str
    status: DependencyConsumerResolutionStatusType

class ListStepDependenciesRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class StepDependencyTypeDef(TypedDict):
    stepId: str
    status: DependencyConsumerResolutionStatusType

class ListStepsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListStorageProfilesForQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class StorageProfileSummaryTypeDef(TypedDict):
    storageProfileId: str
    displayName: str
    osFamily: StorageProfileOperatingSystemFamilyType

class ListStorageProfilesRequestRequestTypeDef(TypedDict):
    farmId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListTasksRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListWorkersRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ManifestPropertiesTypeDef(TypedDict):
    rootPath: str
    rootPathFormat: PathFormatType
    fileSystemLocationName: NotRequired[str]
    outputRelativeDirectories: NotRequired[Sequence[str]]
    inputManifestPath: NotRequired[str]
    inputManifestHash: NotRequired[str]

ParameterFilterExpressionTypeDef = TypedDict(
    "ParameterFilterExpressionTypeDef",
    {
        "name": str,
        "operator": ComparisonOperatorType,
        "value": str,
    },
)

class ParameterSortExpressionTypeDef(TypedDict):
    sortOrder: SortOrderType
    name: str

StepParameterTypeDef = TypedDict(
    "StepParameterTypeDef",
    {
        "name": str,
        "type": StepParameterTypeType,
    },
)

class PutMeteredProductRequestRequestTypeDef(TypedDict):
    licenseEndpointId: str
    productId: str

class SearchTermFilterExpressionTypeDef(TypedDict):
    searchTerm: str

StringFilterExpressionTypeDef = TypedDict(
    "StringFilterExpressionTypeDef",
    {
        "name": str,
        "operator": ComparisonOperatorType,
        "value": str,
    },
)

class UserJobsFirstTypeDef(TypedDict):
    userIdentityId: str

ServiceManagedEc2InstanceMarketOptionsTypeDef = TypedDict(
    "ServiceManagedEc2InstanceMarketOptionsTypeDef",
    {
        "type": Ec2MarketTypeType,
    },
)

class SyncInputJobAttachmentsSessionActionDefinitionSummaryTypeDef(TypedDict):
    stepId: NotRequired[str]

class TaskRunSessionActionDefinitionSummaryTypeDef(TypedDict):
    taskId: str
    stepId: str

class SyncInputJobAttachmentsSessionActionDefinitionTypeDef(TypedDict):
    stepId: NotRequired[str]

class SessionsStatisticsResourcesTypeDef(TypedDict):
    queueIds: NotRequired[Sequence[str]]
    fleetIds: NotRequired[Sequence[str]]

StatsTypeDef = TypedDict(
    "StatsTypeDef",
    {
        "min": NotRequired[float],
        "max": NotRequired[float],
        "avg": NotRequired[float],
        "sum": NotRequired[float],
    },
)
StepAmountCapabilityTypeDef = TypedDict(
    "StepAmountCapabilityTypeDef",
    {
        "name": str,
        "min": NotRequired[float],
        "max": NotRequired[float],
        "value": NotRequired[float],
    },
)

class StepAttributeCapabilityTypeDef(TypedDict):
    name: str
    anyOf: NotRequired[List[str]]
    allOf: NotRequired[List[str]]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: NotRequired[Mapping[str, str]]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateFarmRequestRequestTypeDef(TypedDict):
    farmId: str
    displayName: NotRequired[str]
    description: NotRequired[str]

class UpdateJobRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    clientToken: NotRequired[str]
    targetTaskRunStatus: NotRequired[JobTargetTaskRunStatusType]
    priority: NotRequired[int]
    maxFailedTasksCount: NotRequired[int]
    maxRetriesPerTask: NotRequired[int]
    lifecycleStatus: NotRequired[Literal["ARCHIVED"]]

class UpdateMonitorRequestRequestTypeDef(TypedDict):
    monitorId: str
    subdomain: NotRequired[str]
    displayName: NotRequired[str]
    roleArn: NotRequired[str]

class UpdateQueueEnvironmentRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    queueEnvironmentId: str
    clientToken: NotRequired[str]
    priority: NotRequired[int]
    templateType: NotRequired[EnvironmentTemplateTypeType]
    template: NotRequired[str]

class UpdateQueueFleetAssociationRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    fleetId: str
    status: UpdateQueueFleetAssociationStatusType

class UpdateSessionRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    sessionId: str
    targetLifecycleStatus: Literal["ENDED"]
    clientToken: NotRequired[str]

class UpdateStepRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    targetTaskRunStatus: StepTargetTaskRunStatusType
    clientToken: NotRequired[str]

class UpdateTaskRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    taskId: str
    targetRunStatus: TaskTargetRunStatusType
    clientToken: NotRequired[str]

class WorkerAmountCapabilityTypeDef(TypedDict):
    name: str
    value: float

class WorkerAttributeCapabilityTypeDef(TypedDict):
    name: str
    values: Sequence[str]

class AcceleratorCapabilitiesOutputTypeDef(TypedDict):
    selections: List[AcceleratorSelectionTypeDef]
    count: NotRequired[AcceleratorCountRangeTypeDef]

class AcceleratorCapabilitiesTypeDef(TypedDict):
    selections: Sequence[AcceleratorSelectionTypeDef]
    count: NotRequired[AcceleratorCountRangeTypeDef]

class AssignedTaskRunSessionActionDefinitionTypeDef(TypedDict):
    taskId: str
    stepId: str
    parameters: Dict[str, TaskParameterValueTypeDef]

class TaskRunSessionActionDefinitionTypeDef(TypedDict):
    taskId: str
    stepId: str
    parameters: Dict[str, TaskParameterValueTypeDef]

class TaskSearchSummaryTypeDef(TypedDict):
    taskId: NotRequired[str]
    stepId: NotRequired[str]
    jobId: NotRequired[str]
    queueId: NotRequired[str]
    runStatus: NotRequired[TaskRunStatusType]
    targetRunStatus: NotRequired[TaskTargetRunStatusType]
    parameters: NotRequired[Dict[str, TaskParameterValueTypeDef]]
    failureRetryCount: NotRequired[int]
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]

class TaskSummaryTypeDef(TypedDict):
    taskId: str
    createdAt: datetime
    createdBy: str
    runStatus: TaskRunStatusType
    targetRunStatus: NotRequired[TaskTargetRunStatusType]
    failureRetryCount: NotRequired[int]
    parameters: NotRequired[Dict[str, TaskParameterValueTypeDef]]
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    latestSessionActionId: NotRequired[str]

class AssumeFleetRoleForReadResponseTypeDef(TypedDict):
    credentials: AwsCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssumeFleetRoleForWorkerResponseTypeDef(TypedDict):
    credentials: AwsCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssumeQueueRoleForReadResponseTypeDef(TypedDict):
    credentials: AwsCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssumeQueueRoleForUserResponseTypeDef(TypedDict):
    credentials: AwsCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssumeQueueRoleForWorkerResponseTypeDef(TypedDict):
    credentials: AwsCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CopyJobTemplateResponseTypeDef(TypedDict):
    templateType: JobTemplateTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBudgetResponseTypeDef(TypedDict):
    budgetId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFarmResponseTypeDef(TypedDict):
    farmId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFleetResponseTypeDef(TypedDict):
    fleetId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateJobResponseTypeDef(TypedDict):
    jobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLicenseEndpointResponseTypeDef(TypedDict):
    licenseEndpointId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMonitorResponseTypeDef(TypedDict):
    monitorId: str
    identityCenterApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateQueueEnvironmentResponseTypeDef(TypedDict):
    queueEnvironmentId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateQueueResponseTypeDef(TypedDict):
    queueId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStorageProfileResponseTypeDef(TypedDict):
    storageProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorkerResponseTypeDef(TypedDict):
    workerId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetFarmResponseTypeDef(TypedDict):
    farmId: str
    displayName: str
    description: str
    kmsKeyArn: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetLicenseEndpointResponseTypeDef(TypedDict):
    licenseEndpointId: str
    status: LicenseEndpointStatusType
    statusMessage: str
    vpcId: str
    dnsName: str
    subnetIds: List[str]
    securityGroupIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetMonitorResponseTypeDef(TypedDict):
    monitorId: str
    displayName: str
    subdomain: str
    url: str
    roleArn: str
    identityCenterInstanceArn: str
    identityCenterApplicationArn: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetQueueEnvironmentResponseTypeDef(TypedDict):
    queueEnvironmentId: str
    name: str
    priority: int
    templateType: EnvironmentTemplateTypeType
    template: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetQueueFleetAssociationResponseTypeDef(TypedDict):
    queueId: str
    fleetId: str
    status: QueueFleetAssociationStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetTaskResponseTypeDef(TypedDict):
    taskId: str
    createdAt: datetime
    createdBy: str
    runStatus: TaskRunStatusType
    targetRunStatus: TaskTargetRunStatusType
    failureRetryCount: int
    parameters: Dict[str, TaskParameterValueTypeDef]
    startedAt: datetime
    endedAt: datetime
    updatedAt: datetime
    updatedBy: str
    latestSessionActionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListJobParameterDefinitionsResponseTypeDef(TypedDict):
    jobParameterDefinitions: List[Dict[str, Any]]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartSessionsStatisticsAggregationResponseTypeDef(TypedDict):
    aggregationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWorkerResponseTypeDef(TypedDict):
    log: LogConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AttachmentsOutputTypeDef(TypedDict):
    manifests: List[ManifestPropertiesOutputTypeDef]
    fileSystem: NotRequired[JobAttachmentsFileSystemType]

class BudgetScheduleOutputTypeDef(TypedDict):
    fixed: NotRequired[FixedBudgetScheduleOutputTypeDef]

class BudgetSummaryTypeDef(TypedDict):
    budgetId: str
    usageTrackingResource: UsageTrackingResourceTypeDef
    status: BudgetStatusType
    displayName: str
    approximateDollarLimit: float
    usages: ConsumedUsagesTypeDef
    createdBy: str
    createdAt: datetime
    description: NotRequired[str]
    updatedBy: NotRequired[str]
    updatedAt: NotRequired[datetime]

class CopyJobTemplateRequestRequestTypeDef(TypedDict):
    farmId: str
    jobId: str
    queueId: str
    targetS3Location: S3LocationTypeDef

class JobSearchSummaryTypeDef(TypedDict):
    jobId: NotRequired[str]
    queueId: NotRequired[str]
    name: NotRequired[str]
    lifecycleStatus: NotRequired[JobLifecycleStatusType]
    lifecycleStatusMessage: NotRequired[str]
    taskRunStatus: NotRequired[TaskRunStatusType]
    targetTaskRunStatus: NotRequired[JobTargetTaskRunStatusType]
    taskRunStatusCounts: NotRequired[Dict[TaskRunStatusType, int]]
    priority: NotRequired[int]
    maxFailedTasksCount: NotRequired[int]
    maxRetriesPerTask: NotRequired[int]
    createdBy: NotRequired[str]
    createdAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    jobParameters: NotRequired[Dict[str, JobParameterTypeDef]]
    sourceJobId: NotRequired[str]

class CreateStorageProfileRequestRequestTypeDef(TypedDict):
    farmId: str
    displayName: str
    osFamily: StorageProfileOperatingSystemFamilyType
    clientToken: NotRequired[str]
    fileSystemLocations: NotRequired[Sequence[FileSystemLocationTypeDef]]

class GetStorageProfileForQueueResponseTypeDef(TypedDict):
    storageProfileId: str
    displayName: str
    osFamily: StorageProfileOperatingSystemFamilyType
    fileSystemLocations: List[FileSystemLocationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetStorageProfileResponseTypeDef(TypedDict):
    storageProfileId: str
    displayName: str
    osFamily: StorageProfileOperatingSystemFamilyType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    fileSystemLocations: List[FileSystemLocationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateStorageProfileRequestRequestTypeDef(TypedDict):
    farmId: str
    storageProfileId: str
    clientToken: NotRequired[str]
    displayName: NotRequired[str]
    osFamily: NotRequired[StorageProfileOperatingSystemFamilyType]
    fileSystemLocationsToAdd: NotRequired[Sequence[FileSystemLocationTypeDef]]
    fileSystemLocationsToRemove: NotRequired[Sequence[FileSystemLocationTypeDef]]

class FleetCapabilitiesTypeDef(TypedDict):
    amounts: NotRequired[List[FleetAmountCapabilityTypeDef]]
    attributes: NotRequired[List[FleetAttributeCapabilityOutputTypeDef]]

class CustomerManagedWorkerCapabilitiesOutputTypeDef(TypedDict):
    vCpuCount: VCpuCountRangeTypeDef
    memoryMiB: MemoryMiBRangeTypeDef
    osFamily: CustomerManagedFleetOperatingSystemFamilyType
    cpuArchitectureType: CpuArchitectureTypeType
    acceleratorTypes: NotRequired[List[Literal["gpu"]]]
    acceleratorCount: NotRequired[AcceleratorCountRangeTypeDef]
    acceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBRangeTypeDef]
    customAmounts: NotRequired[List[FleetAmountCapabilityTypeDef]]
    customAttributes: NotRequired[List[FleetAttributeCapabilityOutputTypeDef]]

DateTimeFilterExpressionTypeDef = TypedDict(
    "DateTimeFilterExpressionTypeDef",
    {
        "name": str,
        "operator": ComparisonOperatorType,
        "dateTime": TimestampTypeDef,
    },
)

class FixedBudgetScheduleTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef

class UpdatedSessionActionInfoTypeDef(TypedDict):
    completedStatus: NotRequired[CompletedStatusType]
    processExitCode: NotRequired[int]
    progressMessage: NotRequired[str]
    startedAt: NotRequired[TimestampTypeDef]
    endedAt: NotRequired[TimestampTypeDef]
    updatedAt: NotRequired[TimestampTypeDef]
    progressPercent: NotRequired[float]

class StepSummaryTypeDef(TypedDict):
    stepId: str
    name: str
    lifecycleStatus: StepLifecycleStatusType
    taskRunStatus: TaskRunStatusType
    taskRunStatusCounts: Dict[TaskRunStatusType, int]
    createdAt: datetime
    createdBy: str
    lifecycleStatusMessage: NotRequired[str]
    targetTaskRunStatus: NotRequired[StepTargetTaskRunStatusType]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    dependencyCounts: NotRequired[DependencyCountsTypeDef]

class ListFarmMembersResponseTypeDef(TypedDict):
    members: List[FarmMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFarmsResponseTypeDef(TypedDict):
    farms: List[FarmSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

FleetAttributeCapabilityUnionTypeDef = Union[
    FleetAttributeCapabilityTypeDef, FleetAttributeCapabilityOutputTypeDef
]

class ListFleetMembersResponseTypeDef(TypedDict):
    members: List[FleetMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetFleetRequestFleetActiveWaitTypeDef(TypedDict):
    farmId: str
    fleetId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetJobRequestJobCreateCompleteWaitTypeDef(TypedDict):
    farmId: str
    jobId: str
    queueId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLicenseEndpointRequestLicenseEndpointDeletedWaitTypeDef(TypedDict):
    licenseEndpointId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLicenseEndpointRequestLicenseEndpointValidWaitTypeDef(TypedDict):
    licenseEndpointId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetQueueFleetAssociationRequestQueueFleetAssociationStoppedWaitTypeDef(TypedDict):
    farmId: str
    queueId: str
    fleetId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetQueueRequestQueueSchedulingBlockedWaitTypeDef(TypedDict):
    farmId: str
    queueId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetQueueRequestQueueSchedulingWaitTypeDef(TypedDict):
    farmId: str
    queueId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetJobEntityErrorTypeDef(TypedDict):
    jobDetails: NotRequired[JobDetailsErrorTypeDef]
    jobAttachmentDetails: NotRequired[JobAttachmentDetailsErrorTypeDef]
    stepDetails: NotRequired[StepDetailsErrorTypeDef]
    environmentDetails: NotRequired[EnvironmentDetailsErrorTypeDef]

class GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef(
    TypedDict
):
    farmId: str
    aggregationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBudgetsRequestListBudgetsPaginateTypeDef(TypedDict):
    farmId: str
    status: NotRequired[BudgetStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFarmMembersRequestListFarmMembersPaginateTypeDef(TypedDict):
    farmId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFarmsRequestListFarmsPaginateTypeDef(TypedDict):
    principalId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFleetMembersRequestListFleetMembersPaginateTypeDef(TypedDict):
    farmId: str
    fleetId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFleetsRequestListFleetsPaginateTypeDef(TypedDict):
    farmId: str
    principalId: NotRequired[str]
    displayName: NotRequired[str]
    status: NotRequired[FleetStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListJobMembersRequestListJobMembersPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListJobParameterDefinitionsRequestListJobParameterDefinitionsPaginateTypeDef(TypedDict):
    farmId: str
    jobId: str
    queueId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListJobsRequestListJobsPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    principalId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMeteredProductsRequestListMeteredProductsPaginateTypeDef(TypedDict):
    licenseEndpointId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMonitorsRequestListMonitorsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef(TypedDict):
    farmId: str
    queueId: NotRequired[str]
    fleetId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQueueMembersRequestListQueueMembersPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQueuesRequestListQueuesPaginateTypeDef(TypedDict):
    farmId: str
    principalId: NotRequired[str]
    status: NotRequired[QueueStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSessionActionsRequestListSessionActionsPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    sessionId: NotRequired[str]
    taskId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSessionsRequestListSessionsPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStepConsumersRequestListStepConsumersPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStepDependenciesRequestListStepDependenciesPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStepsRequestListStepsPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStorageProfilesRequestListStorageProfilesPaginateTypeDef(TypedDict):
    farmId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTasksRequestListTasksPaginateTypeDef(TypedDict):
    farmId: str
    queueId: str
    jobId: str
    stepId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkersRequestListWorkersPaginateTypeDef(TypedDict):
    farmId: str
    fleetId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class HostPropertiesResponseTypeDef(TypedDict):
    ipAddresses: NotRequired[IpAddressesOutputTypeDef]
    hostName: NotRequired[str]
    ec2InstanceArn: NotRequired[str]
    ec2InstanceType: NotRequired[str]

IpAddressesUnionTypeDef = Union[IpAddressesTypeDef, IpAddressesOutputTypeDef]

class JobEntityIdentifiersUnionTypeDef(TypedDict):
    jobDetails: NotRequired[JobDetailsIdentifiersTypeDef]
    jobAttachmentDetails: NotRequired[JobAttachmentDetailsIdentifiersTypeDef]
    stepDetails: NotRequired[StepDetailsIdentifiersTypeDef]
    environmentDetails: NotRequired[EnvironmentDetailsIdentifiersTypeDef]

class ListJobMembersResponseTypeDef(TypedDict):
    members: List[JobMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class JobRunAsUserTypeDef(TypedDict):
    runAs: RunAsType
    posix: NotRequired[PosixUserTypeDef]
    windows: NotRequired[WindowsUserTypeDef]

class ListJobsResponseTypeDef(TypedDict):
    jobs: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListLicenseEndpointsResponseTypeDef(TypedDict):
    licenseEndpoints: List[LicenseEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAvailableMeteredProductsResponseTypeDef(TypedDict):
    meteredProducts: List[MeteredProductSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMeteredProductsResponseTypeDef(TypedDict):
    meteredProducts: List[MeteredProductSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMonitorsResponseTypeDef(TypedDict):
    monitors: List[MonitorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListQueueEnvironmentsResponseTypeDef(TypedDict):
    environments: List[QueueEnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListQueueFleetAssociationsResponseTypeDef(TypedDict):
    queueFleetAssociations: List[QueueFleetAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListQueueMembersResponseTypeDef(TypedDict):
    members: List[QueueMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListQueuesResponseTypeDef(TypedDict):
    queues: List[QueueSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSessionsForWorkerResponseTypeDef(TypedDict):
    sessions: List[WorkerSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSessionsResponseTypeDef(TypedDict):
    sessions: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListStepConsumersResponseTypeDef(TypedDict):
    consumers: List[StepConsumerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListStepDependenciesResponseTypeDef(TypedDict):
    dependencies: List[StepDependencyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListStorageProfilesForQueueResponseTypeDef(TypedDict):
    storageProfiles: List[StorageProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListStorageProfilesResponseTypeDef(TypedDict):
    storageProfiles: List[StorageProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ManifestPropertiesUnionTypeDef = Union[ManifestPropertiesTypeDef, ManifestPropertiesOutputTypeDef]

class ParameterSpaceTypeDef(TypedDict):
    parameters: List[StepParameterTypeDef]
    combination: NotRequired[str]

class SearchSortExpressionTypeDef(TypedDict):
    userJobsFirst: NotRequired[UserJobsFirstTypeDef]
    fieldSort: NotRequired[FieldSortExpressionTypeDef]
    parameterSort: NotRequired[ParameterSortExpressionTypeDef]

class SessionActionDefinitionSummaryTypeDef(TypedDict):
    envEnter: NotRequired[EnvironmentEnterSessionActionDefinitionSummaryTypeDef]
    envExit: NotRequired[EnvironmentExitSessionActionDefinitionSummaryTypeDef]
    taskRun: NotRequired[TaskRunSessionActionDefinitionSummaryTypeDef]
    syncInputJobAttachments: NotRequired[
        SyncInputJobAttachmentsSessionActionDefinitionSummaryTypeDef
    ]

class StartSessionsStatisticsAggregationRequestRequestTypeDef(TypedDict):
    farmId: str
    resourceIds: SessionsStatisticsResourcesTypeDef
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    groupBy: Sequence[UsageGroupByFieldType]
    statistics: Sequence[UsageStatisticType]
    timezone: NotRequired[str]
    period: NotRequired[PeriodType]

class StatisticsTypeDef(TypedDict):
    count: int
    costInUsd: StatsTypeDef
    runtimeInSeconds: StatsTypeDef
    queueId: NotRequired[str]
    fleetId: NotRequired[str]
    jobId: NotRequired[str]
    jobName: NotRequired[str]
    userId: NotRequired[str]
    usageType: NotRequired[UsageTypeType]
    licenseProduct: NotRequired[str]
    instanceType: NotRequired[str]
    aggregationStartTime: NotRequired[datetime]
    aggregationEndTime: NotRequired[datetime]

class StepRequiredCapabilitiesTypeDef(TypedDict):
    attributes: List[StepAttributeCapabilityTypeDef]
    amounts: List[StepAmountCapabilityTypeDef]

class WorkerCapabilitiesTypeDef(TypedDict):
    amounts: Sequence[WorkerAmountCapabilityTypeDef]
    attributes: Sequence[WorkerAttributeCapabilityTypeDef]

class ServiceManagedEc2InstanceCapabilitiesOutputTypeDef(TypedDict):
    vCpuCount: VCpuCountRangeTypeDef
    memoryMiB: MemoryMiBRangeTypeDef
    osFamily: ServiceManagedFleetOperatingSystemFamilyType
    cpuArchitectureType: CpuArchitectureTypeType
    rootEbsVolume: NotRequired[Ec2EbsVolumeTypeDef]
    acceleratorCapabilities: NotRequired[AcceleratorCapabilitiesOutputTypeDef]
    allowedInstanceTypes: NotRequired[List[str]]
    excludedInstanceTypes: NotRequired[List[str]]
    customAmounts: NotRequired[List[FleetAmountCapabilityTypeDef]]
    customAttributes: NotRequired[List[FleetAttributeCapabilityOutputTypeDef]]

AcceleratorCapabilitiesUnionTypeDef = Union[
    AcceleratorCapabilitiesTypeDef, AcceleratorCapabilitiesOutputTypeDef
]

class AssignedSessionActionDefinitionTypeDef(TypedDict):
    envEnter: NotRequired[AssignedEnvironmentEnterSessionActionDefinitionTypeDef]
    envExit: NotRequired[AssignedEnvironmentExitSessionActionDefinitionTypeDef]
    taskRun: NotRequired[AssignedTaskRunSessionActionDefinitionTypeDef]
    syncInputJobAttachments: NotRequired[
        AssignedSyncInputJobAttachmentsSessionActionDefinitionTypeDef
    ]

class SessionActionDefinitionTypeDef(TypedDict):
    envEnter: NotRequired[EnvironmentEnterSessionActionDefinitionTypeDef]
    envExit: NotRequired[EnvironmentExitSessionActionDefinitionTypeDef]
    taskRun: NotRequired[TaskRunSessionActionDefinitionTypeDef]
    syncInputJobAttachments: NotRequired[SyncInputJobAttachmentsSessionActionDefinitionTypeDef]

class SearchTasksResponseTypeDef(TypedDict):
    tasks: List[TaskSearchSummaryTypeDef]
    nextItemOffset: int
    totalResults: int
    ResponseMetadata: ResponseMetadataTypeDef

class ListTasksResponseTypeDef(TypedDict):
    tasks: List[TaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetJobResponseTypeDef(TypedDict):
    jobId: str
    name: str
    lifecycleStatus: JobLifecycleStatusType
    lifecycleStatusMessage: str
    priority: int
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    startedAt: datetime
    endedAt: datetime
    taskRunStatus: TaskRunStatusType
    targetTaskRunStatus: JobTargetTaskRunStatusType
    taskRunStatusCounts: Dict[TaskRunStatusType, int]
    storageProfileId: str
    maxFailedTasksCount: int
    maxRetriesPerTask: int
    parameters: Dict[str, JobParameterTypeDef]
    attachments: AttachmentsOutputTypeDef
    description: str
    sourceJobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class JobAttachmentDetailsEntityTypeDef(TypedDict):
    jobId: str
    attachments: AttachmentsOutputTypeDef

class GetBudgetResponseTypeDef(TypedDict):
    budgetId: str
    usageTrackingResource: UsageTrackingResourceTypeDef
    status: BudgetStatusType
    displayName: str
    description: str
    approximateDollarLimit: float
    usages: ConsumedUsagesTypeDef
    actions: List[ResponseBudgetActionTypeDef]
    schedule: BudgetScheduleOutputTypeDef
    createdBy: str
    createdAt: datetime
    updatedBy: str
    updatedAt: datetime
    queueStoppedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListBudgetsResponseTypeDef(TypedDict):
    budgets: List[BudgetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchJobsResponseTypeDef(TypedDict):
    jobs: List[JobSearchSummaryTypeDef]
    nextItemOffset: int
    totalResults: int
    ResponseMetadata: ResponseMetadataTypeDef

class CustomerManagedFleetConfigurationOutputTypeDef(TypedDict):
    mode: AutoScalingModeType
    workerCapabilities: CustomerManagedWorkerCapabilitiesOutputTypeDef
    storageProfileId: NotRequired[str]

class SearchFilterExpressionTypeDef(TypedDict):
    dateTimeFilter: NotRequired[DateTimeFilterExpressionTypeDef]
    parameterFilter: NotRequired[ParameterFilterExpressionTypeDef]
    searchTermFilter: NotRequired[SearchTermFilterExpressionTypeDef]
    stringFilter: NotRequired[StringFilterExpressionTypeDef]
    groupFilter: NotRequired[Mapping[str, Any]]

FixedBudgetScheduleUnionTypeDef = Union[
    FixedBudgetScheduleTypeDef, FixedBudgetScheduleOutputTypeDef
]

class UpdateWorkerScheduleRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str
    updatedSessionActions: NotRequired[Mapping[str, UpdatedSessionActionInfoTypeDef]]

class ListStepsResponseTypeDef(TypedDict):
    steps: List[StepSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CustomerManagedWorkerCapabilitiesTypeDef(TypedDict):
    vCpuCount: VCpuCountRangeTypeDef
    memoryMiB: MemoryMiBRangeTypeDef
    osFamily: CustomerManagedFleetOperatingSystemFamilyType
    cpuArchitectureType: CpuArchitectureTypeType
    acceleratorTypes: NotRequired[Sequence[Literal["gpu"]]]
    acceleratorCount: NotRequired[AcceleratorCountRangeTypeDef]
    acceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBRangeTypeDef]
    customAmounts: NotRequired[Sequence[FleetAmountCapabilityTypeDef]]
    customAttributes: NotRequired[Sequence[FleetAttributeCapabilityUnionTypeDef]]

class GetSessionResponseTypeDef(TypedDict):
    sessionId: str
    fleetId: str
    workerId: str
    startedAt: datetime
    log: LogConfigurationTypeDef
    lifecycleStatus: SessionLifecycleStatusType
    endedAt: datetime
    updatedAt: datetime
    updatedBy: str
    targetLifecycleStatus: Literal["ENDED"]
    hostProperties: HostPropertiesResponseTypeDef
    workerLog: LogConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetWorkerResponseTypeDef(TypedDict):
    workerId: str
    farmId: str
    fleetId: str
    hostProperties: HostPropertiesResponseTypeDef
    status: WorkerStatusType
    log: LogConfigurationTypeDef
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class WorkerSearchSummaryTypeDef(TypedDict):
    fleetId: NotRequired[str]
    workerId: NotRequired[str]
    status: NotRequired[WorkerStatusType]
    hostProperties: NotRequired[HostPropertiesResponseTypeDef]
    createdBy: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    updatedAt: NotRequired[datetime]

class WorkerSummaryTypeDef(TypedDict):
    workerId: str
    farmId: str
    fleetId: str
    status: WorkerStatusType
    createdAt: datetime
    createdBy: str
    hostProperties: NotRequired[HostPropertiesResponseTypeDef]
    log: NotRequired[LogConfigurationTypeDef]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class HostPropertiesRequestTypeDef(TypedDict):
    ipAddresses: NotRequired[IpAddressesUnionTypeDef]
    hostName: NotRequired[str]

class BatchGetJobEntityRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str
    identifiers: Sequence[JobEntityIdentifiersUnionTypeDef]

class CreateQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    displayName: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    defaultBudgetAction: NotRequired[DefaultQueueBudgetActionType]
    jobAttachmentSettings: NotRequired[JobAttachmentSettingsTypeDef]
    roleArn: NotRequired[str]
    jobRunAsUser: NotRequired[JobRunAsUserTypeDef]
    requiredFileSystemLocationNames: NotRequired[Sequence[str]]
    allowedStorageProfileIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]

class GetQueueResponseTypeDef(TypedDict):
    queueId: str
    displayName: str
    description: str
    farmId: str
    status: QueueStatusType
    defaultBudgetAction: DefaultQueueBudgetActionType
    blockedReason: QueueBlockedReasonType
    jobAttachmentSettings: JobAttachmentSettingsTypeDef
    roleArn: str
    requiredFileSystemLocationNames: List[str]
    allowedStorageProfileIds: List[str]
    jobRunAsUser: JobRunAsUserTypeDef
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class JobDetailsEntityTypeDef(TypedDict):
    jobId: str
    logGroupName: str
    schemaVersion: str
    jobAttachmentSettings: NotRequired[JobAttachmentSettingsTypeDef]
    jobRunAsUser: NotRequired[JobRunAsUserTypeDef]
    queueRoleArn: NotRequired[str]
    parameters: NotRequired[Dict[str, JobParameterTypeDef]]
    pathMappingRules: NotRequired[List[PathMappingRuleTypeDef]]

class UpdateQueueRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    clientToken: NotRequired[str]
    displayName: NotRequired[str]
    description: NotRequired[str]
    defaultBudgetAction: NotRequired[DefaultQueueBudgetActionType]
    jobAttachmentSettings: NotRequired[JobAttachmentSettingsTypeDef]
    roleArn: NotRequired[str]
    jobRunAsUser: NotRequired[JobRunAsUserTypeDef]
    requiredFileSystemLocationNamesToAdd: NotRequired[Sequence[str]]
    requiredFileSystemLocationNamesToRemove: NotRequired[Sequence[str]]
    allowedStorageProfileIdsToAdd: NotRequired[Sequence[str]]
    allowedStorageProfileIdsToRemove: NotRequired[Sequence[str]]

class AttachmentsTypeDef(TypedDict):
    manifests: Sequence[ManifestPropertiesUnionTypeDef]
    fileSystem: NotRequired[JobAttachmentsFileSystemType]

class StepSearchSummaryTypeDef(TypedDict):
    stepId: NotRequired[str]
    jobId: NotRequired[str]
    queueId: NotRequired[str]
    name: NotRequired[str]
    lifecycleStatus: NotRequired[StepLifecycleStatusType]
    lifecycleStatusMessage: NotRequired[str]
    taskRunStatus: NotRequired[TaskRunStatusType]
    targetTaskRunStatus: NotRequired[StepTargetTaskRunStatusType]
    taskRunStatusCounts: NotRequired[Dict[TaskRunStatusType, int]]
    createdAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    parameterSpace: NotRequired[ParameterSpaceTypeDef]

class SessionActionSummaryTypeDef(TypedDict):
    sessionActionId: str
    status: SessionActionStatusType
    definition: SessionActionDefinitionSummaryTypeDef
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    workerUpdatedAt: NotRequired[datetime]
    progressPercent: NotRequired[float]

class GetSessionsStatisticsAggregationResponseTypeDef(TypedDict):
    statistics: List[StatisticsTypeDef]
    status: SessionsStatisticsAggregationStatusType
    statusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetStepResponseTypeDef(TypedDict):
    stepId: str
    name: str
    lifecycleStatus: StepLifecycleStatusType
    lifecycleStatusMessage: str
    taskRunStatus: TaskRunStatusType
    taskRunStatusCounts: Dict[TaskRunStatusType, int]
    targetTaskRunStatus: StepTargetTaskRunStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    startedAt: datetime
    endedAt: datetime
    dependencyCounts: DependencyCountsTypeDef
    requiredCapabilities: StepRequiredCapabilitiesTypeDef
    parameterSpace: ParameterSpaceTypeDef
    description: str
    ResponseMetadata: ResponseMetadataTypeDef

class ServiceManagedEc2FleetConfigurationOutputTypeDef(TypedDict):
    instanceCapabilities: ServiceManagedEc2InstanceCapabilitiesOutputTypeDef
    instanceMarketOptions: ServiceManagedEc2InstanceMarketOptionsTypeDef

class ServiceManagedEc2InstanceCapabilitiesTypeDef(TypedDict):
    vCpuCount: VCpuCountRangeTypeDef
    memoryMiB: MemoryMiBRangeTypeDef
    osFamily: ServiceManagedFleetOperatingSystemFamilyType
    cpuArchitectureType: CpuArchitectureTypeType
    rootEbsVolume: NotRequired[Ec2EbsVolumeTypeDef]
    acceleratorCapabilities: NotRequired[AcceleratorCapabilitiesUnionTypeDef]
    allowedInstanceTypes: NotRequired[Sequence[str]]
    excludedInstanceTypes: NotRequired[Sequence[str]]
    customAmounts: NotRequired[Sequence[FleetAmountCapabilityTypeDef]]
    customAttributes: NotRequired[Sequence[FleetAttributeCapabilityTypeDef]]

class AssignedSessionActionTypeDef(TypedDict):
    sessionActionId: str
    definition: AssignedSessionActionDefinitionTypeDef

class GetSessionActionResponseTypeDef(TypedDict):
    sessionActionId: str
    status: SessionActionStatusType
    startedAt: datetime
    endedAt: datetime
    workerUpdatedAt: datetime
    progressPercent: float
    sessionId: str
    processExitCode: int
    progressMessage: str
    definition: SessionActionDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

SearchGroupedFilterExpressionsTypeDef = TypedDict(
    "SearchGroupedFilterExpressionsTypeDef",
    {
        "filters": Sequence[SearchFilterExpressionTypeDef],
        "operator": LogicalOperatorType,
    },
)

class BudgetScheduleTypeDef(TypedDict):
    fixed: NotRequired[FixedBudgetScheduleUnionTypeDef]

CustomerManagedWorkerCapabilitiesUnionTypeDef = Union[
    CustomerManagedWorkerCapabilitiesTypeDef, CustomerManagedWorkerCapabilitiesOutputTypeDef
]

class SearchWorkersResponseTypeDef(TypedDict):
    workers: List[WorkerSearchSummaryTypeDef]
    nextItemOffset: int
    totalResults: int
    ResponseMetadata: ResponseMetadataTypeDef

class ListWorkersResponseTypeDef(TypedDict):
    workers: List[WorkerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateWorkerRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    hostProperties: NotRequired[HostPropertiesRequestTypeDef]
    clientToken: NotRequired[str]

class UpdateWorkerRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    workerId: str
    status: NotRequired[UpdatedWorkerStatusType]
    capabilities: NotRequired[WorkerCapabilitiesTypeDef]
    hostProperties: NotRequired[HostPropertiesRequestTypeDef]

class JobEntityTypeDef(TypedDict):
    jobDetails: NotRequired[JobDetailsEntityTypeDef]
    jobAttachmentDetails: NotRequired[JobAttachmentDetailsEntityTypeDef]
    stepDetails: NotRequired[StepDetailsEntityTypeDef]
    environmentDetails: NotRequired[EnvironmentDetailsEntityTypeDef]

class CreateJobRequestRequestTypeDef(TypedDict):
    farmId: str
    queueId: str
    priority: int
    clientToken: NotRequired[str]
    template: NotRequired[str]
    templateType: NotRequired[JobTemplateTypeType]
    parameters: NotRequired[Mapping[str, JobParameterTypeDef]]
    attachments: NotRequired[AttachmentsTypeDef]
    storageProfileId: NotRequired[str]
    targetTaskRunStatus: NotRequired[CreateJobTargetTaskRunStatusType]
    maxFailedTasksCount: NotRequired[int]
    maxRetriesPerTask: NotRequired[int]
    sourceJobId: NotRequired[str]

class SearchStepsResponseTypeDef(TypedDict):
    steps: List[StepSearchSummaryTypeDef]
    nextItemOffset: int
    totalResults: int
    ResponseMetadata: ResponseMetadataTypeDef

class ListSessionActionsResponseTypeDef(TypedDict):
    sessionActions: List[SessionActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FleetConfigurationOutputTypeDef(TypedDict):
    customerManaged: NotRequired[CustomerManagedFleetConfigurationOutputTypeDef]
    serviceManagedEc2: NotRequired[ServiceManagedEc2FleetConfigurationOutputTypeDef]

ServiceManagedEc2InstanceCapabilitiesUnionTypeDef = Union[
    ServiceManagedEc2InstanceCapabilitiesTypeDef, ServiceManagedEc2InstanceCapabilitiesOutputTypeDef
]

class AssignedSessionTypeDef(TypedDict):
    queueId: str
    jobId: str
    sessionActions: List[AssignedSessionActionTypeDef]
    logConfiguration: LogConfigurationTypeDef

class SearchJobsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueIds: Sequence[str]
    itemOffset: int
    filterExpressions: NotRequired[SearchGroupedFilterExpressionsTypeDef]
    sortExpressions: NotRequired[Sequence[SearchSortExpressionTypeDef]]
    pageSize: NotRequired[int]

class SearchStepsRequestRequestTypeDef(TypedDict):
    farmId: str
    queueIds: Sequence[str]
    itemOffset: int
    jobId: NotRequired[str]
    filterExpressions: NotRequired[SearchGroupedFilterExpressionsTypeDef]
    sortExpressions: NotRequired[Sequence[SearchSortExpressionTypeDef]]
    pageSize: NotRequired[int]

class SearchTasksRequestRequestTypeDef(TypedDict):
    farmId: str
    queueIds: Sequence[str]
    itemOffset: int
    jobId: NotRequired[str]
    filterExpressions: NotRequired[SearchGroupedFilterExpressionsTypeDef]
    sortExpressions: NotRequired[Sequence[SearchSortExpressionTypeDef]]
    pageSize: NotRequired[int]

class SearchWorkersRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetIds: Sequence[str]
    itemOffset: int
    filterExpressions: NotRequired[SearchGroupedFilterExpressionsTypeDef]
    sortExpressions: NotRequired[Sequence[SearchSortExpressionTypeDef]]
    pageSize: NotRequired[int]

class CreateBudgetRequestRequestTypeDef(TypedDict):
    farmId: str
    usageTrackingResource: UsageTrackingResourceTypeDef
    displayName: str
    approximateDollarLimit: float
    actions: Sequence[BudgetActionToAddTypeDef]
    schedule: BudgetScheduleTypeDef
    clientToken: NotRequired[str]
    description: NotRequired[str]

class UpdateBudgetRequestRequestTypeDef(TypedDict):
    farmId: str
    budgetId: str
    clientToken: NotRequired[str]
    displayName: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[BudgetStatusType]
    approximateDollarLimit: NotRequired[float]
    actionsToAdd: NotRequired[Sequence[BudgetActionToAddTypeDef]]
    actionsToRemove: NotRequired[Sequence[BudgetActionToRemoveTypeDef]]
    schedule: NotRequired[BudgetScheduleTypeDef]

class CustomerManagedFleetConfigurationTypeDef(TypedDict):
    mode: AutoScalingModeType
    workerCapabilities: CustomerManagedWorkerCapabilitiesUnionTypeDef
    storageProfileId: NotRequired[str]

class BatchGetJobEntityResponseTypeDef(TypedDict):
    entities: List[JobEntityTypeDef]
    errors: List[GetJobEntityErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class FleetSummaryTypeDef(TypedDict):
    fleetId: str
    farmId: str
    displayName: str
    status: FleetStatusType
    workerCount: int
    minWorkerCount: int
    maxWorkerCount: int
    configuration: FleetConfigurationOutputTypeDef
    createdAt: datetime
    createdBy: str
    autoScalingStatus: NotRequired[AutoScalingStatusType]
    targetWorkerCount: NotRequired[int]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class GetFleetResponseTypeDef(TypedDict):
    fleetId: str
    farmId: str
    displayName: str
    description: str
    status: FleetStatusType
    autoScalingStatus: AutoScalingStatusType
    targetWorkerCount: int
    workerCount: int
    minWorkerCount: int
    maxWorkerCount: int
    configuration: FleetConfigurationOutputTypeDef
    capabilities: FleetCapabilitiesTypeDef
    roleArn: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ServiceManagedEc2FleetConfigurationTypeDef(TypedDict):
    instanceCapabilities: ServiceManagedEc2InstanceCapabilitiesUnionTypeDef
    instanceMarketOptions: ServiceManagedEc2InstanceMarketOptionsTypeDef

class UpdateWorkerScheduleResponseTypeDef(TypedDict):
    assignedSessions: Dict[str, AssignedSessionTypeDef]
    cancelSessionActions: Dict[str, List[str]]
    desiredWorkerStatus: Literal["STOPPED"]
    updateIntervalSeconds: int
    ResponseMetadata: ResponseMetadataTypeDef

CustomerManagedFleetConfigurationUnionTypeDef = Union[
    CustomerManagedFleetConfigurationTypeDef, CustomerManagedFleetConfigurationOutputTypeDef
]

class ListFleetsResponseTypeDef(TypedDict):
    fleets: List[FleetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ServiceManagedEc2FleetConfigurationUnionTypeDef = Union[
    ServiceManagedEc2FleetConfigurationTypeDef, ServiceManagedEc2FleetConfigurationOutputTypeDef
]

class FleetConfigurationTypeDef(TypedDict):
    customerManaged: NotRequired[CustomerManagedFleetConfigurationUnionTypeDef]
    serviceManagedEc2: NotRequired[ServiceManagedEc2FleetConfigurationUnionTypeDef]

class CreateFleetRequestRequestTypeDef(TypedDict):
    farmId: str
    displayName: str
    roleArn: str
    maxWorkerCount: int
    configuration: FleetConfigurationTypeDef
    clientToken: NotRequired[str]
    description: NotRequired[str]
    minWorkerCount: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]

class UpdateFleetRequestRequestTypeDef(TypedDict):
    farmId: str
    fleetId: str
    clientToken: NotRequired[str]
    displayName: NotRequired[str]
    description: NotRequired[str]
    roleArn: NotRequired[str]
    minWorkerCount: NotRequired[int]
    maxWorkerCount: NotRequired[int]
    configuration: NotRequired[FleetConfigurationTypeDef]
