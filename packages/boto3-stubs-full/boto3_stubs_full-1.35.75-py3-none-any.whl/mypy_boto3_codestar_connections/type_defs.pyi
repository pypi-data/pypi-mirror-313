"""
Type annotations for codestar-connections service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_connections/type_defs/)

Usage::

    ```python
    from mypy_boto3_codestar_connections.type_defs import ConnectionTypeDef

    data: ConnectionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    BlockerStatusType,
    ConnectionStatusType,
    ProviderTypeType,
    PublishDeploymentStatusType,
    RepositorySyncStatusType,
    ResourceSyncStatusType,
    TriggerResourceUpdateOnType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ConnectionTypeDef",
    "CreateConnectionInputRequestTypeDef",
    "CreateConnectionOutputTypeDef",
    "CreateHostInputRequestTypeDef",
    "CreateHostOutputTypeDef",
    "CreateRepositoryLinkInputRequestTypeDef",
    "CreateRepositoryLinkOutputTypeDef",
    "CreateSyncConfigurationInputRequestTypeDef",
    "CreateSyncConfigurationOutputTypeDef",
    "DeleteConnectionInputRequestTypeDef",
    "DeleteHostInputRequestTypeDef",
    "DeleteRepositoryLinkInputRequestTypeDef",
    "DeleteSyncConfigurationInputRequestTypeDef",
    "GetConnectionInputRequestTypeDef",
    "GetConnectionOutputTypeDef",
    "GetHostInputRequestTypeDef",
    "GetHostOutputTypeDef",
    "GetRepositoryLinkInputRequestTypeDef",
    "GetRepositoryLinkOutputTypeDef",
    "GetRepositorySyncStatusInputRequestTypeDef",
    "GetRepositorySyncStatusOutputTypeDef",
    "GetResourceSyncStatusInputRequestTypeDef",
    "GetResourceSyncStatusOutputTypeDef",
    "GetSyncBlockerSummaryInputRequestTypeDef",
    "GetSyncBlockerSummaryOutputTypeDef",
    "GetSyncConfigurationInputRequestTypeDef",
    "GetSyncConfigurationOutputTypeDef",
    "HostTypeDef",
    "ListConnectionsInputRequestTypeDef",
    "ListConnectionsOutputTypeDef",
    "ListHostsInputRequestTypeDef",
    "ListHostsOutputTypeDef",
    "ListRepositoryLinksInputRequestTypeDef",
    "ListRepositoryLinksOutputTypeDef",
    "ListRepositorySyncDefinitionsInputRequestTypeDef",
    "ListRepositorySyncDefinitionsOutputTypeDef",
    "ListSyncConfigurationsInputRequestTypeDef",
    "ListSyncConfigurationsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "RepositoryLinkInfoTypeDef",
    "RepositorySyncAttemptTypeDef",
    "RepositorySyncDefinitionTypeDef",
    "RepositorySyncEventTypeDef",
    "ResourceSyncAttemptTypeDef",
    "ResourceSyncEventTypeDef",
    "ResponseMetadataTypeDef",
    "RevisionTypeDef",
    "SyncBlockerContextTypeDef",
    "SyncBlockerSummaryTypeDef",
    "SyncBlockerTypeDef",
    "SyncConfigurationTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateHostInputRequestTypeDef",
    "UpdateRepositoryLinkInputRequestTypeDef",
    "UpdateRepositoryLinkOutputTypeDef",
    "UpdateSyncBlockerInputRequestTypeDef",
    "UpdateSyncBlockerOutputTypeDef",
    "UpdateSyncConfigurationInputRequestTypeDef",
    "UpdateSyncConfigurationOutputTypeDef",
    "VpcConfigurationOutputTypeDef",
    "VpcConfigurationTypeDef",
)

class ConnectionTypeDef(TypedDict):
    ConnectionName: NotRequired[str]
    ConnectionArn: NotRequired[str]
    ProviderType: NotRequired[ProviderTypeType]
    OwnerAccountId: NotRequired[str]
    ConnectionStatus: NotRequired[ConnectionStatusType]
    HostArn: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class VpcConfigurationTypeDef(TypedDict):
    VpcId: str
    SubnetIds: Sequence[str]
    SecurityGroupIds: Sequence[str]
    TlsCertificate: NotRequired[str]

class RepositoryLinkInfoTypeDef(TypedDict):
    ConnectionArn: str
    OwnerId: str
    ProviderType: ProviderTypeType
    RepositoryLinkArn: str
    RepositoryLinkId: str
    RepositoryName: str
    EncryptionKeyArn: NotRequired[str]

class CreateSyncConfigurationInputRequestTypeDef(TypedDict):
    Branch: str
    ConfigFile: str
    RepositoryLinkId: str
    ResourceName: str
    RoleArn: str
    SyncType: Literal["CFN_STACK_SYNC"]
    PublishDeploymentStatus: NotRequired[PublishDeploymentStatusType]
    TriggerResourceUpdateOn: NotRequired[TriggerResourceUpdateOnType]

class SyncConfigurationTypeDef(TypedDict):
    Branch: str
    OwnerId: str
    ProviderType: ProviderTypeType
    RepositoryLinkId: str
    RepositoryName: str
    ResourceName: str
    RoleArn: str
    SyncType: Literal["CFN_STACK_SYNC"]
    ConfigFile: NotRequired[str]
    PublishDeploymentStatus: NotRequired[PublishDeploymentStatusType]
    TriggerResourceUpdateOn: NotRequired[TriggerResourceUpdateOnType]

class DeleteConnectionInputRequestTypeDef(TypedDict):
    ConnectionArn: str

class DeleteHostInputRequestTypeDef(TypedDict):
    HostArn: str

class DeleteRepositoryLinkInputRequestTypeDef(TypedDict):
    RepositoryLinkId: str

class DeleteSyncConfigurationInputRequestTypeDef(TypedDict):
    SyncType: Literal["CFN_STACK_SYNC"]
    ResourceName: str

class GetConnectionInputRequestTypeDef(TypedDict):
    ConnectionArn: str

class GetHostInputRequestTypeDef(TypedDict):
    HostArn: str

class VpcConfigurationOutputTypeDef(TypedDict):
    VpcId: str
    SubnetIds: List[str]
    SecurityGroupIds: List[str]
    TlsCertificate: NotRequired[str]

class GetRepositoryLinkInputRequestTypeDef(TypedDict):
    RepositoryLinkId: str

class GetRepositorySyncStatusInputRequestTypeDef(TypedDict):
    Branch: str
    RepositoryLinkId: str
    SyncType: Literal["CFN_STACK_SYNC"]

class GetResourceSyncStatusInputRequestTypeDef(TypedDict):
    ResourceName: str
    SyncType: Literal["CFN_STACK_SYNC"]

class RevisionTypeDef(TypedDict):
    Branch: str
    Directory: str
    OwnerId: str
    RepositoryName: str
    ProviderType: ProviderTypeType
    Sha: str

class GetSyncBlockerSummaryInputRequestTypeDef(TypedDict):
    SyncType: Literal["CFN_STACK_SYNC"]
    ResourceName: str

class GetSyncConfigurationInputRequestTypeDef(TypedDict):
    SyncType: Literal["CFN_STACK_SYNC"]
    ResourceName: str

class ListConnectionsInputRequestTypeDef(TypedDict):
    ProviderTypeFilter: NotRequired[ProviderTypeType]
    HostArnFilter: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListHostsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRepositoryLinksInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRepositorySyncDefinitionsInputRequestTypeDef(TypedDict):
    RepositoryLinkId: str
    SyncType: Literal["CFN_STACK_SYNC"]

class RepositorySyncDefinitionTypeDef(TypedDict):
    Branch: str
    Directory: str
    Parent: str
    Target: str

class ListSyncConfigurationsInputRequestTypeDef(TypedDict):
    RepositoryLinkId: str
    SyncType: Literal["CFN_STACK_SYNC"]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str

RepositorySyncEventTypeDef = TypedDict(
    "RepositorySyncEventTypeDef",
    {
        "Event": str,
        "Time": datetime,
        "Type": str,
        "ExternalId": NotRequired[str],
    },
)
ResourceSyncEventTypeDef = TypedDict(
    "ResourceSyncEventTypeDef",
    {
        "Event": str,
        "Time": datetime,
        "Type": str,
        "ExternalId": NotRequired[str],
    },
)

class SyncBlockerContextTypeDef(TypedDict):
    Key: str
    Value: str

class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateRepositoryLinkInputRequestTypeDef(TypedDict):
    RepositoryLinkId: str
    ConnectionArn: NotRequired[str]
    EncryptionKeyArn: NotRequired[str]

class UpdateSyncBlockerInputRequestTypeDef(TypedDict):
    Id: str
    SyncType: Literal["CFN_STACK_SYNC"]
    ResourceName: str
    ResolvedReason: str

class UpdateSyncConfigurationInputRequestTypeDef(TypedDict):
    ResourceName: str
    SyncType: Literal["CFN_STACK_SYNC"]
    Branch: NotRequired[str]
    ConfigFile: NotRequired[str]
    RepositoryLinkId: NotRequired[str]
    RoleArn: NotRequired[str]
    PublishDeploymentStatus: NotRequired[PublishDeploymentStatusType]
    TriggerResourceUpdateOn: NotRequired[TriggerResourceUpdateOnType]

class CreateConnectionInputRequestTypeDef(TypedDict):
    ConnectionName: str
    ProviderType: NotRequired[ProviderTypeType]
    Tags: NotRequired[Sequence[TagTypeDef]]
    HostArn: NotRequired[str]

class CreateRepositoryLinkInputRequestTypeDef(TypedDict):
    ConnectionArn: str
    OwnerId: str
    RepositoryName: str
    EncryptionKeyArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class CreateConnectionOutputTypeDef(TypedDict):
    ConnectionArn: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateHostOutputTypeDef(TypedDict):
    HostArn: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetConnectionOutputTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListConnectionsOutputTypeDef(TypedDict):
    Connections: List[ConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateHostInputRequestTypeDef(TypedDict):
    Name: str
    ProviderType: ProviderTypeType
    ProviderEndpoint: str
    VpcConfiguration: NotRequired[VpcConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateHostInputRequestTypeDef(TypedDict):
    HostArn: str
    ProviderEndpoint: NotRequired[str]
    VpcConfiguration: NotRequired[VpcConfigurationTypeDef]

class CreateRepositoryLinkOutputTypeDef(TypedDict):
    RepositoryLinkInfo: RepositoryLinkInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRepositoryLinkOutputTypeDef(TypedDict):
    RepositoryLinkInfo: RepositoryLinkInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRepositoryLinksOutputTypeDef(TypedDict):
    RepositoryLinks: List[RepositoryLinkInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateRepositoryLinkOutputTypeDef(TypedDict):
    RepositoryLinkInfo: RepositoryLinkInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSyncConfigurationOutputTypeDef(TypedDict):
    SyncConfiguration: SyncConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSyncConfigurationOutputTypeDef(TypedDict):
    SyncConfiguration: SyncConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSyncConfigurationsOutputTypeDef(TypedDict):
    SyncConfigurations: List[SyncConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateSyncConfigurationOutputTypeDef(TypedDict):
    SyncConfiguration: SyncConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetHostOutputTypeDef(TypedDict):
    Name: str
    Status: str
    ProviderType: ProviderTypeType
    ProviderEndpoint: str
    VpcConfiguration: VpcConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class HostTypeDef(TypedDict):
    Name: NotRequired[str]
    HostArn: NotRequired[str]
    ProviderType: NotRequired[ProviderTypeType]
    ProviderEndpoint: NotRequired[str]
    VpcConfiguration: NotRequired[VpcConfigurationOutputTypeDef]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]

class ListRepositorySyncDefinitionsOutputTypeDef(TypedDict):
    RepositorySyncDefinitions: List[RepositorySyncDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RepositorySyncAttemptTypeDef(TypedDict):
    StartedAt: datetime
    Status: RepositorySyncStatusType
    Events: List[RepositorySyncEventTypeDef]

class ResourceSyncAttemptTypeDef(TypedDict):
    Events: List[ResourceSyncEventTypeDef]
    InitialRevision: RevisionTypeDef
    StartedAt: datetime
    Status: ResourceSyncStatusType
    TargetRevision: RevisionTypeDef
    Target: str

SyncBlockerTypeDef = TypedDict(
    "SyncBlockerTypeDef",
    {
        "Id": str,
        "Type": Literal["AUTOMATED"],
        "Status": BlockerStatusType,
        "CreatedReason": str,
        "CreatedAt": datetime,
        "Contexts": NotRequired[List[SyncBlockerContextTypeDef]],
        "ResolvedReason": NotRequired[str],
        "ResolvedAt": NotRequired[datetime],
    },
)

class ListHostsOutputTypeDef(TypedDict):
    Hosts: List[HostTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetRepositorySyncStatusOutputTypeDef(TypedDict):
    LatestSync: RepositorySyncAttemptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceSyncStatusOutputTypeDef(TypedDict):
    DesiredState: RevisionTypeDef
    LatestSuccessfulSync: ResourceSyncAttemptTypeDef
    LatestSync: ResourceSyncAttemptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SyncBlockerSummaryTypeDef(TypedDict):
    ResourceName: str
    ParentResourceName: NotRequired[str]
    LatestBlockers: NotRequired[List[SyncBlockerTypeDef]]

class UpdateSyncBlockerOutputTypeDef(TypedDict):
    ResourceName: str
    ParentResourceName: str
    SyncBlocker: SyncBlockerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSyncBlockerSummaryOutputTypeDef(TypedDict):
    SyncBlockerSummary: SyncBlockerSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
