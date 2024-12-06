"""
Type annotations for waf-regional service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_waf_regional.client import WAFRegionalClient

    session = Session()
    client: WAFRegionalClient = session.client("waf-regional")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AssociateWebACLRequestRequestTypeDef,
    CreateByteMatchSetRequestRequestTypeDef,
    CreateByteMatchSetResponseTypeDef,
    CreateGeoMatchSetRequestRequestTypeDef,
    CreateGeoMatchSetResponseTypeDef,
    CreateIPSetRequestRequestTypeDef,
    CreateIPSetResponseTypeDef,
    CreateRateBasedRuleRequestRequestTypeDef,
    CreateRateBasedRuleResponseTypeDef,
    CreateRegexMatchSetRequestRequestTypeDef,
    CreateRegexMatchSetResponseTypeDef,
    CreateRegexPatternSetRequestRequestTypeDef,
    CreateRegexPatternSetResponseTypeDef,
    CreateRuleGroupRequestRequestTypeDef,
    CreateRuleGroupResponseTypeDef,
    CreateRuleRequestRequestTypeDef,
    CreateRuleResponseTypeDef,
    CreateSizeConstraintSetRequestRequestTypeDef,
    CreateSizeConstraintSetResponseTypeDef,
    CreateSqlInjectionMatchSetRequestRequestTypeDef,
    CreateSqlInjectionMatchSetResponseTypeDef,
    CreateWebACLMigrationStackRequestRequestTypeDef,
    CreateWebACLMigrationStackResponseTypeDef,
    CreateWebACLRequestRequestTypeDef,
    CreateWebACLResponseTypeDef,
    CreateXssMatchSetRequestRequestTypeDef,
    CreateXssMatchSetResponseTypeDef,
    DeleteByteMatchSetRequestRequestTypeDef,
    DeleteByteMatchSetResponseTypeDef,
    DeleteGeoMatchSetRequestRequestTypeDef,
    DeleteGeoMatchSetResponseTypeDef,
    DeleteIPSetRequestRequestTypeDef,
    DeleteIPSetResponseTypeDef,
    DeleteLoggingConfigurationRequestRequestTypeDef,
    DeletePermissionPolicyRequestRequestTypeDef,
    DeleteRateBasedRuleRequestRequestTypeDef,
    DeleteRateBasedRuleResponseTypeDef,
    DeleteRegexMatchSetRequestRequestTypeDef,
    DeleteRegexMatchSetResponseTypeDef,
    DeleteRegexPatternSetRequestRequestTypeDef,
    DeleteRegexPatternSetResponseTypeDef,
    DeleteRuleGroupRequestRequestTypeDef,
    DeleteRuleGroupResponseTypeDef,
    DeleteRuleRequestRequestTypeDef,
    DeleteRuleResponseTypeDef,
    DeleteSizeConstraintSetRequestRequestTypeDef,
    DeleteSizeConstraintSetResponseTypeDef,
    DeleteSqlInjectionMatchSetRequestRequestTypeDef,
    DeleteSqlInjectionMatchSetResponseTypeDef,
    DeleteWebACLRequestRequestTypeDef,
    DeleteWebACLResponseTypeDef,
    DeleteXssMatchSetRequestRequestTypeDef,
    DeleteXssMatchSetResponseTypeDef,
    DisassociateWebACLRequestRequestTypeDef,
    GetByteMatchSetRequestRequestTypeDef,
    GetByteMatchSetResponseTypeDef,
    GetChangeTokenResponseTypeDef,
    GetChangeTokenStatusRequestRequestTypeDef,
    GetChangeTokenStatusResponseTypeDef,
    GetGeoMatchSetRequestRequestTypeDef,
    GetGeoMatchSetResponseTypeDef,
    GetIPSetRequestRequestTypeDef,
    GetIPSetResponseTypeDef,
    GetLoggingConfigurationRequestRequestTypeDef,
    GetLoggingConfigurationResponseTypeDef,
    GetPermissionPolicyRequestRequestTypeDef,
    GetPermissionPolicyResponseTypeDef,
    GetRateBasedRuleManagedKeysRequestRequestTypeDef,
    GetRateBasedRuleManagedKeysResponseTypeDef,
    GetRateBasedRuleRequestRequestTypeDef,
    GetRateBasedRuleResponseTypeDef,
    GetRegexMatchSetRequestRequestTypeDef,
    GetRegexMatchSetResponseTypeDef,
    GetRegexPatternSetRequestRequestTypeDef,
    GetRegexPatternSetResponseTypeDef,
    GetRuleGroupRequestRequestTypeDef,
    GetRuleGroupResponseTypeDef,
    GetRuleRequestRequestTypeDef,
    GetRuleResponseTypeDef,
    GetSampledRequestsRequestRequestTypeDef,
    GetSampledRequestsResponseTypeDef,
    GetSizeConstraintSetRequestRequestTypeDef,
    GetSizeConstraintSetResponseTypeDef,
    GetSqlInjectionMatchSetRequestRequestTypeDef,
    GetSqlInjectionMatchSetResponseTypeDef,
    GetWebACLForResourceRequestRequestTypeDef,
    GetWebACLForResourceResponseTypeDef,
    GetWebACLRequestRequestTypeDef,
    GetWebACLResponseTypeDef,
    GetXssMatchSetRequestRequestTypeDef,
    GetXssMatchSetResponseTypeDef,
    ListActivatedRulesInRuleGroupRequestRequestTypeDef,
    ListActivatedRulesInRuleGroupResponseTypeDef,
    ListByteMatchSetsRequestRequestTypeDef,
    ListByteMatchSetsResponseTypeDef,
    ListGeoMatchSetsRequestRequestTypeDef,
    ListGeoMatchSetsResponseTypeDef,
    ListIPSetsRequestRequestTypeDef,
    ListIPSetsResponseTypeDef,
    ListLoggingConfigurationsRequestRequestTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRateBasedRulesRequestRequestTypeDef,
    ListRateBasedRulesResponseTypeDef,
    ListRegexMatchSetsRequestRequestTypeDef,
    ListRegexMatchSetsResponseTypeDef,
    ListRegexPatternSetsRequestRequestTypeDef,
    ListRegexPatternSetsResponseTypeDef,
    ListResourcesForWebACLRequestRequestTypeDef,
    ListResourcesForWebACLResponseTypeDef,
    ListRuleGroupsRequestRequestTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListSizeConstraintSetsRequestRequestTypeDef,
    ListSizeConstraintSetsResponseTypeDef,
    ListSqlInjectionMatchSetsRequestRequestTypeDef,
    ListSqlInjectionMatchSetsResponseTypeDef,
    ListSubscribedRuleGroupsRequestRequestTypeDef,
    ListSubscribedRuleGroupsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebACLsRequestRequestTypeDef,
    ListWebACLsResponseTypeDef,
    ListXssMatchSetsRequestRequestTypeDef,
    ListXssMatchSetsResponseTypeDef,
    PutLoggingConfigurationRequestRequestTypeDef,
    PutLoggingConfigurationResponseTypeDef,
    PutPermissionPolicyRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateByteMatchSetRequestRequestTypeDef,
    UpdateByteMatchSetResponseTypeDef,
    UpdateGeoMatchSetRequestRequestTypeDef,
    UpdateGeoMatchSetResponseTypeDef,
    UpdateIPSetRequestRequestTypeDef,
    UpdateIPSetResponseTypeDef,
    UpdateRateBasedRuleRequestRequestTypeDef,
    UpdateRateBasedRuleResponseTypeDef,
    UpdateRegexMatchSetRequestRequestTypeDef,
    UpdateRegexMatchSetResponseTypeDef,
    UpdateRegexPatternSetRequestRequestTypeDef,
    UpdateRegexPatternSetResponseTypeDef,
    UpdateRuleGroupRequestRequestTypeDef,
    UpdateRuleGroupResponseTypeDef,
    UpdateRuleRequestRequestTypeDef,
    UpdateRuleResponseTypeDef,
    UpdateSizeConstraintSetRequestRequestTypeDef,
    UpdateSizeConstraintSetResponseTypeDef,
    UpdateSqlInjectionMatchSetRequestRequestTypeDef,
    UpdateSqlInjectionMatchSetResponseTypeDef,
    UpdateWebACLRequestRequestTypeDef,
    UpdateWebACLResponseTypeDef,
    UpdateXssMatchSetRequestRequestTypeDef,
    UpdateXssMatchSetResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("WAFRegionalClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    WAFBadRequestException: Type[BotocoreClientError]
    WAFDisallowedNameException: Type[BotocoreClientError]
    WAFEntityMigrationException: Type[BotocoreClientError]
    WAFInternalErrorException: Type[BotocoreClientError]
    WAFInvalidAccountException: Type[BotocoreClientError]
    WAFInvalidOperationException: Type[BotocoreClientError]
    WAFInvalidParameterException: Type[BotocoreClientError]
    WAFInvalidPermissionPolicyException: Type[BotocoreClientError]
    WAFInvalidRegexPatternException: Type[BotocoreClientError]
    WAFLimitsExceededException: Type[BotocoreClientError]
    WAFNonEmptyEntityException: Type[BotocoreClientError]
    WAFNonexistentContainerException: Type[BotocoreClientError]
    WAFNonexistentItemException: Type[BotocoreClientError]
    WAFReferencedItemException: Type[BotocoreClientError]
    WAFServiceLinkedRoleErrorException: Type[BotocoreClientError]
    WAFStaleDataException: Type[BotocoreClientError]
    WAFSubscriptionNotFoundException: Type[BotocoreClientError]
    WAFTagOperationException: Type[BotocoreClientError]
    WAFTagOperationInternalErrorException: Type[BotocoreClientError]
    WAFUnavailableEntityException: Type[BotocoreClientError]


class WAFRegionalClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WAFRegionalClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#close)
        """

    def associate_web_acl(
        self, **kwargs: Unpack[AssociateWebACLRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic Regional</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/associate_web_acl.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#associate_web_acl)
        """

    def create_byte_match_set(
        self, **kwargs: Unpack[CreateByteMatchSetRequestRequestTypeDef]
    ) -> CreateByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_byte_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_byte_match_set)
        """

    def create_geo_match_set(
        self, **kwargs: Unpack[CreateGeoMatchSetRequestRequestTypeDef]
    ) -> CreateGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_geo_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_geo_match_set)
        """

    def create_ip_set(
        self, **kwargs: Unpack[CreateIPSetRequestRequestTypeDef]
    ) -> CreateIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_ip_set)
        """

    def create_rate_based_rule(
        self, **kwargs: Unpack[CreateRateBasedRuleRequestRequestTypeDef]
    ) -> CreateRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_rate_based_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_rate_based_rule)
        """

    def create_regex_match_set(
        self, **kwargs: Unpack[CreateRegexMatchSetRequestRequestTypeDef]
    ) -> CreateRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_regex_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_regex_match_set)
        """

    def create_regex_pattern_set(
        self, **kwargs: Unpack[CreateRegexPatternSetRequestRequestTypeDef]
    ) -> CreateRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_regex_pattern_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_regex_pattern_set)
        """

    def create_rule(
        self, **kwargs: Unpack[CreateRuleRequestRequestTypeDef]
    ) -> CreateRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_rule)
        """

    def create_rule_group(
        self, **kwargs: Unpack[CreateRuleGroupRequestRequestTypeDef]
    ) -> CreateRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_rule_group)
        """

    def create_size_constraint_set(
        self, **kwargs: Unpack[CreateSizeConstraintSetRequestRequestTypeDef]
    ) -> CreateSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_size_constraint_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_size_constraint_set)
        """

    def create_sql_injection_match_set(
        self, **kwargs: Unpack[CreateSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> CreateSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_sql_injection_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_sql_injection_match_set)
        """

    def create_web_acl(
        self, **kwargs: Unpack[CreateWebACLRequestRequestTypeDef]
    ) -> CreateWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_web_acl.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_web_acl)
        """

    def create_web_acl_migration_stack(
        self, **kwargs: Unpack[CreateWebACLMigrationStackRequestRequestTypeDef]
    ) -> CreateWebACLMigrationStackResponseTypeDef:
        """
        Creates an AWS CloudFormation WAFV2 template for the specified web ACL in the
        specified Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_web_acl_migration_stack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_web_acl_migration_stack)
        """

    def create_xss_match_set(
        self, **kwargs: Unpack[CreateXssMatchSetRequestRequestTypeDef]
    ) -> CreateXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/create_xss_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#create_xss_match_set)
        """

    def delete_byte_match_set(
        self, **kwargs: Unpack[DeleteByteMatchSetRequestRequestTypeDef]
    ) -> DeleteByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_byte_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_byte_match_set)
        """

    def delete_geo_match_set(
        self, **kwargs: Unpack[DeleteGeoMatchSetRequestRequestTypeDef]
    ) -> DeleteGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_geo_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_geo_match_set)
        """

    def delete_ip_set(
        self, **kwargs: Unpack[DeleteIPSetRequestRequestTypeDef]
    ) -> DeleteIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_ip_set)
        """

    def delete_logging_configuration(
        self, **kwargs: Unpack[DeleteLoggingConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_logging_configuration)
        """

    def delete_permission_policy(
        self, **kwargs: Unpack[DeletePermissionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_permission_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_permission_policy)
        """

    def delete_rate_based_rule(
        self, **kwargs: Unpack[DeleteRateBasedRuleRequestRequestTypeDef]
    ) -> DeleteRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_rate_based_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_rate_based_rule)
        """

    def delete_regex_match_set(
        self, **kwargs: Unpack[DeleteRegexMatchSetRequestRequestTypeDef]
    ) -> DeleteRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_regex_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_regex_match_set)
        """

    def delete_regex_pattern_set(
        self, **kwargs: Unpack[DeleteRegexPatternSetRequestRequestTypeDef]
    ) -> DeleteRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_regex_pattern_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_regex_pattern_set)
        """

    def delete_rule(
        self, **kwargs: Unpack[DeleteRuleRequestRequestTypeDef]
    ) -> DeleteRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_rule)
        """

    def delete_rule_group(
        self, **kwargs: Unpack[DeleteRuleGroupRequestRequestTypeDef]
    ) -> DeleteRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_rule_group)
        """

    def delete_size_constraint_set(
        self, **kwargs: Unpack[DeleteSizeConstraintSetRequestRequestTypeDef]
    ) -> DeleteSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_size_constraint_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_size_constraint_set)
        """

    def delete_sql_injection_match_set(
        self, **kwargs: Unpack[DeleteSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> DeleteSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_sql_injection_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_sql_injection_match_set)
        """

    def delete_web_acl(
        self, **kwargs: Unpack[DeleteWebACLRequestRequestTypeDef]
    ) -> DeleteWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_web_acl.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_web_acl)
        """

    def delete_xss_match_set(
        self, **kwargs: Unpack[DeleteXssMatchSetRequestRequestTypeDef]
    ) -> DeleteXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/delete_xss_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#delete_xss_match_set)
        """

    def disassociate_web_acl(
        self, **kwargs: Unpack[DisassociateWebACLRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic Regional</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/disassociate_web_acl.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#disassociate_web_acl)
        """

    def get_byte_match_set(
        self, **kwargs: Unpack[GetByteMatchSetRequestRequestTypeDef]
    ) -> GetByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_byte_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_byte_match_set)
        """

    def get_change_token(self) -> GetChangeTokenResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_change_token.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_change_token)
        """

    def get_change_token_status(
        self, **kwargs: Unpack[GetChangeTokenStatusRequestRequestTypeDef]
    ) -> GetChangeTokenStatusResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_change_token_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_change_token_status)
        """

    def get_geo_match_set(
        self, **kwargs: Unpack[GetGeoMatchSetRequestRequestTypeDef]
    ) -> GetGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_geo_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_geo_match_set)
        """

    def get_ip_set(
        self, **kwargs: Unpack[GetIPSetRequestRequestTypeDef]
    ) -> GetIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_ip_set)
        """

    def get_logging_configuration(
        self, **kwargs: Unpack[GetLoggingConfigurationRequestRequestTypeDef]
    ) -> GetLoggingConfigurationResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_logging_configuration)
        """

    def get_permission_policy(
        self, **kwargs: Unpack[GetPermissionPolicyRequestRequestTypeDef]
    ) -> GetPermissionPolicyResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_permission_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_permission_policy)
        """

    def get_rate_based_rule(
        self, **kwargs: Unpack[GetRateBasedRuleRequestRequestTypeDef]
    ) -> GetRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_rate_based_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_rate_based_rule)
        """

    def get_rate_based_rule_managed_keys(
        self, **kwargs: Unpack[GetRateBasedRuleManagedKeysRequestRequestTypeDef]
    ) -> GetRateBasedRuleManagedKeysResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_rate_based_rule_managed_keys.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_rate_based_rule_managed_keys)
        """

    def get_regex_match_set(
        self, **kwargs: Unpack[GetRegexMatchSetRequestRequestTypeDef]
    ) -> GetRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_regex_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_regex_match_set)
        """

    def get_regex_pattern_set(
        self, **kwargs: Unpack[GetRegexPatternSetRequestRequestTypeDef]
    ) -> GetRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_regex_pattern_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_regex_pattern_set)
        """

    def get_rule(self, **kwargs: Unpack[GetRuleRequestRequestTypeDef]) -> GetRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_rule)
        """

    def get_rule_group(
        self, **kwargs: Unpack[GetRuleGroupRequestRequestTypeDef]
    ) -> GetRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_rule_group)
        """

    def get_sampled_requests(
        self, **kwargs: Unpack[GetSampledRequestsRequestRequestTypeDef]
    ) -> GetSampledRequestsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_sampled_requests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_sampled_requests)
        """

    def get_size_constraint_set(
        self, **kwargs: Unpack[GetSizeConstraintSetRequestRequestTypeDef]
    ) -> GetSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_size_constraint_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_size_constraint_set)
        """

    def get_sql_injection_match_set(
        self, **kwargs: Unpack[GetSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> GetSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_sql_injection_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_sql_injection_match_set)
        """

    def get_web_acl(
        self, **kwargs: Unpack[GetWebACLRequestRequestTypeDef]
    ) -> GetWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_web_acl.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_web_acl)
        """

    def get_web_acl_for_resource(
        self, **kwargs: Unpack[GetWebACLForResourceRequestRequestTypeDef]
    ) -> GetWebACLForResourceResponseTypeDef:
        """
        This is <b>AWS WAF Classic Regional</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_web_acl_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_web_acl_for_resource)
        """

    def get_xss_match_set(
        self, **kwargs: Unpack[GetXssMatchSetRequestRequestTypeDef]
    ) -> GetXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/get_xss_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#get_xss_match_set)
        """

    def list_activated_rules_in_rule_group(
        self, **kwargs: Unpack[ListActivatedRulesInRuleGroupRequestRequestTypeDef]
    ) -> ListActivatedRulesInRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_activated_rules_in_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_activated_rules_in_rule_group)
        """

    def list_byte_match_sets(
        self, **kwargs: Unpack[ListByteMatchSetsRequestRequestTypeDef]
    ) -> ListByteMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_byte_match_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_byte_match_sets)
        """

    def list_geo_match_sets(
        self, **kwargs: Unpack[ListGeoMatchSetsRequestRequestTypeDef]
    ) -> ListGeoMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_geo_match_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_geo_match_sets)
        """

    def list_ip_sets(
        self, **kwargs: Unpack[ListIPSetsRequestRequestTypeDef]
    ) -> ListIPSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_ip_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_ip_sets)
        """

    def list_logging_configurations(
        self, **kwargs: Unpack[ListLoggingConfigurationsRequestRequestTypeDef]
    ) -> ListLoggingConfigurationsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_logging_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_logging_configurations)
        """

    def list_rate_based_rules(
        self, **kwargs: Unpack[ListRateBasedRulesRequestRequestTypeDef]
    ) -> ListRateBasedRulesResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_rate_based_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_rate_based_rules)
        """

    def list_regex_match_sets(
        self, **kwargs: Unpack[ListRegexMatchSetsRequestRequestTypeDef]
    ) -> ListRegexMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_regex_match_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_regex_match_sets)
        """

    def list_regex_pattern_sets(
        self, **kwargs: Unpack[ListRegexPatternSetsRequestRequestTypeDef]
    ) -> ListRegexPatternSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_regex_pattern_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_regex_pattern_sets)
        """

    def list_resources_for_web_acl(
        self, **kwargs: Unpack[ListResourcesForWebACLRequestRequestTypeDef]
    ) -> ListResourcesForWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic Regional</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_resources_for_web_acl.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_resources_for_web_acl)
        """

    def list_rule_groups(
        self, **kwargs: Unpack[ListRuleGroupsRequestRequestTypeDef]
    ) -> ListRuleGroupsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_rule_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_rule_groups)
        """

    def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_rules)
        """

    def list_size_constraint_sets(
        self, **kwargs: Unpack[ListSizeConstraintSetsRequestRequestTypeDef]
    ) -> ListSizeConstraintSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_size_constraint_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_size_constraint_sets)
        """

    def list_sql_injection_match_sets(
        self, **kwargs: Unpack[ListSqlInjectionMatchSetsRequestRequestTypeDef]
    ) -> ListSqlInjectionMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_sql_injection_match_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_sql_injection_match_sets)
        """

    def list_subscribed_rule_groups(
        self, **kwargs: Unpack[ListSubscribedRuleGroupsRequestRequestTypeDef]
    ) -> ListSubscribedRuleGroupsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_subscribed_rule_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_subscribed_rule_groups)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_tags_for_resource)
        """

    def list_web_acls(
        self, **kwargs: Unpack[ListWebACLsRequestRequestTypeDef]
    ) -> ListWebACLsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_web_acls.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_web_acls)
        """

    def list_xss_match_sets(
        self, **kwargs: Unpack[ListXssMatchSetsRequestRequestTypeDef]
    ) -> ListXssMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/list_xss_match_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#list_xss_match_sets)
        """

    def put_logging_configuration(
        self, **kwargs: Unpack[PutLoggingConfigurationRequestRequestTypeDef]
    ) -> PutLoggingConfigurationResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/put_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#put_logging_configuration)
        """

    def put_permission_policy(
        self, **kwargs: Unpack[PutPermissionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/put_permission_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#put_permission_policy)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#untag_resource)
        """

    def update_byte_match_set(
        self, **kwargs: Unpack[UpdateByteMatchSetRequestRequestTypeDef]
    ) -> UpdateByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_byte_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_byte_match_set)
        """

    def update_geo_match_set(
        self, **kwargs: Unpack[UpdateGeoMatchSetRequestRequestTypeDef]
    ) -> UpdateGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_geo_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_geo_match_set)
        """

    def update_ip_set(
        self, **kwargs: Unpack[UpdateIPSetRequestRequestTypeDef]
    ) -> UpdateIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_ip_set)
        """

    def update_rate_based_rule(
        self, **kwargs: Unpack[UpdateRateBasedRuleRequestRequestTypeDef]
    ) -> UpdateRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_rate_based_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_rate_based_rule)
        """

    def update_regex_match_set(
        self, **kwargs: Unpack[UpdateRegexMatchSetRequestRequestTypeDef]
    ) -> UpdateRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_regex_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_regex_match_set)
        """

    def update_regex_pattern_set(
        self, **kwargs: Unpack[UpdateRegexPatternSetRequestRequestTypeDef]
    ) -> UpdateRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_regex_pattern_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_regex_pattern_set)
        """

    def update_rule(
        self, **kwargs: Unpack[UpdateRuleRequestRequestTypeDef]
    ) -> UpdateRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_rule)
        """

    def update_rule_group(
        self, **kwargs: Unpack[UpdateRuleGroupRequestRequestTypeDef]
    ) -> UpdateRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_rule_group)
        """

    def update_size_constraint_set(
        self, **kwargs: Unpack[UpdateSizeConstraintSetRequestRequestTypeDef]
    ) -> UpdateSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_size_constraint_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_size_constraint_set)
        """

    def update_sql_injection_match_set(
        self, **kwargs: Unpack[UpdateSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> UpdateSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_sql_injection_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_sql_injection_match_set)
        """

    def update_web_acl(
        self, **kwargs: Unpack[UpdateWebACLRequestRequestTypeDef]
    ) -> UpdateWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_web_acl.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_web_acl)
        """

    def update_xss_match_set(
        self, **kwargs: Unpack[UpdateXssMatchSetRequestRequestTypeDef]
    ) -> UpdateXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional/client/update_xss_match_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/client/#update_xss_match_set)
        """
