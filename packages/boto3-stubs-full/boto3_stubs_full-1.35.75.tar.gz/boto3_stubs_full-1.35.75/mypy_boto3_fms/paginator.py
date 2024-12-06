"""
Type annotations for fms service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_fms.client import FMSClient
    from mypy_boto3_fms.paginator import (
        ListAdminAccountsForOrganizationPaginator,
        ListAdminsManagingAccountPaginator,
        ListAppsListsPaginator,
        ListComplianceStatusPaginator,
        ListMemberAccountsPaginator,
        ListPoliciesPaginator,
        ListProtocolsListsPaginator,
        ListThirdPartyFirewallFirewallPoliciesPaginator,
    )

    session = Session()
    client: FMSClient = session.client("fms")

    list_admin_accounts_for_organization_paginator: ListAdminAccountsForOrganizationPaginator = client.get_paginator("list_admin_accounts_for_organization")
    list_admins_managing_account_paginator: ListAdminsManagingAccountPaginator = client.get_paginator("list_admins_managing_account")
    list_apps_lists_paginator: ListAppsListsPaginator = client.get_paginator("list_apps_lists")
    list_compliance_status_paginator: ListComplianceStatusPaginator = client.get_paginator("list_compliance_status")
    list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_protocols_lists_paginator: ListProtocolsListsPaginator = client.get_paginator("list_protocols_lists")
    list_third_party_firewall_firewall_policies_paginator: ListThirdPartyFirewallFirewallPoliciesPaginator = client.get_paginator("list_third_party_firewall_firewall_policies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAdminAccountsForOrganizationRequestListAdminAccountsForOrganizationPaginateTypeDef,
    ListAdminAccountsForOrganizationResponseTypeDef,
    ListAdminsManagingAccountRequestListAdminsManagingAccountPaginateTypeDef,
    ListAdminsManagingAccountResponseTypeDef,
    ListAppsListsRequestListAppsListsPaginateTypeDef,
    ListAppsListsResponseTypeDef,
    ListComplianceStatusRequestListComplianceStatusPaginateTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListMemberAccountsRequestListMemberAccountsPaginateTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesRequestListPoliciesPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsRequestListProtocolsListsPaginateTypeDef,
    ListProtocolsListsResponseTypeDef,
    ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef,
    ListThirdPartyFirewallFirewallPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAdminAccountsForOrganizationPaginator",
    "ListAdminsManagingAccountPaginator",
    "ListAppsListsPaginator",
    "ListComplianceStatusPaginator",
    "ListMemberAccountsPaginator",
    "ListPoliciesPaginator",
    "ListProtocolsListsPaginator",
    "ListThirdPartyFirewallFirewallPoliciesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAdminAccountsForOrganizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminAccountsForOrganization.html#FMS.Paginator.ListAdminAccountsForOrganization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listadminaccountsfororganizationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAdminAccountsForOrganizationRequestListAdminAccountsForOrganizationPaginateTypeDef
        ],
    ) -> _PageIterator[ListAdminAccountsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminAccountsForOrganization.html#FMS.Paginator.ListAdminAccountsForOrganization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listadminaccountsfororganizationpaginator)
        """


class ListAdminsManagingAccountPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminsManagingAccount.html#FMS.Paginator.ListAdminsManagingAccount)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listadminsmanagingaccountpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAdminsManagingAccountRequestListAdminsManagingAccountPaginateTypeDef],
    ) -> _PageIterator[ListAdminsManagingAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminsManagingAccount.html#FMS.Paginator.ListAdminsManagingAccount.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listadminsmanagingaccountpaginator)
        """


class ListAppsListsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAppsLists.html#FMS.Paginator.ListAppsLists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listappslistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppsListsRequestListAppsListsPaginateTypeDef]
    ) -> _PageIterator[ListAppsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAppsLists.html#FMS.Paginator.ListAppsLists.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listappslistspaginator)
        """


class ListComplianceStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListComplianceStatus.html#FMS.Paginator.ListComplianceStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listcompliancestatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComplianceStatusRequestListComplianceStatusPaginateTypeDef]
    ) -> _PageIterator[ListComplianceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListComplianceStatus.html#FMS.Paginator.ListComplianceStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listcompliancestatuspaginator)
        """


class ListMemberAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListMemberAccounts.html#FMS.Paginator.ListMemberAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listmemberaccountspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMemberAccountsRequestListMemberAccountsPaginateTypeDef]
    ) -> _PageIterator[ListMemberAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListMemberAccounts.html#FMS.Paginator.ListMemberAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listmemberaccountspaginator)
        """


class ListPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListPolicies.html#FMS.Paginator.ListPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listpoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPoliciesRequestListPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListPolicies.html#FMS.Paginator.ListPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listpoliciespaginator)
        """


class ListProtocolsListsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListProtocolsLists.html#FMS.Paginator.ListProtocolsLists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listprotocolslistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProtocolsListsRequestListProtocolsListsPaginateTypeDef]
    ) -> _PageIterator[ListProtocolsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListProtocolsLists.html#FMS.Paginator.ListProtocolsLists.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listprotocolslistspaginator)
        """


class ListThirdPartyFirewallFirewallPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListThirdPartyFirewallFirewallPolicies.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef
        ],
    ) -> _PageIterator[ListThirdPartyFirewallFirewallPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListThirdPartyFirewallFirewallPolicies.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
        """
