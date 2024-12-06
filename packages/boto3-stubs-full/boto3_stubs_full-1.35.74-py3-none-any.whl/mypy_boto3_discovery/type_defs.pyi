"""
Type annotations for discovery service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_discovery/type_defs/)

Usage::

    ```python
    from mypy_boto3_discovery.type_defs import AgentConfigurationStatusTypeDef

    data: AgentConfigurationStatusTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AgentStatusType,
    BatchDeleteConfigurationTaskStatusType,
    BatchDeleteImportDataErrorCodeType,
    ConfigurationItemTypeType,
    ContinuousExportStatusType,
    DeleteAgentErrorCodeType,
    ExportStatusType,
    FileClassificationType,
    ImportStatusType,
    ImportTaskFilterNameType,
    OfferingClassType,
    OrderStringType,
    PurchasingOptionType,
    TenancyType,
    TermLengthType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AgentConfigurationStatusTypeDef",
    "AgentInfoTypeDef",
    "AgentNetworkInfoTypeDef",
    "AssociateConfigurationItemsToApplicationRequestRequestTypeDef",
    "BatchDeleteAgentErrorTypeDef",
    "BatchDeleteAgentsRequestRequestTypeDef",
    "BatchDeleteAgentsResponseTypeDef",
    "BatchDeleteConfigurationTaskTypeDef",
    "BatchDeleteImportDataErrorTypeDef",
    "BatchDeleteImportDataRequestRequestTypeDef",
    "BatchDeleteImportDataResponseTypeDef",
    "ConfigurationTagTypeDef",
    "ContinuousExportDescriptionTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateTagsRequestRequestTypeDef",
    "CustomerAgentInfoTypeDef",
    "CustomerAgentlessCollectorInfoTypeDef",
    "CustomerConnectorInfoTypeDef",
    "CustomerMeCollectorInfoTypeDef",
    "DeleteAgentTypeDef",
    "DeleteApplicationsRequestRequestTypeDef",
    "DeleteTagsRequestRequestTypeDef",
    "DeletionWarningTypeDef",
    "DescribeAgentsRequestDescribeAgentsPaginateTypeDef",
    "DescribeAgentsRequestRequestTypeDef",
    "DescribeAgentsResponseTypeDef",
    "DescribeBatchDeleteConfigurationTaskRequestRequestTypeDef",
    "DescribeBatchDeleteConfigurationTaskResponseTypeDef",
    "DescribeConfigurationsRequestRequestTypeDef",
    "DescribeConfigurationsResponseTypeDef",
    "DescribeContinuousExportsRequestDescribeContinuousExportsPaginateTypeDef",
    "DescribeContinuousExportsRequestRequestTypeDef",
    "DescribeContinuousExportsResponseTypeDef",
    "DescribeExportConfigurationsRequestDescribeExportConfigurationsPaginateTypeDef",
    "DescribeExportConfigurationsRequestRequestTypeDef",
    "DescribeExportConfigurationsResponseTypeDef",
    "DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef",
    "DescribeExportTasksRequestRequestTypeDef",
    "DescribeExportTasksResponseTypeDef",
    "DescribeImportTasksRequestDescribeImportTasksPaginateTypeDef",
    "DescribeImportTasksRequestRequestTypeDef",
    "DescribeImportTasksResponseTypeDef",
    "DescribeTagsRequestDescribeTagsPaginateTypeDef",
    "DescribeTagsRequestRequestTypeDef",
    "DescribeTagsResponseTypeDef",
    "DisassociateConfigurationItemsFromApplicationRequestRequestTypeDef",
    "Ec2RecommendationsExportPreferencesTypeDef",
    "ExportConfigurationsResponseTypeDef",
    "ExportFilterTypeDef",
    "ExportInfoTypeDef",
    "ExportPreferencesTypeDef",
    "FailedConfigurationTypeDef",
    "FilterTypeDef",
    "GetDiscoverySummaryResponseTypeDef",
    "ImportTaskFilterTypeDef",
    "ImportTaskTypeDef",
    "ListConfigurationsRequestListConfigurationsPaginateTypeDef",
    "ListConfigurationsRequestRequestTypeDef",
    "ListConfigurationsResponseTypeDef",
    "ListServerNeighborsRequestRequestTypeDef",
    "ListServerNeighborsResponseTypeDef",
    "NeighborConnectionDetailTypeDef",
    "OrderByElementTypeDef",
    "PaginatorConfigTypeDef",
    "ReservedInstanceOptionsTypeDef",
    "ResponseMetadataTypeDef",
    "StartBatchDeleteConfigurationTaskRequestRequestTypeDef",
    "StartBatchDeleteConfigurationTaskResponseTypeDef",
    "StartContinuousExportResponseTypeDef",
    "StartDataCollectionByAgentIdsRequestRequestTypeDef",
    "StartDataCollectionByAgentIdsResponseTypeDef",
    "StartExportTaskRequestRequestTypeDef",
    "StartExportTaskResponseTypeDef",
    "StartImportTaskRequestRequestTypeDef",
    "StartImportTaskResponseTypeDef",
    "StopContinuousExportRequestRequestTypeDef",
    "StopContinuousExportResponseTypeDef",
    "StopDataCollectionByAgentIdsRequestRequestTypeDef",
    "StopDataCollectionByAgentIdsResponseTypeDef",
    "TagFilterTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UsageMetricBasisTypeDef",
)

class AgentConfigurationStatusTypeDef(TypedDict):
    agentId: NotRequired[str]
    operationSucceeded: NotRequired[bool]
    description: NotRequired[str]

class AgentNetworkInfoTypeDef(TypedDict):
    ipAddress: NotRequired[str]
    macAddress: NotRequired[str]

class AssociateConfigurationItemsToApplicationRequestRequestTypeDef(TypedDict):
    applicationConfigurationId: str
    configurationIds: Sequence[str]

class BatchDeleteAgentErrorTypeDef(TypedDict):
    agentId: str
    errorMessage: str
    errorCode: DeleteAgentErrorCodeType

class DeleteAgentTypeDef(TypedDict):
    agentId: str
    force: NotRequired[bool]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeletionWarningTypeDef(TypedDict):
    configurationId: NotRequired[str]
    warningCode: NotRequired[int]
    warningText: NotRequired[str]

class FailedConfigurationTypeDef(TypedDict):
    configurationId: NotRequired[str]
    errorStatusCode: NotRequired[int]
    errorMessage: NotRequired[str]

class BatchDeleteImportDataErrorTypeDef(TypedDict):
    importTaskId: NotRequired[str]
    errorCode: NotRequired[BatchDeleteImportDataErrorCodeType]
    errorDescription: NotRequired[str]

class BatchDeleteImportDataRequestRequestTypeDef(TypedDict):
    importTaskIds: Sequence[str]
    deleteHistory: NotRequired[bool]

class ConfigurationTagTypeDef(TypedDict):
    configurationType: NotRequired[ConfigurationItemTypeType]
    configurationId: NotRequired[str]
    key: NotRequired[str]
    value: NotRequired[str]
    timeOfCreation: NotRequired[datetime]

class ContinuousExportDescriptionTypeDef(TypedDict):
    exportId: NotRequired[str]
    status: NotRequired[ContinuousExportStatusType]
    statusDetail: NotRequired[str]
    s3Bucket: NotRequired[str]
    startTime: NotRequired[datetime]
    stopTime: NotRequired[datetime]
    dataSource: NotRequired[Literal["AGENT"]]
    schemaStorageConfig: NotRequired[Dict[str, str]]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    wave: NotRequired[str]

class TagTypeDef(TypedDict):
    key: str
    value: str

class CustomerAgentInfoTypeDef(TypedDict):
    activeAgents: int
    healthyAgents: int
    blackListedAgents: int
    shutdownAgents: int
    unhealthyAgents: int
    totalAgents: int
    unknownAgents: int

class CustomerAgentlessCollectorInfoTypeDef(TypedDict):
    activeAgentlessCollectors: int
    healthyAgentlessCollectors: int
    denyListedAgentlessCollectors: int
    shutdownAgentlessCollectors: int
    unhealthyAgentlessCollectors: int
    totalAgentlessCollectors: int
    unknownAgentlessCollectors: int

class CustomerConnectorInfoTypeDef(TypedDict):
    activeConnectors: int
    healthyConnectors: int
    blackListedConnectors: int
    shutdownConnectors: int
    unhealthyConnectors: int
    totalConnectors: int
    unknownConnectors: int

class CustomerMeCollectorInfoTypeDef(TypedDict):
    activeMeCollectors: int
    healthyMeCollectors: int
    denyListedMeCollectors: int
    shutdownMeCollectors: int
    unhealthyMeCollectors: int
    totalMeCollectors: int
    unknownMeCollectors: int

class DeleteApplicationsRequestRequestTypeDef(TypedDict):
    configurationIds: Sequence[str]

class FilterTypeDef(TypedDict):
    name: str
    values: Sequence[str]
    condition: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeBatchDeleteConfigurationTaskRequestRequestTypeDef(TypedDict):
    taskId: str

class DescribeConfigurationsRequestRequestTypeDef(TypedDict):
    configurationIds: Sequence[str]

class DescribeContinuousExportsRequestRequestTypeDef(TypedDict):
    exportIds: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeExportConfigurationsRequestRequestTypeDef(TypedDict):
    exportIds: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ExportInfoTypeDef(TypedDict):
    exportId: str
    exportStatus: ExportStatusType
    statusMessage: str
    exportRequestTime: datetime
    configurationsDownloadUrl: NotRequired[str]
    isTruncated: NotRequired[bool]
    requestedStartTime: NotRequired[datetime]
    requestedEndTime: NotRequired[datetime]

class ExportFilterTypeDef(TypedDict):
    name: str
    values: Sequence[str]
    condition: str

class ImportTaskFilterTypeDef(TypedDict):
    name: NotRequired[ImportTaskFilterNameType]
    values: NotRequired[Sequence[str]]

class ImportTaskTypeDef(TypedDict):
    importTaskId: NotRequired[str]
    clientRequestToken: NotRequired[str]
    name: NotRequired[str]
    importUrl: NotRequired[str]
    status: NotRequired[ImportStatusType]
    importRequestTime: NotRequired[datetime]
    importCompletionTime: NotRequired[datetime]
    importDeletedTime: NotRequired[datetime]
    fileClassification: NotRequired[FileClassificationType]
    serverImportSuccess: NotRequired[int]
    serverImportFailure: NotRequired[int]
    applicationImportSuccess: NotRequired[int]
    applicationImportFailure: NotRequired[int]
    errorsAndFailedEntriesZip: NotRequired[str]

class TagFilterTypeDef(TypedDict):
    name: str
    values: Sequence[str]

class DisassociateConfigurationItemsFromApplicationRequestRequestTypeDef(TypedDict):
    applicationConfigurationId: str
    configurationIds: Sequence[str]

class ReservedInstanceOptionsTypeDef(TypedDict):
    purchasingOption: PurchasingOptionType
    offeringClass: OfferingClassType
    termLength: TermLengthType

class UsageMetricBasisTypeDef(TypedDict):
    name: NotRequired[str]
    percentageAdjust: NotRequired[float]

class OrderByElementTypeDef(TypedDict):
    fieldName: str
    sortOrder: NotRequired[OrderStringType]

class ListServerNeighborsRequestRequestTypeDef(TypedDict):
    configurationId: str
    portInformationNeeded: NotRequired[bool]
    neighborConfigurationIds: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class NeighborConnectionDetailTypeDef(TypedDict):
    sourceServerId: str
    destinationServerId: str
    connectionsCount: int
    destinationPort: NotRequired[int]
    transportProtocol: NotRequired[str]

class StartBatchDeleteConfigurationTaskRequestRequestTypeDef(TypedDict):
    configurationType: Literal["SERVER"]
    configurationIds: Sequence[str]

class StartDataCollectionByAgentIdsRequestRequestTypeDef(TypedDict):
    agentIds: Sequence[str]

TimestampTypeDef = Union[datetime, str]

class StartImportTaskRequestRequestTypeDef(TypedDict):
    name: str
    importUrl: str
    clientRequestToken: NotRequired[str]

class StopContinuousExportRequestRequestTypeDef(TypedDict):
    exportId: str

class StopDataCollectionByAgentIdsRequestRequestTypeDef(TypedDict):
    agentIds: Sequence[str]

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    configurationId: str
    name: NotRequired[str]
    description: NotRequired[str]
    wave: NotRequired[str]

class AgentInfoTypeDef(TypedDict):
    agentId: NotRequired[str]
    hostName: NotRequired[str]
    agentNetworkInfoList: NotRequired[List[AgentNetworkInfoTypeDef]]
    connectorId: NotRequired[str]
    version: NotRequired[str]
    health: NotRequired[AgentStatusType]
    lastHealthPingTime: NotRequired[str]
    collectionStatus: NotRequired[str]
    agentType: NotRequired[str]
    registeredTime: NotRequired[str]

class BatchDeleteAgentsRequestRequestTypeDef(TypedDict):
    deleteAgents: Sequence[DeleteAgentTypeDef]

class BatchDeleteAgentsResponseTypeDef(TypedDict):
    errors: List[BatchDeleteAgentErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationResponseTypeDef(TypedDict):
    configurationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeConfigurationsResponseTypeDef(TypedDict):
    configurations: List[Dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef

class ExportConfigurationsResponseTypeDef(TypedDict):
    exportId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationsResponseTypeDef(TypedDict):
    configurations: List[Dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartBatchDeleteConfigurationTaskResponseTypeDef(TypedDict):
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartContinuousExportResponseTypeDef(TypedDict):
    exportId: str
    s3Bucket: str
    startTime: datetime
    dataSource: Literal["AGENT"]
    schemaStorageConfig: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartDataCollectionByAgentIdsResponseTypeDef(TypedDict):
    agentsConfigurationStatus: List[AgentConfigurationStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartExportTaskResponseTypeDef(TypedDict):
    exportId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopContinuousExportResponseTypeDef(TypedDict):
    startTime: datetime
    stopTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StopDataCollectionByAgentIdsResponseTypeDef(TypedDict):
    agentsConfigurationStatus: List[AgentConfigurationStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteConfigurationTaskTypeDef(TypedDict):
    taskId: NotRequired[str]
    status: NotRequired[BatchDeleteConfigurationTaskStatusType]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    configurationType: NotRequired[Literal["SERVER"]]
    requestedConfigurations: NotRequired[List[str]]
    deletedConfigurations: NotRequired[List[str]]
    failedConfigurations: NotRequired[List[FailedConfigurationTypeDef]]
    deletionWarnings: NotRequired[List[DeletionWarningTypeDef]]

class BatchDeleteImportDataResponseTypeDef(TypedDict):
    errors: List[BatchDeleteImportDataErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTagsResponseTypeDef(TypedDict):
    tags: List[ConfigurationTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeContinuousExportsResponseTypeDef(TypedDict):
    descriptions: List[ContinuousExportDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateTagsRequestRequestTypeDef(TypedDict):
    configurationIds: Sequence[str]
    tags: Sequence[TagTypeDef]

class DeleteTagsRequestRequestTypeDef(TypedDict):
    configurationIds: Sequence[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class GetDiscoverySummaryResponseTypeDef(TypedDict):
    servers: int
    applications: int
    serversMappedToApplications: int
    serversMappedtoTags: int
    agentSummary: CustomerAgentInfoTypeDef
    connectorSummary: CustomerConnectorInfoTypeDef
    meCollectorSummary: CustomerMeCollectorInfoTypeDef
    agentlessCollectorSummary: CustomerAgentlessCollectorInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAgentsRequestRequestTypeDef(TypedDict):
    agentIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeAgentsRequestDescribeAgentsPaginateTypeDef(TypedDict):
    agentIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeContinuousExportsRequestDescribeContinuousExportsPaginateTypeDef(TypedDict):
    exportIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeExportConfigurationsRequestDescribeExportConfigurationsPaginateTypeDef(TypedDict):
    exportIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeExportConfigurationsResponseTypeDef(TypedDict):
    exportsInfo: List[ExportInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeExportTasksResponseTypeDef(TypedDict):
    exportsInfo: List[ExportInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef(TypedDict):
    exportIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[ExportFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeExportTasksRequestRequestTypeDef(TypedDict):
    exportIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[ExportFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeImportTasksRequestDescribeImportTasksPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[ImportTaskFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeImportTasksRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[ImportTaskFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeImportTasksResponseTypeDef(TypedDict):
    tasks: List[ImportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartImportTaskResponseTypeDef(TypedDict):
    task: ImportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTagsRequestDescribeTagsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[TagFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeTagsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[TagFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class Ec2RecommendationsExportPreferencesTypeDef(TypedDict):
    enabled: NotRequired[bool]
    cpuPerformanceMetricBasis: NotRequired[UsageMetricBasisTypeDef]
    ramPerformanceMetricBasis: NotRequired[UsageMetricBasisTypeDef]
    tenancy: NotRequired[TenancyType]
    excludedInstanceTypes: NotRequired[Sequence[str]]
    preferredRegion: NotRequired[str]
    reservedInstanceOptions: NotRequired[ReservedInstanceOptionsTypeDef]

class ListConfigurationsRequestListConfigurationsPaginateTypeDef(TypedDict):
    configurationType: ConfigurationItemTypeType
    filters: NotRequired[Sequence[FilterTypeDef]]
    orderBy: NotRequired[Sequence[OrderByElementTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfigurationsRequestRequestTypeDef(TypedDict):
    configurationType: ConfigurationItemTypeType
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    orderBy: NotRequired[Sequence[OrderByElementTypeDef]]

class ListServerNeighborsResponseTypeDef(TypedDict):
    neighbors: List[NeighborConnectionDetailTypeDef]
    knownDependencyCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeAgentsResponseTypeDef(TypedDict):
    agentsInfo: List[AgentInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribeBatchDeleteConfigurationTaskResponseTypeDef(TypedDict):
    task: BatchDeleteConfigurationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportPreferencesTypeDef(TypedDict):
    ec2RecommendationsPreferences: NotRequired[Ec2RecommendationsExportPreferencesTypeDef]

class StartExportTaskRequestRequestTypeDef(TypedDict):
    exportDataFormat: NotRequired[Sequence[Literal["CSV"]]]
    filters: NotRequired[Sequence[ExportFilterTypeDef]]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    preferences: NotRequired[ExportPreferencesTypeDef]
