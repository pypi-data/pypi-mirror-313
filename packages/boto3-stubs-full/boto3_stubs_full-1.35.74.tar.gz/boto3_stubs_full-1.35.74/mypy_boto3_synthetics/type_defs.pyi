"""
Type annotations for synthetics service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_synthetics/type_defs/)

Usage::

    ```python
    from mypy_boto3_synthetics.type_defs import S3EncryptionConfigTypeDef

    data: S3EncryptionConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    CanaryRunStateReasonCodeType,
    CanaryRunStateType,
    CanaryStateReasonCodeType,
    CanaryStateType,
    EncryptionModeType,
    ProvisionedResourceCleanupSettingType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ArtifactConfigInputTypeDef",
    "ArtifactConfigOutputTypeDef",
    "AssociateResourceRequestRequestTypeDef",
    "BaseScreenshotOutputTypeDef",
    "BaseScreenshotTypeDef",
    "BaseScreenshotUnionTypeDef",
    "BlobTypeDef",
    "CanaryCodeInputTypeDef",
    "CanaryCodeOutputTypeDef",
    "CanaryLastRunTypeDef",
    "CanaryRunConfigInputTypeDef",
    "CanaryRunConfigOutputTypeDef",
    "CanaryRunStatusTypeDef",
    "CanaryRunTimelineTypeDef",
    "CanaryRunTypeDef",
    "CanaryScheduleInputTypeDef",
    "CanaryScheduleOutputTypeDef",
    "CanaryStatusTypeDef",
    "CanaryTimelineTypeDef",
    "CanaryTypeDef",
    "CreateCanaryRequestRequestTypeDef",
    "CreateCanaryResponseTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "DeleteCanaryRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DescribeCanariesLastRunRequestRequestTypeDef",
    "DescribeCanariesLastRunResponseTypeDef",
    "DescribeCanariesRequestRequestTypeDef",
    "DescribeCanariesResponseTypeDef",
    "DescribeRuntimeVersionsRequestRequestTypeDef",
    "DescribeRuntimeVersionsResponseTypeDef",
    "DisassociateResourceRequestRequestTypeDef",
    "GetCanaryRequestRequestTypeDef",
    "GetCanaryResponseTypeDef",
    "GetCanaryRunsRequestRequestTypeDef",
    "GetCanaryRunsResponseTypeDef",
    "GetGroupRequestRequestTypeDef",
    "GetGroupResponseTypeDef",
    "GroupSummaryTypeDef",
    "GroupTypeDef",
    "ListAssociatedGroupsRequestRequestTypeDef",
    "ListAssociatedGroupsResponseTypeDef",
    "ListGroupResourcesRequestRequestTypeDef",
    "ListGroupResourcesResponseTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RuntimeVersionTypeDef",
    "S3EncryptionConfigTypeDef",
    "StartCanaryRequestRequestTypeDef",
    "StopCanaryRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCanaryRequestRequestTypeDef",
    "VisualReferenceInputTypeDef",
    "VisualReferenceOutputTypeDef",
    "VpcConfigInputTypeDef",
    "VpcConfigOutputTypeDef",
)

class S3EncryptionConfigTypeDef(TypedDict):
    EncryptionMode: NotRequired[EncryptionModeType]
    KmsKeyArn: NotRequired[str]

class AssociateResourceRequestRequestTypeDef(TypedDict):
    GroupIdentifier: str
    ResourceArn: str

class BaseScreenshotOutputTypeDef(TypedDict):
    ScreenshotName: str
    IgnoreCoordinates: NotRequired[List[str]]

class BaseScreenshotTypeDef(TypedDict):
    ScreenshotName: str
    IgnoreCoordinates: NotRequired[Sequence[str]]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CanaryCodeOutputTypeDef(TypedDict):
    SourceLocationArn: NotRequired[str]
    Handler: NotRequired[str]

class CanaryRunConfigInputTypeDef(TypedDict):
    TimeoutInSeconds: NotRequired[int]
    MemoryInMB: NotRequired[int]
    ActiveTracing: NotRequired[bool]
    EnvironmentVariables: NotRequired[Mapping[str, str]]

class CanaryRunConfigOutputTypeDef(TypedDict):
    TimeoutInSeconds: NotRequired[int]
    MemoryInMB: NotRequired[int]
    ActiveTracing: NotRequired[bool]

class CanaryRunStatusTypeDef(TypedDict):
    State: NotRequired[CanaryRunStateType]
    StateReason: NotRequired[str]
    StateReasonCode: NotRequired[CanaryRunStateReasonCodeType]

class CanaryRunTimelineTypeDef(TypedDict):
    Started: NotRequired[datetime]
    Completed: NotRequired[datetime]

class CanaryScheduleInputTypeDef(TypedDict):
    Expression: str
    DurationInSeconds: NotRequired[int]

class CanaryScheduleOutputTypeDef(TypedDict):
    Expression: NotRequired[str]
    DurationInSeconds: NotRequired[int]

class CanaryStatusTypeDef(TypedDict):
    State: NotRequired[CanaryStateType]
    StateReason: NotRequired[str]
    StateReasonCode: NotRequired[CanaryStateReasonCodeType]

class CanaryTimelineTypeDef(TypedDict):
    Created: NotRequired[datetime]
    LastModified: NotRequired[datetime]
    LastStarted: NotRequired[datetime]
    LastStopped: NotRequired[datetime]

class VpcConfigOutputTypeDef(TypedDict):
    VpcId: NotRequired[str]
    SubnetIds: NotRequired[List[str]]
    SecurityGroupIds: NotRequired[List[str]]

class VpcConfigInputTypeDef(TypedDict):
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateGroupRequestRequestTypeDef(TypedDict):
    Name: str
    Tags: NotRequired[Mapping[str, str]]

class GroupTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Arn: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    CreatedTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class DeleteCanaryRequestRequestTypeDef(TypedDict):
    Name: str
    DeleteLambda: NotRequired[bool]

class DeleteGroupRequestRequestTypeDef(TypedDict):
    GroupIdentifier: str

class DescribeCanariesLastRunRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Names: NotRequired[Sequence[str]]

class DescribeCanariesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Names: NotRequired[Sequence[str]]

class DescribeRuntimeVersionsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class RuntimeVersionTypeDef(TypedDict):
    VersionName: NotRequired[str]
    Description: NotRequired[str]
    ReleaseDate: NotRequired[datetime]
    DeprecationDate: NotRequired[datetime]

class DisassociateResourceRequestRequestTypeDef(TypedDict):
    GroupIdentifier: str
    ResourceArn: str

class GetCanaryRequestRequestTypeDef(TypedDict):
    Name: str

class GetCanaryRunsRequestRequestTypeDef(TypedDict):
    Name: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetGroupRequestRequestTypeDef(TypedDict):
    GroupIdentifier: str

class GroupSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Arn: NotRequired[str]

class ListAssociatedGroupsRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListGroupResourcesRequestRequestTypeDef(TypedDict):
    GroupIdentifier: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListGroupsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class StartCanaryRequestRequestTypeDef(TypedDict):
    Name: str

class StopCanaryRequestRequestTypeDef(TypedDict):
    Name: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class ArtifactConfigInputTypeDef(TypedDict):
    S3Encryption: NotRequired[S3EncryptionConfigTypeDef]

class ArtifactConfigOutputTypeDef(TypedDict):
    S3Encryption: NotRequired[S3EncryptionConfigTypeDef]

class VisualReferenceOutputTypeDef(TypedDict):
    BaseScreenshots: NotRequired[List[BaseScreenshotOutputTypeDef]]
    BaseCanaryRunId: NotRequired[str]

BaseScreenshotUnionTypeDef = Union[BaseScreenshotTypeDef, BaseScreenshotOutputTypeDef]

class CanaryCodeInputTypeDef(TypedDict):
    Handler: str
    S3Bucket: NotRequired[str]
    S3Key: NotRequired[str]
    S3Version: NotRequired[str]
    ZipFile: NotRequired[BlobTypeDef]

class CanaryRunTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[CanaryRunStatusTypeDef]
    Timeline: NotRequired[CanaryRunTimelineTypeDef]
    ArtifactS3Location: NotRequired[str]

class ListGroupResourcesResponseTypeDef(TypedDict):
    Resources: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRuntimeVersionsResponseTypeDef(TypedDict):
    RuntimeVersions: List[RuntimeVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAssociatedGroupsResponseTypeDef(TypedDict):
    Groups: List[GroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListGroupsResponseTypeDef(TypedDict):
    Groups: List[GroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CanaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Code: NotRequired[CanaryCodeOutputTypeDef]
    ExecutionRoleArn: NotRequired[str]
    Schedule: NotRequired[CanaryScheduleOutputTypeDef]
    RunConfig: NotRequired[CanaryRunConfigOutputTypeDef]
    SuccessRetentionPeriodInDays: NotRequired[int]
    FailureRetentionPeriodInDays: NotRequired[int]
    Status: NotRequired[CanaryStatusTypeDef]
    Timeline: NotRequired[CanaryTimelineTypeDef]
    ArtifactS3Location: NotRequired[str]
    EngineArn: NotRequired[str]
    RuntimeVersion: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    VisualReference: NotRequired[VisualReferenceOutputTypeDef]
    ProvisionedResourceCleanup: NotRequired[ProvisionedResourceCleanupSettingType]
    Tags: NotRequired[Dict[str, str]]
    ArtifactConfig: NotRequired[ArtifactConfigOutputTypeDef]

class VisualReferenceInputTypeDef(TypedDict):
    BaseCanaryRunId: str
    BaseScreenshots: NotRequired[Sequence[BaseScreenshotUnionTypeDef]]

class CreateCanaryRequestRequestTypeDef(TypedDict):
    Name: str
    Code: CanaryCodeInputTypeDef
    ArtifactS3Location: str
    ExecutionRoleArn: str
    Schedule: CanaryScheduleInputTypeDef
    RuntimeVersion: str
    RunConfig: NotRequired[CanaryRunConfigInputTypeDef]
    SuccessRetentionPeriodInDays: NotRequired[int]
    FailureRetentionPeriodInDays: NotRequired[int]
    VpcConfig: NotRequired[VpcConfigInputTypeDef]
    ResourcesToReplicateTags: NotRequired[Sequence[Literal["lambda-function"]]]
    ProvisionedResourceCleanup: NotRequired[ProvisionedResourceCleanupSettingType]
    Tags: NotRequired[Mapping[str, str]]
    ArtifactConfig: NotRequired[ArtifactConfigInputTypeDef]

class CanaryLastRunTypeDef(TypedDict):
    CanaryName: NotRequired[str]
    LastRun: NotRequired[CanaryRunTypeDef]

class GetCanaryRunsResponseTypeDef(TypedDict):
    CanaryRuns: List[CanaryRunTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateCanaryResponseTypeDef(TypedDict):
    Canary: CanaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCanariesResponseTypeDef(TypedDict):
    Canaries: List[CanaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetCanaryResponseTypeDef(TypedDict):
    Canary: CanaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCanaryRequestRequestTypeDef(TypedDict):
    Name: str
    Code: NotRequired[CanaryCodeInputTypeDef]
    ExecutionRoleArn: NotRequired[str]
    RuntimeVersion: NotRequired[str]
    Schedule: NotRequired[CanaryScheduleInputTypeDef]
    RunConfig: NotRequired[CanaryRunConfigInputTypeDef]
    SuccessRetentionPeriodInDays: NotRequired[int]
    FailureRetentionPeriodInDays: NotRequired[int]
    VpcConfig: NotRequired[VpcConfigInputTypeDef]
    VisualReference: NotRequired[VisualReferenceInputTypeDef]
    ArtifactS3Location: NotRequired[str]
    ArtifactConfig: NotRequired[ArtifactConfigInputTypeDef]
    ProvisionedResourceCleanup: NotRequired[ProvisionedResourceCleanupSettingType]

class DescribeCanariesLastRunResponseTypeDef(TypedDict):
    CanariesLastRun: List[CanaryLastRunTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
