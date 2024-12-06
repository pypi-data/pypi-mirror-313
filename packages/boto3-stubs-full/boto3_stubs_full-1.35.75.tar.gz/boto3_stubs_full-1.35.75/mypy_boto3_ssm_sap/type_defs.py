"""
Type annotations for ssm-sap service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm_sap.type_defs import ApplicationCredentialTypeDef

    data: ApplicationCredentialTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AllocationTypeType,
    ApplicationDiscoveryStatusType,
    ApplicationStatusType,
    ApplicationTypeType,
    ClusterStatusType,
    ComponentStatusType,
    ComponentTypeType,
    DatabaseConnectionMethodType,
    DatabaseStatusType,
    DatabaseTypeType,
    FilterOperatorType,
    HostRoleType,
    OperationEventStatusType,
    OperationModeType,
    OperationStatusType,
    ReplicationModeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ApplicationCredentialTypeDef",
    "ApplicationSummaryTypeDef",
    "ApplicationTypeDef",
    "AssociatedHostTypeDef",
    "BackintConfigTypeDef",
    "ComponentSummaryTypeDef",
    "ComponentTypeDef",
    "DatabaseConnectionTypeDef",
    "DatabaseSummaryTypeDef",
    "DatabaseTypeDef",
    "DeleteResourcePermissionInputRequestTypeDef",
    "DeleteResourcePermissionOutputTypeDef",
    "DeregisterApplicationInputRequestTypeDef",
    "FilterTypeDef",
    "GetApplicationInputRequestTypeDef",
    "GetApplicationOutputTypeDef",
    "GetComponentInputRequestTypeDef",
    "GetComponentOutputTypeDef",
    "GetDatabaseInputRequestTypeDef",
    "GetDatabaseOutputTypeDef",
    "GetOperationInputRequestTypeDef",
    "GetOperationOutputTypeDef",
    "GetResourcePermissionInputRequestTypeDef",
    "GetResourcePermissionOutputTypeDef",
    "HostTypeDef",
    "IpAddressMemberTypeDef",
    "ListApplicationsInputListApplicationsPaginateTypeDef",
    "ListApplicationsInputRequestTypeDef",
    "ListApplicationsOutputTypeDef",
    "ListComponentsInputListComponentsPaginateTypeDef",
    "ListComponentsInputRequestTypeDef",
    "ListComponentsOutputTypeDef",
    "ListDatabasesInputListDatabasesPaginateTypeDef",
    "ListDatabasesInputRequestTypeDef",
    "ListDatabasesOutputTypeDef",
    "ListOperationEventsInputListOperationEventsPaginateTypeDef",
    "ListOperationEventsInputRequestTypeDef",
    "ListOperationEventsOutputTypeDef",
    "ListOperationsInputListOperationsPaginateTypeDef",
    "ListOperationsInputRequestTypeDef",
    "ListOperationsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OperationEventTypeDef",
    "OperationTypeDef",
    "PaginatorConfigTypeDef",
    "PutResourcePermissionInputRequestTypeDef",
    "PutResourcePermissionOutputTypeDef",
    "RegisterApplicationInputRequestTypeDef",
    "RegisterApplicationOutputTypeDef",
    "ResilienceTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "StartApplicationInputRequestTypeDef",
    "StartApplicationOutputTypeDef",
    "StartApplicationRefreshInputRequestTypeDef",
    "StartApplicationRefreshOutputTypeDef",
    "StopApplicationInputRequestTypeDef",
    "StopApplicationOutputTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationSettingsInputRequestTypeDef",
    "UpdateApplicationSettingsOutputTypeDef",
)


class ApplicationCredentialTypeDef(TypedDict):
    DatabaseName: str
    CredentialType: Literal["ADMIN"]
    SecretId: str


ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "DiscoveryStatus": NotRequired[ApplicationDiscoveryStatusType],
        "Type": NotRequired[ApplicationTypeType],
        "Arn": NotRequired[str],
        "Tags": NotRequired[Dict[str, str]],
    },
)
ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[ApplicationTypeType],
        "Arn": NotRequired[str],
        "AppRegistryArn": NotRequired[str],
        "Status": NotRequired[ApplicationStatusType],
        "DiscoveryStatus": NotRequired[ApplicationDiscoveryStatusType],
        "Components": NotRequired[List[str]],
        "LastUpdated": NotRequired[datetime],
        "StatusMessage": NotRequired[str],
        "AssociatedApplicationArns": NotRequired[List[str]],
    },
)


class IpAddressMemberTypeDef(TypedDict):
    IpAddress: NotRequired[str]
    Primary: NotRequired[bool]
    AllocationType: NotRequired[AllocationTypeType]


class BackintConfigTypeDef(TypedDict):
    BackintMode: Literal["AWSBackup"]
    EnsureNoBackupInProcess: bool


class ComponentSummaryTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ComponentId: NotRequired[str]
    ComponentType: NotRequired[ComponentTypeType]
    Tags: NotRequired[Dict[str, str]]
    Arn: NotRequired[str]


class DatabaseConnectionTypeDef(TypedDict):
    DatabaseConnectionMethod: NotRequired[DatabaseConnectionMethodType]
    DatabaseArn: NotRequired[str]
    ConnectionIp: NotRequired[str]


class HostTypeDef(TypedDict):
    HostName: NotRequired[str]
    HostIp: NotRequired[str]
    EC2InstanceId: NotRequired[str]
    InstanceId: NotRequired[str]
    HostRole: NotRequired[HostRoleType]
    OsVersion: NotRequired[str]


class ResilienceTypeDef(TypedDict):
    HsrTier: NotRequired[str]
    HsrReplicationMode: NotRequired[ReplicationModeType]
    HsrOperationMode: NotRequired[OperationModeType]
    ClusterStatus: NotRequired[ClusterStatusType]
    EnqueueReplication: NotRequired[bool]


class DatabaseSummaryTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ComponentId: NotRequired[str]
    DatabaseId: NotRequired[str]
    DatabaseType: NotRequired[DatabaseTypeType]
    Arn: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]


class DeleteResourcePermissionInputRequestTypeDef(TypedDict):
    ResourceArn: str
    ActionType: NotRequired[Literal["RESTORE"]]
    SourceResourceArn: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeregisterApplicationInputRequestTypeDef(TypedDict):
    ApplicationId: str


class FilterTypeDef(TypedDict):
    Name: str
    Value: str
    Operator: FilterOperatorType


class GetApplicationInputRequestTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ApplicationArn: NotRequired[str]
    AppRegistryArn: NotRequired[str]


class GetComponentInputRequestTypeDef(TypedDict):
    ApplicationId: str
    ComponentId: str


class GetDatabaseInputRequestTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ComponentId: NotRequired[str]
    DatabaseId: NotRequired[str]
    DatabaseArn: NotRequired[str]


class GetOperationInputRequestTypeDef(TypedDict):
    OperationId: str


OperationTypeDef = TypedDict(
    "OperationTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[str],
        "Status": NotRequired[OperationStatusType],
        "StatusMessage": NotRequired[str],
        "Properties": NotRequired[Dict[str, str]],
        "ResourceType": NotRequired[str],
        "ResourceId": NotRequired[str],
        "ResourceArn": NotRequired[str],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)


class GetResourcePermissionInputRequestTypeDef(TypedDict):
    ResourceArn: str
    ActionType: NotRequired[Literal["RESTORE"]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListComponentsInputRequestTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDatabasesInputRequestTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ComponentId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ResourceTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]


class PutResourcePermissionInputRequestTypeDef(TypedDict):
    ActionType: Literal["RESTORE"]
    SourceResourceArn: str
    ResourceArn: str


class StartApplicationInputRequestTypeDef(TypedDict):
    ApplicationId: str


class StartApplicationRefreshInputRequestTypeDef(TypedDict):
    ApplicationId: str


class StopApplicationInputRequestTypeDef(TypedDict):
    ApplicationId: str
    StopConnectedEntity: NotRequired[Literal["DBMS"]]
    IncludeEc2InstanceShutdown: NotRequired[bool]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class DatabaseTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ComponentId: NotRequired[str]
    Credentials: NotRequired[List[ApplicationCredentialTypeDef]]
    DatabaseId: NotRequired[str]
    DatabaseName: NotRequired[str]
    DatabaseType: NotRequired[DatabaseTypeType]
    Arn: NotRequired[str]
    Status: NotRequired[DatabaseStatusType]
    PrimaryHost: NotRequired[str]
    SQLPort: NotRequired[int]
    LastUpdated: NotRequired[datetime]
    ConnectedComponentArns: NotRequired[List[str]]


class RegisterApplicationInputRequestTypeDef(TypedDict):
    ApplicationId: str
    ApplicationType: ApplicationTypeType
    Instances: Sequence[str]
    SapInstanceNumber: NotRequired[str]
    Sid: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    Credentials: NotRequired[Sequence[ApplicationCredentialTypeDef]]
    DatabaseArn: NotRequired[str]


class AssociatedHostTypeDef(TypedDict):
    Hostname: NotRequired[str]
    Ec2InstanceId: NotRequired[str]
    IpAddresses: NotRequired[List[IpAddressMemberTypeDef]]
    OsVersion: NotRequired[str]


class UpdateApplicationSettingsInputRequestTypeDef(TypedDict):
    ApplicationId: str
    CredentialsToAddOrUpdate: NotRequired[Sequence[ApplicationCredentialTypeDef]]
    CredentialsToRemove: NotRequired[Sequence[ApplicationCredentialTypeDef]]
    Backint: NotRequired[BackintConfigTypeDef]
    DatabaseArn: NotRequired[str]


class DeleteResourcePermissionOutputTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetApplicationOutputTypeDef(TypedDict):
    Application: ApplicationTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourcePermissionOutputTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListApplicationsOutputTypeDef(TypedDict):
    Applications: List[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListComponentsOutputTypeDef(TypedDict):
    Components: List[ComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDatabasesOutputTypeDef(TypedDict):
    Databases: List[DatabaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourcePermissionOutputTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterApplicationOutputTypeDef(TypedDict):
    Application: ApplicationTypeDef
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartApplicationOutputTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartApplicationRefreshOutputTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopApplicationOutputTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationSettingsOutputTypeDef(TypedDict):
    Message: str
    OperationIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListApplicationsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class ListOperationEventsInputRequestTypeDef(TypedDict):
    OperationId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class ListOperationsInputRequestTypeDef(TypedDict):
    ApplicationId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class GetOperationOutputTypeDef(TypedDict):
    Operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListOperationsOutputTypeDef(TypedDict):
    Operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListApplicationsInputListApplicationsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListComponentsInputListComponentsPaginateTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDatabasesInputListDatabasesPaginateTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ComponentId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOperationEventsInputListOperationEventsPaginateTypeDef(TypedDict):
    OperationId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOperationsInputListOperationsPaginateTypeDef(TypedDict):
    ApplicationId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class OperationEventTypeDef(TypedDict):
    Description: NotRequired[str]
    Resource: NotRequired[ResourceTypeDef]
    Status: NotRequired[OperationEventStatusType]
    StatusMessage: NotRequired[str]
    Timestamp: NotRequired[datetime]


class GetDatabaseOutputTypeDef(TypedDict):
    Database: DatabaseTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ComponentTypeDef(TypedDict):
    ComponentId: NotRequired[str]
    Sid: NotRequired[str]
    SystemNumber: NotRequired[str]
    ParentComponent: NotRequired[str]
    ChildComponents: NotRequired[List[str]]
    ApplicationId: NotRequired[str]
    ComponentType: NotRequired[ComponentTypeType]
    Status: NotRequired[ComponentStatusType]
    SapHostname: NotRequired[str]
    SapFeature: NotRequired[str]
    SapKernelVersion: NotRequired[str]
    HdbVersion: NotRequired[str]
    Resilience: NotRequired[ResilienceTypeDef]
    AssociatedHost: NotRequired[AssociatedHostTypeDef]
    Databases: NotRequired[List[str]]
    Hosts: NotRequired[List[HostTypeDef]]
    PrimaryHost: NotRequired[str]
    DatabaseConnection: NotRequired[DatabaseConnectionTypeDef]
    LastUpdated: NotRequired[datetime]
    Arn: NotRequired[str]


class ListOperationEventsOutputTypeDef(TypedDict):
    OperationEvents: List[OperationEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetComponentOutputTypeDef(TypedDict):
    Component: ComponentTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
