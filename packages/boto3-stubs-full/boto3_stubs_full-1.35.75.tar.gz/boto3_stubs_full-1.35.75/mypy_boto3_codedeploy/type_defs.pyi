"""
Type annotations for codedeploy service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/type_defs/)

Usage::

    ```python
    from mypy_boto3_codedeploy.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ApplicationRevisionSortByType,
    AutoRollbackEventType,
    BundleTypeType,
    ComputePlatformType,
    DeploymentCreatorType,
    DeploymentOptionType,
    DeploymentReadyActionType,
    DeploymentStatusType,
    DeploymentTargetTypeType,
    DeploymentTypeType,
    DeploymentWaitTypeType,
    EC2TagFilterTypeType,
    ErrorCodeType,
    FileExistsBehaviorType,
    GreenFleetProvisioningActionType,
    InstanceActionType,
    InstanceStatusType,
    InstanceTypeType,
    LifecycleErrorCodeType,
    LifecycleEventStatusType,
    ListStateFilterActionType,
    MinimumHealthyHostsPerZoneTypeType,
    MinimumHealthyHostsTypeType,
    OutdatedInstancesStrategyType,
    RegistrationStatusType,
    RevisionLocationTypeType,
    SortOrderType,
    StopStatusType,
    TagFilterTypeType,
    TargetFilterNameType,
    TargetLabelType,
    TargetStatusType,
    TrafficRoutingTypeType,
    TriggerEventTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AddTagsToOnPremisesInstancesInputRequestTypeDef",
    "AlarmConfigurationOutputTypeDef",
    "AlarmConfigurationTypeDef",
    "AlarmTypeDef",
    "AppSpecContentTypeDef",
    "ApplicationInfoTypeDef",
    "AutoRollbackConfigurationOutputTypeDef",
    "AutoRollbackConfigurationTypeDef",
    "AutoScalingGroupTypeDef",
    "BatchGetApplicationRevisionsInputRequestTypeDef",
    "BatchGetApplicationRevisionsOutputTypeDef",
    "BatchGetApplicationsInputRequestTypeDef",
    "BatchGetApplicationsOutputTypeDef",
    "BatchGetDeploymentGroupsInputRequestTypeDef",
    "BatchGetDeploymentGroupsOutputTypeDef",
    "BatchGetDeploymentInstancesInputRequestTypeDef",
    "BatchGetDeploymentInstancesOutputTypeDef",
    "BatchGetDeploymentTargetsInputRequestTypeDef",
    "BatchGetDeploymentTargetsOutputTypeDef",
    "BatchGetDeploymentsInputRequestTypeDef",
    "BatchGetDeploymentsOutputTypeDef",
    "BatchGetOnPremisesInstancesInputRequestTypeDef",
    "BatchGetOnPremisesInstancesOutputTypeDef",
    "BlueGreenDeploymentConfigurationTypeDef",
    "BlueInstanceTerminationOptionTypeDef",
    "CloudFormationTargetTypeDef",
    "ContinueDeploymentInputRequestTypeDef",
    "CreateApplicationInputRequestTypeDef",
    "CreateApplicationOutputTypeDef",
    "CreateDeploymentConfigInputRequestTypeDef",
    "CreateDeploymentConfigOutputTypeDef",
    "CreateDeploymentGroupInputRequestTypeDef",
    "CreateDeploymentGroupOutputTypeDef",
    "CreateDeploymentInputRequestTypeDef",
    "CreateDeploymentOutputTypeDef",
    "DeleteApplicationInputRequestTypeDef",
    "DeleteDeploymentConfigInputRequestTypeDef",
    "DeleteDeploymentGroupInputRequestTypeDef",
    "DeleteDeploymentGroupOutputTypeDef",
    "DeleteGitHubAccountTokenInputRequestTypeDef",
    "DeleteGitHubAccountTokenOutputTypeDef",
    "DeleteResourcesByExternalIdInputRequestTypeDef",
    "DeploymentConfigInfoTypeDef",
    "DeploymentGroupInfoTypeDef",
    "DeploymentInfoTypeDef",
    "DeploymentOverviewTypeDef",
    "DeploymentReadyOptionTypeDef",
    "DeploymentStyleTypeDef",
    "DeploymentTargetTypeDef",
    "DeregisterOnPremisesInstanceInputRequestTypeDef",
    "DiagnosticsTypeDef",
    "EC2TagFilterTypeDef",
    "EC2TagSetOutputTypeDef",
    "EC2TagSetTypeDef",
    "EC2TagSetUnionTypeDef",
    "ECSServiceTypeDef",
    "ECSTargetTypeDef",
    "ECSTaskSetTypeDef",
    "ELBInfoTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ErrorInformationTypeDef",
    "GenericRevisionInfoTypeDef",
    "GetApplicationInputRequestTypeDef",
    "GetApplicationOutputTypeDef",
    "GetApplicationRevisionInputRequestTypeDef",
    "GetApplicationRevisionOutputTypeDef",
    "GetDeploymentConfigInputRequestTypeDef",
    "GetDeploymentConfigOutputTypeDef",
    "GetDeploymentGroupInputRequestTypeDef",
    "GetDeploymentGroupOutputTypeDef",
    "GetDeploymentInputDeploymentSuccessfulWaitTypeDef",
    "GetDeploymentInputRequestTypeDef",
    "GetDeploymentInstanceInputRequestTypeDef",
    "GetDeploymentInstanceOutputTypeDef",
    "GetDeploymentOutputTypeDef",
    "GetDeploymentTargetInputRequestTypeDef",
    "GetDeploymentTargetOutputTypeDef",
    "GetOnPremisesInstanceInputRequestTypeDef",
    "GetOnPremisesInstanceOutputTypeDef",
    "GitHubLocationTypeDef",
    "GreenFleetProvisioningOptionTypeDef",
    "InstanceInfoTypeDef",
    "InstanceSummaryTypeDef",
    "InstanceTargetTypeDef",
    "LambdaFunctionInfoTypeDef",
    "LambdaTargetTypeDef",
    "LastDeploymentInfoTypeDef",
    "LifecycleEventTypeDef",
    "ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef",
    "ListApplicationRevisionsInputRequestTypeDef",
    "ListApplicationRevisionsOutputTypeDef",
    "ListApplicationsInputListApplicationsPaginateTypeDef",
    "ListApplicationsInputRequestTypeDef",
    "ListApplicationsOutputTypeDef",
    "ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef",
    "ListDeploymentConfigsInputRequestTypeDef",
    "ListDeploymentConfigsOutputTypeDef",
    "ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef",
    "ListDeploymentGroupsInputRequestTypeDef",
    "ListDeploymentGroupsOutputTypeDef",
    "ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef",
    "ListDeploymentInstancesInputRequestTypeDef",
    "ListDeploymentInstancesOutputTypeDef",
    "ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef",
    "ListDeploymentTargetsInputRequestTypeDef",
    "ListDeploymentTargetsOutputTypeDef",
    "ListDeploymentsInputListDeploymentsPaginateTypeDef",
    "ListDeploymentsInputRequestTypeDef",
    "ListDeploymentsOutputTypeDef",
    "ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef",
    "ListGitHubAccountTokenNamesInputRequestTypeDef",
    "ListGitHubAccountTokenNamesOutputTypeDef",
    "ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef",
    "ListOnPremisesInstancesInputRequestTypeDef",
    "ListOnPremisesInstancesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "LoadBalancerInfoOutputTypeDef",
    "LoadBalancerInfoTypeDef",
    "MinimumHealthyHostsPerZoneTypeDef",
    "MinimumHealthyHostsTypeDef",
    "OnPremisesTagSetOutputTypeDef",
    "OnPremisesTagSetTypeDef",
    "PaginatorConfigTypeDef",
    "PutLifecycleEventHookExecutionStatusInputRequestTypeDef",
    "PutLifecycleEventHookExecutionStatusOutputTypeDef",
    "RawStringTypeDef",
    "RegisterApplicationRevisionInputRequestTypeDef",
    "RegisterOnPremisesInstanceInputRequestTypeDef",
    "RelatedDeploymentsTypeDef",
    "RemoveTagsFromOnPremisesInstancesInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RevisionInfoTypeDef",
    "RevisionLocationTypeDef",
    "RollbackInfoTypeDef",
    "S3LocationTypeDef",
    "SkipWaitTimeForInstanceTerminationInputRequestTypeDef",
    "StopDeploymentInputRequestTypeDef",
    "StopDeploymentOutputTypeDef",
    "TagFilterTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "TargetGroupInfoTypeDef",
    "TargetGroupPairInfoOutputTypeDef",
    "TargetGroupPairInfoTypeDef",
    "TargetGroupPairInfoUnionTypeDef",
    "TargetInstancesOutputTypeDef",
    "TargetInstancesTypeDef",
    "TimeBasedCanaryTypeDef",
    "TimeBasedLinearTypeDef",
    "TimeRangeTypeDef",
    "TimestampTypeDef",
    "TrafficRouteOutputTypeDef",
    "TrafficRouteTypeDef",
    "TrafficRouteUnionTypeDef",
    "TrafficRoutingConfigTypeDef",
    "TriggerConfigOutputTypeDef",
    "TriggerConfigTypeDef",
    "TriggerConfigUnionTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateApplicationInputRequestTypeDef",
    "UpdateDeploymentGroupInputRequestTypeDef",
    "UpdateDeploymentGroupOutputTypeDef",
    "WaiterConfigTypeDef",
    "ZonalConfigTypeDef",
)

class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class AlarmTypeDef(TypedDict):
    name: NotRequired[str]

class AppSpecContentTypeDef(TypedDict):
    content: NotRequired[str]
    sha256: NotRequired[str]

class ApplicationInfoTypeDef(TypedDict):
    applicationId: NotRequired[str]
    applicationName: NotRequired[str]
    createTime: NotRequired[datetime]
    linkedToGitHub: NotRequired[bool]
    gitHubAccountName: NotRequired[str]
    computePlatform: NotRequired[ComputePlatformType]

class AutoRollbackConfigurationOutputTypeDef(TypedDict):
    enabled: NotRequired[bool]
    events: NotRequired[List[AutoRollbackEventType]]

class AutoRollbackConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]
    events: NotRequired[Sequence[AutoRollbackEventType]]

class AutoScalingGroupTypeDef(TypedDict):
    name: NotRequired[str]
    hook: NotRequired[str]
    terminationHook: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchGetApplicationsInputRequestTypeDef(TypedDict):
    applicationNames: Sequence[str]

class BatchGetDeploymentGroupsInputRequestTypeDef(TypedDict):
    applicationName: str
    deploymentGroupNames: Sequence[str]

class BatchGetDeploymentInstancesInputRequestTypeDef(TypedDict):
    deploymentId: str
    instanceIds: Sequence[str]

class BatchGetDeploymentTargetsInputRequestTypeDef(TypedDict):
    deploymentId: str
    targetIds: Sequence[str]

class BatchGetDeploymentsInputRequestTypeDef(TypedDict):
    deploymentIds: Sequence[str]

class BatchGetOnPremisesInstancesInputRequestTypeDef(TypedDict):
    instanceNames: Sequence[str]

class BlueInstanceTerminationOptionTypeDef(TypedDict):
    action: NotRequired[InstanceActionType]
    terminationWaitTimeInMinutes: NotRequired[int]

class DeploymentReadyOptionTypeDef(TypedDict):
    actionOnTimeout: NotRequired[DeploymentReadyActionType]
    waitTimeInMinutes: NotRequired[int]

class GreenFleetProvisioningOptionTypeDef(TypedDict):
    action: NotRequired[GreenFleetProvisioningActionType]

class ContinueDeploymentInputRequestTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    deploymentWaitType: NotRequired[DeploymentWaitTypeType]

MinimumHealthyHostsTypeDef = TypedDict(
    "MinimumHealthyHostsTypeDef",
    {
        "type": NotRequired[MinimumHealthyHostsTypeType],
        "value": NotRequired[int],
    },
)

class DeploymentStyleTypeDef(TypedDict):
    deploymentType: NotRequired[DeploymentTypeType]
    deploymentOption: NotRequired[DeploymentOptionType]

EC2TagFilterTypeDef = TypedDict(
    "EC2TagFilterTypeDef",
    {
        "Key": NotRequired[str],
        "Value": NotRequired[str],
        "Type": NotRequired[EC2TagFilterTypeType],
    },
)

class ECSServiceTypeDef(TypedDict):
    serviceName: NotRequired[str]
    clusterName: NotRequired[str]

TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "Key": NotRequired[str],
        "Value": NotRequired[str],
        "Type": NotRequired[TagFilterTypeType],
    },
)

class DeleteApplicationInputRequestTypeDef(TypedDict):
    applicationName: str

class DeleteDeploymentConfigInputRequestTypeDef(TypedDict):
    deploymentConfigName: str

class DeleteDeploymentGroupInputRequestTypeDef(TypedDict):
    applicationName: str
    deploymentGroupName: str

class DeleteGitHubAccountTokenInputRequestTypeDef(TypedDict):
    tokenName: NotRequired[str]

class DeleteResourcesByExternalIdInputRequestTypeDef(TypedDict):
    externalId: NotRequired[str]

class LastDeploymentInfoTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    status: NotRequired[DeploymentStatusType]
    endTime: NotRequired[datetime]
    createTime: NotRequired[datetime]

class TriggerConfigOutputTypeDef(TypedDict):
    triggerName: NotRequired[str]
    triggerTargetArn: NotRequired[str]
    triggerEvents: NotRequired[List[TriggerEventTypeType]]

class DeploymentOverviewTypeDef(TypedDict):
    Pending: NotRequired[int]
    InProgress: NotRequired[int]
    Succeeded: NotRequired[int]
    Failed: NotRequired[int]
    Skipped: NotRequired[int]
    Ready: NotRequired[int]

class ErrorInformationTypeDef(TypedDict):
    code: NotRequired[ErrorCodeType]
    message: NotRequired[str]

class RelatedDeploymentsTypeDef(TypedDict):
    autoUpdateOutdatedInstancesRootDeploymentId: NotRequired[str]
    autoUpdateOutdatedInstancesDeploymentIds: NotRequired[List[str]]

class RollbackInfoTypeDef(TypedDict):
    rollbackDeploymentId: NotRequired[str]
    rollbackTriggeringDeploymentId: NotRequired[str]
    rollbackMessage: NotRequired[str]

class DeregisterOnPremisesInstanceInputRequestTypeDef(TypedDict):
    instanceName: str

class DiagnosticsTypeDef(TypedDict):
    errorCode: NotRequired[LifecycleErrorCodeType]
    scriptName: NotRequired[str]
    message: NotRequired[str]
    logTail: NotRequired[str]

class TargetGroupInfoTypeDef(TypedDict):
    name: NotRequired[str]

class ELBInfoTypeDef(TypedDict):
    name: NotRequired[str]

class GenericRevisionInfoTypeDef(TypedDict):
    description: NotRequired[str]
    deploymentGroups: NotRequired[List[str]]
    firstUsedTime: NotRequired[datetime]
    lastUsedTime: NotRequired[datetime]
    registerTime: NotRequired[datetime]

class GetApplicationInputRequestTypeDef(TypedDict):
    applicationName: str

class GetDeploymentConfigInputRequestTypeDef(TypedDict):
    deploymentConfigName: str

class GetDeploymentGroupInputRequestTypeDef(TypedDict):
    applicationName: str
    deploymentGroupName: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetDeploymentInputRequestTypeDef(TypedDict):
    deploymentId: str

class GetDeploymentInstanceInputRequestTypeDef(TypedDict):
    deploymentId: str
    instanceId: str

class GetDeploymentTargetInputRequestTypeDef(TypedDict):
    deploymentId: str
    targetId: str

class GetOnPremisesInstanceInputRequestTypeDef(TypedDict):
    instanceName: str

class GitHubLocationTypeDef(TypedDict):
    repository: NotRequired[str]
    commitId: NotRequired[str]

class LambdaFunctionInfoTypeDef(TypedDict):
    functionName: NotRequired[str]
    functionAlias: NotRequired[str]
    currentVersion: NotRequired[str]
    targetVersion: NotRequired[str]
    targetVersionWeight: NotRequired[float]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListApplicationRevisionsInputRequestTypeDef(TypedDict):
    applicationName: str
    sortBy: NotRequired[ApplicationRevisionSortByType]
    sortOrder: NotRequired[SortOrderType]
    s3Bucket: NotRequired[str]
    s3KeyPrefix: NotRequired[str]
    deployed: NotRequired[ListStateFilterActionType]
    nextToken: NotRequired[str]

class ListApplicationsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]

class ListDeploymentConfigsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]

class ListDeploymentGroupsInputRequestTypeDef(TypedDict):
    applicationName: str
    nextToken: NotRequired[str]

class ListDeploymentInstancesInputRequestTypeDef(TypedDict):
    deploymentId: str
    nextToken: NotRequired[str]
    instanceStatusFilter: NotRequired[Sequence[InstanceStatusType]]
    instanceTypeFilter: NotRequired[Sequence[InstanceTypeType]]

class ListDeploymentTargetsInputRequestTypeDef(TypedDict):
    deploymentId: str
    nextToken: NotRequired[str]
    targetFilters: NotRequired[Mapping[TargetFilterNameType, Sequence[str]]]

class ListGitHubAccountTokenNamesInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]

MinimumHealthyHostsPerZoneTypeDef = TypedDict(
    "MinimumHealthyHostsPerZoneTypeDef",
    {
        "type": NotRequired[MinimumHealthyHostsPerZoneTypeType],
        "value": NotRequired[int],
    },
)

class PutLifecycleEventHookExecutionStatusInputRequestTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    lifecycleEventHookExecutionId: NotRequired[str]
    status: NotRequired[LifecycleEventStatusType]

class RawStringTypeDef(TypedDict):
    content: NotRequired[str]
    sha256: NotRequired[str]

class RegisterOnPremisesInstanceInputRequestTypeDef(TypedDict):
    instanceName: str
    iamSessionArn: NotRequired[str]
    iamUserArn: NotRequired[str]

class S3LocationTypeDef(TypedDict):
    bucket: NotRequired[str]
    key: NotRequired[str]
    bundleType: NotRequired[BundleTypeType]
    version: NotRequired[str]
    eTag: NotRequired[str]

class SkipWaitTimeForInstanceTerminationInputRequestTypeDef(TypedDict):
    deploymentId: NotRequired[str]

class StopDeploymentInputRequestTypeDef(TypedDict):
    deploymentId: str
    autoRollbackEnabled: NotRequired[bool]

class TrafficRouteOutputTypeDef(TypedDict):
    listenerArns: NotRequired[List[str]]

class TimeBasedCanaryTypeDef(TypedDict):
    canaryPercentage: NotRequired[int]
    canaryInterval: NotRequired[int]

class TimeBasedLinearTypeDef(TypedDict):
    linearPercentage: NotRequired[int]
    linearInterval: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class TrafficRouteTypeDef(TypedDict):
    listenerArns: NotRequired[Sequence[str]]

class TriggerConfigTypeDef(TypedDict):
    triggerName: NotRequired[str]
    triggerTargetArn: NotRequired[str]
    triggerEvents: NotRequired[Sequence[TriggerEventTypeType]]

class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateApplicationInputRequestTypeDef(TypedDict):
    applicationName: NotRequired[str]
    newApplicationName: NotRequired[str]

class AddTagsToOnPremisesInstancesInputRequestTypeDef(TypedDict):
    tags: Sequence[TagTypeDef]
    instanceNames: Sequence[str]

class CreateApplicationInputRequestTypeDef(TypedDict):
    applicationName: str
    computePlatform: NotRequired[ComputePlatformType]
    tags: NotRequired[Sequence[TagTypeDef]]

class InstanceInfoTypeDef(TypedDict):
    instanceName: NotRequired[str]
    iamSessionArn: NotRequired[str]
    iamUserArn: NotRequired[str]
    instanceArn: NotRequired[str]
    registerTime: NotRequired[datetime]
    deregisterTime: NotRequired[datetime]
    tags: NotRequired[List[TagTypeDef]]

class RemoveTagsFromOnPremisesInstancesInputRequestTypeDef(TypedDict):
    tags: Sequence[TagTypeDef]
    instanceNames: Sequence[str]

class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class AlarmConfigurationOutputTypeDef(TypedDict):
    enabled: NotRequired[bool]
    ignorePollAlarmFailure: NotRequired[bool]
    alarms: NotRequired[List[AlarmTypeDef]]

class AlarmConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]
    ignorePollAlarmFailure: NotRequired[bool]
    alarms: NotRequired[Sequence[AlarmTypeDef]]

class BatchGetApplicationsOutputTypeDef(TypedDict):
    applicationsInfo: List[ApplicationInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationOutputTypeDef(TypedDict):
    applicationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDeploymentConfigOutputTypeDef(TypedDict):
    deploymentConfigId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDeploymentGroupOutputTypeDef(TypedDict):
    deploymentGroupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDeploymentOutputTypeDef(TypedDict):
    deploymentId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDeploymentGroupOutputTypeDef(TypedDict):
    hooksNotCleanedUp: List[AutoScalingGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteGitHubAccountTokenOutputTypeDef(TypedDict):
    tokenName: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationOutputTypeDef(TypedDict):
    application: ApplicationInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationsOutputTypeDef(TypedDict):
    applications: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDeploymentConfigsOutputTypeDef(TypedDict):
    deploymentConfigsList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDeploymentGroupsOutputTypeDef(TypedDict):
    applicationName: str
    deploymentGroups: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDeploymentInstancesOutputTypeDef(TypedDict):
    instancesList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDeploymentTargetsOutputTypeDef(TypedDict):
    targetIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDeploymentsOutputTypeDef(TypedDict):
    deployments: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListGitHubAccountTokenNamesOutputTypeDef(TypedDict):
    tokenNameList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListOnPremisesInstancesOutputTypeDef(TypedDict):
    instanceNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutLifecycleEventHookExecutionStatusOutputTypeDef(TypedDict):
    lifecycleEventHookExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopDeploymentOutputTypeDef(TypedDict):
    status: StopStatusType
    statusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDeploymentGroupOutputTypeDef(TypedDict):
    hooksNotCleanedUp: List[AutoScalingGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BlueGreenDeploymentConfigurationTypeDef(TypedDict):
    terminateBlueInstancesOnDeploymentSuccess: NotRequired[BlueInstanceTerminationOptionTypeDef]
    deploymentReadyOption: NotRequired[DeploymentReadyOptionTypeDef]
    greenFleetProvisioningOption: NotRequired[GreenFleetProvisioningOptionTypeDef]

class EC2TagSetOutputTypeDef(TypedDict):
    ec2TagSetList: NotRequired[List[List[EC2TagFilterTypeDef]]]

class EC2TagSetTypeDef(TypedDict):
    ec2TagSetList: NotRequired[Sequence[Sequence[EC2TagFilterTypeDef]]]

class ListOnPremisesInstancesInputRequestTypeDef(TypedDict):
    registrationStatus: NotRequired[RegistrationStatusType]
    tagFilters: NotRequired[Sequence[TagFilterTypeDef]]
    nextToken: NotRequired[str]

class OnPremisesTagSetOutputTypeDef(TypedDict):
    onPremisesTagSetList: NotRequired[List[List[TagFilterTypeDef]]]

class OnPremisesTagSetTypeDef(TypedDict):
    onPremisesTagSetList: NotRequired[Sequence[Sequence[TagFilterTypeDef]]]

class LifecycleEventTypeDef(TypedDict):
    lifecycleEventName: NotRequired[str]
    diagnostics: NotRequired[DiagnosticsTypeDef]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    status: NotRequired[LifecycleEventStatusType]

class ECSTaskSetTypeDef(TypedDict):
    identifer: NotRequired[str]
    desiredCount: NotRequired[int]
    pendingCount: NotRequired[int]
    runningCount: NotRequired[int]
    status: NotRequired[str]
    trafficWeight: NotRequired[float]
    targetGroup: NotRequired[TargetGroupInfoTypeDef]
    taskSetLabel: NotRequired[TargetLabelType]

class GetDeploymentInputDeploymentSuccessfulWaitTypeDef(TypedDict):
    deploymentId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef(TypedDict):
    applicationName: str
    sortBy: NotRequired[ApplicationRevisionSortByType]
    sortOrder: NotRequired[SortOrderType]
    s3Bucket: NotRequired[str]
    s3KeyPrefix: NotRequired[str]
    deployed: NotRequired[ListStateFilterActionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsInputListApplicationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef(TypedDict):
    applicationName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef(TypedDict):
    deploymentId: str
    instanceStatusFilter: NotRequired[Sequence[InstanceStatusType]]
    instanceTypeFilter: NotRequired[Sequence[InstanceTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef(TypedDict):
    deploymentId: str
    targetFilters: NotRequired[Mapping[TargetFilterNameType, Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef(TypedDict):
    registrationStatus: NotRequired[RegistrationStatusType]
    tagFilters: NotRequired[Sequence[TagFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ZonalConfigTypeDef(TypedDict):
    firstZoneMonitorDurationInSeconds: NotRequired[int]
    monitorDurationInSeconds: NotRequired[int]
    minimumHealthyHostsPerZone: NotRequired[MinimumHealthyHostsPerZoneTypeDef]

class RevisionLocationTypeDef(TypedDict):
    revisionType: NotRequired[RevisionLocationTypeType]
    s3Location: NotRequired[S3LocationTypeDef]
    gitHubLocation: NotRequired[GitHubLocationTypeDef]
    string: NotRequired[RawStringTypeDef]
    appSpecContent: NotRequired[AppSpecContentTypeDef]

class TargetGroupPairInfoOutputTypeDef(TypedDict):
    targetGroups: NotRequired[List[TargetGroupInfoTypeDef]]
    prodTrafficRoute: NotRequired[TrafficRouteOutputTypeDef]
    testTrafficRoute: NotRequired[TrafficRouteOutputTypeDef]

TrafficRoutingConfigTypeDef = TypedDict(
    "TrafficRoutingConfigTypeDef",
    {
        "type": NotRequired[TrafficRoutingTypeType],
        "timeBasedCanary": NotRequired[TimeBasedCanaryTypeDef],
        "timeBasedLinear": NotRequired[TimeBasedLinearTypeDef],
    },
)

class TimeRangeTypeDef(TypedDict):
    start: NotRequired[TimestampTypeDef]
    end: NotRequired[TimestampTypeDef]

TrafficRouteUnionTypeDef = Union[TrafficRouteTypeDef, TrafficRouteOutputTypeDef]
TriggerConfigUnionTypeDef = Union[TriggerConfigTypeDef, TriggerConfigOutputTypeDef]

class BatchGetOnPremisesInstancesOutputTypeDef(TypedDict):
    instanceInfos: List[InstanceInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetOnPremisesInstanceOutputTypeDef(TypedDict):
    instanceInfo: InstanceInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class TargetInstancesOutputTypeDef(TypedDict):
    tagFilters: NotRequired[List[EC2TagFilterTypeDef]]
    autoScalingGroups: NotRequired[List[str]]
    ec2TagSet: NotRequired[EC2TagSetOutputTypeDef]

EC2TagSetUnionTypeDef = Union[EC2TagSetTypeDef, EC2TagSetOutputTypeDef]

class CloudFormationTargetTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    targetId: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]
    lifecycleEvents: NotRequired[List[LifecycleEventTypeDef]]
    status: NotRequired[TargetStatusType]
    resourceType: NotRequired[str]
    targetVersionWeight: NotRequired[float]

class InstanceSummaryTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    instanceId: NotRequired[str]
    status: NotRequired[InstanceStatusType]
    lastUpdatedAt: NotRequired[datetime]
    lifecycleEvents: NotRequired[List[LifecycleEventTypeDef]]
    instanceType: NotRequired[InstanceTypeType]

class InstanceTargetTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    targetId: NotRequired[str]
    targetArn: NotRequired[str]
    status: NotRequired[TargetStatusType]
    lastUpdatedAt: NotRequired[datetime]
    lifecycleEvents: NotRequired[List[LifecycleEventTypeDef]]
    instanceLabel: NotRequired[TargetLabelType]

class LambdaTargetTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    targetId: NotRequired[str]
    targetArn: NotRequired[str]
    status: NotRequired[TargetStatusType]
    lastUpdatedAt: NotRequired[datetime]
    lifecycleEvents: NotRequired[List[LifecycleEventTypeDef]]
    lambdaFunctionInfo: NotRequired[LambdaFunctionInfoTypeDef]

class ECSTargetTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    targetId: NotRequired[str]
    targetArn: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]
    lifecycleEvents: NotRequired[List[LifecycleEventTypeDef]]
    status: NotRequired[TargetStatusType]
    taskSetsInfo: NotRequired[List[ECSTaskSetTypeDef]]

class BatchGetApplicationRevisionsInputRequestTypeDef(TypedDict):
    applicationName: str
    revisions: Sequence[RevisionLocationTypeDef]

class GetApplicationRevisionInputRequestTypeDef(TypedDict):
    applicationName: str
    revision: RevisionLocationTypeDef

class GetApplicationRevisionOutputTypeDef(TypedDict):
    applicationName: str
    revision: RevisionLocationTypeDef
    revisionInfo: GenericRevisionInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationRevisionsOutputTypeDef(TypedDict):
    revisions: List[RevisionLocationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RegisterApplicationRevisionInputRequestTypeDef(TypedDict):
    applicationName: str
    revision: RevisionLocationTypeDef
    description: NotRequired[str]

class RevisionInfoTypeDef(TypedDict):
    revisionLocation: NotRequired[RevisionLocationTypeDef]
    genericRevisionInfo: NotRequired[GenericRevisionInfoTypeDef]

class LoadBalancerInfoOutputTypeDef(TypedDict):
    elbInfoList: NotRequired[List[ELBInfoTypeDef]]
    targetGroupInfoList: NotRequired[List[TargetGroupInfoTypeDef]]
    targetGroupPairInfoList: NotRequired[List[TargetGroupPairInfoOutputTypeDef]]

class CreateDeploymentConfigInputRequestTypeDef(TypedDict):
    deploymentConfigName: str
    minimumHealthyHosts: NotRequired[MinimumHealthyHostsTypeDef]
    trafficRoutingConfig: NotRequired[TrafficRoutingConfigTypeDef]
    computePlatform: NotRequired[ComputePlatformType]
    zonalConfig: NotRequired[ZonalConfigTypeDef]

class DeploymentConfigInfoTypeDef(TypedDict):
    deploymentConfigId: NotRequired[str]
    deploymentConfigName: NotRequired[str]
    minimumHealthyHosts: NotRequired[MinimumHealthyHostsTypeDef]
    createTime: NotRequired[datetime]
    computePlatform: NotRequired[ComputePlatformType]
    trafficRoutingConfig: NotRequired[TrafficRoutingConfigTypeDef]
    zonalConfig: NotRequired[ZonalConfigTypeDef]

class ListDeploymentsInputListDeploymentsPaginateTypeDef(TypedDict):
    applicationName: NotRequired[str]
    deploymentGroupName: NotRequired[str]
    externalId: NotRequired[str]
    includeOnlyStatuses: NotRequired[Sequence[DeploymentStatusType]]
    createTimeRange: NotRequired[TimeRangeTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeploymentsInputRequestTypeDef(TypedDict):
    applicationName: NotRequired[str]
    deploymentGroupName: NotRequired[str]
    externalId: NotRequired[str]
    includeOnlyStatuses: NotRequired[Sequence[DeploymentStatusType]]
    createTimeRange: NotRequired[TimeRangeTypeDef]
    nextToken: NotRequired[str]

class TargetGroupPairInfoTypeDef(TypedDict):
    targetGroups: NotRequired[Sequence[TargetGroupInfoTypeDef]]
    prodTrafficRoute: NotRequired[TrafficRouteUnionTypeDef]
    testTrafficRoute: NotRequired[TrafficRouteUnionTypeDef]

class TargetInstancesTypeDef(TypedDict):
    tagFilters: NotRequired[Sequence[EC2TagFilterTypeDef]]
    autoScalingGroups: NotRequired[Sequence[str]]
    ec2TagSet: NotRequired[EC2TagSetUnionTypeDef]

class BatchGetDeploymentInstancesOutputTypeDef(TypedDict):
    instancesSummary: List[InstanceSummaryTypeDef]
    errorMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeploymentInstanceOutputTypeDef(TypedDict):
    instanceSummary: InstanceSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeploymentTargetTypeDef(TypedDict):
    deploymentTargetType: NotRequired[DeploymentTargetTypeType]
    instanceTarget: NotRequired[InstanceTargetTypeDef]
    lambdaTarget: NotRequired[LambdaTargetTypeDef]
    ecsTarget: NotRequired[ECSTargetTypeDef]
    cloudFormationTarget: NotRequired[CloudFormationTargetTypeDef]

class BatchGetApplicationRevisionsOutputTypeDef(TypedDict):
    applicationName: str
    errorMessage: str
    revisions: List[RevisionInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeploymentGroupInfoTypeDef(TypedDict):
    applicationName: NotRequired[str]
    deploymentGroupId: NotRequired[str]
    deploymentGroupName: NotRequired[str]
    deploymentConfigName: NotRequired[str]
    ec2TagFilters: NotRequired[List[EC2TagFilterTypeDef]]
    onPremisesInstanceTagFilters: NotRequired[List[TagFilterTypeDef]]
    autoScalingGroups: NotRequired[List[AutoScalingGroupTypeDef]]
    serviceRoleArn: NotRequired[str]
    targetRevision: NotRequired[RevisionLocationTypeDef]
    triggerConfigurations: NotRequired[List[TriggerConfigOutputTypeDef]]
    alarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    autoRollbackConfiguration: NotRequired[AutoRollbackConfigurationOutputTypeDef]
    deploymentStyle: NotRequired[DeploymentStyleTypeDef]
    outdatedInstancesStrategy: NotRequired[OutdatedInstancesStrategyType]
    blueGreenDeploymentConfiguration: NotRequired[BlueGreenDeploymentConfigurationTypeDef]
    loadBalancerInfo: NotRequired[LoadBalancerInfoOutputTypeDef]
    lastSuccessfulDeployment: NotRequired[LastDeploymentInfoTypeDef]
    lastAttemptedDeployment: NotRequired[LastDeploymentInfoTypeDef]
    ec2TagSet: NotRequired[EC2TagSetOutputTypeDef]
    onPremisesTagSet: NotRequired[OnPremisesTagSetOutputTypeDef]
    computePlatform: NotRequired[ComputePlatformType]
    ecsServices: NotRequired[List[ECSServiceTypeDef]]
    terminationHookEnabled: NotRequired[bool]

class DeploymentInfoTypeDef(TypedDict):
    applicationName: NotRequired[str]
    deploymentGroupName: NotRequired[str]
    deploymentConfigName: NotRequired[str]
    deploymentId: NotRequired[str]
    previousRevision: NotRequired[RevisionLocationTypeDef]
    revision: NotRequired[RevisionLocationTypeDef]
    status: NotRequired[DeploymentStatusType]
    errorInformation: NotRequired[ErrorInformationTypeDef]
    createTime: NotRequired[datetime]
    startTime: NotRequired[datetime]
    completeTime: NotRequired[datetime]
    deploymentOverview: NotRequired[DeploymentOverviewTypeDef]
    description: NotRequired[str]
    creator: NotRequired[DeploymentCreatorType]
    ignoreApplicationStopFailures: NotRequired[bool]
    autoRollbackConfiguration: NotRequired[AutoRollbackConfigurationOutputTypeDef]
    updateOutdatedInstancesOnly: NotRequired[bool]
    rollbackInfo: NotRequired[RollbackInfoTypeDef]
    deploymentStyle: NotRequired[DeploymentStyleTypeDef]
    targetInstances: NotRequired[TargetInstancesOutputTypeDef]
    instanceTerminationWaitTimeStarted: NotRequired[bool]
    blueGreenDeploymentConfiguration: NotRequired[BlueGreenDeploymentConfigurationTypeDef]
    loadBalancerInfo: NotRequired[LoadBalancerInfoOutputTypeDef]
    additionalDeploymentStatusInfo: NotRequired[str]
    fileExistsBehavior: NotRequired[FileExistsBehaviorType]
    deploymentStatusMessages: NotRequired[List[str]]
    computePlatform: NotRequired[ComputePlatformType]
    externalId: NotRequired[str]
    relatedDeployments: NotRequired[RelatedDeploymentsTypeDef]
    overrideAlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]

class GetDeploymentConfigOutputTypeDef(TypedDict):
    deploymentConfigInfo: DeploymentConfigInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

TargetGroupPairInfoUnionTypeDef = Union[
    TargetGroupPairInfoTypeDef, TargetGroupPairInfoOutputTypeDef
]

class CreateDeploymentInputRequestTypeDef(TypedDict):
    applicationName: str
    deploymentGroupName: NotRequired[str]
    revision: NotRequired[RevisionLocationTypeDef]
    deploymentConfigName: NotRequired[str]
    description: NotRequired[str]
    ignoreApplicationStopFailures: NotRequired[bool]
    targetInstances: NotRequired[TargetInstancesTypeDef]
    autoRollbackConfiguration: NotRequired[AutoRollbackConfigurationTypeDef]
    updateOutdatedInstancesOnly: NotRequired[bool]
    fileExistsBehavior: NotRequired[FileExistsBehaviorType]
    overrideAlarmConfiguration: NotRequired[AlarmConfigurationTypeDef]

class BatchGetDeploymentTargetsOutputTypeDef(TypedDict):
    deploymentTargets: List[DeploymentTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeploymentTargetOutputTypeDef(TypedDict):
    deploymentTarget: DeploymentTargetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetDeploymentGroupsOutputTypeDef(TypedDict):
    deploymentGroupsInfo: List[DeploymentGroupInfoTypeDef]
    errorMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeploymentGroupOutputTypeDef(TypedDict):
    deploymentGroupInfo: DeploymentGroupInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetDeploymentsOutputTypeDef(TypedDict):
    deploymentsInfo: List[DeploymentInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeploymentOutputTypeDef(TypedDict):
    deploymentInfo: DeploymentInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class LoadBalancerInfoTypeDef(TypedDict):
    elbInfoList: NotRequired[Sequence[ELBInfoTypeDef]]
    targetGroupInfoList: NotRequired[Sequence[TargetGroupInfoTypeDef]]
    targetGroupPairInfoList: NotRequired[Sequence[TargetGroupPairInfoUnionTypeDef]]

class CreateDeploymentGroupInputRequestTypeDef(TypedDict):
    applicationName: str
    deploymentGroupName: str
    serviceRoleArn: str
    deploymentConfigName: NotRequired[str]
    ec2TagFilters: NotRequired[Sequence[EC2TagFilterTypeDef]]
    onPremisesInstanceTagFilters: NotRequired[Sequence[TagFilterTypeDef]]
    autoScalingGroups: NotRequired[Sequence[str]]
    triggerConfigurations: NotRequired[Sequence[TriggerConfigUnionTypeDef]]
    alarmConfiguration: NotRequired[AlarmConfigurationTypeDef]
    autoRollbackConfiguration: NotRequired[AutoRollbackConfigurationTypeDef]
    outdatedInstancesStrategy: NotRequired[OutdatedInstancesStrategyType]
    deploymentStyle: NotRequired[DeploymentStyleTypeDef]
    blueGreenDeploymentConfiguration: NotRequired[BlueGreenDeploymentConfigurationTypeDef]
    loadBalancerInfo: NotRequired[LoadBalancerInfoTypeDef]
    ec2TagSet: NotRequired[EC2TagSetTypeDef]
    ecsServices: NotRequired[Sequence[ECSServiceTypeDef]]
    onPremisesTagSet: NotRequired[OnPremisesTagSetTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    terminationHookEnabled: NotRequired[bool]

class UpdateDeploymentGroupInputRequestTypeDef(TypedDict):
    applicationName: str
    currentDeploymentGroupName: str
    newDeploymentGroupName: NotRequired[str]
    deploymentConfigName: NotRequired[str]
    ec2TagFilters: NotRequired[Sequence[EC2TagFilterTypeDef]]
    onPremisesInstanceTagFilters: NotRequired[Sequence[TagFilterTypeDef]]
    autoScalingGroups: NotRequired[Sequence[str]]
    serviceRoleArn: NotRequired[str]
    triggerConfigurations: NotRequired[Sequence[TriggerConfigTypeDef]]
    alarmConfiguration: NotRequired[AlarmConfigurationTypeDef]
    autoRollbackConfiguration: NotRequired[AutoRollbackConfigurationTypeDef]
    outdatedInstancesStrategy: NotRequired[OutdatedInstancesStrategyType]
    deploymentStyle: NotRequired[DeploymentStyleTypeDef]
    blueGreenDeploymentConfiguration: NotRequired[BlueGreenDeploymentConfigurationTypeDef]
    loadBalancerInfo: NotRequired[LoadBalancerInfoTypeDef]
    ec2TagSet: NotRequired[EC2TagSetTypeDef]
    ecsServices: NotRequired[Sequence[ECSServiceTypeDef]]
    onPremisesTagSet: NotRequired[OnPremisesTagSetTypeDef]
    terminationHookEnabled: NotRequired[bool]
