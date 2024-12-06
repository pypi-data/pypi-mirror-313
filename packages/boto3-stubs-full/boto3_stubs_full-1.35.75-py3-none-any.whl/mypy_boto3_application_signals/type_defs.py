"""
Type annotations for application-signals service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/type_defs/)

Usage::

    ```python
    from mypy_boto3_application_signals.type_defs import TimestampTypeDef

    data: TimestampTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    DurationUnitType,
    EvaluationTypeType,
    ServiceLevelIndicatorComparisonOperatorType,
    ServiceLevelIndicatorMetricTypeType,
    ServiceLevelObjectiveBudgetStatusType,
    StandardUnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BatchGetServiceLevelObjectiveBudgetReportInputRequestTypeDef",
    "BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef",
    "BurnRateConfigurationTypeDef",
    "CalendarIntervalOutputTypeDef",
    "CalendarIntervalTypeDef",
    "CalendarIntervalUnionTypeDef",
    "CreateServiceLevelObjectiveInputRequestTypeDef",
    "CreateServiceLevelObjectiveOutputTypeDef",
    "DeleteServiceLevelObjectiveInputRequestTypeDef",
    "DimensionTypeDef",
    "GetServiceInputRequestTypeDef",
    "GetServiceLevelObjectiveInputRequestTypeDef",
    "GetServiceLevelObjectiveOutputTypeDef",
    "GetServiceOutputTypeDef",
    "GoalOutputTypeDef",
    "GoalTypeDef",
    "IntervalOutputTypeDef",
    "IntervalTypeDef",
    "IntervalUnionTypeDef",
    "ListServiceDependenciesInputListServiceDependenciesPaginateTypeDef",
    "ListServiceDependenciesInputRequestTypeDef",
    "ListServiceDependenciesOutputTypeDef",
    "ListServiceDependentsInputListServiceDependentsPaginateTypeDef",
    "ListServiceDependentsInputRequestTypeDef",
    "ListServiceDependentsOutputTypeDef",
    "ListServiceLevelObjectivesInputListServiceLevelObjectivesPaginateTypeDef",
    "ListServiceLevelObjectivesInputRequestTypeDef",
    "ListServiceLevelObjectivesOutputTypeDef",
    "ListServiceOperationsInputListServiceOperationsPaginateTypeDef",
    "ListServiceOperationsInputRequestTypeDef",
    "ListServiceOperationsOutputTypeDef",
    "ListServicesInputListServicesPaginateTypeDef",
    "ListServicesInputRequestTypeDef",
    "ListServicesOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricDataQueryOutputTypeDef",
    "MetricDataQueryTypeDef",
    "MetricDataQueryUnionTypeDef",
    "MetricOutputTypeDef",
    "MetricReferenceTypeDef",
    "MetricStatOutputTypeDef",
    "MetricStatTypeDef",
    "MetricStatUnionTypeDef",
    "MetricTypeDef",
    "MetricUnionTypeDef",
    "MonitoredRequestCountMetricDataQueriesOutputTypeDef",
    "MonitoredRequestCountMetricDataQueriesTypeDef",
    "MonitoredRequestCountMetricDataQueriesUnionTypeDef",
    "PaginatorConfigTypeDef",
    "RequestBasedServiceLevelIndicatorConfigTypeDef",
    "RequestBasedServiceLevelIndicatorMetricConfigTypeDef",
    "RequestBasedServiceLevelIndicatorMetricTypeDef",
    "RequestBasedServiceLevelIndicatorTypeDef",
    "ResponseMetadataTypeDef",
    "RollingIntervalTypeDef",
    "ServiceDependencyTypeDef",
    "ServiceDependentTypeDef",
    "ServiceLevelIndicatorConfigTypeDef",
    "ServiceLevelIndicatorMetricConfigTypeDef",
    "ServiceLevelIndicatorMetricTypeDef",
    "ServiceLevelIndicatorTypeDef",
    "ServiceLevelObjectiveBudgetReportErrorTypeDef",
    "ServiceLevelObjectiveBudgetReportTypeDef",
    "ServiceLevelObjectiveSummaryTypeDef",
    "ServiceLevelObjectiveTypeDef",
    "ServiceOperationTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateServiceLevelObjectiveInputRequestTypeDef",
    "UpdateServiceLevelObjectiveOutputTypeDef",
)

TimestampTypeDef = Union[datetime, str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ServiceLevelObjectiveBudgetReportErrorTypeDef(TypedDict):
    Name: str
    Arn: str
    ErrorCode: str
    ErrorMessage: str


class BurnRateConfigurationTypeDef(TypedDict):
    LookBackWindowMinutes: int


class CalendarIntervalOutputTypeDef(TypedDict):
    StartTime: datetime
    DurationUnit: DurationUnitType
    Duration: int


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class DeleteServiceLevelObjectiveInputRequestTypeDef(TypedDict):
    Id: str


class DimensionTypeDef(TypedDict):
    Name: str
    Value: str


class GetServiceLevelObjectiveInputRequestTypeDef(TypedDict):
    Id: str


class RollingIntervalTypeDef(TypedDict):
    DurationUnit: DurationUnitType
    Duration: int


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListServiceLevelObjectivesInputRequestTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ServiceLevelObjectiveSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    KeyAttributes: NotRequired[Dict[str, str]]
    OperationName: NotRequired[str]
    CreatedTime: NotRequired[datetime]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class BatchGetServiceLevelObjectiveBudgetReportInputRequestTypeDef(TypedDict):
    Timestamp: TimestampTypeDef
    SloIds: Sequence[str]


class CalendarIntervalTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    DurationUnit: DurationUnitType
    Duration: int


class GetServiceInputRequestTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]


class ListServiceDependenciesInputRequestTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListServiceDependentsInputRequestTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListServiceOperationsInputRequestTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListServicesInputRequestTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class MetricOutputTypeDef(TypedDict):
    Namespace: NotRequired[str]
    MetricName: NotRequired[str]
    Dimensions: NotRequired[List[DimensionTypeDef]]


class MetricReferenceTypeDef(TypedDict):
    Namespace: str
    MetricType: str
    MetricName: str
    Dimensions: NotRequired[List[DimensionTypeDef]]


class MetricTypeDef(TypedDict):
    Namespace: NotRequired[str]
    MetricName: NotRequired[str]
    Dimensions: NotRequired[Sequence[DimensionTypeDef]]


class IntervalOutputTypeDef(TypedDict):
    RollingInterval: NotRequired[RollingIntervalTypeDef]
    CalendarInterval: NotRequired[CalendarIntervalOutputTypeDef]


class ListServiceDependenciesInputListServiceDependenciesPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceDependentsInputListServiceDependentsPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceLevelObjectivesInputListServiceLevelObjectivesPaginateTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceOperationsInputListServiceOperationsPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServicesInputListServicesPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceLevelObjectivesOutputTypeDef(TypedDict):
    SloSummaries: List[ServiceLevelObjectiveSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CalendarIntervalUnionTypeDef = Union[CalendarIntervalTypeDef, CalendarIntervalOutputTypeDef]


class MetricStatOutputTypeDef(TypedDict):
    Metric: MetricOutputTypeDef
    Period: int
    Stat: str
    Unit: NotRequired[StandardUnitType]


class ServiceDependencyTypeDef(TypedDict):
    OperationName: str
    DependencyKeyAttributes: Dict[str, str]
    DependencyOperationName: str
    MetricReferences: List[MetricReferenceTypeDef]


class ServiceDependentTypeDef(TypedDict):
    DependentKeyAttributes: Dict[str, str]
    MetricReferences: List[MetricReferenceTypeDef]
    OperationName: NotRequired[str]
    DependentOperationName: NotRequired[str]


class ServiceOperationTypeDef(TypedDict):
    Name: str
    MetricReferences: List[MetricReferenceTypeDef]


class ServiceSummaryTypeDef(TypedDict):
    KeyAttributes: Dict[str, str]
    MetricReferences: List[MetricReferenceTypeDef]
    AttributeMaps: NotRequired[List[Dict[str, str]]]


class ServiceTypeDef(TypedDict):
    KeyAttributes: Dict[str, str]
    MetricReferences: List[MetricReferenceTypeDef]
    AttributeMaps: NotRequired[List[Dict[str, str]]]
    LogGroupReferences: NotRequired[List[Dict[str, str]]]


MetricUnionTypeDef = Union[MetricTypeDef, MetricOutputTypeDef]


class GoalOutputTypeDef(TypedDict):
    Interval: NotRequired[IntervalOutputTypeDef]
    AttainmentGoal: NotRequired[float]
    WarningThreshold: NotRequired[float]


class IntervalTypeDef(TypedDict):
    RollingInterval: NotRequired[RollingIntervalTypeDef]
    CalendarInterval: NotRequired[CalendarIntervalUnionTypeDef]


class MetricDataQueryOutputTypeDef(TypedDict):
    Id: str
    MetricStat: NotRequired[MetricStatOutputTypeDef]
    Expression: NotRequired[str]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]
    Period: NotRequired[int]
    AccountId: NotRequired[str]


class ListServiceDependenciesOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceDependencies: List[ServiceDependencyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListServiceDependentsOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceDependents: List[ServiceDependentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListServiceOperationsOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceOperations: List[ServiceOperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListServicesOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceSummaries: List[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetServiceOutputTypeDef(TypedDict):
    Service: ServiceTypeDef
    StartTime: datetime
    EndTime: datetime
    LogGroupReferences: List[Dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef


class MetricStatTypeDef(TypedDict):
    Metric: MetricUnionTypeDef
    Period: int
    Stat: str
    Unit: NotRequired[StandardUnitType]


IntervalUnionTypeDef = Union[IntervalTypeDef, IntervalOutputTypeDef]


class MonitoredRequestCountMetricDataQueriesOutputTypeDef(TypedDict):
    GoodCountMetric: NotRequired[List[MetricDataQueryOutputTypeDef]]
    BadCountMetric: NotRequired[List[MetricDataQueryOutputTypeDef]]


class ServiceLevelIndicatorMetricTypeDef(TypedDict):
    MetricDataQueries: List[MetricDataQueryOutputTypeDef]
    KeyAttributes: NotRequired[Dict[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]


MetricStatUnionTypeDef = Union[MetricStatTypeDef, MetricStatOutputTypeDef]


class GoalTypeDef(TypedDict):
    Interval: NotRequired[IntervalUnionTypeDef]
    AttainmentGoal: NotRequired[float]
    WarningThreshold: NotRequired[float]


class RequestBasedServiceLevelIndicatorMetricTypeDef(TypedDict):
    TotalRequestCountMetric: List[MetricDataQueryOutputTypeDef]
    MonitoredRequestCountMetric: MonitoredRequestCountMetricDataQueriesOutputTypeDef
    KeyAttributes: NotRequired[Dict[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]


class ServiceLevelIndicatorTypeDef(TypedDict):
    SliMetric: ServiceLevelIndicatorMetricTypeDef
    MetricThreshold: float
    ComparisonOperator: ServiceLevelIndicatorComparisonOperatorType


class MetricDataQueryTypeDef(TypedDict):
    Id: str
    MetricStat: NotRequired[MetricStatUnionTypeDef]
    Expression: NotRequired[str]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]
    Period: NotRequired[int]
    AccountId: NotRequired[str]


class RequestBasedServiceLevelIndicatorTypeDef(TypedDict):
    RequestBasedSliMetric: RequestBasedServiceLevelIndicatorMetricTypeDef
    MetricThreshold: NotRequired[float]
    ComparisonOperator: NotRequired[ServiceLevelIndicatorComparisonOperatorType]


MetricDataQueryUnionTypeDef = Union[MetricDataQueryTypeDef, MetricDataQueryOutputTypeDef]


class MonitoredRequestCountMetricDataQueriesTypeDef(TypedDict):
    GoodCountMetric: NotRequired[Sequence[MetricDataQueryTypeDef]]
    BadCountMetric: NotRequired[Sequence[MetricDataQueryTypeDef]]


class ServiceLevelObjectiveBudgetReportTypeDef(TypedDict):
    Arn: str
    Name: str
    BudgetStatus: ServiceLevelObjectiveBudgetStatusType
    EvaluationType: NotRequired[EvaluationTypeType]
    Attainment: NotRequired[float]
    TotalBudgetSeconds: NotRequired[int]
    BudgetSecondsRemaining: NotRequired[int]
    TotalBudgetRequests: NotRequired[int]
    BudgetRequestsRemaining: NotRequired[int]
    Sli: NotRequired[ServiceLevelIndicatorTypeDef]
    RequestBasedSli: NotRequired[RequestBasedServiceLevelIndicatorTypeDef]
    Goal: NotRequired[GoalOutputTypeDef]


class ServiceLevelObjectiveTypeDef(TypedDict):
    Arn: str
    Name: str
    CreatedTime: datetime
    LastUpdatedTime: datetime
    Goal: GoalOutputTypeDef
    Description: NotRequired[str]
    Sli: NotRequired[ServiceLevelIndicatorTypeDef]
    RequestBasedSli: NotRequired[RequestBasedServiceLevelIndicatorTypeDef]
    EvaluationType: NotRequired[EvaluationTypeType]
    BurnRateConfigurations: NotRequired[List[BurnRateConfigurationTypeDef]]


class ServiceLevelIndicatorMetricConfigTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]
    Statistic: NotRequired[str]
    PeriodSeconds: NotRequired[int]
    MetricDataQueries: NotRequired[Sequence[MetricDataQueryUnionTypeDef]]


MonitoredRequestCountMetricDataQueriesUnionTypeDef = Union[
    MonitoredRequestCountMetricDataQueriesTypeDef,
    MonitoredRequestCountMetricDataQueriesOutputTypeDef,
]


class BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef(TypedDict):
    Timestamp: datetime
    Reports: List[ServiceLevelObjectiveBudgetReportTypeDef]
    Errors: List[ServiceLevelObjectiveBudgetReportErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateServiceLevelObjectiveOutputTypeDef(TypedDict):
    Slo: ServiceLevelObjectiveTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetServiceLevelObjectiveOutputTypeDef(TypedDict):
    Slo: ServiceLevelObjectiveTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateServiceLevelObjectiveOutputTypeDef(TypedDict):
    Slo: ServiceLevelObjectiveTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ServiceLevelIndicatorConfigTypeDef(TypedDict):
    SliMetricConfig: ServiceLevelIndicatorMetricConfigTypeDef
    MetricThreshold: float
    ComparisonOperator: ServiceLevelIndicatorComparisonOperatorType


class RequestBasedServiceLevelIndicatorMetricConfigTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]
    TotalRequestCountMetric: NotRequired[Sequence[MetricDataQueryUnionTypeDef]]
    MonitoredRequestCountMetric: NotRequired[MonitoredRequestCountMetricDataQueriesUnionTypeDef]


class RequestBasedServiceLevelIndicatorConfigTypeDef(TypedDict):
    RequestBasedSliMetricConfig: RequestBasedServiceLevelIndicatorMetricConfigTypeDef
    MetricThreshold: NotRequired[float]
    ComparisonOperator: NotRequired[ServiceLevelIndicatorComparisonOperatorType]


class CreateServiceLevelObjectiveInputRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    SliConfig: NotRequired[ServiceLevelIndicatorConfigTypeDef]
    RequestBasedSliConfig: NotRequired[RequestBasedServiceLevelIndicatorConfigTypeDef]
    Goal: NotRequired[GoalTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    BurnRateConfigurations: NotRequired[Sequence[BurnRateConfigurationTypeDef]]


class UpdateServiceLevelObjectiveInputRequestTypeDef(TypedDict):
    Id: str
    Description: NotRequired[str]
    SliConfig: NotRequired[ServiceLevelIndicatorConfigTypeDef]
    RequestBasedSliConfig: NotRequired[RequestBasedServiceLevelIndicatorConfigTypeDef]
    Goal: NotRequired[GoalTypeDef]
    BurnRateConfigurations: NotRequired[Sequence[BurnRateConfigurationTypeDef]]
