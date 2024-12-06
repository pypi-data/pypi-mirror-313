"""
Type annotations for mediastore service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediastore.type_defs import ContainerTypeDef

    data: ContainerTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import ContainerLevelMetricsType, ContainerStatusType, MethodNameType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ContainerTypeDef",
    "CorsRuleOutputTypeDef",
    "CorsRuleTypeDef",
    "CorsRuleUnionTypeDef",
    "CreateContainerInputRequestTypeDef",
    "CreateContainerOutputTypeDef",
    "DeleteContainerInputRequestTypeDef",
    "DeleteContainerPolicyInputRequestTypeDef",
    "DeleteCorsPolicyInputRequestTypeDef",
    "DeleteLifecyclePolicyInputRequestTypeDef",
    "DeleteMetricPolicyInputRequestTypeDef",
    "DescribeContainerInputRequestTypeDef",
    "DescribeContainerOutputTypeDef",
    "GetContainerPolicyInputRequestTypeDef",
    "GetContainerPolicyOutputTypeDef",
    "GetCorsPolicyInputRequestTypeDef",
    "GetCorsPolicyOutputTypeDef",
    "GetLifecyclePolicyInputRequestTypeDef",
    "GetLifecyclePolicyOutputTypeDef",
    "GetMetricPolicyInputRequestTypeDef",
    "GetMetricPolicyOutputTypeDef",
    "ListContainersInputListContainersPaginateTypeDef",
    "ListContainersInputRequestTypeDef",
    "ListContainersOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MetricPolicyOutputTypeDef",
    "MetricPolicyRuleTypeDef",
    "MetricPolicyTypeDef",
    "PaginatorConfigTypeDef",
    "PutContainerPolicyInputRequestTypeDef",
    "PutCorsPolicyInputRequestTypeDef",
    "PutLifecyclePolicyInputRequestTypeDef",
    "PutMetricPolicyInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "StartAccessLoggingInputRequestTypeDef",
    "StopAccessLoggingInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "UntagResourceInputRequestTypeDef",
)

class ContainerTypeDef(TypedDict):
    Endpoint: NotRequired[str]
    CreationTime: NotRequired[datetime]
    ARN: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ContainerStatusType]
    AccessLoggingEnabled: NotRequired[bool]

class CorsRuleOutputTypeDef(TypedDict):
    AllowedOrigins: List[str]
    AllowedHeaders: List[str]
    AllowedMethods: NotRequired[List[MethodNameType]]
    MaxAgeSeconds: NotRequired[int]
    ExposeHeaders: NotRequired[List[str]]

class CorsRuleTypeDef(TypedDict):
    AllowedOrigins: Sequence[str]
    AllowedHeaders: Sequence[str]
    AllowedMethods: NotRequired[Sequence[MethodNameType]]
    MaxAgeSeconds: NotRequired[int]
    ExposeHeaders: NotRequired[Sequence[str]]

class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteContainerInputRequestTypeDef(TypedDict):
    ContainerName: str

class DeleteContainerPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class DeleteCorsPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class DeleteLifecyclePolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class DeleteMetricPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class DescribeContainerInputRequestTypeDef(TypedDict):
    ContainerName: NotRequired[str]

class GetContainerPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class GetCorsPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class GetLifecyclePolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class GetMetricPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListContainersInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    Resource: str

class MetricPolicyRuleTypeDef(TypedDict):
    ObjectGroup: str
    ObjectGroupName: str

class PutContainerPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str
    Policy: str

class PutLifecyclePolicyInputRequestTypeDef(TypedDict):
    ContainerName: str
    LifecyclePolicy: str

class StartAccessLoggingInputRequestTypeDef(TypedDict):
    ContainerName: str

class StopAccessLoggingInputRequestTypeDef(TypedDict):
    ContainerName: str

class UntagResourceInputRequestTypeDef(TypedDict):
    Resource: str
    TagKeys: Sequence[str]

CorsRuleUnionTypeDef = Union[CorsRuleTypeDef, CorsRuleOutputTypeDef]

class CreateContainerInputRequestTypeDef(TypedDict):
    ContainerName: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class TagResourceInputRequestTypeDef(TypedDict):
    Resource: str
    Tags: Sequence[TagTypeDef]

CreateContainerOutputTypeDef = TypedDict(
    "CreateContainerOutputTypeDef",
    {
        "Container": ContainerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeContainerOutputTypeDef = TypedDict(
    "DescribeContainerOutputTypeDef",
    {
        "Container": ContainerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetContainerPolicyOutputTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCorsPolicyOutputTypeDef(TypedDict):
    CorsPolicy: List[CorsRuleOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetLifecyclePolicyOutputTypeDef(TypedDict):
    LifecyclePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListContainersOutputTypeDef(TypedDict):
    Containers: List[ContainerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListContainersInputListContainersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class MetricPolicyOutputTypeDef(TypedDict):
    ContainerLevelMetrics: ContainerLevelMetricsType
    MetricPolicyRules: NotRequired[List[MetricPolicyRuleTypeDef]]

class MetricPolicyTypeDef(TypedDict):
    ContainerLevelMetrics: ContainerLevelMetricsType
    MetricPolicyRules: NotRequired[Sequence[MetricPolicyRuleTypeDef]]

class PutCorsPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str
    CorsPolicy: Sequence[CorsRuleUnionTypeDef]

class GetMetricPolicyOutputTypeDef(TypedDict):
    MetricPolicy: MetricPolicyOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutMetricPolicyInputRequestTypeDef(TypedDict):
    ContainerName: str
    MetricPolicy: MetricPolicyTypeDef
