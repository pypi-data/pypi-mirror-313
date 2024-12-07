"""
Type annotations for rbin service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rbin/type_defs/)

Usage::

    ```python
    from mypy_boto3_rbin.type_defs import ResourceTagTypeDef

    data: ResourceTagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import LockStateType, ResourceTypeType, RuleStatusType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "CreateRuleRequestRequestTypeDef",
    "CreateRuleResponseTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "GetRuleRequestRequestTypeDef",
    "GetRuleResponseTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListRulesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LockConfigurationTypeDef",
    "LockRuleRequestRequestTypeDef",
    "LockRuleResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "RetentionPeriodTypeDef",
    "RuleSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UnlockDelayTypeDef",
    "UnlockRuleRequestRequestTypeDef",
    "UnlockRuleResponseTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "UpdateRuleResponseTypeDef",
)

class ResourceTagTypeDef(TypedDict):
    ResourceTagKey: str
    ResourceTagValue: NotRequired[str]

class RetentionPeriodTypeDef(TypedDict):
    RetentionPeriodValue: int
    RetentionPeriodUnit: Literal["DAYS"]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteRuleRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetRuleRequestRequestTypeDef(TypedDict):
    Identifier: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class UnlockDelayTypeDef(TypedDict):
    UnlockDelayValue: int
    UnlockDelayUnit: Literal["DAYS"]

class UnlockRuleRequestRequestTypeDef(TypedDict):
    Identifier: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class ListRulesRequestRequestTypeDef(TypedDict):
    ResourceType: ResourceTypeType
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    LockState: NotRequired[LockStateType]
    ExcludeResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class RuleSummaryTypeDef(TypedDict):
    Identifier: NotRequired[str]
    Description: NotRequired[str]
    RetentionPeriod: NotRequired[RetentionPeriodTypeDef]
    LockState: NotRequired[LockStateType]
    RuleArn: NotRequired[str]

class UpdateRuleRequestRequestTypeDef(TypedDict):
    Identifier: str
    RetentionPeriod: NotRequired[RetentionPeriodTypeDef]
    Description: NotRequired[str]
    ResourceType: NotRequired[ResourceTypeType]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    ExcludeResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRuleResponseTypeDef(TypedDict):
    Identifier: str
    RetentionPeriod: RetentionPeriodTypeDef
    Description: str
    ResourceType: ResourceTypeType
    ResourceTags: List[ResourceTagTypeDef]
    Status: RuleStatusType
    LockState: LockStateType
    LockEndTime: datetime
    RuleArn: str
    ExcludeResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListRulesRequestListRulesPaginateTypeDef(TypedDict):
    ResourceType: ResourceTypeType
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    LockState: NotRequired[LockStateType]
    ExcludeResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class LockConfigurationTypeDef(TypedDict):
    UnlockDelay: UnlockDelayTypeDef

class ListRulesResponseTypeDef(TypedDict):
    Rules: List[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateRuleRequestRequestTypeDef(TypedDict):
    RetentionPeriod: RetentionPeriodTypeDef
    ResourceType: ResourceTypeType
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    LockConfiguration: NotRequired[LockConfigurationTypeDef]
    ExcludeResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class CreateRuleResponseTypeDef(TypedDict):
    Identifier: str
    RetentionPeriod: RetentionPeriodTypeDef
    Description: str
    Tags: List[TagTypeDef]
    ResourceType: ResourceTypeType
    ResourceTags: List[ResourceTagTypeDef]
    Status: RuleStatusType
    LockConfiguration: LockConfigurationTypeDef
    LockState: LockStateType
    RuleArn: str
    ExcludeResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRuleResponseTypeDef(TypedDict):
    Identifier: str
    Description: str
    ResourceType: ResourceTypeType
    RetentionPeriod: RetentionPeriodTypeDef
    ResourceTags: List[ResourceTagTypeDef]
    Status: RuleStatusType
    LockConfiguration: LockConfigurationTypeDef
    LockState: LockStateType
    LockEndTime: datetime
    RuleArn: str
    ExcludeResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class LockRuleRequestRequestTypeDef(TypedDict):
    Identifier: str
    LockConfiguration: LockConfigurationTypeDef

class LockRuleResponseTypeDef(TypedDict):
    Identifier: str
    Description: str
    ResourceType: ResourceTypeType
    RetentionPeriod: RetentionPeriodTypeDef
    ResourceTags: List[ResourceTagTypeDef]
    Status: RuleStatusType
    LockConfiguration: LockConfigurationTypeDef
    LockState: LockStateType
    RuleArn: str
    ExcludeResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UnlockRuleResponseTypeDef(TypedDict):
    Identifier: str
    Description: str
    ResourceType: ResourceTypeType
    RetentionPeriod: RetentionPeriodTypeDef
    ResourceTags: List[ResourceTagTypeDef]
    Status: RuleStatusType
    LockConfiguration: LockConfigurationTypeDef
    LockState: LockStateType
    LockEndTime: datetime
    RuleArn: str
    ExcludeResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
