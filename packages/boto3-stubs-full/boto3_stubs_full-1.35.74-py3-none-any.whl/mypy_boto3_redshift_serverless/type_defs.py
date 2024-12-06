"""
Type annotations for redshift-serverless service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/type_defs/)

Usage::

    ```python
    from mypy_boto3_redshift_serverless.type_defs import AssociationTypeDef

    data: AssociationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    LogExportType,
    ManagedWorkgroupStatusType,
    NamespaceStatusType,
    PerformanceTargetStatusType,
    SnapshotStatusType,
    StateType,
    UsageLimitBreachActionType,
    UsageLimitPeriodType,
    UsageLimitUsageTypeType,
    WorkgroupStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AssociationTypeDef",
    "ConfigParameterTypeDef",
    "ConvertRecoveryPointToSnapshotRequestRequestTypeDef",
    "ConvertRecoveryPointToSnapshotResponseTypeDef",
    "CreateCustomDomainAssociationRequestRequestTypeDef",
    "CreateCustomDomainAssociationResponseTypeDef",
    "CreateEndpointAccessRequestRequestTypeDef",
    "CreateEndpointAccessResponseTypeDef",
    "CreateNamespaceRequestRequestTypeDef",
    "CreateNamespaceResponseTypeDef",
    "CreateScheduledActionRequestRequestTypeDef",
    "CreateScheduledActionResponseTypeDef",
    "CreateSnapshotCopyConfigurationRequestRequestTypeDef",
    "CreateSnapshotCopyConfigurationResponseTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateSnapshotResponseTypeDef",
    "CreateSnapshotScheduleActionParametersOutputTypeDef",
    "CreateSnapshotScheduleActionParametersTypeDef",
    "CreateSnapshotScheduleActionParametersUnionTypeDef",
    "CreateUsageLimitRequestRequestTypeDef",
    "CreateUsageLimitResponseTypeDef",
    "CreateWorkgroupRequestRequestTypeDef",
    "CreateWorkgroupResponseTypeDef",
    "DeleteCustomDomainAssociationRequestRequestTypeDef",
    "DeleteEndpointAccessRequestRequestTypeDef",
    "DeleteEndpointAccessResponseTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteScheduledActionRequestRequestTypeDef",
    "DeleteScheduledActionResponseTypeDef",
    "DeleteSnapshotCopyConfigurationRequestRequestTypeDef",
    "DeleteSnapshotCopyConfigurationResponseTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteSnapshotResponseTypeDef",
    "DeleteUsageLimitRequestRequestTypeDef",
    "DeleteUsageLimitResponseTypeDef",
    "DeleteWorkgroupRequestRequestTypeDef",
    "DeleteWorkgroupResponseTypeDef",
    "EndpointAccessTypeDef",
    "EndpointTypeDef",
    "GetCredentialsRequestRequestTypeDef",
    "GetCredentialsResponseTypeDef",
    "GetCustomDomainAssociationRequestRequestTypeDef",
    "GetCustomDomainAssociationResponseTypeDef",
    "GetEndpointAccessRequestRequestTypeDef",
    "GetEndpointAccessResponseTypeDef",
    "GetNamespaceRequestRequestTypeDef",
    "GetNamespaceResponseTypeDef",
    "GetRecoveryPointRequestRequestTypeDef",
    "GetRecoveryPointResponseTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetScheduledActionRequestRequestTypeDef",
    "GetScheduledActionResponseTypeDef",
    "GetSnapshotRequestRequestTypeDef",
    "GetSnapshotResponseTypeDef",
    "GetTableRestoreStatusRequestRequestTypeDef",
    "GetTableRestoreStatusResponseTypeDef",
    "GetUsageLimitRequestRequestTypeDef",
    "GetUsageLimitResponseTypeDef",
    "GetWorkgroupRequestRequestTypeDef",
    "GetWorkgroupResponseTypeDef",
    "ListCustomDomainAssociationsRequestListCustomDomainAssociationsPaginateTypeDef",
    "ListCustomDomainAssociationsRequestRequestTypeDef",
    "ListCustomDomainAssociationsResponseTypeDef",
    "ListEndpointAccessRequestListEndpointAccessPaginateTypeDef",
    "ListEndpointAccessRequestRequestTypeDef",
    "ListEndpointAccessResponseTypeDef",
    "ListManagedWorkgroupsRequestListManagedWorkgroupsPaginateTypeDef",
    "ListManagedWorkgroupsRequestRequestTypeDef",
    "ListManagedWorkgroupsResponseTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListNamespacesResponseTypeDef",
    "ListRecoveryPointsRequestListRecoveryPointsPaginateTypeDef",
    "ListRecoveryPointsRequestRequestTypeDef",
    "ListRecoveryPointsResponseTypeDef",
    "ListScheduledActionsRequestListScheduledActionsPaginateTypeDef",
    "ListScheduledActionsRequestRequestTypeDef",
    "ListScheduledActionsResponseTypeDef",
    "ListSnapshotCopyConfigurationsRequestListSnapshotCopyConfigurationsPaginateTypeDef",
    "ListSnapshotCopyConfigurationsRequestRequestTypeDef",
    "ListSnapshotCopyConfigurationsResponseTypeDef",
    "ListSnapshotsRequestListSnapshotsPaginateTypeDef",
    "ListSnapshotsRequestRequestTypeDef",
    "ListSnapshotsResponseTypeDef",
    "ListTableRestoreStatusRequestListTableRestoreStatusPaginateTypeDef",
    "ListTableRestoreStatusRequestRequestTypeDef",
    "ListTableRestoreStatusResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsageLimitsRequestListUsageLimitsPaginateTypeDef",
    "ListUsageLimitsRequestRequestTypeDef",
    "ListUsageLimitsResponseTypeDef",
    "ListWorkgroupsRequestListWorkgroupsPaginateTypeDef",
    "ListWorkgroupsRequestRequestTypeDef",
    "ListWorkgroupsResponseTypeDef",
    "ManagedWorkgroupListItemTypeDef",
    "NamespaceTypeDef",
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceTargetTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "RecoveryPointTypeDef",
    "ResourcePolicyTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreFromRecoveryPointRequestRequestTypeDef",
    "RestoreFromRecoveryPointResponseTypeDef",
    "RestoreFromSnapshotRequestRequestTypeDef",
    "RestoreFromSnapshotResponseTypeDef",
    "RestoreTableFromRecoveryPointRequestRequestTypeDef",
    "RestoreTableFromRecoveryPointResponseTypeDef",
    "RestoreTableFromSnapshotRequestRequestTypeDef",
    "RestoreTableFromSnapshotResponseTypeDef",
    "ScheduleOutputTypeDef",
    "ScheduleTypeDef",
    "ScheduledActionAssociationTypeDef",
    "ScheduledActionResponseTypeDef",
    "SnapshotCopyConfigurationTypeDef",
    "SnapshotTypeDef",
    "TableRestoreStatusTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetActionOutputTypeDef",
    "TargetActionTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCustomDomainAssociationRequestRequestTypeDef",
    "UpdateCustomDomainAssociationResponseTypeDef",
    "UpdateEndpointAccessRequestRequestTypeDef",
    "UpdateEndpointAccessResponseTypeDef",
    "UpdateNamespaceRequestRequestTypeDef",
    "UpdateNamespaceResponseTypeDef",
    "UpdateScheduledActionRequestRequestTypeDef",
    "UpdateScheduledActionResponseTypeDef",
    "UpdateSnapshotCopyConfigurationRequestRequestTypeDef",
    "UpdateSnapshotCopyConfigurationResponseTypeDef",
    "UpdateSnapshotRequestRequestTypeDef",
    "UpdateSnapshotResponseTypeDef",
    "UpdateUsageLimitRequestRequestTypeDef",
    "UpdateUsageLimitResponseTypeDef",
    "UpdateWorkgroupRequestRequestTypeDef",
    "UpdateWorkgroupResponseTypeDef",
    "UsageLimitTypeDef",
    "VpcEndpointTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "WorkgroupTypeDef",
)


class AssociationTypeDef(TypedDict):
    customDomainCertificateArn: NotRequired[str]
    customDomainCertificateExpiryTime: NotRequired[datetime]
    customDomainName: NotRequired[str]
    workgroupName: NotRequired[str]


class ConfigParameterTypeDef(TypedDict):
    parameterKey: NotRequired[str]
    parameterValue: NotRequired[str]


class TagTypeDef(TypedDict):
    key: str
    value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SnapshotTypeDef(TypedDict):
    accountsWithProvisionedRestoreAccess: NotRequired[List[str]]
    accountsWithRestoreAccess: NotRequired[List[str]]
    actualIncrementalBackupSizeInMegaBytes: NotRequired[float]
    adminPasswordSecretArn: NotRequired[str]
    adminPasswordSecretKmsKeyId: NotRequired[str]
    adminUsername: NotRequired[str]
    backupProgressInMegaBytes: NotRequired[float]
    currentBackupRateInMegaBytesPerSecond: NotRequired[float]
    elapsedTimeInSeconds: NotRequired[int]
    estimatedSecondsToCompletion: NotRequired[int]
    kmsKeyId: NotRequired[str]
    namespaceArn: NotRequired[str]
    namespaceName: NotRequired[str]
    ownerAccount: NotRequired[str]
    snapshotArn: NotRequired[str]
    snapshotCreateTime: NotRequired[datetime]
    snapshotName: NotRequired[str]
    snapshotRemainingDays: NotRequired[int]
    snapshotRetentionPeriod: NotRequired[int]
    snapshotRetentionStartTime: NotRequired[datetime]
    status: NotRequired[SnapshotStatusType]
    totalBackupSizeInMegaBytes: NotRequired[float]


class CreateCustomDomainAssociationRequestRequestTypeDef(TypedDict):
    customDomainCertificateArn: str
    customDomainName: str
    workgroupName: str


class CreateEndpointAccessRequestRequestTypeDef(TypedDict):
    endpointName: str
    subnetIds: Sequence[str]
    workgroupName: str
    ownerAccount: NotRequired[str]
    vpcSecurityGroupIds: NotRequired[Sequence[str]]


class NamespaceTypeDef(TypedDict):
    adminPasswordSecretArn: NotRequired[str]
    adminPasswordSecretKmsKeyId: NotRequired[str]
    adminUsername: NotRequired[str]
    creationDate: NotRequired[datetime]
    dbName: NotRequired[str]
    defaultIamRoleArn: NotRequired[str]
    iamRoles: NotRequired[List[str]]
    kmsKeyId: NotRequired[str]
    logExports: NotRequired[List[LogExportType]]
    namespaceArn: NotRequired[str]
    namespaceId: NotRequired[str]
    namespaceName: NotRequired[str]
    status: NotRequired[NamespaceStatusType]


TimestampTypeDef = Union[datetime, str]


class CreateSnapshotCopyConfigurationRequestRequestTypeDef(TypedDict):
    destinationRegion: str
    namespaceName: str
    destinationKmsKeyId: NotRequired[str]
    snapshotRetentionPeriod: NotRequired[int]


class SnapshotCopyConfigurationTypeDef(TypedDict):
    destinationKmsKeyId: NotRequired[str]
    destinationRegion: NotRequired[str]
    namespaceName: NotRequired[str]
    snapshotCopyConfigurationArn: NotRequired[str]
    snapshotCopyConfigurationId: NotRequired[str]
    snapshotRetentionPeriod: NotRequired[int]


class CreateUsageLimitRequestRequestTypeDef(TypedDict):
    amount: int
    resourceArn: str
    usageType: UsageLimitUsageTypeType
    breachAction: NotRequired[UsageLimitBreachActionType]
    period: NotRequired[UsageLimitPeriodType]


class UsageLimitTypeDef(TypedDict):
    amount: NotRequired[int]
    breachAction: NotRequired[UsageLimitBreachActionType]
    period: NotRequired[UsageLimitPeriodType]
    resourceArn: NotRequired[str]
    usageLimitArn: NotRequired[str]
    usageLimitId: NotRequired[str]
    usageType: NotRequired[UsageLimitUsageTypeType]


class PerformanceTargetTypeDef(TypedDict):
    level: NotRequired[int]
    status: NotRequired[PerformanceTargetStatusType]


class DeleteCustomDomainAssociationRequestRequestTypeDef(TypedDict):
    customDomainName: str
    workgroupName: str


class DeleteEndpointAccessRequestRequestTypeDef(TypedDict):
    endpointName: str


class DeleteNamespaceRequestRequestTypeDef(TypedDict):
    namespaceName: str
    finalSnapshotName: NotRequired[str]
    finalSnapshotRetentionPeriod: NotRequired[int]


class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str


class DeleteScheduledActionRequestRequestTypeDef(TypedDict):
    scheduledActionName: str


class DeleteSnapshotCopyConfigurationRequestRequestTypeDef(TypedDict):
    snapshotCopyConfigurationId: str


class DeleteSnapshotRequestRequestTypeDef(TypedDict):
    snapshotName: str


class DeleteUsageLimitRequestRequestTypeDef(TypedDict):
    usageLimitId: str


class DeleteWorkgroupRequestRequestTypeDef(TypedDict):
    workgroupName: str


class VpcSecurityGroupMembershipTypeDef(TypedDict):
    status: NotRequired[str]
    vpcSecurityGroupId: NotRequired[str]


class GetCredentialsRequestRequestTypeDef(TypedDict):
    customDomainName: NotRequired[str]
    dbName: NotRequired[str]
    durationSeconds: NotRequired[int]
    workgroupName: NotRequired[str]


class GetCustomDomainAssociationRequestRequestTypeDef(TypedDict):
    customDomainName: str
    workgroupName: str


class GetEndpointAccessRequestRequestTypeDef(TypedDict):
    endpointName: str


class GetNamespaceRequestRequestTypeDef(TypedDict):
    namespaceName: str


class GetRecoveryPointRequestRequestTypeDef(TypedDict):
    recoveryPointId: str


class RecoveryPointTypeDef(TypedDict):
    namespaceArn: NotRequired[str]
    namespaceName: NotRequired[str]
    recoveryPointCreateTime: NotRequired[datetime]
    recoveryPointId: NotRequired[str]
    totalSizeInMegaBytes: NotRequired[float]
    workgroupName: NotRequired[str]


class GetResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ResourcePolicyTypeDef(TypedDict):
    policy: NotRequired[str]
    resourceArn: NotRequired[str]


class GetScheduledActionRequestRequestTypeDef(TypedDict):
    scheduledActionName: str


class GetSnapshotRequestRequestTypeDef(TypedDict):
    ownerAccount: NotRequired[str]
    snapshotArn: NotRequired[str]
    snapshotName: NotRequired[str]


class GetTableRestoreStatusRequestRequestTypeDef(TypedDict):
    tableRestoreRequestId: str


class TableRestoreStatusTypeDef(TypedDict):
    message: NotRequired[str]
    namespaceName: NotRequired[str]
    newTableName: NotRequired[str]
    progressInMegaBytes: NotRequired[int]
    recoveryPointId: NotRequired[str]
    requestTime: NotRequired[datetime]
    snapshotName: NotRequired[str]
    sourceDatabaseName: NotRequired[str]
    sourceSchemaName: NotRequired[str]
    sourceTableName: NotRequired[str]
    status: NotRequired[str]
    tableRestoreRequestId: NotRequired[str]
    targetDatabaseName: NotRequired[str]
    targetSchemaName: NotRequired[str]
    totalDataInMegaBytes: NotRequired[int]
    workgroupName: NotRequired[str]


class GetUsageLimitRequestRequestTypeDef(TypedDict):
    usageLimitId: str


class GetWorkgroupRequestRequestTypeDef(TypedDict):
    workgroupName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListCustomDomainAssociationsRequestRequestTypeDef(TypedDict):
    customDomainCertificateArn: NotRequired[str]
    customDomainName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListEndpointAccessRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    ownerAccount: NotRequired[str]
    vpcId: NotRequired[str]
    workgroupName: NotRequired[str]


class ListManagedWorkgroupsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sourceArn: NotRequired[str]


class ManagedWorkgroupListItemTypeDef(TypedDict):
    creationDate: NotRequired[datetime]
    managedWorkgroupId: NotRequired[str]
    managedWorkgroupName: NotRequired[str]
    sourceArn: NotRequired[str]
    status: NotRequired[ManagedWorkgroupStatusType]


class ListNamespacesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListScheduledActionsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    namespaceName: NotRequired[str]
    nextToken: NotRequired[str]


class ScheduledActionAssociationTypeDef(TypedDict):
    namespaceName: NotRequired[str]
    scheduledActionName: NotRequired[str]


class ListSnapshotCopyConfigurationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    namespaceName: NotRequired[str]
    nextToken: NotRequired[str]


class ListTableRestoreStatusRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    namespaceName: NotRequired[str]
    nextToken: NotRequired[str]
    workgroupName: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListUsageLimitsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    resourceArn: NotRequired[str]
    usageType: NotRequired[UsageLimitUsageTypeType]


class ListWorkgroupsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    ownerAccount: NotRequired[str]


class NetworkInterfaceTypeDef(TypedDict):
    availabilityZone: NotRequired[str]
    ipv6Address: NotRequired[str]
    networkInterfaceId: NotRequired[str]
    privateIpAddress: NotRequired[str]
    subnetId: NotRequired[str]


class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    policy: str
    resourceArn: str


class RestoreFromRecoveryPointRequestRequestTypeDef(TypedDict):
    namespaceName: str
    recoveryPointId: str
    workgroupName: str


class RestoreFromSnapshotRequestRequestTypeDef(TypedDict):
    namespaceName: str
    workgroupName: str
    adminPasswordSecretKmsKeyId: NotRequired[str]
    manageAdminPassword: NotRequired[bool]
    ownerAccount: NotRequired[str]
    snapshotArn: NotRequired[str]
    snapshotName: NotRequired[str]


class RestoreTableFromRecoveryPointRequestRequestTypeDef(TypedDict):
    namespaceName: str
    newTableName: str
    recoveryPointId: str
    sourceDatabaseName: str
    sourceTableName: str
    workgroupName: str
    activateCaseSensitiveIdentifier: NotRequired[bool]
    sourceSchemaName: NotRequired[str]
    targetDatabaseName: NotRequired[str]
    targetSchemaName: NotRequired[str]


class RestoreTableFromSnapshotRequestRequestTypeDef(TypedDict):
    namespaceName: str
    newTableName: str
    snapshotName: str
    sourceDatabaseName: str
    sourceTableName: str
    workgroupName: str
    activateCaseSensitiveIdentifier: NotRequired[bool]
    sourceSchemaName: NotRequired[str]
    targetDatabaseName: NotRequired[str]
    targetSchemaName: NotRequired[str]


class ScheduleOutputTypeDef(TypedDict):
    at: NotRequired[datetime]
    cron: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateCustomDomainAssociationRequestRequestTypeDef(TypedDict):
    customDomainCertificateArn: str
    customDomainName: str
    workgroupName: str


class UpdateEndpointAccessRequestRequestTypeDef(TypedDict):
    endpointName: str
    vpcSecurityGroupIds: NotRequired[Sequence[str]]


class UpdateNamespaceRequestRequestTypeDef(TypedDict):
    namespaceName: str
    adminPasswordSecretKmsKeyId: NotRequired[str]
    adminUserPassword: NotRequired[str]
    adminUsername: NotRequired[str]
    defaultIamRoleArn: NotRequired[str]
    iamRoles: NotRequired[Sequence[str]]
    kmsKeyId: NotRequired[str]
    logExports: NotRequired[Sequence[LogExportType]]
    manageAdminPassword: NotRequired[bool]


class UpdateSnapshotCopyConfigurationRequestRequestTypeDef(TypedDict):
    snapshotCopyConfigurationId: str
    snapshotRetentionPeriod: NotRequired[int]


class UpdateSnapshotRequestRequestTypeDef(TypedDict):
    snapshotName: str
    retentionPeriod: NotRequired[int]


class UpdateUsageLimitRequestRequestTypeDef(TypedDict):
    usageLimitId: str
    amount: NotRequired[int]
    breachAction: NotRequired[UsageLimitBreachActionType]


class ConvertRecoveryPointToSnapshotRequestRequestTypeDef(TypedDict):
    recoveryPointId: str
    snapshotName: str
    retentionPeriod: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateNamespaceRequestRequestTypeDef(TypedDict):
    namespaceName: str
    adminPasswordSecretKmsKeyId: NotRequired[str]
    adminUserPassword: NotRequired[str]
    adminUsername: NotRequired[str]
    dbName: NotRequired[str]
    defaultIamRoleArn: NotRequired[str]
    iamRoles: NotRequired[Sequence[str]]
    kmsKeyId: NotRequired[str]
    logExports: NotRequired[Sequence[LogExportType]]
    manageAdminPassword: NotRequired[bool]
    redshiftIdcApplicationArn: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateSnapshotRequestRequestTypeDef(TypedDict):
    namespaceName: str
    snapshotName: str
    retentionPeriod: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateSnapshotScheduleActionParametersOutputTypeDef(TypedDict):
    namespaceName: str
    snapshotNamePrefix: str
    retentionPeriod: NotRequired[int]
    tags: NotRequired[List[TagTypeDef]]


class CreateSnapshotScheduleActionParametersTypeDef(TypedDict):
    namespaceName: str
    snapshotNamePrefix: str
    retentionPeriod: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class CreateCustomDomainAssociationResponseTypeDef(TypedDict):
    customDomainCertificateArn: str
    customDomainCertificateExpiryTime: datetime
    customDomainName: str
    workgroupName: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCredentialsResponseTypeDef(TypedDict):
    dbPassword: str
    dbUser: str
    expiration: datetime
    nextRefreshTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetCustomDomainAssociationResponseTypeDef(TypedDict):
    customDomainCertificateArn: str
    customDomainCertificateExpiryTime: datetime
    customDomainName: str
    workgroupName: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListCustomDomainAssociationsResponseTypeDef(TypedDict):
    associations: List[AssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCustomDomainAssociationResponseTypeDef(TypedDict):
    customDomainCertificateArn: str
    customDomainCertificateExpiryTime: datetime
    customDomainName: str
    workgroupName: str
    ResponseMetadata: ResponseMetadataTypeDef


class ConvertRecoveryPointToSnapshotResponseTypeDef(TypedDict):
    snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSnapshotResponseTypeDef(TypedDict):
    snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSnapshotResponseTypeDef(TypedDict):
    snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSnapshotResponseTypeDef(TypedDict):
    snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListSnapshotsResponseTypeDef(TypedDict):
    snapshots: List[SnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateSnapshotResponseTypeDef(TypedDict):
    snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNamespaceResponseTypeDef(TypedDict):
    namespace: NamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNamespaceResponseTypeDef(TypedDict):
    namespace: NamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNamespaceResponseTypeDef(TypedDict):
    namespace: NamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListNamespacesResponseTypeDef(TypedDict):
    namespaces: List[NamespaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RestoreFromRecoveryPointResponseTypeDef(TypedDict):
    namespace: NamespaceTypeDef
    recoveryPointId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreFromSnapshotResponseTypeDef(TypedDict):
    namespace: NamespaceTypeDef
    ownerAccount: str
    snapshotName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNamespaceResponseTypeDef(TypedDict):
    namespace: NamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRecoveryPointsRequestRequestTypeDef(TypedDict):
    endTime: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    namespaceArn: NotRequired[str]
    namespaceName: NotRequired[str]
    nextToken: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]


class ListSnapshotsRequestRequestTypeDef(TypedDict):
    endTime: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    namespaceArn: NotRequired[str]
    namespaceName: NotRequired[str]
    nextToken: NotRequired[str]
    ownerAccount: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]


class ScheduleTypeDef(TypedDict):
    at: NotRequired[TimestampTypeDef]
    cron: NotRequired[str]


class CreateSnapshotCopyConfigurationResponseTypeDef(TypedDict):
    snapshotCopyConfiguration: SnapshotCopyConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSnapshotCopyConfigurationResponseTypeDef(TypedDict):
    snapshotCopyConfiguration: SnapshotCopyConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListSnapshotCopyConfigurationsResponseTypeDef(TypedDict):
    snapshotCopyConfigurations: List[SnapshotCopyConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateSnapshotCopyConfigurationResponseTypeDef(TypedDict):
    snapshotCopyConfiguration: SnapshotCopyConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUsageLimitResponseTypeDef(TypedDict):
    usageLimit: UsageLimitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUsageLimitResponseTypeDef(TypedDict):
    usageLimit: UsageLimitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetUsageLimitResponseTypeDef(TypedDict):
    usageLimit: UsageLimitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListUsageLimitsResponseTypeDef(TypedDict):
    usageLimits: List[UsageLimitTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateUsageLimitResponseTypeDef(TypedDict):
    usageLimit: UsageLimitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkgroupRequestRequestTypeDef(TypedDict):
    namespaceName: str
    workgroupName: str
    baseCapacity: NotRequired[int]
    configParameters: NotRequired[Sequence[ConfigParameterTypeDef]]
    enhancedVpcRouting: NotRequired[bool]
    ipAddressType: NotRequired[str]
    maxCapacity: NotRequired[int]
    port: NotRequired[int]
    pricePerformanceTarget: NotRequired[PerformanceTargetTypeDef]
    publiclyAccessible: NotRequired[bool]
    securityGroupIds: NotRequired[Sequence[str]]
    subnetIds: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateWorkgroupRequestRequestTypeDef(TypedDict):
    workgroupName: str
    baseCapacity: NotRequired[int]
    configParameters: NotRequired[Sequence[ConfigParameterTypeDef]]
    enhancedVpcRouting: NotRequired[bool]
    ipAddressType: NotRequired[str]
    maxCapacity: NotRequired[int]
    port: NotRequired[int]
    pricePerformanceTarget: NotRequired[PerformanceTargetTypeDef]
    publiclyAccessible: NotRequired[bool]
    securityGroupIds: NotRequired[Sequence[str]]
    subnetIds: NotRequired[Sequence[str]]


class GetRecoveryPointResponseTypeDef(TypedDict):
    recoveryPoint: RecoveryPointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRecoveryPointsResponseTypeDef(TypedDict):
    recoveryPoints: List[RecoveryPointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetResourcePolicyResponseTypeDef(TypedDict):
    resourcePolicy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourcePolicyResponseTypeDef(TypedDict):
    resourcePolicy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableRestoreStatusResponseTypeDef(TypedDict):
    tableRestoreStatus: TableRestoreStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTableRestoreStatusResponseTypeDef(TypedDict):
    tableRestoreStatuses: List[TableRestoreStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RestoreTableFromRecoveryPointResponseTypeDef(TypedDict):
    tableRestoreStatus: TableRestoreStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreTableFromSnapshotResponseTypeDef(TypedDict):
    tableRestoreStatus: TableRestoreStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCustomDomainAssociationsRequestListCustomDomainAssociationsPaginateTypeDef(TypedDict):
    customDomainCertificateArn: NotRequired[str]
    customDomainName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEndpointAccessRequestListEndpointAccessPaginateTypeDef(TypedDict):
    ownerAccount: NotRequired[str]
    vpcId: NotRequired[str]
    workgroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedWorkgroupsRequestListManagedWorkgroupsPaginateTypeDef(TypedDict):
    sourceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNamespacesRequestListNamespacesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecoveryPointsRequestListRecoveryPointsPaginateTypeDef(TypedDict):
    endTime: NotRequired[TimestampTypeDef]
    namespaceArn: NotRequired[str]
    namespaceName: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScheduledActionsRequestListScheduledActionsPaginateTypeDef(TypedDict):
    namespaceName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSnapshotCopyConfigurationsRequestListSnapshotCopyConfigurationsPaginateTypeDef(TypedDict):
    namespaceName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSnapshotsRequestListSnapshotsPaginateTypeDef(TypedDict):
    endTime: NotRequired[TimestampTypeDef]
    namespaceArn: NotRequired[str]
    namespaceName: NotRequired[str]
    ownerAccount: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTableRestoreStatusRequestListTableRestoreStatusPaginateTypeDef(TypedDict):
    namespaceName: NotRequired[str]
    workgroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsageLimitsRequestListUsageLimitsPaginateTypeDef(TypedDict):
    resourceArn: NotRequired[str]
    usageType: NotRequired[UsageLimitUsageTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkgroupsRequestListWorkgroupsPaginateTypeDef(TypedDict):
    ownerAccount: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedWorkgroupsResponseTypeDef(TypedDict):
    managedWorkgroups: List[ManagedWorkgroupListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListScheduledActionsResponseTypeDef(TypedDict):
    scheduledActions: List[ScheduledActionAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class VpcEndpointTypeDef(TypedDict):
    networkInterfaces: NotRequired[List[NetworkInterfaceTypeDef]]
    vpcEndpointId: NotRequired[str]
    vpcId: NotRequired[str]


class TargetActionOutputTypeDef(TypedDict):
    createSnapshot: NotRequired[CreateSnapshotScheduleActionParametersOutputTypeDef]


CreateSnapshotScheduleActionParametersUnionTypeDef = Union[
    CreateSnapshotScheduleActionParametersTypeDef,
    CreateSnapshotScheduleActionParametersOutputTypeDef,
]


class EndpointAccessTypeDef(TypedDict):
    address: NotRequired[str]
    endpointArn: NotRequired[str]
    endpointCreateTime: NotRequired[datetime]
    endpointName: NotRequired[str]
    endpointStatus: NotRequired[str]
    port: NotRequired[int]
    subnetIds: NotRequired[List[str]]
    vpcEndpoint: NotRequired[VpcEndpointTypeDef]
    vpcSecurityGroups: NotRequired[List[VpcSecurityGroupMembershipTypeDef]]
    workgroupName: NotRequired[str]


class EndpointTypeDef(TypedDict):
    address: NotRequired[str]
    port: NotRequired[int]
    vpcEndpoints: NotRequired[List[VpcEndpointTypeDef]]


class ScheduledActionResponseTypeDef(TypedDict):
    endTime: NotRequired[datetime]
    namespaceName: NotRequired[str]
    nextInvocations: NotRequired[List[datetime]]
    roleArn: NotRequired[str]
    schedule: NotRequired[ScheduleOutputTypeDef]
    scheduledActionDescription: NotRequired[str]
    scheduledActionName: NotRequired[str]
    scheduledActionUuid: NotRequired[str]
    startTime: NotRequired[datetime]
    state: NotRequired[StateType]
    targetAction: NotRequired[TargetActionOutputTypeDef]


class TargetActionTypeDef(TypedDict):
    createSnapshot: NotRequired[CreateSnapshotScheduleActionParametersUnionTypeDef]


class CreateEndpointAccessResponseTypeDef(TypedDict):
    endpoint: EndpointAccessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEndpointAccessResponseTypeDef(TypedDict):
    endpoint: EndpointAccessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetEndpointAccessResponseTypeDef(TypedDict):
    endpoint: EndpointAccessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEndpointAccessResponseTypeDef(TypedDict):
    endpoints: List[EndpointAccessTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateEndpointAccessResponseTypeDef(TypedDict):
    endpoint: EndpointAccessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class WorkgroupTypeDef(TypedDict):
    baseCapacity: NotRequired[int]
    configParameters: NotRequired[List[ConfigParameterTypeDef]]
    creationDate: NotRequired[datetime]
    crossAccountVpcs: NotRequired[List[str]]
    customDomainCertificateArn: NotRequired[str]
    customDomainCertificateExpiryTime: NotRequired[datetime]
    customDomainName: NotRequired[str]
    endpoint: NotRequired[EndpointTypeDef]
    enhancedVpcRouting: NotRequired[bool]
    ipAddressType: NotRequired[str]
    maxCapacity: NotRequired[int]
    namespaceName: NotRequired[str]
    patchVersion: NotRequired[str]
    port: NotRequired[int]
    pricePerformanceTarget: NotRequired[PerformanceTargetTypeDef]
    publiclyAccessible: NotRequired[bool]
    securityGroupIds: NotRequired[List[str]]
    status: NotRequired[WorkgroupStatusType]
    subnetIds: NotRequired[List[str]]
    workgroupArn: NotRequired[str]
    workgroupId: NotRequired[str]
    workgroupName: NotRequired[str]
    workgroupVersion: NotRequired[str]


class CreateScheduledActionResponseTypeDef(TypedDict):
    scheduledAction: ScheduledActionResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteScheduledActionResponseTypeDef(TypedDict):
    scheduledAction: ScheduledActionResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetScheduledActionResponseTypeDef(TypedDict):
    scheduledAction: ScheduledActionResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScheduledActionResponseTypeDef(TypedDict):
    scheduledAction: ScheduledActionResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateScheduledActionRequestRequestTypeDef(TypedDict):
    namespaceName: str
    roleArn: str
    schedule: ScheduleTypeDef
    scheduledActionName: str
    targetAction: TargetActionTypeDef
    enabled: NotRequired[bool]
    endTime: NotRequired[TimestampTypeDef]
    scheduledActionDescription: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]


class UpdateScheduledActionRequestRequestTypeDef(TypedDict):
    scheduledActionName: str
    enabled: NotRequired[bool]
    endTime: NotRequired[TimestampTypeDef]
    roleArn: NotRequired[str]
    schedule: NotRequired[ScheduleTypeDef]
    scheduledActionDescription: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    targetAction: NotRequired[TargetActionTypeDef]


class CreateWorkgroupResponseTypeDef(TypedDict):
    workgroup: WorkgroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkgroupResponseTypeDef(TypedDict):
    workgroup: WorkgroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetWorkgroupResponseTypeDef(TypedDict):
    workgroup: WorkgroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListWorkgroupsResponseTypeDef(TypedDict):
    workgroups: List[WorkgroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateWorkgroupResponseTypeDef(TypedDict):
    workgroup: WorkgroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
