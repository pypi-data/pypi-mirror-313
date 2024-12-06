"""
Type annotations for route53resolver service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53resolver.client import Route53ResolverClient

    session = Session()
    client: Route53ResolverClient = session.client("route53resolver")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
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
from .type_defs import (
    AssociateFirewallRuleGroupRequestRequestTypeDef,
    AssociateFirewallRuleGroupResponseTypeDef,
    AssociateResolverEndpointIpAddressRequestRequestTypeDef,
    AssociateResolverEndpointIpAddressResponseTypeDef,
    AssociateResolverQueryLogConfigRequestRequestTypeDef,
    AssociateResolverQueryLogConfigResponseTypeDef,
    AssociateResolverRuleRequestRequestTypeDef,
    AssociateResolverRuleResponseTypeDef,
    CreateFirewallDomainListRequestRequestTypeDef,
    CreateFirewallDomainListResponseTypeDef,
    CreateFirewallRuleGroupRequestRequestTypeDef,
    CreateFirewallRuleGroupResponseTypeDef,
    CreateFirewallRuleRequestRequestTypeDef,
    CreateFirewallRuleResponseTypeDef,
    CreateOutpostResolverRequestRequestTypeDef,
    CreateOutpostResolverResponseTypeDef,
    CreateResolverEndpointRequestRequestTypeDef,
    CreateResolverEndpointResponseTypeDef,
    CreateResolverQueryLogConfigRequestRequestTypeDef,
    CreateResolverQueryLogConfigResponseTypeDef,
    CreateResolverRuleRequestRequestTypeDef,
    CreateResolverRuleResponseTypeDef,
    DeleteFirewallDomainListRequestRequestTypeDef,
    DeleteFirewallDomainListResponseTypeDef,
    DeleteFirewallRuleGroupRequestRequestTypeDef,
    DeleteFirewallRuleGroupResponseTypeDef,
    DeleteFirewallRuleRequestRequestTypeDef,
    DeleteFirewallRuleResponseTypeDef,
    DeleteOutpostResolverRequestRequestTypeDef,
    DeleteOutpostResolverResponseTypeDef,
    DeleteResolverEndpointRequestRequestTypeDef,
    DeleteResolverEndpointResponseTypeDef,
    DeleteResolverQueryLogConfigRequestRequestTypeDef,
    DeleteResolverQueryLogConfigResponseTypeDef,
    DeleteResolverRuleRequestRequestTypeDef,
    DeleteResolverRuleResponseTypeDef,
    DisassociateFirewallRuleGroupRequestRequestTypeDef,
    DisassociateFirewallRuleGroupResponseTypeDef,
    DisassociateResolverEndpointIpAddressRequestRequestTypeDef,
    DisassociateResolverEndpointIpAddressResponseTypeDef,
    DisassociateResolverQueryLogConfigRequestRequestTypeDef,
    DisassociateResolverQueryLogConfigResponseTypeDef,
    DisassociateResolverRuleRequestRequestTypeDef,
    DisassociateResolverRuleResponseTypeDef,
    GetFirewallConfigRequestRequestTypeDef,
    GetFirewallConfigResponseTypeDef,
    GetFirewallDomainListRequestRequestTypeDef,
    GetFirewallDomainListResponseTypeDef,
    GetFirewallRuleGroupAssociationRequestRequestTypeDef,
    GetFirewallRuleGroupAssociationResponseTypeDef,
    GetFirewallRuleGroupPolicyRequestRequestTypeDef,
    GetFirewallRuleGroupPolicyResponseTypeDef,
    GetFirewallRuleGroupRequestRequestTypeDef,
    GetFirewallRuleGroupResponseTypeDef,
    GetOutpostResolverRequestRequestTypeDef,
    GetOutpostResolverResponseTypeDef,
    GetResolverConfigRequestRequestTypeDef,
    GetResolverConfigResponseTypeDef,
    GetResolverDnssecConfigRequestRequestTypeDef,
    GetResolverDnssecConfigResponseTypeDef,
    GetResolverEndpointRequestRequestTypeDef,
    GetResolverEndpointResponseTypeDef,
    GetResolverQueryLogConfigAssociationRequestRequestTypeDef,
    GetResolverQueryLogConfigAssociationResponseTypeDef,
    GetResolverQueryLogConfigPolicyRequestRequestTypeDef,
    GetResolverQueryLogConfigPolicyResponseTypeDef,
    GetResolverQueryLogConfigRequestRequestTypeDef,
    GetResolverQueryLogConfigResponseTypeDef,
    GetResolverRuleAssociationRequestRequestTypeDef,
    GetResolverRuleAssociationResponseTypeDef,
    GetResolverRulePolicyRequestRequestTypeDef,
    GetResolverRulePolicyResponseTypeDef,
    GetResolverRuleRequestRequestTypeDef,
    GetResolverRuleResponseTypeDef,
    ImportFirewallDomainsRequestRequestTypeDef,
    ImportFirewallDomainsResponseTypeDef,
    ListFirewallConfigsRequestRequestTypeDef,
    ListFirewallConfigsResponseTypeDef,
    ListFirewallDomainListsRequestRequestTypeDef,
    ListFirewallDomainListsResponseTypeDef,
    ListFirewallDomainsRequestRequestTypeDef,
    ListFirewallDomainsResponseTypeDef,
    ListFirewallRuleGroupAssociationsRequestRequestTypeDef,
    ListFirewallRuleGroupAssociationsResponseTypeDef,
    ListFirewallRuleGroupsRequestRequestTypeDef,
    ListFirewallRuleGroupsResponseTypeDef,
    ListFirewallRulesRequestRequestTypeDef,
    ListFirewallRulesResponseTypeDef,
    ListOutpostResolversRequestRequestTypeDef,
    ListOutpostResolversResponseTypeDef,
    ListResolverConfigsRequestRequestTypeDef,
    ListResolverConfigsResponseTypeDef,
    ListResolverDnssecConfigsRequestRequestTypeDef,
    ListResolverDnssecConfigsResponseTypeDef,
    ListResolverEndpointIpAddressesRequestRequestTypeDef,
    ListResolverEndpointIpAddressesResponseTypeDef,
    ListResolverEndpointsRequestRequestTypeDef,
    ListResolverEndpointsResponseTypeDef,
    ListResolverQueryLogConfigAssociationsRequestRequestTypeDef,
    ListResolverQueryLogConfigAssociationsResponseTypeDef,
    ListResolverQueryLogConfigsRequestRequestTypeDef,
    ListResolverQueryLogConfigsResponseTypeDef,
    ListResolverRuleAssociationsRequestRequestTypeDef,
    ListResolverRuleAssociationsResponseTypeDef,
    ListResolverRulesRequestRequestTypeDef,
    ListResolverRulesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutFirewallRuleGroupPolicyRequestRequestTypeDef,
    PutFirewallRuleGroupPolicyResponseTypeDef,
    PutResolverQueryLogConfigPolicyRequestRequestTypeDef,
    PutResolverQueryLogConfigPolicyResponseTypeDef,
    PutResolverRulePolicyRequestRequestTypeDef,
    PutResolverRulePolicyResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateFirewallConfigRequestRequestTypeDef,
    UpdateFirewallConfigResponseTypeDef,
    UpdateFirewallDomainsRequestRequestTypeDef,
    UpdateFirewallDomainsResponseTypeDef,
    UpdateFirewallRuleGroupAssociationRequestRequestTypeDef,
    UpdateFirewallRuleGroupAssociationResponseTypeDef,
    UpdateFirewallRuleRequestRequestTypeDef,
    UpdateFirewallRuleResponseTypeDef,
    UpdateOutpostResolverRequestRequestTypeDef,
    UpdateOutpostResolverResponseTypeDef,
    UpdateResolverConfigRequestRequestTypeDef,
    UpdateResolverConfigResponseTypeDef,
    UpdateResolverDnssecConfigRequestRequestTypeDef,
    UpdateResolverDnssecConfigResponseTypeDef,
    UpdateResolverEndpointRequestRequestTypeDef,
    UpdateResolverEndpointResponseTypeDef,
    UpdateResolverRuleRequestRequestTypeDef,
    UpdateResolverRuleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("Route53ResolverClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPolicyDocument: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnknownResourceException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Route53ResolverClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53ResolverClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#close)
        """

    def associate_firewall_rule_group(
        self, **kwargs: Unpack[AssociateFirewallRuleGroupRequestRequestTypeDef]
    ) -> AssociateFirewallRuleGroupResponseTypeDef:
        """
        Associates a <a>FirewallRuleGroup</a> with a VPC, to provide DNS filtering for
        the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/associate_firewall_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_firewall_rule_group)
        """

    def associate_resolver_endpoint_ip_address(
        self, **kwargs: Unpack[AssociateResolverEndpointIpAddressRequestRequestTypeDef]
    ) -> AssociateResolverEndpointIpAddressResponseTypeDef:
        """
        Adds IP addresses to an inbound or an outbound Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/associate_resolver_endpoint_ip_address.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_resolver_endpoint_ip_address)
        """

    def associate_resolver_query_log_config(
        self, **kwargs: Unpack[AssociateResolverQueryLogConfigRequestRequestTypeDef]
    ) -> AssociateResolverQueryLogConfigResponseTypeDef:
        """
        Associates an Amazon VPC with a specified query logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/associate_resolver_query_log_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_resolver_query_log_config)
        """

    def associate_resolver_rule(
        self, **kwargs: Unpack[AssociateResolverRuleRequestRequestTypeDef]
    ) -> AssociateResolverRuleResponseTypeDef:
        """
        Associates a Resolver rule with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/associate_resolver_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_resolver_rule)
        """

    def create_firewall_domain_list(
        self, **kwargs: Unpack[CreateFirewallDomainListRequestRequestTypeDef]
    ) -> CreateFirewallDomainListResponseTypeDef:
        """
        Creates an empty firewall domain list for use in DNS Firewall rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/create_firewall_domain_list.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_firewall_domain_list)
        """

    def create_firewall_rule(
        self, **kwargs: Unpack[CreateFirewallRuleRequestRequestTypeDef]
    ) -> CreateFirewallRuleResponseTypeDef:
        """
        Creates a single DNS Firewall rule in the specified rule group, using the
        specified domain list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/create_firewall_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_firewall_rule)
        """

    def create_firewall_rule_group(
        self, **kwargs: Unpack[CreateFirewallRuleGroupRequestRequestTypeDef]
    ) -> CreateFirewallRuleGroupResponseTypeDef:
        """
        Creates an empty DNS Firewall rule group for filtering DNS network traffic in a
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/create_firewall_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_firewall_rule_group)
        """

    def create_outpost_resolver(
        self, **kwargs: Unpack[CreateOutpostResolverRequestRequestTypeDef]
    ) -> CreateOutpostResolverResponseTypeDef:
        """
        Creates a Route 53 Resolver on an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/create_outpost_resolver.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_outpost_resolver)
        """

    def create_resolver_endpoint(
        self, **kwargs: Unpack[CreateResolverEndpointRequestRequestTypeDef]
    ) -> CreateResolverEndpointResponseTypeDef:
        """
        Creates a Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/create_resolver_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_resolver_endpoint)
        """

    def create_resolver_query_log_config(
        self, **kwargs: Unpack[CreateResolverQueryLogConfigRequestRequestTypeDef]
    ) -> CreateResolverQueryLogConfigResponseTypeDef:
        """
        Creates a Resolver query logging configuration, which defines where you want
        Resolver to save DNS query logs that originate in your VPCs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/create_resolver_query_log_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_resolver_query_log_config)
        """

    def create_resolver_rule(
        self, **kwargs: Unpack[CreateResolverRuleRequestRequestTypeDef]
    ) -> CreateResolverRuleResponseTypeDef:
        """
        For DNS queries that originate in your VPCs, specifies which Resolver endpoint
        the queries pass through, one domain name that you want to forward to your
        network, and the IP addresses of the DNS resolvers in your network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/create_resolver_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_resolver_rule)
        """

    def delete_firewall_domain_list(
        self, **kwargs: Unpack[DeleteFirewallDomainListRequestRequestTypeDef]
    ) -> DeleteFirewallDomainListResponseTypeDef:
        """
        Deletes the specified domain list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/delete_firewall_domain_list.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_firewall_domain_list)
        """

    def delete_firewall_rule(
        self, **kwargs: Unpack[DeleteFirewallRuleRequestRequestTypeDef]
    ) -> DeleteFirewallRuleResponseTypeDef:
        """
        Deletes the specified firewall rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/delete_firewall_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_firewall_rule)
        """

    def delete_firewall_rule_group(
        self, **kwargs: Unpack[DeleteFirewallRuleGroupRequestRequestTypeDef]
    ) -> DeleteFirewallRuleGroupResponseTypeDef:
        """
        Deletes the specified firewall rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/delete_firewall_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_firewall_rule_group)
        """

    def delete_outpost_resolver(
        self, **kwargs: Unpack[DeleteOutpostResolverRequestRequestTypeDef]
    ) -> DeleteOutpostResolverResponseTypeDef:
        """
        Deletes a Resolver on the Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/delete_outpost_resolver.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_outpost_resolver)
        """

    def delete_resolver_endpoint(
        self, **kwargs: Unpack[DeleteResolverEndpointRequestRequestTypeDef]
    ) -> DeleteResolverEndpointResponseTypeDef:
        """
        Deletes a Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/delete_resolver_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_resolver_endpoint)
        """

    def delete_resolver_query_log_config(
        self, **kwargs: Unpack[DeleteResolverQueryLogConfigRequestRequestTypeDef]
    ) -> DeleteResolverQueryLogConfigResponseTypeDef:
        """
        Deletes a query logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/delete_resolver_query_log_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_resolver_query_log_config)
        """

    def delete_resolver_rule(
        self, **kwargs: Unpack[DeleteResolverRuleRequestRequestTypeDef]
    ) -> DeleteResolverRuleResponseTypeDef:
        """
        Deletes a Resolver rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/delete_resolver_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_resolver_rule)
        """

    def disassociate_firewall_rule_group(
        self, **kwargs: Unpack[DisassociateFirewallRuleGroupRequestRequestTypeDef]
    ) -> DisassociateFirewallRuleGroupResponseTypeDef:
        """
        Disassociates a <a>FirewallRuleGroup</a> from a VPC, to remove DNS filtering
        from the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/disassociate_firewall_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_firewall_rule_group)
        """

    def disassociate_resolver_endpoint_ip_address(
        self, **kwargs: Unpack[DisassociateResolverEndpointIpAddressRequestRequestTypeDef]
    ) -> DisassociateResolverEndpointIpAddressResponseTypeDef:
        """
        Removes IP addresses from an inbound or an outbound Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/disassociate_resolver_endpoint_ip_address.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_resolver_endpoint_ip_address)
        """

    def disassociate_resolver_query_log_config(
        self, **kwargs: Unpack[DisassociateResolverQueryLogConfigRequestRequestTypeDef]
    ) -> DisassociateResolverQueryLogConfigResponseTypeDef:
        """
        Disassociates a VPC from a query logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/disassociate_resolver_query_log_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_resolver_query_log_config)
        """

    def disassociate_resolver_rule(
        self, **kwargs: Unpack[DisassociateResolverRuleRequestRequestTypeDef]
    ) -> DisassociateResolverRuleResponseTypeDef:
        """
        Removes the association between a specified Resolver rule and a specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/disassociate_resolver_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_resolver_rule)
        """

    def get_firewall_config(
        self, **kwargs: Unpack[GetFirewallConfigRequestRequestTypeDef]
    ) -> GetFirewallConfigResponseTypeDef:
        """
        Retrieves the configuration of the firewall behavior provided by DNS Firewall
        for a single VPC from Amazon Virtual Private Cloud (Amazon VPC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_firewall_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_config)
        """

    def get_firewall_domain_list(
        self, **kwargs: Unpack[GetFirewallDomainListRequestRequestTypeDef]
    ) -> GetFirewallDomainListResponseTypeDef:
        """
        Retrieves the specified firewall domain list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_firewall_domain_list.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_domain_list)
        """

    def get_firewall_rule_group(
        self, **kwargs: Unpack[GetFirewallRuleGroupRequestRequestTypeDef]
    ) -> GetFirewallRuleGroupResponseTypeDef:
        """
        Retrieves the specified firewall rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_firewall_rule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_rule_group)
        """

    def get_firewall_rule_group_association(
        self, **kwargs: Unpack[GetFirewallRuleGroupAssociationRequestRequestTypeDef]
    ) -> GetFirewallRuleGroupAssociationResponseTypeDef:
        """
        Retrieves a firewall rule group association, which enables DNS filtering for a
        VPC with one rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_firewall_rule_group_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_rule_group_association)
        """

    def get_firewall_rule_group_policy(
        self, **kwargs: Unpack[GetFirewallRuleGroupPolicyRequestRequestTypeDef]
    ) -> GetFirewallRuleGroupPolicyResponseTypeDef:
        """
        Returns the Identity and Access Management (Amazon Web Services IAM) policy for
        sharing the specified rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_firewall_rule_group_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_rule_group_policy)
        """

    def get_outpost_resolver(
        self, **kwargs: Unpack[GetOutpostResolverRequestRequestTypeDef]
    ) -> GetOutpostResolverResponseTypeDef:
        """
        Gets information about a specified Resolver on the Outpost, such as its
        instance count and type, name, and the current status of the Resolver.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_outpost_resolver.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_outpost_resolver)
        """

    def get_resolver_config(
        self, **kwargs: Unpack[GetResolverConfigRequestRequestTypeDef]
    ) -> GetResolverConfigResponseTypeDef:
        """
        Retrieves the behavior configuration of Route 53 Resolver behavior for a single
        VPC from Amazon Virtual Private Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_config)
        """

    def get_resolver_dnssec_config(
        self, **kwargs: Unpack[GetResolverDnssecConfigRequestRequestTypeDef]
    ) -> GetResolverDnssecConfigResponseTypeDef:
        """
        Gets DNSSEC validation information for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_dnssec_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_dnssec_config)
        """

    def get_resolver_endpoint(
        self, **kwargs: Unpack[GetResolverEndpointRequestRequestTypeDef]
    ) -> GetResolverEndpointResponseTypeDef:
        """
        Gets information about a specified Resolver endpoint, such as whether it's an
        inbound or an outbound Resolver endpoint, and the current status of the
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_endpoint)
        """

    def get_resolver_query_log_config(
        self, **kwargs: Unpack[GetResolverQueryLogConfigRequestRequestTypeDef]
    ) -> GetResolverQueryLogConfigResponseTypeDef:
        """
        Gets information about a specified Resolver query logging configuration, such
        as the number of VPCs that the configuration is logging queries for and the
        location that logs are sent to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_query_log_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_query_log_config)
        """

    def get_resolver_query_log_config_association(
        self, **kwargs: Unpack[GetResolverQueryLogConfigAssociationRequestRequestTypeDef]
    ) -> GetResolverQueryLogConfigAssociationResponseTypeDef:
        """
        Gets information about a specified association between a Resolver query logging
        configuration and an Amazon VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_query_log_config_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_query_log_config_association)
        """

    def get_resolver_query_log_config_policy(
        self, **kwargs: Unpack[GetResolverQueryLogConfigPolicyRequestRequestTypeDef]
    ) -> GetResolverQueryLogConfigPolicyResponseTypeDef:
        """
        Gets information about a query logging policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_query_log_config_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_query_log_config_policy)
        """

    def get_resolver_rule(
        self, **kwargs: Unpack[GetResolverRuleRequestRequestTypeDef]
    ) -> GetResolverRuleResponseTypeDef:
        """
        Gets information about a specified Resolver rule, such as the domain name that
        the rule forwards DNS queries for and the ID of the outbound Resolver endpoint
        that the rule is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_rule)
        """

    def get_resolver_rule_association(
        self, **kwargs: Unpack[GetResolverRuleAssociationRequestRequestTypeDef]
    ) -> GetResolverRuleAssociationResponseTypeDef:
        """
        Gets information about an association between a specified Resolver rule and a
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_rule_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_rule_association)
        """

    def get_resolver_rule_policy(
        self, **kwargs: Unpack[GetResolverRulePolicyRequestRequestTypeDef]
    ) -> GetResolverRulePolicyResponseTypeDef:
        """
        Gets information about the Resolver rule policy for a specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_resolver_rule_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_rule_policy)
        """

    def import_firewall_domains(
        self, **kwargs: Unpack[ImportFirewallDomainsRequestRequestTypeDef]
    ) -> ImportFirewallDomainsResponseTypeDef:
        """
        Imports domain names from a file into a domain list, for use in a DNS firewall
        rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/import_firewall_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#import_firewall_domains)
        """

    def list_firewall_configs(
        self, **kwargs: Unpack[ListFirewallConfigsRequestRequestTypeDef]
    ) -> ListFirewallConfigsResponseTypeDef:
        """
        Retrieves the firewall configurations that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_firewall_configs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_configs)
        """

    def list_firewall_domain_lists(
        self, **kwargs: Unpack[ListFirewallDomainListsRequestRequestTypeDef]
    ) -> ListFirewallDomainListsResponseTypeDef:
        """
        Retrieves the firewall domain lists that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_firewall_domain_lists.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_domain_lists)
        """

    def list_firewall_domains(
        self, **kwargs: Unpack[ListFirewallDomainsRequestRequestTypeDef]
    ) -> ListFirewallDomainsResponseTypeDef:
        """
        Retrieves the domains that you have defined for the specified firewall domain
        list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_firewall_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_domains)
        """

    def list_firewall_rule_group_associations(
        self, **kwargs: Unpack[ListFirewallRuleGroupAssociationsRequestRequestTypeDef]
    ) -> ListFirewallRuleGroupAssociationsResponseTypeDef:
        """
        Retrieves the firewall rule group associations that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_firewall_rule_group_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_rule_group_associations)
        """

    def list_firewall_rule_groups(
        self, **kwargs: Unpack[ListFirewallRuleGroupsRequestRequestTypeDef]
    ) -> ListFirewallRuleGroupsResponseTypeDef:
        """
        Retrieves the minimal high-level information for the rule groups that you have
        defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_firewall_rule_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_rule_groups)
        """

    def list_firewall_rules(
        self, **kwargs: Unpack[ListFirewallRulesRequestRequestTypeDef]
    ) -> ListFirewallRulesResponseTypeDef:
        """
        Retrieves the firewall rules that you have defined for the specified firewall
        rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_firewall_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_rules)
        """

    def list_outpost_resolvers(
        self, **kwargs: Unpack[ListOutpostResolversRequestRequestTypeDef]
    ) -> ListOutpostResolversResponseTypeDef:
        """
        Lists all the Resolvers on Outposts that were created using the current Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_outpost_resolvers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_outpost_resolvers)
        """

    def list_resolver_configs(
        self, **kwargs: Unpack[ListResolverConfigsRequestRequestTypeDef]
    ) -> ListResolverConfigsResponseTypeDef:
        """
        Retrieves the Resolver configurations that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_configs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_configs)
        """

    def list_resolver_dnssec_configs(
        self, **kwargs: Unpack[ListResolverDnssecConfigsRequestRequestTypeDef]
    ) -> ListResolverDnssecConfigsResponseTypeDef:
        """
        Lists the configurations for DNSSEC validation that are associated with the
        current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_dnssec_configs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_dnssec_configs)
        """

    def list_resolver_endpoint_ip_addresses(
        self, **kwargs: Unpack[ListResolverEndpointIpAddressesRequestRequestTypeDef]
    ) -> ListResolverEndpointIpAddressesResponseTypeDef:
        """
        Gets the IP addresses for a specified Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_endpoint_ip_addresses.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_endpoint_ip_addresses)
        """

    def list_resolver_endpoints(
        self, **kwargs: Unpack[ListResolverEndpointsRequestRequestTypeDef]
    ) -> ListResolverEndpointsResponseTypeDef:
        """
        Lists all the Resolver endpoints that were created using the current Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_endpoints)
        """

    def list_resolver_query_log_config_associations(
        self, **kwargs: Unpack[ListResolverQueryLogConfigAssociationsRequestRequestTypeDef]
    ) -> ListResolverQueryLogConfigAssociationsResponseTypeDef:
        """
        Lists information about associations between Amazon VPCs and query logging
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_query_log_config_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_query_log_config_associations)
        """

    def list_resolver_query_log_configs(
        self, **kwargs: Unpack[ListResolverQueryLogConfigsRequestRequestTypeDef]
    ) -> ListResolverQueryLogConfigsResponseTypeDef:
        """
        Lists information about the specified query logging configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_query_log_configs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_query_log_configs)
        """

    def list_resolver_rule_associations(
        self, **kwargs: Unpack[ListResolverRuleAssociationsRequestRequestTypeDef]
    ) -> ListResolverRuleAssociationsResponseTypeDef:
        """
        Lists the associations that were created between Resolver rules and VPCs using
        the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_rule_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_rule_associations)
        """

    def list_resolver_rules(
        self, **kwargs: Unpack[ListResolverRulesRequestRequestTypeDef]
    ) -> ListResolverRulesResponseTypeDef:
        """
        Lists the Resolver rules that were created using the current Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_resolver_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_rules)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that you associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_tags_for_resource)
        """

    def put_firewall_rule_group_policy(
        self, **kwargs: Unpack[PutFirewallRuleGroupPolicyRequestRequestTypeDef]
    ) -> PutFirewallRuleGroupPolicyResponseTypeDef:
        """
        Attaches an Identity and Access Management (Amazon Web Services IAM) policy for
        sharing the rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/put_firewall_rule_group_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#put_firewall_rule_group_policy)
        """

    def put_resolver_query_log_config_policy(
        self, **kwargs: Unpack[PutResolverQueryLogConfigPolicyRequestRequestTypeDef]
    ) -> PutResolverQueryLogConfigPolicyResponseTypeDef:
        """
        Specifies an Amazon Web Services account that you want to share a query logging
        configuration with, the query logging configuration that you want to share, and
        the operations that you want the account to be able to perform on the
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/put_resolver_query_log_config_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#put_resolver_query_log_config_policy)
        """

    def put_resolver_rule_policy(
        self, **kwargs: Unpack[PutResolverRulePolicyRequestRequestTypeDef]
    ) -> PutResolverRulePolicyResponseTypeDef:
        """
        Specifies an Amazon Web Services rule that you want to share with another
        account, the account that you want to share the rule with, and the operations
        that you want the account to be able to perform on the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/put_resolver_rule_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#put_resolver_rule_policy)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#untag_resource)
        """

    def update_firewall_config(
        self, **kwargs: Unpack[UpdateFirewallConfigRequestRequestTypeDef]
    ) -> UpdateFirewallConfigResponseTypeDef:
        """
        Updates the configuration of the firewall behavior provided by DNS Firewall for
        a single VPC from Amazon Virtual Private Cloud (Amazon VPC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_firewall_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_config)
        """

    def update_firewall_domains(
        self, **kwargs: Unpack[UpdateFirewallDomainsRequestRequestTypeDef]
    ) -> UpdateFirewallDomainsResponseTypeDef:
        """
        Updates the firewall domain list from an array of domain specifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_firewall_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_domains)
        """

    def update_firewall_rule(
        self, **kwargs: Unpack[UpdateFirewallRuleRequestRequestTypeDef]
    ) -> UpdateFirewallRuleResponseTypeDef:
        """
        Updates the specified firewall rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_firewall_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_rule)
        """

    def update_firewall_rule_group_association(
        self, **kwargs: Unpack[UpdateFirewallRuleGroupAssociationRequestRequestTypeDef]
    ) -> UpdateFirewallRuleGroupAssociationResponseTypeDef:
        """
        Changes the association of a <a>FirewallRuleGroup</a> with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_firewall_rule_group_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_rule_group_association)
        """

    def update_outpost_resolver(
        self, **kwargs: Unpack[UpdateOutpostResolverRequestRequestTypeDef]
    ) -> UpdateOutpostResolverResponseTypeDef:
        """
        You can use <code>UpdateOutpostResolver</code> to update the instance count,
        type, or name of a Resolver on an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_outpost_resolver.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_outpost_resolver)
        """

    def update_resolver_config(
        self, **kwargs: Unpack[UpdateResolverConfigRequestRequestTypeDef]
    ) -> UpdateResolverConfigResponseTypeDef:
        """
        Updates the behavior configuration of Route 53 Resolver behavior for a single
        VPC from Amazon Virtual Private Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_resolver_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_config)
        """

    def update_resolver_dnssec_config(
        self, **kwargs: Unpack[UpdateResolverDnssecConfigRequestRequestTypeDef]
    ) -> UpdateResolverDnssecConfigResponseTypeDef:
        """
        Updates an existing DNSSEC validation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_resolver_dnssec_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_dnssec_config)
        """

    def update_resolver_endpoint(
        self, **kwargs: Unpack[UpdateResolverEndpointRequestRequestTypeDef]
    ) -> UpdateResolverEndpointResponseTypeDef:
        """
        Updates the name, or endpoint type for an inbound or an outbound Resolver
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_resolver_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_endpoint)
        """

    def update_resolver_rule(
        self, **kwargs: Unpack[UpdateResolverRuleRequestRequestTypeDef]
    ) -> UpdateResolverRuleResponseTypeDef:
        """
        Updates settings for a specified Resolver rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/update_resolver_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_rule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_configs"]
    ) -> ListFirewallConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_domain_lists"]
    ) -> ListFirewallDomainListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_domains"]
    ) -> ListFirewallDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_rule_group_associations"]
    ) -> ListFirewallRuleGroupAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_rule_groups"]
    ) -> ListFirewallRuleGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_rules"]
    ) -> ListFirewallRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_outpost_resolvers"]
    ) -> ListOutpostResolversPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_configs"]
    ) -> ListResolverConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_dnssec_configs"]
    ) -> ListResolverDnssecConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_endpoint_ip_addresses"]
    ) -> ListResolverEndpointIpAddressesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_endpoints"]
    ) -> ListResolverEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_query_log_config_associations"]
    ) -> ListResolverQueryLogConfigAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_query_log_configs"]
    ) -> ListResolverQueryLogConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_rule_associations"]
    ) -> ListResolverRuleAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_rules"]
    ) -> ListResolverRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """
