"""
Type annotations for route53resolver service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53resolver.client import Route53ResolverClient
    from mypy_boto3_route53resolver.paginator import (
        ListFirewallConfigsPaginator,
        ListFirewallDomainListsPaginator,
        ListFirewallDomainsPaginator,
        ListFirewallRuleGroupAssociationsPaginator,
        ListFirewallRuleGroupsPaginator,
        ListFirewallRulesPaginator,
        ListOutpostResolversPaginator,
        ListResolverConfigsPaginator,
        ListResolverDnssecConfigsPaginator,
        ListResolverEndpointIpAddressesPaginator,
        ListResolverEndpointsPaginator,
        ListResolverQueryLogConfigAssociationsPaginator,
        ListResolverQueryLogConfigsPaginator,
        ListResolverRuleAssociationsPaginator,
        ListResolverRulesPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: Route53ResolverClient = session.client("route53resolver")

    list_firewall_configs_paginator: ListFirewallConfigsPaginator = client.get_paginator("list_firewall_configs")
    list_firewall_domain_lists_paginator: ListFirewallDomainListsPaginator = client.get_paginator("list_firewall_domain_lists")
    list_firewall_domains_paginator: ListFirewallDomainsPaginator = client.get_paginator("list_firewall_domains")
    list_firewall_rule_group_associations_paginator: ListFirewallRuleGroupAssociationsPaginator = client.get_paginator("list_firewall_rule_group_associations")
    list_firewall_rule_groups_paginator: ListFirewallRuleGroupsPaginator = client.get_paginator("list_firewall_rule_groups")
    list_firewall_rules_paginator: ListFirewallRulesPaginator = client.get_paginator("list_firewall_rules")
    list_outpost_resolvers_paginator: ListOutpostResolversPaginator = client.get_paginator("list_outpost_resolvers")
    list_resolver_configs_paginator: ListResolverConfigsPaginator = client.get_paginator("list_resolver_configs")
    list_resolver_dnssec_configs_paginator: ListResolverDnssecConfigsPaginator = client.get_paginator("list_resolver_dnssec_configs")
    list_resolver_endpoint_ip_addresses_paginator: ListResolverEndpointIpAddressesPaginator = client.get_paginator("list_resolver_endpoint_ip_addresses")
    list_resolver_endpoints_paginator: ListResolverEndpointsPaginator = client.get_paginator("list_resolver_endpoints")
    list_resolver_query_log_config_associations_paginator: ListResolverQueryLogConfigAssociationsPaginator = client.get_paginator("list_resolver_query_log_config_associations")
    list_resolver_query_log_configs_paginator: ListResolverQueryLogConfigsPaginator = client.get_paginator("list_resolver_query_log_configs")
    list_resolver_rule_associations_paginator: ListResolverRuleAssociationsPaginator = client.get_paginator("list_resolver_rule_associations")
    list_resolver_rules_paginator: ListResolverRulesPaginator = client.get_paginator("list_resolver_rules")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef,
    ListFirewallConfigsResponseTypeDef,
    ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef,
    ListFirewallDomainListsResponseTypeDef,
    ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef,
    ListFirewallDomainsResponseTypeDef,
    ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef,
    ListFirewallRuleGroupAssociationsResponseTypeDef,
    ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef,
    ListFirewallRuleGroupsResponseTypeDef,
    ListFirewallRulesRequestListFirewallRulesPaginateTypeDef,
    ListFirewallRulesResponseTypeDef,
    ListOutpostResolversRequestListOutpostResolversPaginateTypeDef,
    ListOutpostResolversResponseTypeDef,
    ListResolverConfigsRequestListResolverConfigsPaginateTypeDef,
    ListResolverConfigsResponseTypeDef,
    ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef,
    ListResolverDnssecConfigsResponseTypeDef,
    ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef,
    ListResolverEndpointIpAddressesResponseTypeDef,
    ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef,
    ListResolverEndpointsResponseTypeDef,
    ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef,
    ListResolverQueryLogConfigAssociationsResponseTypeDef,
    ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef,
    ListResolverQueryLogConfigsResponseTypeDef,
    ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef,
    ListResolverRuleAssociationsResponseTypeDef,
    ListResolverRulesRequestListResolverRulesPaginateTypeDef,
    ListResolverRulesResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListFirewallConfigsPaginator",
    "ListFirewallDomainListsPaginator",
    "ListFirewallDomainsPaginator",
    "ListFirewallRuleGroupAssociationsPaginator",
    "ListFirewallRuleGroupsPaginator",
    "ListFirewallRulesPaginator",
    "ListOutpostResolversPaginator",
    "ListResolverConfigsPaginator",
    "ListResolverDnssecConfigsPaginator",
    "ListResolverEndpointIpAddressesPaginator",
    "ListResolverEndpointsPaginator",
    "ListResolverQueryLogConfigAssociationsPaginator",
    "ListResolverQueryLogConfigsPaginator",
    "ListResolverRuleAssociationsPaginator",
    "ListResolverRulesPaginator",
    "ListTagsForResourcePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListFirewallConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallConfigs.html#Route53Resolver.Paginator.ListFirewallConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef]
    ) -> _PageIterator[ListFirewallConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallConfigs.html#Route53Resolver.Paginator.ListFirewallConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallconfigspaginator)
        """


class ListFirewallDomainListsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomainLists.html#Route53Resolver.Paginator.ListFirewallDomainLists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainlistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef]
    ) -> _PageIterator[ListFirewallDomainListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomainLists.html#Route53Resolver.Paginator.ListFirewallDomainLists.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainlistspaginator)
        """


class ListFirewallDomainsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomains.html#Route53Resolver.Paginator.ListFirewallDomains)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef]
    ) -> _PageIterator[ListFirewallDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomains.html#Route53Resolver.Paginator.ListFirewallDomains.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainspaginator)
        """


class ListFirewallRuleGroupAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroupAssociations.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListFirewallRuleGroupAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroupAssociations.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupassociationspaginator)
        """


class ListFirewallRuleGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroups.html#Route53Resolver.Paginator.ListFirewallRuleGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef]
    ) -> _PageIterator[ListFirewallRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroups.html#Route53Resolver.Paginator.ListFirewallRuleGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupspaginator)
        """


class ListFirewallRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRules.html#Route53Resolver.Paginator.ListFirewallRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallRulesRequestListFirewallRulesPaginateTypeDef]
    ) -> _PageIterator[ListFirewallRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRules.html#Route53Resolver.Paginator.ListFirewallRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulespaginator)
        """


class ListOutpostResolversPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListOutpostResolvers.html#Route53Resolver.Paginator.ListOutpostResolvers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listoutpostresolverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOutpostResolversRequestListOutpostResolversPaginateTypeDef]
    ) -> _PageIterator[ListOutpostResolversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListOutpostResolvers.html#Route53Resolver.Paginator.ListOutpostResolvers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listoutpostresolverspaginator)
        """


class ListResolverConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverConfigs.html#Route53Resolver.Paginator.ListResolverConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolverConfigsRequestListResolverConfigsPaginateTypeDef]
    ) -> _PageIterator[ListResolverConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverConfigs.html#Route53Resolver.Paginator.ListResolverConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverconfigspaginator)
        """


class ListResolverDnssecConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverDnssecConfigs.html#Route53Resolver.Paginator.ListResolverDnssecConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverdnssecconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef],
    ) -> _PageIterator[ListResolverDnssecConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverDnssecConfigs.html#Route53Resolver.Paginator.ListResolverDnssecConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverdnssecconfigspaginator)
        """


class ListResolverEndpointIpAddressesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpointIpAddresses.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointipaddressespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef
        ],
    ) -> _PageIterator[ListResolverEndpointIpAddressesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpointIpAddresses.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointipaddressespaginator)
        """


class ListResolverEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpoints.html#Route53Resolver.Paginator.ListResolverEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListResolverEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpoints.html#Route53Resolver.Paginator.ListResolverEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointspaginator)
        """


class ListResolverQueryLogConfigAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigAssociations.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListResolverQueryLogConfigAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigAssociations.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigassociationspaginator)
        """


class ListResolverQueryLogConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigs.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef
        ],
    ) -> _PageIterator[ListResolverQueryLogConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigs.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigspaginator)
        """


class ListResolverRuleAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRuleAssociations.html#Route53Resolver.Paginator.ListResolverRuleAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverruleassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListResolverRuleAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRuleAssociations.html#Route53Resolver.Paginator.ListResolverRuleAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverruleassociationspaginator)
        """


class ListResolverRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRules.html#Route53Resolver.Paginator.ListResolverRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolverRulesRequestListResolverRulesPaginateTypeDef]
    ) -> _PageIterator[ListResolverRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRules.html#Route53Resolver.Paginator.ListResolverRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverrulespaginator)
        """


class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListTagsForResource.html#Route53Resolver.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListTagsForResource.html#Route53Resolver.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listtagsforresourcepaginator)
        """
