"""
Type annotations for robomaker service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/type_defs/)

Usage::

    ```python
    from mypy_boto3_robomaker.type_defs import BatchDeleteWorldsRequestRequestTypeDef

    data: BatchDeleteWorldsRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ArchitectureType,
    ComputeTypeType,
    DataSourceTypeType,
    DeploymentJobErrorCodeType,
    DeploymentStatusType,
    ExitBehaviorType,
    FailureBehaviorType,
    RobotDeploymentStepType,
    RobotSoftwareSuiteTypeType,
    RobotSoftwareSuiteVersionTypeType,
    RobotStatusType,
    SimulationJobBatchStatusType,
    SimulationJobErrorCodeType,
    SimulationJobStatusType,
    SimulationSoftwareSuiteTypeType,
    UploadBehaviorType,
    WorldExportJobErrorCodeType,
    WorldExportJobStatusType,
    WorldGenerationJobErrorCodeType,
    WorldGenerationJobStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "BatchDeleteWorldsRequestRequestTypeDef",
    "BatchDeleteWorldsResponseTypeDef",
    "BatchDescribeSimulationJobRequestRequestTypeDef",
    "BatchDescribeSimulationJobResponseTypeDef",
    "BatchPolicyTypeDef",
    "CancelDeploymentJobRequestRequestTypeDef",
    "CancelSimulationJobBatchRequestRequestTypeDef",
    "CancelSimulationJobRequestRequestTypeDef",
    "CancelWorldExportJobRequestRequestTypeDef",
    "CancelWorldGenerationJobRequestRequestTypeDef",
    "ComputeResponseTypeDef",
    "ComputeTypeDef",
    "CreateDeploymentJobRequestRequestTypeDef",
    "CreateDeploymentJobResponseTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "CreateFleetResponseTypeDef",
    "CreateRobotApplicationRequestRequestTypeDef",
    "CreateRobotApplicationResponseTypeDef",
    "CreateRobotApplicationVersionRequestRequestTypeDef",
    "CreateRobotApplicationVersionResponseTypeDef",
    "CreateRobotRequestRequestTypeDef",
    "CreateRobotResponseTypeDef",
    "CreateSimulationApplicationRequestRequestTypeDef",
    "CreateSimulationApplicationResponseTypeDef",
    "CreateSimulationApplicationVersionRequestRequestTypeDef",
    "CreateSimulationApplicationVersionResponseTypeDef",
    "CreateSimulationJobRequestRequestTypeDef",
    "CreateSimulationJobResponseTypeDef",
    "CreateWorldExportJobRequestRequestTypeDef",
    "CreateWorldExportJobResponseTypeDef",
    "CreateWorldGenerationJobRequestRequestTypeDef",
    "CreateWorldGenerationJobResponseTypeDef",
    "CreateWorldTemplateRequestRequestTypeDef",
    "CreateWorldTemplateResponseTypeDef",
    "DataSourceConfigOutputTypeDef",
    "DataSourceConfigTypeDef",
    "DataSourceConfigUnionTypeDef",
    "DataSourceTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DeleteRobotApplicationRequestRequestTypeDef",
    "DeleteRobotRequestRequestTypeDef",
    "DeleteSimulationApplicationRequestRequestTypeDef",
    "DeleteWorldTemplateRequestRequestTypeDef",
    "DeploymentApplicationConfigOutputTypeDef",
    "DeploymentApplicationConfigTypeDef",
    "DeploymentApplicationConfigUnionTypeDef",
    "DeploymentConfigTypeDef",
    "DeploymentJobTypeDef",
    "DeploymentLaunchConfigOutputTypeDef",
    "DeploymentLaunchConfigTypeDef",
    "DeploymentLaunchConfigUnionTypeDef",
    "DeregisterRobotRequestRequestTypeDef",
    "DeregisterRobotResponseTypeDef",
    "DescribeDeploymentJobRequestRequestTypeDef",
    "DescribeDeploymentJobResponseTypeDef",
    "DescribeFleetRequestRequestTypeDef",
    "DescribeFleetResponseTypeDef",
    "DescribeRobotApplicationRequestRequestTypeDef",
    "DescribeRobotApplicationResponseTypeDef",
    "DescribeRobotRequestRequestTypeDef",
    "DescribeRobotResponseTypeDef",
    "DescribeSimulationApplicationRequestRequestTypeDef",
    "DescribeSimulationApplicationResponseTypeDef",
    "DescribeSimulationJobBatchRequestRequestTypeDef",
    "DescribeSimulationJobBatchResponseTypeDef",
    "DescribeSimulationJobRequestRequestTypeDef",
    "DescribeSimulationJobResponseTypeDef",
    "DescribeWorldExportJobRequestRequestTypeDef",
    "DescribeWorldExportJobResponseTypeDef",
    "DescribeWorldGenerationJobRequestRequestTypeDef",
    "DescribeWorldGenerationJobResponseTypeDef",
    "DescribeWorldRequestRequestTypeDef",
    "DescribeWorldResponseTypeDef",
    "DescribeWorldTemplateRequestRequestTypeDef",
    "DescribeWorldTemplateResponseTypeDef",
    "EnvironmentTypeDef",
    "FailedCreateSimulationJobRequestTypeDef",
    "FailureSummaryTypeDef",
    "FilterTypeDef",
    "FinishedWorldsSummaryTypeDef",
    "FleetTypeDef",
    "GetWorldTemplateBodyRequestRequestTypeDef",
    "GetWorldTemplateBodyResponseTypeDef",
    "LaunchConfigOutputTypeDef",
    "LaunchConfigTypeDef",
    "LaunchConfigUnionTypeDef",
    "ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef",
    "ListDeploymentJobsRequestRequestTypeDef",
    "ListDeploymentJobsResponseTypeDef",
    "ListFleetsRequestListFleetsPaginateTypeDef",
    "ListFleetsRequestRequestTypeDef",
    "ListFleetsResponseTypeDef",
    "ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef",
    "ListRobotApplicationsRequestRequestTypeDef",
    "ListRobotApplicationsResponseTypeDef",
    "ListRobotsRequestListRobotsPaginateTypeDef",
    "ListRobotsRequestRequestTypeDef",
    "ListRobotsResponseTypeDef",
    "ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef",
    "ListSimulationApplicationsRequestRequestTypeDef",
    "ListSimulationApplicationsResponseTypeDef",
    "ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef",
    "ListSimulationJobBatchesRequestRequestTypeDef",
    "ListSimulationJobBatchesResponseTypeDef",
    "ListSimulationJobsRequestListSimulationJobsPaginateTypeDef",
    "ListSimulationJobsRequestRequestTypeDef",
    "ListSimulationJobsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef",
    "ListWorldExportJobsRequestRequestTypeDef",
    "ListWorldExportJobsResponseTypeDef",
    "ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef",
    "ListWorldGenerationJobsRequestRequestTypeDef",
    "ListWorldGenerationJobsResponseTypeDef",
    "ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef",
    "ListWorldTemplatesRequestRequestTypeDef",
    "ListWorldTemplatesResponseTypeDef",
    "ListWorldsRequestListWorldsPaginateTypeDef",
    "ListWorldsRequestRequestTypeDef",
    "ListWorldsResponseTypeDef",
    "LoggingConfigTypeDef",
    "NetworkInterfaceTypeDef",
    "OutputLocationTypeDef",
    "PaginatorConfigTypeDef",
    "PortForwardingConfigOutputTypeDef",
    "PortForwardingConfigTypeDef",
    "PortForwardingConfigUnionTypeDef",
    "PortMappingTypeDef",
    "ProgressDetailTypeDef",
    "RegisterRobotRequestRequestTypeDef",
    "RegisterRobotResponseTypeDef",
    "RenderingEngineTypeDef",
    "ResponseMetadataTypeDef",
    "RestartSimulationJobRequestRequestTypeDef",
    "RobotApplicationConfigOutputTypeDef",
    "RobotApplicationConfigTypeDef",
    "RobotApplicationConfigUnionTypeDef",
    "RobotApplicationSummaryTypeDef",
    "RobotDeploymentTypeDef",
    "RobotSoftwareSuiteTypeDef",
    "RobotTypeDef",
    "S3KeyOutputTypeDef",
    "S3ObjectTypeDef",
    "SimulationApplicationConfigOutputTypeDef",
    "SimulationApplicationConfigTypeDef",
    "SimulationApplicationConfigUnionTypeDef",
    "SimulationApplicationSummaryTypeDef",
    "SimulationJobBatchSummaryTypeDef",
    "SimulationJobRequestOutputTypeDef",
    "SimulationJobRequestTypeDef",
    "SimulationJobRequestUnionTypeDef",
    "SimulationJobSummaryTypeDef",
    "SimulationJobTypeDef",
    "SimulationSoftwareSuiteTypeDef",
    "SourceConfigTypeDef",
    "SourceTypeDef",
    "StartSimulationJobBatchRequestRequestTypeDef",
    "StartSimulationJobBatchResponseTypeDef",
    "SyncDeploymentJobRequestRequestTypeDef",
    "SyncDeploymentJobResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TemplateLocationTypeDef",
    "TemplateSummaryTypeDef",
    "ToolTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateRobotApplicationRequestRequestTypeDef",
    "UpdateRobotApplicationResponseTypeDef",
    "UpdateSimulationApplicationRequestRequestTypeDef",
    "UpdateSimulationApplicationResponseTypeDef",
    "UpdateWorldTemplateRequestRequestTypeDef",
    "UpdateWorldTemplateResponseTypeDef",
    "UploadConfigurationTypeDef",
    "VPCConfigOutputTypeDef",
    "VPCConfigResponseTypeDef",
    "VPCConfigTypeDef",
    "VPCConfigUnionTypeDef",
    "WorldConfigTypeDef",
    "WorldCountTypeDef",
    "WorldExportJobSummaryTypeDef",
    "WorldFailureTypeDef",
    "WorldGenerationJobSummaryTypeDef",
    "WorldSummaryTypeDef",
)

class BatchDeleteWorldsRequestRequestTypeDef(TypedDict):
    worlds: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchDescribeSimulationJobRequestRequestTypeDef(TypedDict):
    jobs: Sequence[str]

class BatchPolicyTypeDef(TypedDict):
    timeoutInSeconds: NotRequired[int]
    maxConcurrency: NotRequired[int]

class CancelDeploymentJobRequestRequestTypeDef(TypedDict):
    job: str

class CancelSimulationJobBatchRequestRequestTypeDef(TypedDict):
    batch: str

class CancelSimulationJobRequestRequestTypeDef(TypedDict):
    job: str

class CancelWorldExportJobRequestRequestTypeDef(TypedDict):
    job: str

class CancelWorldGenerationJobRequestRequestTypeDef(TypedDict):
    job: str

class ComputeResponseTypeDef(TypedDict):
    simulationUnitLimit: NotRequired[int]
    computeType: NotRequired[ComputeTypeType]
    gpuUnitLimit: NotRequired[int]

class ComputeTypeDef(TypedDict):
    simulationUnitLimit: NotRequired[int]
    computeType: NotRequired[ComputeTypeType]
    gpuUnitLimit: NotRequired[int]

class CreateFleetRequestRequestTypeDef(TypedDict):
    name: str
    tags: NotRequired[Mapping[str, str]]

class EnvironmentTypeDef(TypedDict):
    uri: NotRequired[str]

class RobotSoftwareSuiteTypeDef(TypedDict):
    name: NotRequired[RobotSoftwareSuiteTypeType]
    version: NotRequired[RobotSoftwareSuiteVersionTypeType]

class SourceConfigTypeDef(TypedDict):
    s3Bucket: NotRequired[str]
    s3Key: NotRequired[str]
    architecture: NotRequired[ArchitectureType]

class SourceTypeDef(TypedDict):
    s3Bucket: NotRequired[str]
    s3Key: NotRequired[str]
    etag: NotRequired[str]
    architecture: NotRequired[ArchitectureType]

class CreateRobotApplicationVersionRequestRequestTypeDef(TypedDict):
    application: str
    currentRevisionId: NotRequired[str]
    s3Etags: NotRequired[Sequence[str]]
    imageDigest: NotRequired[str]

class CreateRobotRequestRequestTypeDef(TypedDict):
    name: str
    architecture: ArchitectureType
    greengrassGroupId: str
    tags: NotRequired[Mapping[str, str]]

class RenderingEngineTypeDef(TypedDict):
    name: NotRequired[Literal["OGRE"]]
    version: NotRequired[str]

class SimulationSoftwareSuiteTypeDef(TypedDict):
    name: NotRequired[SimulationSoftwareSuiteTypeType]
    version: NotRequired[str]

class CreateSimulationApplicationVersionRequestRequestTypeDef(TypedDict):
    application: str
    currentRevisionId: NotRequired[str]
    s3Etags: NotRequired[Sequence[str]]
    imageDigest: NotRequired[str]

class LoggingConfigTypeDef(TypedDict):
    recordAllRosTopics: NotRequired[bool]

class OutputLocationTypeDef(TypedDict):
    s3Bucket: NotRequired[str]
    s3Prefix: NotRequired[str]

class VPCConfigTypeDef(TypedDict):
    subnets: Sequence[str]
    securityGroups: NotRequired[Sequence[str]]
    assignPublicIp: NotRequired[bool]

class VPCConfigResponseTypeDef(TypedDict):
    subnets: NotRequired[List[str]]
    securityGroups: NotRequired[List[str]]
    vpcId: NotRequired[str]
    assignPublicIp: NotRequired[bool]

class WorldCountTypeDef(TypedDict):
    floorplanCount: NotRequired[int]
    interiorCountPerFloorplan: NotRequired[int]

class TemplateLocationTypeDef(TypedDict):
    s3Bucket: str
    s3Key: str

DataSourceConfigOutputTypeDef = TypedDict(
    "DataSourceConfigOutputTypeDef",
    {
        "name": str,
        "s3Bucket": str,
        "s3Keys": List[str],
        "type": NotRequired[DataSourceTypeType],
        "destination": NotRequired[str],
    },
)
DataSourceConfigTypeDef = TypedDict(
    "DataSourceConfigTypeDef",
    {
        "name": str,
        "s3Bucket": str,
        "s3Keys": Sequence[str],
        "type": NotRequired[DataSourceTypeType],
        "destination": NotRequired[str],
    },
)

class S3KeyOutputTypeDef(TypedDict):
    s3Key: NotRequired[str]
    etag: NotRequired[str]

class DeleteFleetRequestRequestTypeDef(TypedDict):
    fleet: str

class DeleteRobotApplicationRequestRequestTypeDef(TypedDict):
    application: str
    applicationVersion: NotRequired[str]

class DeleteRobotRequestRequestTypeDef(TypedDict):
    robot: str

class DeleteSimulationApplicationRequestRequestTypeDef(TypedDict):
    application: str
    applicationVersion: NotRequired[str]

class DeleteWorldTemplateRequestRequestTypeDef(TypedDict):
    template: str

class DeploymentLaunchConfigOutputTypeDef(TypedDict):
    packageName: str
    launchFile: str
    preLaunchFile: NotRequired[str]
    postLaunchFile: NotRequired[str]
    environmentVariables: NotRequired[Dict[str, str]]

class S3ObjectTypeDef(TypedDict):
    bucket: str
    key: str
    etag: NotRequired[str]

class DeploymentLaunchConfigTypeDef(TypedDict):
    packageName: str
    launchFile: str
    preLaunchFile: NotRequired[str]
    postLaunchFile: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]

class DeregisterRobotRequestRequestTypeDef(TypedDict):
    fleet: str
    robot: str

class DescribeDeploymentJobRequestRequestTypeDef(TypedDict):
    job: str

class DescribeFleetRequestRequestTypeDef(TypedDict):
    fleet: str

class RobotTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    fleetArn: NotRequired[str]
    status: NotRequired[RobotStatusType]
    greenGrassGroupId: NotRequired[str]
    createdAt: NotRequired[datetime]
    architecture: NotRequired[ArchitectureType]
    lastDeploymentJob: NotRequired[str]
    lastDeploymentTime: NotRequired[datetime]

class DescribeRobotApplicationRequestRequestTypeDef(TypedDict):
    application: str
    applicationVersion: NotRequired[str]

class DescribeRobotRequestRequestTypeDef(TypedDict):
    robot: str

class DescribeSimulationApplicationRequestRequestTypeDef(TypedDict):
    application: str
    applicationVersion: NotRequired[str]

class DescribeSimulationJobBatchRequestRequestTypeDef(TypedDict):
    batch: str

class SimulationJobSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]
    name: NotRequired[str]
    status: NotRequired[SimulationJobStatusType]
    simulationApplicationNames: NotRequired[List[str]]
    robotApplicationNames: NotRequired[List[str]]
    dataSourceNames: NotRequired[List[str]]
    computeType: NotRequired[ComputeTypeType]

class DescribeSimulationJobRequestRequestTypeDef(TypedDict):
    job: str

class NetworkInterfaceTypeDef(TypedDict):
    networkInterfaceId: NotRequired[str]
    privateIpAddress: NotRequired[str]
    publicIpAddress: NotRequired[str]

class DescribeWorldExportJobRequestRequestTypeDef(TypedDict):
    job: str

class DescribeWorldGenerationJobRequestRequestTypeDef(TypedDict):
    job: str

class DescribeWorldRequestRequestTypeDef(TypedDict):
    world: str

class DescribeWorldTemplateRequestRequestTypeDef(TypedDict):
    template: str

class WorldFailureTypeDef(TypedDict):
    failureCode: NotRequired[WorldGenerationJobErrorCodeType]
    sampleFailureReason: NotRequired[str]
    failureCount: NotRequired[int]

class FilterTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]

class FleetTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    lastDeploymentStatus: NotRequired[DeploymentStatusType]
    lastDeploymentJob: NotRequired[str]
    lastDeploymentTime: NotRequired[datetime]

class GetWorldTemplateBodyRequestRequestTypeDef(TypedDict):
    template: NotRequired[str]
    generationJob: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class SimulationJobBatchSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]
    createdAt: NotRequired[datetime]
    status: NotRequired[SimulationJobBatchStatusType]
    failedRequestCount: NotRequired[int]
    pendingRequestCount: NotRequired[int]
    createdRequestCount: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListWorldTemplatesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class TemplateSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    name: NotRequired[str]
    version: NotRequired[str]

class WorldSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    generationJob: NotRequired[str]
    template: NotRequired[str]

class PortMappingTypeDef(TypedDict):
    jobPort: int
    applicationPort: int
    enableOnPublicIp: NotRequired[bool]

class ProgressDetailTypeDef(TypedDict):
    currentProgress: NotRequired[RobotDeploymentStepType]
    percentDone: NotRequired[float]
    estimatedTimeRemainingSeconds: NotRequired[int]
    targetResource: NotRequired[str]

class RegisterRobotRequestRequestTypeDef(TypedDict):
    fleet: str
    robot: str

class RestartSimulationJobRequestRequestTypeDef(TypedDict):
    job: str

class ToolTypeDef(TypedDict):
    name: str
    command: str
    streamUI: NotRequired[bool]
    streamOutputToCloudWatch: NotRequired[bool]
    exitBehavior: NotRequired[ExitBehaviorType]

class UploadConfigurationTypeDef(TypedDict):
    name: str
    path: str
    uploadBehavior: UploadBehaviorType

class WorldConfigTypeDef(TypedDict):
    world: NotRequired[str]

class VPCConfigOutputTypeDef(TypedDict):
    subnets: List[str]
    securityGroups: NotRequired[List[str]]
    assignPublicIp: NotRequired[bool]

class SyncDeploymentJobRequestRequestTypeDef(TypedDict):
    clientRequestToken: str
    fleet: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class BatchDeleteWorldsResponseTypeDef(TypedDict):
    unprocessedWorlds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFleetResponseTypeDef(TypedDict):
    arn: str
    name: str
    createdAt: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRobotResponseTypeDef(TypedDict):
    arn: str
    name: str
    createdAt: datetime
    greengrassGroupId: str
    architecture: ArchitectureType
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorldTemplateResponseTypeDef(TypedDict):
    arn: str
    clientRequestToken: str
    createdAt: datetime
    name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeregisterRobotResponseTypeDef(TypedDict):
    fleet: str
    robot: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRobotResponseTypeDef(TypedDict):
    arn: str
    name: str
    fleetArn: str
    status: RobotStatusType
    greengrassGroupId: str
    createdAt: datetime
    architecture: ArchitectureType
    lastDeploymentJob: str
    lastDeploymentTime: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeWorldResponseTypeDef(TypedDict):
    arn: str
    generationJob: str
    template: str
    createdAt: datetime
    tags: Dict[str, str]
    worldDescriptionBody: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeWorldTemplateResponseTypeDef(TypedDict):
    arn: str
    clientRequestToken: str
    name: str
    createdAt: datetime
    lastUpdatedAt: datetime
    tags: Dict[str, str]
    version: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetWorldTemplateBodyResponseTypeDef(TypedDict):
    templateBody: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterRobotResponseTypeDef(TypedDict):
    fleet: str
    robot: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWorldTemplateResponseTypeDef(TypedDict):
    arn: str
    name: str
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class RobotApplicationSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    version: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]
    robotSoftwareSuite: NotRequired[RobotSoftwareSuiteTypeDef]

class CreateRobotApplicationRequestRequestTypeDef(TypedDict):
    name: str
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    sources: NotRequired[Sequence[SourceConfigTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    environment: NotRequired[EnvironmentTypeDef]

class UpdateRobotApplicationRequestRequestTypeDef(TypedDict):
    application: str
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    sources: NotRequired[Sequence[SourceConfigTypeDef]]
    currentRevisionId: NotRequired[str]
    environment: NotRequired[EnvironmentTypeDef]

class CreateRobotApplicationResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    lastUpdatedAt: datetime
    revisionId: str
    tags: Dict[str, str]
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRobotApplicationVersionResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    lastUpdatedAt: datetime
    revisionId: str
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRobotApplicationResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    revisionId: str
    lastUpdatedAt: datetime
    tags: Dict[str, str]
    environment: EnvironmentTypeDef
    imageDigest: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRobotApplicationResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    lastUpdatedAt: datetime
    revisionId: str
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSimulationApplicationRequestRequestTypeDef(TypedDict):
    name: str
    simulationSoftwareSuite: SimulationSoftwareSuiteTypeDef
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    sources: NotRequired[Sequence[SourceConfigTypeDef]]
    renderingEngine: NotRequired[RenderingEngineTypeDef]
    tags: NotRequired[Mapping[str, str]]
    environment: NotRequired[EnvironmentTypeDef]

class CreateSimulationApplicationResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    simulationSoftwareSuite: SimulationSoftwareSuiteTypeDef
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    renderingEngine: RenderingEngineTypeDef
    lastUpdatedAt: datetime
    revisionId: str
    tags: Dict[str, str]
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSimulationApplicationVersionResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    simulationSoftwareSuite: SimulationSoftwareSuiteTypeDef
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    renderingEngine: RenderingEngineTypeDef
    lastUpdatedAt: datetime
    revisionId: str
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSimulationApplicationResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    simulationSoftwareSuite: SimulationSoftwareSuiteTypeDef
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    renderingEngine: RenderingEngineTypeDef
    revisionId: str
    lastUpdatedAt: datetime
    tags: Dict[str, str]
    environment: EnvironmentTypeDef
    imageDigest: str
    ResponseMetadata: ResponseMetadataTypeDef

class SimulationApplicationSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    version: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]
    robotSoftwareSuite: NotRequired[RobotSoftwareSuiteTypeDef]
    simulationSoftwareSuite: NotRequired[SimulationSoftwareSuiteTypeDef]

class UpdateSimulationApplicationRequestRequestTypeDef(TypedDict):
    application: str
    simulationSoftwareSuite: SimulationSoftwareSuiteTypeDef
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    sources: NotRequired[Sequence[SourceConfigTypeDef]]
    renderingEngine: NotRequired[RenderingEngineTypeDef]
    currentRevisionId: NotRequired[str]
    environment: NotRequired[EnvironmentTypeDef]

class UpdateSimulationApplicationResponseTypeDef(TypedDict):
    arn: str
    name: str
    version: str
    sources: List[SourceTypeDef]
    simulationSoftwareSuite: SimulationSoftwareSuiteTypeDef
    robotSoftwareSuite: RobotSoftwareSuiteTypeDef
    renderingEngine: RenderingEngineTypeDef
    lastUpdatedAt: datetime
    revisionId: str
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorldExportJobRequestRequestTypeDef(TypedDict):
    worlds: Sequence[str]
    outputLocation: OutputLocationTypeDef
    iamRole: str
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateWorldExportJobResponseTypeDef(TypedDict):
    arn: str
    status: WorldExportJobStatusType
    createdAt: datetime
    failureCode: WorldExportJobErrorCodeType
    clientRequestToken: str
    outputLocation: OutputLocationTypeDef
    iamRole: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeWorldExportJobResponseTypeDef(TypedDict):
    arn: str
    status: WorldExportJobStatusType
    createdAt: datetime
    failureCode: WorldExportJobErrorCodeType
    failureReason: str
    clientRequestToken: str
    worlds: List[str]
    outputLocation: OutputLocationTypeDef
    iamRole: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class WorldExportJobSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    status: NotRequired[WorldExportJobStatusType]
    createdAt: NotRequired[datetime]
    worlds: NotRequired[List[str]]
    outputLocation: NotRequired[OutputLocationTypeDef]

class CreateWorldGenerationJobRequestRequestTypeDef(TypedDict):
    template: str
    worldCount: WorldCountTypeDef
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    worldTags: NotRequired[Mapping[str, str]]

class CreateWorldGenerationJobResponseTypeDef(TypedDict):
    arn: str
    status: WorldGenerationJobStatusType
    createdAt: datetime
    failureCode: WorldGenerationJobErrorCodeType
    clientRequestToken: str
    template: str
    worldCount: WorldCountTypeDef
    tags: Dict[str, str]
    worldTags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class WorldGenerationJobSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    template: NotRequired[str]
    createdAt: NotRequired[datetime]
    status: NotRequired[WorldGenerationJobStatusType]
    worldCount: NotRequired[WorldCountTypeDef]
    succeededWorldCount: NotRequired[int]
    failedWorldCount: NotRequired[int]

class CreateWorldTemplateRequestRequestTypeDef(TypedDict):
    clientRequestToken: NotRequired[str]
    name: NotRequired[str]
    templateBody: NotRequired[str]
    templateLocation: NotRequired[TemplateLocationTypeDef]
    tags: NotRequired[Mapping[str, str]]

class UpdateWorldTemplateRequestRequestTypeDef(TypedDict):
    template: str
    name: NotRequired[str]
    templateBody: NotRequired[str]
    templateLocation: NotRequired[TemplateLocationTypeDef]

DataSourceConfigUnionTypeDef = Union[DataSourceConfigTypeDef, DataSourceConfigOutputTypeDef]
DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "name": NotRequired[str],
        "s3Bucket": NotRequired[str],
        "s3Keys": NotRequired[List[S3KeyOutputTypeDef]],
        "type": NotRequired[DataSourceTypeType],
        "destination": NotRequired[str],
    },
)

class DeploymentApplicationConfigOutputTypeDef(TypedDict):
    application: str
    applicationVersion: str
    launchConfig: DeploymentLaunchConfigOutputTypeDef

class DeploymentConfigTypeDef(TypedDict):
    concurrentDeploymentPercentage: NotRequired[int]
    failureThresholdPercentage: NotRequired[int]
    robotDeploymentTimeoutInSeconds: NotRequired[int]
    downloadConditionFile: NotRequired[S3ObjectTypeDef]

DeploymentLaunchConfigUnionTypeDef = Union[
    DeploymentLaunchConfigTypeDef, DeploymentLaunchConfigOutputTypeDef
]

class DescribeFleetResponseTypeDef(TypedDict):
    name: str
    arn: str
    robots: List[RobotTypeDef]
    createdAt: datetime
    lastDeploymentStatus: DeploymentStatusType
    lastDeploymentJob: str
    lastDeploymentTime: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListRobotsResponseTypeDef(TypedDict):
    robots: List[RobotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSimulationJobsResponseTypeDef(TypedDict):
    simulationJobSummaries: List[SimulationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FailureSummaryTypeDef(TypedDict):
    totalFailureCount: NotRequired[int]
    failures: NotRequired[List[WorldFailureTypeDef]]

class ListDeploymentJobsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListFleetsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListRobotApplicationsRequestRequestTypeDef(TypedDict):
    versionQualifier: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListRobotsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListSimulationApplicationsRequestRequestTypeDef(TypedDict):
    versionQualifier: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListSimulationJobBatchesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListSimulationJobsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListWorldExportJobsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListWorldGenerationJobsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListWorldsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[FilterTypeDef]]

class ListFleetsResponseTypeDef(TypedDict):
    fleetDetails: List[FleetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFleetsRequestListFleetsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef(TypedDict):
    versionQualifier: NotRequired[str]
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRobotsRequestListRobotsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef(TypedDict):
    versionQualifier: NotRequired[str]
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSimulationJobsRequestListSimulationJobsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorldsRequestListWorldsPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSimulationJobBatchesResponseTypeDef(TypedDict):
    simulationJobBatchSummaries: List[SimulationJobBatchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorldTemplatesResponseTypeDef(TypedDict):
    templateSummaries: List[TemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorldsResponseTypeDef(TypedDict):
    worldSummaries: List[WorldSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PortForwardingConfigOutputTypeDef(TypedDict):
    portMappings: NotRequired[List[PortMappingTypeDef]]

class PortForwardingConfigTypeDef(TypedDict):
    portMappings: NotRequired[Sequence[PortMappingTypeDef]]

class RobotDeploymentTypeDef(TypedDict):
    arn: NotRequired[str]
    deploymentStartTime: NotRequired[datetime]
    deploymentFinishTime: NotRequired[datetime]
    status: NotRequired[RobotStatusType]
    progressDetail: NotRequired[ProgressDetailTypeDef]
    failureReason: NotRequired[str]
    failureCode: NotRequired[DeploymentJobErrorCodeType]

VPCConfigUnionTypeDef = Union[VPCConfigTypeDef, VPCConfigOutputTypeDef]

class ListRobotApplicationsResponseTypeDef(TypedDict):
    robotApplicationSummaries: List[RobotApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSimulationApplicationsResponseTypeDef(TypedDict):
    simulationApplicationSummaries: List[SimulationApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorldExportJobsResponseTypeDef(TypedDict):
    worldExportJobSummaries: List[WorldExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorldGenerationJobsResponseTypeDef(TypedDict):
    worldGenerationJobSummaries: List[WorldGenerationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateDeploymentJobResponseTypeDef(TypedDict):
    arn: str
    fleet: str
    status: DeploymentStatusType
    deploymentApplicationConfigs: List[DeploymentApplicationConfigOutputTypeDef]
    failureReason: str
    failureCode: DeploymentJobErrorCodeType
    createdAt: datetime
    deploymentConfig: DeploymentConfigTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeploymentJobTypeDef(TypedDict):
    arn: NotRequired[str]
    fleet: NotRequired[str]
    status: NotRequired[DeploymentStatusType]
    deploymentApplicationConfigs: NotRequired[List[DeploymentApplicationConfigOutputTypeDef]]
    deploymentConfig: NotRequired[DeploymentConfigTypeDef]
    failureReason: NotRequired[str]
    failureCode: NotRequired[DeploymentJobErrorCodeType]
    createdAt: NotRequired[datetime]

class SyncDeploymentJobResponseTypeDef(TypedDict):
    arn: str
    fleet: str
    status: DeploymentStatusType
    deploymentConfig: DeploymentConfigTypeDef
    deploymentApplicationConfigs: List[DeploymentApplicationConfigOutputTypeDef]
    failureReason: str
    failureCode: DeploymentJobErrorCodeType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DeploymentApplicationConfigTypeDef(TypedDict):
    application: str
    applicationVersion: str
    launchConfig: DeploymentLaunchConfigUnionTypeDef

class FinishedWorldsSummaryTypeDef(TypedDict):
    finishedCount: NotRequired[int]
    succeededWorlds: NotRequired[List[str]]
    failureSummary: NotRequired[FailureSummaryTypeDef]

class LaunchConfigOutputTypeDef(TypedDict):
    packageName: NotRequired[str]
    launchFile: NotRequired[str]
    environmentVariables: NotRequired[Dict[str, str]]
    portForwardingConfig: NotRequired[PortForwardingConfigOutputTypeDef]
    streamUI: NotRequired[bool]
    command: NotRequired[List[str]]

PortForwardingConfigUnionTypeDef = Union[
    PortForwardingConfigTypeDef, PortForwardingConfigOutputTypeDef
]

class DescribeDeploymentJobResponseTypeDef(TypedDict):
    arn: str
    fleet: str
    status: DeploymentStatusType
    deploymentConfig: DeploymentConfigTypeDef
    deploymentApplicationConfigs: List[DeploymentApplicationConfigOutputTypeDef]
    failureReason: str
    failureCode: DeploymentJobErrorCodeType
    createdAt: datetime
    robotDeploymentSummary: List[RobotDeploymentTypeDef]
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDeploymentJobsResponseTypeDef(TypedDict):
    deploymentJobs: List[DeploymentJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

DeploymentApplicationConfigUnionTypeDef = Union[
    DeploymentApplicationConfigTypeDef, DeploymentApplicationConfigOutputTypeDef
]

class DescribeWorldGenerationJobResponseTypeDef(TypedDict):
    arn: str
    status: WorldGenerationJobStatusType
    createdAt: datetime
    failureCode: WorldGenerationJobErrorCodeType
    failureReason: str
    clientRequestToken: str
    template: str
    worldCount: WorldCountTypeDef
    finishedWorldsSummary: FinishedWorldsSummaryTypeDef
    tags: Dict[str, str]
    worldTags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RobotApplicationConfigOutputTypeDef(TypedDict):
    application: str
    launchConfig: LaunchConfigOutputTypeDef
    applicationVersion: NotRequired[str]
    uploadConfigurations: NotRequired[List[UploadConfigurationTypeDef]]
    useDefaultUploadConfigurations: NotRequired[bool]
    tools: NotRequired[List[ToolTypeDef]]
    useDefaultTools: NotRequired[bool]

class SimulationApplicationConfigOutputTypeDef(TypedDict):
    application: str
    launchConfig: LaunchConfigOutputTypeDef
    applicationVersion: NotRequired[str]
    uploadConfigurations: NotRequired[List[UploadConfigurationTypeDef]]
    worldConfigs: NotRequired[List[WorldConfigTypeDef]]
    useDefaultUploadConfigurations: NotRequired[bool]
    tools: NotRequired[List[ToolTypeDef]]
    useDefaultTools: NotRequired[bool]

class LaunchConfigTypeDef(TypedDict):
    packageName: NotRequired[str]
    launchFile: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]
    portForwardingConfig: NotRequired[PortForwardingConfigUnionTypeDef]
    streamUI: NotRequired[bool]
    command: NotRequired[Sequence[str]]

class CreateDeploymentJobRequestRequestTypeDef(TypedDict):
    clientRequestToken: str
    fleet: str
    deploymentApplicationConfigs: Sequence[DeploymentApplicationConfigUnionTypeDef]
    deploymentConfig: NotRequired[DeploymentConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]

class CreateSimulationJobResponseTypeDef(TypedDict):
    arn: str
    status: SimulationJobStatusType
    lastStartedAt: datetime
    lastUpdatedAt: datetime
    failureBehavior: FailureBehaviorType
    failureCode: SimulationJobErrorCodeType
    clientRequestToken: str
    outputLocation: OutputLocationTypeDef
    loggingConfig: LoggingConfigTypeDef
    maxJobDurationInSeconds: int
    simulationTimeMillis: int
    iamRole: str
    robotApplications: List[RobotApplicationConfigOutputTypeDef]
    simulationApplications: List[SimulationApplicationConfigOutputTypeDef]
    dataSources: List[DataSourceTypeDef]
    tags: Dict[str, str]
    vpcConfig: VPCConfigResponseTypeDef
    compute: ComputeResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSimulationJobResponseTypeDef(TypedDict):
    arn: str
    name: str
    status: SimulationJobStatusType
    lastStartedAt: datetime
    lastUpdatedAt: datetime
    failureBehavior: FailureBehaviorType
    failureCode: SimulationJobErrorCodeType
    failureReason: str
    clientRequestToken: str
    outputLocation: OutputLocationTypeDef
    loggingConfig: LoggingConfigTypeDef
    maxJobDurationInSeconds: int
    simulationTimeMillis: int
    iamRole: str
    robotApplications: List[RobotApplicationConfigOutputTypeDef]
    simulationApplications: List[SimulationApplicationConfigOutputTypeDef]
    dataSources: List[DataSourceTypeDef]
    tags: Dict[str, str]
    vpcConfig: VPCConfigResponseTypeDef
    networkInterface: NetworkInterfaceTypeDef
    compute: ComputeResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SimulationJobRequestOutputTypeDef(TypedDict):
    maxJobDurationInSeconds: int
    outputLocation: NotRequired[OutputLocationTypeDef]
    loggingConfig: NotRequired[LoggingConfigTypeDef]
    iamRole: NotRequired[str]
    failureBehavior: NotRequired[FailureBehaviorType]
    useDefaultApplications: NotRequired[bool]
    robotApplications: NotRequired[List[RobotApplicationConfigOutputTypeDef]]
    simulationApplications: NotRequired[List[SimulationApplicationConfigOutputTypeDef]]
    dataSources: NotRequired[List[DataSourceConfigOutputTypeDef]]
    vpcConfig: NotRequired[VPCConfigOutputTypeDef]
    compute: NotRequired[ComputeTypeDef]
    tags: NotRequired[Dict[str, str]]

class SimulationJobTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[SimulationJobStatusType]
    lastStartedAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    failureBehavior: NotRequired[FailureBehaviorType]
    failureCode: NotRequired[SimulationJobErrorCodeType]
    failureReason: NotRequired[str]
    clientRequestToken: NotRequired[str]
    outputLocation: NotRequired[OutputLocationTypeDef]
    loggingConfig: NotRequired[LoggingConfigTypeDef]
    maxJobDurationInSeconds: NotRequired[int]
    simulationTimeMillis: NotRequired[int]
    iamRole: NotRequired[str]
    robotApplications: NotRequired[List[RobotApplicationConfigOutputTypeDef]]
    simulationApplications: NotRequired[List[SimulationApplicationConfigOutputTypeDef]]
    dataSources: NotRequired[List[DataSourceTypeDef]]
    tags: NotRequired[Dict[str, str]]
    vpcConfig: NotRequired[VPCConfigResponseTypeDef]
    networkInterface: NotRequired[NetworkInterfaceTypeDef]
    compute: NotRequired[ComputeResponseTypeDef]

LaunchConfigUnionTypeDef = Union[LaunchConfigTypeDef, LaunchConfigOutputTypeDef]

class FailedCreateSimulationJobRequestTypeDef(TypedDict):
    request: NotRequired[SimulationJobRequestOutputTypeDef]
    failureReason: NotRequired[str]
    failureCode: NotRequired[SimulationJobErrorCodeType]
    failedAt: NotRequired[datetime]

class BatchDescribeSimulationJobResponseTypeDef(TypedDict):
    jobs: List[SimulationJobTypeDef]
    unprocessedJobs: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class RobotApplicationConfigTypeDef(TypedDict):
    application: str
    launchConfig: LaunchConfigUnionTypeDef
    applicationVersion: NotRequired[str]
    uploadConfigurations: NotRequired[Sequence[UploadConfigurationTypeDef]]
    useDefaultUploadConfigurations: NotRequired[bool]
    tools: NotRequired[Sequence[ToolTypeDef]]
    useDefaultTools: NotRequired[bool]

class SimulationApplicationConfigTypeDef(TypedDict):
    application: str
    launchConfig: LaunchConfigUnionTypeDef
    applicationVersion: NotRequired[str]
    uploadConfigurations: NotRequired[Sequence[UploadConfigurationTypeDef]]
    worldConfigs: NotRequired[Sequence[WorldConfigTypeDef]]
    useDefaultUploadConfigurations: NotRequired[bool]
    tools: NotRequired[Sequence[ToolTypeDef]]
    useDefaultTools: NotRequired[bool]

class DescribeSimulationJobBatchResponseTypeDef(TypedDict):
    arn: str
    status: SimulationJobBatchStatusType
    lastUpdatedAt: datetime
    createdAt: datetime
    clientRequestToken: str
    batchPolicy: BatchPolicyTypeDef
    failureCode: Literal["InternalServiceError"]
    failureReason: str
    failedRequests: List[FailedCreateSimulationJobRequestTypeDef]
    pendingRequests: List[SimulationJobRequestOutputTypeDef]
    createdRequests: List[SimulationJobSummaryTypeDef]
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartSimulationJobBatchResponseTypeDef(TypedDict):
    arn: str
    status: SimulationJobBatchStatusType
    createdAt: datetime
    clientRequestToken: str
    batchPolicy: BatchPolicyTypeDef
    failureCode: Literal["InternalServiceError"]
    failureReason: str
    failedRequests: List[FailedCreateSimulationJobRequestTypeDef]
    pendingRequests: List[SimulationJobRequestOutputTypeDef]
    createdRequests: List[SimulationJobSummaryTypeDef]
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

RobotApplicationConfigUnionTypeDef = Union[
    RobotApplicationConfigTypeDef, RobotApplicationConfigOutputTypeDef
]
SimulationApplicationConfigUnionTypeDef = Union[
    SimulationApplicationConfigTypeDef, SimulationApplicationConfigOutputTypeDef
]

class CreateSimulationJobRequestRequestTypeDef(TypedDict):
    maxJobDurationInSeconds: int
    iamRole: str
    clientRequestToken: NotRequired[str]
    outputLocation: NotRequired[OutputLocationTypeDef]
    loggingConfig: NotRequired[LoggingConfigTypeDef]
    failureBehavior: NotRequired[FailureBehaviorType]
    robotApplications: NotRequired[Sequence[RobotApplicationConfigUnionTypeDef]]
    simulationApplications: NotRequired[Sequence[SimulationApplicationConfigUnionTypeDef]]
    dataSources: NotRequired[Sequence[DataSourceConfigUnionTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    vpcConfig: NotRequired[VPCConfigTypeDef]
    compute: NotRequired[ComputeTypeDef]

class SimulationJobRequestTypeDef(TypedDict):
    maxJobDurationInSeconds: int
    outputLocation: NotRequired[OutputLocationTypeDef]
    loggingConfig: NotRequired[LoggingConfigTypeDef]
    iamRole: NotRequired[str]
    failureBehavior: NotRequired[FailureBehaviorType]
    useDefaultApplications: NotRequired[bool]
    robotApplications: NotRequired[Sequence[RobotApplicationConfigUnionTypeDef]]
    simulationApplications: NotRequired[Sequence[SimulationApplicationConfigUnionTypeDef]]
    dataSources: NotRequired[Sequence[DataSourceConfigUnionTypeDef]]
    vpcConfig: NotRequired[VPCConfigUnionTypeDef]
    compute: NotRequired[ComputeTypeDef]
    tags: NotRequired[Mapping[str, str]]

SimulationJobRequestUnionTypeDef = Union[
    SimulationJobRequestTypeDef, SimulationJobRequestOutputTypeDef
]

class StartSimulationJobBatchRequestRequestTypeDef(TypedDict):
    createSimulationJobRequests: Sequence[SimulationJobRequestUnionTypeDef]
    clientRequestToken: NotRequired[str]
    batchPolicy: NotRequired[BatchPolicyTypeDef]
    tags: NotRequired[Mapping[str, str]]
