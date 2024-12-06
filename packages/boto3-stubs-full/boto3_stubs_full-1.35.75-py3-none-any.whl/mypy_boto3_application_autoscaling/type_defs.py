"""
Type annotations for application-autoscaling service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/type_defs/)

Usage::

    ```python
    from mypy_boto3_application_autoscaling.type_defs import AlarmTypeDef

    data: AlarmTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AdjustmentTypeType,
    MetricAggregationTypeType,
    MetricStatisticType,
    MetricTypeType,
    PolicyTypeType,
    PredictiveScalingMaxCapacityBreachBehaviorType,
    PredictiveScalingModeType,
    ScalableDimensionType,
    ScalingActivityStatusCodeType,
    ServiceNamespaceType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AlarmTypeDef",
    "CapacityForecastTypeDef",
    "CustomizedMetricSpecificationOutputTypeDef",
    "CustomizedMetricSpecificationTypeDef",
    "CustomizedMetricSpecificationUnionTypeDef",
    "DeleteScalingPolicyRequestRequestTypeDef",
    "DeleteScheduledActionRequestRequestTypeDef",
    "DeregisterScalableTargetRequestRequestTypeDef",
    "DescribeScalableTargetsRequestDescribeScalableTargetsPaginateTypeDef",
    "DescribeScalableTargetsRequestRequestTypeDef",
    "DescribeScalableTargetsResponseTypeDef",
    "DescribeScalingActivitiesRequestDescribeScalingActivitiesPaginateTypeDef",
    "DescribeScalingActivitiesRequestRequestTypeDef",
    "DescribeScalingActivitiesResponseTypeDef",
    "DescribeScalingPoliciesRequestDescribeScalingPoliciesPaginateTypeDef",
    "DescribeScalingPoliciesRequestRequestTypeDef",
    "DescribeScalingPoliciesResponseTypeDef",
    "DescribeScheduledActionsRequestDescribeScheduledActionsPaginateTypeDef",
    "DescribeScheduledActionsRequestRequestTypeDef",
    "DescribeScheduledActionsResponseTypeDef",
    "GetPredictiveScalingForecastRequestRequestTypeDef",
    "GetPredictiveScalingForecastResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LoadForecastTypeDef",
    "MetricDimensionTypeDef",
    "NotScaledReasonTypeDef",
    "PaginatorConfigTypeDef",
    "PredefinedMetricSpecificationTypeDef",
    "PredictiveScalingCustomizedMetricSpecificationOutputTypeDef",
    "PredictiveScalingCustomizedMetricSpecificationTypeDef",
    "PredictiveScalingCustomizedMetricSpecificationUnionTypeDef",
    "PredictiveScalingMetricDataQueryOutputTypeDef",
    "PredictiveScalingMetricDataQueryTypeDef",
    "PredictiveScalingMetricDataQueryUnionTypeDef",
    "PredictiveScalingMetricDimensionTypeDef",
    "PredictiveScalingMetricOutputTypeDef",
    "PredictiveScalingMetricSpecificationOutputTypeDef",
    "PredictiveScalingMetricSpecificationTypeDef",
    "PredictiveScalingMetricSpecificationUnionTypeDef",
    "PredictiveScalingMetricStatOutputTypeDef",
    "PredictiveScalingMetricStatTypeDef",
    "PredictiveScalingMetricStatUnionTypeDef",
    "PredictiveScalingMetricTypeDef",
    "PredictiveScalingMetricUnionTypeDef",
    "PredictiveScalingPolicyConfigurationOutputTypeDef",
    "PredictiveScalingPolicyConfigurationTypeDef",
    "PredictiveScalingPredefinedLoadMetricSpecificationTypeDef",
    "PredictiveScalingPredefinedMetricPairSpecificationTypeDef",
    "PredictiveScalingPredefinedScalingMetricSpecificationTypeDef",
    "PutScalingPolicyRequestRequestTypeDef",
    "PutScalingPolicyResponseTypeDef",
    "PutScheduledActionRequestRequestTypeDef",
    "RegisterScalableTargetRequestRequestTypeDef",
    "RegisterScalableTargetResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ScalableTargetActionTypeDef",
    "ScalableTargetTypeDef",
    "ScalingActivityTypeDef",
    "ScalingPolicyTypeDef",
    "ScheduledActionTypeDef",
    "StepAdjustmentTypeDef",
    "StepScalingPolicyConfigurationOutputTypeDef",
    "StepScalingPolicyConfigurationTypeDef",
    "SuspendedStateTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetTrackingMetricDataQueryOutputTypeDef",
    "TargetTrackingMetricDataQueryTypeDef",
    "TargetTrackingMetricDataQueryUnionTypeDef",
    "TargetTrackingMetricDimensionTypeDef",
    "TargetTrackingMetricOutputTypeDef",
    "TargetTrackingMetricStatOutputTypeDef",
    "TargetTrackingMetricStatTypeDef",
    "TargetTrackingMetricStatUnionTypeDef",
    "TargetTrackingMetricTypeDef",
    "TargetTrackingMetricUnionTypeDef",
    "TargetTrackingScalingPolicyConfigurationOutputTypeDef",
    "TargetTrackingScalingPolicyConfigurationTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
)


class AlarmTypeDef(TypedDict):
    AlarmName: str
    AlarmARN: str


class CapacityForecastTypeDef(TypedDict):
    Timestamps: List[datetime]
    Values: List[float]


class MetricDimensionTypeDef(TypedDict):
    Name: str
    Value: str


class DeleteScalingPolicyRequestRequestTypeDef(TypedDict):
    PolicyName: str
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType


class DeleteScheduledActionRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ScheduledActionName: str
    ResourceId: str
    ScalableDimension: ScalableDimensionType


class DeregisterScalableTargetRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeScalableTargetsRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceIds: NotRequired[Sequence[str]]
    ScalableDimension: NotRequired[ScalableDimensionType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DescribeScalingActivitiesRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: NotRequired[str]
    ScalableDimension: NotRequired[ScalableDimensionType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IncludeNotScaledActivities: NotRequired[bool]


class DescribeScalingPoliciesRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    PolicyNames: NotRequired[Sequence[str]]
    ResourceId: NotRequired[str]
    ScalableDimension: NotRequired[ScalableDimensionType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeScheduledActionsRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ScheduledActionNames: NotRequired[Sequence[str]]
    ResourceId: NotRequired[str]
    ScalableDimension: NotRequired[ScalableDimensionType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class NotScaledReasonTypeDef(TypedDict):
    Code: str
    MaxCapacity: NotRequired[int]
    MinCapacity: NotRequired[int]
    CurrentCapacity: NotRequired[int]


class PredefinedMetricSpecificationTypeDef(TypedDict):
    PredefinedMetricType: MetricTypeType
    ResourceLabel: NotRequired[str]


class PredictiveScalingMetricDimensionTypeDef(TypedDict):
    Name: str
    Value: str


class PredictiveScalingPredefinedLoadMetricSpecificationTypeDef(TypedDict):
    PredefinedMetricType: str
    ResourceLabel: NotRequired[str]


class PredictiveScalingPredefinedMetricPairSpecificationTypeDef(TypedDict):
    PredefinedMetricType: str
    ResourceLabel: NotRequired[str]


class PredictiveScalingPredefinedScalingMetricSpecificationTypeDef(TypedDict):
    PredefinedMetricType: str
    ResourceLabel: NotRequired[str]


class ScalableTargetActionTypeDef(TypedDict):
    MinCapacity: NotRequired[int]
    MaxCapacity: NotRequired[int]


class SuspendedStateTypeDef(TypedDict):
    DynamicScalingInSuspended: NotRequired[bool]
    DynamicScalingOutSuspended: NotRequired[bool]
    ScheduledScalingSuspended: NotRequired[bool]


class StepAdjustmentTypeDef(TypedDict):
    ScalingAdjustment: int
    MetricIntervalLowerBound: NotRequired[float]
    MetricIntervalUpperBound: NotRequired[float]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Mapping[str, str]


class TargetTrackingMetricDimensionTypeDef(TypedDict):
    Name: str
    Value: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class DescribeScalableTargetsRequestDescribeScalableTargetsPaginateTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceIds: NotRequired[Sequence[str]]
    ScalableDimension: NotRequired[ScalableDimensionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScalingActivitiesRequestDescribeScalingActivitiesPaginateTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: NotRequired[str]
    ScalableDimension: NotRequired[ScalableDimensionType]
    IncludeNotScaledActivities: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScalingPoliciesRequestDescribeScalingPoliciesPaginateTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    PolicyNames: NotRequired[Sequence[str]]
    ResourceId: NotRequired[str]
    ScalableDimension: NotRequired[ScalableDimensionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScheduledActionsRequestDescribeScheduledActionsPaginateTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ScheduledActionNames: NotRequired[Sequence[str]]
    ResourceId: NotRequired[str]
    ScalableDimension: NotRequired[ScalableDimensionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutScalingPolicyResponseTypeDef(TypedDict):
    PolicyARN: str
    Alarms: List[AlarmTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterScalableTargetResponseTypeDef(TypedDict):
    ScalableTargetARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPredictiveScalingForecastRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    PolicyName: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef


class ScalingActivityTypeDef(TypedDict):
    ActivityId: str
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    Description: str
    Cause: str
    StartTime: datetime
    StatusCode: ScalingActivityStatusCodeType
    EndTime: NotRequired[datetime]
    StatusMessage: NotRequired[str]
    Details: NotRequired[str]
    NotScaledReasons: NotRequired[List[NotScaledReasonTypeDef]]


class PredictiveScalingMetricOutputTypeDef(TypedDict):
    Dimensions: NotRequired[List[PredictiveScalingMetricDimensionTypeDef]]
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]


class PredictiveScalingMetricTypeDef(TypedDict):
    Dimensions: NotRequired[Sequence[PredictiveScalingMetricDimensionTypeDef]]
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]


class PutScheduledActionRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ScheduledActionName: str
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    Schedule: NotRequired[str]
    Timezone: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    ScalableTargetAction: NotRequired[ScalableTargetActionTypeDef]


class ScheduledActionTypeDef(TypedDict):
    ScheduledActionName: str
    ScheduledActionARN: str
    ServiceNamespace: ServiceNamespaceType
    Schedule: str
    ResourceId: str
    CreationTime: datetime
    Timezone: NotRequired[str]
    ScalableDimension: NotRequired[ScalableDimensionType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ScalableTargetAction: NotRequired[ScalableTargetActionTypeDef]


class RegisterScalableTargetRequestRequestTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    MinCapacity: NotRequired[int]
    MaxCapacity: NotRequired[int]
    RoleARN: NotRequired[str]
    SuspendedState: NotRequired[SuspendedStateTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class ScalableTargetTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    MinCapacity: int
    MaxCapacity: int
    RoleARN: str
    CreationTime: datetime
    PredictedCapacity: NotRequired[int]
    SuspendedState: NotRequired[SuspendedStateTypeDef]
    ScalableTargetARN: NotRequired[str]


class StepScalingPolicyConfigurationOutputTypeDef(TypedDict):
    AdjustmentType: NotRequired[AdjustmentTypeType]
    StepAdjustments: NotRequired[List[StepAdjustmentTypeDef]]
    MinAdjustmentMagnitude: NotRequired[int]
    Cooldown: NotRequired[int]
    MetricAggregationType: NotRequired[MetricAggregationTypeType]


class StepScalingPolicyConfigurationTypeDef(TypedDict):
    AdjustmentType: NotRequired[AdjustmentTypeType]
    StepAdjustments: NotRequired[Sequence[StepAdjustmentTypeDef]]
    MinAdjustmentMagnitude: NotRequired[int]
    Cooldown: NotRequired[int]
    MetricAggregationType: NotRequired[MetricAggregationTypeType]


class TargetTrackingMetricOutputTypeDef(TypedDict):
    Dimensions: NotRequired[List[TargetTrackingMetricDimensionTypeDef]]
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]


class TargetTrackingMetricTypeDef(TypedDict):
    Dimensions: NotRequired[Sequence[TargetTrackingMetricDimensionTypeDef]]
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]


class DescribeScalingActivitiesResponseTypeDef(TypedDict):
    ScalingActivities: List[ScalingActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PredictiveScalingMetricStatOutputTypeDef(TypedDict):
    Metric: PredictiveScalingMetricOutputTypeDef
    Stat: str
    Unit: NotRequired[str]


PredictiveScalingMetricUnionTypeDef = Union[
    PredictiveScalingMetricTypeDef, PredictiveScalingMetricOutputTypeDef
]


class DescribeScheduledActionsResponseTypeDef(TypedDict):
    ScheduledActions: List[ScheduledActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeScalableTargetsResponseTypeDef(TypedDict):
    ScalableTargets: List[ScalableTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TargetTrackingMetricStatOutputTypeDef(TypedDict):
    Metric: TargetTrackingMetricOutputTypeDef
    Stat: str
    Unit: NotRequired[str]


TargetTrackingMetricUnionTypeDef = Union[
    TargetTrackingMetricTypeDef, TargetTrackingMetricOutputTypeDef
]


class PredictiveScalingMetricDataQueryOutputTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    MetricStat: NotRequired[PredictiveScalingMetricStatOutputTypeDef]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]


class PredictiveScalingMetricStatTypeDef(TypedDict):
    Metric: PredictiveScalingMetricUnionTypeDef
    Stat: str
    Unit: NotRequired[str]


class TargetTrackingMetricDataQueryOutputTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    Label: NotRequired[str]
    MetricStat: NotRequired[TargetTrackingMetricStatOutputTypeDef]
    ReturnData: NotRequired[bool]


class TargetTrackingMetricStatTypeDef(TypedDict):
    Metric: TargetTrackingMetricUnionTypeDef
    Stat: str
    Unit: NotRequired[str]


class PredictiveScalingCustomizedMetricSpecificationOutputTypeDef(TypedDict):
    MetricDataQueries: List[PredictiveScalingMetricDataQueryOutputTypeDef]


PredictiveScalingMetricStatUnionTypeDef = Union[
    PredictiveScalingMetricStatTypeDef, PredictiveScalingMetricStatOutputTypeDef
]


class CustomizedMetricSpecificationOutputTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]
    Dimensions: NotRequired[List[MetricDimensionTypeDef]]
    Statistic: NotRequired[MetricStatisticType]
    Unit: NotRequired[str]
    Metrics: NotRequired[List[TargetTrackingMetricDataQueryOutputTypeDef]]


TargetTrackingMetricStatUnionTypeDef = Union[
    TargetTrackingMetricStatTypeDef, TargetTrackingMetricStatOutputTypeDef
]


class PredictiveScalingMetricSpecificationOutputTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricPairSpecification: NotRequired[
        PredictiveScalingPredefinedMetricPairSpecificationTypeDef
    ]
    PredefinedScalingMetricSpecification: NotRequired[
        PredictiveScalingPredefinedScalingMetricSpecificationTypeDef
    ]
    PredefinedLoadMetricSpecification: NotRequired[
        PredictiveScalingPredefinedLoadMetricSpecificationTypeDef
    ]
    CustomizedScalingMetricSpecification: NotRequired[
        PredictiveScalingCustomizedMetricSpecificationOutputTypeDef
    ]
    CustomizedLoadMetricSpecification: NotRequired[
        PredictiveScalingCustomizedMetricSpecificationOutputTypeDef
    ]
    CustomizedCapacityMetricSpecification: NotRequired[
        PredictiveScalingCustomizedMetricSpecificationOutputTypeDef
    ]


class PredictiveScalingMetricDataQueryTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    MetricStat: NotRequired[PredictiveScalingMetricStatUnionTypeDef]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]


class TargetTrackingScalingPolicyConfigurationOutputTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricSpecification: NotRequired[PredefinedMetricSpecificationTypeDef]
    CustomizedMetricSpecification: NotRequired[CustomizedMetricSpecificationOutputTypeDef]
    ScaleOutCooldown: NotRequired[int]
    ScaleInCooldown: NotRequired[int]
    DisableScaleIn: NotRequired[bool]


class TargetTrackingMetricDataQueryTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    Label: NotRequired[str]
    MetricStat: NotRequired[TargetTrackingMetricStatUnionTypeDef]
    ReturnData: NotRequired[bool]


class LoadForecastTypeDef(TypedDict):
    Timestamps: List[datetime]
    Values: List[float]
    MetricSpecification: PredictiveScalingMetricSpecificationOutputTypeDef


class PredictiveScalingPolicyConfigurationOutputTypeDef(TypedDict):
    MetricSpecifications: List[PredictiveScalingMetricSpecificationOutputTypeDef]
    Mode: NotRequired[PredictiveScalingModeType]
    SchedulingBufferTime: NotRequired[int]
    MaxCapacityBreachBehavior: NotRequired[PredictiveScalingMaxCapacityBreachBehaviorType]
    MaxCapacityBuffer: NotRequired[int]


PredictiveScalingMetricDataQueryUnionTypeDef = Union[
    PredictiveScalingMetricDataQueryTypeDef, PredictiveScalingMetricDataQueryOutputTypeDef
]
TargetTrackingMetricDataQueryUnionTypeDef = Union[
    TargetTrackingMetricDataQueryTypeDef, TargetTrackingMetricDataQueryOutputTypeDef
]


class GetPredictiveScalingForecastResponseTypeDef(TypedDict):
    LoadForecast: List[LoadForecastTypeDef]
    CapacityForecast: CapacityForecastTypeDef
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ScalingPolicyTypeDef(TypedDict):
    PolicyARN: str
    PolicyName: str
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    PolicyType: PolicyTypeType
    CreationTime: datetime
    StepScalingPolicyConfiguration: NotRequired[StepScalingPolicyConfigurationOutputTypeDef]
    TargetTrackingScalingPolicyConfiguration: NotRequired[
        TargetTrackingScalingPolicyConfigurationOutputTypeDef
    ]
    PredictiveScalingPolicyConfiguration: NotRequired[
        PredictiveScalingPolicyConfigurationOutputTypeDef
    ]
    Alarms: NotRequired[List[AlarmTypeDef]]


class PredictiveScalingCustomizedMetricSpecificationTypeDef(TypedDict):
    MetricDataQueries: Sequence[PredictiveScalingMetricDataQueryUnionTypeDef]


class CustomizedMetricSpecificationTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]
    Dimensions: NotRequired[Sequence[MetricDimensionTypeDef]]
    Statistic: NotRequired[MetricStatisticType]
    Unit: NotRequired[str]
    Metrics: NotRequired[Sequence[TargetTrackingMetricDataQueryUnionTypeDef]]


class DescribeScalingPoliciesResponseTypeDef(TypedDict):
    ScalingPolicies: List[ScalingPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


PredictiveScalingCustomizedMetricSpecificationUnionTypeDef = Union[
    PredictiveScalingCustomizedMetricSpecificationTypeDef,
    PredictiveScalingCustomizedMetricSpecificationOutputTypeDef,
]
CustomizedMetricSpecificationUnionTypeDef = Union[
    CustomizedMetricSpecificationTypeDef, CustomizedMetricSpecificationOutputTypeDef
]


class PredictiveScalingMetricSpecificationTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricPairSpecification: NotRequired[
        PredictiveScalingPredefinedMetricPairSpecificationTypeDef
    ]
    PredefinedScalingMetricSpecification: NotRequired[
        PredictiveScalingPredefinedScalingMetricSpecificationTypeDef
    ]
    PredefinedLoadMetricSpecification: NotRequired[
        PredictiveScalingPredefinedLoadMetricSpecificationTypeDef
    ]
    CustomizedScalingMetricSpecification: NotRequired[
        PredictiveScalingCustomizedMetricSpecificationUnionTypeDef
    ]
    CustomizedLoadMetricSpecification: NotRequired[
        PredictiveScalingCustomizedMetricSpecificationUnionTypeDef
    ]
    CustomizedCapacityMetricSpecification: NotRequired[
        PredictiveScalingCustomizedMetricSpecificationUnionTypeDef
    ]


class TargetTrackingScalingPolicyConfigurationTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricSpecification: NotRequired[PredefinedMetricSpecificationTypeDef]
    CustomizedMetricSpecification: NotRequired[CustomizedMetricSpecificationUnionTypeDef]
    ScaleOutCooldown: NotRequired[int]
    ScaleInCooldown: NotRequired[int]
    DisableScaleIn: NotRequired[bool]


PredictiveScalingMetricSpecificationUnionTypeDef = Union[
    PredictiveScalingMetricSpecificationTypeDef, PredictiveScalingMetricSpecificationOutputTypeDef
]


class PredictiveScalingPolicyConfigurationTypeDef(TypedDict):
    MetricSpecifications: Sequence[PredictiveScalingMetricSpecificationUnionTypeDef]
    Mode: NotRequired[PredictiveScalingModeType]
    SchedulingBufferTime: NotRequired[int]
    MaxCapacityBreachBehavior: NotRequired[PredictiveScalingMaxCapacityBreachBehaviorType]
    MaxCapacityBuffer: NotRequired[int]


class PutScalingPolicyRequestRequestTypeDef(TypedDict):
    PolicyName: str
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    PolicyType: NotRequired[PolicyTypeType]
    StepScalingPolicyConfiguration: NotRequired[StepScalingPolicyConfigurationTypeDef]
    TargetTrackingScalingPolicyConfiguration: NotRequired[
        TargetTrackingScalingPolicyConfigurationTypeDef
    ]
    PredictiveScalingPolicyConfiguration: NotRequired[PredictiveScalingPolicyConfigurationTypeDef]
