"""
Type annotations for proton service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/type_defs/)

Usage::

    ```python
    from mypy_boto3_proton.type_defs import AcceptEnvironmentAccountConnectionInputRequestTypeDef

    data: AcceptEnvironmentAccountConnectionInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    BlockerStatusType,
    ComponentDeploymentUpdateTypeType,
    DeploymentStatusType,
    DeploymentTargetResourceTypeType,
    DeploymentUpdateTypeType,
    EnvironmentAccountConnectionRequesterAccountTypeType,
    EnvironmentAccountConnectionStatusType,
    ListServiceInstancesFilterByType,
    ListServiceInstancesSortByType,
    ProvisionedResourceEngineType,
    RepositoryProviderType,
    RepositorySyncStatusType,
    ResourceDeploymentStatusType,
    ResourceSyncStatusType,
    ServiceStatusType,
    SortOrderType,
    SyncTypeType,
    TemplateTypeType,
    TemplateVersionStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    "AcceptEnvironmentAccountConnectionOutputTypeDef",
    "AccountSettingsTypeDef",
    "CancelComponentDeploymentInputRequestTypeDef",
    "CancelComponentDeploymentOutputTypeDef",
    "CancelEnvironmentDeploymentInputRequestTypeDef",
    "CancelEnvironmentDeploymentOutputTypeDef",
    "CancelServiceInstanceDeploymentInputRequestTypeDef",
    "CancelServiceInstanceDeploymentOutputTypeDef",
    "CancelServicePipelineDeploymentInputRequestTypeDef",
    "CancelServicePipelineDeploymentOutputTypeDef",
    "CompatibleEnvironmentTemplateInputTypeDef",
    "CompatibleEnvironmentTemplateTypeDef",
    "ComponentStateTypeDef",
    "ComponentSummaryTypeDef",
    "ComponentTypeDef",
    "CountsSummaryTypeDef",
    "CreateComponentInputRequestTypeDef",
    "CreateComponentOutputTypeDef",
    "CreateEnvironmentAccountConnectionInputRequestTypeDef",
    "CreateEnvironmentAccountConnectionOutputTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateEnvironmentTemplateInputRequestTypeDef",
    "CreateEnvironmentTemplateOutputTypeDef",
    "CreateEnvironmentTemplateVersionInputRequestTypeDef",
    "CreateEnvironmentTemplateVersionOutputTypeDef",
    "CreateRepositoryInputRequestTypeDef",
    "CreateRepositoryOutputTypeDef",
    "CreateServiceInputRequestTypeDef",
    "CreateServiceInstanceInputRequestTypeDef",
    "CreateServiceInstanceOutputTypeDef",
    "CreateServiceOutputTypeDef",
    "CreateServiceSyncConfigInputRequestTypeDef",
    "CreateServiceSyncConfigOutputTypeDef",
    "CreateServiceTemplateInputRequestTypeDef",
    "CreateServiceTemplateOutputTypeDef",
    "CreateServiceTemplateVersionInputRequestTypeDef",
    "CreateServiceTemplateVersionOutputTypeDef",
    "CreateTemplateSyncConfigInputRequestTypeDef",
    "CreateTemplateSyncConfigOutputTypeDef",
    "DeleteComponentInputRequestTypeDef",
    "DeleteComponentOutputTypeDef",
    "DeleteDeploymentInputRequestTypeDef",
    "DeleteDeploymentOutputTypeDef",
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    "DeleteEnvironmentAccountConnectionOutputTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DeleteEnvironmentOutputTypeDef",
    "DeleteEnvironmentTemplateInputRequestTypeDef",
    "DeleteEnvironmentTemplateOutputTypeDef",
    "DeleteEnvironmentTemplateVersionInputRequestTypeDef",
    "DeleteEnvironmentTemplateVersionOutputTypeDef",
    "DeleteRepositoryInputRequestTypeDef",
    "DeleteRepositoryOutputTypeDef",
    "DeleteServiceInputRequestTypeDef",
    "DeleteServiceOutputTypeDef",
    "DeleteServiceSyncConfigInputRequestTypeDef",
    "DeleteServiceSyncConfigOutputTypeDef",
    "DeleteServiceTemplateInputRequestTypeDef",
    "DeleteServiceTemplateOutputTypeDef",
    "DeleteServiceTemplateVersionInputRequestTypeDef",
    "DeleteServiceTemplateVersionOutputTypeDef",
    "DeleteTemplateSyncConfigInputRequestTypeDef",
    "DeleteTemplateSyncConfigOutputTypeDef",
    "DeploymentStateTypeDef",
    "DeploymentSummaryTypeDef",
    "DeploymentTypeDef",
    "EnvironmentAccountConnectionSummaryTypeDef",
    "EnvironmentAccountConnectionTypeDef",
    "EnvironmentStateTypeDef",
    "EnvironmentSummaryTypeDef",
    "EnvironmentTemplateFilterTypeDef",
    "EnvironmentTemplateSummaryTypeDef",
    "EnvironmentTemplateTypeDef",
    "EnvironmentTemplateVersionSummaryTypeDef",
    "EnvironmentTemplateVersionTypeDef",
    "EnvironmentTypeDef",
    "GetAccountSettingsOutputTypeDef",
    "GetComponentInputComponentDeletedWaitTypeDef",
    "GetComponentInputComponentDeployedWaitTypeDef",
    "GetComponentInputRequestTypeDef",
    "GetComponentOutputTypeDef",
    "GetDeploymentInputRequestTypeDef",
    "GetDeploymentOutputTypeDef",
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    "GetEnvironmentAccountConnectionOutputTypeDef",
    "GetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "GetEnvironmentOutputTypeDef",
    "GetEnvironmentTemplateInputRequestTypeDef",
    "GetEnvironmentTemplateOutputTypeDef",
    "GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    "GetEnvironmentTemplateVersionInputRequestTypeDef",
    "GetEnvironmentTemplateVersionOutputTypeDef",
    "GetRepositoryInputRequestTypeDef",
    "GetRepositoryOutputTypeDef",
    "GetRepositorySyncStatusInputRequestTypeDef",
    "GetRepositorySyncStatusOutputTypeDef",
    "GetResourcesSummaryOutputTypeDef",
    "GetServiceInputRequestTypeDef",
    "GetServiceInputServiceCreatedWaitTypeDef",
    "GetServiceInputServiceDeletedWaitTypeDef",
    "GetServiceInputServicePipelineDeployedWaitTypeDef",
    "GetServiceInputServiceUpdatedWaitTypeDef",
    "GetServiceInstanceInputRequestTypeDef",
    "GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    "GetServiceInstanceOutputTypeDef",
    "GetServiceInstanceSyncStatusInputRequestTypeDef",
    "GetServiceInstanceSyncStatusOutputTypeDef",
    "GetServiceOutputTypeDef",
    "GetServiceSyncBlockerSummaryInputRequestTypeDef",
    "GetServiceSyncBlockerSummaryOutputTypeDef",
    "GetServiceSyncConfigInputRequestTypeDef",
    "GetServiceSyncConfigOutputTypeDef",
    "GetServiceTemplateInputRequestTypeDef",
    "GetServiceTemplateOutputTypeDef",
    "GetServiceTemplateVersionInputRequestTypeDef",
    "GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    "GetServiceTemplateVersionOutputTypeDef",
    "GetTemplateSyncConfigInputRequestTypeDef",
    "GetTemplateSyncConfigOutputTypeDef",
    "GetTemplateSyncStatusInputRequestTypeDef",
    "GetTemplateSyncStatusOutputTypeDef",
    "ListComponentOutputsInputListComponentOutputsPaginateTypeDef",
    "ListComponentOutputsInputRequestTypeDef",
    "ListComponentOutputsOutputTypeDef",
    "ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef",
    "ListComponentProvisionedResourcesInputRequestTypeDef",
    "ListComponentProvisionedResourcesOutputTypeDef",
    "ListComponentsInputListComponentsPaginateTypeDef",
    "ListComponentsInputRequestTypeDef",
    "ListComponentsOutputTypeDef",
    "ListDeploymentsInputListDeploymentsPaginateTypeDef",
    "ListDeploymentsInputRequestTypeDef",
    "ListDeploymentsOutputTypeDef",
    "ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    "ListEnvironmentAccountConnectionsInputRequestTypeDef",
    "ListEnvironmentAccountConnectionsOutputTypeDef",
    "ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    "ListEnvironmentOutputsInputRequestTypeDef",
    "ListEnvironmentOutputsOutputTypeDef",
    "ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    "ListEnvironmentProvisionedResourcesInputRequestTypeDef",
    "ListEnvironmentProvisionedResourcesOutputTypeDef",
    "ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    "ListEnvironmentTemplateVersionsInputRequestTypeDef",
    "ListEnvironmentTemplateVersionsOutputTypeDef",
    "ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef",
    "ListEnvironmentTemplatesInputRequestTypeDef",
    "ListEnvironmentTemplatesOutputTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    "ListRepositoriesInputRequestTypeDef",
    "ListRepositoriesOutputTypeDef",
    "ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    "ListRepositorySyncDefinitionsInputRequestTypeDef",
    "ListRepositorySyncDefinitionsOutputTypeDef",
    "ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    "ListServiceInstanceOutputsInputRequestTypeDef",
    "ListServiceInstanceOutputsOutputTypeDef",
    "ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    "ListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    "ListServiceInstanceProvisionedResourcesOutputTypeDef",
    "ListServiceInstancesFilterTypeDef",
    "ListServiceInstancesInputListServiceInstancesPaginateTypeDef",
    "ListServiceInstancesInputRequestTypeDef",
    "ListServiceInstancesOutputTypeDef",
    "ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    "ListServicePipelineOutputsInputRequestTypeDef",
    "ListServicePipelineOutputsOutputTypeDef",
    "ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    "ListServicePipelineProvisionedResourcesInputRequestTypeDef",
    "ListServicePipelineProvisionedResourcesOutputTypeDef",
    "ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    "ListServiceTemplateVersionsInputRequestTypeDef",
    "ListServiceTemplateVersionsOutputTypeDef",
    "ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef",
    "ListServiceTemplatesInputRequestTypeDef",
    "ListServiceTemplatesOutputTypeDef",
    "ListServicesInputListServicesPaginateTypeDef",
    "ListServicesInputRequestTypeDef",
    "ListServicesOutputTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "NotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    "OutputTypeDef",
    "PaginatorConfigTypeDef",
    "ProvisionedResourceTypeDef",
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    "RejectEnvironmentAccountConnectionOutputTypeDef",
    "RepositoryBranchInputTypeDef",
    "RepositoryBranchTypeDef",
    "RepositorySummaryTypeDef",
    "RepositorySyncAttemptTypeDef",
    "RepositorySyncDefinitionTypeDef",
    "RepositorySyncEventTypeDef",
    "RepositoryTypeDef",
    "ResourceCountsSummaryTypeDef",
    "ResourceSyncAttemptTypeDef",
    "ResourceSyncEventTypeDef",
    "ResponseMetadataTypeDef",
    "RevisionTypeDef",
    "S3ObjectSourceTypeDef",
    "ServiceInstanceStateTypeDef",
    "ServiceInstanceSummaryTypeDef",
    "ServiceInstanceTypeDef",
    "ServicePipelineStateTypeDef",
    "ServicePipelineTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceSyncBlockerSummaryTypeDef",
    "ServiceSyncConfigTypeDef",
    "ServiceTemplateSummaryTypeDef",
    "ServiceTemplateTypeDef",
    "ServiceTemplateVersionSummaryTypeDef",
    "ServiceTemplateVersionTypeDef",
    "ServiceTypeDef",
    "SyncBlockerContextTypeDef",
    "SyncBlockerTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "TemplateSyncConfigTypeDef",
    "TemplateVersionSourceInputTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateAccountSettingsInputRequestTypeDef",
    "UpdateAccountSettingsOutputTypeDef",
    "UpdateComponentInputRequestTypeDef",
    "UpdateComponentOutputTypeDef",
    "UpdateEnvironmentAccountConnectionInputRequestTypeDef",
    "UpdateEnvironmentAccountConnectionOutputTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "UpdateEnvironmentTemplateInputRequestTypeDef",
    "UpdateEnvironmentTemplateOutputTypeDef",
    "UpdateEnvironmentTemplateVersionInputRequestTypeDef",
    "UpdateEnvironmentTemplateVersionOutputTypeDef",
    "UpdateServiceInputRequestTypeDef",
    "UpdateServiceInstanceInputRequestTypeDef",
    "UpdateServiceInstanceOutputTypeDef",
    "UpdateServiceOutputTypeDef",
    "UpdateServicePipelineInputRequestTypeDef",
    "UpdateServicePipelineOutputTypeDef",
    "UpdateServiceSyncBlockerInputRequestTypeDef",
    "UpdateServiceSyncBlockerOutputTypeDef",
    "UpdateServiceSyncConfigInputRequestTypeDef",
    "UpdateServiceSyncConfigOutputTypeDef",
    "UpdateServiceTemplateInputRequestTypeDef",
    "UpdateServiceTemplateOutputTypeDef",
    "UpdateServiceTemplateVersionInputRequestTypeDef",
    "UpdateServiceTemplateVersionOutputTypeDef",
    "UpdateTemplateSyncConfigInputRequestTypeDef",
    "UpdateTemplateSyncConfigOutputTypeDef",
    "WaiterConfigTypeDef",
)

AcceptEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)
EnvironmentAccountConnectionTypeDef = TypedDict(
    "EnvironmentAccountConnectionTypeDef",
    {
        "arn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
        "codebuildRoleArn": NotRequired[str],
        "componentRoleArn": NotRequired[str],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class RepositoryBranchTypeDef(TypedDict):
    arn: str
    branch: str
    name: str
    provider: RepositoryProviderType

class CancelComponentDeploymentInputRequestTypeDef(TypedDict):
    componentName: str

class ComponentTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    deploymentStatus: DeploymentStatusType
    environmentName: str
    lastModifiedAt: datetime
    name: str
    deploymentStatusMessage: NotRequired[str]
    description: NotRequired[str]
    lastAttemptedDeploymentId: NotRequired[str]
    lastClientRequestToken: NotRequired[str]
    lastDeploymentAttemptedAt: NotRequired[datetime]
    lastDeploymentSucceededAt: NotRequired[datetime]
    lastSucceededDeploymentId: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]
    serviceSpec: NotRequired[str]

class CancelEnvironmentDeploymentInputRequestTypeDef(TypedDict):
    environmentName: str

class CancelServiceInstanceDeploymentInputRequestTypeDef(TypedDict):
    serviceInstanceName: str
    serviceName: str

class ServiceInstanceTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    deploymentStatus: DeploymentStatusType
    environmentName: str
    lastDeploymentAttemptedAt: datetime
    lastDeploymentSucceededAt: datetime
    name: str
    serviceName: str
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    deploymentStatusMessage: NotRequired[str]
    lastAttemptedDeploymentId: NotRequired[str]
    lastClientRequestToken: NotRequired[str]
    lastSucceededDeploymentId: NotRequired[str]
    spec: NotRequired[str]

class CancelServicePipelineDeploymentInputRequestTypeDef(TypedDict):
    serviceName: str

class ServicePipelineTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    deploymentStatus: DeploymentStatusType
    lastDeploymentAttemptedAt: datetime
    lastDeploymentSucceededAt: datetime
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    deploymentStatusMessage: NotRequired[str]
    lastAttemptedDeploymentId: NotRequired[str]
    lastSucceededDeploymentId: NotRequired[str]
    spec: NotRequired[str]

class CompatibleEnvironmentTemplateInputTypeDef(TypedDict):
    majorVersion: str
    templateName: str

class CompatibleEnvironmentTemplateTypeDef(TypedDict):
    majorVersion: str
    templateName: str

class ComponentStateTypeDef(TypedDict):
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]
    serviceSpec: NotRequired[str]
    templateFile: NotRequired[str]

class ComponentSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    deploymentStatus: DeploymentStatusType
    environmentName: str
    lastModifiedAt: datetime
    name: str
    deploymentStatusMessage: NotRequired[str]
    lastAttemptedDeploymentId: NotRequired[str]
    lastDeploymentAttemptedAt: NotRequired[datetime]
    lastDeploymentSucceededAt: NotRequired[datetime]
    lastSucceededDeploymentId: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]

class ResourceCountsSummaryTypeDef(TypedDict):
    total: int
    behindMajor: NotRequired[int]
    behindMinor: NotRequired[int]
    failed: NotRequired[int]
    upToDate: NotRequired[int]

class TagTypeDef(TypedDict):
    key: str
    value: str

class RepositoryBranchInputTypeDef(TypedDict):
    branch: str
    name: str
    provider: RepositoryProviderType

class EnvironmentTemplateTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]
    encryptionKey: NotRequired[str]
    provisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]
    recommendedVersion: NotRequired[str]

class EnvironmentTemplateVersionTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    majorVersion: str
    minorVersion: str
    status: TemplateVersionStatusType
    templateName: str
    description: NotRequired[str]
    recommendedMinorVersion: NotRequired[str]
    schema: NotRequired[str]
    statusMessage: NotRequired[str]

class RepositoryTypeDef(TypedDict):
    arn: str
    connectionArn: str
    name: str
    provider: RepositoryProviderType
    encryptionKey: NotRequired[str]

class CreateServiceSyncConfigInputRequestTypeDef(TypedDict):
    branch: str
    filePath: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    serviceName: str

class ServiceSyncConfigTypeDef(TypedDict):
    branch: str
    filePath: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    serviceName: str

class ServiceTemplateTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]
    encryptionKey: NotRequired[str]
    pipelineProvisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]
    recommendedVersion: NotRequired[str]

class CreateTemplateSyncConfigInputRequestTypeDef(TypedDict):
    branch: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    templateName: str
    templateType: TemplateTypeType
    subdirectory: NotRequired[str]

class TemplateSyncConfigTypeDef(TypedDict):
    branch: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    templateName: str
    templateType: TemplateTypeType
    subdirectory: NotRequired[str]

class DeleteComponentInputRequestTypeDef(TypedDict):
    name: str

DeleteDeploymentInputRequestTypeDef = TypedDict(
    "DeleteDeploymentInputRequestTypeDef",
    {
        "id": str,
    },
)
DeleteEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

class DeleteEnvironmentInputRequestTypeDef(TypedDict):
    name: str

class DeleteEnvironmentTemplateInputRequestTypeDef(TypedDict):
    name: str

class DeleteEnvironmentTemplateVersionInputRequestTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str

class DeleteRepositoryInputRequestTypeDef(TypedDict):
    name: str
    provider: RepositoryProviderType

class DeleteServiceInputRequestTypeDef(TypedDict):
    name: str

class DeleteServiceSyncConfigInputRequestTypeDef(TypedDict):
    serviceName: str

class DeleteServiceTemplateInputRequestTypeDef(TypedDict):
    name: str

class DeleteServiceTemplateVersionInputRequestTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str

class DeleteTemplateSyncConfigInputRequestTypeDef(TypedDict):
    templateName: str
    templateType: TemplateTypeType

class EnvironmentStateTypeDef(TypedDict):
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    spec: NotRequired[str]

class ServiceInstanceStateTypeDef(TypedDict):
    spec: str
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    lastSuccessfulComponentDeploymentIds: NotRequired[List[str]]
    lastSuccessfulEnvironmentDeploymentId: NotRequired[str]
    lastSuccessfulServicePipelineDeploymentId: NotRequired[str]

class ServicePipelineStateTypeDef(TypedDict):
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    spec: NotRequired[str]

DeploymentSummaryTypeDef = TypedDict(
    "DeploymentSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "targetArn": str,
        "targetResourceCreatedAt": datetime,
        "targetResourceType": DeploymentTargetResourceTypeType,
        "completedAt": NotRequired[datetime],
        "componentName": NotRequired[str],
        "lastAttemptedDeploymentId": NotRequired[str],
        "lastSucceededDeploymentId": NotRequired[str],
        "serviceInstanceName": NotRequired[str],
        "serviceName": NotRequired[str],
    },
)
EnvironmentAccountConnectionSummaryTypeDef = TypedDict(
    "EnvironmentAccountConnectionSummaryTypeDef",
    {
        "arn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
        "componentRoleArn": NotRequired[str],
    },
)

class EnvironmentSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    deploymentStatus: DeploymentStatusType
    lastDeploymentAttemptedAt: datetime
    lastDeploymentSucceededAt: datetime
    name: str
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    componentRoleArn: NotRequired[str]
    deploymentStatusMessage: NotRequired[str]
    description: NotRequired[str]
    environmentAccountConnectionId: NotRequired[str]
    environmentAccountId: NotRequired[str]
    lastAttemptedDeploymentId: NotRequired[str]
    lastSucceededDeploymentId: NotRequired[str]
    protonServiceRoleArn: NotRequired[str]
    provisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]

class EnvironmentTemplateFilterTypeDef(TypedDict):
    majorVersion: str
    templateName: str

class EnvironmentTemplateSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]
    provisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]
    recommendedVersion: NotRequired[str]

class EnvironmentTemplateVersionSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    majorVersion: str
    minorVersion: str
    status: TemplateVersionStatusType
    templateName: str
    description: NotRequired[str]
    recommendedMinorVersion: NotRequired[str]
    statusMessage: NotRequired[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetComponentInputRequestTypeDef(TypedDict):
    name: str

GetDeploymentInputRequestTypeDef = TypedDict(
    "GetDeploymentInputRequestTypeDef",
    {
        "id": str,
        "componentName": NotRequired[str],
        "environmentName": NotRequired[str],
        "serviceInstanceName": NotRequired[str],
        "serviceName": NotRequired[str],
    },
)
GetEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

class GetEnvironmentInputRequestTypeDef(TypedDict):
    name: str

class GetEnvironmentTemplateInputRequestTypeDef(TypedDict):
    name: str

class GetEnvironmentTemplateVersionInputRequestTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str

class GetRepositoryInputRequestTypeDef(TypedDict):
    name: str
    provider: RepositoryProviderType

class GetRepositorySyncStatusInputRequestTypeDef(TypedDict):
    branch: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    syncType: SyncTypeType

class GetServiceInputRequestTypeDef(TypedDict):
    name: str

class GetServiceInstanceInputRequestTypeDef(TypedDict):
    name: str
    serviceName: str

class GetServiceInstanceSyncStatusInputRequestTypeDef(TypedDict):
    serviceInstanceName: str
    serviceName: str

class RevisionTypeDef(TypedDict):
    branch: str
    directory: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    sha: str

class GetServiceSyncBlockerSummaryInputRequestTypeDef(TypedDict):
    serviceName: str
    serviceInstanceName: NotRequired[str]

class GetServiceSyncConfigInputRequestTypeDef(TypedDict):
    serviceName: str

class GetServiceTemplateInputRequestTypeDef(TypedDict):
    name: str

class GetServiceTemplateVersionInputRequestTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str

class GetTemplateSyncConfigInputRequestTypeDef(TypedDict):
    templateName: str
    templateType: TemplateTypeType

class GetTemplateSyncStatusInputRequestTypeDef(TypedDict):
    templateName: str
    templateType: TemplateTypeType
    templateVersion: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListComponentOutputsInputRequestTypeDef(TypedDict):
    componentName: str
    deploymentId: NotRequired[str]
    nextToken: NotRequired[str]

class OutputTypeDef(TypedDict):
    key: NotRequired[str]
    valueString: NotRequired[str]

class ListComponentProvisionedResourcesInputRequestTypeDef(TypedDict):
    componentName: str
    nextToken: NotRequired[str]

class ProvisionedResourceTypeDef(TypedDict):
    identifier: NotRequired[str]
    name: NotRequired[str]
    provisioningEngine: NotRequired[ProvisionedResourceEngineType]

class ListComponentsInputRequestTypeDef(TypedDict):
    environmentName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]

class ListDeploymentsInputRequestTypeDef(TypedDict):
    componentName: NotRequired[str]
    environmentName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]

class ListEnvironmentAccountConnectionsInputRequestTypeDef(TypedDict):
    requestedBy: EnvironmentAccountConnectionRequesterAccountTypeType
    environmentName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    statuses: NotRequired[Sequence[EnvironmentAccountConnectionStatusType]]

class ListEnvironmentOutputsInputRequestTypeDef(TypedDict):
    environmentName: str
    deploymentId: NotRequired[str]
    nextToken: NotRequired[str]

class ListEnvironmentProvisionedResourcesInputRequestTypeDef(TypedDict):
    environmentName: str
    nextToken: NotRequired[str]

class ListEnvironmentTemplateVersionsInputRequestTypeDef(TypedDict):
    templateName: str
    majorVersion: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentTemplatesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListRepositoriesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class RepositorySummaryTypeDef(TypedDict):
    arn: str
    connectionArn: str
    name: str
    provider: RepositoryProviderType

class ListRepositorySyncDefinitionsInputRequestTypeDef(TypedDict):
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    syncType: SyncTypeType
    nextToken: NotRequired[str]

class RepositorySyncDefinitionTypeDef(TypedDict):
    branch: str
    directory: str
    parent: str
    target: str

class ListServiceInstanceOutputsInputRequestTypeDef(TypedDict):
    serviceInstanceName: str
    serviceName: str
    deploymentId: NotRequired[str]
    nextToken: NotRequired[str]

class ListServiceInstanceProvisionedResourcesInputRequestTypeDef(TypedDict):
    serviceInstanceName: str
    serviceName: str
    nextToken: NotRequired[str]

class ListServiceInstancesFilterTypeDef(TypedDict):
    key: NotRequired[ListServiceInstancesFilterByType]
    value: NotRequired[str]

class ServiceInstanceSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    deploymentStatus: DeploymentStatusType
    environmentName: str
    lastDeploymentAttemptedAt: datetime
    lastDeploymentSucceededAt: datetime
    name: str
    serviceName: str
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    deploymentStatusMessage: NotRequired[str]
    lastAttemptedDeploymentId: NotRequired[str]
    lastSucceededDeploymentId: NotRequired[str]

class ListServicePipelineOutputsInputRequestTypeDef(TypedDict):
    serviceName: str
    deploymentId: NotRequired[str]
    nextToken: NotRequired[str]

class ListServicePipelineProvisionedResourcesInputRequestTypeDef(TypedDict):
    serviceName: str
    nextToken: NotRequired[str]

class ListServiceTemplateVersionsInputRequestTypeDef(TypedDict):
    templateName: str
    majorVersion: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ServiceTemplateVersionSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    majorVersion: str
    minorVersion: str
    status: TemplateVersionStatusType
    templateName: str
    description: NotRequired[str]
    recommendedMinorVersion: NotRequired[str]
    statusMessage: NotRequired[str]

class ListServiceTemplatesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ServiceTemplateSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]
    pipelineProvisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]
    recommendedVersion: NotRequired[str]

class ListServicesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ServiceSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    name: str
    status: ServiceStatusType
    templateName: str
    description: NotRequired[str]
    statusMessage: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

RejectEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)
RepositorySyncEventTypeDef = TypedDict(
    "RepositorySyncEventTypeDef",
    {
        "event": str,
        "time": datetime,
        "type": str,
        "externalId": NotRequired[str],
    },
)
ResourceSyncEventTypeDef = TypedDict(
    "ResourceSyncEventTypeDef",
    {
        "event": str,
        "time": datetime,
        "type": str,
        "externalId": NotRequired[str],
    },
)

class S3ObjectSourceTypeDef(TypedDict):
    bucket: str
    key: str

class SyncBlockerContextTypeDef(TypedDict):
    key: str
    value: str

class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateComponentInputRequestTypeDef(TypedDict):
    deploymentType: ComponentDeploymentUpdateTypeType
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]
    serviceSpec: NotRequired[str]
    templateFile: NotRequired[str]

UpdateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "UpdateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
        "codebuildRoleArn": NotRequired[str],
        "componentRoleArn": NotRequired[str],
        "roleArn": NotRequired[str],
    },
)

class UpdateEnvironmentTemplateInputRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]

class UpdateEnvironmentTemplateVersionInputRequestTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str
    description: NotRequired[str]
    status: NotRequired[TemplateVersionStatusType]

class UpdateServiceInputRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    spec: NotRequired[str]

class UpdateServiceInstanceInputRequestTypeDef(TypedDict):
    deploymentType: DeploymentUpdateTypeType
    name: str
    serviceName: str
    clientToken: NotRequired[str]
    spec: NotRequired[str]
    templateMajorVersion: NotRequired[str]
    templateMinorVersion: NotRequired[str]

class UpdateServicePipelineInputRequestTypeDef(TypedDict):
    deploymentType: DeploymentUpdateTypeType
    serviceName: str
    spec: str
    templateMajorVersion: NotRequired[str]
    templateMinorVersion: NotRequired[str]

UpdateServiceSyncBlockerInputRequestTypeDef = TypedDict(
    "UpdateServiceSyncBlockerInputRequestTypeDef",
    {
        "id": str,
        "resolvedReason": str,
    },
)

class UpdateServiceSyncConfigInputRequestTypeDef(TypedDict):
    branch: str
    filePath: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    serviceName: str

class UpdateServiceTemplateInputRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]

class UpdateTemplateSyncConfigInputRequestTypeDef(TypedDict):
    branch: str
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    templateName: str
    templateType: TemplateTypeType
    subdirectory: NotRequired[str]

class AcceptEnvironmentAccountConnectionOutputTypeDef(TypedDict):
    environmentAccountConnection: EnvironmentAccountConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEnvironmentAccountConnectionOutputTypeDef(TypedDict):
    environmentAccountConnection: EnvironmentAccountConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEnvironmentAccountConnectionOutputTypeDef(TypedDict):
    environmentAccountConnection: EnvironmentAccountConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentAccountConnectionOutputTypeDef(TypedDict):
    environmentAccountConnection: EnvironmentAccountConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RejectEnvironmentAccountConnectionOutputTypeDef(TypedDict):
    environmentAccountConnection: EnvironmentAccountConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEnvironmentAccountConnectionOutputTypeDef(TypedDict):
    environmentAccountConnection: EnvironmentAccountConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AccountSettingsTypeDef(TypedDict):
    pipelineCodebuildRoleArn: NotRequired[str]
    pipelineProvisioningRepository: NotRequired[RepositoryBranchTypeDef]
    pipelineServiceRoleArn: NotRequired[str]

class EnvironmentTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    deploymentStatus: DeploymentStatusType
    lastDeploymentAttemptedAt: datetime
    lastDeploymentSucceededAt: datetime
    name: str
    templateMajorVersion: str
    templateMinorVersion: str
    templateName: str
    codebuildRoleArn: NotRequired[str]
    componentRoleArn: NotRequired[str]
    deploymentStatusMessage: NotRequired[str]
    description: NotRequired[str]
    environmentAccountConnectionId: NotRequired[str]
    environmentAccountId: NotRequired[str]
    lastAttemptedDeploymentId: NotRequired[str]
    lastSucceededDeploymentId: NotRequired[str]
    protonServiceRoleArn: NotRequired[str]
    provisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]
    provisioningRepository: NotRequired[RepositoryBranchTypeDef]
    spec: NotRequired[str]

class CancelComponentDeploymentOutputTypeDef(TypedDict):
    component: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateComponentOutputTypeDef(TypedDict):
    component: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteComponentOutputTypeDef(TypedDict):
    component: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetComponentOutputTypeDef(TypedDict):
    component: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateComponentOutputTypeDef(TypedDict):
    component: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CancelServiceInstanceDeploymentOutputTypeDef(TypedDict):
    serviceInstance: ServiceInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceInstanceOutputTypeDef(TypedDict):
    serviceInstance: ServiceInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceInstanceOutputTypeDef(TypedDict):
    serviceInstance: ServiceInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceInstanceOutputTypeDef(TypedDict):
    serviceInstance: ServiceInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CancelServicePipelineDeploymentOutputTypeDef(TypedDict):
    pipeline: ServicePipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ServiceTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastModifiedAt: datetime
    name: str
    spec: str
    status: ServiceStatusType
    templateName: str
    branchName: NotRequired[str]
    description: NotRequired[str]
    pipeline: NotRequired[ServicePipelineTypeDef]
    repositoryConnectionArn: NotRequired[str]
    repositoryId: NotRequired[str]
    statusMessage: NotRequired[str]

class UpdateServicePipelineOutputTypeDef(TypedDict):
    pipeline: ServicePipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceTemplateVersionInputRequestTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str
    compatibleEnvironmentTemplates: NotRequired[Sequence[CompatibleEnvironmentTemplateInputTypeDef]]
    description: NotRequired[str]
    status: NotRequired[TemplateVersionStatusType]
    supportedComponentSources: NotRequired[Sequence[Literal["DIRECTLY_DEFINED"]]]

class ServiceTemplateVersionTypeDef(TypedDict):
    arn: str
    compatibleEnvironmentTemplates: List[CompatibleEnvironmentTemplateTypeDef]
    createdAt: datetime
    lastModifiedAt: datetime
    majorVersion: str
    minorVersion: str
    status: TemplateVersionStatusType
    templateName: str
    description: NotRequired[str]
    recommendedMinorVersion: NotRequired[str]
    schema: NotRequired[str]
    statusMessage: NotRequired[str]
    supportedComponentSources: NotRequired[List[Literal["DIRECTLY_DEFINED"]]]

class ListComponentsOutputTypeDef(TypedDict):
    components: List[ComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CountsSummaryTypeDef(TypedDict):
    components: NotRequired[ResourceCountsSummaryTypeDef]
    environmentTemplates: NotRequired[ResourceCountsSummaryTypeDef]
    environments: NotRequired[ResourceCountsSummaryTypeDef]
    pipelines: NotRequired[ResourceCountsSummaryTypeDef]
    serviceInstances: NotRequired[ResourceCountsSummaryTypeDef]
    serviceTemplates: NotRequired[ResourceCountsSummaryTypeDef]
    services: NotRequired[ResourceCountsSummaryTypeDef]

class CreateComponentInputRequestTypeDef(TypedDict):
    manifest: str
    name: str
    templateFile: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    environmentName: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]
    serviceSpec: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateEnvironmentAccountConnectionInputRequestTypeDef(TypedDict):
    environmentName: str
    managementAccountId: str
    clientToken: NotRequired[str]
    codebuildRoleArn: NotRequired[str]
    componentRoleArn: NotRequired[str]
    roleArn: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateEnvironmentTemplateInputRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]
    encryptionKey: NotRequired[str]
    provisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateRepositoryInputRequestTypeDef(TypedDict):
    connectionArn: str
    name: str
    provider: RepositoryProviderType
    encryptionKey: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateServiceInputRequestTypeDef(TypedDict):
    name: str
    spec: str
    templateMajorVersion: str
    templateName: str
    branchName: NotRequired[str]
    description: NotRequired[str]
    repositoryConnectionArn: NotRequired[str]
    repositoryId: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    templateMinorVersion: NotRequired[str]

class CreateServiceInstanceInputRequestTypeDef(TypedDict):
    name: str
    serviceName: str
    spec: str
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    templateMajorVersion: NotRequired[str]
    templateMinorVersion: NotRequired[str]

class CreateServiceTemplateInputRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    displayName: NotRequired[str]
    encryptionKey: NotRequired[str]
    pipelineProvisioning: NotRequired[Literal["CUSTOMER_MANAGED"]]
    tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class CreateEnvironmentInputRequestTypeDef(TypedDict):
    name: str
    spec: str
    templateMajorVersion: str
    templateName: str
    codebuildRoleArn: NotRequired[str]
    componentRoleArn: NotRequired[str]
    description: NotRequired[str]
    environmentAccountConnectionId: NotRequired[str]
    protonServiceRoleArn: NotRequired[str]
    provisioningRepository: NotRequired[RepositoryBranchInputTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    templateMinorVersion: NotRequired[str]

class UpdateAccountSettingsInputRequestTypeDef(TypedDict):
    deletePipelineProvisioningRepository: NotRequired[bool]
    pipelineCodebuildRoleArn: NotRequired[str]
    pipelineProvisioningRepository: NotRequired[RepositoryBranchInputTypeDef]
    pipelineServiceRoleArn: NotRequired[str]

class UpdateEnvironmentInputRequestTypeDef(TypedDict):
    deploymentType: DeploymentUpdateTypeType
    name: str
    codebuildRoleArn: NotRequired[str]
    componentRoleArn: NotRequired[str]
    description: NotRequired[str]
    environmentAccountConnectionId: NotRequired[str]
    protonServiceRoleArn: NotRequired[str]
    provisioningRepository: NotRequired[RepositoryBranchInputTypeDef]
    spec: NotRequired[str]
    templateMajorVersion: NotRequired[str]
    templateMinorVersion: NotRequired[str]

class CreateEnvironmentTemplateOutputTypeDef(TypedDict):
    environmentTemplate: EnvironmentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEnvironmentTemplateOutputTypeDef(TypedDict):
    environmentTemplate: EnvironmentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentTemplateOutputTypeDef(TypedDict):
    environmentTemplate: EnvironmentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEnvironmentTemplateOutputTypeDef(TypedDict):
    environmentTemplate: EnvironmentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEnvironmentTemplateVersionOutputTypeDef(TypedDict):
    environmentTemplateVersion: EnvironmentTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEnvironmentTemplateVersionOutputTypeDef(TypedDict):
    environmentTemplateVersion: EnvironmentTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentTemplateVersionOutputTypeDef(TypedDict):
    environmentTemplateVersion: EnvironmentTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEnvironmentTemplateVersionOutputTypeDef(TypedDict):
    environmentTemplateVersion: EnvironmentTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRepositoryOutputTypeDef(TypedDict):
    repository: RepositoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRepositoryOutputTypeDef(TypedDict):
    repository: RepositoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRepositoryOutputTypeDef(TypedDict):
    repository: RepositoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceSyncConfigOutputTypeDef(TypedDict):
    serviceSyncConfig: ServiceSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteServiceSyncConfigOutputTypeDef(TypedDict):
    serviceSyncConfig: ServiceSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceSyncConfigOutputTypeDef(TypedDict):
    serviceSyncConfig: ServiceSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceSyncConfigOutputTypeDef(TypedDict):
    serviceSyncConfig: ServiceSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceTemplateOutputTypeDef(TypedDict):
    serviceTemplate: ServiceTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteServiceTemplateOutputTypeDef(TypedDict):
    serviceTemplate: ServiceTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceTemplateOutputTypeDef(TypedDict):
    serviceTemplate: ServiceTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceTemplateOutputTypeDef(TypedDict):
    serviceTemplate: ServiceTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTemplateSyncConfigOutputTypeDef(TypedDict):
    templateSyncConfig: TemplateSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTemplateSyncConfigOutputTypeDef(TypedDict):
    templateSyncConfig: TemplateSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetTemplateSyncConfigOutputTypeDef(TypedDict):
    templateSyncConfig: TemplateSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTemplateSyncConfigOutputTypeDef(TypedDict):
    templateSyncConfig: TemplateSyncConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeploymentStateTypeDef(TypedDict):
    component: NotRequired[ComponentStateTypeDef]
    environment: NotRequired[EnvironmentStateTypeDef]
    serviceInstance: NotRequired[ServiceInstanceStateTypeDef]
    servicePipeline: NotRequired[ServicePipelineStateTypeDef]

class ListDeploymentsOutputTypeDef(TypedDict):
    deployments: List[DeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentAccountConnectionsOutputTypeDef(TypedDict):
    environmentAccountConnections: List[EnvironmentAccountConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentsOutputTypeDef(TypedDict):
    environments: List[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentsInputRequestTypeDef(TypedDict):
    environmentTemplates: NotRequired[Sequence[EnvironmentTemplateFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentTemplatesOutputTypeDef(TypedDict):
    templates: List[EnvironmentTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentTemplateVersionsOutputTypeDef(TypedDict):
    templateVersions: List[EnvironmentTemplateVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetComponentInputComponentDeletedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetComponentInputComponentDeployedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetEnvironmentInputEnvironmentDeployedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetServiceInputServiceCreatedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetServiceInputServiceDeletedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetServiceInputServicePipelineDeployedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetServiceInputServiceUpdatedWaitTypeDef(TypedDict):
    name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef(TypedDict):
    name: str
    serviceName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef(TypedDict):
    majorVersion: str
    minorVersion: str
    templateName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListComponentOutputsInputListComponentOutputsPaginateTypeDef(TypedDict):
    componentName: str
    deploymentId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef(
    TypedDict
):
    componentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComponentsInputListComponentsPaginateTypeDef(TypedDict):
    environmentName: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeploymentsInputListDeploymentsPaginateTypeDef(TypedDict):
    componentName: NotRequired[str]
    environmentName: NotRequired[str]
    serviceInstanceName: NotRequired[str]
    serviceName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef(
    TypedDict
):
    requestedBy: EnvironmentAccountConnectionRequesterAccountTypeType
    environmentName: NotRequired[str]
    statuses: NotRequired[Sequence[EnvironmentAccountConnectionStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef(TypedDict):
    environmentName: str
    deploymentId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef(
    TypedDict
):
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef(TypedDict):
    templateName: str
    majorVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsInputListEnvironmentsPaginateTypeDef(TypedDict):
    environmentTemplates: NotRequired[Sequence[EnvironmentTemplateFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRepositoriesInputListRepositoriesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef(TypedDict):
    repositoryName: str
    repositoryProvider: RepositoryProviderType
    syncType: SyncTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef(TypedDict):
    serviceInstanceName: str
    serviceName: str
    deploymentId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef(
    TypedDict
):
    serviceInstanceName: str
    serviceName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef(TypedDict):
    serviceName: str
    deploymentId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef(
    TypedDict
):
    serviceName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef(TypedDict):
    templateName: str
    majorVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicesInputListServicesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComponentOutputsOutputTypeDef(TypedDict):
    outputs: List[OutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentOutputsOutputTypeDef(TypedDict):
    outputs: List[OutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceInstanceOutputsOutputTypeDef(TypedDict):
    outputs: List[OutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServicePipelineOutputsOutputTypeDef(TypedDict):
    outputs: List[OutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class NotifyResourceDeploymentStatusChangeInputRequestTypeDef(TypedDict):
    resourceArn: str
    deploymentId: NotRequired[str]
    outputs: NotRequired[Sequence[OutputTypeDef]]
    status: NotRequired[ResourceDeploymentStatusType]
    statusMessage: NotRequired[str]

class ListComponentProvisionedResourcesOutputTypeDef(TypedDict):
    provisionedResources: List[ProvisionedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentProvisionedResourcesOutputTypeDef(TypedDict):
    provisionedResources: List[ProvisionedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceInstanceProvisionedResourcesOutputTypeDef(TypedDict):
    provisionedResources: List[ProvisionedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServicePipelineProvisionedResourcesOutputTypeDef(TypedDict):
    provisionedResources: List[ProvisionedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRepositoriesOutputTypeDef(TypedDict):
    repositories: List[RepositorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRepositorySyncDefinitionsOutputTypeDef(TypedDict):
    syncDefinitions: List[RepositorySyncDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceInstancesInputListServiceInstancesPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[ListServiceInstancesFilterTypeDef]]
    serviceName: NotRequired[str]
    sortBy: NotRequired[ListServiceInstancesSortByType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceInstancesInputRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[ListServiceInstancesFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    serviceName: NotRequired[str]
    sortBy: NotRequired[ListServiceInstancesSortByType]
    sortOrder: NotRequired[SortOrderType]

class ListServiceInstancesOutputTypeDef(TypedDict):
    serviceInstances: List[ServiceInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceTemplateVersionsOutputTypeDef(TypedDict):
    templateVersions: List[ServiceTemplateVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceTemplatesOutputTypeDef(TypedDict):
    templates: List[ServiceTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServicesOutputTypeDef(TypedDict):
    services: List[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RepositorySyncAttemptTypeDef(TypedDict):
    events: List[RepositorySyncEventTypeDef]
    startedAt: datetime
    status: RepositorySyncStatusType

class ResourceSyncAttemptTypeDef(TypedDict):
    events: List[ResourceSyncEventTypeDef]
    initialRevision: RevisionTypeDef
    startedAt: datetime
    status: ResourceSyncStatusType
    target: str
    targetRevision: RevisionTypeDef

class TemplateVersionSourceInputTypeDef(TypedDict):
    s3: NotRequired[S3ObjectSourceTypeDef]

SyncBlockerTypeDef = TypedDict(
    "SyncBlockerTypeDef",
    {
        "createdAt": datetime,
        "createdReason": str,
        "id": str,
        "status": BlockerStatusType,
        "type": Literal["AUTOMATED"],
        "contexts": NotRequired[List[SyncBlockerContextTypeDef]],
        "resolvedAt": NotRequired[datetime],
        "resolvedReason": NotRequired[str],
    },
)

class GetAccountSettingsOutputTypeDef(TypedDict):
    accountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAccountSettingsOutputTypeDef(TypedDict):
    accountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CancelEnvironmentDeploymentOutputTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEnvironmentOutputTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEnvironmentOutputTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentOutputTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEnvironmentOutputTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceOutputTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteServiceOutputTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceOutputTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceOutputTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceTemplateVersionOutputTypeDef(TypedDict):
    serviceTemplateVersion: ServiceTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteServiceTemplateVersionOutputTypeDef(TypedDict):
    serviceTemplateVersion: ServiceTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceTemplateVersionOutputTypeDef(TypedDict):
    serviceTemplateVersion: ServiceTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceTemplateVersionOutputTypeDef(TypedDict):
    serviceTemplateVersion: ServiceTemplateVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcesSummaryOutputTypeDef(TypedDict):
    counts: CountsSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "targetArn": str,
        "targetResourceCreatedAt": datetime,
        "targetResourceType": DeploymentTargetResourceTypeType,
        "completedAt": NotRequired[datetime],
        "componentName": NotRequired[str],
        "deploymentStatusMessage": NotRequired[str],
        "initialState": NotRequired[DeploymentStateTypeDef],
        "lastAttemptedDeploymentId": NotRequired[str],
        "lastSucceededDeploymentId": NotRequired[str],
        "serviceInstanceName": NotRequired[str],
        "serviceName": NotRequired[str],
        "targetState": NotRequired[DeploymentStateTypeDef],
    },
)

class GetRepositorySyncStatusOutputTypeDef(TypedDict):
    latestSync: RepositorySyncAttemptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceInstanceSyncStatusOutputTypeDef(TypedDict):
    desiredState: RevisionTypeDef
    latestSuccessfulSync: ResourceSyncAttemptTypeDef
    latestSync: ResourceSyncAttemptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetTemplateSyncStatusOutputTypeDef(TypedDict):
    desiredState: RevisionTypeDef
    latestSuccessfulSync: ResourceSyncAttemptTypeDef
    latestSync: ResourceSyncAttemptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEnvironmentTemplateVersionInputRequestTypeDef(TypedDict):
    source: TemplateVersionSourceInputTypeDef
    templateName: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    majorVersion: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateServiceTemplateVersionInputRequestTypeDef(TypedDict):
    compatibleEnvironmentTemplates: Sequence[CompatibleEnvironmentTemplateInputTypeDef]
    source: TemplateVersionSourceInputTypeDef
    templateName: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    majorVersion: NotRequired[str]
    supportedComponentSources: NotRequired[Sequence[Literal["DIRECTLY_DEFINED"]]]
    tags: NotRequired[Sequence[TagTypeDef]]

class ServiceSyncBlockerSummaryTypeDef(TypedDict):
    serviceName: str
    latestBlockers: NotRequired[List[SyncBlockerTypeDef]]
    serviceInstanceName: NotRequired[str]

class UpdateServiceSyncBlockerOutputTypeDef(TypedDict):
    serviceInstanceName: str
    serviceName: str
    serviceSyncBlocker: SyncBlockerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDeploymentOutputTypeDef(TypedDict):
    deployment: DeploymentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeploymentOutputTypeDef(TypedDict):
    deployment: DeploymentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceSyncBlockerSummaryOutputTypeDef(TypedDict):
    serviceSyncBlockerSummary: ServiceSyncBlockerSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
