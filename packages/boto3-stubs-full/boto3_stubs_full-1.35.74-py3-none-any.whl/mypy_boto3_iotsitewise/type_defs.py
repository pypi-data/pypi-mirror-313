"""
Type annotations for iotsitewise service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotsitewise.type_defs import AccessDeniedExceptionTypeDef

    data: AccessDeniedExceptionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    AggregateTypeType,
    AssetModelStateType,
    AssetModelTypeType,
    AssetModelVersionTypeType,
    AssetStateType,
    AuthModeType,
    BatchEntryCompletionStatusType,
    BatchGetAssetPropertyAggregatesErrorCodeType,
    BatchGetAssetPropertyValueErrorCodeType,
    BatchGetAssetPropertyValueHistoryErrorCodeType,
    BatchPutAssetPropertyValueErrorCodeType,
    CapabilitySyncStatusType,
    ColumnNameType,
    ComputeLocationType,
    ConfigurationStateType,
    DatasetStateType,
    DetailedErrorCodeType,
    DisassociatedDataStorageStateType,
    EncryptionTypeType,
    ErrorCodeType,
    ForwardingConfigStateType,
    IdentityTypeType,
    JobStatusType,
    ListAssetModelPropertiesFilterType,
    ListAssetPropertiesFilterType,
    ListAssetsFilterType,
    ListBulkImportJobsFilterType,
    ListTimeSeriesTypeType,
    LoggingLevelType,
    MonitorErrorCodeType,
    PermissionType,
    PortalStateType,
    PortalTypeType,
    PropertyDataTypeType,
    PropertyNotificationStateType,
    QualityType,
    ResourceTypeType,
    ScalarTypeType,
    StorageTypeType,
    TimeOrderingType,
    TraversalDirectionType,
    WarmTierStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessDeniedExceptionTypeDef",
    "AccessPolicySummaryTypeDef",
    "ActionDefinitionTypeDef",
    "ActionPayloadTypeDef",
    "ActionSummaryTypeDef",
    "AggregatedValueTypeDef",
    "AggregatesTypeDef",
    "AlarmsTypeDef",
    "AssetCompositeModelPathSegmentTypeDef",
    "AssetCompositeModelSummaryTypeDef",
    "AssetCompositeModelTypeDef",
    "AssetErrorDetailsTypeDef",
    "AssetHierarchyInfoTypeDef",
    "AssetHierarchyTypeDef",
    "AssetModelCompositeModelDefinitionTypeDef",
    "AssetModelCompositeModelOutputTypeDef",
    "AssetModelCompositeModelPathSegmentTypeDef",
    "AssetModelCompositeModelSummaryTypeDef",
    "AssetModelCompositeModelTypeDef",
    "AssetModelCompositeModelUnionTypeDef",
    "AssetModelHierarchyDefinitionTypeDef",
    "AssetModelHierarchyTypeDef",
    "AssetModelPropertyDefinitionTypeDef",
    "AssetModelPropertyOutputTypeDef",
    "AssetModelPropertyPathSegmentTypeDef",
    "AssetModelPropertySummaryTypeDef",
    "AssetModelPropertyTypeDef",
    "AssetModelPropertyUnionTypeDef",
    "AssetModelStatusTypeDef",
    "AssetModelSummaryTypeDef",
    "AssetPropertyPathSegmentTypeDef",
    "AssetPropertySummaryTypeDef",
    "AssetPropertyTypeDef",
    "AssetPropertyValueTypeDef",
    "AssetRelationshipSummaryTypeDef",
    "AssetStatusTypeDef",
    "AssetSummaryTypeDef",
    "AssociateAssetsRequestRequestTypeDef",
    "AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    "AssociatedAssetsSummaryTypeDef",
    "AttributeTypeDef",
    "BatchAssociateProjectAssetsRequestRequestTypeDef",
    "BatchAssociateProjectAssetsResponseTypeDef",
    "BatchDisassociateProjectAssetsRequestRequestTypeDef",
    "BatchDisassociateProjectAssetsResponseTypeDef",
    "BatchGetAssetPropertyAggregatesEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    "BatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    "BatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    "BatchGetAssetPropertyValueEntryTypeDef",
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    "BatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    "BatchGetAssetPropertyValueRequestRequestTypeDef",
    "BatchGetAssetPropertyValueResponseTypeDef",
    "BatchGetAssetPropertyValueSkippedEntryTypeDef",
    "BatchGetAssetPropertyValueSuccessEntryTypeDef",
    "BatchPutAssetPropertyErrorEntryTypeDef",
    "BatchPutAssetPropertyErrorTypeDef",
    "BatchPutAssetPropertyValueRequestRequestTypeDef",
    "BatchPutAssetPropertyValueResponseTypeDef",
    "BlobTypeDef",
    "CitationTypeDef",
    "ColumnInfoTypeDef",
    "ColumnTypeTypeDef",
    "CompositeModelPropertyTypeDef",
    "CompositionDetailsTypeDef",
    "CompositionRelationshipItemTypeDef",
    "CompositionRelationshipSummaryTypeDef",
    "ConfigurationErrorDetailsTypeDef",
    "ConfigurationStatusTypeDef",
    "ConflictingOperationExceptionTypeDef",
    "ContentTypeDef",
    "CreateAccessPolicyRequestRequestTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "CreateAssetModelCompositeModelRequestRequestTypeDef",
    "CreateAssetModelCompositeModelResponseTypeDef",
    "CreateAssetModelRequestRequestTypeDef",
    "CreateAssetModelResponseTypeDef",
    "CreateAssetRequestRequestTypeDef",
    "CreateAssetResponseTypeDef",
    "CreateBulkImportJobRequestRequestTypeDef",
    "CreateBulkImportJobResponseTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateGatewayRequestRequestTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreatePortalRequestRequestTypeDef",
    "CreatePortalResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CsvOutputTypeDef",
    "CsvTypeDef",
    "CsvUnionTypeDef",
    "CustomerManagedS3StorageTypeDef",
    "DashboardSummaryTypeDef",
    "DataSetReferenceTypeDef",
    "DatasetSourceTypeDef",
    "DatasetStatusTypeDef",
    "DatasetSummaryTypeDef",
    "DatumPaginatorTypeDef",
    "DatumTypeDef",
    "DeleteAccessPolicyRequestRequestTypeDef",
    "DeleteAssetModelCompositeModelRequestRequestTypeDef",
    "DeleteAssetModelCompositeModelResponseTypeDef",
    "DeleteAssetModelRequestRequestTypeDef",
    "DeleteAssetModelResponseTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeleteAssetResponseTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteDatasetResponseTypeDef",
    "DeleteGatewayRequestRequestTypeDef",
    "DeletePortalRequestRequestTypeDef",
    "DeletePortalResponseTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteTimeSeriesRequestRequestTypeDef",
    "DescribeAccessPolicyRequestRequestTypeDef",
    "DescribeAccessPolicyResponseTypeDef",
    "DescribeActionRequestRequestTypeDef",
    "DescribeActionResponseTypeDef",
    "DescribeAssetCompositeModelRequestRequestTypeDef",
    "DescribeAssetCompositeModelResponseTypeDef",
    "DescribeAssetModelCompositeModelRequestRequestTypeDef",
    "DescribeAssetModelCompositeModelResponseTypeDef",
    "DescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    "DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    "DescribeAssetModelRequestRequestTypeDef",
    "DescribeAssetModelResponseTypeDef",
    "DescribeAssetPropertyRequestRequestTypeDef",
    "DescribeAssetPropertyResponseTypeDef",
    "DescribeAssetRequestAssetActiveWaitTypeDef",
    "DescribeAssetRequestAssetNotExistsWaitTypeDef",
    "DescribeAssetRequestRequestTypeDef",
    "DescribeAssetResponseTypeDef",
    "DescribeBulkImportJobRequestRequestTypeDef",
    "DescribeBulkImportJobResponseTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    "DescribeGatewayCapabilityConfigurationRequestRequestTypeDef",
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    "DescribeGatewayRequestRequestTypeDef",
    "DescribeGatewayResponseTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "DescribePortalRequestPortalActiveWaitTypeDef",
    "DescribePortalRequestPortalNotExistsWaitTypeDef",
    "DescribePortalRequestRequestTypeDef",
    "DescribePortalResponseTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DescribeProjectResponseTypeDef",
    "DescribeStorageConfigurationResponseTypeDef",
    "DescribeTimeSeriesRequestRequestTypeDef",
    "DescribeTimeSeriesResponseTypeDef",
    "DetailedErrorTypeDef",
    "DisassociateAssetsRequestRequestTypeDef",
    "DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ErrorDetailsTypeDef",
    "ErrorReportLocationTypeDef",
    "ExecuteActionRequestRequestTypeDef",
    "ExecuteActionResponseTypeDef",
    "ExecuteQueryRequestExecuteQueryPaginateTypeDef",
    "ExecuteQueryRequestRequestTypeDef",
    "ExecuteQueryResponsePaginatorTypeDef",
    "ExecuteQueryResponseTypeDef",
    "ExpressionVariableOutputTypeDef",
    "ExpressionVariableTypeDef",
    "ExpressionVariableUnionTypeDef",
    "FileFormatOutputTypeDef",
    "FileFormatTypeDef",
    "FileFormatUnionTypeDef",
    "FileTypeDef",
    "ForwardingConfigTypeDef",
    "GatewayCapabilitySummaryTypeDef",
    "GatewayPlatformTypeDef",
    "GatewaySummaryTypeDef",
    "GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    "GetAssetPropertyAggregatesRequestRequestTypeDef",
    "GetAssetPropertyAggregatesResponseTypeDef",
    "GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef",
    "GetAssetPropertyValueHistoryRequestRequestTypeDef",
    "GetAssetPropertyValueHistoryResponseTypeDef",
    "GetAssetPropertyValueRequestRequestTypeDef",
    "GetAssetPropertyValueResponseTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    "GreengrassTypeDef",
    "GreengrassV2TypeDef",
    "GroupIdentityTypeDef",
    "IAMRoleIdentityTypeDef",
    "IAMUserIdentityTypeDef",
    "IdentityTypeDef",
    "ImageFileTypeDef",
    "ImageLocationTypeDef",
    "ImageTypeDef",
    "InternalFailureExceptionTypeDef",
    "InterpolatedAssetPropertyValueTypeDef",
    "InvalidRequestExceptionTypeDef",
    "InvocationOutputTypeDef",
    "InvokeAssistantRequestRequestTypeDef",
    "InvokeAssistantResponseTypeDef",
    "JobConfigurationOutputTypeDef",
    "JobConfigurationTypeDef",
    "JobSummaryTypeDef",
    "KendraSourceDetailTypeDef",
    "LimitExceededExceptionTypeDef",
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    "ListAccessPoliciesRequestRequestTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "ListActionsRequestListActionsPaginateTypeDef",
    "ListActionsRequestRequestTypeDef",
    "ListActionsResponseTypeDef",
    "ListAssetModelCompositeModelsRequestListAssetModelCompositeModelsPaginateTypeDef",
    "ListAssetModelCompositeModelsRequestRequestTypeDef",
    "ListAssetModelCompositeModelsResponseTypeDef",
    "ListAssetModelPropertiesRequestListAssetModelPropertiesPaginateTypeDef",
    "ListAssetModelPropertiesRequestRequestTypeDef",
    "ListAssetModelPropertiesResponseTypeDef",
    "ListAssetModelsRequestListAssetModelsPaginateTypeDef",
    "ListAssetModelsRequestRequestTypeDef",
    "ListAssetModelsResponseTypeDef",
    "ListAssetPropertiesRequestListAssetPropertiesPaginateTypeDef",
    "ListAssetPropertiesRequestRequestTypeDef",
    "ListAssetPropertiesResponseTypeDef",
    "ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    "ListAssetRelationshipsRequestRequestTypeDef",
    "ListAssetRelationshipsResponseTypeDef",
    "ListAssetsRequestListAssetsPaginateTypeDef",
    "ListAssetsRequestRequestTypeDef",
    "ListAssetsResponseTypeDef",
    "ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    "ListAssociatedAssetsRequestRequestTypeDef",
    "ListAssociatedAssetsResponseTypeDef",
    "ListBulkImportJobsRequestListBulkImportJobsPaginateTypeDef",
    "ListBulkImportJobsRequestRequestTypeDef",
    "ListBulkImportJobsResponseTypeDef",
    "ListCompositionRelationshipsRequestListCompositionRelationshipsPaginateTypeDef",
    "ListCompositionRelationshipsRequestRequestTypeDef",
    "ListCompositionRelationshipsResponseTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListGatewaysResponseTypeDef",
    "ListPortalsRequestListPortalsPaginateTypeDef",
    "ListPortalsRequestRequestTypeDef",
    "ListPortalsResponseTypeDef",
    "ListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    "ListProjectAssetsRequestRequestTypeDef",
    "ListProjectAssetsResponseTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTimeSeriesRequestListTimeSeriesPaginateTypeDef",
    "ListTimeSeriesRequestRequestTypeDef",
    "ListTimeSeriesResponseTypeDef",
    "LocationTypeDef",
    "LoggingOptionsTypeDef",
    "MeasurementProcessingConfigTypeDef",
    "MeasurementTypeDef",
    "MetricOutputTypeDef",
    "MetricProcessingConfigTypeDef",
    "MetricTypeDef",
    "MetricUnionTypeDef",
    "MetricWindowTypeDef",
    "MonitorErrorDetailsTypeDef",
    "MultiLayerStorageTypeDef",
    "PaginatorConfigTypeDef",
    "PortalResourceTypeDef",
    "PortalStatusTypeDef",
    "PortalSummaryTypeDef",
    "PortalTypeEntryOutputTypeDef",
    "PortalTypeEntryTypeDef",
    "PortalTypeEntryUnionTypeDef",
    "ProjectResourceTypeDef",
    "ProjectSummaryTypeDef",
    "PropertyNotificationTypeDef",
    "PropertyTypeDef",
    "PropertyTypeOutputTypeDef",
    "PropertyTypeTypeDef",
    "PropertyTypeUnionTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "PutDefaultEncryptionConfigurationRequestRequestTypeDef",
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    "PutLoggingOptionsRequestRequestTypeDef",
    "PutStorageConfigurationRequestRequestTypeDef",
    "PutStorageConfigurationResponseTypeDef",
    "ReferenceTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseStreamTypeDef",
    "RetentionPeriodTypeDef",
    "RowPaginatorTypeDef",
    "RowTypeDef",
    "SiemensIETypeDef",
    "SourceDetailTypeDef",
    "SourceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetResourceTypeDef",
    "ThrottlingExceptionTypeDef",
    "TimeInNanosTypeDef",
    "TimeSeriesSummaryTypeDef",
    "TimestampTypeDef",
    "TraceTypeDef",
    "TransformOutputTypeDef",
    "TransformProcessingConfigTypeDef",
    "TransformTypeDef",
    "TransformUnionTypeDef",
    "TumblingWindowTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessPolicyRequestRequestTypeDef",
    "UpdateAssetModelCompositeModelRequestRequestTypeDef",
    "UpdateAssetModelCompositeModelResponseTypeDef",
    "UpdateAssetModelRequestRequestTypeDef",
    "UpdateAssetModelResponseTypeDef",
    "UpdateAssetPropertyRequestRequestTypeDef",
    "UpdateAssetRequestRequestTypeDef",
    "UpdateAssetResponseTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "UpdateDatasetRequestRequestTypeDef",
    "UpdateDatasetResponseTypeDef",
    "UpdateGatewayCapabilityConfigurationRequestRequestTypeDef",
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    "UpdateGatewayRequestRequestTypeDef",
    "UpdatePortalRequestRequestTypeDef",
    "UpdatePortalResponseTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UserIdentityTypeDef",
    "VariableValueOutputTypeDef",
    "VariableValueTypeDef",
    "VariableValueUnionTypeDef",
    "VariantTypeDef",
    "WaiterConfigTypeDef",
    "WarmTierRetentionPeriodTypeDef",
)


class AccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ActionDefinitionTypeDef(TypedDict):
    actionDefinitionId: str
    actionName: str
    actionType: str


class ActionPayloadTypeDef(TypedDict):
    stringValue: str


class TargetResourceTypeDef(TypedDict):
    assetId: str


AggregatesTypeDef = TypedDict(
    "AggregatesTypeDef",
    {
        "average": NotRequired[float],
        "count": NotRequired[float],
        "maximum": NotRequired[float],
        "minimum": NotRequired[float],
        "sum": NotRequired[float],
        "standardDeviation": NotRequired[float],
    },
)


class AlarmsTypeDef(TypedDict):
    alarmRoleArn: str
    notificationLambdaArn: NotRequired[str]


AssetCompositeModelPathSegmentTypeDef = TypedDict(
    "AssetCompositeModelPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)


class AssetErrorDetailsTypeDef(TypedDict):
    assetId: str
    code: Literal["INTERNAL_FAILURE"]
    message: str


class AssetHierarchyInfoTypeDef(TypedDict):
    parentAssetId: NotRequired[str]
    childAssetId: NotRequired[str]


AssetHierarchyTypeDef = TypedDict(
    "AssetHierarchyTypeDef",
    {
        "name": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
AssetModelCompositeModelPathSegmentTypeDef = TypedDict(
    "AssetModelCompositeModelPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)
AssetModelHierarchyDefinitionTypeDef = TypedDict(
    "AssetModelHierarchyDefinitionTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
AssetModelHierarchyTypeDef = TypedDict(
    "AssetModelHierarchyTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
AssetModelPropertyPathSegmentTypeDef = TypedDict(
    "AssetModelPropertyPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)
AssetPropertyPathSegmentTypeDef = TypedDict(
    "AssetPropertyPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)


class PropertyNotificationTypeDef(TypedDict):
    topic: str
    state: PropertyNotificationStateType


class TimeInNanosTypeDef(TypedDict):
    timeInSeconds: int
    offsetInNanos: NotRequired[int]


class VariantTypeDef(TypedDict):
    stringValue: NotRequired[str]
    integerValue: NotRequired[int]
    doubleValue: NotRequired[float]
    booleanValue: NotRequired[bool]


class AssociateAssetsRequestRequestTypeDef(TypedDict):
    assetId: str
    hierarchyId: str
    childAssetId: str
    clientToken: NotRequired[str]


class AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef(TypedDict):
    alias: str
    assetId: str
    propertyId: str
    clientToken: NotRequired[str]


class AttributeTypeDef(TypedDict):
    defaultValue: NotRequired[str]


class BatchAssociateProjectAssetsRequestRequestTypeDef(TypedDict):
    projectId: str
    assetIds: Sequence[str]
    clientToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BatchDisassociateProjectAssetsRequestRequestTypeDef(TypedDict):
    projectId: str
    assetIds: Sequence[str]
    clientToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class BatchGetAssetPropertyAggregatesErrorEntryTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyAggregatesErrorCodeType
    errorMessage: str
    entryId: str


class BatchGetAssetPropertyAggregatesErrorInfoTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyAggregatesErrorCodeType
    errorTimestamp: datetime


class BatchGetAssetPropertyValueEntryTypeDef(TypedDict):
    entryId: str
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]


class BatchGetAssetPropertyValueErrorEntryTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueErrorCodeType
    errorMessage: str
    entryId: str


class BatchGetAssetPropertyValueErrorInfoTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueErrorCodeType
    errorTimestamp: datetime


class BatchGetAssetPropertyValueHistoryErrorEntryTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueHistoryErrorCodeType
    errorMessage: str
    entryId: str


class BatchGetAssetPropertyValueHistoryErrorInfoTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueHistoryErrorCodeType
    errorTimestamp: datetime


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ContentTypeDef(TypedDict):
    text: NotRequired[str]


class ColumnTypeTypeDef(TypedDict):
    scalarType: NotRequired[ScalarTypeType]


CompositionRelationshipItemTypeDef = TypedDict(
    "CompositionRelationshipItemTypeDef",
    {
        "id": NotRequired[str],
    },
)


class CompositionRelationshipSummaryTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelCompositeModelType: str


class ConfigurationErrorDetailsTypeDef(TypedDict):
    code: ErrorCodeType
    message: str


class ConflictingOperationExceptionTypeDef(TypedDict):
    message: str
    resourceId: str
    resourceArn: str


class CreateAssetRequestRequestTypeDef(TypedDict):
    assetName: str
    assetModelId: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    assetDescription: NotRequired[str]
    assetId: NotRequired[str]
    assetExternalId: NotRequired[str]


class ErrorReportLocationTypeDef(TypedDict):
    bucket: str
    prefix: str


class FileTypeDef(TypedDict):
    bucket: str
    key: str
    versionId: NotRequired[str]


class CreateDashboardRequestRequestTypeDef(TypedDict):
    projectId: str
    dashboardName: str
    dashboardDefinition: str
    dashboardDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateProjectRequestRequestTypeDef(TypedDict):
    portalId: str
    projectName: str
    projectDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CsvOutputTypeDef(TypedDict):
    columnNames: List[ColumnNameType]


class CsvTypeDef(TypedDict):
    columnNames: Sequence[ColumnNameType]


class CustomerManagedS3StorageTypeDef(TypedDict):
    s3ResourceArn: str
    roleArn: str


DashboardSummaryTypeDef = TypedDict(
    "DashboardSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)


class DatumPaginatorTypeDef(TypedDict):
    scalarValue: NotRequired[str]
    arrayValue: NotRequired[List[Dict[str, Any]]]
    rowValue: NotRequired[Dict[str, Any]]
    nullValue: NotRequired[bool]


class DatumTypeDef(TypedDict):
    scalarValue: NotRequired[str]
    arrayValue: NotRequired[List[Dict[str, Any]]]
    rowValue: NotRequired[Dict[str, Any]]
    nullValue: NotRequired[bool]


class DeleteAccessPolicyRequestRequestTypeDef(TypedDict):
    accessPolicyId: str
    clientToken: NotRequired[str]


class DeleteAssetModelCompositeModelRequestRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    clientToken: NotRequired[str]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]


class DeleteAssetModelRequestRequestTypeDef(TypedDict):
    assetModelId: str
    clientToken: NotRequired[str]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]


class DeleteAssetRequestRequestTypeDef(TypedDict):
    assetId: str
    clientToken: NotRequired[str]


class DeleteDashboardRequestRequestTypeDef(TypedDict):
    dashboardId: str
    clientToken: NotRequired[str]


class DeleteDatasetRequestRequestTypeDef(TypedDict):
    datasetId: str
    clientToken: NotRequired[str]


class DeleteGatewayRequestRequestTypeDef(TypedDict):
    gatewayId: str


class DeletePortalRequestRequestTypeDef(TypedDict):
    portalId: str
    clientToken: NotRequired[str]


class DeleteProjectRequestRequestTypeDef(TypedDict):
    projectId: str
    clientToken: NotRequired[str]


class DeleteTimeSeriesRequestRequestTypeDef(TypedDict):
    alias: NotRequired[str]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    clientToken: NotRequired[str]


class DescribeAccessPolicyRequestRequestTypeDef(TypedDict):
    accessPolicyId: str


class DescribeActionRequestRequestTypeDef(TypedDict):
    actionId: str


class DescribeAssetCompositeModelRequestRequestTypeDef(TypedDict):
    assetId: str
    assetCompositeModelId: str


class DescribeAssetModelCompositeModelRequestRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelVersion: NotRequired[str]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeAssetModelRequestRequestTypeDef(TypedDict):
    assetModelId: str
    excludeProperties: NotRequired[bool]
    assetModelVersion: NotRequired[str]


class DescribeAssetPropertyRequestRequestTypeDef(TypedDict):
    assetId: str
    propertyId: str


class DescribeAssetRequestRequestTypeDef(TypedDict):
    assetId: str
    excludeProperties: NotRequired[bool]


class DescribeBulkImportJobRequestRequestTypeDef(TypedDict):
    jobId: str


class DescribeDashboardRequestRequestTypeDef(TypedDict):
    dashboardId: str


class DescribeDatasetRequestRequestTypeDef(TypedDict):
    datasetId: str


class DescribeGatewayCapabilityConfigurationRequestRequestTypeDef(TypedDict):
    gatewayId: str
    capabilityNamespace: str


class DescribeGatewayRequestRequestTypeDef(TypedDict):
    gatewayId: str


class GatewayCapabilitySummaryTypeDef(TypedDict):
    capabilityNamespace: str
    capabilitySyncStatus: CapabilitySyncStatusType


class LoggingOptionsTypeDef(TypedDict):
    level: LoggingLevelType


class DescribePortalRequestRequestTypeDef(TypedDict):
    portalId: str


ImageLocationTypeDef = TypedDict(
    "ImageLocationTypeDef",
    {
        "id": str,
        "url": str,
    },
)


class PortalTypeEntryOutputTypeDef(TypedDict):
    portalTools: NotRequired[List[str]]


class DescribeProjectRequestRequestTypeDef(TypedDict):
    projectId: str


class RetentionPeriodTypeDef(TypedDict):
    numberOfDays: NotRequired[int]
    unlimited: NotRequired[bool]


class WarmTierRetentionPeriodTypeDef(TypedDict):
    numberOfDays: NotRequired[int]
    unlimited: NotRequired[bool]


class DescribeTimeSeriesRequestRequestTypeDef(TypedDict):
    alias: NotRequired[str]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]


class DetailedErrorTypeDef(TypedDict):
    code: DetailedErrorCodeType
    message: str


class DisassociateAssetsRequestRequestTypeDef(TypedDict):
    assetId: str
    hierarchyId: str
    childAssetId: str
    clientToken: NotRequired[str]


class DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef(TypedDict):
    alias: str
    assetId: str
    propertyId: str
    clientToken: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ExecuteQueryRequestRequestTypeDef(TypedDict):
    queryStatement: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    clientToken: NotRequired[str]


class ForwardingConfigTypeDef(TypedDict):
    state: ForwardingConfigStateType


class GreengrassTypeDef(TypedDict):
    groupArn: str


class GreengrassV2TypeDef(TypedDict):
    coreDeviceThingName: str


class SiemensIETypeDef(TypedDict):
    iotCoreThingName: str


class GetAssetPropertyValueRequestRequestTypeDef(TypedDict):
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]


GetInterpolatedAssetPropertyValuesRequestRequestTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startTimeOffsetInNanos": NotRequired[int],
        "endTimeOffsetInNanos": NotRequired[int],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "intervalWindowInSeconds": NotRequired[int],
    },
)
GroupIdentityTypeDef = TypedDict(
    "GroupIdentityTypeDef",
    {
        "id": str,
    },
)


class IAMRoleIdentityTypeDef(TypedDict):
    arn: str


class IAMUserIdentityTypeDef(TypedDict):
    arn: str


UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "id": str,
    },
)


class InternalFailureExceptionTypeDef(TypedDict):
    message: str


class InvalidRequestExceptionTypeDef(TypedDict):
    message: str


class InvokeAssistantRequestRequestTypeDef(TypedDict):
    message: str
    conversationId: NotRequired[str]
    enableTrace: NotRequired[bool]


JobSummaryTypeDef = TypedDict(
    "JobSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "status": JobStatusType,
    },
)


class KendraSourceDetailTypeDef(TypedDict):
    knowledgeBaseArn: str
    roleArn: str


class LimitExceededExceptionTypeDef(TypedDict):
    message: str


class ListAccessPoliciesRequestRequestTypeDef(TypedDict):
    identityType: NotRequired[IdentityTypeType]
    identityId: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    resourceId: NotRequired[str]
    iamArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListActionsRequestRequestTypeDef(TypedDict):
    targetResourceType: Literal["ASSET"]
    targetResourceId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAssetModelCompositeModelsRequestRequestTypeDef(TypedDict):
    assetModelId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    assetModelVersion: NotRequired[str]


ListAssetModelPropertiesRequestRequestTypeDef = TypedDict(
    "ListAssetModelPropertiesRequestRequestTypeDef",
    {
        "assetModelId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListAssetModelPropertiesFilterType],
        "assetModelVersion": NotRequired[str],
    },
)


class ListAssetModelsRequestRequestTypeDef(TypedDict):
    assetModelTypes: NotRequired[Sequence[AssetModelTypeType]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    assetModelVersion: NotRequired[str]


ListAssetPropertiesRequestRequestTypeDef = TypedDict(
    "ListAssetPropertiesRequestRequestTypeDef",
    {
        "assetId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListAssetPropertiesFilterType],
    },
)


class ListAssetRelationshipsRequestRequestTypeDef(TypedDict):
    assetId: str
    traversalType: Literal["PATH_TO_ROOT"]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ListAssetsRequestRequestTypeDef = TypedDict(
    "ListAssetsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "assetModelId": NotRequired[str],
        "filter": NotRequired[ListAssetsFilterType],
    },
)


class ListAssociatedAssetsRequestRequestTypeDef(TypedDict):
    assetId: str
    hierarchyId: NotRequired[str]
    traversalDirection: NotRequired[TraversalDirectionType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ListBulkImportJobsRequestRequestTypeDef = TypedDict(
    "ListBulkImportJobsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListBulkImportJobsFilterType],
    },
)


class ListCompositionRelationshipsRequestRequestTypeDef(TypedDict):
    assetModelId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDashboardsRequestRequestTypeDef(TypedDict):
    projectId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDatasetsRequestRequestTypeDef(TypedDict):
    sourceType: Literal["KENDRA"]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListGatewaysRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPortalsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListProjectAssetsRequestRequestTypeDef(TypedDict):
    projectId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListProjectsRequestRequestTypeDef(TypedDict):
    portalId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListTimeSeriesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    assetId: NotRequired[str]
    aliasPrefix: NotRequired[str]
    timeSeriesType: NotRequired[ListTimeSeriesTypeType]


class TimeSeriesSummaryTypeDef(TypedDict):
    timeSeriesId: str
    dataType: PropertyDataTypeType
    timeSeriesCreationDate: datetime
    timeSeriesLastUpdateDate: datetime
    timeSeriesArn: str
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    alias: NotRequired[str]
    dataTypeSpec: NotRequired[str]


class LocationTypeDef(TypedDict):
    uri: NotRequired[str]


class MetricProcessingConfigTypeDef(TypedDict):
    computeLocation: ComputeLocationType


class TumblingWindowTypeDef(TypedDict):
    interval: str
    offset: NotRequired[str]


class MonitorErrorDetailsTypeDef(TypedDict):
    code: NotRequired[MonitorErrorCodeType]
    message: NotRequired[str]


PortalResourceTypeDef = TypedDict(
    "PortalResourceTypeDef",
    {
        "id": str,
    },
)


class PortalTypeEntryTypeDef(TypedDict):
    portalTools: NotRequired[Sequence[str]]


ProjectResourceTypeDef = TypedDict(
    "ProjectResourceTypeDef",
    {
        "id": str,
    },
)


class PutDefaultEncryptionConfigurationRequestRequestTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyId: NotRequired[str]


class ResourceNotFoundExceptionTypeDef(TypedDict):
    message: str


class ThrottlingExceptionTypeDef(TypedDict):
    message: str


class TraceTypeDef(TypedDict):
    text: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateAssetPropertyRequestRequestTypeDef(TypedDict):
    assetId: str
    propertyId: str
    propertyAlias: NotRequired[str]
    propertyNotificationState: NotRequired[PropertyNotificationStateType]
    clientToken: NotRequired[str]
    propertyUnit: NotRequired[str]


class UpdateAssetRequestRequestTypeDef(TypedDict):
    assetId: str
    assetName: str
    clientToken: NotRequired[str]
    assetDescription: NotRequired[str]
    assetExternalId: NotRequired[str]


class UpdateDashboardRequestRequestTypeDef(TypedDict):
    dashboardId: str
    dashboardName: str
    dashboardDefinition: str
    dashboardDescription: NotRequired[str]
    clientToken: NotRequired[str]


class UpdateGatewayCapabilityConfigurationRequestRequestTypeDef(TypedDict):
    gatewayId: str
    capabilityNamespace: str
    capabilityConfiguration: str


class UpdateGatewayRequestRequestTypeDef(TypedDict):
    gatewayId: str
    gatewayName: str


class UpdateProjectRequestRequestTypeDef(TypedDict):
    projectId: str
    projectName: str
    projectDescription: NotRequired[str]
    clientToken: NotRequired[str]


class ActionSummaryTypeDef(TypedDict):
    actionId: NotRequired[str]
    actionDefinitionId: NotRequired[str]
    targetResource: NotRequired[TargetResourceTypeDef]


class ExecuteActionRequestRequestTypeDef(TypedDict):
    targetResource: TargetResourceTypeDef
    actionDefinitionId: str
    actionPayload: ActionPayloadTypeDef
    clientToken: NotRequired[str]


class AggregatedValueTypeDef(TypedDict):
    timestamp: datetime
    value: AggregatesTypeDef
    quality: NotRequired[QualityType]


AssetCompositeModelSummaryTypeDef = TypedDict(
    "AssetCompositeModelSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "type": str,
        "description": str,
        "path": List[AssetCompositeModelPathSegmentTypeDef],
        "externalId": NotRequired[str],
    },
)


class AssetRelationshipSummaryTypeDef(TypedDict):
    relationshipType: Literal["HIERARCHY"]
    hierarchyInfo: NotRequired[AssetHierarchyInfoTypeDef]


AssetModelCompositeModelSummaryTypeDef = TypedDict(
    "AssetModelCompositeModelSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "type": str,
        "externalId": NotRequired[str],
        "description": NotRequired[str],
        "path": NotRequired[List[AssetModelCompositeModelPathSegmentTypeDef]],
    },
)


class VariableValueOutputTypeDef(TypedDict):
    propertyId: NotRequired[str]
    hierarchyId: NotRequired[str]
    propertyPath: NotRequired[List[AssetModelPropertyPathSegmentTypeDef]]


class VariableValueTypeDef(TypedDict):
    propertyId: NotRequired[str]
    hierarchyId: NotRequired[str]
    propertyPath: NotRequired[Sequence[AssetModelPropertyPathSegmentTypeDef]]


AssetPropertySummaryTypeDef = TypedDict(
    "AssetPropertySummaryTypeDef",
    {
        "id": str,
        "alias": NotRequired[str],
        "unit": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "assetCompositeModelId": NotRequired[str],
        "path": NotRequired[List[AssetPropertyPathSegmentTypeDef]],
        "externalId": NotRequired[str],
    },
)
AssetPropertyTypeDef = TypedDict(
    "AssetPropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
        "alias": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "path": NotRequired[List[AssetPropertyPathSegmentTypeDef]],
        "externalId": NotRequired[str],
    },
)


class BatchPutAssetPropertyErrorTypeDef(TypedDict):
    errorCode: BatchPutAssetPropertyValueErrorCodeType
    errorMessage: str
    timestamps: List[TimeInNanosTypeDef]


class AssetPropertyValueTypeDef(TypedDict):
    value: VariantTypeDef
    timestamp: TimeInNanosTypeDef
    quality: NotRequired[QualityType]


class InterpolatedAssetPropertyValueTypeDef(TypedDict):
    timestamp: TimeInNanosTypeDef
    value: VariantTypeDef


class BatchAssociateProjectAssetsResponseTypeDef(TypedDict):
    errors: List[AssetErrorDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDisassociateProjectAssetsResponseTypeDef(TypedDict):
    errors: List[AssetErrorDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAccessPolicyResponseTypeDef(TypedDict):
    accessPolicyId: str
    accessPolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBulkImportJobResponseTypeDef(TypedDict):
    jobId: str
    jobName: str
    jobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDashboardResponseTypeDef(TypedDict):
    dashboardId: str
    dashboardArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    gatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProjectResponseTypeDef(TypedDict):
    projectId: str
    projectArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeActionResponseTypeDef(TypedDict):
    actionId: str
    targetResource: TargetResourceTypeDef
    actionDefinitionId: str
    actionPayload: ActionPayloadTypeDef
    executionTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDashboardResponseTypeDef(TypedDict):
    dashboardId: str
    dashboardArn: str
    dashboardName: str
    projectId: str
    dashboardDescription: str
    dashboardDefinition: str
    dashboardCreationDate: datetime
    dashboardLastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGatewayCapabilityConfigurationResponseTypeDef(TypedDict):
    gatewayId: str
    capabilityNamespace: str
    capabilityConfiguration: str
    capabilitySyncStatus: CapabilitySyncStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProjectResponseTypeDef(TypedDict):
    projectId: str
    projectArn: str
    projectName: str
    portalId: str
    projectDescription: str
    projectCreationDate: datetime
    projectLastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTimeSeriesResponseTypeDef(TypedDict):
    assetId: str
    propertyId: str
    alias: str
    timeSeriesId: str
    dataType: PropertyDataTypeType
    dataTypeSpec: str
    timeSeriesCreationDate: datetime
    timeSeriesLastUpdateDate: datetime
    timeSeriesArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExecuteActionResponseTypeDef(TypedDict):
    actionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListProjectAssetsResponseTypeDef(TypedDict):
    assetIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGatewayCapabilityConfigurationResponseTypeDef(TypedDict):
    capabilityNamespace: str
    capabilitySyncStatus: CapabilitySyncStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetAssetPropertyAggregatesEntryTypeDef(TypedDict):
    entryId: str
    aggregateTypes: Sequence[AggregateTypeType]
    resolution: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]


class BatchGetAssetPropertyValueHistoryEntryTypeDef(TypedDict):
    entryId: str
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]


class GetAssetPropertyAggregatesRequestRequestTypeDef(TypedDict):
    aggregateTypes: Sequence[AggregateTypeType]
    resolution: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetAssetPropertyValueHistoryRequestRequestTypeDef(TypedDict):
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class BatchGetAssetPropertyAggregatesSkippedEntryTypeDef(TypedDict):
    entryId: str
    completionStatus: BatchEntryCompletionStatusType
    errorInfo: NotRequired[BatchGetAssetPropertyAggregatesErrorInfoTypeDef]


class BatchGetAssetPropertyValueRequestRequestTypeDef(TypedDict):
    entries: Sequence[BatchGetAssetPropertyValueEntryTypeDef]
    nextToken: NotRequired[str]


class BatchGetAssetPropertyValueSkippedEntryTypeDef(TypedDict):
    entryId: str
    completionStatus: BatchEntryCompletionStatusType
    errorInfo: NotRequired[BatchGetAssetPropertyValueErrorInfoTypeDef]


class BatchGetAssetPropertyValueHistorySkippedEntryTypeDef(TypedDict):
    entryId: str
    completionStatus: BatchEntryCompletionStatusType
    errorInfo: NotRequired[BatchGetAssetPropertyValueHistoryErrorInfoTypeDef]


ImageFileTypeDef = TypedDict(
    "ImageFileTypeDef",
    {
        "data": BlobTypeDef,
        "type": Literal["PNG"],
    },
)
ColumnInfoTypeDef = TypedDict(
    "ColumnInfoTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[ColumnTypeTypeDef],
    },
)


class CompositionDetailsTypeDef(TypedDict):
    compositionRelationship: NotRequired[List[CompositionRelationshipItemTypeDef]]


class ListCompositionRelationshipsResponseTypeDef(TypedDict):
    compositionRelationshipSummaries: List[CompositionRelationshipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ConfigurationStatusTypeDef(TypedDict):
    state: ConfigurationStateType
    error: NotRequired[ConfigurationErrorDetailsTypeDef]


class FileFormatOutputTypeDef(TypedDict):
    csv: NotRequired[CsvOutputTypeDef]
    parquet: NotRequired[Dict[str, Any]]


CsvUnionTypeDef = Union[CsvTypeDef, CsvOutputTypeDef]


class MultiLayerStorageTypeDef(TypedDict):
    customerManagedS3Storage: CustomerManagedS3StorageTypeDef


class ListDashboardsResponseTypeDef(TypedDict):
    dashboardSummaries: List[DashboardSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RowPaginatorTypeDef(TypedDict):
    data: List[DatumPaginatorTypeDef]


class RowTypeDef(TypedDict):
    data: List[DatumTypeDef]


class DescribeAssetModelRequestAssetModelActiveWaitTypeDef(TypedDict):
    assetModelId: str
    excludeProperties: NotRequired[bool]
    assetModelVersion: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef(TypedDict):
    assetModelId: str
    excludeProperties: NotRequired[bool]
    assetModelVersion: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeAssetRequestAssetActiveWaitTypeDef(TypedDict):
    assetId: str
    excludeProperties: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeAssetRequestAssetNotExistsWaitTypeDef(TypedDict):
    assetId: str
    excludeProperties: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribePortalRequestPortalActiveWaitTypeDef(TypedDict):
    portalId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribePortalRequestPortalNotExistsWaitTypeDef(TypedDict):
    portalId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeLoggingOptionsResponseTypeDef(TypedDict):
    loggingOptions: LoggingOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutLoggingOptionsRequestRequestTypeDef(TypedDict):
    loggingOptions: LoggingOptionsTypeDef


class ErrorDetailsTypeDef(TypedDict):
    code: ErrorCodeType
    message: str
    details: NotRequired[List[DetailedErrorTypeDef]]


class ExecuteQueryRequestExecuteQueryPaginateTypeDef(TypedDict):
    queryStatement: str
    clientToken: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef(TypedDict):
    aggregateTypes: Sequence[AggregateTypeType]
    resolution: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef(TypedDict):
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startTimeOffsetInNanos": NotRequired[int],
        "endTimeOffsetInNanos": NotRequired[int],
        "intervalWindowInSeconds": NotRequired[int],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef(TypedDict):
    identityType: NotRequired[IdentityTypeType]
    identityId: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    resourceId: NotRequired[str]
    iamArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListActionsRequestListActionsPaginateTypeDef(TypedDict):
    targetResourceType: Literal["ASSET"]
    targetResourceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetModelCompositeModelsRequestListAssetModelCompositeModelsPaginateTypeDef(TypedDict):
    assetModelId: str
    assetModelVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListAssetModelPropertiesRequestListAssetModelPropertiesPaginateTypeDef = TypedDict(
    "ListAssetModelPropertiesRequestListAssetModelPropertiesPaginateTypeDef",
    {
        "assetModelId": str,
        "filter": NotRequired[ListAssetModelPropertiesFilterType],
        "assetModelVersion": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListAssetModelsRequestListAssetModelsPaginateTypeDef(TypedDict):
    assetModelTypes: NotRequired[Sequence[AssetModelTypeType]]
    assetModelVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListAssetPropertiesRequestListAssetPropertiesPaginateTypeDef = TypedDict(
    "ListAssetPropertiesRequestListAssetPropertiesPaginateTypeDef",
    {
        "assetId": str,
        "filter": NotRequired[ListAssetPropertiesFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef(TypedDict):
    assetId: str
    traversalType: Literal["PATH_TO_ROOT"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListAssetsRequestListAssetsPaginateTypeDef = TypedDict(
    "ListAssetsRequestListAssetsPaginateTypeDef",
    {
        "assetModelId": NotRequired[str],
        "filter": NotRequired[ListAssetsFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef(TypedDict):
    assetId: str
    hierarchyId: NotRequired[str]
    traversalDirection: NotRequired[TraversalDirectionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListBulkImportJobsRequestListBulkImportJobsPaginateTypeDef = TypedDict(
    "ListBulkImportJobsRequestListBulkImportJobsPaginateTypeDef",
    {
        "filter": NotRequired[ListBulkImportJobsFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListCompositionRelationshipsRequestListCompositionRelationshipsPaginateTypeDef(TypedDict):
    assetModelId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDashboardsRequestListDashboardsPaginateTypeDef(TypedDict):
    projectId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDatasetsRequestListDatasetsPaginateTypeDef(TypedDict):
    sourceType: Literal["KENDRA"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGatewaysRequestListGatewaysPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPortalsRequestListPortalsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectAssetsRequestListProjectAssetsPaginateTypeDef(TypedDict):
    projectId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectsRequestListProjectsPaginateTypeDef(TypedDict):
    portalId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTimeSeriesRequestListTimeSeriesPaginateTypeDef(TypedDict):
    assetId: NotRequired[str]
    aliasPrefix: NotRequired[str]
    timeSeriesType: NotRequired[ListTimeSeriesTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class MeasurementProcessingConfigTypeDef(TypedDict):
    forwardingConfig: ForwardingConfigTypeDef


class TransformProcessingConfigTypeDef(TypedDict):
    computeLocation: ComputeLocationType
    forwardingConfig: NotRequired[ForwardingConfigTypeDef]


class GatewayPlatformTypeDef(TypedDict):
    greengrass: NotRequired[GreengrassTypeDef]
    greengrassV2: NotRequired[GreengrassV2TypeDef]
    siemensIE: NotRequired[SiemensIETypeDef]


class IdentityTypeDef(TypedDict):
    user: NotRequired[UserIdentityTypeDef]
    group: NotRequired[GroupIdentityTypeDef]
    iamUser: NotRequired[IAMUserIdentityTypeDef]
    iamRole: NotRequired[IAMRoleIdentityTypeDef]


class ListBulkImportJobsResponseTypeDef(TypedDict):
    jobSummaries: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SourceDetailTypeDef(TypedDict):
    kendra: NotRequired[KendraSourceDetailTypeDef]


class ListProjectsResponseTypeDef(TypedDict):
    projectSummaries: List[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTimeSeriesResponseTypeDef(TypedDict):
    TimeSeriesSummaries: List[TimeSeriesSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SourceTypeDef(TypedDict):
    arn: NotRequired[str]
    location: NotRequired[LocationTypeDef]


class MetricWindowTypeDef(TypedDict):
    tumbling: NotRequired[TumblingWindowTypeDef]


class PortalStatusTypeDef(TypedDict):
    state: PortalStateType
    error: NotRequired[MonitorErrorDetailsTypeDef]


PortalTypeEntryUnionTypeDef = Union[PortalTypeEntryTypeDef, PortalTypeEntryOutputTypeDef]


class ResourceTypeDef(TypedDict):
    portal: NotRequired[PortalResourceTypeDef]
    project: NotRequired[ProjectResourceTypeDef]


class ListActionsResponseTypeDef(TypedDict):
    actionSummaries: List[ActionSummaryTypeDef]
    nextToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetAssetPropertyAggregatesSuccessEntryTypeDef(TypedDict):
    entryId: str
    aggregatedValues: List[AggregatedValueTypeDef]


class GetAssetPropertyAggregatesResponseTypeDef(TypedDict):
    aggregatedValues: List[AggregatedValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssetRelationshipsResponseTypeDef(TypedDict):
    assetRelationshipSummaries: List[AssetRelationshipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssetModelCompositeModelsResponseTypeDef(TypedDict):
    assetModelCompositeModelSummaries: List[AssetModelCompositeModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ExpressionVariableOutputTypeDef(TypedDict):
    name: str
    value: VariableValueOutputTypeDef


VariableValueUnionTypeDef = Union[VariableValueTypeDef, VariableValueOutputTypeDef]


class ListAssetPropertiesResponseTypeDef(TypedDict):
    assetPropertySummaries: List[AssetPropertySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AssetCompositeModelTypeDef = TypedDict(
    "AssetCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "properties": List[AssetPropertyTypeDef],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)


class DescribeAssetCompositeModelResponseTypeDef(TypedDict):
    assetId: str
    assetCompositeModelId: str
    assetCompositeModelExternalId: str
    assetCompositeModelPath: List[AssetCompositeModelPathSegmentTypeDef]
    assetCompositeModelName: str
    assetCompositeModelDescription: str
    assetCompositeModelType: str
    assetCompositeModelProperties: List[AssetPropertyTypeDef]
    assetCompositeModelSummaries: List[AssetCompositeModelSummaryTypeDef]
    actionDefinitions: List[ActionDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchPutAssetPropertyErrorEntryTypeDef(TypedDict):
    entryId: str
    errors: List[BatchPutAssetPropertyErrorTypeDef]


class BatchGetAssetPropertyValueHistorySuccessEntryTypeDef(TypedDict):
    entryId: str
    assetPropertyValueHistory: List[AssetPropertyValueTypeDef]


class BatchGetAssetPropertyValueSuccessEntryTypeDef(TypedDict):
    entryId: str
    assetPropertyValue: NotRequired[AssetPropertyValueTypeDef]


class GetAssetPropertyValueHistoryResponseTypeDef(TypedDict):
    assetPropertyValueHistory: List[AssetPropertyValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetAssetPropertyValueResponseTypeDef(TypedDict):
    propertyValue: AssetPropertyValueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutAssetPropertyValueEntryTypeDef(TypedDict):
    entryId: str
    propertyValues: Sequence[AssetPropertyValueTypeDef]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]


class GetInterpolatedAssetPropertyValuesResponseTypeDef(TypedDict):
    interpolatedAssetPropertyValues: List[InterpolatedAssetPropertyValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchGetAssetPropertyAggregatesRequestRequestTypeDef(TypedDict):
    entries: Sequence[BatchGetAssetPropertyAggregatesEntryTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class BatchGetAssetPropertyValueHistoryRequestRequestTypeDef(TypedDict):
    entries: Sequence[BatchGetAssetPropertyValueHistoryEntryTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "id": NotRequired[str],
        "file": NotRequired[ImageFileTypeDef],
    },
)


class DescribeDefaultEncryptionConfigurationResponseTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyArn: str
    configurationStatus: ConfigurationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutDefaultEncryptionConfigurationResponseTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyArn: str
    configurationStatus: ConfigurationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class JobConfigurationOutputTypeDef(TypedDict):
    fileFormat: FileFormatOutputTypeDef


class FileFormatTypeDef(TypedDict):
    csv: NotRequired[CsvUnionTypeDef]
    parquet: NotRequired[Mapping[str, Any]]


class DescribeStorageConfigurationResponseTypeDef(TypedDict):
    storageType: StorageTypeType
    multiLayerStorage: MultiLayerStorageTypeDef
    disassociatedDataStorage: DisassociatedDataStorageStateType
    retentionPeriod: RetentionPeriodTypeDef
    configurationStatus: ConfigurationStatusTypeDef
    lastUpdateDate: datetime
    warmTier: WarmTierStateType
    warmTierRetentionPeriod: WarmTierRetentionPeriodTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutStorageConfigurationRequestRequestTypeDef(TypedDict):
    storageType: StorageTypeType
    multiLayerStorage: NotRequired[MultiLayerStorageTypeDef]
    disassociatedDataStorage: NotRequired[DisassociatedDataStorageStateType]
    retentionPeriod: NotRequired[RetentionPeriodTypeDef]
    warmTier: NotRequired[WarmTierStateType]
    warmTierRetentionPeriod: NotRequired[WarmTierRetentionPeriodTypeDef]


class PutStorageConfigurationResponseTypeDef(TypedDict):
    storageType: StorageTypeType
    multiLayerStorage: MultiLayerStorageTypeDef
    disassociatedDataStorage: DisassociatedDataStorageStateType
    retentionPeriod: RetentionPeriodTypeDef
    configurationStatus: ConfigurationStatusTypeDef
    warmTier: WarmTierStateType
    warmTierRetentionPeriod: WarmTierRetentionPeriodTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ExecuteQueryResponsePaginatorTypeDef(TypedDict):
    columns: List[ColumnInfoTypeDef]
    rows: List[RowPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ExecuteQueryResponseTypeDef(TypedDict):
    columns: List[ColumnInfoTypeDef]
    rows: List[RowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AssetModelStatusTypeDef(TypedDict):
    state: AssetModelStateType
    error: NotRequired[ErrorDetailsTypeDef]


class AssetStatusTypeDef(TypedDict):
    state: AssetStateType
    error: NotRequired[ErrorDetailsTypeDef]


class DatasetStatusTypeDef(TypedDict):
    state: DatasetStateType
    error: NotRequired[ErrorDetailsTypeDef]


class MeasurementTypeDef(TypedDict):
    processingConfig: NotRequired[MeasurementProcessingConfigTypeDef]


class CreateGatewayRequestRequestTypeDef(TypedDict):
    gatewayName: str
    gatewayPlatform: GatewayPlatformTypeDef
    tags: NotRequired[Mapping[str, str]]


class DescribeGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    gatewayName: str
    gatewayArn: str
    gatewayPlatform: GatewayPlatformTypeDef
    gatewayCapabilitySummaries: List[GatewayCapabilitySummaryTypeDef]
    creationDate: datetime
    lastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GatewaySummaryTypeDef(TypedDict):
    gatewayId: str
    gatewayName: str
    creationDate: datetime
    lastUpdateDate: datetime
    gatewayPlatform: NotRequired[GatewayPlatformTypeDef]
    gatewayCapabilitySummaries: NotRequired[List[GatewayCapabilitySummaryTypeDef]]


class DatasetSourceTypeDef(TypedDict):
    sourceType: Literal["KENDRA"]
    sourceFormat: Literal["KNOWLEDGE_BASE"]
    sourceDetail: NotRequired[SourceDetailTypeDef]


class DataSetReferenceTypeDef(TypedDict):
    datasetArn: NotRequired[str]
    source: NotRequired[SourceTypeDef]


class CreatePortalResponseTypeDef(TypedDict):
    portalId: str
    portalArn: str
    portalStartUrl: str
    portalStatus: PortalStatusTypeDef
    ssoApplicationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePortalResponseTypeDef(TypedDict):
    portalStatus: PortalStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePortalResponseTypeDef(TypedDict):
    portalId: str
    portalArn: str
    portalName: str
    portalDescription: str
    portalClientId: str
    portalStartUrl: str
    portalContactEmail: str
    portalStatus: PortalStatusTypeDef
    portalCreationDate: datetime
    portalLastUpdateDate: datetime
    portalLogoImageLocation: ImageLocationTypeDef
    roleArn: str
    portalAuthMode: AuthModeType
    notificationSenderEmail: str
    alarms: AlarmsTypeDef
    portalType: PortalTypeType
    portalTypeConfiguration: Dict[str, PortalTypeEntryOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


PortalSummaryTypeDef = TypedDict(
    "PortalSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "startUrl": str,
        "status": PortalStatusTypeDef,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
        "roleArn": NotRequired[str],
        "portalType": NotRequired[PortalTypeType],
    },
)


class UpdatePortalResponseTypeDef(TypedDict):
    portalStatus: PortalStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePortalRequestRequestTypeDef(TypedDict):
    portalName: str
    portalContactEmail: str
    roleArn: str
    portalDescription: NotRequired[str]
    clientToken: NotRequired[str]
    portalLogoImageFile: NotRequired[ImageFileTypeDef]
    tags: NotRequired[Mapping[str, str]]
    portalAuthMode: NotRequired[AuthModeType]
    notificationSenderEmail: NotRequired[str]
    alarms: NotRequired[AlarmsTypeDef]
    portalType: NotRequired[PortalTypeType]
    portalTypeConfiguration: NotRequired[Mapping[str, PortalTypeEntryUnionTypeDef]]


AccessPolicySummaryTypeDef = TypedDict(
    "AccessPolicySummaryTypeDef",
    {
        "id": str,
        "identity": IdentityTypeDef,
        "resource": ResourceTypeDef,
        "permission": PermissionType,
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)


class CreateAccessPolicyRequestRequestTypeDef(TypedDict):
    accessPolicyIdentity: IdentityTypeDef
    accessPolicyResource: ResourceTypeDef
    accessPolicyPermission: PermissionType
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class DescribeAccessPolicyResponseTypeDef(TypedDict):
    accessPolicyId: str
    accessPolicyArn: str
    accessPolicyIdentity: IdentityTypeDef
    accessPolicyResource: ResourceTypeDef
    accessPolicyPermission: PermissionType
    accessPolicyCreationDate: datetime
    accessPolicyLastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccessPolicyRequestRequestTypeDef(TypedDict):
    accessPolicyId: str
    accessPolicyIdentity: IdentityTypeDef
    accessPolicyResource: ResourceTypeDef
    accessPolicyPermission: PermissionType
    clientToken: NotRequired[str]


class BatchGetAssetPropertyAggregatesResponseTypeDef(TypedDict):
    errorEntries: List[BatchGetAssetPropertyAggregatesErrorEntryTypeDef]
    successEntries: List[BatchGetAssetPropertyAggregatesSuccessEntryTypeDef]
    skippedEntries: List[BatchGetAssetPropertyAggregatesSkippedEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MetricOutputTypeDef(TypedDict):
    expression: str
    variables: List[ExpressionVariableOutputTypeDef]
    window: MetricWindowTypeDef
    processingConfig: NotRequired[MetricProcessingConfigTypeDef]


class TransformOutputTypeDef(TypedDict):
    expression: str
    variables: List[ExpressionVariableOutputTypeDef]
    processingConfig: NotRequired[TransformProcessingConfigTypeDef]


class ExpressionVariableTypeDef(TypedDict):
    name: str
    value: VariableValueUnionTypeDef


class BatchPutAssetPropertyValueResponseTypeDef(TypedDict):
    errorEntries: List[BatchPutAssetPropertyErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetAssetPropertyValueHistoryResponseTypeDef(TypedDict):
    errorEntries: List[BatchGetAssetPropertyValueHistoryErrorEntryTypeDef]
    successEntries: List[BatchGetAssetPropertyValueHistorySuccessEntryTypeDef]
    skippedEntries: List[BatchGetAssetPropertyValueHistorySkippedEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchGetAssetPropertyValueResponseTypeDef(TypedDict):
    errorEntries: List[BatchGetAssetPropertyValueErrorEntryTypeDef]
    successEntries: List[BatchGetAssetPropertyValueSuccessEntryTypeDef]
    skippedEntries: List[BatchGetAssetPropertyValueSkippedEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchPutAssetPropertyValueRequestRequestTypeDef(TypedDict):
    entries: Sequence[PutAssetPropertyValueEntryTypeDef]


class UpdatePortalRequestRequestTypeDef(TypedDict):
    portalId: str
    portalName: str
    portalContactEmail: str
    roleArn: str
    portalDescription: NotRequired[str]
    portalLogoImage: NotRequired[ImageTypeDef]
    clientToken: NotRequired[str]
    notificationSenderEmail: NotRequired[str]
    alarms: NotRequired[AlarmsTypeDef]
    portalType: NotRequired[PortalTypeType]
    portalTypeConfiguration: NotRequired[Mapping[str, PortalTypeEntryTypeDef]]


class DescribeBulkImportJobResponseTypeDef(TypedDict):
    jobId: str
    jobName: str
    jobStatus: JobStatusType
    jobRoleArn: str
    files: List[FileTypeDef]
    errorReportLocation: ErrorReportLocationTypeDef
    jobConfiguration: JobConfigurationOutputTypeDef
    jobCreationDate: datetime
    jobLastUpdateDate: datetime
    adaptiveIngestion: bool
    deleteFilesAfterImport: bool
    ResponseMetadata: ResponseMetadataTypeDef


FileFormatUnionTypeDef = Union[FileFormatTypeDef, FileFormatOutputTypeDef]
AssetModelSummaryTypeDef = TypedDict(
    "AssetModelSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetModelStatusTypeDef,
        "externalId": NotRequired[str],
        "assetModelType": NotRequired[AssetModelTypeType],
        "version": NotRequired[str],
    },
)


class CreateAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelCompositeModelId: str
    assetModelCompositeModelPath: List[AssetModelCompositeModelPathSegmentTypeDef]
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAssetModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelArn: str
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAssetModelResponseTypeDef(TypedDict):
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelCompositeModelPath: List[AssetModelCompositeModelPathSegmentTypeDef]
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssetModelResponseTypeDef(TypedDict):
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AssetSummaryTypeDef = TypedDict(
    "AssetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
        "description": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
AssociatedAssetsSummaryTypeDef = TypedDict(
    "AssociatedAssetsSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
        "description": NotRequired[str],
        "externalId": NotRequired[str],
    },
)


class CreateAssetResponseTypeDef(TypedDict):
    assetId: str
    assetArn: str
    assetStatus: AssetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAssetResponseTypeDef(TypedDict):
    assetStatus: AssetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAssetResponseTypeDef(TypedDict):
    assetId: str
    assetArn: str
    assetName: str
    assetModelId: str
    assetProperties: List[AssetPropertyTypeDef]
    assetHierarchies: List[AssetHierarchyTypeDef]
    assetCompositeModels: List[AssetCompositeModelTypeDef]
    assetCreationDate: datetime
    assetLastUpdateDate: datetime
    assetStatus: AssetStatusTypeDef
    assetDescription: str
    assetCompositeModelSummaries: List[AssetCompositeModelSummaryTypeDef]
    assetExternalId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssetResponseTypeDef(TypedDict):
    assetStatus: AssetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetArn: str
    datasetStatus: DatasetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": DatasetStatusTypeDef,
    },
)


class DeleteDatasetResponseTypeDef(TypedDict):
    datasetStatus: DatasetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetArn: str
    datasetStatus: DatasetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListGatewaysResponseTypeDef(TypedDict):
    gatewaySummaries: List[GatewaySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateDatasetRequestRequestTypeDef(TypedDict):
    datasetName: str
    datasetSource: DatasetSourceTypeDef
    datasetId: NotRequired[str]
    datasetDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class DescribeDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetArn: str
    datasetName: str
    datasetDescription: str
    datasetSource: DatasetSourceTypeDef
    datasetStatus: DatasetStatusTypeDef
    datasetCreationDate: datetime
    datasetLastUpdateDate: datetime
    datasetVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDatasetRequestRequestTypeDef(TypedDict):
    datasetId: str
    datasetName: str
    datasetSource: DatasetSourceTypeDef
    datasetDescription: NotRequired[str]
    clientToken: NotRequired[str]


class ReferenceTypeDef(TypedDict):
    dataset: NotRequired[DataSetReferenceTypeDef]


class ListPortalsResponseTypeDef(TypedDict):
    portalSummaries: List[PortalSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAccessPoliciesResponseTypeDef(TypedDict):
    accessPolicySummaries: List[AccessPolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PropertyTypeOutputTypeDef(TypedDict):
    attribute: NotRequired[AttributeTypeDef]
    measurement: NotRequired[MeasurementTypeDef]
    transform: NotRequired[TransformOutputTypeDef]
    metric: NotRequired[MetricOutputTypeDef]


ExpressionVariableUnionTypeDef = Union[ExpressionVariableTypeDef, ExpressionVariableOutputTypeDef]


class JobConfigurationTypeDef(TypedDict):
    fileFormat: FileFormatUnionTypeDef


class ListAssetModelsResponseTypeDef(TypedDict):
    assetModelSummaries: List[AssetModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssetsResponseTypeDef(TypedDict):
    assetSummaries: List[AssetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssociatedAssetsResponseTypeDef(TypedDict):
    assetSummaries: List[AssociatedAssetsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDatasetsResponseTypeDef(TypedDict):
    datasetSummaries: List[DatasetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CitationTypeDef(TypedDict):
    reference: NotRequired[ReferenceTypeDef]
    content: NotRequired[ContentTypeDef]


AssetModelPropertyOutputTypeDef = TypedDict(
    "AssetModelPropertyOutputTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeOutputTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "path": NotRequired[List[AssetModelPropertyPathSegmentTypeDef]],
    },
)
AssetModelPropertySummaryTypeDef = TypedDict(
    "AssetModelPropertySummaryTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeOutputTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "assetModelCompositeModelId": NotRequired[str],
        "path": NotRequired[List[AssetModelPropertyPathSegmentTypeDef]],
    },
)
PropertyTypeDef = TypedDict(
    "PropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
        "alias": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "unit": NotRequired[str],
        "type": NotRequired[PropertyTypeOutputTypeDef],
        "path": NotRequired[List[AssetPropertyPathSegmentTypeDef]],
        "externalId": NotRequired[str],
    },
)


class MetricTypeDef(TypedDict):
    expression: str
    variables: Sequence[ExpressionVariableUnionTypeDef]
    window: MetricWindowTypeDef
    processingConfig: NotRequired[MetricProcessingConfigTypeDef]


class TransformTypeDef(TypedDict):
    expression: str
    variables: Sequence[ExpressionVariableUnionTypeDef]
    processingConfig: NotRequired[TransformProcessingConfigTypeDef]


class CreateBulkImportJobRequestRequestTypeDef(TypedDict):
    jobName: str
    jobRoleArn: str
    files: Sequence[FileTypeDef]
    errorReportLocation: ErrorReportLocationTypeDef
    jobConfiguration: JobConfigurationTypeDef
    adaptiveIngestion: NotRequired[bool]
    deleteFilesAfterImport: NotRequired[bool]


class InvocationOutputTypeDef(TypedDict):
    message: NotRequired[str]
    citations: NotRequired[List[CitationTypeDef]]


AssetModelCompositeModelOutputTypeDef = TypedDict(
    "AssetModelCompositeModelOutputTypeDef",
    {
        "name": str,
        "type": str,
        "description": NotRequired[str],
        "properties": NotRequired[List[AssetModelPropertyOutputTypeDef]],
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)


class DescribeAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelCompositeModelExternalId: str
    assetModelCompositeModelPath: List[AssetModelCompositeModelPathSegmentTypeDef]
    assetModelCompositeModelName: str
    assetModelCompositeModelDescription: str
    assetModelCompositeModelType: str
    assetModelCompositeModelProperties: List[AssetModelPropertyOutputTypeDef]
    compositionDetails: CompositionDetailsTypeDef
    assetModelCompositeModelSummaries: List[AssetModelCompositeModelSummaryTypeDef]
    actionDefinitions: List[ActionDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssetModelPropertiesResponseTypeDef(TypedDict):
    assetModelPropertySummaries: List[AssetModelPropertySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


CompositeModelPropertyTypeDef = TypedDict(
    "CompositeModelPropertyTypeDef",
    {
        "name": str,
        "type": str,
        "assetProperty": PropertyTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
MetricUnionTypeDef = Union[MetricTypeDef, MetricOutputTypeDef]
TransformUnionTypeDef = Union[TransformTypeDef, TransformOutputTypeDef]


class ResponseStreamTypeDef(TypedDict):
    trace: NotRequired[TraceTypeDef]
    output: NotRequired[InvocationOutputTypeDef]
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    conflictingOperationException: NotRequired[ConflictingOperationExceptionTypeDef]
    internalFailureException: NotRequired[InternalFailureExceptionTypeDef]
    invalidRequestException: NotRequired[InvalidRequestExceptionTypeDef]
    limitExceededException: NotRequired[LimitExceededExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]


class DescribeAssetModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelExternalId: str
    assetModelArn: str
    assetModelName: str
    assetModelType: AssetModelTypeType
    assetModelDescription: str
    assetModelProperties: List[AssetModelPropertyOutputTypeDef]
    assetModelHierarchies: List[AssetModelHierarchyTypeDef]
    assetModelCompositeModels: List[AssetModelCompositeModelOutputTypeDef]
    assetModelCompositeModelSummaries: List[AssetModelCompositeModelSummaryTypeDef]
    assetModelCreationDate: datetime
    assetModelLastUpdateDate: datetime
    assetModelStatus: AssetModelStatusTypeDef
    assetModelVersion: str
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAssetPropertyResponseTypeDef(TypedDict):
    assetId: str
    assetName: str
    assetModelId: str
    assetProperty: PropertyTypeDef
    compositeModel: CompositeModelPropertyTypeDef
    assetExternalId: str
    ResponseMetadata: ResponseMetadataTypeDef


class PropertyTypeTypeDef(TypedDict):
    attribute: NotRequired[AttributeTypeDef]
    measurement: NotRequired[MeasurementTypeDef]
    transform: NotRequired[TransformUnionTypeDef]
    metric: NotRequired[MetricUnionTypeDef]


class InvokeAssistantResponseTypeDef(TypedDict):
    body: "EventStream[ResponseStreamTypeDef]"
    conversationId: str
    ResponseMetadata: ResponseMetadataTypeDef


PropertyTypeUnionTypeDef = Union[PropertyTypeTypeDef, PropertyTypeOutputTypeDef]
AssetModelPropertyDefinitionTypeDef = TypedDict(
    "AssetModelPropertyDefinitionTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeUnionTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
    },
)
AssetModelPropertyTypeDef = TypedDict(
    "AssetModelPropertyTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeUnionTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "path": NotRequired[Sequence[AssetModelPropertyPathSegmentTypeDef]],
    },
)
AssetModelCompositeModelDefinitionTypeDef = TypedDict(
    "AssetModelCompositeModelDefinitionTypeDef",
    {
        "name": str,
        "type": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "description": NotRequired[str],
        "properties": NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]],
    },
)


class CreateAssetModelCompositeModelRequestRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelName: str
    assetModelCompositeModelType: str
    assetModelCompositeModelExternalId: NotRequired[str]
    parentAssetModelCompositeModelId: NotRequired[str]
    assetModelCompositeModelId: NotRequired[str]
    assetModelCompositeModelDescription: NotRequired[str]
    clientToken: NotRequired[str]
    composedAssetModelId: NotRequired[str]
    assetModelCompositeModelProperties: NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]


AssetModelPropertyUnionTypeDef = Union[AssetModelPropertyTypeDef, AssetModelPropertyOutputTypeDef]


class UpdateAssetModelCompositeModelRequestRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelCompositeModelName: str
    assetModelCompositeModelExternalId: NotRequired[str]
    assetModelCompositeModelDescription: NotRequired[str]
    clientToken: NotRequired[str]
    assetModelCompositeModelProperties: NotRequired[Sequence[AssetModelPropertyTypeDef]]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]


class CreateAssetModelRequestRequestTypeDef(TypedDict):
    assetModelName: str
    assetModelType: NotRequired[AssetModelTypeType]
    assetModelId: NotRequired[str]
    assetModelExternalId: NotRequired[str]
    assetModelDescription: NotRequired[str]
    assetModelProperties: NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]]
    assetModelHierarchies: NotRequired[Sequence[AssetModelHierarchyDefinitionTypeDef]]
    assetModelCompositeModels: NotRequired[Sequence[AssetModelCompositeModelDefinitionTypeDef]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


AssetModelCompositeModelTypeDef = TypedDict(
    "AssetModelCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "description": NotRequired[str],
        "properties": NotRequired[Sequence[AssetModelPropertyUnionTypeDef]],
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
AssetModelCompositeModelUnionTypeDef = Union[
    AssetModelCompositeModelTypeDef, AssetModelCompositeModelOutputTypeDef
]


class UpdateAssetModelRequestRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelName: str
    assetModelExternalId: NotRequired[str]
    assetModelDescription: NotRequired[str]
    assetModelProperties: NotRequired[Sequence[AssetModelPropertyUnionTypeDef]]
    assetModelHierarchies: NotRequired[Sequence[AssetModelHierarchyTypeDef]]
    assetModelCompositeModels: NotRequired[Sequence[AssetModelCompositeModelUnionTypeDef]]
    clientToken: NotRequired[str]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]
