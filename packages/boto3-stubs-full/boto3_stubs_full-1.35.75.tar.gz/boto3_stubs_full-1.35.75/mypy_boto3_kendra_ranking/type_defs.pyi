"""
Type annotations for kendra-ranking service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/type_defs/)

Usage::

    ```python
    from mypy_boto3_kendra_ranking.type_defs import CapacityUnitsConfigurationTypeDef

    data: CapacityUnitsConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import RescoreExecutionPlanStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CapacityUnitsConfigurationTypeDef",
    "CreateRescoreExecutionPlanRequestRequestTypeDef",
    "CreateRescoreExecutionPlanResponseTypeDef",
    "DeleteRescoreExecutionPlanRequestRequestTypeDef",
    "DescribeRescoreExecutionPlanRequestRequestTypeDef",
    "DescribeRescoreExecutionPlanResponseTypeDef",
    "DocumentTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListRescoreExecutionPlansRequestRequestTypeDef",
    "ListRescoreExecutionPlansResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RescoreExecutionPlanSummaryTypeDef",
    "RescoreRequestRequestTypeDef",
    "RescoreResultItemTypeDef",
    "RescoreResultTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateRescoreExecutionPlanRequestRequestTypeDef",
)

class CapacityUnitsConfigurationTypeDef(TypedDict):
    RescoreCapacityUnits: int

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteRescoreExecutionPlanRequestRequestTypeDef(TypedDict):
    Id: str

class DescribeRescoreExecutionPlanRequestRequestTypeDef(TypedDict):
    Id: str

class DocumentTypeDef(TypedDict):
    Id: str
    OriginalScore: float
    GroupId: NotRequired[str]
    Title: NotRequired[str]
    Body: NotRequired[str]
    TokenizedTitle: NotRequired[Sequence[str]]
    TokenizedBody: NotRequired[Sequence[str]]

class ListRescoreExecutionPlansRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class RescoreExecutionPlanSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    Id: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]
    Status: NotRequired[RescoreExecutionPlanStatusType]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class RescoreResultItemTypeDef(TypedDict):
    DocumentId: NotRequired[str]
    Score: NotRequired[float]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateRescoreExecutionPlanRequestRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    CapacityUnits: NotRequired[CapacityUnitsConfigurationTypeDef]

class CreateRescoreExecutionPlanRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    CapacityUnits: NotRequired[CapacityUnitsConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class CreateRescoreExecutionPlanResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRescoreExecutionPlanResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    Name: str
    Description: str
    CapacityUnits: CapacityUnitsConfigurationTypeDef
    CreatedAt: datetime
    UpdatedAt: datetime
    Status: RescoreExecutionPlanStatusType
    ErrorMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RescoreRequestRequestTypeDef(TypedDict):
    RescoreExecutionPlanId: str
    SearchQuery: str
    Documents: Sequence[DocumentTypeDef]

class ListRescoreExecutionPlansResponseTypeDef(TypedDict):
    SummaryItems: List[RescoreExecutionPlanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RescoreResultTypeDef(TypedDict):
    RescoreId: str
    ResultItems: List[RescoreResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
