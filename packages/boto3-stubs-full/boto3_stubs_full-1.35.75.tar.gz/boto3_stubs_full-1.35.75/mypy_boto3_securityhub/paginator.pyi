"""
Type annotations for securityhub service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_securityhub.client import SecurityHubClient
    from mypy_boto3_securityhub.paginator import (
        DescribeActionTargetsPaginator,
        DescribeProductsPaginator,
        DescribeStandardsControlsPaginator,
        DescribeStandardsPaginator,
        GetEnabledStandardsPaginator,
        GetFindingHistoryPaginator,
        GetFindingsPaginator,
        GetInsightsPaginator,
        ListConfigurationPoliciesPaginator,
        ListConfigurationPolicyAssociationsPaginator,
        ListEnabledProductsForImportPaginator,
        ListFindingAggregatorsPaginator,
        ListInvitationsPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        ListSecurityControlDefinitionsPaginator,
        ListStandardsControlAssociationsPaginator,
    )

    session = Session()
    client: SecurityHubClient = session.client("securityhub")

    describe_action_targets_paginator: DescribeActionTargetsPaginator = client.get_paginator("describe_action_targets")
    describe_products_paginator: DescribeProductsPaginator = client.get_paginator("describe_products")
    describe_standards_controls_paginator: DescribeStandardsControlsPaginator = client.get_paginator("describe_standards_controls")
    describe_standards_paginator: DescribeStandardsPaginator = client.get_paginator("describe_standards")
    get_enabled_standards_paginator: GetEnabledStandardsPaginator = client.get_paginator("get_enabled_standards")
    get_finding_history_paginator: GetFindingHistoryPaginator = client.get_paginator("get_finding_history")
    get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
    get_insights_paginator: GetInsightsPaginator = client.get_paginator("get_insights")
    list_configuration_policies_paginator: ListConfigurationPoliciesPaginator = client.get_paginator("list_configuration_policies")
    list_configuration_policy_associations_paginator: ListConfigurationPolicyAssociationsPaginator = client.get_paginator("list_configuration_policy_associations")
    list_enabled_products_for_import_paginator: ListEnabledProductsForImportPaginator = client.get_paginator("list_enabled_products_for_import")
    list_finding_aggregators_paginator: ListFindingAggregatorsPaginator = client.get_paginator("list_finding_aggregators")
    list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
    list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
    list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
    list_security_control_definitions_paginator: ListSecurityControlDefinitionsPaginator = client.get_paginator("list_security_control_definitions")
    list_standards_control_associations_paginator: ListStandardsControlAssociationsPaginator = client.get_paginator("list_standards_control_associations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef,
    DescribeActionTargetsResponseTypeDef,
    DescribeProductsRequestDescribeProductsPaginateTypeDef,
    DescribeProductsResponseTypeDef,
    DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef,
    DescribeStandardsControlsResponseTypeDef,
    DescribeStandardsRequestDescribeStandardsPaginateTypeDef,
    DescribeStandardsResponseTypeDef,
    GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef,
    GetEnabledStandardsResponseTypeDef,
    GetFindingHistoryRequestGetFindingHistoryPaginateTypeDef,
    GetFindingHistoryResponseTypeDef,
    GetFindingsRequestGetFindingsPaginateTypeDef,
    GetFindingsResponseTypeDef,
    GetInsightsRequestGetInsightsPaginateTypeDef,
    GetInsightsResponseTypeDef,
    ListConfigurationPoliciesRequestListConfigurationPoliciesPaginateTypeDef,
    ListConfigurationPoliciesResponseTypeDef,
    ListConfigurationPolicyAssociationsRequestListConfigurationPolicyAssociationsPaginateTypeDef,
    ListConfigurationPolicyAssociationsResponseTypeDef,
    ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef,
    ListEnabledProductsForImportResponseTypeDef,
    ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef,
    ListFindingAggregatorsResponseTypeDef,
    ListInvitationsRequestListInvitationsPaginateTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersRequestListMembersPaginateTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListSecurityControlDefinitionsRequestListSecurityControlDefinitionsPaginateTypeDef,
    ListSecurityControlDefinitionsResponseTypeDef,
    ListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef,
    ListStandardsControlAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeActionTargetsPaginator",
    "DescribeProductsPaginator",
    "DescribeStandardsControlsPaginator",
    "DescribeStandardsPaginator",
    "GetEnabledStandardsPaginator",
    "GetFindingHistoryPaginator",
    "GetFindingsPaginator",
    "GetInsightsPaginator",
    "ListConfigurationPoliciesPaginator",
    "ListConfigurationPolicyAssociationsPaginator",
    "ListEnabledProductsForImportPaginator",
    "ListFindingAggregatorsPaginator",
    "ListInvitationsPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "ListSecurityControlDefinitionsPaginator",
    "ListStandardsControlAssociationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeActionTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeActionTargets.html#SecurityHub.Paginator.DescribeActionTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeactiontargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef]
    ) -> _PageIterator[DescribeActionTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeActionTargets.html#SecurityHub.Paginator.DescribeActionTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeactiontargetspaginator)
        """

class DescribeProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProducts.html#SecurityHub.Paginator.DescribeProducts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeproductspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeProductsRequestDescribeProductsPaginateTypeDef]
    ) -> _PageIterator[DescribeProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProducts.html#SecurityHub.Paginator.DescribeProducts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeproductspaginator)
        """

class DescribeStandardsControlsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandardsControls.html#SecurityHub.Paginator.DescribeStandardsControls)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardscontrolspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef],
    ) -> _PageIterator[DescribeStandardsControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandardsControls.html#SecurityHub.Paginator.DescribeStandardsControls.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardscontrolspaginator)
        """

class DescribeStandardsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandards.html#SecurityHub.Paginator.DescribeStandards)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeStandardsRequestDescribeStandardsPaginateTypeDef]
    ) -> _PageIterator[DescribeStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandards.html#SecurityHub.Paginator.DescribeStandards.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardspaginator)
        """

class GetEnabledStandardsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetEnabledStandards.html#SecurityHub.Paginator.GetEnabledStandards)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getenabledstandardspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef]
    ) -> _PageIterator[GetEnabledStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetEnabledStandards.html#SecurityHub.Paginator.GetEnabledStandards.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getenabledstandardspaginator)
        """

class GetFindingHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingHistory.html#SecurityHub.Paginator.GetFindingHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindinghistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetFindingHistoryRequestGetFindingHistoryPaginateTypeDef]
    ) -> _PageIterator[GetFindingHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingHistory.html#SecurityHub.Paginator.GetFindingHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindinghistorypaginator)
        """

class GetFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindings.html#SecurityHub.Paginator.GetFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetFindingsRequestGetFindingsPaginateTypeDef]
    ) -> _PageIterator[GetFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindings.html#SecurityHub.Paginator.GetFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindingspaginator)
        """

class GetInsightsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetInsights.html#SecurityHub.Paginator.GetInsights)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getinsightspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetInsightsRequestGetInsightsPaginateTypeDef]
    ) -> _PageIterator[GetInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetInsights.html#SecurityHub.Paginator.GetInsights.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getinsightspaginator)
        """

class ListConfigurationPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicies.html#SecurityHub.Paginator.ListConfigurationPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listconfigurationpoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListConfigurationPoliciesRequestListConfigurationPoliciesPaginateTypeDef],
    ) -> _PageIterator[ListConfigurationPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicies.html#SecurityHub.Paginator.ListConfigurationPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listconfigurationpoliciespaginator)
        """

class ListConfigurationPolicyAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicyAssociations.html#SecurityHub.Paginator.ListConfigurationPolicyAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listconfigurationpolicyassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfigurationPolicyAssociationsRequestListConfigurationPolicyAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfigurationPolicyAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicyAssociations.html#SecurityHub.Paginator.ListConfigurationPolicyAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listconfigurationpolicyassociationspaginator)
        """

class ListEnabledProductsForImportPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListEnabledProductsForImport.html#SecurityHub.Paginator.ListEnabledProductsForImport)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listenabledproductsforimportpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef
        ],
    ) -> _PageIterator[ListEnabledProductsForImportResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListEnabledProductsForImport.html#SecurityHub.Paginator.ListEnabledProductsForImport.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listenabledproductsforimportpaginator)
        """

class ListFindingAggregatorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListFindingAggregators.html#SecurityHub.Paginator.ListFindingAggregators)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listfindingaggregatorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef]
    ) -> _PageIterator[ListFindingAggregatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListFindingAggregators.html#SecurityHub.Paginator.ListFindingAggregators.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listfindingaggregatorspaginator)
        """

class ListInvitationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListInvitations.html#SecurityHub.Paginator.ListInvitations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listinvitationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInvitationsRequestListInvitationsPaginateTypeDef]
    ) -> _PageIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListInvitations.html#SecurityHub.Paginator.ListInvitations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listinvitationspaginator)
        """

class ListMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListMembers.html#SecurityHub.Paginator.ListMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMembersRequestListMembersPaginateTypeDef]
    ) -> _PageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListMembers.html#SecurityHub.Paginator.ListMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listmemberspaginator)
        """

class ListOrganizationAdminAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListOrganizationAdminAccounts.html#SecurityHub.Paginator.ListOrganizationAdminAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listorganizationadminaccountspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef
        ],
    ) -> _PageIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListOrganizationAdminAccounts.html#SecurityHub.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listorganizationadminaccountspaginator)
        """

class ListSecurityControlDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListSecurityControlDefinitions.html#SecurityHub.Paginator.ListSecurityControlDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityControlDefinitionsRequestListSecurityControlDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSecurityControlDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListSecurityControlDefinitions.html#SecurityHub.Paginator.ListSecurityControlDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
        """

class ListStandardsControlAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListStandardsControlAssociations.html#SecurityHub.Paginator.ListStandardsControlAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#liststandardscontrolassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListStandardsControlAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListStandardsControlAssociations.html#SecurityHub.Paginator.ListStandardsControlAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#liststandardscontrolassociationspaginator)
        """
