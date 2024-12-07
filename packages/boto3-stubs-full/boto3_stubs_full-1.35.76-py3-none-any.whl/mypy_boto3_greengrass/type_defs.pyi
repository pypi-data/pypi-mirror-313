"""
Type annotations for greengrass service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/type_defs/)

Usage::

    ```python
    from mypy_boto3_greengrass.type_defs import AssociateRoleToGroupRequestRequestTypeDef

    data: AssociateRoleToGroupRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    BulkDeploymentStatusType,
    ConfigurationSyncStatusType,
    DeploymentTypeType,
    EncodingTypeType,
    FunctionIsolationModeType,
    LoggerComponentType,
    LoggerLevelType,
    LoggerTypeType,
    PermissionType,
    SoftwareToUpdateType,
    TelemetryType,
    UpdateAgentLogLevelType,
    UpdateTargetsArchitectureType,
    UpdateTargetsOperatingSystemType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AssociateRoleToGroupRequestRequestTypeDef",
    "AssociateRoleToGroupResponseTypeDef",
    "AssociateServiceRoleToAccountRequestRequestTypeDef",
    "AssociateServiceRoleToAccountResponseTypeDef",
    "BulkDeploymentMetricsTypeDef",
    "BulkDeploymentResultTypeDef",
    "BulkDeploymentTypeDef",
    "ConnectivityInfoTypeDef",
    "ConnectorDefinitionVersionOutputTypeDef",
    "ConnectorDefinitionVersionTypeDef",
    "ConnectorOutputTypeDef",
    "ConnectorTypeDef",
    "ConnectorUnionTypeDef",
    "CoreDefinitionVersionOutputTypeDef",
    "CoreDefinitionVersionTypeDef",
    "CoreTypeDef",
    "CreateConnectorDefinitionRequestRequestTypeDef",
    "CreateConnectorDefinitionResponseTypeDef",
    "CreateConnectorDefinitionVersionRequestRequestTypeDef",
    "CreateConnectorDefinitionVersionResponseTypeDef",
    "CreateCoreDefinitionRequestRequestTypeDef",
    "CreateCoreDefinitionResponseTypeDef",
    "CreateCoreDefinitionVersionRequestRequestTypeDef",
    "CreateCoreDefinitionVersionResponseTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "CreateDeploymentResponseTypeDef",
    "CreateDeviceDefinitionRequestRequestTypeDef",
    "CreateDeviceDefinitionResponseTypeDef",
    "CreateDeviceDefinitionVersionRequestRequestTypeDef",
    "CreateDeviceDefinitionVersionResponseTypeDef",
    "CreateFunctionDefinitionRequestRequestTypeDef",
    "CreateFunctionDefinitionResponseTypeDef",
    "CreateFunctionDefinitionVersionRequestRequestTypeDef",
    "CreateFunctionDefinitionVersionResponseTypeDef",
    "CreateGroupCertificateAuthorityRequestRequestTypeDef",
    "CreateGroupCertificateAuthorityResponseTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateGroupVersionRequestRequestTypeDef",
    "CreateGroupVersionResponseTypeDef",
    "CreateLoggerDefinitionRequestRequestTypeDef",
    "CreateLoggerDefinitionResponseTypeDef",
    "CreateLoggerDefinitionVersionRequestRequestTypeDef",
    "CreateLoggerDefinitionVersionResponseTypeDef",
    "CreateResourceDefinitionRequestRequestTypeDef",
    "CreateResourceDefinitionResponseTypeDef",
    "CreateResourceDefinitionVersionRequestRequestTypeDef",
    "CreateResourceDefinitionVersionResponseTypeDef",
    "CreateSoftwareUpdateJobRequestRequestTypeDef",
    "CreateSoftwareUpdateJobResponseTypeDef",
    "CreateSubscriptionDefinitionRequestRequestTypeDef",
    "CreateSubscriptionDefinitionResponseTypeDef",
    "CreateSubscriptionDefinitionVersionRequestRequestTypeDef",
    "CreateSubscriptionDefinitionVersionResponseTypeDef",
    "DefinitionInformationTypeDef",
    "DeleteConnectorDefinitionRequestRequestTypeDef",
    "DeleteCoreDefinitionRequestRequestTypeDef",
    "DeleteDeviceDefinitionRequestRequestTypeDef",
    "DeleteFunctionDefinitionRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteLoggerDefinitionRequestRequestTypeDef",
    "DeleteResourceDefinitionRequestRequestTypeDef",
    "DeleteSubscriptionDefinitionRequestRequestTypeDef",
    "DeploymentTypeDef",
    "DeviceDefinitionVersionOutputTypeDef",
    "DeviceDefinitionVersionTypeDef",
    "DeviceTypeDef",
    "DisassociateRoleFromGroupRequestRequestTypeDef",
    "DisassociateRoleFromGroupResponseTypeDef",
    "DisassociateServiceRoleFromAccountResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ErrorDetailTypeDef",
    "FunctionConfigurationEnvironmentOutputTypeDef",
    "FunctionConfigurationEnvironmentTypeDef",
    "FunctionConfigurationEnvironmentUnionTypeDef",
    "FunctionConfigurationOutputTypeDef",
    "FunctionConfigurationTypeDef",
    "FunctionConfigurationUnionTypeDef",
    "FunctionDefaultConfigTypeDef",
    "FunctionDefaultExecutionConfigTypeDef",
    "FunctionDefinitionVersionOutputTypeDef",
    "FunctionDefinitionVersionTypeDef",
    "FunctionExecutionConfigTypeDef",
    "FunctionOutputTypeDef",
    "FunctionRunAsConfigTypeDef",
    "FunctionTypeDef",
    "FunctionUnionTypeDef",
    "GetAssociatedRoleRequestRequestTypeDef",
    "GetAssociatedRoleResponseTypeDef",
    "GetBulkDeploymentStatusRequestRequestTypeDef",
    "GetBulkDeploymentStatusResponseTypeDef",
    "GetConnectivityInfoRequestRequestTypeDef",
    "GetConnectivityInfoResponseTypeDef",
    "GetConnectorDefinitionRequestRequestTypeDef",
    "GetConnectorDefinitionResponseTypeDef",
    "GetConnectorDefinitionVersionRequestRequestTypeDef",
    "GetConnectorDefinitionVersionResponseTypeDef",
    "GetCoreDefinitionRequestRequestTypeDef",
    "GetCoreDefinitionResponseTypeDef",
    "GetCoreDefinitionVersionRequestRequestTypeDef",
    "GetCoreDefinitionVersionResponseTypeDef",
    "GetDeploymentStatusRequestRequestTypeDef",
    "GetDeploymentStatusResponseTypeDef",
    "GetDeviceDefinitionRequestRequestTypeDef",
    "GetDeviceDefinitionResponseTypeDef",
    "GetDeviceDefinitionVersionRequestRequestTypeDef",
    "GetDeviceDefinitionVersionResponseTypeDef",
    "GetFunctionDefinitionRequestRequestTypeDef",
    "GetFunctionDefinitionResponseTypeDef",
    "GetFunctionDefinitionVersionRequestRequestTypeDef",
    "GetFunctionDefinitionVersionResponseTypeDef",
    "GetGroupCertificateAuthorityRequestRequestTypeDef",
    "GetGroupCertificateAuthorityResponseTypeDef",
    "GetGroupCertificateConfigurationRequestRequestTypeDef",
    "GetGroupCertificateConfigurationResponseTypeDef",
    "GetGroupRequestRequestTypeDef",
    "GetGroupResponseTypeDef",
    "GetGroupVersionRequestRequestTypeDef",
    "GetGroupVersionResponseTypeDef",
    "GetLoggerDefinitionRequestRequestTypeDef",
    "GetLoggerDefinitionResponseTypeDef",
    "GetLoggerDefinitionVersionRequestRequestTypeDef",
    "GetLoggerDefinitionVersionResponseTypeDef",
    "GetResourceDefinitionRequestRequestTypeDef",
    "GetResourceDefinitionResponseTypeDef",
    "GetResourceDefinitionVersionRequestRequestTypeDef",
    "GetResourceDefinitionVersionResponseTypeDef",
    "GetServiceRoleForAccountResponseTypeDef",
    "GetSubscriptionDefinitionRequestRequestTypeDef",
    "GetSubscriptionDefinitionResponseTypeDef",
    "GetSubscriptionDefinitionVersionRequestRequestTypeDef",
    "GetSubscriptionDefinitionVersionResponseTypeDef",
    "GetThingRuntimeConfigurationRequestRequestTypeDef",
    "GetThingRuntimeConfigurationResponseTypeDef",
    "GroupCertificateAuthorityPropertiesTypeDef",
    "GroupInformationTypeDef",
    "GroupOwnerSettingTypeDef",
    "GroupVersionTypeDef",
    "ListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef",
    "ListBulkDeploymentDetailedReportsRequestRequestTypeDef",
    "ListBulkDeploymentDetailedReportsResponseTypeDef",
    "ListBulkDeploymentsRequestListBulkDeploymentsPaginateTypeDef",
    "ListBulkDeploymentsRequestRequestTypeDef",
    "ListBulkDeploymentsResponseTypeDef",
    "ListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef",
    "ListConnectorDefinitionVersionsRequestRequestTypeDef",
    "ListConnectorDefinitionVersionsResponseTypeDef",
    "ListConnectorDefinitionsRequestListConnectorDefinitionsPaginateTypeDef",
    "ListConnectorDefinitionsRequestRequestTypeDef",
    "ListConnectorDefinitionsResponseTypeDef",
    "ListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef",
    "ListCoreDefinitionVersionsRequestRequestTypeDef",
    "ListCoreDefinitionVersionsResponseTypeDef",
    "ListCoreDefinitionsRequestListCoreDefinitionsPaginateTypeDef",
    "ListCoreDefinitionsRequestRequestTypeDef",
    "ListCoreDefinitionsResponseTypeDef",
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListDeploymentsResponseTypeDef",
    "ListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef",
    "ListDeviceDefinitionVersionsRequestRequestTypeDef",
    "ListDeviceDefinitionVersionsResponseTypeDef",
    "ListDeviceDefinitionsRequestListDeviceDefinitionsPaginateTypeDef",
    "ListDeviceDefinitionsRequestRequestTypeDef",
    "ListDeviceDefinitionsResponseTypeDef",
    "ListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef",
    "ListFunctionDefinitionVersionsRequestRequestTypeDef",
    "ListFunctionDefinitionVersionsResponseTypeDef",
    "ListFunctionDefinitionsRequestListFunctionDefinitionsPaginateTypeDef",
    "ListFunctionDefinitionsRequestRequestTypeDef",
    "ListFunctionDefinitionsResponseTypeDef",
    "ListGroupCertificateAuthoritiesRequestRequestTypeDef",
    "ListGroupCertificateAuthoritiesResponseTypeDef",
    "ListGroupVersionsRequestListGroupVersionsPaginateTypeDef",
    "ListGroupVersionsRequestRequestTypeDef",
    "ListGroupVersionsResponseTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef",
    "ListLoggerDefinitionVersionsRequestRequestTypeDef",
    "ListLoggerDefinitionVersionsResponseTypeDef",
    "ListLoggerDefinitionsRequestListLoggerDefinitionsPaginateTypeDef",
    "ListLoggerDefinitionsRequestRequestTypeDef",
    "ListLoggerDefinitionsResponseTypeDef",
    "ListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef",
    "ListResourceDefinitionVersionsRequestRequestTypeDef",
    "ListResourceDefinitionVersionsResponseTypeDef",
    "ListResourceDefinitionsRequestListResourceDefinitionsPaginateTypeDef",
    "ListResourceDefinitionsRequestRequestTypeDef",
    "ListResourceDefinitionsResponseTypeDef",
    "ListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef",
    "ListSubscriptionDefinitionVersionsRequestRequestTypeDef",
    "ListSubscriptionDefinitionVersionsResponseTypeDef",
    "ListSubscriptionDefinitionsRequestListSubscriptionDefinitionsPaginateTypeDef",
    "ListSubscriptionDefinitionsRequestRequestTypeDef",
    "ListSubscriptionDefinitionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LocalDeviceResourceDataTypeDef",
    "LocalVolumeResourceDataTypeDef",
    "LoggerDefinitionVersionOutputTypeDef",
    "LoggerDefinitionVersionTypeDef",
    "LoggerTypeDef",
    "PaginatorConfigTypeDef",
    "ResetDeploymentsRequestRequestTypeDef",
    "ResetDeploymentsResponseTypeDef",
    "ResourceAccessPolicyTypeDef",
    "ResourceDataContainerOutputTypeDef",
    "ResourceDataContainerTypeDef",
    "ResourceDataContainerUnionTypeDef",
    "ResourceDefinitionVersionOutputTypeDef",
    "ResourceDefinitionVersionTypeDef",
    "ResourceDownloadOwnerSettingTypeDef",
    "ResourceOutputTypeDef",
    "ResourceTypeDef",
    "ResourceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RuntimeConfigurationTypeDef",
    "S3MachineLearningModelResourceDataTypeDef",
    "SageMakerMachineLearningModelResourceDataTypeDef",
    "SecretsManagerSecretResourceDataOutputTypeDef",
    "SecretsManagerSecretResourceDataTypeDef",
    "SecretsManagerSecretResourceDataUnionTypeDef",
    "StartBulkDeploymentRequestRequestTypeDef",
    "StartBulkDeploymentResponseTypeDef",
    "StopBulkDeploymentRequestRequestTypeDef",
    "SubscriptionDefinitionVersionOutputTypeDef",
    "SubscriptionDefinitionVersionTypeDef",
    "SubscriptionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TelemetryConfigurationTypeDef",
    "TelemetryConfigurationUpdateTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConnectivityInfoRequestRequestTypeDef",
    "UpdateConnectivityInfoResponseTypeDef",
    "UpdateConnectorDefinitionRequestRequestTypeDef",
    "UpdateCoreDefinitionRequestRequestTypeDef",
    "UpdateDeviceDefinitionRequestRequestTypeDef",
    "UpdateFunctionDefinitionRequestRequestTypeDef",
    "UpdateGroupCertificateConfigurationRequestRequestTypeDef",
    "UpdateGroupCertificateConfigurationResponseTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateLoggerDefinitionRequestRequestTypeDef",
    "UpdateResourceDefinitionRequestRequestTypeDef",
    "UpdateSubscriptionDefinitionRequestRequestTypeDef",
    "UpdateThingRuntimeConfigurationRequestRequestTypeDef",
    "VersionInformationTypeDef",
)

class AssociateRoleToGroupRequestRequestTypeDef(TypedDict):
    GroupId: str
    RoleArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociateServiceRoleToAccountRequestRequestTypeDef(TypedDict):
    RoleArn: str

class BulkDeploymentMetricsTypeDef(TypedDict):
    InvalidInputRecords: NotRequired[int]
    RecordsProcessed: NotRequired[int]
    RetryAttempts: NotRequired[int]

class ErrorDetailTypeDef(TypedDict):
    DetailedErrorCode: NotRequired[str]
    DetailedErrorMessage: NotRequired[str]

class BulkDeploymentTypeDef(TypedDict):
    BulkDeploymentArn: NotRequired[str]
    BulkDeploymentId: NotRequired[str]
    CreatedAt: NotRequired[str]

class ConnectivityInfoTypeDef(TypedDict):
    HostAddress: NotRequired[str]
    Id: NotRequired[str]
    Metadata: NotRequired[str]
    PortNumber: NotRequired[int]

class ConnectorOutputTypeDef(TypedDict):
    ConnectorArn: str
    Id: str
    Parameters: NotRequired[Dict[str, str]]

class ConnectorTypeDef(TypedDict):
    ConnectorArn: str
    Id: str
    Parameters: NotRequired[Mapping[str, str]]

class CoreTypeDef(TypedDict):
    CertificateArn: str
    Id: str
    ThingArn: str
    SyncShadow: NotRequired[bool]

class CreateDeploymentRequestRequestTypeDef(TypedDict):
    DeploymentType: DeploymentTypeType
    GroupId: str
    AmznClientToken: NotRequired[str]
    DeploymentId: NotRequired[str]
    GroupVersionId: NotRequired[str]

class DeviceTypeDef(TypedDict):
    CertificateArn: str
    Id: str
    ThingArn: str
    SyncShadow: NotRequired[bool]

class CreateGroupCertificateAuthorityRequestRequestTypeDef(TypedDict):
    GroupId: str
    AmznClientToken: NotRequired[str]

class GroupVersionTypeDef(TypedDict):
    ConnectorDefinitionVersionArn: NotRequired[str]
    CoreDefinitionVersionArn: NotRequired[str]
    DeviceDefinitionVersionArn: NotRequired[str]
    FunctionDefinitionVersionArn: NotRequired[str]
    LoggerDefinitionVersionArn: NotRequired[str]
    ResourceDefinitionVersionArn: NotRequired[str]
    SubscriptionDefinitionVersionArn: NotRequired[str]

class CreateGroupVersionRequestRequestTypeDef(TypedDict):
    GroupId: str
    AmznClientToken: NotRequired[str]
    ConnectorDefinitionVersionArn: NotRequired[str]
    CoreDefinitionVersionArn: NotRequired[str]
    DeviceDefinitionVersionArn: NotRequired[str]
    FunctionDefinitionVersionArn: NotRequired[str]
    LoggerDefinitionVersionArn: NotRequired[str]
    ResourceDefinitionVersionArn: NotRequired[str]
    SubscriptionDefinitionVersionArn: NotRequired[str]

LoggerTypeDef = TypedDict(
    "LoggerTypeDef",
    {
        "Component": LoggerComponentType,
        "Id": str,
        "Level": LoggerLevelType,
        "Type": LoggerTypeType,
        "Space": NotRequired[int],
    },
)

class CreateSoftwareUpdateJobRequestRequestTypeDef(TypedDict):
    S3UrlSignerRole: str
    SoftwareToUpdate: SoftwareToUpdateType
    UpdateTargets: Sequence[str]
    UpdateTargetsArchitecture: UpdateTargetsArchitectureType
    UpdateTargetsOperatingSystem: UpdateTargetsOperatingSystemType
    AmznClientToken: NotRequired[str]
    UpdateAgentLogLevel: NotRequired[UpdateAgentLogLevelType]

class SubscriptionTypeDef(TypedDict):
    Id: str
    Source: str
    Subject: str
    Target: str

class DefinitionInformationTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationTimestamp: NotRequired[str]
    Id: NotRequired[str]
    LastUpdatedTimestamp: NotRequired[str]
    LatestVersion: NotRequired[str]
    LatestVersionArn: NotRequired[str]
    Name: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]

class DeleteConnectorDefinitionRequestRequestTypeDef(TypedDict):
    ConnectorDefinitionId: str

class DeleteCoreDefinitionRequestRequestTypeDef(TypedDict):
    CoreDefinitionId: str

class DeleteDeviceDefinitionRequestRequestTypeDef(TypedDict):
    DeviceDefinitionId: str

class DeleteFunctionDefinitionRequestRequestTypeDef(TypedDict):
    FunctionDefinitionId: str

class DeleteGroupRequestRequestTypeDef(TypedDict):
    GroupId: str

class DeleteLoggerDefinitionRequestRequestTypeDef(TypedDict):
    LoggerDefinitionId: str

class DeleteResourceDefinitionRequestRequestTypeDef(TypedDict):
    ResourceDefinitionId: str

class DeleteSubscriptionDefinitionRequestRequestTypeDef(TypedDict):
    SubscriptionDefinitionId: str

class DeploymentTypeDef(TypedDict):
    CreatedAt: NotRequired[str]
    DeploymentArn: NotRequired[str]
    DeploymentId: NotRequired[str]
    DeploymentType: NotRequired[DeploymentTypeType]
    GroupArn: NotRequired[str]

class DisassociateRoleFromGroupRequestRequestTypeDef(TypedDict):
    GroupId: str

class ResourceAccessPolicyTypeDef(TypedDict):
    ResourceId: str
    Permission: NotRequired[PermissionType]

class FunctionRunAsConfigTypeDef(TypedDict):
    Gid: NotRequired[int]
    Uid: NotRequired[int]

class GetAssociatedRoleRequestRequestTypeDef(TypedDict):
    GroupId: str

class GetBulkDeploymentStatusRequestRequestTypeDef(TypedDict):
    BulkDeploymentId: str

class GetConnectivityInfoRequestRequestTypeDef(TypedDict):
    ThingName: str

class GetConnectorDefinitionRequestRequestTypeDef(TypedDict):
    ConnectorDefinitionId: str

class GetConnectorDefinitionVersionRequestRequestTypeDef(TypedDict):
    ConnectorDefinitionId: str
    ConnectorDefinitionVersionId: str
    NextToken: NotRequired[str]

class GetCoreDefinitionRequestRequestTypeDef(TypedDict):
    CoreDefinitionId: str

class GetCoreDefinitionVersionRequestRequestTypeDef(TypedDict):
    CoreDefinitionId: str
    CoreDefinitionVersionId: str

class GetDeploymentStatusRequestRequestTypeDef(TypedDict):
    DeploymentId: str
    GroupId: str

class GetDeviceDefinitionRequestRequestTypeDef(TypedDict):
    DeviceDefinitionId: str

class GetDeviceDefinitionVersionRequestRequestTypeDef(TypedDict):
    DeviceDefinitionId: str
    DeviceDefinitionVersionId: str
    NextToken: NotRequired[str]

class GetFunctionDefinitionRequestRequestTypeDef(TypedDict):
    FunctionDefinitionId: str

class GetFunctionDefinitionVersionRequestRequestTypeDef(TypedDict):
    FunctionDefinitionId: str
    FunctionDefinitionVersionId: str
    NextToken: NotRequired[str]

class GetGroupCertificateAuthorityRequestRequestTypeDef(TypedDict):
    CertificateAuthorityId: str
    GroupId: str

class GetGroupCertificateConfigurationRequestRequestTypeDef(TypedDict):
    GroupId: str

class GetGroupRequestRequestTypeDef(TypedDict):
    GroupId: str

class GetGroupVersionRequestRequestTypeDef(TypedDict):
    GroupId: str
    GroupVersionId: str

class GetLoggerDefinitionRequestRequestTypeDef(TypedDict):
    LoggerDefinitionId: str

class GetLoggerDefinitionVersionRequestRequestTypeDef(TypedDict):
    LoggerDefinitionId: str
    LoggerDefinitionVersionId: str
    NextToken: NotRequired[str]

class GetResourceDefinitionRequestRequestTypeDef(TypedDict):
    ResourceDefinitionId: str

class GetResourceDefinitionVersionRequestRequestTypeDef(TypedDict):
    ResourceDefinitionId: str
    ResourceDefinitionVersionId: str

class GetSubscriptionDefinitionRequestRequestTypeDef(TypedDict):
    SubscriptionDefinitionId: str

class GetSubscriptionDefinitionVersionRequestRequestTypeDef(TypedDict):
    SubscriptionDefinitionId: str
    SubscriptionDefinitionVersionId: str
    NextToken: NotRequired[str]

class GetThingRuntimeConfigurationRequestRequestTypeDef(TypedDict):
    ThingName: str

class GroupCertificateAuthorityPropertiesTypeDef(TypedDict):
    GroupCertificateAuthorityArn: NotRequired[str]
    GroupCertificateAuthorityId: NotRequired[str]

class GroupInformationTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationTimestamp: NotRequired[str]
    Id: NotRequired[str]
    LastUpdatedTimestamp: NotRequired[str]
    LatestVersion: NotRequired[str]
    LatestVersionArn: NotRequired[str]
    Name: NotRequired[str]

class GroupOwnerSettingTypeDef(TypedDict):
    AutoAddGroupOwner: NotRequired[bool]
    GroupOwner: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListBulkDeploymentDetailedReportsRequestRequestTypeDef(TypedDict):
    BulkDeploymentId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListBulkDeploymentsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListConnectorDefinitionVersionsRequestRequestTypeDef(TypedDict):
    ConnectorDefinitionId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class VersionInformationTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationTimestamp: NotRequired[str]
    Id: NotRequired[str]
    Version: NotRequired[str]

class ListConnectorDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListCoreDefinitionVersionsRequestRequestTypeDef(TypedDict):
    CoreDefinitionId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListCoreDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListDeploymentsRequestRequestTypeDef(TypedDict):
    GroupId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListDeviceDefinitionVersionsRequestRequestTypeDef(TypedDict):
    DeviceDefinitionId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListDeviceDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListFunctionDefinitionVersionsRequestRequestTypeDef(TypedDict):
    FunctionDefinitionId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListFunctionDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListGroupCertificateAuthoritiesRequestRequestTypeDef(TypedDict):
    GroupId: str

class ListGroupVersionsRequestRequestTypeDef(TypedDict):
    GroupId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListLoggerDefinitionVersionsRequestRequestTypeDef(TypedDict):
    LoggerDefinitionId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListLoggerDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListResourceDefinitionVersionsRequestRequestTypeDef(TypedDict):
    ResourceDefinitionId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListResourceDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListSubscriptionDefinitionVersionsRequestRequestTypeDef(TypedDict):
    SubscriptionDefinitionId: str
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListSubscriptionDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ResetDeploymentsRequestRequestTypeDef(TypedDict):
    GroupId: str
    AmznClientToken: NotRequired[str]
    Force: NotRequired[bool]

class SecretsManagerSecretResourceDataOutputTypeDef(TypedDict):
    ARN: NotRequired[str]
    AdditionalStagingLabelsToDownload: NotRequired[List[str]]

class ResourceDownloadOwnerSettingTypeDef(TypedDict):
    GroupOwner: str
    GroupPermission: PermissionType

class TelemetryConfigurationTypeDef(TypedDict):
    Telemetry: TelemetryType
    ConfigurationSyncStatus: NotRequired[ConfigurationSyncStatusType]

class SecretsManagerSecretResourceDataTypeDef(TypedDict):
    ARN: NotRequired[str]
    AdditionalStagingLabelsToDownload: NotRequired[Sequence[str]]

class StartBulkDeploymentRequestRequestTypeDef(TypedDict):
    ExecutionRoleArn: str
    InputFileUri: str
    AmznClientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class StopBulkDeploymentRequestRequestTypeDef(TypedDict):
    BulkDeploymentId: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    tags: NotRequired[Mapping[str, str]]

class TelemetryConfigurationUpdateTypeDef(TypedDict):
    Telemetry: TelemetryType

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateConnectorDefinitionRequestRequestTypeDef(TypedDict):
    ConnectorDefinitionId: str
    Name: NotRequired[str]

class UpdateCoreDefinitionRequestRequestTypeDef(TypedDict):
    CoreDefinitionId: str
    Name: NotRequired[str]

class UpdateDeviceDefinitionRequestRequestTypeDef(TypedDict):
    DeviceDefinitionId: str
    Name: NotRequired[str]

class UpdateFunctionDefinitionRequestRequestTypeDef(TypedDict):
    FunctionDefinitionId: str
    Name: NotRequired[str]

class UpdateGroupCertificateConfigurationRequestRequestTypeDef(TypedDict):
    GroupId: str
    CertificateExpiryInMilliseconds: NotRequired[str]

class UpdateGroupRequestRequestTypeDef(TypedDict):
    GroupId: str
    Name: NotRequired[str]

class UpdateLoggerDefinitionRequestRequestTypeDef(TypedDict):
    LoggerDefinitionId: str
    Name: NotRequired[str]

class UpdateResourceDefinitionRequestRequestTypeDef(TypedDict):
    ResourceDefinitionId: str
    Name: NotRequired[str]

class UpdateSubscriptionDefinitionRequestRequestTypeDef(TypedDict):
    SubscriptionDefinitionId: str
    Name: NotRequired[str]

class AssociateRoleToGroupResponseTypeDef(TypedDict):
    AssociatedAt: str
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateServiceRoleToAccountResponseTypeDef(TypedDict):
    AssociatedAt: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConnectorDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConnectorDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCoreDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCoreDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDeploymentResponseTypeDef(TypedDict):
    DeploymentArn: str
    DeploymentId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDeviceDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDeviceDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFunctionDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFunctionDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGroupCertificateAuthorityResponseTypeDef(TypedDict):
    GroupCertificateAuthorityArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGroupResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGroupVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLoggerDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLoggerDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourceDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourceDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSoftwareUpdateJobResponseTypeDef(TypedDict):
    IotJobArn: str
    IotJobId: str
    PlatformSoftwareVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSubscriptionDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSubscriptionDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateRoleFromGroupResponseTypeDef(TypedDict):
    DisassociatedAt: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateServiceRoleFromAccountResponseTypeDef(TypedDict):
    DisassociatedAt: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAssociatedRoleResponseTypeDef(TypedDict):
    AssociatedAt: str
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetConnectorDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetCoreDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeviceDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetFunctionDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetGroupCertificateAuthorityResponseTypeDef(TypedDict):
    GroupCertificateAuthorityArn: str
    GroupCertificateAuthorityId: str
    PemEncodedCertificate: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetGroupCertificateConfigurationResponseTypeDef(TypedDict):
    CertificateAuthorityExpiryInMilliseconds: str
    CertificateExpiryInMilliseconds: str
    GroupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetGroupResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetLoggerDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceRoleForAccountResponseTypeDef(TypedDict):
    AssociatedAt: str
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSubscriptionDefinitionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Id: str
    LastUpdatedTimestamp: str
    LatestVersion: str
    LatestVersionArn: str
    Name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ResetDeploymentsResponseTypeDef(TypedDict):
    DeploymentArn: str
    DeploymentId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartBulkDeploymentResponseTypeDef(TypedDict):
    BulkDeploymentArn: str
    BulkDeploymentId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConnectivityInfoResponseTypeDef(TypedDict):
    Message: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGroupCertificateConfigurationResponseTypeDef(TypedDict):
    CertificateAuthorityExpiryInMilliseconds: str
    CertificateExpiryInMilliseconds: str
    GroupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class BulkDeploymentResultTypeDef(TypedDict):
    CreatedAt: NotRequired[str]
    DeploymentArn: NotRequired[str]
    DeploymentId: NotRequired[str]
    DeploymentStatus: NotRequired[str]
    DeploymentType: NotRequired[DeploymentTypeType]
    ErrorDetails: NotRequired[List[ErrorDetailTypeDef]]
    ErrorMessage: NotRequired[str]
    GroupArn: NotRequired[str]

class GetBulkDeploymentStatusResponseTypeDef(TypedDict):
    BulkDeploymentMetrics: BulkDeploymentMetricsTypeDef
    BulkDeploymentStatus: BulkDeploymentStatusType
    CreatedAt: str
    ErrorDetails: List[ErrorDetailTypeDef]
    ErrorMessage: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeploymentStatusResponseTypeDef(TypedDict):
    DeploymentStatus: str
    DeploymentType: DeploymentTypeType
    ErrorDetails: List[ErrorDetailTypeDef]
    ErrorMessage: str
    UpdatedAt: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListBulkDeploymentsResponseTypeDef(TypedDict):
    BulkDeployments: List[BulkDeploymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetConnectivityInfoResponseTypeDef(TypedDict):
    ConnectivityInfo: List[ConnectivityInfoTypeDef]
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConnectivityInfoRequestRequestTypeDef(TypedDict):
    ThingName: str
    ConnectivityInfo: NotRequired[Sequence[ConnectivityInfoTypeDef]]

class ConnectorDefinitionVersionOutputTypeDef(TypedDict):
    Connectors: NotRequired[List[ConnectorOutputTypeDef]]

ConnectorUnionTypeDef = Union[ConnectorTypeDef, ConnectorOutputTypeDef]

class CoreDefinitionVersionOutputTypeDef(TypedDict):
    Cores: NotRequired[List[CoreTypeDef]]

class CoreDefinitionVersionTypeDef(TypedDict):
    Cores: NotRequired[Sequence[CoreTypeDef]]

class CreateCoreDefinitionVersionRequestRequestTypeDef(TypedDict):
    CoreDefinitionId: str
    AmznClientToken: NotRequired[str]
    Cores: NotRequired[Sequence[CoreTypeDef]]

class CreateDeviceDefinitionVersionRequestRequestTypeDef(TypedDict):
    DeviceDefinitionId: str
    AmznClientToken: NotRequired[str]
    Devices: NotRequired[Sequence[DeviceTypeDef]]

class DeviceDefinitionVersionOutputTypeDef(TypedDict):
    Devices: NotRequired[List[DeviceTypeDef]]

class DeviceDefinitionVersionTypeDef(TypedDict):
    Devices: NotRequired[Sequence[DeviceTypeDef]]

class CreateGroupRequestRequestTypeDef(TypedDict):
    Name: str
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[GroupVersionTypeDef]
    tags: NotRequired[Mapping[str, str]]

class GetGroupVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: GroupVersionTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLoggerDefinitionVersionRequestRequestTypeDef(TypedDict):
    LoggerDefinitionId: str
    AmznClientToken: NotRequired[str]
    Loggers: NotRequired[Sequence[LoggerTypeDef]]

class LoggerDefinitionVersionOutputTypeDef(TypedDict):
    Loggers: NotRequired[List[LoggerTypeDef]]

class LoggerDefinitionVersionTypeDef(TypedDict):
    Loggers: NotRequired[Sequence[LoggerTypeDef]]

class CreateSubscriptionDefinitionVersionRequestRequestTypeDef(TypedDict):
    SubscriptionDefinitionId: str
    AmznClientToken: NotRequired[str]
    Subscriptions: NotRequired[Sequence[SubscriptionTypeDef]]

class SubscriptionDefinitionVersionOutputTypeDef(TypedDict):
    Subscriptions: NotRequired[List[SubscriptionTypeDef]]

class SubscriptionDefinitionVersionTypeDef(TypedDict):
    Subscriptions: NotRequired[Sequence[SubscriptionTypeDef]]

class ListConnectorDefinitionsResponseTypeDef(TypedDict):
    Definitions: List[DefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCoreDefinitionsResponseTypeDef(TypedDict):
    Definitions: List[DefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListDeviceDefinitionsResponseTypeDef(TypedDict):
    Definitions: List[DefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListFunctionDefinitionsResponseTypeDef(TypedDict):
    Definitions: List[DefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListLoggerDefinitionsResponseTypeDef(TypedDict):
    Definitions: List[DefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListResourceDefinitionsResponseTypeDef(TypedDict):
    Definitions: List[DefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSubscriptionDefinitionsResponseTypeDef(TypedDict):
    Definitions: List[DefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListDeploymentsResponseTypeDef(TypedDict):
    Deployments: List[DeploymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class FunctionDefaultExecutionConfigTypeDef(TypedDict):
    IsolationMode: NotRequired[FunctionIsolationModeType]
    RunAs: NotRequired[FunctionRunAsConfigTypeDef]

class FunctionExecutionConfigTypeDef(TypedDict):
    IsolationMode: NotRequired[FunctionIsolationModeType]
    RunAs: NotRequired[FunctionRunAsConfigTypeDef]

class ListGroupCertificateAuthoritiesResponseTypeDef(TypedDict):
    GroupCertificateAuthorities: List[GroupCertificateAuthorityPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListGroupsResponseTypeDef(TypedDict):
    Groups: List[GroupInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class LocalDeviceResourceDataTypeDef(TypedDict):
    GroupOwnerSetting: NotRequired[GroupOwnerSettingTypeDef]
    SourcePath: NotRequired[str]

class LocalVolumeResourceDataTypeDef(TypedDict):
    DestinationPath: NotRequired[str]
    GroupOwnerSetting: NotRequired[GroupOwnerSettingTypeDef]
    SourcePath: NotRequired[str]

class ListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef(
    TypedDict
):
    BulkDeploymentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBulkDeploymentsRequestListBulkDeploymentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef(
    TypedDict
):
    ConnectorDefinitionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConnectorDefinitionsRequestListConnectorDefinitionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef(TypedDict):
    CoreDefinitionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCoreDefinitionsRequestListCoreDefinitionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeploymentsRequestListDeploymentsPaginateTypeDef(TypedDict):
    GroupId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef(TypedDict):
    DeviceDefinitionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeviceDefinitionsRequestListDeviceDefinitionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef(TypedDict):
    FunctionDefinitionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFunctionDefinitionsRequestListFunctionDefinitionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGroupVersionsRequestListGroupVersionsPaginateTypeDef(TypedDict):
    GroupId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGroupsRequestListGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef(TypedDict):
    LoggerDefinitionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLoggerDefinitionsRequestListLoggerDefinitionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef(TypedDict):
    ResourceDefinitionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceDefinitionsRequestListResourceDefinitionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef(
    TypedDict
):
    SubscriptionDefinitionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionDefinitionsRequestListSubscriptionDefinitionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConnectorDefinitionVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCoreDefinitionVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListDeviceDefinitionVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListFunctionDefinitionVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListGroupVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListLoggerDefinitionVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListResourceDefinitionVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSubscriptionDefinitionVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class S3MachineLearningModelResourceDataTypeDef(TypedDict):
    DestinationPath: NotRequired[str]
    OwnerSetting: NotRequired[ResourceDownloadOwnerSettingTypeDef]
    S3Uri: NotRequired[str]

class SageMakerMachineLearningModelResourceDataTypeDef(TypedDict):
    DestinationPath: NotRequired[str]
    OwnerSetting: NotRequired[ResourceDownloadOwnerSettingTypeDef]
    SageMakerJobArn: NotRequired[str]

class RuntimeConfigurationTypeDef(TypedDict):
    TelemetryConfiguration: NotRequired[TelemetryConfigurationTypeDef]

SecretsManagerSecretResourceDataUnionTypeDef = Union[
    SecretsManagerSecretResourceDataTypeDef, SecretsManagerSecretResourceDataOutputTypeDef
]

class UpdateThingRuntimeConfigurationRequestRequestTypeDef(TypedDict):
    ThingName: str
    TelemetryConfiguration: NotRequired[TelemetryConfigurationUpdateTypeDef]

class ListBulkDeploymentDetailedReportsResponseTypeDef(TypedDict):
    Deployments: List[BulkDeploymentResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetConnectorDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: ConnectorDefinitionVersionOutputTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ConnectorDefinitionVersionTypeDef(TypedDict):
    Connectors: NotRequired[Sequence[ConnectorUnionTypeDef]]

class CreateConnectorDefinitionVersionRequestRequestTypeDef(TypedDict):
    ConnectorDefinitionId: str
    AmznClientToken: NotRequired[str]
    Connectors: NotRequired[Sequence[ConnectorUnionTypeDef]]

class GetCoreDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: CoreDefinitionVersionOutputTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateCoreDefinitionRequestRequestTypeDef(TypedDict):
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[CoreDefinitionVersionTypeDef]
    Name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class GetDeviceDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: DeviceDefinitionVersionOutputTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateDeviceDefinitionRequestRequestTypeDef(TypedDict):
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[DeviceDefinitionVersionTypeDef]
    Name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class GetLoggerDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: LoggerDefinitionVersionOutputTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLoggerDefinitionRequestRequestTypeDef(TypedDict):
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[LoggerDefinitionVersionTypeDef]
    Name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class GetSubscriptionDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: SubscriptionDefinitionVersionOutputTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateSubscriptionDefinitionRequestRequestTypeDef(TypedDict):
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[SubscriptionDefinitionVersionTypeDef]
    Name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class FunctionDefaultConfigTypeDef(TypedDict):
    Execution: NotRequired[FunctionDefaultExecutionConfigTypeDef]

class FunctionConfigurationEnvironmentOutputTypeDef(TypedDict):
    AccessSysfs: NotRequired[bool]
    Execution: NotRequired[FunctionExecutionConfigTypeDef]
    ResourceAccessPolicies: NotRequired[List[ResourceAccessPolicyTypeDef]]
    Variables: NotRequired[Dict[str, str]]

class FunctionConfigurationEnvironmentTypeDef(TypedDict):
    AccessSysfs: NotRequired[bool]
    Execution: NotRequired[FunctionExecutionConfigTypeDef]
    ResourceAccessPolicies: NotRequired[Sequence[ResourceAccessPolicyTypeDef]]
    Variables: NotRequired[Mapping[str, str]]

class ResourceDataContainerOutputTypeDef(TypedDict):
    LocalDeviceResourceData: NotRequired[LocalDeviceResourceDataTypeDef]
    LocalVolumeResourceData: NotRequired[LocalVolumeResourceDataTypeDef]
    S3MachineLearningModelResourceData: NotRequired[S3MachineLearningModelResourceDataTypeDef]
    SageMakerMachineLearningModelResourceData: NotRequired[
        SageMakerMachineLearningModelResourceDataTypeDef
    ]
    SecretsManagerSecretResourceData: NotRequired[SecretsManagerSecretResourceDataOutputTypeDef]

class GetThingRuntimeConfigurationResponseTypeDef(TypedDict):
    RuntimeConfiguration: RuntimeConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ResourceDataContainerTypeDef(TypedDict):
    LocalDeviceResourceData: NotRequired[LocalDeviceResourceDataTypeDef]
    LocalVolumeResourceData: NotRequired[LocalVolumeResourceDataTypeDef]
    S3MachineLearningModelResourceData: NotRequired[S3MachineLearningModelResourceDataTypeDef]
    SageMakerMachineLearningModelResourceData: NotRequired[
        SageMakerMachineLearningModelResourceDataTypeDef
    ]
    SecretsManagerSecretResourceData: NotRequired[SecretsManagerSecretResourceDataUnionTypeDef]

class CreateConnectorDefinitionRequestRequestTypeDef(TypedDict):
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[ConnectorDefinitionVersionTypeDef]
    Name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class FunctionConfigurationOutputTypeDef(TypedDict):
    EncodingType: NotRequired[EncodingTypeType]
    Environment: NotRequired[FunctionConfigurationEnvironmentOutputTypeDef]
    ExecArgs: NotRequired[str]
    Executable: NotRequired[str]
    MemorySize: NotRequired[int]
    Pinned: NotRequired[bool]
    Timeout: NotRequired[int]
    FunctionRuntimeOverride: NotRequired[str]

FunctionConfigurationEnvironmentUnionTypeDef = Union[
    FunctionConfigurationEnvironmentTypeDef, FunctionConfigurationEnvironmentOutputTypeDef
]

class ResourceOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ResourceDataContainer: ResourceDataContainerOutputTypeDef

ResourceDataContainerUnionTypeDef = Union[
    ResourceDataContainerTypeDef, ResourceDataContainerOutputTypeDef
]

class FunctionOutputTypeDef(TypedDict):
    Id: str
    FunctionArn: NotRequired[str]
    FunctionConfiguration: NotRequired[FunctionConfigurationOutputTypeDef]

class FunctionConfigurationTypeDef(TypedDict):
    EncodingType: NotRequired[EncodingTypeType]
    Environment: NotRequired[FunctionConfigurationEnvironmentUnionTypeDef]
    ExecArgs: NotRequired[str]
    Executable: NotRequired[str]
    MemorySize: NotRequired[int]
    Pinned: NotRequired[bool]
    Timeout: NotRequired[int]
    FunctionRuntimeOverride: NotRequired[str]

class ResourceDefinitionVersionOutputTypeDef(TypedDict):
    Resources: NotRequired[List[ResourceOutputTypeDef]]

class ResourceTypeDef(TypedDict):
    Id: str
    Name: str
    ResourceDataContainer: ResourceDataContainerUnionTypeDef

class FunctionDefinitionVersionOutputTypeDef(TypedDict):
    DefaultConfig: NotRequired[FunctionDefaultConfigTypeDef]
    Functions: NotRequired[List[FunctionOutputTypeDef]]

FunctionConfigurationUnionTypeDef = Union[
    FunctionConfigurationTypeDef, FunctionConfigurationOutputTypeDef
]

class GetResourceDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: ResourceDefinitionVersionOutputTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef

ResourceUnionTypeDef = Union[ResourceTypeDef, ResourceOutputTypeDef]

class GetFunctionDefinitionVersionResponseTypeDef(TypedDict):
    Arn: str
    CreationTimestamp: str
    Definition: FunctionDefinitionVersionOutputTypeDef
    Id: str
    Version: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class FunctionTypeDef(TypedDict):
    Id: str
    FunctionArn: NotRequired[str]
    FunctionConfiguration: NotRequired[FunctionConfigurationUnionTypeDef]

class CreateResourceDefinitionVersionRequestRequestTypeDef(TypedDict):
    ResourceDefinitionId: str
    AmznClientToken: NotRequired[str]
    Resources: NotRequired[Sequence[ResourceUnionTypeDef]]

class ResourceDefinitionVersionTypeDef(TypedDict):
    Resources: NotRequired[Sequence[ResourceUnionTypeDef]]

FunctionUnionTypeDef = Union[FunctionTypeDef, FunctionOutputTypeDef]

class CreateResourceDefinitionRequestRequestTypeDef(TypedDict):
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[ResourceDefinitionVersionTypeDef]
    Name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateFunctionDefinitionVersionRequestRequestTypeDef(TypedDict):
    FunctionDefinitionId: str
    AmznClientToken: NotRequired[str]
    DefaultConfig: NotRequired[FunctionDefaultConfigTypeDef]
    Functions: NotRequired[Sequence[FunctionUnionTypeDef]]

class FunctionDefinitionVersionTypeDef(TypedDict):
    DefaultConfig: NotRequired[FunctionDefaultConfigTypeDef]
    Functions: NotRequired[Sequence[FunctionUnionTypeDef]]

class CreateFunctionDefinitionRequestRequestTypeDef(TypedDict):
    AmznClientToken: NotRequired[str]
    InitialVersion: NotRequired[FunctionDefinitionVersionTypeDef]
    Name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
