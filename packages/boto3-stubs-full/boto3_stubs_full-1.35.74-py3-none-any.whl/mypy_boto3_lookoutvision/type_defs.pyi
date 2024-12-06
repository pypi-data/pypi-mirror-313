"""
Type annotations for lookoutvision service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/type_defs/)

Usage::

    ```python
    from mypy_boto3_lookoutvision.type_defs import PixelAnomalyTypeDef

    data: PixelAnomalyTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    DatasetStatusType,
    ModelHostingStatusType,
    ModelPackagingJobStatusType,
    ModelStatusType,
    TargetPlatformArchType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AnomalyTypeDef",
    "BlobTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateModelRequestRequestTypeDef",
    "CreateModelResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "DatasetDescriptionTypeDef",
    "DatasetGroundTruthManifestTypeDef",
    "DatasetImageStatsTypeDef",
    "DatasetMetadataTypeDef",
    "DatasetSourceTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteModelRequestRequestTypeDef",
    "DeleteModelResponseTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteProjectResponseTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeModelPackagingJobRequestRequestTypeDef",
    "DescribeModelPackagingJobResponseTypeDef",
    "DescribeModelRequestRequestTypeDef",
    "DescribeModelResponseTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DescribeProjectResponseTypeDef",
    "DetectAnomaliesRequestRequestTypeDef",
    "DetectAnomaliesResponseTypeDef",
    "DetectAnomalyResultTypeDef",
    "GreengrassConfigurationOutputTypeDef",
    "GreengrassConfigurationTypeDef",
    "GreengrassConfigurationUnionTypeDef",
    "GreengrassOutputDetailsTypeDef",
    "ImageSourceTypeDef",
    "InputS3ObjectTypeDef",
    "ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    "ListDatasetEntriesRequestRequestTypeDef",
    "ListDatasetEntriesResponseTypeDef",
    "ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef",
    "ListModelPackagingJobsRequestRequestTypeDef",
    "ListModelPackagingJobsResponseTypeDef",
    "ListModelsRequestListModelsPaginateTypeDef",
    "ListModelsRequestRequestTypeDef",
    "ListModelsResponseTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModelDescriptionTypeDef",
    "ModelMetadataTypeDef",
    "ModelPackagingConfigurationOutputTypeDef",
    "ModelPackagingConfigurationTypeDef",
    "ModelPackagingDescriptionTypeDef",
    "ModelPackagingJobMetadataTypeDef",
    "ModelPackagingOutputDetailsTypeDef",
    "ModelPerformanceTypeDef",
    "OutputConfigTypeDef",
    "OutputS3ObjectTypeDef",
    "PaginatorConfigTypeDef",
    "PixelAnomalyTypeDef",
    "ProjectDescriptionTypeDef",
    "ProjectMetadataTypeDef",
    "ResponseMetadataTypeDef",
    "S3LocationTypeDef",
    "StartModelPackagingJobRequestRequestTypeDef",
    "StartModelPackagingJobResponseTypeDef",
    "StartModelRequestRequestTypeDef",
    "StartModelResponseTypeDef",
    "StopModelRequestRequestTypeDef",
    "StopModelResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetPlatformTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatasetEntriesRequestRequestTypeDef",
    "UpdateDatasetEntriesResponseTypeDef",
)

class PixelAnomalyTypeDef(TypedDict):
    TotalPercentageArea: NotRequired[float]
    Color: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class DatasetMetadataTypeDef(TypedDict):
    DatasetType: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]
    Status: NotRequired[DatasetStatusType]
    StatusMessage: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CreateProjectRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ClientToken: NotRequired[str]

class ProjectMetadataTypeDef(TypedDict):
    ProjectArn: NotRequired[str]
    ProjectName: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]

class DatasetImageStatsTypeDef(TypedDict):
    Total: NotRequired[int]
    Labeled: NotRequired[int]
    Normal: NotRequired[int]
    Anomaly: NotRequired[int]

class InputS3ObjectTypeDef(TypedDict):
    Bucket: str
    Key: str
    VersionId: NotRequired[str]

class DeleteDatasetRequestRequestTypeDef(TypedDict):
    ProjectName: str
    DatasetType: str
    ClientToken: NotRequired[str]

class DeleteModelRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ModelVersion: str
    ClientToken: NotRequired[str]

class DeleteProjectRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ClientToken: NotRequired[str]

class DescribeDatasetRequestRequestTypeDef(TypedDict):
    ProjectName: str
    DatasetType: str

class DescribeModelPackagingJobRequestRequestTypeDef(TypedDict):
    ProjectName: str
    JobName: str

class DescribeModelRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ModelVersion: str

class DescribeProjectRequestRequestTypeDef(TypedDict):
    ProjectName: str

ImageSourceTypeDef = TypedDict(
    "ImageSourceTypeDef",
    {
        "Type": NotRequired[str],
    },
)

class S3LocationTypeDef(TypedDict):
    Bucket: str
    Prefix: NotRequired[str]

class TargetPlatformTypeDef(TypedDict):
    Os: Literal["LINUX"]
    Arch: TargetPlatformArchType
    Accelerator: NotRequired[Literal["NVIDIA"]]

class GreengrassOutputDetailsTypeDef(TypedDict):
    ComponentVersionArn: NotRequired[str]
    ComponentName: NotRequired[str]
    ComponentVersion: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ListModelPackagingJobsRequestRequestTypeDef(TypedDict):
    ProjectName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ModelPackagingJobMetadataTypeDef(TypedDict):
    JobName: NotRequired[str]
    ProjectName: NotRequired[str]
    ModelVersion: NotRequired[str]
    ModelPackagingJobDescription: NotRequired[str]
    ModelPackagingMethod: NotRequired[str]
    Status: NotRequired[ModelPackagingJobStatusType]
    StatusMessage: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]

class ListModelsRequestRequestTypeDef(TypedDict):
    ProjectName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListProjectsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ModelPerformanceTypeDef(TypedDict):
    F1Score: NotRequired[float]
    Recall: NotRequired[float]
    Precision: NotRequired[float]

class OutputS3ObjectTypeDef(TypedDict):
    Bucket: str
    Key: str

class StartModelRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ModelVersion: str
    MinInferenceUnits: int
    ClientToken: NotRequired[str]
    MaxInferenceUnits: NotRequired[int]

class StopModelRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ModelVersion: str
    ClientToken: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class AnomalyTypeDef(TypedDict):
    Name: NotRequired[str]
    PixelAnomaly: NotRequired[PixelAnomalyTypeDef]

class DetectAnomaliesRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ModelVersion: str
    Body: BlobTypeDef
    ContentType: str

class UpdateDatasetEntriesRequestRequestTypeDef(TypedDict):
    ProjectName: str
    DatasetType: str
    Changes: BlobTypeDef
    ClientToken: NotRequired[str]

class ProjectDescriptionTypeDef(TypedDict):
    ProjectArn: NotRequired[str]
    ProjectName: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]
    Datasets: NotRequired[List[DatasetMetadataTypeDef]]

class CreateDatasetResponseTypeDef(TypedDict):
    DatasetMetadata: DatasetMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteModelResponseTypeDef(TypedDict):
    ModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteProjectResponseTypeDef(TypedDict):
    ProjectArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListDatasetEntriesResponseTypeDef(TypedDict):
    DatasetEntries: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartModelPackagingJobResponseTypeDef(TypedDict):
    JobName: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartModelResponseTypeDef(TypedDict):
    Status: ModelHostingStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopModelResponseTypeDef(TypedDict):
    Status: ModelHostingStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDatasetEntriesResponseTypeDef(TypedDict):
    Status: DatasetStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class CreateProjectResponseTypeDef(TypedDict):
    ProjectMetadata: ProjectMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListProjectsResponseTypeDef(TypedDict):
    Projects: List[ProjectMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DatasetDescriptionTypeDef(TypedDict):
    ProjectName: NotRequired[str]
    DatasetType: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]
    Status: NotRequired[DatasetStatusType]
    StatusMessage: NotRequired[str]
    ImageStats: NotRequired[DatasetImageStatsTypeDef]

class DatasetGroundTruthManifestTypeDef(TypedDict):
    S3Object: NotRequired[InputS3ObjectTypeDef]

class OutputConfigTypeDef(TypedDict):
    S3Location: S3LocationTypeDef

class GreengrassConfigurationOutputTypeDef(TypedDict):
    S3OutputLocation: S3LocationTypeDef
    ComponentName: str
    CompilerOptions: NotRequired[str]
    TargetDevice: NotRequired[Literal["jetson_xavier"]]
    TargetPlatform: NotRequired[TargetPlatformTypeDef]
    ComponentVersion: NotRequired[str]
    ComponentDescription: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]

class GreengrassConfigurationTypeDef(TypedDict):
    S3OutputLocation: S3LocationTypeDef
    ComponentName: str
    CompilerOptions: NotRequired[str]
    TargetDevice: NotRequired[Literal["jetson_xavier"]]
    TargetPlatform: NotRequired[TargetPlatformTypeDef]
    ComponentVersion: NotRequired[str]
    ComponentDescription: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ModelPackagingOutputDetailsTypeDef(TypedDict):
    Greengrass: NotRequired[GreengrassOutputDetailsTypeDef]

class ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef(TypedDict):
    ProjectName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListModelsRequestListModelsPaginateTypeDef(TypedDict):
    ProjectName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsRequestListProjectsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef(TypedDict):
    ProjectName: str
    DatasetType: str
    Labeled: NotRequired[bool]
    AnomalyClass: NotRequired[str]
    BeforeCreationDate: NotRequired[TimestampTypeDef]
    AfterCreationDate: NotRequired[TimestampTypeDef]
    SourceRefContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDatasetEntriesRequestRequestTypeDef(TypedDict):
    ProjectName: str
    DatasetType: str
    Labeled: NotRequired[bool]
    AnomalyClass: NotRequired[str]
    BeforeCreationDate: NotRequired[TimestampTypeDef]
    AfterCreationDate: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SourceRefContains: NotRequired[str]

class ListModelPackagingJobsResponseTypeDef(TypedDict):
    ModelPackagingJobs: List[ModelPackagingJobMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ModelMetadataTypeDef(TypedDict):
    CreationTimestamp: NotRequired[datetime]
    ModelVersion: NotRequired[str]
    ModelArn: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[ModelStatusType]
    StatusMessage: NotRequired[str]
    Performance: NotRequired[ModelPerformanceTypeDef]

class DetectAnomalyResultTypeDef(TypedDict):
    Source: NotRequired[ImageSourceTypeDef]
    IsAnomalous: NotRequired[bool]
    Confidence: NotRequired[float]
    Anomalies: NotRequired[List[AnomalyTypeDef]]
    AnomalyMask: NotRequired[bytes]

class DescribeProjectResponseTypeDef(TypedDict):
    ProjectDescription: ProjectDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDatasetResponseTypeDef(TypedDict):
    DatasetDescription: DatasetDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DatasetSourceTypeDef(TypedDict):
    GroundTruthManifest: NotRequired[DatasetGroundTruthManifestTypeDef]

class CreateModelRequestRequestTypeDef(TypedDict):
    ProjectName: str
    OutputConfig: OutputConfigTypeDef
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ModelDescriptionTypeDef(TypedDict):
    ModelVersion: NotRequired[str]
    ModelArn: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]
    Description: NotRequired[str]
    Status: NotRequired[ModelStatusType]
    StatusMessage: NotRequired[str]
    Performance: NotRequired[ModelPerformanceTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    EvaluationManifest: NotRequired[OutputS3ObjectTypeDef]
    EvaluationResult: NotRequired[OutputS3ObjectTypeDef]
    EvaluationEndTimestamp: NotRequired[datetime]
    KmsKeyId: NotRequired[str]
    MinInferenceUnits: NotRequired[int]
    MaxInferenceUnits: NotRequired[int]

class ModelPackagingConfigurationOutputTypeDef(TypedDict):
    Greengrass: GreengrassConfigurationOutputTypeDef

GreengrassConfigurationUnionTypeDef = Union[
    GreengrassConfigurationTypeDef, GreengrassConfigurationOutputTypeDef
]

class CreateModelResponseTypeDef(TypedDict):
    ModelMetadata: ModelMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListModelsResponseTypeDef(TypedDict):
    Models: List[ModelMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DetectAnomaliesResponseTypeDef(TypedDict):
    DetectAnomalyResult: DetectAnomalyResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDatasetRequestRequestTypeDef(TypedDict):
    ProjectName: str
    DatasetType: str
    DatasetSource: NotRequired[DatasetSourceTypeDef]
    ClientToken: NotRequired[str]

class DescribeModelResponseTypeDef(TypedDict):
    ModelDescription: ModelDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ModelPackagingDescriptionTypeDef(TypedDict):
    JobName: NotRequired[str]
    ProjectName: NotRequired[str]
    ModelVersion: NotRequired[str]
    ModelPackagingConfiguration: NotRequired[ModelPackagingConfigurationOutputTypeDef]
    ModelPackagingJobDescription: NotRequired[str]
    ModelPackagingMethod: NotRequired[str]
    ModelPackagingOutputDetails: NotRequired[ModelPackagingOutputDetailsTypeDef]
    Status: NotRequired[ModelPackagingJobStatusType]
    StatusMessage: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]

class ModelPackagingConfigurationTypeDef(TypedDict):
    Greengrass: GreengrassConfigurationUnionTypeDef

class DescribeModelPackagingJobResponseTypeDef(TypedDict):
    ModelPackagingDescription: ModelPackagingDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartModelPackagingJobRequestRequestTypeDef(TypedDict):
    ProjectName: str
    ModelVersion: str
    Configuration: ModelPackagingConfigurationTypeDef
    JobName: NotRequired[str]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
