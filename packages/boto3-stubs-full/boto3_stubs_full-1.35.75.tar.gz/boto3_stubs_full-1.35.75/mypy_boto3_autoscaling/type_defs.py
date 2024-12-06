"""
Type annotations for autoscaling service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/type_defs/)

Usage::

    ```python
    from mypy_boto3_autoscaling.type_defs import AcceleratorCountRequestTypeDef

    data: AcceleratorCountRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AcceleratorManufacturerType,
    AcceleratorNameType,
    AcceleratorTypeType,
    BareMetalType,
    BurstablePerformanceType,
    CapacityDistributionStrategyType,
    CapacityReservationPreferenceType,
    CpuManufacturerType,
    ImpairedZoneHealthCheckBehaviorType,
    InstanceGenerationType,
    InstanceMetadataEndpointStateType,
    InstanceMetadataHttpTokensStateType,
    InstanceRefreshStatusType,
    LifecycleStateType,
    LocalStorageType,
    LocalStorageTypeType,
    MetricStatisticType,
    MetricTypeType,
    PredefinedLoadMetricTypeType,
    PredefinedMetricPairTypeType,
    PredefinedScalingMetricTypeType,
    PredictiveScalingMaxCapacityBreachBehaviorType,
    PredictiveScalingModeType,
    ScaleInProtectedInstancesType,
    ScalingActivityStatusCodeType,
    StandbyInstancesType,
    WarmPoolStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceleratorCountRequestTypeDef",
    "AcceleratorTotalMemoryMiBRequestTypeDef",
    "ActivitiesTypeTypeDef",
    "ActivityTypeDef",
    "ActivityTypeTypeDef",
    "AdjustmentTypeTypeDef",
    "AlarmSpecificationOutputTypeDef",
    "AlarmSpecificationTypeDef",
    "AlarmSpecificationUnionTypeDef",
    "AlarmTypeDef",
    "AttachInstancesQueryRequestTypeDef",
    "AttachLoadBalancerTargetGroupsTypeRequestTypeDef",
    "AttachLoadBalancersTypeRequestTypeDef",
    "AttachTrafficSourcesTypeRequestTypeDef",
    "AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef",
    "AutoScalingGroupNamesTypeRequestTypeDef",
    "AutoScalingGroupTypeDef",
    "AutoScalingGroupsTypeTypeDef",
    "AutoScalingInstanceDetailsTypeDef",
    "AutoScalingInstancesTypeTypeDef",
    "AvailabilityZoneDistributionTypeDef",
    "AvailabilityZoneImpairmentPolicyTypeDef",
    "BaselineEbsBandwidthMbpsRequestTypeDef",
    "BaselinePerformanceFactorsRequestOutputTypeDef",
    "BaselinePerformanceFactorsRequestTypeDef",
    "BaselinePerformanceFactorsRequestUnionTypeDef",
    "BatchDeleteScheduledActionAnswerTypeDef",
    "BatchDeleteScheduledActionTypeRequestTypeDef",
    "BatchPutScheduledUpdateGroupActionAnswerTypeDef",
    "BatchPutScheduledUpdateGroupActionTypeRequestTypeDef",
    "BlockDeviceMappingTypeDef",
    "CancelInstanceRefreshAnswerTypeDef",
    "CancelInstanceRefreshTypeRequestTypeDef",
    "CapacityForecastTypeDef",
    "CapacityReservationSpecificationOutputTypeDef",
    "CapacityReservationSpecificationTypeDef",
    "CapacityReservationTargetOutputTypeDef",
    "CapacityReservationTargetTypeDef",
    "CapacityReservationTargetUnionTypeDef",
    "CompleteLifecycleActionTypeRequestTypeDef",
    "CpuPerformanceFactorRequestOutputTypeDef",
    "CpuPerformanceFactorRequestTypeDef",
    "CpuPerformanceFactorRequestUnionTypeDef",
    "CreateAutoScalingGroupTypeRequestTypeDef",
    "CreateLaunchConfigurationTypeRequestTypeDef",
    "CreateOrUpdateTagsTypeRequestTypeDef",
    "CustomizedMetricSpecificationOutputTypeDef",
    "CustomizedMetricSpecificationTypeDef",
    "CustomizedMetricSpecificationUnionTypeDef",
    "DeleteAutoScalingGroupTypeRequestTypeDef",
    "DeleteLifecycleHookTypeRequestTypeDef",
    "DeleteNotificationConfigurationTypeRequestTypeDef",
    "DeletePolicyTypeRequestTypeDef",
    "DeleteScheduledActionTypeRequestTypeDef",
    "DeleteTagsTypeRequestTypeDef",
    "DeleteWarmPoolTypeRequestTypeDef",
    "DescribeAccountLimitsAnswerTypeDef",
    "DescribeAdjustmentTypesAnswerTypeDef",
    "DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef",
    "DescribeAutoScalingInstancesTypeRequestTypeDef",
    "DescribeAutoScalingNotificationTypesAnswerTypeDef",
    "DescribeInstanceRefreshesAnswerTypeDef",
    "DescribeInstanceRefreshesTypeRequestTypeDef",
    "DescribeLifecycleHookTypesAnswerTypeDef",
    "DescribeLifecycleHooksAnswerTypeDef",
    "DescribeLifecycleHooksTypeRequestTypeDef",
    "DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef",
    "DescribeLoadBalancerTargetGroupsRequestRequestTypeDef",
    "DescribeLoadBalancerTargetGroupsResponseTypeDef",
    "DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef",
    "DescribeLoadBalancersRequestRequestTypeDef",
    "DescribeLoadBalancersResponseTypeDef",
    "DescribeMetricCollectionTypesAnswerTypeDef",
    "DescribeNotificationConfigurationsAnswerTypeDef",
    "DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef",
    "DescribeNotificationConfigurationsTypeRequestTypeDef",
    "DescribePoliciesTypeDescribePoliciesPaginateTypeDef",
    "DescribePoliciesTypeRequestTypeDef",
    "DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef",
    "DescribeScalingActivitiesTypeRequestTypeDef",
    "DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef",
    "DescribeScheduledActionsTypeRequestTypeDef",
    "DescribeTagsTypeDescribeTagsPaginateTypeDef",
    "DescribeTagsTypeRequestTypeDef",
    "DescribeTerminationPolicyTypesAnswerTypeDef",
    "DescribeTrafficSourcesRequestRequestTypeDef",
    "DescribeTrafficSourcesResponseTypeDef",
    "DescribeWarmPoolAnswerTypeDef",
    "DescribeWarmPoolTypeDescribeWarmPoolPaginateTypeDef",
    "DescribeWarmPoolTypeRequestTypeDef",
    "DesiredConfigurationOutputTypeDef",
    "DesiredConfigurationTypeDef",
    "DetachInstancesAnswerTypeDef",
    "DetachInstancesQueryRequestTypeDef",
    "DetachLoadBalancerTargetGroupsTypeRequestTypeDef",
    "DetachLoadBalancersTypeRequestTypeDef",
    "DetachTrafficSourcesTypeRequestTypeDef",
    "DisableMetricsCollectionQueryRequestTypeDef",
    "EbsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableMetricsCollectionQueryRequestTypeDef",
    "EnabledMetricTypeDef",
    "EnterStandbyAnswerTypeDef",
    "EnterStandbyQueryRequestTypeDef",
    "ExecutePolicyTypeRequestTypeDef",
    "ExitStandbyAnswerTypeDef",
    "ExitStandbyQueryRequestTypeDef",
    "FailedScheduledUpdateGroupActionRequestTypeDef",
    "FilterTypeDef",
    "GetPredictiveScalingForecastAnswerTypeDef",
    "GetPredictiveScalingForecastTypeRequestTypeDef",
    "InstanceMaintenancePolicyTypeDef",
    "InstanceMetadataOptionsTypeDef",
    "InstanceMonitoringTypeDef",
    "InstanceRefreshLivePoolProgressTypeDef",
    "InstanceRefreshProgressDetailsTypeDef",
    "InstanceRefreshTypeDef",
    "InstanceRefreshWarmPoolProgressTypeDef",
    "InstanceRequirementsOutputTypeDef",
    "InstanceRequirementsTypeDef",
    "InstanceRequirementsUnionTypeDef",
    "InstanceReusePolicyTypeDef",
    "InstanceTypeDef",
    "InstancesDistributionTypeDef",
    "LaunchConfigurationNameTypeRequestTypeDef",
    "LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef",
    "LaunchConfigurationNamesTypeRequestTypeDef",
    "LaunchConfigurationTypeDef",
    "LaunchConfigurationsTypeTypeDef",
    "LaunchTemplateOutputTypeDef",
    "LaunchTemplateOverridesOutputTypeDef",
    "LaunchTemplateOverridesTypeDef",
    "LaunchTemplateOverridesUnionTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "LaunchTemplateTypeDef",
    "LaunchTemplateUnionTypeDef",
    "LifecycleHookSpecificationTypeDef",
    "LifecycleHookTypeDef",
    "LoadBalancerStateTypeDef",
    "LoadBalancerTargetGroupStateTypeDef",
    "LoadForecastTypeDef",
    "MemoryGiBPerVCpuRequestTypeDef",
    "MemoryMiBRequestTypeDef",
    "MetricCollectionTypeTypeDef",
    "MetricDataQueryOutputTypeDef",
    "MetricDataQueryTypeDef",
    "MetricDataQueryUnionTypeDef",
    "MetricDimensionTypeDef",
    "MetricGranularityTypeTypeDef",
    "MetricOutputTypeDef",
    "MetricStatOutputTypeDef",
    "MetricStatTypeDef",
    "MetricStatUnionTypeDef",
    "MetricTypeDef",
    "MetricUnionTypeDef",
    "MixedInstancesPolicyOutputTypeDef",
    "MixedInstancesPolicyTypeDef",
    "MixedInstancesPolicyUnionTypeDef",
    "NetworkBandwidthGbpsRequestTypeDef",
    "NetworkInterfaceCountRequestTypeDef",
    "NotificationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceFactorReferenceRequestTypeDef",
    "PoliciesTypeTypeDef",
    "PolicyARNTypeTypeDef",
    "PredefinedMetricSpecificationTypeDef",
    "PredictiveScalingConfigurationOutputTypeDef",
    "PredictiveScalingConfigurationTypeDef",
    "PredictiveScalingCustomizedCapacityMetricOutputTypeDef",
    "PredictiveScalingCustomizedCapacityMetricTypeDef",
    "PredictiveScalingCustomizedCapacityMetricUnionTypeDef",
    "PredictiveScalingCustomizedLoadMetricOutputTypeDef",
    "PredictiveScalingCustomizedLoadMetricTypeDef",
    "PredictiveScalingCustomizedLoadMetricUnionTypeDef",
    "PredictiveScalingCustomizedScalingMetricOutputTypeDef",
    "PredictiveScalingCustomizedScalingMetricTypeDef",
    "PredictiveScalingCustomizedScalingMetricUnionTypeDef",
    "PredictiveScalingMetricSpecificationOutputTypeDef",
    "PredictiveScalingMetricSpecificationTypeDef",
    "PredictiveScalingMetricSpecificationUnionTypeDef",
    "PredictiveScalingPredefinedLoadMetricTypeDef",
    "PredictiveScalingPredefinedMetricPairTypeDef",
    "PredictiveScalingPredefinedScalingMetricTypeDef",
    "ProcessTypeTypeDef",
    "ProcessesTypeTypeDef",
    "PutLifecycleHookTypeRequestTypeDef",
    "PutNotificationConfigurationTypeRequestTypeDef",
    "PutScalingPolicyTypeRequestTypeDef",
    "PutScheduledUpdateGroupActionTypeRequestTypeDef",
    "PutWarmPoolTypeRequestTypeDef",
    "RecordLifecycleActionHeartbeatTypeRequestTypeDef",
    "RefreshPreferencesOutputTypeDef",
    "RefreshPreferencesTypeDef",
    "ResponseMetadataTypeDef",
    "RollbackDetailsTypeDef",
    "RollbackInstanceRefreshAnswerTypeDef",
    "RollbackInstanceRefreshTypeRequestTypeDef",
    "ScalingPolicyTypeDef",
    "ScalingProcessQueryRequestTypeDef",
    "ScheduledActionsTypeTypeDef",
    "ScheduledUpdateGroupActionRequestTypeDef",
    "ScheduledUpdateGroupActionTypeDef",
    "SetDesiredCapacityTypeRequestTypeDef",
    "SetInstanceHealthQueryRequestTypeDef",
    "SetInstanceProtectionQueryRequestTypeDef",
    "StartInstanceRefreshAnswerTypeDef",
    "StartInstanceRefreshTypeRequestTypeDef",
    "StepAdjustmentTypeDef",
    "SuspendedProcessTypeDef",
    "TagDescriptionTypeDef",
    "TagTypeDef",
    "TagsTypeTypeDef",
    "TargetTrackingConfigurationOutputTypeDef",
    "TargetTrackingConfigurationTypeDef",
    "TargetTrackingMetricDataQueryOutputTypeDef",
    "TargetTrackingMetricDataQueryTypeDef",
    "TargetTrackingMetricDataQueryUnionTypeDef",
    "TargetTrackingMetricStatOutputTypeDef",
    "TargetTrackingMetricStatTypeDef",
    "TargetTrackingMetricStatUnionTypeDef",
    "TerminateInstanceInAutoScalingGroupTypeRequestTypeDef",
    "TimestampTypeDef",
    "TotalLocalStorageGBRequestTypeDef",
    "TrafficSourceIdentifierTypeDef",
    "TrafficSourceStateTypeDef",
    "UpdateAutoScalingGroupTypeRequestTypeDef",
    "VCpuCountRequestTypeDef",
    "WarmPoolConfigurationTypeDef",
)


class AcceleratorCountRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class AcceleratorTotalMemoryMiBRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class ActivityTypeDef(TypedDict):
    ActivityId: str
    AutoScalingGroupName: str
    Cause: str
    StartTime: datetime
    StatusCode: ScalingActivityStatusCodeType
    Description: NotRequired[str]
    EndTime: NotRequired[datetime]
    StatusMessage: NotRequired[str]
    Progress: NotRequired[int]
    Details: NotRequired[str]
    AutoScalingGroupState: NotRequired[str]
    AutoScalingGroupARN: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AdjustmentTypeTypeDef(TypedDict):
    AdjustmentType: NotRequired[str]


class AlarmSpecificationOutputTypeDef(TypedDict):
    Alarms: NotRequired[List[str]]


class AlarmSpecificationTypeDef(TypedDict):
    Alarms: NotRequired[Sequence[str]]


class AlarmTypeDef(TypedDict):
    AlarmName: NotRequired[str]
    AlarmARN: NotRequired[str]


class AttachInstancesQueryRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    InstanceIds: NotRequired[Sequence[str]]


class AttachLoadBalancerTargetGroupsTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    TargetGroupARNs: Sequence[str]


class AttachLoadBalancersTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    LoadBalancerNames: Sequence[str]


TrafficSourceIdentifierTypeDef = TypedDict(
    "TrafficSourceIdentifierTypeDef",
    {
        "Identifier": str,
        "Type": NotRequired[str],
    },
)


class FilterTypeDef(TypedDict):
    Name: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class AvailabilityZoneDistributionTypeDef(TypedDict):
    CapacityDistributionStrategy: NotRequired[CapacityDistributionStrategyType]


class AvailabilityZoneImpairmentPolicyTypeDef(TypedDict):
    ZonalShiftEnabled: NotRequired[bool]
    ImpairedZoneHealthCheckBehavior: NotRequired[ImpairedZoneHealthCheckBehaviorType]


class EnabledMetricTypeDef(TypedDict):
    Metric: NotRequired[str]
    Granularity: NotRequired[str]


class InstanceMaintenancePolicyTypeDef(TypedDict):
    MinHealthyPercentage: NotRequired[int]
    MaxHealthyPercentage: NotRequired[int]


class LaunchTemplateSpecificationTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Version: NotRequired[str]


class SuspendedProcessTypeDef(TypedDict):
    ProcessName: NotRequired[str]
    SuspensionReason: NotRequired[str]


class TagDescriptionTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[str]
    Key: NotRequired[str]
    Value: NotRequired[str]
    PropagateAtLaunch: NotRequired[bool]


class BaselineEbsBandwidthMbpsRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class FailedScheduledUpdateGroupActionRequestTypeDef(TypedDict):
    ScheduledActionName: str
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class BatchDeleteScheduledActionTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ScheduledActionNames: Sequence[str]


class EbsTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    VolumeSize: NotRequired[int]
    VolumeType: NotRequired[str]
    DeleteOnTermination: NotRequired[bool]
    Iops: NotRequired[int]
    Encrypted: NotRequired[bool]
    Throughput: NotRequired[int]


class CancelInstanceRefreshTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str


class CapacityForecastTypeDef(TypedDict):
    Timestamps: List[datetime]
    Values: List[float]


class CapacityReservationTargetOutputTypeDef(TypedDict):
    CapacityReservationIds: NotRequired[List[str]]
    CapacityReservationResourceGroupArns: NotRequired[List[str]]


class CapacityReservationTargetTypeDef(TypedDict):
    CapacityReservationIds: NotRequired[Sequence[str]]
    CapacityReservationResourceGroupArns: NotRequired[Sequence[str]]


class CompleteLifecycleActionTypeRequestTypeDef(TypedDict):
    LifecycleHookName: str
    AutoScalingGroupName: str
    LifecycleActionResult: str
    LifecycleActionToken: NotRequired[str]
    InstanceId: NotRequired[str]


class PerformanceFactorReferenceRequestTypeDef(TypedDict):
    InstanceFamily: NotRequired[str]


class LifecycleHookSpecificationTypeDef(TypedDict):
    LifecycleHookName: str
    LifecycleTransition: str
    NotificationMetadata: NotRequired[str]
    HeartbeatTimeout: NotRequired[int]
    DefaultResult: NotRequired[str]
    NotificationTargetARN: NotRequired[str]
    RoleARN: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[str]
    Value: NotRequired[str]
    PropagateAtLaunch: NotRequired[bool]


class InstanceMetadataOptionsTypeDef(TypedDict):
    HttpTokens: NotRequired[InstanceMetadataHttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[InstanceMetadataEndpointStateType]


class InstanceMonitoringTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class MetricDimensionTypeDef(TypedDict):
    Name: str
    Value: str


class DeleteAutoScalingGroupTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ForceDelete: NotRequired[bool]


class DeleteLifecycleHookTypeRequestTypeDef(TypedDict):
    LifecycleHookName: str
    AutoScalingGroupName: str


class DeleteNotificationConfigurationTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    TopicARN: str


class DeletePolicyTypeRequestTypeDef(TypedDict):
    PolicyName: str
    AutoScalingGroupName: NotRequired[str]


class DeleteScheduledActionTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ScheduledActionName: str


class DeleteWarmPoolTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ForceDelete: NotRequired[bool]


class DescribeAutoScalingInstancesTypeRequestTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstanceRefreshesTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    InstanceRefreshIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class LifecycleHookTypeDef(TypedDict):
    LifecycleHookName: NotRequired[str]
    AutoScalingGroupName: NotRequired[str]
    LifecycleTransition: NotRequired[str]
    NotificationTargetARN: NotRequired[str]
    RoleARN: NotRequired[str]
    NotificationMetadata: NotRequired[str]
    HeartbeatTimeout: NotRequired[int]
    GlobalTimeout: NotRequired[int]
    DefaultResult: NotRequired[str]


class DescribeLifecycleHooksTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    LifecycleHookNames: NotRequired[Sequence[str]]


class DescribeLoadBalancerTargetGroupsRequestRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class LoadBalancerTargetGroupStateTypeDef(TypedDict):
    LoadBalancerTargetGroupARN: NotRequired[str]
    State: NotRequired[str]


class DescribeLoadBalancersRequestRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class LoadBalancerStateTypeDef(TypedDict):
    LoadBalancerName: NotRequired[str]
    State: NotRequired[str]


class MetricCollectionTypeTypeDef(TypedDict):
    Metric: NotRequired[str]


class MetricGranularityTypeTypeDef(TypedDict):
    Granularity: NotRequired[str]


class NotificationConfigurationTypeDef(TypedDict):
    AutoScalingGroupName: NotRequired[str]
    TopicARN: NotRequired[str]
    NotificationType: NotRequired[str]


class DescribeNotificationConfigurationsTypeRequestTypeDef(TypedDict):
    AutoScalingGroupNames: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribePoliciesTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: NotRequired[str]
    PolicyNames: NotRequired[Sequence[str]]
    PolicyTypes: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeScalingActivitiesTypeRequestTypeDef(TypedDict):
    ActivityIds: NotRequired[Sequence[str]]
    AutoScalingGroupName: NotRequired[str]
    IncludeDeletedGroups: NotRequired[bool]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class DescribeTrafficSourcesRequestRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    TrafficSourceType: NotRequired[str]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


TrafficSourceStateTypeDef = TypedDict(
    "TrafficSourceStateTypeDef",
    {
        "TrafficSource": NotRequired[str],
        "State": NotRequired[str],
        "Identifier": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class DescribeWarmPoolTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DetachInstancesQueryRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ShouldDecrementDesiredCapacity: bool
    InstanceIds: NotRequired[Sequence[str]]


class DetachLoadBalancerTargetGroupsTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    TargetGroupARNs: Sequence[str]


class DetachLoadBalancersTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    LoadBalancerNames: Sequence[str]


class DisableMetricsCollectionQueryRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    Metrics: NotRequired[Sequence[str]]


class EnableMetricsCollectionQueryRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    Granularity: str
    Metrics: NotRequired[Sequence[str]]


class EnterStandbyQueryRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ShouldDecrementDesiredCapacity: bool
    InstanceIds: NotRequired[Sequence[str]]


class ExecutePolicyTypeRequestTypeDef(TypedDict):
    PolicyName: str
    AutoScalingGroupName: NotRequired[str]
    HonorCooldown: NotRequired[bool]
    MetricValue: NotRequired[float]
    BreachThreshold: NotRequired[float]


class ExitStandbyQueryRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    InstanceIds: NotRequired[Sequence[str]]


class InstanceRefreshLivePoolProgressTypeDef(TypedDict):
    PercentageComplete: NotRequired[int]
    InstancesToUpdate: NotRequired[int]


class InstanceRefreshWarmPoolProgressTypeDef(TypedDict):
    PercentageComplete: NotRequired[int]
    InstancesToUpdate: NotRequired[int]


class MemoryGiBPerVCpuRequestTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class MemoryMiBRequestTypeDef(TypedDict):
    Min: int
    Max: NotRequired[int]


class NetworkBandwidthGbpsRequestTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class NetworkInterfaceCountRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class TotalLocalStorageGBRequestTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class VCpuCountRequestTypeDef(TypedDict):
    Min: int
    Max: NotRequired[int]


class InstanceReusePolicyTypeDef(TypedDict):
    ReuseOnScaleIn: NotRequired[bool]


class InstancesDistributionTypeDef(TypedDict):
    OnDemandAllocationStrategy: NotRequired[str]
    OnDemandBaseCapacity: NotRequired[int]
    OnDemandPercentageAboveBaseCapacity: NotRequired[int]
    SpotAllocationStrategy: NotRequired[str]
    SpotInstancePools: NotRequired[int]
    SpotMaxPrice: NotRequired[str]


class LaunchConfigurationNameTypeRequestTypeDef(TypedDict):
    LaunchConfigurationName: str


class LaunchConfigurationNamesTypeRequestTypeDef(TypedDict):
    LaunchConfigurationNames: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class PredefinedMetricSpecificationTypeDef(TypedDict):
    PredefinedMetricType: MetricTypeType
    ResourceLabel: NotRequired[str]


class PredictiveScalingPredefinedLoadMetricTypeDef(TypedDict):
    PredefinedMetricType: PredefinedLoadMetricTypeType
    ResourceLabel: NotRequired[str]


class PredictiveScalingPredefinedMetricPairTypeDef(TypedDict):
    PredefinedMetricType: PredefinedMetricPairTypeType
    ResourceLabel: NotRequired[str]


class PredictiveScalingPredefinedScalingMetricTypeDef(TypedDict):
    PredefinedMetricType: PredefinedScalingMetricTypeType
    ResourceLabel: NotRequired[str]


class ProcessTypeTypeDef(TypedDict):
    ProcessName: str


class PutLifecycleHookTypeRequestTypeDef(TypedDict):
    LifecycleHookName: str
    AutoScalingGroupName: str
    LifecycleTransition: NotRequired[str]
    RoleARN: NotRequired[str]
    NotificationTargetARN: NotRequired[str]
    NotificationMetadata: NotRequired[str]
    HeartbeatTimeout: NotRequired[int]
    DefaultResult: NotRequired[str]


class PutNotificationConfigurationTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    TopicARN: str
    NotificationTypes: Sequence[str]


class StepAdjustmentTypeDef(TypedDict):
    ScalingAdjustment: int
    MetricIntervalLowerBound: NotRequired[float]
    MetricIntervalUpperBound: NotRequired[float]


class RecordLifecycleActionHeartbeatTypeRequestTypeDef(TypedDict):
    LifecycleHookName: str
    AutoScalingGroupName: str
    LifecycleActionToken: NotRequired[str]
    InstanceId: NotRequired[str]


class RollbackInstanceRefreshTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str


class ScalingProcessQueryRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ScalingProcesses: NotRequired[Sequence[str]]


class ScheduledUpdateGroupActionTypeDef(TypedDict):
    AutoScalingGroupName: NotRequired[str]
    ScheduledActionName: NotRequired[str]
    ScheduledActionARN: NotRequired[str]
    Time: NotRequired[datetime]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Recurrence: NotRequired[str]
    MinSize: NotRequired[int]
    MaxSize: NotRequired[int]
    DesiredCapacity: NotRequired[int]
    TimeZone: NotRequired[str]


class SetDesiredCapacityTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    DesiredCapacity: int
    HonorCooldown: NotRequired[bool]


class SetInstanceHealthQueryRequestTypeDef(TypedDict):
    InstanceId: str
    HealthStatus: str
    ShouldRespectGracePeriod: NotRequired[bool]


class SetInstanceProtectionQueryRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    AutoScalingGroupName: str
    ProtectedFromScaleIn: bool


class TerminateInstanceInAutoScalingGroupTypeRequestTypeDef(TypedDict):
    InstanceId: str
    ShouldDecrementDesiredCapacity: bool


class ActivitiesTypeTypeDef(TypedDict):
    Activities: List[ActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ActivityTypeTypeDef(TypedDict):
    Activity: ActivityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CancelInstanceRefreshAnswerTypeDef(TypedDict):
    InstanceRefreshId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountLimitsAnswerTypeDef(TypedDict):
    MaxNumberOfAutoScalingGroups: int
    MaxNumberOfLaunchConfigurations: int
    NumberOfAutoScalingGroups: int
    NumberOfLaunchConfigurations: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAutoScalingNotificationTypesAnswerTypeDef(TypedDict):
    AutoScalingNotificationTypes: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLifecycleHookTypesAnswerTypeDef(TypedDict):
    LifecycleHookTypes: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTerminationPolicyTypesAnswerTypeDef(TypedDict):
    TerminationPolicyTypes: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DetachInstancesAnswerTypeDef(TypedDict):
    Activities: List[ActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class EnterStandbyAnswerTypeDef(TypedDict):
    Activities: List[ActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExitStandbyAnswerTypeDef(TypedDict):
    Activities: List[ActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RollbackInstanceRefreshAnswerTypeDef(TypedDict):
    InstanceRefreshId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartInstanceRefreshAnswerTypeDef(TypedDict):
    InstanceRefreshId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAdjustmentTypesAnswerTypeDef(TypedDict):
    AdjustmentTypes: List[AdjustmentTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RefreshPreferencesOutputTypeDef(TypedDict):
    MinHealthyPercentage: NotRequired[int]
    InstanceWarmup: NotRequired[int]
    CheckpointPercentages: NotRequired[List[int]]
    CheckpointDelay: NotRequired[int]
    SkipMatching: NotRequired[bool]
    AutoRollback: NotRequired[bool]
    ScaleInProtectedInstances: NotRequired[ScaleInProtectedInstancesType]
    StandbyInstances: NotRequired[StandbyInstancesType]
    AlarmSpecification: NotRequired[AlarmSpecificationOutputTypeDef]
    MaxHealthyPercentage: NotRequired[int]
    BakeTime: NotRequired[int]


AlarmSpecificationUnionTypeDef = Union[AlarmSpecificationTypeDef, AlarmSpecificationOutputTypeDef]


class PolicyARNTypeTypeDef(TypedDict):
    PolicyARN: str
    Alarms: List[AlarmTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AttachTrafficSourcesTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    TrafficSources: Sequence[TrafficSourceIdentifierTypeDef]
    SkipZonalShiftValidation: NotRequired[bool]


class DetachTrafficSourcesTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    TrafficSources: Sequence[TrafficSourceIdentifierTypeDef]


class AutoScalingGroupNamesTypeRequestTypeDef(TypedDict):
    AutoScalingGroupNames: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeTagsTypeRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef(TypedDict):
    AutoScalingGroupNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef(
    TypedDict
):
    AutoScalingGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef(TypedDict):
    AutoScalingGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef(
    TypedDict
):
    AutoScalingGroupNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePoliciesTypeDescribePoliciesPaginateTypeDef(TypedDict):
    AutoScalingGroupName: NotRequired[str]
    PolicyNames: NotRequired[Sequence[str]]
    PolicyTypes: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef(TypedDict):
    ActivityIds: NotRequired[Sequence[str]]
    AutoScalingGroupName: NotRequired[str]
    IncludeDeletedGroups: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTagsTypeDescribeTagsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeWarmPoolTypeDescribeWarmPoolPaginateTypeDef(TypedDict):
    AutoScalingGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef(TypedDict):
    LaunchConfigurationNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class AutoScalingInstanceDetailsTypeDef(TypedDict):
    InstanceId: str
    AutoScalingGroupName: str
    AvailabilityZone: str
    LifecycleState: str
    HealthStatus: str
    ProtectedFromScaleIn: bool
    InstanceType: NotRequired[str]
    LaunchConfigurationName: NotRequired[str]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    WeightedCapacity: NotRequired[str]


class InstanceTypeDef(TypedDict):
    InstanceId: str
    AvailabilityZone: str
    LifecycleState: LifecycleStateType
    HealthStatus: str
    ProtectedFromScaleIn: bool
    InstanceType: NotRequired[str]
    LaunchConfigurationName: NotRequired[str]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    WeightedCapacity: NotRequired[str]


class TagsTypeTypeDef(TypedDict):
    Tags: List[TagDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchDeleteScheduledActionAnswerTypeDef(TypedDict):
    FailedScheduledActions: List[FailedScheduledUpdateGroupActionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchPutScheduledUpdateGroupActionAnswerTypeDef(TypedDict):
    FailedScheduledUpdateGroupActions: List[FailedScheduledUpdateGroupActionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BlockDeviceMappingTypeDef(TypedDict):
    DeviceName: str
    VirtualName: NotRequired[str]
    Ebs: NotRequired[EbsTypeDef]
    NoDevice: NotRequired[bool]


class CapacityReservationSpecificationOutputTypeDef(TypedDict):
    CapacityReservationPreference: NotRequired[CapacityReservationPreferenceType]
    CapacityReservationTarget: NotRequired[CapacityReservationTargetOutputTypeDef]


CapacityReservationTargetUnionTypeDef = Union[
    CapacityReservationTargetTypeDef, CapacityReservationTargetOutputTypeDef
]


class CpuPerformanceFactorRequestOutputTypeDef(TypedDict):
    References: NotRequired[List[PerformanceFactorReferenceRequestTypeDef]]


class CpuPerformanceFactorRequestTypeDef(TypedDict):
    References: NotRequired[Sequence[PerformanceFactorReferenceRequestTypeDef]]


class CreateOrUpdateTagsTypeRequestTypeDef(TypedDict):
    Tags: Sequence[TagTypeDef]


class DeleteTagsTypeRequestTypeDef(TypedDict):
    Tags: Sequence[TagTypeDef]


class MetricOutputTypeDef(TypedDict):
    Namespace: str
    MetricName: str
    Dimensions: NotRequired[List[MetricDimensionTypeDef]]


class MetricTypeDef(TypedDict):
    Namespace: str
    MetricName: str
    Dimensions: NotRequired[Sequence[MetricDimensionTypeDef]]


class DescribeLifecycleHooksAnswerTypeDef(TypedDict):
    LifecycleHooks: List[LifecycleHookTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLoadBalancerTargetGroupsResponseTypeDef(TypedDict):
    LoadBalancerTargetGroups: List[LoadBalancerTargetGroupStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeLoadBalancersResponseTypeDef(TypedDict):
    LoadBalancers: List[LoadBalancerStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMetricCollectionTypesAnswerTypeDef(TypedDict):
    Metrics: List[MetricCollectionTypeTypeDef]
    Granularities: List[MetricGranularityTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNotificationConfigurationsAnswerTypeDef(TypedDict):
    NotificationConfigurations: List[NotificationConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef(TypedDict):
    AutoScalingGroupName: NotRequired[str]
    ScheduledActionNames: NotRequired[Sequence[str]]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScheduledActionsTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: NotRequired[str]
    ScheduledActionNames: NotRequired[Sequence[str]]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxRecords: NotRequired[int]


class GetPredictiveScalingForecastTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    PolicyName: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef


class PutScheduledUpdateGroupActionTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ScheduledActionName: str
    Time: NotRequired[TimestampTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Recurrence: NotRequired[str]
    MinSize: NotRequired[int]
    MaxSize: NotRequired[int]
    DesiredCapacity: NotRequired[int]
    TimeZone: NotRequired[str]


class ScheduledUpdateGroupActionRequestTypeDef(TypedDict):
    ScheduledActionName: str
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Recurrence: NotRequired[str]
    MinSize: NotRequired[int]
    MaxSize: NotRequired[int]
    DesiredCapacity: NotRequired[int]
    TimeZone: NotRequired[str]


class DescribeTrafficSourcesResponseTypeDef(TypedDict):
    TrafficSources: List[TrafficSourceStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstanceRefreshProgressDetailsTypeDef(TypedDict):
    LivePoolProgress: NotRequired[InstanceRefreshLivePoolProgressTypeDef]
    WarmPoolProgress: NotRequired[InstanceRefreshWarmPoolProgressTypeDef]


class PutWarmPoolTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    MaxGroupPreparedCapacity: NotRequired[int]
    MinSize: NotRequired[int]
    PoolState: NotRequired[WarmPoolStateType]
    InstanceReusePolicy: NotRequired[InstanceReusePolicyTypeDef]


class WarmPoolConfigurationTypeDef(TypedDict):
    MaxGroupPreparedCapacity: NotRequired[int]
    MinSize: NotRequired[int]
    PoolState: NotRequired[WarmPoolStateType]
    Status: NotRequired[Literal["PendingDelete"]]
    InstanceReusePolicy: NotRequired[InstanceReusePolicyTypeDef]


class ProcessesTypeTypeDef(TypedDict):
    Processes: List[ProcessTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ScheduledActionsTypeTypeDef(TypedDict):
    ScheduledUpdateGroupActions: List[ScheduledUpdateGroupActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RefreshPreferencesTypeDef(TypedDict):
    MinHealthyPercentage: NotRequired[int]
    InstanceWarmup: NotRequired[int]
    CheckpointPercentages: NotRequired[Sequence[int]]
    CheckpointDelay: NotRequired[int]
    SkipMatching: NotRequired[bool]
    AutoRollback: NotRequired[bool]
    ScaleInProtectedInstances: NotRequired[ScaleInProtectedInstancesType]
    StandbyInstances: NotRequired[StandbyInstancesType]
    AlarmSpecification: NotRequired[AlarmSpecificationUnionTypeDef]
    MaxHealthyPercentage: NotRequired[int]
    BakeTime: NotRequired[int]


class AutoScalingInstancesTypeTypeDef(TypedDict):
    AutoScalingInstances: List[AutoScalingInstanceDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateLaunchConfigurationTypeRequestTypeDef(TypedDict):
    LaunchConfigurationName: str
    ImageId: NotRequired[str]
    KeyName: NotRequired[str]
    SecurityGroups: NotRequired[Sequence[str]]
    ClassicLinkVPCId: NotRequired[str]
    ClassicLinkVPCSecurityGroups: NotRequired[Sequence[str]]
    UserData: NotRequired[str]
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[str]
    KernelId: NotRequired[str]
    RamdiskId: NotRequired[str]
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    InstanceMonitoring: NotRequired[InstanceMonitoringTypeDef]
    SpotPrice: NotRequired[str]
    IamInstanceProfile: NotRequired[str]
    EbsOptimized: NotRequired[bool]
    AssociatePublicIpAddress: NotRequired[bool]
    PlacementTenancy: NotRequired[str]
    MetadataOptions: NotRequired[InstanceMetadataOptionsTypeDef]


class LaunchConfigurationTypeDef(TypedDict):
    LaunchConfigurationName: str
    ImageId: str
    InstanceType: str
    CreatedTime: datetime
    LaunchConfigurationARN: NotRequired[str]
    KeyName: NotRequired[str]
    SecurityGroups: NotRequired[List[str]]
    ClassicLinkVPCId: NotRequired[str]
    ClassicLinkVPCSecurityGroups: NotRequired[List[str]]
    UserData: NotRequired[str]
    KernelId: NotRequired[str]
    RamdiskId: NotRequired[str]
    BlockDeviceMappings: NotRequired[List[BlockDeviceMappingTypeDef]]
    InstanceMonitoring: NotRequired[InstanceMonitoringTypeDef]
    SpotPrice: NotRequired[str]
    IamInstanceProfile: NotRequired[str]
    EbsOptimized: NotRequired[bool]
    AssociatePublicIpAddress: NotRequired[bool]
    PlacementTenancy: NotRequired[str]
    MetadataOptions: NotRequired[InstanceMetadataOptionsTypeDef]


class CapacityReservationSpecificationTypeDef(TypedDict):
    CapacityReservationPreference: NotRequired[CapacityReservationPreferenceType]
    CapacityReservationTarget: NotRequired[CapacityReservationTargetUnionTypeDef]


class BaselinePerformanceFactorsRequestOutputTypeDef(TypedDict):
    Cpu: NotRequired[CpuPerformanceFactorRequestOutputTypeDef]


CpuPerformanceFactorRequestUnionTypeDef = Union[
    CpuPerformanceFactorRequestTypeDef, CpuPerformanceFactorRequestOutputTypeDef
]


class MetricStatOutputTypeDef(TypedDict):
    Metric: MetricOutputTypeDef
    Stat: str
    Unit: NotRequired[str]


class TargetTrackingMetricStatOutputTypeDef(TypedDict):
    Metric: MetricOutputTypeDef
    Stat: str
    Unit: NotRequired[str]
    Period: NotRequired[int]


MetricUnionTypeDef = Union[MetricTypeDef, MetricOutputTypeDef]


class BatchPutScheduledUpdateGroupActionTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    ScheduledUpdateGroupActions: Sequence[ScheduledUpdateGroupActionRequestTypeDef]


class RollbackDetailsTypeDef(TypedDict):
    RollbackReason: NotRequired[str]
    RollbackStartTime: NotRequired[datetime]
    PercentageCompleteOnRollback: NotRequired[int]
    InstancesToUpdateOnRollback: NotRequired[int]
    ProgressDetailsOnRollback: NotRequired[InstanceRefreshProgressDetailsTypeDef]


class DescribeWarmPoolAnswerTypeDef(TypedDict):
    WarmPoolConfiguration: WarmPoolConfigurationTypeDef
    Instances: List[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LaunchConfigurationsTypeTypeDef(TypedDict):
    LaunchConfigurations: List[LaunchConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstanceRequirementsOutputTypeDef(TypedDict):
    VCpuCount: VCpuCountRequestTypeDef
    MemoryMiB: MemoryMiBRequestTypeDef
    CpuManufacturers: NotRequired[List[CpuManufacturerType]]
    MemoryGiBPerVCpu: NotRequired[MemoryGiBPerVCpuRequestTypeDef]
    ExcludedInstanceTypes: NotRequired[List[str]]
    InstanceGenerations: NotRequired[List[InstanceGenerationType]]
    SpotMaxPricePercentageOverLowestPrice: NotRequired[int]
    MaxSpotPriceAsPercentageOfOptimalOnDemandPrice: NotRequired[int]
    OnDemandMaxPricePercentageOverLowestPrice: NotRequired[int]
    BareMetal: NotRequired[BareMetalType]
    BurstablePerformance: NotRequired[BurstablePerformanceType]
    RequireHibernateSupport: NotRequired[bool]
    NetworkInterfaceCount: NotRequired[NetworkInterfaceCountRequestTypeDef]
    LocalStorage: NotRequired[LocalStorageType]
    LocalStorageTypes: NotRequired[List[LocalStorageTypeType]]
    TotalLocalStorageGB: NotRequired[TotalLocalStorageGBRequestTypeDef]
    BaselineEbsBandwidthMbps: NotRequired[BaselineEbsBandwidthMbpsRequestTypeDef]
    AcceleratorTypes: NotRequired[List[AcceleratorTypeType]]
    AcceleratorCount: NotRequired[AcceleratorCountRequestTypeDef]
    AcceleratorManufacturers: NotRequired[List[AcceleratorManufacturerType]]
    AcceleratorNames: NotRequired[List[AcceleratorNameType]]
    AcceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBRequestTypeDef]
    NetworkBandwidthGbps: NotRequired[NetworkBandwidthGbpsRequestTypeDef]
    AllowedInstanceTypes: NotRequired[List[str]]
    BaselinePerformanceFactors: NotRequired[BaselinePerformanceFactorsRequestOutputTypeDef]


class BaselinePerformanceFactorsRequestTypeDef(TypedDict):
    Cpu: NotRequired[CpuPerformanceFactorRequestUnionTypeDef]


class MetricDataQueryOutputTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    MetricStat: NotRequired[MetricStatOutputTypeDef]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]


class TargetTrackingMetricDataQueryOutputTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    MetricStat: NotRequired[TargetTrackingMetricStatOutputTypeDef]
    Label: NotRequired[str]
    Period: NotRequired[int]
    ReturnData: NotRequired[bool]


class MetricStatTypeDef(TypedDict):
    Metric: MetricUnionTypeDef
    Stat: str
    Unit: NotRequired[str]


class TargetTrackingMetricStatTypeDef(TypedDict):
    Metric: MetricUnionTypeDef
    Stat: str
    Unit: NotRequired[str]
    Period: NotRequired[int]


class LaunchTemplateOverridesOutputTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    WeightedCapacity: NotRequired[str]
    LaunchTemplateSpecification: NotRequired[LaunchTemplateSpecificationTypeDef]
    InstanceRequirements: NotRequired[InstanceRequirementsOutputTypeDef]


BaselinePerformanceFactorsRequestUnionTypeDef = Union[
    BaselinePerformanceFactorsRequestTypeDef, BaselinePerformanceFactorsRequestOutputTypeDef
]


class PredictiveScalingCustomizedCapacityMetricOutputTypeDef(TypedDict):
    MetricDataQueries: List[MetricDataQueryOutputTypeDef]


class PredictiveScalingCustomizedLoadMetricOutputTypeDef(TypedDict):
    MetricDataQueries: List[MetricDataQueryOutputTypeDef]


class PredictiveScalingCustomizedScalingMetricOutputTypeDef(TypedDict):
    MetricDataQueries: List[MetricDataQueryOutputTypeDef]


class CustomizedMetricSpecificationOutputTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]
    Dimensions: NotRequired[List[MetricDimensionTypeDef]]
    Statistic: NotRequired[MetricStatisticType]
    Unit: NotRequired[str]
    Period: NotRequired[int]
    Metrics: NotRequired[List[TargetTrackingMetricDataQueryOutputTypeDef]]


MetricStatUnionTypeDef = Union[MetricStatTypeDef, MetricStatOutputTypeDef]
TargetTrackingMetricStatUnionTypeDef = Union[
    TargetTrackingMetricStatTypeDef, TargetTrackingMetricStatOutputTypeDef
]


class LaunchTemplateOutputTypeDef(TypedDict):
    LaunchTemplateSpecification: NotRequired[LaunchTemplateSpecificationTypeDef]
    Overrides: NotRequired[List[LaunchTemplateOverridesOutputTypeDef]]


class InstanceRequirementsTypeDef(TypedDict):
    VCpuCount: VCpuCountRequestTypeDef
    MemoryMiB: MemoryMiBRequestTypeDef
    CpuManufacturers: NotRequired[Sequence[CpuManufacturerType]]
    MemoryGiBPerVCpu: NotRequired[MemoryGiBPerVCpuRequestTypeDef]
    ExcludedInstanceTypes: NotRequired[Sequence[str]]
    InstanceGenerations: NotRequired[Sequence[InstanceGenerationType]]
    SpotMaxPricePercentageOverLowestPrice: NotRequired[int]
    MaxSpotPriceAsPercentageOfOptimalOnDemandPrice: NotRequired[int]
    OnDemandMaxPricePercentageOverLowestPrice: NotRequired[int]
    BareMetal: NotRequired[BareMetalType]
    BurstablePerformance: NotRequired[BurstablePerformanceType]
    RequireHibernateSupport: NotRequired[bool]
    NetworkInterfaceCount: NotRequired[NetworkInterfaceCountRequestTypeDef]
    LocalStorage: NotRequired[LocalStorageType]
    LocalStorageTypes: NotRequired[Sequence[LocalStorageTypeType]]
    TotalLocalStorageGB: NotRequired[TotalLocalStorageGBRequestTypeDef]
    BaselineEbsBandwidthMbps: NotRequired[BaselineEbsBandwidthMbpsRequestTypeDef]
    AcceleratorTypes: NotRequired[Sequence[AcceleratorTypeType]]
    AcceleratorCount: NotRequired[AcceleratorCountRequestTypeDef]
    AcceleratorManufacturers: NotRequired[Sequence[AcceleratorManufacturerType]]
    AcceleratorNames: NotRequired[Sequence[AcceleratorNameType]]
    AcceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBRequestTypeDef]
    NetworkBandwidthGbps: NotRequired[NetworkBandwidthGbpsRequestTypeDef]
    AllowedInstanceTypes: NotRequired[Sequence[str]]
    BaselinePerformanceFactors: NotRequired[BaselinePerformanceFactorsRequestUnionTypeDef]


class PredictiveScalingMetricSpecificationOutputTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricPairSpecification: NotRequired[PredictiveScalingPredefinedMetricPairTypeDef]
    PredefinedScalingMetricSpecification: NotRequired[
        PredictiveScalingPredefinedScalingMetricTypeDef
    ]
    PredefinedLoadMetricSpecification: NotRequired[PredictiveScalingPredefinedLoadMetricTypeDef]
    CustomizedScalingMetricSpecification: NotRequired[
        PredictiveScalingCustomizedScalingMetricOutputTypeDef
    ]
    CustomizedLoadMetricSpecification: NotRequired[
        PredictiveScalingCustomizedLoadMetricOutputTypeDef
    ]
    CustomizedCapacityMetricSpecification: NotRequired[
        PredictiveScalingCustomizedCapacityMetricOutputTypeDef
    ]


class TargetTrackingConfigurationOutputTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricSpecification: NotRequired[PredefinedMetricSpecificationTypeDef]
    CustomizedMetricSpecification: NotRequired[CustomizedMetricSpecificationOutputTypeDef]
    DisableScaleIn: NotRequired[bool]


class MetricDataQueryTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    MetricStat: NotRequired[MetricStatUnionTypeDef]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]


class TargetTrackingMetricDataQueryTypeDef(TypedDict):
    Id: str
    Expression: NotRequired[str]
    MetricStat: NotRequired[TargetTrackingMetricStatUnionTypeDef]
    Label: NotRequired[str]
    Period: NotRequired[int]
    ReturnData: NotRequired[bool]


class MixedInstancesPolicyOutputTypeDef(TypedDict):
    LaunchTemplate: NotRequired[LaunchTemplateOutputTypeDef]
    InstancesDistribution: NotRequired[InstancesDistributionTypeDef]


InstanceRequirementsUnionTypeDef = Union[
    InstanceRequirementsTypeDef, InstanceRequirementsOutputTypeDef
]


class LoadForecastTypeDef(TypedDict):
    Timestamps: List[datetime]
    Values: List[float]
    MetricSpecification: PredictiveScalingMetricSpecificationOutputTypeDef


class PredictiveScalingConfigurationOutputTypeDef(TypedDict):
    MetricSpecifications: List[PredictiveScalingMetricSpecificationOutputTypeDef]
    Mode: NotRequired[PredictiveScalingModeType]
    SchedulingBufferTime: NotRequired[int]
    MaxCapacityBreachBehavior: NotRequired[PredictiveScalingMaxCapacityBreachBehaviorType]
    MaxCapacityBuffer: NotRequired[int]


MetricDataQueryUnionTypeDef = Union[MetricDataQueryTypeDef, MetricDataQueryOutputTypeDef]


class PredictiveScalingCustomizedCapacityMetricTypeDef(TypedDict):
    MetricDataQueries: Sequence[MetricDataQueryTypeDef]


class PredictiveScalingCustomizedLoadMetricTypeDef(TypedDict):
    MetricDataQueries: Sequence[MetricDataQueryTypeDef]


TargetTrackingMetricDataQueryUnionTypeDef = Union[
    TargetTrackingMetricDataQueryTypeDef, TargetTrackingMetricDataQueryOutputTypeDef
]


class AutoScalingGroupTypeDef(TypedDict):
    AutoScalingGroupName: str
    MinSize: int
    MaxSize: int
    DesiredCapacity: int
    DefaultCooldown: int
    AvailabilityZones: List[str]
    HealthCheckType: str
    CreatedTime: datetime
    AutoScalingGroupARN: NotRequired[str]
    LaunchConfigurationName: NotRequired[str]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    MixedInstancesPolicy: NotRequired[MixedInstancesPolicyOutputTypeDef]
    PredictedCapacity: NotRequired[int]
    LoadBalancerNames: NotRequired[List[str]]
    TargetGroupARNs: NotRequired[List[str]]
    HealthCheckGracePeriod: NotRequired[int]
    Instances: NotRequired[List[InstanceTypeDef]]
    SuspendedProcesses: NotRequired[List[SuspendedProcessTypeDef]]
    PlacementGroup: NotRequired[str]
    VPCZoneIdentifier: NotRequired[str]
    EnabledMetrics: NotRequired[List[EnabledMetricTypeDef]]
    Status: NotRequired[str]
    Tags: NotRequired[List[TagDescriptionTypeDef]]
    TerminationPolicies: NotRequired[List[str]]
    NewInstancesProtectedFromScaleIn: NotRequired[bool]
    ServiceLinkedRoleARN: NotRequired[str]
    MaxInstanceLifetime: NotRequired[int]
    CapacityRebalance: NotRequired[bool]
    WarmPoolConfiguration: NotRequired[WarmPoolConfigurationTypeDef]
    WarmPoolSize: NotRequired[int]
    Context: NotRequired[str]
    DesiredCapacityType: NotRequired[str]
    DefaultInstanceWarmup: NotRequired[int]
    TrafficSources: NotRequired[List[TrafficSourceIdentifierTypeDef]]
    InstanceMaintenancePolicy: NotRequired[InstanceMaintenancePolicyTypeDef]
    AvailabilityZoneDistribution: NotRequired[AvailabilityZoneDistributionTypeDef]
    AvailabilityZoneImpairmentPolicy: NotRequired[AvailabilityZoneImpairmentPolicyTypeDef]
    CapacityReservationSpecification: NotRequired[CapacityReservationSpecificationOutputTypeDef]


class DesiredConfigurationOutputTypeDef(TypedDict):
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    MixedInstancesPolicy: NotRequired[MixedInstancesPolicyOutputTypeDef]


class LaunchTemplateOverridesTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    WeightedCapacity: NotRequired[str]
    LaunchTemplateSpecification: NotRequired[LaunchTemplateSpecificationTypeDef]
    InstanceRequirements: NotRequired[InstanceRequirementsUnionTypeDef]


class GetPredictiveScalingForecastAnswerTypeDef(TypedDict):
    LoadForecast: List[LoadForecastTypeDef]
    CapacityForecast: CapacityForecastTypeDef
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ScalingPolicyTypeDef(TypedDict):
    AutoScalingGroupName: NotRequired[str]
    PolicyName: NotRequired[str]
    PolicyARN: NotRequired[str]
    PolicyType: NotRequired[str]
    AdjustmentType: NotRequired[str]
    MinAdjustmentStep: NotRequired[int]
    MinAdjustmentMagnitude: NotRequired[int]
    ScalingAdjustment: NotRequired[int]
    Cooldown: NotRequired[int]
    StepAdjustments: NotRequired[List[StepAdjustmentTypeDef]]
    MetricAggregationType: NotRequired[str]
    EstimatedInstanceWarmup: NotRequired[int]
    Alarms: NotRequired[List[AlarmTypeDef]]
    TargetTrackingConfiguration: NotRequired[TargetTrackingConfigurationOutputTypeDef]
    Enabled: NotRequired[bool]
    PredictiveScalingConfiguration: NotRequired[PredictiveScalingConfigurationOutputTypeDef]


class PredictiveScalingCustomizedScalingMetricTypeDef(TypedDict):
    MetricDataQueries: Sequence[MetricDataQueryUnionTypeDef]


PredictiveScalingCustomizedCapacityMetricUnionTypeDef = Union[
    PredictiveScalingCustomizedCapacityMetricTypeDef,
    PredictiveScalingCustomizedCapacityMetricOutputTypeDef,
]
PredictiveScalingCustomizedLoadMetricUnionTypeDef = Union[
    PredictiveScalingCustomizedLoadMetricTypeDef, PredictiveScalingCustomizedLoadMetricOutputTypeDef
]


class CustomizedMetricSpecificationTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]
    Dimensions: NotRequired[Sequence[MetricDimensionTypeDef]]
    Statistic: NotRequired[MetricStatisticType]
    Unit: NotRequired[str]
    Period: NotRequired[int]
    Metrics: NotRequired[Sequence[TargetTrackingMetricDataQueryUnionTypeDef]]


class AutoScalingGroupsTypeTypeDef(TypedDict):
    AutoScalingGroups: List[AutoScalingGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstanceRefreshTypeDef(TypedDict):
    InstanceRefreshId: NotRequired[str]
    AutoScalingGroupName: NotRequired[str]
    Status: NotRequired[InstanceRefreshStatusType]
    StatusReason: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    PercentageComplete: NotRequired[int]
    InstancesToUpdate: NotRequired[int]
    ProgressDetails: NotRequired[InstanceRefreshProgressDetailsTypeDef]
    Preferences: NotRequired[RefreshPreferencesOutputTypeDef]
    DesiredConfiguration: NotRequired[DesiredConfigurationOutputTypeDef]
    RollbackDetails: NotRequired[RollbackDetailsTypeDef]


LaunchTemplateOverridesUnionTypeDef = Union[
    LaunchTemplateOverridesTypeDef, LaunchTemplateOverridesOutputTypeDef
]


class PoliciesTypeTypeDef(TypedDict):
    ScalingPolicies: List[ScalingPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


PredictiveScalingCustomizedScalingMetricUnionTypeDef = Union[
    PredictiveScalingCustomizedScalingMetricTypeDef,
    PredictiveScalingCustomizedScalingMetricOutputTypeDef,
]
CustomizedMetricSpecificationUnionTypeDef = Union[
    CustomizedMetricSpecificationTypeDef, CustomizedMetricSpecificationOutputTypeDef
]


class DescribeInstanceRefreshesAnswerTypeDef(TypedDict):
    InstanceRefreshes: List[InstanceRefreshTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LaunchTemplateTypeDef(TypedDict):
    LaunchTemplateSpecification: NotRequired[LaunchTemplateSpecificationTypeDef]
    Overrides: NotRequired[Sequence[LaunchTemplateOverridesUnionTypeDef]]


class PredictiveScalingMetricSpecificationTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricPairSpecification: NotRequired[PredictiveScalingPredefinedMetricPairTypeDef]
    PredefinedScalingMetricSpecification: NotRequired[
        PredictiveScalingPredefinedScalingMetricTypeDef
    ]
    PredefinedLoadMetricSpecification: NotRequired[PredictiveScalingPredefinedLoadMetricTypeDef]
    CustomizedScalingMetricSpecification: NotRequired[
        PredictiveScalingCustomizedScalingMetricUnionTypeDef
    ]
    CustomizedLoadMetricSpecification: NotRequired[
        PredictiveScalingCustomizedLoadMetricUnionTypeDef
    ]
    CustomizedCapacityMetricSpecification: NotRequired[
        PredictiveScalingCustomizedCapacityMetricUnionTypeDef
    ]


class TargetTrackingConfigurationTypeDef(TypedDict):
    TargetValue: float
    PredefinedMetricSpecification: NotRequired[PredefinedMetricSpecificationTypeDef]
    CustomizedMetricSpecification: NotRequired[CustomizedMetricSpecificationUnionTypeDef]
    DisableScaleIn: NotRequired[bool]


LaunchTemplateUnionTypeDef = Union[LaunchTemplateTypeDef, LaunchTemplateOutputTypeDef]
PredictiveScalingMetricSpecificationUnionTypeDef = Union[
    PredictiveScalingMetricSpecificationTypeDef, PredictiveScalingMetricSpecificationOutputTypeDef
]


class MixedInstancesPolicyTypeDef(TypedDict):
    LaunchTemplate: NotRequired[LaunchTemplateUnionTypeDef]
    InstancesDistribution: NotRequired[InstancesDistributionTypeDef]


class PredictiveScalingConfigurationTypeDef(TypedDict):
    MetricSpecifications: Sequence[PredictiveScalingMetricSpecificationUnionTypeDef]
    Mode: NotRequired[PredictiveScalingModeType]
    SchedulingBufferTime: NotRequired[int]
    MaxCapacityBreachBehavior: NotRequired[PredictiveScalingMaxCapacityBreachBehaviorType]
    MaxCapacityBuffer: NotRequired[int]


class CreateAutoScalingGroupTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    MinSize: int
    MaxSize: int
    LaunchConfigurationName: NotRequired[str]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    MixedInstancesPolicy: NotRequired[MixedInstancesPolicyTypeDef]
    InstanceId: NotRequired[str]
    DesiredCapacity: NotRequired[int]
    DefaultCooldown: NotRequired[int]
    AvailabilityZones: NotRequired[Sequence[str]]
    LoadBalancerNames: NotRequired[Sequence[str]]
    TargetGroupARNs: NotRequired[Sequence[str]]
    HealthCheckType: NotRequired[str]
    HealthCheckGracePeriod: NotRequired[int]
    PlacementGroup: NotRequired[str]
    VPCZoneIdentifier: NotRequired[str]
    TerminationPolicies: NotRequired[Sequence[str]]
    NewInstancesProtectedFromScaleIn: NotRequired[bool]
    CapacityRebalance: NotRequired[bool]
    LifecycleHookSpecificationList: NotRequired[Sequence[LifecycleHookSpecificationTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ServiceLinkedRoleARN: NotRequired[str]
    MaxInstanceLifetime: NotRequired[int]
    Context: NotRequired[str]
    DesiredCapacityType: NotRequired[str]
    DefaultInstanceWarmup: NotRequired[int]
    TrafficSources: NotRequired[Sequence[TrafficSourceIdentifierTypeDef]]
    InstanceMaintenancePolicy: NotRequired[InstanceMaintenancePolicyTypeDef]
    AvailabilityZoneDistribution: NotRequired[AvailabilityZoneDistributionTypeDef]
    AvailabilityZoneImpairmentPolicy: NotRequired[AvailabilityZoneImpairmentPolicyTypeDef]
    SkipZonalShiftValidation: NotRequired[bool]
    CapacityReservationSpecification: NotRequired[CapacityReservationSpecificationTypeDef]


MixedInstancesPolicyUnionTypeDef = Union[
    MixedInstancesPolicyTypeDef, MixedInstancesPolicyOutputTypeDef
]


class UpdateAutoScalingGroupTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    LaunchConfigurationName: NotRequired[str]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    MixedInstancesPolicy: NotRequired[MixedInstancesPolicyTypeDef]
    MinSize: NotRequired[int]
    MaxSize: NotRequired[int]
    DesiredCapacity: NotRequired[int]
    DefaultCooldown: NotRequired[int]
    AvailabilityZones: NotRequired[Sequence[str]]
    HealthCheckType: NotRequired[str]
    HealthCheckGracePeriod: NotRequired[int]
    PlacementGroup: NotRequired[str]
    VPCZoneIdentifier: NotRequired[str]
    TerminationPolicies: NotRequired[Sequence[str]]
    NewInstancesProtectedFromScaleIn: NotRequired[bool]
    ServiceLinkedRoleARN: NotRequired[str]
    MaxInstanceLifetime: NotRequired[int]
    CapacityRebalance: NotRequired[bool]
    Context: NotRequired[str]
    DesiredCapacityType: NotRequired[str]
    DefaultInstanceWarmup: NotRequired[int]
    InstanceMaintenancePolicy: NotRequired[InstanceMaintenancePolicyTypeDef]
    AvailabilityZoneDistribution: NotRequired[AvailabilityZoneDistributionTypeDef]
    AvailabilityZoneImpairmentPolicy: NotRequired[AvailabilityZoneImpairmentPolicyTypeDef]
    SkipZonalShiftValidation: NotRequired[bool]
    CapacityReservationSpecification: NotRequired[CapacityReservationSpecificationTypeDef]


class PutScalingPolicyTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    PolicyName: str
    PolicyType: NotRequired[str]
    AdjustmentType: NotRequired[str]
    MinAdjustmentStep: NotRequired[int]
    MinAdjustmentMagnitude: NotRequired[int]
    ScalingAdjustment: NotRequired[int]
    Cooldown: NotRequired[int]
    MetricAggregationType: NotRequired[str]
    StepAdjustments: NotRequired[Sequence[StepAdjustmentTypeDef]]
    EstimatedInstanceWarmup: NotRequired[int]
    TargetTrackingConfiguration: NotRequired[TargetTrackingConfigurationTypeDef]
    Enabled: NotRequired[bool]
    PredictiveScalingConfiguration: NotRequired[PredictiveScalingConfigurationTypeDef]


class DesiredConfigurationTypeDef(TypedDict):
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    MixedInstancesPolicy: NotRequired[MixedInstancesPolicyUnionTypeDef]


class StartInstanceRefreshTypeRequestTypeDef(TypedDict):
    AutoScalingGroupName: str
    Strategy: NotRequired[Literal["Rolling"]]
    DesiredConfiguration: NotRequired[DesiredConfigurationTypeDef]
    Preferences: NotRequired[RefreshPreferencesTypeDef]
