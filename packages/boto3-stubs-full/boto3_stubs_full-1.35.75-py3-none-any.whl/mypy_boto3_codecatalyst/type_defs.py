"""
Type annotations for codecatalyst service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/type_defs/)

Usage::

    ```python
    from mypy_boto3_codecatalyst.type_defs import AccessTokenSummaryTypeDef

    data: AccessTokenSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ComparisonOperatorType,
    DevEnvironmentSessionTypeType,
    DevEnvironmentStatusType,
    FilterKeyType,
    InstanceTypeType,
    OperationTypeType,
    UserTypeType,
    WorkflowRunModeType,
    WorkflowRunStatusType,
    WorkflowStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccessTokenSummaryTypeDef",
    "CreateAccessTokenRequestRequestTypeDef",
    "CreateAccessTokenResponseTypeDef",
    "CreateDevEnvironmentRequestRequestTypeDef",
    "CreateDevEnvironmentResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateSourceRepositoryBranchRequestRequestTypeDef",
    "CreateSourceRepositoryBranchResponseTypeDef",
    "CreateSourceRepositoryRequestRequestTypeDef",
    "CreateSourceRepositoryResponseTypeDef",
    "DeleteAccessTokenRequestRequestTypeDef",
    "DeleteDevEnvironmentRequestRequestTypeDef",
    "DeleteDevEnvironmentResponseTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteProjectResponseTypeDef",
    "DeleteSourceRepositoryRequestRequestTypeDef",
    "DeleteSourceRepositoryResponseTypeDef",
    "DeleteSpaceRequestRequestTypeDef",
    "DeleteSpaceResponseTypeDef",
    "DevEnvironmentAccessDetailsTypeDef",
    "DevEnvironmentRepositorySummaryTypeDef",
    "DevEnvironmentSessionConfigurationTypeDef",
    "DevEnvironmentSessionSummaryTypeDef",
    "DevEnvironmentSummaryTypeDef",
    "EmailAddressTypeDef",
    "EventLogEntryTypeDef",
    "EventPayloadTypeDef",
    "ExecuteCommandSessionConfigurationTypeDef",
    "FilterTypeDef",
    "GetDevEnvironmentRequestRequestTypeDef",
    "GetDevEnvironmentResponseTypeDef",
    "GetProjectRequestRequestTypeDef",
    "GetProjectResponseTypeDef",
    "GetSourceRepositoryCloneUrlsRequestRequestTypeDef",
    "GetSourceRepositoryCloneUrlsResponseTypeDef",
    "GetSourceRepositoryRequestRequestTypeDef",
    "GetSourceRepositoryResponseTypeDef",
    "GetSpaceRequestRequestTypeDef",
    "GetSpaceResponseTypeDef",
    "GetSubscriptionRequestRequestTypeDef",
    "GetSubscriptionResponseTypeDef",
    "GetUserDetailsRequestRequestTypeDef",
    "GetUserDetailsResponseTypeDef",
    "GetWorkflowRequestRequestTypeDef",
    "GetWorkflowResponseTypeDef",
    "GetWorkflowRunRequestRequestTypeDef",
    "GetWorkflowRunResponseTypeDef",
    "IdeConfigurationTypeDef",
    "IdeTypeDef",
    "ListAccessTokensRequestListAccessTokensPaginateTypeDef",
    "ListAccessTokensRequestRequestTypeDef",
    "ListAccessTokensResponseTypeDef",
    "ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef",
    "ListDevEnvironmentSessionsRequestRequestTypeDef",
    "ListDevEnvironmentSessionsResponseTypeDef",
    "ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef",
    "ListDevEnvironmentsRequestRequestTypeDef",
    "ListDevEnvironmentsResponseTypeDef",
    "ListEventLogsRequestListEventLogsPaginateTypeDef",
    "ListEventLogsRequestRequestTypeDef",
    "ListEventLogsResponseTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListSourceRepositoriesItemTypeDef",
    "ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef",
    "ListSourceRepositoriesRequestRequestTypeDef",
    "ListSourceRepositoriesResponseTypeDef",
    "ListSourceRepositoryBranchesItemTypeDef",
    "ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef",
    "ListSourceRepositoryBranchesRequestRequestTypeDef",
    "ListSourceRepositoryBranchesResponseTypeDef",
    "ListSpacesRequestListSpacesPaginateTypeDef",
    "ListSpacesRequestRequestTypeDef",
    "ListSpacesResponseTypeDef",
    "ListWorkflowRunsRequestListWorkflowRunsPaginateTypeDef",
    "ListWorkflowRunsRequestRequestTypeDef",
    "ListWorkflowRunsResponseTypeDef",
    "ListWorkflowsRequestListWorkflowsPaginateTypeDef",
    "ListWorkflowsRequestRequestTypeDef",
    "ListWorkflowsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PersistentStorageConfigurationTypeDef",
    "PersistentStorageTypeDef",
    "ProjectInformationTypeDef",
    "ProjectListFilterTypeDef",
    "ProjectSummaryTypeDef",
    "RepositoryInputTypeDef",
    "ResponseMetadataTypeDef",
    "SpaceSummaryTypeDef",
    "StartDevEnvironmentRequestRequestTypeDef",
    "StartDevEnvironmentResponseTypeDef",
    "StartDevEnvironmentSessionRequestRequestTypeDef",
    "StartDevEnvironmentSessionResponseTypeDef",
    "StartWorkflowRunRequestRequestTypeDef",
    "StartWorkflowRunResponseTypeDef",
    "StopDevEnvironmentRequestRequestTypeDef",
    "StopDevEnvironmentResponseTypeDef",
    "StopDevEnvironmentSessionRequestRequestTypeDef",
    "StopDevEnvironmentSessionResponseTypeDef",
    "TimestampTypeDef",
    "UpdateDevEnvironmentRequestRequestTypeDef",
    "UpdateDevEnvironmentResponseTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateProjectResponseTypeDef",
    "UpdateSpaceRequestRequestTypeDef",
    "UpdateSpaceResponseTypeDef",
    "UserIdentityTypeDef",
    "VerifySessionResponseTypeDef",
    "WorkflowDefinitionSummaryTypeDef",
    "WorkflowDefinitionTypeDef",
    "WorkflowRunSummaryTypeDef",
    "WorkflowSummaryTypeDef",
)

AccessTokenSummaryTypeDef = TypedDict(
    "AccessTokenSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "expiresTime": NotRequired[datetime],
    },
)
TimestampTypeDef = Union[datetime, str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class IdeConfigurationTypeDef(TypedDict):
    runtime: NotRequired[str]
    name: NotRequired[str]


class PersistentStorageConfigurationTypeDef(TypedDict):
    sizeInGiB: int


class RepositoryInputTypeDef(TypedDict):
    repositoryName: str
    branchName: NotRequired[str]


class CreateProjectRequestRequestTypeDef(TypedDict):
    spaceName: str
    displayName: str
    description: NotRequired[str]


class CreateSourceRepositoryBranchRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    sourceRepositoryName: str
    name: str
    headCommitId: NotRequired[str]


class CreateSourceRepositoryRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    name: str
    description: NotRequired[str]


DeleteAccessTokenRequestRequestTypeDef = TypedDict(
    "DeleteAccessTokenRequestRequestTypeDef",
    {
        "id": str,
    },
)
DeleteDevEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)


class DeleteProjectRequestRequestTypeDef(TypedDict):
    spaceName: str
    name: str


class DeleteSourceRepositoryRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    name: str


class DeleteSpaceRequestRequestTypeDef(TypedDict):
    name: str


class DevEnvironmentAccessDetailsTypeDef(TypedDict):
    streamUrl: str
    tokenValue: str


class DevEnvironmentRepositorySummaryTypeDef(TypedDict):
    repositoryName: str
    branchName: NotRequired[str]


class ExecuteCommandSessionConfigurationTypeDef(TypedDict):
    command: str
    arguments: NotRequired[Sequence[str]]


DevEnvironmentSessionSummaryTypeDef = TypedDict(
    "DevEnvironmentSessionSummaryTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "devEnvironmentId": str,
        "startedTime": datetime,
        "id": str,
    },
)


class IdeTypeDef(TypedDict):
    runtime: NotRequired[str]
    name: NotRequired[str]


class PersistentStorageTypeDef(TypedDict):
    sizeInGiB: int


class EmailAddressTypeDef(TypedDict):
    email: NotRequired[str]
    verified: NotRequired[bool]


class EventPayloadTypeDef(TypedDict):
    contentType: NotRequired[str]
    data: NotRequired[str]


class ProjectInformationTypeDef(TypedDict):
    name: NotRequired[str]
    projectId: NotRequired[str]


class UserIdentityTypeDef(TypedDict):
    userType: UserTypeType
    principalId: str
    userName: NotRequired[str]
    awsAccountId: NotRequired[str]


class FilterTypeDef(TypedDict):
    key: str
    values: Sequence[str]
    comparisonOperator: NotRequired[str]


GetDevEnvironmentRequestRequestTypeDef = TypedDict(
    "GetDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)


class GetProjectRequestRequestTypeDef(TypedDict):
    spaceName: str
    name: str


class GetSourceRepositoryCloneUrlsRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    sourceRepositoryName: str


class GetSourceRepositoryRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    name: str


class GetSpaceRequestRequestTypeDef(TypedDict):
    name: str


class GetSubscriptionRequestRequestTypeDef(TypedDict):
    spaceName: str


GetUserDetailsRequestRequestTypeDef = TypedDict(
    "GetUserDetailsRequestRequestTypeDef",
    {
        "id": NotRequired[str],
        "userName": NotRequired[str],
    },
)
GetWorkflowRequestRequestTypeDef = TypedDict(
    "GetWorkflowRequestRequestTypeDef",
    {
        "spaceName": str,
        "id": str,
        "projectName": str,
    },
)


class WorkflowDefinitionTypeDef(TypedDict):
    path: str


GetWorkflowRunRequestRequestTypeDef = TypedDict(
    "GetWorkflowRunRequestRequestTypeDef",
    {
        "spaceName": str,
        "id": str,
        "projectName": str,
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAccessTokensRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDevEnvironmentSessionsRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    devEnvironmentId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ProjectListFilterTypeDef(TypedDict):
    key: FilterKeyType
    values: Sequence[str]
    comparisonOperator: NotRequired[ComparisonOperatorType]


class ProjectSummaryTypeDef(TypedDict):
    name: str
    displayName: NotRequired[str]
    description: NotRequired[str]


ListSourceRepositoriesItemTypeDef = TypedDict(
    "ListSourceRepositoriesItemTypeDef",
    {
        "id": str,
        "name": str,
        "lastUpdatedTime": datetime,
        "createdTime": datetime,
        "description": NotRequired[str],
    },
)


class ListSourceRepositoriesRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListSourceRepositoryBranchesItemTypeDef(TypedDict):
    ref: NotRequired[str]
    name: NotRequired[str]
    lastUpdatedTime: NotRequired[datetime]
    headCommitId: NotRequired[str]


class ListSourceRepositoryBranchesRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    sourceRepositoryName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListSpacesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]


class SpaceSummaryTypeDef(TypedDict):
    name: str
    regionName: str
    displayName: NotRequired[str]
    description: NotRequired[str]


class ListWorkflowRunsRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    workflowId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortBy: NotRequired[Sequence[Mapping[str, Any]]]


WorkflowRunSummaryTypeDef = TypedDict(
    "WorkflowRunSummaryTypeDef",
    {
        "id": str,
        "workflowId": str,
        "workflowName": str,
        "status": WorkflowRunStatusType,
        "startTime": datetime,
        "lastUpdatedTime": datetime,
        "statusReasons": NotRequired[List[Dict[str, Any]]],
        "endTime": NotRequired[datetime],
    },
)


class ListWorkflowsRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortBy: NotRequired[Sequence[Mapping[str, Any]]]


class StartWorkflowRunRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    workflowId: str
    clientToken: NotRequired[str]


StopDevEnvironmentRequestRequestTypeDef = TypedDict(
    "StopDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)
StopDevEnvironmentSessionRequestRequestTypeDef = TypedDict(
    "StopDevEnvironmentSessionRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "sessionId": str,
    },
)


class UpdateProjectRequestRequestTypeDef(TypedDict):
    spaceName: str
    name: str
    description: NotRequired[str]


class UpdateSpaceRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]


class WorkflowDefinitionSummaryTypeDef(TypedDict):
    path: str


class CreateAccessTokenRequestRequestTypeDef(TypedDict):
    name: str
    expiresTime: NotRequired[TimestampTypeDef]


class ListEventLogsRequestRequestTypeDef(TypedDict):
    spaceName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    eventName: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class CreateAccessTokenResponseTypeDef(TypedDict):
    secret: str
    name: str
    expiresTime: datetime
    accessTokenId: str
    ResponseMetadata: ResponseMetadataTypeDef


CreateDevEnvironmentResponseTypeDef = TypedDict(
    "CreateDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "vpcConnectionName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateProjectResponseTypeDef(TypedDict):
    spaceName: str
    name: str
    displayName: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSourceRepositoryBranchResponseTypeDef(TypedDict):
    ref: str
    name: str
    lastUpdatedTime: datetime
    headCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSourceRepositoryResponseTypeDef(TypedDict):
    spaceName: str
    projectName: str
    name: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


DeleteDevEnvironmentResponseTypeDef = TypedDict(
    "DeleteDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DeleteProjectResponseTypeDef(TypedDict):
    spaceName: str
    name: str
    displayName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSourceRepositoryResponseTypeDef(TypedDict):
    spaceName: str
    projectName: str
    name: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSpaceResponseTypeDef(TypedDict):
    name: str
    displayName: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetProjectResponseTypeDef(TypedDict):
    spaceName: str
    name: str
    displayName: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSourceRepositoryCloneUrlsResponseTypeDef(TypedDict):
    https: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSourceRepositoryResponseTypeDef(TypedDict):
    spaceName: str
    projectName: str
    name: str
    description: str
    lastUpdatedTime: datetime
    createdTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetSpaceResponseTypeDef(TypedDict):
    name: str
    regionName: str
    displayName: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSubscriptionResponseTypeDef(TypedDict):
    subscriptionType: str
    awsAccountName: str
    pendingSubscriptionType: str
    pendingSubscriptionStartTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


GetWorkflowRunResponseTypeDef = TypedDict(
    "GetWorkflowRunResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "workflowId": str,
        "status": WorkflowRunStatusType,
        "statusReasons": List[Dict[str, Any]],
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListAccessTokensResponseTypeDef(TypedDict):
    items: List[AccessTokenSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


StartDevEnvironmentResponseTypeDef = TypedDict(
    "StartDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "status": DevEnvironmentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartWorkflowRunResponseTypeDef = TypedDict(
    "StartWorkflowRunResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "workflowId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StopDevEnvironmentResponseTypeDef = TypedDict(
    "StopDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "status": DevEnvironmentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StopDevEnvironmentSessionResponseTypeDef = TypedDict(
    "StopDevEnvironmentSessionResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateProjectResponseTypeDef(TypedDict):
    spaceName: str
    name: str
    displayName: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSpaceResponseTypeDef(TypedDict):
    name: str
    displayName: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class VerifySessionResponseTypeDef(TypedDict):
    identity: str
    ResponseMetadata: ResponseMetadataTypeDef


StartDevEnvironmentRequestRequestTypeDef = TypedDict(
    "StartDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "ides": NotRequired[Sequence[IdeConfigurationTypeDef]],
        "instanceType": NotRequired[InstanceTypeType],
        "inactivityTimeoutMinutes": NotRequired[int],
    },
)
UpdateDevEnvironmentRequestRequestTypeDef = TypedDict(
    "UpdateDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "alias": NotRequired[str],
        "ides": NotRequired[Sequence[IdeConfigurationTypeDef]],
        "instanceType": NotRequired[InstanceTypeType],
        "inactivityTimeoutMinutes": NotRequired[int],
        "clientToken": NotRequired[str],
    },
)
UpdateDevEnvironmentResponseTypeDef = TypedDict(
    "UpdateDevEnvironmentResponseTypeDef",
    {
        "id": str,
        "spaceName": str,
        "projectName": str,
        "alias": str,
        "ides": List[IdeConfigurationTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
        "clientToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateDevEnvironmentRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: str
    instanceType: InstanceTypeType
    persistentStorage: PersistentStorageConfigurationTypeDef
    repositories: NotRequired[Sequence[RepositoryInputTypeDef]]
    clientToken: NotRequired[str]
    alias: NotRequired[str]
    ides: NotRequired[Sequence[IdeConfigurationTypeDef]]
    inactivityTimeoutMinutes: NotRequired[int]
    vpcConnectionName: NotRequired[str]


StartDevEnvironmentSessionResponseTypeDef = TypedDict(
    "StartDevEnvironmentSessionResponseTypeDef",
    {
        "accessDetails": DevEnvironmentAccessDetailsTypeDef,
        "sessionId": str,
        "spaceName": str,
        "projectName": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DevEnvironmentSessionConfigurationTypeDef(TypedDict):
    sessionType: DevEnvironmentSessionTypeType
    executeCommandSessionConfiguration: NotRequired[ExecuteCommandSessionConfigurationTypeDef]


class ListDevEnvironmentSessionsResponseTypeDef(TypedDict):
    items: List[DevEnvironmentSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


DevEnvironmentSummaryTypeDef = TypedDict(
    "DevEnvironmentSummaryTypeDef",
    {
        "id": str,
        "lastUpdatedTime": datetime,
        "creatorId": str,
        "status": DevEnvironmentStatusType,
        "repositories": List[DevEnvironmentRepositorySummaryTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
        "persistentStorage": PersistentStorageTypeDef,
        "spaceName": NotRequired[str],
        "projectName": NotRequired[str],
        "statusReason": NotRequired[str],
        "alias": NotRequired[str],
        "ides": NotRequired[List[IdeTypeDef]],
        "vpcConnectionName": NotRequired[str],
    },
)
GetDevEnvironmentResponseTypeDef = TypedDict(
    "GetDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "lastUpdatedTime": datetime,
        "creatorId": str,
        "status": DevEnvironmentStatusType,
        "statusReason": str,
        "repositories": List[DevEnvironmentRepositorySummaryTypeDef],
        "alias": str,
        "ides": List[IdeTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
        "persistentStorage": PersistentStorageTypeDef,
        "vpcConnectionName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetUserDetailsResponseTypeDef(TypedDict):
    userId: str
    userName: str
    displayName: str
    primaryEmail: EmailAddressTypeDef
    version: str
    ResponseMetadata: ResponseMetadataTypeDef


EventLogEntryTypeDef = TypedDict(
    "EventLogEntryTypeDef",
    {
        "id": str,
        "eventName": str,
        "eventType": str,
        "eventCategory": str,
        "eventSource": str,
        "eventTime": datetime,
        "operationType": OperationTypeType,
        "userIdentity": UserIdentityTypeDef,
        "projectInformation": NotRequired[ProjectInformationTypeDef],
        "requestId": NotRequired[str],
        "requestPayload": NotRequired[EventPayloadTypeDef],
        "responsePayload": NotRequired[EventPayloadTypeDef],
        "errorCode": NotRequired[str],
        "sourceIpAddress": NotRequired[str],
        "userAgent": NotRequired[str],
    },
)


class ListDevEnvironmentsRequestRequestTypeDef(TypedDict):
    spaceName: str
    projectName: NotRequired[str]
    filters: NotRequired[Sequence[FilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


GetWorkflowResponseTypeDef = TypedDict(
    "GetWorkflowResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "name": str,
        "sourceRepositoryName": str,
        "sourceBranchName": str,
        "definition": WorkflowDefinitionTypeDef,
        "createdTime": datetime,
        "lastUpdatedTime": datetime,
        "runMode": WorkflowRunModeType,
        "status": WorkflowStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListAccessTokensRequestListAccessTokensPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef(TypedDict):
    spaceName: str
    projectName: str
    devEnvironmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef(TypedDict):
    spaceName: str
    projectName: NotRequired[str]
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEventLogsRequestListEventLogsPaginateTypeDef(TypedDict):
    spaceName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    eventName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef(TypedDict):
    spaceName: str
    projectName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef(TypedDict):
    spaceName: str
    projectName: str
    sourceRepositoryName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSpacesRequestListSpacesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkflowRunsRequestListWorkflowRunsPaginateTypeDef(TypedDict):
    spaceName: str
    projectName: str
    workflowId: NotRequired[str]
    sortBy: NotRequired[Sequence[Mapping[str, Any]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkflowsRequestListWorkflowsPaginateTypeDef(TypedDict):
    spaceName: str
    projectName: str
    sortBy: NotRequired[Sequence[Mapping[str, Any]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectsRequestListProjectsPaginateTypeDef(TypedDict):
    spaceName: str
    filters: NotRequired[Sequence[ProjectListFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectsRequestRequestTypeDef(TypedDict):
    spaceName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[ProjectListFilterTypeDef]]


class ListProjectsResponseTypeDef(TypedDict):
    items: List[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSourceRepositoriesResponseTypeDef(TypedDict):
    items: List[ListSourceRepositoriesItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSourceRepositoryBranchesResponseTypeDef(TypedDict):
    items: List[ListSourceRepositoryBranchesItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSpacesResponseTypeDef(TypedDict):
    items: List[SpaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWorkflowRunsResponseTypeDef(TypedDict):
    items: List[WorkflowRunSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


WorkflowSummaryTypeDef = TypedDict(
    "WorkflowSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "sourceRepositoryName": str,
        "sourceBranchName": str,
        "definition": WorkflowDefinitionSummaryTypeDef,
        "createdTime": datetime,
        "lastUpdatedTime": datetime,
        "runMode": WorkflowRunModeType,
        "status": WorkflowStatusType,
    },
)
StartDevEnvironmentSessionRequestRequestTypeDef = TypedDict(
    "StartDevEnvironmentSessionRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "sessionConfiguration": DevEnvironmentSessionConfigurationTypeDef,
    },
)


class ListDevEnvironmentsResponseTypeDef(TypedDict):
    items: List[DevEnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListEventLogsResponseTypeDef(TypedDict):
    items: List[EventLogEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWorkflowsResponseTypeDef(TypedDict):
    items: List[WorkflowSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
