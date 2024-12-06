"""
Type annotations for waf service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_waf.client import WAFClient
    from mypy_boto3_waf.paginator import (
        GetRateBasedRuleManagedKeysPaginator,
        ListActivatedRulesInRuleGroupPaginator,
        ListByteMatchSetsPaginator,
        ListGeoMatchSetsPaginator,
        ListIPSetsPaginator,
        ListLoggingConfigurationsPaginator,
        ListRateBasedRulesPaginator,
        ListRegexMatchSetsPaginator,
        ListRegexPatternSetsPaginator,
        ListRuleGroupsPaginator,
        ListRulesPaginator,
        ListSizeConstraintSetsPaginator,
        ListSqlInjectionMatchSetsPaginator,
        ListSubscribedRuleGroupsPaginator,
        ListWebACLsPaginator,
        ListXssMatchSetsPaginator,
    )

    session = Session()
    client: WAFClient = session.client("waf")

    get_rate_based_rule_managed_keys_paginator: GetRateBasedRuleManagedKeysPaginator = client.get_paginator("get_rate_based_rule_managed_keys")
    list_activated_rules_in_rule_group_paginator: ListActivatedRulesInRuleGroupPaginator = client.get_paginator("list_activated_rules_in_rule_group")
    list_byte_match_sets_paginator: ListByteMatchSetsPaginator = client.get_paginator("list_byte_match_sets")
    list_geo_match_sets_paginator: ListGeoMatchSetsPaginator = client.get_paginator("list_geo_match_sets")
    list_ip_sets_paginator: ListIPSetsPaginator = client.get_paginator("list_ip_sets")
    list_logging_configurations_paginator: ListLoggingConfigurationsPaginator = client.get_paginator("list_logging_configurations")
    list_rate_based_rules_paginator: ListRateBasedRulesPaginator = client.get_paginator("list_rate_based_rules")
    list_regex_match_sets_paginator: ListRegexMatchSetsPaginator = client.get_paginator("list_regex_match_sets")
    list_regex_pattern_sets_paginator: ListRegexPatternSetsPaginator = client.get_paginator("list_regex_pattern_sets")
    list_rule_groups_paginator: ListRuleGroupsPaginator = client.get_paginator("list_rule_groups")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_size_constraint_sets_paginator: ListSizeConstraintSetsPaginator = client.get_paginator("list_size_constraint_sets")
    list_sql_injection_match_sets_paginator: ListSqlInjectionMatchSetsPaginator = client.get_paginator("list_sql_injection_match_sets")
    list_subscribed_rule_groups_paginator: ListSubscribedRuleGroupsPaginator = client.get_paginator("list_subscribed_rule_groups")
    list_web_acls_paginator: ListWebACLsPaginator = client.get_paginator("list_web_acls")
    list_xss_match_sets_paginator: ListXssMatchSetsPaginator = client.get_paginator("list_xss_match_sets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetRateBasedRuleManagedKeysRequestGetRateBasedRuleManagedKeysPaginateTypeDef,
    GetRateBasedRuleManagedKeysResponseTypeDef,
    ListActivatedRulesInRuleGroupRequestListActivatedRulesInRuleGroupPaginateTypeDef,
    ListActivatedRulesInRuleGroupResponseTypeDef,
    ListByteMatchSetsRequestListByteMatchSetsPaginateTypeDef,
    ListByteMatchSetsResponseTypeDef,
    ListGeoMatchSetsRequestListGeoMatchSetsPaginateTypeDef,
    ListGeoMatchSetsResponseTypeDef,
    ListIPSetsRequestListIPSetsPaginateTypeDef,
    ListIPSetsResponseTypeDef,
    ListLoggingConfigurationsRequestListLoggingConfigurationsPaginateTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRateBasedRulesRequestListRateBasedRulesPaginateTypeDef,
    ListRateBasedRulesResponseTypeDef,
    ListRegexMatchSetsRequestListRegexMatchSetsPaginateTypeDef,
    ListRegexMatchSetsResponseTypeDef,
    ListRegexPatternSetsRequestListRegexPatternSetsPaginateTypeDef,
    ListRegexPatternSetsResponseTypeDef,
    ListRuleGroupsRequestListRuleGroupsPaginateTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListSizeConstraintSetsRequestListSizeConstraintSetsPaginateTypeDef,
    ListSizeConstraintSetsResponseTypeDef,
    ListSqlInjectionMatchSetsRequestListSqlInjectionMatchSetsPaginateTypeDef,
    ListSqlInjectionMatchSetsResponseTypeDef,
    ListSubscribedRuleGroupsRequestListSubscribedRuleGroupsPaginateTypeDef,
    ListSubscribedRuleGroupsResponseTypeDef,
    ListWebACLsRequestListWebACLsPaginateTypeDef,
    ListWebACLsResponseTypeDef,
    ListXssMatchSetsRequestListXssMatchSetsPaginateTypeDef,
    ListXssMatchSetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetRateBasedRuleManagedKeysPaginator",
    "ListActivatedRulesInRuleGroupPaginator",
    "ListByteMatchSetsPaginator",
    "ListGeoMatchSetsPaginator",
    "ListIPSetsPaginator",
    "ListLoggingConfigurationsPaginator",
    "ListRateBasedRulesPaginator",
    "ListRegexMatchSetsPaginator",
    "ListRegexPatternSetsPaginator",
    "ListRuleGroupsPaginator",
    "ListRulesPaginator",
    "ListSizeConstraintSetsPaginator",
    "ListSqlInjectionMatchSetsPaginator",
    "ListSubscribedRuleGroupsPaginator",
    "ListWebACLsPaginator",
    "ListXssMatchSetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetRateBasedRuleManagedKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/GetRateBasedRuleManagedKeys.html#WAF.Paginator.GetRateBasedRuleManagedKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#getratebasedrulemanagedkeyspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetRateBasedRuleManagedKeysRequestGetRateBasedRuleManagedKeysPaginateTypeDef
        ],
    ) -> _PageIterator[GetRateBasedRuleManagedKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/GetRateBasedRuleManagedKeys.html#WAF.Paginator.GetRateBasedRuleManagedKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#getratebasedrulemanagedkeyspaginator)
        """


class ListActivatedRulesInRuleGroupPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListActivatedRulesInRuleGroup.html#WAF.Paginator.ListActivatedRulesInRuleGroup)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listactivatedrulesinrulegrouppaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListActivatedRulesInRuleGroupRequestListActivatedRulesInRuleGroupPaginateTypeDef
        ],
    ) -> _PageIterator[ListActivatedRulesInRuleGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListActivatedRulesInRuleGroup.html#WAF.Paginator.ListActivatedRulesInRuleGroup.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listactivatedrulesinrulegrouppaginator)
        """


class ListByteMatchSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListByteMatchSets.html#WAF.Paginator.ListByteMatchSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listbytematchsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListByteMatchSetsRequestListByteMatchSetsPaginateTypeDef]
    ) -> _PageIterator[ListByteMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListByteMatchSets.html#WAF.Paginator.ListByteMatchSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listbytematchsetspaginator)
        """


class ListGeoMatchSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListGeoMatchSets.html#WAF.Paginator.ListGeoMatchSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listgeomatchsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGeoMatchSetsRequestListGeoMatchSetsPaginateTypeDef]
    ) -> _PageIterator[ListGeoMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListGeoMatchSets.html#WAF.Paginator.ListGeoMatchSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listgeomatchsetspaginator)
        """


class ListIPSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListIPSets.html#WAF.Paginator.ListIPSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listipsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIPSetsRequestListIPSetsPaginateTypeDef]
    ) -> _PageIterator[ListIPSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListIPSets.html#WAF.Paginator.ListIPSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listipsetspaginator)
        """


class ListLoggingConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListLoggingConfigurations.html#WAF.Paginator.ListLoggingConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listloggingconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListLoggingConfigurationsRequestListLoggingConfigurationsPaginateTypeDef],
    ) -> _PageIterator[ListLoggingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListLoggingConfigurations.html#WAF.Paginator.ListLoggingConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listloggingconfigurationspaginator)
        """


class ListRateBasedRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRateBasedRules.html#WAF.Paginator.ListRateBasedRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listratebasedrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRateBasedRulesRequestListRateBasedRulesPaginateTypeDef]
    ) -> _PageIterator[ListRateBasedRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRateBasedRules.html#WAF.Paginator.ListRateBasedRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listratebasedrulespaginator)
        """


class ListRegexMatchSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexMatchSets.html#WAF.Paginator.ListRegexMatchSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listregexmatchsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRegexMatchSetsRequestListRegexMatchSetsPaginateTypeDef]
    ) -> _PageIterator[ListRegexMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexMatchSets.html#WAF.Paginator.ListRegexMatchSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listregexmatchsetspaginator)
        """


class ListRegexPatternSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexPatternSets.html#WAF.Paginator.ListRegexPatternSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listregexpatternsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRegexPatternSetsRequestListRegexPatternSetsPaginateTypeDef]
    ) -> _PageIterator[ListRegexPatternSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexPatternSets.html#WAF.Paginator.ListRegexPatternSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listregexpatternsetspaginator)
        """


class ListRuleGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRuleGroups.html#WAF.Paginator.ListRuleGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listrulegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRuleGroupsRequestListRuleGroupsPaginateTypeDef]
    ) -> _PageIterator[ListRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRuleGroups.html#WAF.Paginator.ListRuleGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listrulegroupspaginator)
        """


class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRules.html#WAF.Paginator.ListRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRules.html#WAF.Paginator.ListRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listrulespaginator)
        """


class ListSizeConstraintSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSizeConstraintSets.html#WAF.Paginator.ListSizeConstraintSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listsizeconstraintsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSizeConstraintSetsRequestListSizeConstraintSetsPaginateTypeDef]
    ) -> _PageIterator[ListSizeConstraintSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSizeConstraintSets.html#WAF.Paginator.ListSizeConstraintSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listsizeconstraintsetspaginator)
        """


class ListSqlInjectionMatchSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSqlInjectionMatchSets.html#WAF.Paginator.ListSqlInjectionMatchSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listsqlinjectionmatchsetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSqlInjectionMatchSetsRequestListSqlInjectionMatchSetsPaginateTypeDef],
    ) -> _PageIterator[ListSqlInjectionMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSqlInjectionMatchSets.html#WAF.Paginator.ListSqlInjectionMatchSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listsqlinjectionmatchsetspaginator)
        """


class ListSubscribedRuleGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSubscribedRuleGroups.html#WAF.Paginator.ListSubscribedRuleGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listsubscribedrulegroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSubscribedRuleGroupsRequestListSubscribedRuleGroupsPaginateTypeDef],
    ) -> _PageIterator[ListSubscribedRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSubscribedRuleGroups.html#WAF.Paginator.ListSubscribedRuleGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listsubscribedrulegroupspaginator)
        """


class ListWebACLsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListWebACLs.html#WAF.Paginator.ListWebACLs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listwebaclspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWebACLsRequestListWebACLsPaginateTypeDef]
    ) -> _PageIterator[ListWebACLsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListWebACLs.html#WAF.Paginator.ListWebACLs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listwebaclspaginator)
        """


class ListXssMatchSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListXssMatchSets.html#WAF.Paginator.ListXssMatchSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listxssmatchsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListXssMatchSetsRequestListXssMatchSetsPaginateTypeDef]
    ) -> _PageIterator[ListXssMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListXssMatchSets.html#WAF.Paginator.ListXssMatchSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf/paginators/#listxssmatchsetspaginator)
        """
