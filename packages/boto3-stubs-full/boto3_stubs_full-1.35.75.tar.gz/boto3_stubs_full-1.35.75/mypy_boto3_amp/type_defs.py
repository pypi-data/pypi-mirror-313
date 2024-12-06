"""
Type annotations for amp service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amp/type_defs/)

Usage::

    ```python
    from mypy_boto3_amp.type_defs import AlertManagerDefinitionStatusTypeDef

    data: AlertManagerDefinitionStatusTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlertManagerDefinitionStatusCodeType,
    LoggingConfigurationStatusCodeType,
    RuleGroupsNamespaceStatusCodeType,
    ScraperStatusCodeType,
    WorkspaceStatusCodeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AlertManagerDefinitionDescriptionTypeDef",
    "AlertManagerDefinitionStatusTypeDef",
    "AmpConfigurationTypeDef",
    "BlobTypeDef",
    "CreateAlertManagerDefinitionRequestRequestTypeDef",
    "CreateAlertManagerDefinitionResponseTypeDef",
    "CreateLoggingConfigurationRequestRequestTypeDef",
    "CreateLoggingConfigurationResponseTypeDef",
    "CreateRuleGroupsNamespaceRequestRequestTypeDef",
    "CreateRuleGroupsNamespaceResponseTypeDef",
    "CreateScraperRequestRequestTypeDef",
    "CreateScraperResponseTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "DeleteAlertManagerDefinitionRequestRequestTypeDef",
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    "DeleteRuleGroupsNamespaceRequestRequestTypeDef",
    "DeleteScraperRequestRequestTypeDef",
    "DeleteScraperResponseTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "DescribeAlertManagerDefinitionRequestRequestTypeDef",
    "DescribeAlertManagerDefinitionResponseTypeDef",
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    "DescribeLoggingConfigurationResponseTypeDef",
    "DescribeRuleGroupsNamespaceRequestRequestTypeDef",
    "DescribeRuleGroupsNamespaceResponseTypeDef",
    "DescribeScraperRequestRequestTypeDef",
    "DescribeScraperRequestScraperActiveWaitTypeDef",
    "DescribeScraperRequestScraperDeletedWaitTypeDef",
    "DescribeScraperResponseTypeDef",
    "DescribeWorkspaceRequestRequestTypeDef",
    "DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    "DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "DestinationTypeDef",
    "EksConfigurationOutputTypeDef",
    "EksConfigurationTypeDef",
    "EksConfigurationUnionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDefaultScraperConfigurationResponseTypeDef",
    "ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    "ListRuleGroupsNamespacesRequestRequestTypeDef",
    "ListRuleGroupsNamespacesResponseTypeDef",
    "ListScrapersRequestListScrapersPaginateTypeDef",
    "ListScrapersRequestRequestTypeDef",
    "ListScrapersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "ListWorkspacesResponseTypeDef",
    "LoggingConfigurationMetadataTypeDef",
    "LoggingConfigurationStatusTypeDef",
    "PaginatorConfigTypeDef",
    "PutAlertManagerDefinitionRequestRequestTypeDef",
    "PutAlertManagerDefinitionResponseTypeDef",
    "PutRuleGroupsNamespaceRequestRequestTypeDef",
    "PutRuleGroupsNamespaceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RuleGroupsNamespaceDescriptionTypeDef",
    "RuleGroupsNamespaceStatusTypeDef",
    "RuleGroupsNamespaceSummaryTypeDef",
    "ScrapeConfigurationOutputTypeDef",
    "ScrapeConfigurationTypeDef",
    "ScraperDescriptionTypeDef",
    "ScraperStatusTypeDef",
    "ScraperSummaryTypeDef",
    "SourceOutputTypeDef",
    "SourceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "UpdateScraperRequestRequestTypeDef",
    "UpdateScraperResponseTypeDef",
    "UpdateWorkspaceAliasRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "WorkspaceDescriptionTypeDef",
    "WorkspaceStatusTypeDef",
    "WorkspaceSummaryTypeDef",
)


class AlertManagerDefinitionStatusTypeDef(TypedDict):
    statusCode: AlertManagerDefinitionStatusCodeType
    statusReason: NotRequired[str]


class AmpConfigurationTypeDef(TypedDict):
    workspaceArn: str


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateLoggingConfigurationRequestRequestTypeDef(TypedDict):
    logGroupArn: str
    workspaceId: str
    clientToken: NotRequired[str]


class LoggingConfigurationStatusTypeDef(TypedDict):
    statusCode: LoggingConfigurationStatusCodeType
    statusReason: NotRequired[str]


class RuleGroupsNamespaceStatusTypeDef(TypedDict):
    statusCode: RuleGroupsNamespaceStatusCodeType
    statusReason: NotRequired[str]


class ScraperStatusTypeDef(TypedDict):
    statusCode: ScraperStatusCodeType


class CreateWorkspaceRequestRequestTypeDef(TypedDict):
    alias: NotRequired[str]
    clientToken: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class WorkspaceStatusTypeDef(TypedDict):
    statusCode: WorkspaceStatusCodeType


class DeleteAlertManagerDefinitionRequestRequestTypeDef(TypedDict):
    workspaceId: str
    clientToken: NotRequired[str]


class DeleteLoggingConfigurationRequestRequestTypeDef(TypedDict):
    workspaceId: str
    clientToken: NotRequired[str]


class DeleteRuleGroupsNamespaceRequestRequestTypeDef(TypedDict):
    name: str
    workspaceId: str
    clientToken: NotRequired[str]


class DeleteScraperRequestRequestTypeDef(TypedDict):
    scraperId: str
    clientToken: NotRequired[str]


class DeleteWorkspaceRequestRequestTypeDef(TypedDict):
    workspaceId: str
    clientToken: NotRequired[str]


class DescribeAlertManagerDefinitionRequestRequestTypeDef(TypedDict):
    workspaceId: str


class DescribeLoggingConfigurationRequestRequestTypeDef(TypedDict):
    workspaceId: str


class DescribeRuleGroupsNamespaceRequestRequestTypeDef(TypedDict):
    name: str
    workspaceId: str


class DescribeScraperRequestRequestTypeDef(TypedDict):
    scraperId: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeWorkspaceRequestRequestTypeDef(TypedDict):
    workspaceId: str


class EksConfigurationOutputTypeDef(TypedDict):
    clusterArn: str
    subnetIds: List[str]
    securityGroupIds: NotRequired[List[str]]


class EksConfigurationTypeDef(TypedDict):
    clusterArn: str
    subnetIds: Sequence[str]
    securityGroupIds: NotRequired[Sequence[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListRuleGroupsNamespacesRequestRequestTypeDef(TypedDict):
    workspaceId: str
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]


class ListScrapersRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Mapping[str, Sequence[str]]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListWorkspacesRequestRequestTypeDef(TypedDict):
    alias: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ScrapeConfigurationOutputTypeDef(TypedDict):
    configurationBlob: NotRequired[bytes]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateLoggingConfigurationRequestRequestTypeDef(TypedDict):
    logGroupArn: str
    workspaceId: str
    clientToken: NotRequired[str]


class UpdateWorkspaceAliasRequestRequestTypeDef(TypedDict):
    workspaceId: str
    alias: NotRequired[str]
    clientToken: NotRequired[str]


class AlertManagerDefinitionDescriptionTypeDef(TypedDict):
    createdAt: datetime
    data: bytes
    modifiedAt: datetime
    status: AlertManagerDefinitionStatusTypeDef


class DestinationTypeDef(TypedDict):
    ampConfiguration: NotRequired[AmpConfigurationTypeDef]


class CreateAlertManagerDefinitionRequestRequestTypeDef(TypedDict):
    data: BlobTypeDef
    workspaceId: str
    clientToken: NotRequired[str]


class CreateRuleGroupsNamespaceRequestRequestTypeDef(TypedDict):
    data: BlobTypeDef
    name: str
    workspaceId: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class PutAlertManagerDefinitionRequestRequestTypeDef(TypedDict):
    data: BlobTypeDef
    workspaceId: str
    clientToken: NotRequired[str]


class PutRuleGroupsNamespaceRequestRequestTypeDef(TypedDict):
    data: BlobTypeDef
    name: str
    workspaceId: str
    clientToken: NotRequired[str]


class ScrapeConfigurationTypeDef(TypedDict):
    configurationBlob: NotRequired[BlobTypeDef]


class CreateAlertManagerDefinitionResponseTypeDef(TypedDict):
    status: AlertManagerDefinitionStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetDefaultScraperConfigurationResponseTypeDef(TypedDict):
    configuration: bytes
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutAlertManagerDefinitionResponseTypeDef(TypedDict):
    status: AlertManagerDefinitionStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLoggingConfigurationResponseTypeDef(TypedDict):
    status: LoggingConfigurationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class LoggingConfigurationMetadataTypeDef(TypedDict):
    createdAt: datetime
    logGroupArn: str
    modifiedAt: datetime
    status: LoggingConfigurationStatusTypeDef
    workspace: str


class UpdateLoggingConfigurationResponseTypeDef(TypedDict):
    status: LoggingConfigurationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRuleGroupsNamespaceResponseTypeDef(TypedDict):
    arn: str
    name: str
    status: RuleGroupsNamespaceStatusTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutRuleGroupsNamespaceResponseTypeDef(TypedDict):
    arn: str
    name: str
    status: RuleGroupsNamespaceStatusTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class RuleGroupsNamespaceDescriptionTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    data: bytes
    modifiedAt: datetime
    name: str
    status: RuleGroupsNamespaceStatusTypeDef
    tags: NotRequired[Dict[str, str]]


class RuleGroupsNamespaceSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    modifiedAt: datetime
    name: str
    status: RuleGroupsNamespaceStatusTypeDef
    tags: NotRequired[Dict[str, str]]


class CreateScraperResponseTypeDef(TypedDict):
    arn: str
    scraperId: str
    status: ScraperStatusTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteScraperResponseTypeDef(TypedDict):
    scraperId: str
    status: ScraperStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScraperResponseTypeDef(TypedDict):
    arn: str
    scraperId: str
    status: ScraperStatusTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkspaceResponseTypeDef(TypedDict):
    arn: str
    kmsKeyArn: str
    status: WorkspaceStatusTypeDef
    tags: Dict[str, str]
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class WorkspaceDescriptionTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    status: WorkspaceStatusTypeDef
    workspaceId: str
    alias: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    prometheusEndpoint: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class WorkspaceSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    status: WorkspaceStatusTypeDef
    workspaceId: str
    alias: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class DescribeScraperRequestScraperActiveWaitTypeDef(TypedDict):
    scraperId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeScraperRequestScraperDeletedWaitTypeDef(TypedDict):
    scraperId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef(TypedDict):
    workspaceId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef(TypedDict):
    workspaceId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class SourceOutputTypeDef(TypedDict):
    eksConfiguration: NotRequired[EksConfigurationOutputTypeDef]


EksConfigurationUnionTypeDef = Union[EksConfigurationTypeDef, EksConfigurationOutputTypeDef]


class ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef(TypedDict):
    workspaceId: str
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScrapersRequestListScrapersPaginateTypeDef(TypedDict):
    filters: NotRequired[Mapping[str, Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspacesRequestListWorkspacesPaginateTypeDef(TypedDict):
    alias: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAlertManagerDefinitionResponseTypeDef(TypedDict):
    alertManagerDefinition: AlertManagerDefinitionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScraperRequestRequestTypeDef(TypedDict):
    scraperId: str
    alias: NotRequired[str]
    clientToken: NotRequired[str]
    destination: NotRequired[DestinationTypeDef]
    scrapeConfiguration: NotRequired[ScrapeConfigurationTypeDef]


class DescribeLoggingConfigurationResponseTypeDef(TypedDict):
    loggingConfiguration: LoggingConfigurationMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRuleGroupsNamespaceResponseTypeDef(TypedDict):
    ruleGroupsNamespace: RuleGroupsNamespaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRuleGroupsNamespacesResponseTypeDef(TypedDict):
    ruleGroupsNamespaces: List[RuleGroupsNamespaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListWorkspacesResponseTypeDef(TypedDict):
    workspaces: List[WorkspaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ScraperDescriptionTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    destination: DestinationTypeDef
    lastModifiedAt: datetime
    roleArn: str
    scrapeConfiguration: ScrapeConfigurationOutputTypeDef
    scraperId: str
    source: SourceOutputTypeDef
    status: ScraperStatusTypeDef
    alias: NotRequired[str]
    statusReason: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ScraperSummaryTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    destination: DestinationTypeDef
    lastModifiedAt: datetime
    roleArn: str
    scraperId: str
    source: SourceOutputTypeDef
    status: ScraperStatusTypeDef
    alias: NotRequired[str]
    statusReason: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class SourceTypeDef(TypedDict):
    eksConfiguration: NotRequired[EksConfigurationUnionTypeDef]


class DescribeScraperResponseTypeDef(TypedDict):
    scraper: ScraperDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListScrapersResponseTypeDef(TypedDict):
    scrapers: List[ScraperSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateScraperRequestRequestTypeDef(TypedDict):
    destination: DestinationTypeDef
    scrapeConfiguration: ScrapeConfigurationTypeDef
    source: SourceTypeDef
    alias: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
