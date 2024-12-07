"""
Type annotations for personalize-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_personalize_runtime.type_defs import GetActionRecommendationsRequestRequestTypeDef

    data: GetActionRecommendationsRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetActionRecommendationsRequestRequestTypeDef",
    "GetActionRecommendationsResponseTypeDef",
    "GetPersonalizedRankingRequestRequestTypeDef",
    "GetPersonalizedRankingResponseTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetRecommendationsResponseTypeDef",
    "PredictedActionTypeDef",
    "PredictedItemTypeDef",
    "PromotionTypeDef",
    "ResponseMetadataTypeDef",
)

class GetActionRecommendationsRequestRequestTypeDef(TypedDict):
    campaignArn: NotRequired[str]
    userId: NotRequired[str]
    numResults: NotRequired[int]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]

class PredictedActionTypeDef(TypedDict):
    actionId: NotRequired[str]
    score: NotRequired[float]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetPersonalizedRankingRequestRequestTypeDef(TypedDict):
    campaignArn: str
    inputList: Sequence[str]
    userId: str
    context: NotRequired[Mapping[str, str]]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]
    metadataColumns: NotRequired[Mapping[str, Sequence[str]]]

class PredictedItemTypeDef(TypedDict):
    itemId: NotRequired[str]
    score: NotRequired[float]
    promotionName: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]
    reason: NotRequired[List[str]]

class PromotionTypeDef(TypedDict):
    name: NotRequired[str]
    percentPromotedItems: NotRequired[int]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]

class GetActionRecommendationsResponseTypeDef(TypedDict):
    actionList: List[PredictedActionTypeDef]
    recommendationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetPersonalizedRankingResponseTypeDef(TypedDict):
    personalizedRanking: List[PredictedItemTypeDef]
    recommendationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRecommendationsResponseTypeDef(TypedDict):
    itemList: List[PredictedItemTypeDef]
    recommendationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRecommendationsRequestRequestTypeDef(TypedDict):
    campaignArn: NotRequired[str]
    itemId: NotRequired[str]
    userId: NotRequired[str]
    numResults: NotRequired[int]
    context: NotRequired[Mapping[str, str]]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]
    recommenderArn: NotRequired[str]
    promotions: NotRequired[Sequence[PromotionTypeDef]]
    metadataColumns: NotRequired[Mapping[str, Sequence[str]]]
