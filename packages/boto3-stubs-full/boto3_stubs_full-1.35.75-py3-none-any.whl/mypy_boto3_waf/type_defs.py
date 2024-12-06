"""
Type annotations for waf service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/type_defs/)

Usage::

    ```python
    from mypy_boto3_waf.type_defs import ExcludedRuleTypeDef

    data: ExcludedRuleTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ChangeActionType,
    ChangeTokenStatusType,
    ComparisonOperatorType,
    GeoMatchConstraintValueType,
    IPSetDescriptorTypeType,
    MatchFieldTypeType,
    PositionalConstraintType,
    PredicateTypeType,
    TextTransformationType,
    WafActionTypeType,
    WafOverrideActionTypeType,
    WafRuleTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActivatedRuleOutputTypeDef",
    "ActivatedRuleTypeDef",
    "ActivatedRuleUnionTypeDef",
    "BlobTypeDef",
    "ByteMatchSetSummaryTypeDef",
    "ByteMatchSetTypeDef",
    "ByteMatchSetUpdateTypeDef",
    "ByteMatchTupleOutputTypeDef",
    "ByteMatchTupleTypeDef",
    "ByteMatchTupleUnionTypeDef",
    "CreateByteMatchSetRequestRequestTypeDef",
    "CreateByteMatchSetResponseTypeDef",
    "CreateGeoMatchSetRequestRequestTypeDef",
    "CreateGeoMatchSetResponseTypeDef",
    "CreateIPSetRequestRequestTypeDef",
    "CreateIPSetResponseTypeDef",
    "CreateRateBasedRuleRequestRequestTypeDef",
    "CreateRateBasedRuleResponseTypeDef",
    "CreateRegexMatchSetRequestRequestTypeDef",
    "CreateRegexMatchSetResponseTypeDef",
    "CreateRegexPatternSetRequestRequestTypeDef",
    "CreateRegexPatternSetResponseTypeDef",
    "CreateRuleGroupRequestRequestTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "CreateRuleResponseTypeDef",
    "CreateSizeConstraintSetRequestRequestTypeDef",
    "CreateSizeConstraintSetResponseTypeDef",
    "CreateSqlInjectionMatchSetRequestRequestTypeDef",
    "CreateSqlInjectionMatchSetResponseTypeDef",
    "CreateWebACLMigrationStackRequestRequestTypeDef",
    "CreateWebACLMigrationStackResponseTypeDef",
    "CreateWebACLRequestRequestTypeDef",
    "CreateWebACLResponseTypeDef",
    "CreateXssMatchSetRequestRequestTypeDef",
    "CreateXssMatchSetResponseTypeDef",
    "DeleteByteMatchSetRequestRequestTypeDef",
    "DeleteByteMatchSetResponseTypeDef",
    "DeleteGeoMatchSetRequestRequestTypeDef",
    "DeleteGeoMatchSetResponseTypeDef",
    "DeleteIPSetRequestRequestTypeDef",
    "DeleteIPSetResponseTypeDef",
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    "DeletePermissionPolicyRequestRequestTypeDef",
    "DeleteRateBasedRuleRequestRequestTypeDef",
    "DeleteRateBasedRuleResponseTypeDef",
    "DeleteRegexMatchSetRequestRequestTypeDef",
    "DeleteRegexMatchSetResponseTypeDef",
    "DeleteRegexPatternSetRequestRequestTypeDef",
    "DeleteRegexPatternSetResponseTypeDef",
    "DeleteRuleGroupRequestRequestTypeDef",
    "DeleteRuleGroupResponseTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DeleteRuleResponseTypeDef",
    "DeleteSizeConstraintSetRequestRequestTypeDef",
    "DeleteSizeConstraintSetResponseTypeDef",
    "DeleteSqlInjectionMatchSetRequestRequestTypeDef",
    "DeleteSqlInjectionMatchSetResponseTypeDef",
    "DeleteWebACLRequestRequestTypeDef",
    "DeleteWebACLResponseTypeDef",
    "DeleteXssMatchSetRequestRequestTypeDef",
    "DeleteXssMatchSetResponseTypeDef",
    "ExcludedRuleTypeDef",
    "FieldToMatchTypeDef",
    "GeoMatchConstraintTypeDef",
    "GeoMatchSetSummaryTypeDef",
    "GeoMatchSetTypeDef",
    "GeoMatchSetUpdateTypeDef",
    "GetByteMatchSetRequestRequestTypeDef",
    "GetByteMatchSetResponseTypeDef",
    "GetChangeTokenResponseTypeDef",
    "GetChangeTokenStatusRequestRequestTypeDef",
    "GetChangeTokenStatusResponseTypeDef",
    "GetGeoMatchSetRequestRequestTypeDef",
    "GetGeoMatchSetResponseTypeDef",
    "GetIPSetRequestRequestTypeDef",
    "GetIPSetResponseTypeDef",
    "GetLoggingConfigurationRequestRequestTypeDef",
    "GetLoggingConfigurationResponseTypeDef",
    "GetPermissionPolicyRequestRequestTypeDef",
    "GetPermissionPolicyResponseTypeDef",
    "GetRateBasedRuleManagedKeysRequestGetRateBasedRuleManagedKeysPaginateTypeDef",
    "GetRateBasedRuleManagedKeysRequestRequestTypeDef",
    "GetRateBasedRuleManagedKeysResponseTypeDef",
    "GetRateBasedRuleRequestRequestTypeDef",
    "GetRateBasedRuleResponseTypeDef",
    "GetRegexMatchSetRequestRequestTypeDef",
    "GetRegexMatchSetResponseTypeDef",
    "GetRegexPatternSetRequestRequestTypeDef",
    "GetRegexPatternSetResponseTypeDef",
    "GetRuleGroupRequestRequestTypeDef",
    "GetRuleGroupResponseTypeDef",
    "GetRuleRequestRequestTypeDef",
    "GetRuleResponseTypeDef",
    "GetSampledRequestsRequestRequestTypeDef",
    "GetSampledRequestsResponseTypeDef",
    "GetSizeConstraintSetRequestRequestTypeDef",
    "GetSizeConstraintSetResponseTypeDef",
    "GetSqlInjectionMatchSetRequestRequestTypeDef",
    "GetSqlInjectionMatchSetResponseTypeDef",
    "GetWebACLRequestRequestTypeDef",
    "GetWebACLResponseTypeDef",
    "GetXssMatchSetRequestRequestTypeDef",
    "GetXssMatchSetResponseTypeDef",
    "HTTPHeaderTypeDef",
    "HTTPRequestTypeDef",
    "IPSetDescriptorTypeDef",
    "IPSetSummaryTypeDef",
    "IPSetTypeDef",
    "IPSetUpdateTypeDef",
    "ListActivatedRulesInRuleGroupRequestListActivatedRulesInRuleGroupPaginateTypeDef",
    "ListActivatedRulesInRuleGroupRequestRequestTypeDef",
    "ListActivatedRulesInRuleGroupResponseTypeDef",
    "ListByteMatchSetsRequestListByteMatchSetsPaginateTypeDef",
    "ListByteMatchSetsRequestRequestTypeDef",
    "ListByteMatchSetsResponseTypeDef",
    "ListGeoMatchSetsRequestListGeoMatchSetsPaginateTypeDef",
    "ListGeoMatchSetsRequestRequestTypeDef",
    "ListGeoMatchSetsResponseTypeDef",
    "ListIPSetsRequestListIPSetsPaginateTypeDef",
    "ListIPSetsRequestRequestTypeDef",
    "ListIPSetsResponseTypeDef",
    "ListLoggingConfigurationsRequestListLoggingConfigurationsPaginateTypeDef",
    "ListLoggingConfigurationsRequestRequestTypeDef",
    "ListLoggingConfigurationsResponseTypeDef",
    "ListRateBasedRulesRequestListRateBasedRulesPaginateTypeDef",
    "ListRateBasedRulesRequestRequestTypeDef",
    "ListRateBasedRulesResponseTypeDef",
    "ListRegexMatchSetsRequestListRegexMatchSetsPaginateTypeDef",
    "ListRegexMatchSetsRequestRequestTypeDef",
    "ListRegexMatchSetsResponseTypeDef",
    "ListRegexPatternSetsRequestListRegexPatternSetsPaginateTypeDef",
    "ListRegexPatternSetsRequestRequestTypeDef",
    "ListRegexPatternSetsResponseTypeDef",
    "ListRuleGroupsRequestListRuleGroupsPaginateTypeDef",
    "ListRuleGroupsRequestRequestTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListRulesResponseTypeDef",
    "ListSizeConstraintSetsRequestListSizeConstraintSetsPaginateTypeDef",
    "ListSizeConstraintSetsRequestRequestTypeDef",
    "ListSizeConstraintSetsResponseTypeDef",
    "ListSqlInjectionMatchSetsRequestListSqlInjectionMatchSetsPaginateTypeDef",
    "ListSqlInjectionMatchSetsRequestRequestTypeDef",
    "ListSqlInjectionMatchSetsResponseTypeDef",
    "ListSubscribedRuleGroupsRequestListSubscribedRuleGroupsPaginateTypeDef",
    "ListSubscribedRuleGroupsRequestRequestTypeDef",
    "ListSubscribedRuleGroupsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWebACLsRequestListWebACLsPaginateTypeDef",
    "ListWebACLsRequestRequestTypeDef",
    "ListWebACLsResponseTypeDef",
    "ListXssMatchSetsRequestListXssMatchSetsPaginateTypeDef",
    "ListXssMatchSetsRequestRequestTypeDef",
    "ListXssMatchSetsResponseTypeDef",
    "LoggingConfigurationOutputTypeDef",
    "LoggingConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PredicateTypeDef",
    "PutLoggingConfigurationRequestRequestTypeDef",
    "PutLoggingConfigurationResponseTypeDef",
    "PutPermissionPolicyRequestRequestTypeDef",
    "RateBasedRuleTypeDef",
    "RegexMatchSetSummaryTypeDef",
    "RegexMatchSetTypeDef",
    "RegexMatchSetUpdateTypeDef",
    "RegexMatchTupleTypeDef",
    "RegexPatternSetSummaryTypeDef",
    "RegexPatternSetTypeDef",
    "RegexPatternSetUpdateTypeDef",
    "ResponseMetadataTypeDef",
    "RuleGroupSummaryTypeDef",
    "RuleGroupTypeDef",
    "RuleGroupUpdateTypeDef",
    "RuleSummaryTypeDef",
    "RuleTypeDef",
    "RuleUpdateTypeDef",
    "SampledHTTPRequestTypeDef",
    "SizeConstraintSetSummaryTypeDef",
    "SizeConstraintSetTypeDef",
    "SizeConstraintSetUpdateTypeDef",
    "SizeConstraintTypeDef",
    "SqlInjectionMatchSetSummaryTypeDef",
    "SqlInjectionMatchSetTypeDef",
    "SqlInjectionMatchSetUpdateTypeDef",
    "SqlInjectionMatchTupleTypeDef",
    "SubscribedRuleGroupSummaryTypeDef",
    "TagInfoForResourceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimeWindowOutputTypeDef",
    "TimeWindowTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateByteMatchSetRequestRequestTypeDef",
    "UpdateByteMatchSetResponseTypeDef",
    "UpdateGeoMatchSetRequestRequestTypeDef",
    "UpdateGeoMatchSetResponseTypeDef",
    "UpdateIPSetRequestRequestTypeDef",
    "UpdateIPSetResponseTypeDef",
    "UpdateRateBasedRuleRequestRequestTypeDef",
    "UpdateRateBasedRuleResponseTypeDef",
    "UpdateRegexMatchSetRequestRequestTypeDef",
    "UpdateRegexMatchSetResponseTypeDef",
    "UpdateRegexPatternSetRequestRequestTypeDef",
    "UpdateRegexPatternSetResponseTypeDef",
    "UpdateRuleGroupRequestRequestTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "UpdateRuleResponseTypeDef",
    "UpdateSizeConstraintSetRequestRequestTypeDef",
    "UpdateSizeConstraintSetResponseTypeDef",
    "UpdateSqlInjectionMatchSetRequestRequestTypeDef",
    "UpdateSqlInjectionMatchSetResponseTypeDef",
    "UpdateWebACLRequestRequestTypeDef",
    "UpdateWebACLResponseTypeDef",
    "UpdateXssMatchSetRequestRequestTypeDef",
    "UpdateXssMatchSetResponseTypeDef",
    "WafActionTypeDef",
    "WafOverrideActionTypeDef",
    "WebACLSummaryTypeDef",
    "WebACLTypeDef",
    "WebACLUpdateTypeDef",
    "XssMatchSetSummaryTypeDef",
    "XssMatchSetTypeDef",
    "XssMatchSetUpdateTypeDef",
    "XssMatchTupleTypeDef",
)


class ExcludedRuleTypeDef(TypedDict):
    RuleId: str


WafActionTypeDef = TypedDict(
    "WafActionTypeDef",
    {
        "Type": WafActionTypeType,
    },
)
WafOverrideActionTypeDef = TypedDict(
    "WafOverrideActionTypeDef",
    {
        "Type": WafOverrideActionTypeType,
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ByteMatchSetSummaryTypeDef(TypedDict):
    ByteMatchSetId: str
    Name: str


FieldToMatchTypeDef = TypedDict(
    "FieldToMatchTypeDef",
    {
        "Type": MatchFieldTypeType,
        "Data": NotRequired[str],
    },
)


class CreateByteMatchSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateGeoMatchSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class CreateIPSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class CreateRegexMatchSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class CreateRegexPatternSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class RegexPatternSetTypeDef(TypedDict):
    RegexPatternSetId: str
    RegexPatternStrings: List[str]
    Name: NotRequired[str]


class RuleGroupTypeDef(TypedDict):
    RuleGroupId: str
    Name: NotRequired[str]
    MetricName: NotRequired[str]


class CreateSizeConstraintSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class CreateSqlInjectionMatchSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class CreateWebACLMigrationStackRequestRequestTypeDef(TypedDict):
    WebACLId: str
    S3BucketName: str
    IgnoreUnsupportedType: bool


class CreateXssMatchSetRequestRequestTypeDef(TypedDict):
    Name: str
    ChangeToken: str


class DeleteByteMatchSetRequestRequestTypeDef(TypedDict):
    ByteMatchSetId: str
    ChangeToken: str


class DeleteGeoMatchSetRequestRequestTypeDef(TypedDict):
    GeoMatchSetId: str
    ChangeToken: str


class DeleteIPSetRequestRequestTypeDef(TypedDict):
    IPSetId: str
    ChangeToken: str


class DeleteLoggingConfigurationRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class DeletePermissionPolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class DeleteRateBasedRuleRequestRequestTypeDef(TypedDict):
    RuleId: str
    ChangeToken: str


class DeleteRegexMatchSetRequestRequestTypeDef(TypedDict):
    RegexMatchSetId: str
    ChangeToken: str


class DeleteRegexPatternSetRequestRequestTypeDef(TypedDict):
    RegexPatternSetId: str
    ChangeToken: str


class DeleteRuleGroupRequestRequestTypeDef(TypedDict):
    RuleGroupId: str
    ChangeToken: str


class DeleteRuleRequestRequestTypeDef(TypedDict):
    RuleId: str
    ChangeToken: str


class DeleteSizeConstraintSetRequestRequestTypeDef(TypedDict):
    SizeConstraintSetId: str
    ChangeToken: str


class DeleteSqlInjectionMatchSetRequestRequestTypeDef(TypedDict):
    SqlInjectionMatchSetId: str
    ChangeToken: str


class DeleteWebACLRequestRequestTypeDef(TypedDict):
    WebACLId: str
    ChangeToken: str


class DeleteXssMatchSetRequestRequestTypeDef(TypedDict):
    XssMatchSetId: str
    ChangeToken: str


GeoMatchConstraintTypeDef = TypedDict(
    "GeoMatchConstraintTypeDef",
    {
        "Type": Literal["Country"],
        "Value": GeoMatchConstraintValueType,
    },
)


class GeoMatchSetSummaryTypeDef(TypedDict):
    GeoMatchSetId: str
    Name: str


class GetByteMatchSetRequestRequestTypeDef(TypedDict):
    ByteMatchSetId: str


class GetChangeTokenStatusRequestRequestTypeDef(TypedDict):
    ChangeToken: str


class GetGeoMatchSetRequestRequestTypeDef(TypedDict):
    GeoMatchSetId: str


class GetIPSetRequestRequestTypeDef(TypedDict):
    IPSetId: str


class GetLoggingConfigurationRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class GetPermissionPolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetRateBasedRuleManagedKeysRequestRequestTypeDef(TypedDict):
    RuleId: str
    NextMarker: NotRequired[str]


class GetRateBasedRuleRequestRequestTypeDef(TypedDict):
    RuleId: str


class GetRegexMatchSetRequestRequestTypeDef(TypedDict):
    RegexMatchSetId: str


class GetRegexPatternSetRequestRequestTypeDef(TypedDict):
    RegexPatternSetId: str


class GetRuleGroupRequestRequestTypeDef(TypedDict):
    RuleGroupId: str


class GetRuleRequestRequestTypeDef(TypedDict):
    RuleId: str


class TimeWindowOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime


class GetSizeConstraintSetRequestRequestTypeDef(TypedDict):
    SizeConstraintSetId: str


class GetSqlInjectionMatchSetRequestRequestTypeDef(TypedDict):
    SqlInjectionMatchSetId: str


class GetWebACLRequestRequestTypeDef(TypedDict):
    WebACLId: str


class GetXssMatchSetRequestRequestTypeDef(TypedDict):
    XssMatchSetId: str


class HTTPHeaderTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


IPSetDescriptorTypeDef = TypedDict(
    "IPSetDescriptorTypeDef",
    {
        "Type": IPSetDescriptorTypeType,
        "Value": str,
    },
)


class IPSetSummaryTypeDef(TypedDict):
    IPSetId: str
    Name: str


class ListActivatedRulesInRuleGroupRequestRequestTypeDef(TypedDict):
    RuleGroupId: NotRequired[str]
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class ListByteMatchSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class ListGeoMatchSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class ListIPSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class ListLoggingConfigurationsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class ListRateBasedRulesRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class RuleSummaryTypeDef(TypedDict):
    RuleId: str
    Name: str


class ListRegexMatchSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class RegexMatchSetSummaryTypeDef(TypedDict):
    RegexMatchSetId: str
    Name: str


class ListRegexPatternSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class RegexPatternSetSummaryTypeDef(TypedDict):
    RegexPatternSetId: str
    Name: str


class ListRuleGroupsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class RuleGroupSummaryTypeDef(TypedDict):
    RuleGroupId: str
    Name: str


class ListRulesRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class ListSizeConstraintSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class SizeConstraintSetSummaryTypeDef(TypedDict):
    SizeConstraintSetId: str
    Name: str


class ListSqlInjectionMatchSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class SqlInjectionMatchSetSummaryTypeDef(TypedDict):
    SqlInjectionMatchSetId: str
    Name: str


class ListSubscribedRuleGroupsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class SubscribedRuleGroupSummaryTypeDef(TypedDict):
    RuleGroupId: str
    Name: str
    MetricName: str


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class ListWebACLsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class WebACLSummaryTypeDef(TypedDict):
    WebACLId: str
    Name: str


class ListXssMatchSetsRequestRequestTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    Limit: NotRequired[int]


class XssMatchSetSummaryTypeDef(TypedDict):
    XssMatchSetId: str
    Name: str


PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {
        "Negated": bool,
        "Type": PredicateTypeType,
        "DataId": str,
    },
)


class PutPermissionPolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Policy: str


class RegexPatternSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    RegexPatternString: str


TimestampTypeDef = Union[datetime, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


ActivatedRuleOutputTypeDef = TypedDict(
    "ActivatedRuleOutputTypeDef",
    {
        "Priority": int,
        "RuleId": str,
        "Action": NotRequired[WafActionTypeDef],
        "OverrideAction": NotRequired[WafOverrideActionTypeDef],
        "Type": NotRequired[WafRuleTypeType],
        "ExcludedRules": NotRequired[List[ExcludedRuleTypeDef]],
    },
)
ActivatedRuleTypeDef = TypedDict(
    "ActivatedRuleTypeDef",
    {
        "Priority": int,
        "RuleId": str,
        "Action": NotRequired[WafActionTypeDef],
        "OverrideAction": NotRequired[WafOverrideActionTypeDef],
        "Type": NotRequired[WafRuleTypeType],
        "ExcludedRules": NotRequired[Sequence[ExcludedRuleTypeDef]],
    },
)


class ByteMatchTupleOutputTypeDef(TypedDict):
    FieldToMatch: FieldToMatchTypeDef
    TargetString: bytes
    TextTransformation: TextTransformationType
    PositionalConstraint: PositionalConstraintType


class ByteMatchTupleTypeDef(TypedDict):
    FieldToMatch: FieldToMatchTypeDef
    TargetString: BlobTypeDef
    TextTransformation: TextTransformationType
    PositionalConstraint: PositionalConstraintType


class LoggingConfigurationOutputTypeDef(TypedDict):
    ResourceArn: str
    LogDestinationConfigs: List[str]
    RedactedFields: NotRequired[List[FieldToMatchTypeDef]]


class LoggingConfigurationTypeDef(TypedDict):
    ResourceArn: str
    LogDestinationConfigs: Sequence[str]
    RedactedFields: NotRequired[Sequence[FieldToMatchTypeDef]]


class RegexMatchTupleTypeDef(TypedDict):
    FieldToMatch: FieldToMatchTypeDef
    TextTransformation: TextTransformationType
    RegexPatternSetId: str


class SizeConstraintTypeDef(TypedDict):
    FieldToMatch: FieldToMatchTypeDef
    TextTransformation: TextTransformationType
    ComparisonOperator: ComparisonOperatorType
    Size: int


class SqlInjectionMatchTupleTypeDef(TypedDict):
    FieldToMatch: FieldToMatchTypeDef
    TextTransformation: TextTransformationType


class XssMatchTupleTypeDef(TypedDict):
    FieldToMatch: FieldToMatchTypeDef
    TextTransformation: TextTransformationType


class CreateWebACLMigrationStackResponseTypeDef(TypedDict):
    S3ObjectUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteByteMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGeoMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIPSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRateBasedRuleResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRegexMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRegexPatternSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRuleGroupResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRuleResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSizeConstraintSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSqlInjectionMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWebACLResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteXssMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetChangeTokenResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetChangeTokenStatusResponseTypeDef(TypedDict):
    ChangeTokenStatus: ChangeTokenStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetPermissionPolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRateBasedRuleManagedKeysResponseTypeDef(TypedDict):
    ManagedKeys: List[str]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListByteMatchSetsResponseTypeDef(TypedDict):
    NextMarker: str
    ByteMatchSets: List[ByteMatchSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateByteMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGeoMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIPSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRateBasedRuleResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRegexMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRegexPatternSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRuleGroupResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRuleResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSizeConstraintSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSqlInjectionMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWebACLResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateXssMatchSetResponseTypeDef(TypedDict):
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRateBasedRuleRequestRequestTypeDef(TypedDict):
    Name: str
    MetricName: str
    RateKey: Literal["IP"]
    RateLimit: int
    ChangeToken: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateRuleGroupRequestRequestTypeDef(TypedDict):
    Name: str
    MetricName: str
    ChangeToken: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateRuleRequestRequestTypeDef(TypedDict):
    Name: str
    MetricName: str
    ChangeToken: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateWebACLRequestRequestTypeDef(TypedDict):
    Name: str
    MetricName: str
    DefaultAction: WafActionTypeDef
    ChangeToken: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagInfoForResourceTypeDef(TypedDict):
    ResourceARN: NotRequired[str]
    TagList: NotRequired[List[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateRegexPatternSetResponseTypeDef(TypedDict):
    RegexPatternSet: RegexPatternSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRegexPatternSetResponseTypeDef(TypedDict):
    RegexPatternSet: RegexPatternSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRuleGroupResponseTypeDef(TypedDict):
    RuleGroup: RuleGroupTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRuleGroupResponseTypeDef(TypedDict):
    RuleGroup: RuleGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GeoMatchSetTypeDef(TypedDict):
    GeoMatchSetId: str
    GeoMatchConstraints: List[GeoMatchConstraintTypeDef]
    Name: NotRequired[str]


class GeoMatchSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    GeoMatchConstraint: GeoMatchConstraintTypeDef


class ListGeoMatchSetsResponseTypeDef(TypedDict):
    NextMarker: str
    GeoMatchSets: List[GeoMatchSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRateBasedRuleManagedKeysRequestGetRateBasedRuleManagedKeysPaginateTypeDef(TypedDict):
    RuleId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListActivatedRulesInRuleGroupRequestListActivatedRulesInRuleGroupPaginateTypeDef(TypedDict):
    RuleGroupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListByteMatchSetsRequestListByteMatchSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGeoMatchSetsRequestListGeoMatchSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIPSetsRequestListIPSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLoggingConfigurationsRequestListLoggingConfigurationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRateBasedRulesRequestListRateBasedRulesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRegexMatchSetsRequestListRegexMatchSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRegexPatternSetsRequestListRegexPatternSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRuleGroupsRequestListRuleGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRulesRequestListRulesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSizeConstraintSetsRequestListSizeConstraintSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSqlInjectionMatchSetsRequestListSqlInjectionMatchSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscribedRuleGroupsRequestListSubscribedRuleGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWebACLsRequestListWebACLsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListXssMatchSetsRequestListXssMatchSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class HTTPRequestTypeDef(TypedDict):
    ClientIP: NotRequired[str]
    Country: NotRequired[str]
    URI: NotRequired[str]
    Method: NotRequired[str]
    HTTPVersion: NotRequired[str]
    Headers: NotRequired[List[HTTPHeaderTypeDef]]


class IPSetTypeDef(TypedDict):
    IPSetId: str
    IPSetDescriptors: List[IPSetDescriptorTypeDef]
    Name: NotRequired[str]


class IPSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    IPSetDescriptor: IPSetDescriptorTypeDef


class ListIPSetsResponseTypeDef(TypedDict):
    NextMarker: str
    IPSets: List[IPSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListRateBasedRulesResponseTypeDef(TypedDict):
    NextMarker: str
    Rules: List[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListRulesResponseTypeDef(TypedDict):
    NextMarker: str
    Rules: List[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListRegexMatchSetsResponseTypeDef(TypedDict):
    NextMarker: str
    RegexMatchSets: List[RegexMatchSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListRegexPatternSetsResponseTypeDef(TypedDict):
    NextMarker: str
    RegexPatternSets: List[RegexPatternSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListRuleGroupsResponseTypeDef(TypedDict):
    NextMarker: str
    RuleGroups: List[RuleGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListSizeConstraintSetsResponseTypeDef(TypedDict):
    NextMarker: str
    SizeConstraintSets: List[SizeConstraintSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListSqlInjectionMatchSetsResponseTypeDef(TypedDict):
    NextMarker: str
    SqlInjectionMatchSets: List[SqlInjectionMatchSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListSubscribedRuleGroupsResponseTypeDef(TypedDict):
    NextMarker: str
    RuleGroups: List[SubscribedRuleGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListWebACLsResponseTypeDef(TypedDict):
    NextMarker: str
    WebACLs: List[WebACLSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListXssMatchSetsResponseTypeDef(TypedDict):
    NextMarker: str
    XssMatchSets: List[XssMatchSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RateBasedRuleTypeDef(TypedDict):
    RuleId: str
    MatchPredicates: List[PredicateTypeDef]
    RateKey: Literal["IP"]
    RateLimit: int
    Name: NotRequired[str]
    MetricName: NotRequired[str]


class RuleTypeDef(TypedDict):
    RuleId: str
    Predicates: List[PredicateTypeDef]
    Name: NotRequired[str]
    MetricName: NotRequired[str]


class RuleUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    Predicate: PredicateTypeDef


class UpdateRegexPatternSetRequestRequestTypeDef(TypedDict):
    RegexPatternSetId: str
    Updates: Sequence[RegexPatternSetUpdateTypeDef]
    ChangeToken: str


class TimeWindowTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef


class ListActivatedRulesInRuleGroupResponseTypeDef(TypedDict):
    NextMarker: str
    ActivatedRules: List[ActivatedRuleOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class WebACLTypeDef(TypedDict):
    WebACLId: str
    DefaultAction: WafActionTypeDef
    Rules: List[ActivatedRuleOutputTypeDef]
    Name: NotRequired[str]
    MetricName: NotRequired[str]
    WebACLArn: NotRequired[str]


ActivatedRuleUnionTypeDef = Union[ActivatedRuleTypeDef, ActivatedRuleOutputTypeDef]


class ByteMatchSetTypeDef(TypedDict):
    ByteMatchSetId: str
    ByteMatchTuples: List[ByteMatchTupleOutputTypeDef]
    Name: NotRequired[str]


ByteMatchTupleUnionTypeDef = Union[ByteMatchTupleTypeDef, ByteMatchTupleOutputTypeDef]


class GetLoggingConfigurationResponseTypeDef(TypedDict):
    LoggingConfiguration: LoggingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListLoggingConfigurationsResponseTypeDef(TypedDict):
    LoggingConfigurations: List[LoggingConfigurationOutputTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutLoggingConfigurationResponseTypeDef(TypedDict):
    LoggingConfiguration: LoggingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutLoggingConfigurationRequestRequestTypeDef(TypedDict):
    LoggingConfiguration: LoggingConfigurationTypeDef


class RegexMatchSetTypeDef(TypedDict):
    RegexMatchSetId: NotRequired[str]
    Name: NotRequired[str]
    RegexMatchTuples: NotRequired[List[RegexMatchTupleTypeDef]]


class RegexMatchSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    RegexMatchTuple: RegexMatchTupleTypeDef


class SizeConstraintSetTypeDef(TypedDict):
    SizeConstraintSetId: str
    SizeConstraints: List[SizeConstraintTypeDef]
    Name: NotRequired[str]


class SizeConstraintSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    SizeConstraint: SizeConstraintTypeDef


class SqlInjectionMatchSetTypeDef(TypedDict):
    SqlInjectionMatchSetId: str
    SqlInjectionMatchTuples: List[SqlInjectionMatchTupleTypeDef]
    Name: NotRequired[str]


class SqlInjectionMatchSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    SqlInjectionMatchTuple: SqlInjectionMatchTupleTypeDef


class XssMatchSetTypeDef(TypedDict):
    XssMatchSetId: str
    XssMatchTuples: List[XssMatchTupleTypeDef]
    Name: NotRequired[str]


class XssMatchSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    XssMatchTuple: XssMatchTupleTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    NextMarker: str
    TagInfoForResource: TagInfoForResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGeoMatchSetResponseTypeDef(TypedDict):
    GeoMatchSet: GeoMatchSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetGeoMatchSetResponseTypeDef(TypedDict):
    GeoMatchSet: GeoMatchSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGeoMatchSetRequestRequestTypeDef(TypedDict):
    GeoMatchSetId: str
    ChangeToken: str
    Updates: Sequence[GeoMatchSetUpdateTypeDef]


class SampledHTTPRequestTypeDef(TypedDict):
    Request: HTTPRequestTypeDef
    Weight: int
    Timestamp: NotRequired[datetime]
    Action: NotRequired[str]
    RuleWithinRuleGroup: NotRequired[str]


class CreateIPSetResponseTypeDef(TypedDict):
    IPSet: IPSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetIPSetResponseTypeDef(TypedDict):
    IPSet: IPSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIPSetRequestRequestTypeDef(TypedDict):
    IPSetId: str
    ChangeToken: str
    Updates: Sequence[IPSetUpdateTypeDef]


class CreateRateBasedRuleResponseTypeDef(TypedDict):
    Rule: RateBasedRuleTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRateBasedRuleResponseTypeDef(TypedDict):
    Rule: RateBasedRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRuleResponseTypeDef(TypedDict):
    Rule: RuleTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRuleResponseTypeDef(TypedDict):
    Rule: RuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRateBasedRuleRequestRequestTypeDef(TypedDict):
    RuleId: str
    ChangeToken: str
    Updates: Sequence[RuleUpdateTypeDef]
    RateLimit: int


class UpdateRuleRequestRequestTypeDef(TypedDict):
    RuleId: str
    ChangeToken: str
    Updates: Sequence[RuleUpdateTypeDef]


class GetSampledRequestsRequestRequestTypeDef(TypedDict):
    WebAclId: str
    RuleId: str
    TimeWindow: TimeWindowTypeDef
    MaxItems: int


class CreateWebACLResponseTypeDef(TypedDict):
    WebACL: WebACLTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetWebACLResponseTypeDef(TypedDict):
    WebACL: WebACLTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RuleGroupUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    ActivatedRule: ActivatedRuleUnionTypeDef


class WebACLUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    ActivatedRule: ActivatedRuleUnionTypeDef


class CreateByteMatchSetResponseTypeDef(TypedDict):
    ByteMatchSet: ByteMatchSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetByteMatchSetResponseTypeDef(TypedDict):
    ByteMatchSet: ByteMatchSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ByteMatchSetUpdateTypeDef(TypedDict):
    Action: ChangeActionType
    ByteMatchTuple: ByteMatchTupleUnionTypeDef


class CreateRegexMatchSetResponseTypeDef(TypedDict):
    RegexMatchSet: RegexMatchSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRegexMatchSetResponseTypeDef(TypedDict):
    RegexMatchSet: RegexMatchSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRegexMatchSetRequestRequestTypeDef(TypedDict):
    RegexMatchSetId: str
    Updates: Sequence[RegexMatchSetUpdateTypeDef]
    ChangeToken: str


class CreateSizeConstraintSetResponseTypeDef(TypedDict):
    SizeConstraintSet: SizeConstraintSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSizeConstraintSetResponseTypeDef(TypedDict):
    SizeConstraintSet: SizeConstraintSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSizeConstraintSetRequestRequestTypeDef(TypedDict):
    SizeConstraintSetId: str
    ChangeToken: str
    Updates: Sequence[SizeConstraintSetUpdateTypeDef]


class CreateSqlInjectionMatchSetResponseTypeDef(TypedDict):
    SqlInjectionMatchSet: SqlInjectionMatchSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSqlInjectionMatchSetResponseTypeDef(TypedDict):
    SqlInjectionMatchSet: SqlInjectionMatchSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSqlInjectionMatchSetRequestRequestTypeDef(TypedDict):
    SqlInjectionMatchSetId: str
    ChangeToken: str
    Updates: Sequence[SqlInjectionMatchSetUpdateTypeDef]


class CreateXssMatchSetResponseTypeDef(TypedDict):
    XssMatchSet: XssMatchSetTypeDef
    ChangeToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetXssMatchSetResponseTypeDef(TypedDict):
    XssMatchSet: XssMatchSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateXssMatchSetRequestRequestTypeDef(TypedDict):
    XssMatchSetId: str
    ChangeToken: str
    Updates: Sequence[XssMatchSetUpdateTypeDef]


class GetSampledRequestsResponseTypeDef(TypedDict):
    SampledRequests: List[SampledHTTPRequestTypeDef]
    PopulationSize: int
    TimeWindow: TimeWindowOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRuleGroupRequestRequestTypeDef(TypedDict):
    RuleGroupId: str
    Updates: Sequence[RuleGroupUpdateTypeDef]
    ChangeToken: str


class UpdateWebACLRequestRequestTypeDef(TypedDict):
    WebACLId: str
    ChangeToken: str
    Updates: NotRequired[Sequence[WebACLUpdateTypeDef]]
    DefaultAction: NotRequired[WafActionTypeDef]


class UpdateByteMatchSetRequestRequestTypeDef(TypedDict):
    ByteMatchSetId: str
    ChangeToken: str
    Updates: Sequence[ByteMatchSetUpdateTypeDef]
