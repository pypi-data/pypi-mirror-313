"""
Type annotations for connectcampaigns service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/type_defs/)

Usage::

    ```python
    from mypy_boto3_connectcampaigns.type_defs import AgentlessDialerConfigTypeDef

    data: AgentlessDialerConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    CampaignStateType,
    FailureCodeType,
    GetCampaignStateBatchFailureCodeType,
    InstanceOnboardingJobFailureCodeType,
    InstanceOnboardingJobStatusCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AgentlessDialerConfigTypeDef",
    "AnswerMachineDetectionConfigTypeDef",
    "CampaignFiltersTypeDef",
    "CampaignSummaryTypeDef",
    "CampaignTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "CreateCampaignResponseTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteConnectInstanceConfigRequestRequestTypeDef",
    "DeleteInstanceOnboardingJobRequestRequestTypeDef",
    "DescribeCampaignRequestRequestTypeDef",
    "DescribeCampaignResponseTypeDef",
    "DialRequestTypeDef",
    "DialerConfigTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionConfigTypeDef",
    "FailedCampaignStateResponseTypeDef",
    "FailedRequestTypeDef",
    "GetCampaignStateBatchRequestRequestTypeDef",
    "GetCampaignStateBatchResponseTypeDef",
    "GetCampaignStateRequestRequestTypeDef",
    "GetCampaignStateResponseTypeDef",
    "GetConnectInstanceConfigRequestRequestTypeDef",
    "GetConnectInstanceConfigResponseTypeDef",
    "GetInstanceOnboardingJobStatusRequestRequestTypeDef",
    "GetInstanceOnboardingJobStatusResponseTypeDef",
    "InstanceConfigTypeDef",
    "InstanceIdFilterTypeDef",
    "InstanceOnboardingJobStatusTypeDef",
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    "ListCampaignsRequestRequestTypeDef",
    "ListCampaignsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OutboundCallConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PauseCampaignRequestRequestTypeDef",
    "PredictiveDialerConfigTypeDef",
    "ProgressiveDialerConfigTypeDef",
    "PutDialRequestBatchRequestRequestTypeDef",
    "PutDialRequestBatchResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeCampaignRequestRequestTypeDef",
    "StartCampaignRequestRequestTypeDef",
    "StartInstanceOnboardingJobRequestRequestTypeDef",
    "StartInstanceOnboardingJobResponseTypeDef",
    "StopCampaignRequestRequestTypeDef",
    "SuccessfulCampaignStateResponseTypeDef",
    "SuccessfulRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCampaignDialerConfigRequestRequestTypeDef",
    "UpdateCampaignNameRequestRequestTypeDef",
    "UpdateCampaignOutboundCallConfigRequestRequestTypeDef",
)

class AgentlessDialerConfigTypeDef(TypedDict):
    dialingCapacity: NotRequired[float]

class AnswerMachineDetectionConfigTypeDef(TypedDict):
    enableAnswerMachineDetection: bool
    awaitAnswerMachinePrompt: NotRequired[bool]

InstanceIdFilterTypeDef = TypedDict(
    "InstanceIdFilterTypeDef",
    {
        "value": str,
        "operator": Literal["Eq"],
    },
)
CampaignSummaryTypeDef = TypedDict(
    "CampaignSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "connectInstanceId": str,
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

DeleteCampaignRequestRequestTypeDef = TypedDict(
    "DeleteCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DeleteConnectInstanceConfigRequestRequestTypeDef(TypedDict):
    connectInstanceId: str

class DeleteInstanceOnboardingJobRequestRequestTypeDef(TypedDict):
    connectInstanceId: str

DescribeCampaignRequestRequestTypeDef = TypedDict(
    "DescribeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)
TimestampTypeDef = Union[datetime, str]

class PredictiveDialerConfigTypeDef(TypedDict):
    bandwidthAllocation: float
    dialingCapacity: NotRequired[float]

class ProgressiveDialerConfigTypeDef(TypedDict):
    bandwidthAllocation: float
    dialingCapacity: NotRequired[float]

class EncryptionConfigTypeDef(TypedDict):
    enabled: bool
    encryptionType: NotRequired[Literal["KMS"]]
    keyArn: NotRequired[str]

class FailedCampaignStateResponseTypeDef(TypedDict):
    campaignId: NotRequired[str]
    failureCode: NotRequired[GetCampaignStateBatchFailureCodeType]

FailedRequestTypeDef = TypedDict(
    "FailedRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
        "failureCode": NotRequired[FailureCodeType],
    },
)

class GetCampaignStateBatchRequestRequestTypeDef(TypedDict):
    campaignIds: Sequence[str]

class SuccessfulCampaignStateResponseTypeDef(TypedDict):
    campaignId: NotRequired[str]
    state: NotRequired[CampaignStateType]

GetCampaignStateRequestRequestTypeDef = TypedDict(
    "GetCampaignStateRequestRequestTypeDef",
    {
        "id": str,
    },
)

class GetConnectInstanceConfigRequestRequestTypeDef(TypedDict):
    connectInstanceId: str

class GetInstanceOnboardingJobStatusRequestRequestTypeDef(TypedDict):
    connectInstanceId: str

class InstanceOnboardingJobStatusTypeDef(TypedDict):
    connectInstanceId: str
    status: InstanceOnboardingJobStatusCodeType
    failureCode: NotRequired[InstanceOnboardingJobFailureCodeType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    arn: str

PauseCampaignRequestRequestTypeDef = TypedDict(
    "PauseCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)
SuccessfulRequestTypeDef = TypedDict(
    "SuccessfulRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
    },
)
ResumeCampaignRequestRequestTypeDef = TypedDict(
    "ResumeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)
StartCampaignRequestRequestTypeDef = TypedDict(
    "StartCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)
StopCampaignRequestRequestTypeDef = TypedDict(
    "StopCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tagKeys: Sequence[str]

UpdateCampaignNameRequestRequestTypeDef = TypedDict(
    "UpdateCampaignNameRequestRequestTypeDef",
    {
        "id": str,
        "name": str,
    },
)

class OutboundCallConfigTypeDef(TypedDict):
    connectContactFlowId: str
    connectSourcePhoneNumber: NotRequired[str]
    connectQueueId: NotRequired[str]
    answerMachineDetectionConfig: NotRequired[AnswerMachineDetectionConfigTypeDef]

UpdateCampaignOutboundCallConfigRequestRequestTypeDef = TypedDict(
    "UpdateCampaignOutboundCallConfigRequestRequestTypeDef",
    {
        "id": str,
        "connectContactFlowId": NotRequired[str],
        "connectSourcePhoneNumber": NotRequired[str],
        "answerMachineDetectionConfig": NotRequired[AnswerMachineDetectionConfigTypeDef],
    },
)

class CampaignFiltersTypeDef(TypedDict):
    instanceIdFilter: NotRequired[InstanceIdFilterTypeDef]

CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignStateResponseTypeDef(TypedDict):
    state: CampaignStateType
    ResponseMetadata: ResponseMetadataTypeDef

class ListCampaignsResponseTypeDef(TypedDict):
    campaignSummaryList: List[CampaignSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DialRequestTypeDef(TypedDict):
    clientToken: str
    phoneNumber: str
    expirationTime: TimestampTypeDef
    attributes: Mapping[str, str]

class DialerConfigTypeDef(TypedDict):
    progressiveDialerConfig: NotRequired[ProgressiveDialerConfigTypeDef]
    predictiveDialerConfig: NotRequired[PredictiveDialerConfigTypeDef]
    agentlessDialerConfig: NotRequired[AgentlessDialerConfigTypeDef]

class InstanceConfigTypeDef(TypedDict):
    connectInstanceId: str
    serviceLinkedRoleArn: str
    encryptionConfig: EncryptionConfigTypeDef

class StartInstanceOnboardingJobRequestRequestTypeDef(TypedDict):
    connectInstanceId: str
    encryptionConfig: EncryptionConfigTypeDef

class GetCampaignStateBatchResponseTypeDef(TypedDict):
    successfulRequests: List[SuccessfulCampaignStateResponseTypeDef]
    failedRequests: List[FailedCampaignStateResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceOnboardingJobStatusResponseTypeDef(TypedDict):
    connectInstanceOnboardingJobStatus: InstanceOnboardingJobStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartInstanceOnboardingJobResponseTypeDef(TypedDict):
    connectInstanceOnboardingJobStatus: InstanceOnboardingJobStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutDialRequestBatchResponseTypeDef(TypedDict):
    successfulRequests: List[SuccessfulRequestTypeDef]
    failedRequests: List[FailedRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListCampaignsRequestListCampaignsPaginateTypeDef(TypedDict):
    filters: NotRequired[CampaignFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCampaignsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filters: NotRequired[CampaignFiltersTypeDef]

PutDialRequestBatchRequestRequestTypeDef = TypedDict(
    "PutDialRequestBatchRequestRequestTypeDef",
    {
        "id": str,
        "dialRequests": Sequence[DialRequestTypeDef],
    },
)
CampaignTypeDef = TypedDict(
    "CampaignTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "connectInstanceId": str,
        "dialerConfig": DialerConfigTypeDef,
        "outboundCallConfig": OutboundCallConfigTypeDef,
        "tags": NotRequired[Dict[str, str]],
    },
)

class CreateCampaignRequestRequestTypeDef(TypedDict):
    name: str
    connectInstanceId: str
    dialerConfig: DialerConfigTypeDef
    outboundCallConfig: OutboundCallConfigTypeDef
    tags: NotRequired[Mapping[str, str]]

UpdateCampaignDialerConfigRequestRequestTypeDef = TypedDict(
    "UpdateCampaignDialerConfigRequestRequestTypeDef",
    {
        "id": str,
        "dialerConfig": DialerConfigTypeDef,
    },
)

class GetConnectInstanceConfigResponseTypeDef(TypedDict):
    connectInstanceConfig: InstanceConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCampaignResponseTypeDef(TypedDict):
    campaign: CampaignTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
