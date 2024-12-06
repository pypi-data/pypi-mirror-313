"""
Type annotations for osis service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_osis/type_defs/)

Usage::

    ```python
    from mypy_boto3_osis.type_defs import BufferOptionsTypeDef

    data: BufferOptionsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ChangeProgressStageStatusesType,
    ChangeProgressStatusesType,
    PipelineStatusType,
    VpcEndpointManagementType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "BufferOptionsTypeDef",
    "ChangeProgressStageTypeDef",
    "ChangeProgressStatusTypeDef",
    "CloudWatchLogDestinationTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "CreatePipelineResponseTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "EncryptionAtRestOptionsTypeDef",
    "GetPipelineBlueprintRequestRequestTypeDef",
    "GetPipelineBlueprintResponseTypeDef",
    "GetPipelineChangeProgressRequestRequestTypeDef",
    "GetPipelineChangeProgressResponseTypeDef",
    "GetPipelineRequestRequestTypeDef",
    "GetPipelineResponseTypeDef",
    "ListPipelineBlueprintsResponseTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogPublishingOptionsTypeDef",
    "PipelineBlueprintSummaryTypeDef",
    "PipelineBlueprintTypeDef",
    "PipelineDestinationTypeDef",
    "PipelineStatusReasonTypeDef",
    "PipelineSummaryTypeDef",
    "PipelineTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceVpcEndpointTypeDef",
    "StartPipelineRequestRequestTypeDef",
    "StartPipelineResponseTypeDef",
    "StopPipelineRequestRequestTypeDef",
    "StopPipelineResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "UpdatePipelineResponseTypeDef",
    "ValidatePipelineRequestRequestTypeDef",
    "ValidatePipelineResponseTypeDef",
    "ValidationMessageTypeDef",
    "VpcAttachmentOptionsTypeDef",
    "VpcEndpointTypeDef",
    "VpcOptionsOutputTypeDef",
    "VpcOptionsTypeDef",
)

class BufferOptionsTypeDef(TypedDict):
    PersistentBufferEnabled: bool

class ChangeProgressStageTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[ChangeProgressStageStatusesType]
    Description: NotRequired[str]
    LastUpdatedAt: NotRequired[datetime]

class CloudWatchLogDestinationTypeDef(TypedDict):
    LogGroup: str

class EncryptionAtRestOptionsTypeDef(TypedDict):
    KmsKeyArn: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeletePipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str

class GetPipelineBlueprintRequestRequestTypeDef(TypedDict):
    BlueprintName: str
    Format: NotRequired[str]

class PipelineBlueprintTypeDef(TypedDict):
    BlueprintName: NotRequired[str]
    PipelineConfigurationBody: NotRequired[str]
    DisplayName: NotRequired[str]
    DisplayDescription: NotRequired[str]
    Service: NotRequired[str]
    UseCase: NotRequired[str]

class GetPipelineChangeProgressRequestRequestTypeDef(TypedDict):
    PipelineName: str

class GetPipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str

class PipelineBlueprintSummaryTypeDef(TypedDict):
    BlueprintName: NotRequired[str]
    DisplayName: NotRequired[str]
    DisplayDescription: NotRequired[str]
    Service: NotRequired[str]
    UseCase: NotRequired[str]

class ListPipelinesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    Arn: str

PipelineDestinationTypeDef = TypedDict(
    "PipelineDestinationTypeDef",
    {
        "ServiceName": NotRequired[str],
        "Endpoint": NotRequired[str],
    },
)

class PipelineStatusReasonTypeDef(TypedDict):
    Description: NotRequired[str]

ServiceVpcEndpointTypeDef = TypedDict(
    "ServiceVpcEndpointTypeDef",
    {
        "ServiceName": NotRequired[Literal["OPENSEARCH_SERVERLESS"]],
        "VpcEndpointId": NotRequired[str],
    },
)

class StartPipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str

class StopPipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    Arn: str
    TagKeys: Sequence[str]

class ValidatePipelineRequestRequestTypeDef(TypedDict):
    PipelineConfigurationBody: str

class ValidationMessageTypeDef(TypedDict):
    Message: NotRequired[str]

class VpcAttachmentOptionsTypeDef(TypedDict):
    AttachToVpc: bool
    CidrBlock: NotRequired[str]

class ChangeProgressStatusTypeDef(TypedDict):
    StartTime: NotRequired[datetime]
    Status: NotRequired[ChangeProgressStatusesType]
    TotalNumberOfStages: NotRequired[int]
    ChangeProgressStages: NotRequired[List[ChangeProgressStageTypeDef]]

class LogPublishingOptionsTypeDef(TypedDict):
    IsLoggingEnabled: NotRequired[bool]
    CloudWatchLogDestination: NotRequired[CloudWatchLogDestinationTypeDef]

class TagResourceRequestRequestTypeDef(TypedDict):
    Arn: str
    Tags: Sequence[TagTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPipelineBlueprintResponseTypeDef(TypedDict):
    Blueprint: PipelineBlueprintTypeDef
    Format: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListPipelineBlueprintsResponseTypeDef(TypedDict):
    Blueprints: List[PipelineBlueprintSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PipelineSummaryTypeDef(TypedDict):
    Status: NotRequired[PipelineStatusType]
    StatusReason: NotRequired[PipelineStatusReasonTypeDef]
    PipelineName: NotRequired[str]
    PipelineArn: NotRequired[str]
    MinUnits: NotRequired[int]
    MaxUnits: NotRequired[int]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    Destinations: NotRequired[List[PipelineDestinationTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]

class ValidatePipelineResponseTypeDef(TypedDict):
    isValid: bool
    Errors: List[ValidationMessageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class VpcOptionsOutputTypeDef(TypedDict):
    SubnetIds: List[str]
    SecurityGroupIds: NotRequired[List[str]]
    VpcAttachmentOptions: NotRequired[VpcAttachmentOptionsTypeDef]
    VpcEndpointManagement: NotRequired[VpcEndpointManagementType]

class VpcOptionsTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    VpcAttachmentOptions: NotRequired[VpcAttachmentOptionsTypeDef]
    VpcEndpointManagement: NotRequired[VpcEndpointManagementType]

class GetPipelineChangeProgressResponseTypeDef(TypedDict):
    ChangeProgressStatuses: List[ChangeProgressStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str
    MinUnits: NotRequired[int]
    MaxUnits: NotRequired[int]
    PipelineConfigurationBody: NotRequired[str]
    LogPublishingOptions: NotRequired[LogPublishingOptionsTypeDef]
    BufferOptions: NotRequired[BufferOptionsTypeDef]
    EncryptionAtRestOptions: NotRequired[EncryptionAtRestOptionsTypeDef]

class ListPipelinesResponseTypeDef(TypedDict):
    Pipelines: List[PipelineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class VpcEndpointTypeDef(TypedDict):
    VpcEndpointId: NotRequired[str]
    VpcId: NotRequired[str]
    VpcOptions: NotRequired[VpcOptionsOutputTypeDef]

class CreatePipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str
    MinUnits: int
    MaxUnits: int
    PipelineConfigurationBody: str
    LogPublishingOptions: NotRequired[LogPublishingOptionsTypeDef]
    VpcOptions: NotRequired[VpcOptionsTypeDef]
    BufferOptions: NotRequired[BufferOptionsTypeDef]
    EncryptionAtRestOptions: NotRequired[EncryptionAtRestOptionsTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class PipelineTypeDef(TypedDict):
    PipelineName: NotRequired[str]
    PipelineArn: NotRequired[str]
    MinUnits: NotRequired[int]
    MaxUnits: NotRequired[int]
    Status: NotRequired[PipelineStatusType]
    StatusReason: NotRequired[PipelineStatusReasonTypeDef]
    PipelineConfigurationBody: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    IngestEndpointUrls: NotRequired[List[str]]
    LogPublishingOptions: NotRequired[LogPublishingOptionsTypeDef]
    VpcEndpoints: NotRequired[List[VpcEndpointTypeDef]]
    BufferOptions: NotRequired[BufferOptionsTypeDef]
    EncryptionAtRestOptions: NotRequired[EncryptionAtRestOptionsTypeDef]
    VpcEndpointService: NotRequired[str]
    ServiceVpcEndpoints: NotRequired[List[ServiceVpcEndpointTypeDef]]
    Destinations: NotRequired[List[PipelineDestinationTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]

class CreatePipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartPipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopPipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePipelineResponseTypeDef(TypedDict):
    Pipeline: PipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
