"""
Type annotations for rum service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/type_defs/)

Usage::

    ```python
    from mypy_boto3_rum.type_defs import AppMonitorConfigurationOutputTypeDef

    data: AppMonitorConfigurationOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import CustomEventsStatusType, MetricDestinationType, StateEnumType, TelemetryType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AppMonitorConfigurationOutputTypeDef",
    "AppMonitorConfigurationTypeDef",
    "AppMonitorDetailsTypeDef",
    "AppMonitorSummaryTypeDef",
    "AppMonitorTypeDef",
    "BatchCreateRumMetricDefinitionsErrorTypeDef",
    "BatchCreateRumMetricDefinitionsRequestRequestTypeDef",
    "BatchCreateRumMetricDefinitionsResponseTypeDef",
    "BatchDeleteRumMetricDefinitionsErrorTypeDef",
    "BatchDeleteRumMetricDefinitionsRequestRequestTypeDef",
    "BatchDeleteRumMetricDefinitionsResponseTypeDef",
    "BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef",
    "BatchGetRumMetricDefinitionsRequestRequestTypeDef",
    "BatchGetRumMetricDefinitionsResponseTypeDef",
    "CreateAppMonitorRequestRequestTypeDef",
    "CreateAppMonitorResponseTypeDef",
    "CustomEventsTypeDef",
    "CwLogTypeDef",
    "DataStorageTypeDef",
    "DeleteAppMonitorRequestRequestTypeDef",
    "DeleteRumMetricsDestinationRequestRequestTypeDef",
    "GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef",
    "GetAppMonitorDataRequestRequestTypeDef",
    "GetAppMonitorDataResponseTypeDef",
    "GetAppMonitorRequestRequestTypeDef",
    "GetAppMonitorResponseTypeDef",
    "ListAppMonitorsRequestListAppMonitorsPaginateTypeDef",
    "ListAppMonitorsRequestRequestTypeDef",
    "ListAppMonitorsResponseTypeDef",
    "ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef",
    "ListRumMetricsDestinationsRequestRequestTypeDef",
    "ListRumMetricsDestinationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricDefinitionRequestOutputTypeDef",
    "MetricDefinitionRequestTypeDef",
    "MetricDefinitionRequestUnionTypeDef",
    "MetricDefinitionTypeDef",
    "MetricDestinationSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PutRumEventsRequestRequestTypeDef",
    "PutRumMetricsDestinationRequestRequestTypeDef",
    "QueryFilterTypeDef",
    "ResponseMetadataTypeDef",
    "RumEventTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimeRangeTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppMonitorRequestRequestTypeDef",
    "UpdateRumMetricDefinitionRequestRequestTypeDef",
    "UserDetailsTypeDef",
)

class AppMonitorConfigurationOutputTypeDef(TypedDict):
    AllowCookies: NotRequired[bool]
    EnableXRay: NotRequired[bool]
    ExcludedPages: NotRequired[List[str]]
    FavoritePages: NotRequired[List[str]]
    GuestRoleArn: NotRequired[str]
    IdentityPoolId: NotRequired[str]
    IncludedPages: NotRequired[List[str]]
    SessionSampleRate: NotRequired[float]
    Telemetries: NotRequired[List[TelemetryType]]

class AppMonitorConfigurationTypeDef(TypedDict):
    AllowCookies: NotRequired[bool]
    EnableXRay: NotRequired[bool]
    ExcludedPages: NotRequired[Sequence[str]]
    FavoritePages: NotRequired[Sequence[str]]
    GuestRoleArn: NotRequired[str]
    IdentityPoolId: NotRequired[str]
    IncludedPages: NotRequired[Sequence[str]]
    SessionSampleRate: NotRequired[float]
    Telemetries: NotRequired[Sequence[TelemetryType]]

AppMonitorDetailsTypeDef = TypedDict(
    "AppMonitorDetailsTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "version": NotRequired[str],
    },
)

class AppMonitorSummaryTypeDef(TypedDict):
    Created: NotRequired[str]
    Id: NotRequired[str]
    LastModified: NotRequired[str]
    Name: NotRequired[str]
    State: NotRequired[StateEnumType]

class CustomEventsTypeDef(TypedDict):
    Status: NotRequired[CustomEventsStatusType]

class MetricDefinitionRequestOutputTypeDef(TypedDict):
    Name: str
    DimensionKeys: NotRequired[Dict[str, str]]
    EventPattern: NotRequired[str]
    Namespace: NotRequired[str]
    UnitLabel: NotRequired[str]
    ValueKey: NotRequired[str]

class MetricDefinitionTypeDef(TypedDict):
    MetricDefinitionId: str
    Name: str
    DimensionKeys: NotRequired[Dict[str, str]]
    EventPattern: NotRequired[str]
    Namespace: NotRequired[str]
    UnitLabel: NotRequired[str]
    ValueKey: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchDeleteRumMetricDefinitionsErrorTypeDef(TypedDict):
    ErrorCode: str
    ErrorMessage: str
    MetricDefinitionId: str

class BatchDeleteRumMetricDefinitionsRequestRequestTypeDef(TypedDict):
    AppMonitorName: str
    Destination: MetricDestinationType
    MetricDefinitionIds: Sequence[str]
    DestinationArn: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class BatchGetRumMetricDefinitionsRequestRequestTypeDef(TypedDict):
    AppMonitorName: str
    Destination: MetricDestinationType
    DestinationArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class CwLogTypeDef(TypedDict):
    CwLogEnabled: NotRequired[bool]
    CwLogGroup: NotRequired[str]

class DeleteAppMonitorRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteRumMetricsDestinationRequestRequestTypeDef(TypedDict):
    AppMonitorName: str
    Destination: MetricDestinationType
    DestinationArn: NotRequired[str]

class QueryFilterTypeDef(TypedDict):
    Name: NotRequired[str]
    Values: NotRequired[Sequence[str]]

class TimeRangeTypeDef(TypedDict):
    After: int
    Before: NotRequired[int]

class GetAppMonitorRequestRequestTypeDef(TypedDict):
    Name: str

class ListAppMonitorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRumMetricsDestinationsRequestRequestTypeDef(TypedDict):
    AppMonitorName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class MetricDestinationSummaryTypeDef(TypedDict):
    Destination: NotRequired[MetricDestinationType]
    DestinationArn: NotRequired[str]
    IamRoleArn: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class MetricDefinitionRequestTypeDef(TypedDict):
    Name: str
    DimensionKeys: NotRequired[Mapping[str, str]]
    EventPattern: NotRequired[str]
    Namespace: NotRequired[str]
    UnitLabel: NotRequired[str]
    ValueKey: NotRequired[str]

class UserDetailsTypeDef(TypedDict):
    sessionId: NotRequired[str]
    userId: NotRequired[str]

class PutRumMetricsDestinationRequestRequestTypeDef(TypedDict):
    AppMonitorName: str
    Destination: MetricDestinationType
    DestinationArn: NotRequired[str]
    IamRoleArn: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class CreateAppMonitorRequestRequestTypeDef(TypedDict):
    Domain: str
    Name: str
    AppMonitorConfiguration: NotRequired[AppMonitorConfigurationTypeDef]
    CustomEvents: NotRequired[CustomEventsTypeDef]
    CwLogEnabled: NotRequired[bool]
    Tags: NotRequired[Mapping[str, str]]

class UpdateAppMonitorRequestRequestTypeDef(TypedDict):
    Name: str
    AppMonitorConfiguration: NotRequired[AppMonitorConfigurationTypeDef]
    CustomEvents: NotRequired[CustomEventsTypeDef]
    CwLogEnabled: NotRequired[bool]
    Domain: NotRequired[str]

class BatchCreateRumMetricDefinitionsErrorTypeDef(TypedDict):
    ErrorCode: str
    ErrorMessage: str
    MetricDefinition: MetricDefinitionRequestOutputTypeDef

class BatchGetRumMetricDefinitionsResponseTypeDef(TypedDict):
    MetricDefinitions: List[MetricDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateAppMonitorResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppMonitorDataResponseTypeDef(TypedDict):
    Events: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAppMonitorsResponseTypeDef(TypedDict):
    AppMonitorSummaries: List[AppMonitorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceArn: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteRumMetricDefinitionsResponseTypeDef(TypedDict):
    Errors: List[BatchDeleteRumMetricDefinitionsErrorTypeDef]
    MetricDefinitionIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef(TypedDict):
    AppMonitorName: str
    Destination: MetricDestinationType
    DestinationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAppMonitorsRequestListAppMonitorsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef(TypedDict):
    AppMonitorName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DataStorageTypeDef(TypedDict):
    CwLog: NotRequired[CwLogTypeDef]

class GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef(TypedDict):
    Name: str
    TimeRange: TimeRangeTypeDef
    Filters: NotRequired[Sequence[QueryFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetAppMonitorDataRequestRequestTypeDef(TypedDict):
    Name: str
    TimeRange: TimeRangeTypeDef
    Filters: NotRequired[Sequence[QueryFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRumMetricsDestinationsResponseTypeDef(TypedDict):
    Destinations: List[MetricDestinationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

MetricDefinitionRequestUnionTypeDef = Union[
    MetricDefinitionRequestTypeDef, MetricDefinitionRequestOutputTypeDef
]

class UpdateRumMetricDefinitionRequestRequestTypeDef(TypedDict):
    AppMonitorName: str
    Destination: MetricDestinationType
    MetricDefinition: MetricDefinitionRequestTypeDef
    MetricDefinitionId: str
    DestinationArn: NotRequired[str]

RumEventTypeDef = TypedDict(
    "RumEventTypeDef",
    {
        "details": str,
        "id": str,
        "timestamp": TimestampTypeDef,
        "type": str,
        "metadata": NotRequired[str],
    },
)

class BatchCreateRumMetricDefinitionsResponseTypeDef(TypedDict):
    Errors: List[BatchCreateRumMetricDefinitionsErrorTypeDef]
    MetricDefinitions: List[MetricDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AppMonitorTypeDef(TypedDict):
    AppMonitorConfiguration: NotRequired[AppMonitorConfigurationOutputTypeDef]
    Created: NotRequired[str]
    CustomEvents: NotRequired[CustomEventsTypeDef]
    DataStorage: NotRequired[DataStorageTypeDef]
    Domain: NotRequired[str]
    Id: NotRequired[str]
    LastModified: NotRequired[str]
    Name: NotRequired[str]
    State: NotRequired[StateEnumType]
    Tags: NotRequired[Dict[str, str]]

class BatchCreateRumMetricDefinitionsRequestRequestTypeDef(TypedDict):
    AppMonitorName: str
    Destination: MetricDestinationType
    MetricDefinitions: Sequence[MetricDefinitionRequestUnionTypeDef]
    DestinationArn: NotRequired[str]

class PutRumEventsRequestRequestTypeDef(TypedDict):
    AppMonitorDetails: AppMonitorDetailsTypeDef
    BatchId: str
    Id: str
    RumEvents: Sequence[RumEventTypeDef]
    UserDetails: UserDetailsTypeDef

class GetAppMonitorResponseTypeDef(TypedDict):
    AppMonitor: AppMonitorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
