"""
Type annotations for sso-admin service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sso_admin.client import SSOAdminClient
    from mypy_boto3_sso_admin.paginator import (
        ListAccountAssignmentCreationStatusPaginator,
        ListAccountAssignmentDeletionStatusPaginator,
        ListAccountAssignmentsForPrincipalPaginator,
        ListAccountAssignmentsPaginator,
        ListAccountsForProvisionedPermissionSetPaginator,
        ListApplicationAccessScopesPaginator,
        ListApplicationAssignmentsForPrincipalPaginator,
        ListApplicationAssignmentsPaginator,
        ListApplicationAuthenticationMethodsPaginator,
        ListApplicationGrantsPaginator,
        ListApplicationProvidersPaginator,
        ListApplicationsPaginator,
        ListCustomerManagedPolicyReferencesInPermissionSetPaginator,
        ListInstancesPaginator,
        ListManagedPoliciesInPermissionSetPaginator,
        ListPermissionSetProvisioningStatusPaginator,
        ListPermissionSetsPaginator,
        ListPermissionSetsProvisionedToAccountPaginator,
        ListTagsForResourcePaginator,
        ListTrustedTokenIssuersPaginator,
    )

    session = Session()
    client: SSOAdminClient = session.client("sso-admin")

    list_account_assignment_creation_status_paginator: ListAccountAssignmentCreationStatusPaginator = client.get_paginator("list_account_assignment_creation_status")
    list_account_assignment_deletion_status_paginator: ListAccountAssignmentDeletionStatusPaginator = client.get_paginator("list_account_assignment_deletion_status")
    list_account_assignments_for_principal_paginator: ListAccountAssignmentsForPrincipalPaginator = client.get_paginator("list_account_assignments_for_principal")
    list_account_assignments_paginator: ListAccountAssignmentsPaginator = client.get_paginator("list_account_assignments")
    list_accounts_for_provisioned_permission_set_paginator: ListAccountsForProvisionedPermissionSetPaginator = client.get_paginator("list_accounts_for_provisioned_permission_set")
    list_application_access_scopes_paginator: ListApplicationAccessScopesPaginator = client.get_paginator("list_application_access_scopes")
    list_application_assignments_for_principal_paginator: ListApplicationAssignmentsForPrincipalPaginator = client.get_paginator("list_application_assignments_for_principal")
    list_application_assignments_paginator: ListApplicationAssignmentsPaginator = client.get_paginator("list_application_assignments")
    list_application_authentication_methods_paginator: ListApplicationAuthenticationMethodsPaginator = client.get_paginator("list_application_authentication_methods")
    list_application_grants_paginator: ListApplicationGrantsPaginator = client.get_paginator("list_application_grants")
    list_application_providers_paginator: ListApplicationProvidersPaginator = client.get_paginator("list_application_providers")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_customer_managed_policy_references_in_permission_set_paginator: ListCustomerManagedPolicyReferencesInPermissionSetPaginator = client.get_paginator("list_customer_managed_policy_references_in_permission_set")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_managed_policies_in_permission_set_paginator: ListManagedPoliciesInPermissionSetPaginator = client.get_paginator("list_managed_policies_in_permission_set")
    list_permission_set_provisioning_status_paginator: ListPermissionSetProvisioningStatusPaginator = client.get_paginator("list_permission_set_provisioning_status")
    list_permission_sets_paginator: ListPermissionSetsPaginator = client.get_paginator("list_permission_sets")
    list_permission_sets_provisioned_to_account_paginator: ListPermissionSetsProvisionedToAccountPaginator = client.get_paginator("list_permission_sets_provisioned_to_account")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_trusted_token_issuers_paginator: ListTrustedTokenIssuersPaginator = client.get_paginator("list_trusted_token_issuers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef,
    ListAccountAssignmentCreationStatusResponseTypeDef,
    ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef,
    ListAccountAssignmentDeletionStatusResponseTypeDef,
    ListAccountAssignmentsForPrincipalRequestListAccountAssignmentsForPrincipalPaginateTypeDef,
    ListAccountAssignmentsForPrincipalResponseTypeDef,
    ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef,
    ListAccountAssignmentsResponseTypeDef,
    ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef,
    ListAccountsForProvisionedPermissionSetResponseTypeDef,
    ListApplicationAccessScopesRequestListApplicationAccessScopesPaginateTypeDef,
    ListApplicationAccessScopesResponseTypeDef,
    ListApplicationAssignmentsForPrincipalRequestListApplicationAssignmentsForPrincipalPaginateTypeDef,
    ListApplicationAssignmentsForPrincipalResponseTypeDef,
    ListApplicationAssignmentsRequestListApplicationAssignmentsPaginateTypeDef,
    ListApplicationAssignmentsResponseTypeDef,
    ListApplicationAuthenticationMethodsRequestListApplicationAuthenticationMethodsPaginateTypeDef,
    ListApplicationAuthenticationMethodsResponseTypeDef,
    ListApplicationGrantsRequestListApplicationGrantsPaginateTypeDef,
    ListApplicationGrantsResponseTypeDef,
    ListApplicationProvidersRequestListApplicationProvidersPaginateTypeDef,
    ListApplicationProvidersResponseTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListCustomerManagedPolicyReferencesInPermissionSetRequestListCustomerManagedPolicyReferencesInPermissionSetPaginateTypeDef,
    ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef,
    ListInstancesRequestListInstancesPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef,
    ListManagedPoliciesInPermissionSetResponseTypeDef,
    ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef,
    ListPermissionSetProvisioningStatusResponseTypeDef,
    ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef,
    ListPermissionSetsProvisionedToAccountResponseTypeDef,
    ListPermissionSetsRequestListPermissionSetsPaginateTypeDef,
    ListPermissionSetsResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustedTokenIssuersRequestListTrustedTokenIssuersPaginateTypeDef,
    ListTrustedTokenIssuersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccountAssignmentCreationStatusPaginator",
    "ListAccountAssignmentDeletionStatusPaginator",
    "ListAccountAssignmentsForPrincipalPaginator",
    "ListAccountAssignmentsPaginator",
    "ListAccountsForProvisionedPermissionSetPaginator",
    "ListApplicationAccessScopesPaginator",
    "ListApplicationAssignmentsForPrincipalPaginator",
    "ListApplicationAssignmentsPaginator",
    "ListApplicationAuthenticationMethodsPaginator",
    "ListApplicationGrantsPaginator",
    "ListApplicationProvidersPaginator",
    "ListApplicationsPaginator",
    "ListCustomerManagedPolicyReferencesInPermissionSetPaginator",
    "ListInstancesPaginator",
    "ListManagedPoliciesInPermissionSetPaginator",
    "ListPermissionSetProvisioningStatusPaginator",
    "ListPermissionSetsPaginator",
    "ListPermissionSetsProvisionedToAccountPaginator",
    "ListTagsForResourcePaginator",
    "ListTrustedTokenIssuersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccountAssignmentCreationStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentCreationStatus.html#SSOAdmin.Paginator.ListAccountAssignmentCreationStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentcreationstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef
        ],
    ) -> _PageIterator[ListAccountAssignmentCreationStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentCreationStatus.html#SSOAdmin.Paginator.ListAccountAssignmentCreationStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentcreationstatuspaginator)
        """

class ListAccountAssignmentDeletionStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentDeletionStatus.html#SSOAdmin.Paginator.ListAccountAssignmentDeletionStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentdeletionstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef
        ],
    ) -> _PageIterator[ListAccountAssignmentDeletionStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentDeletionStatus.html#SSOAdmin.Paginator.ListAccountAssignmentDeletionStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentdeletionstatuspaginator)
        """

class ListAccountAssignmentsForPrincipalPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListAccountAssignmentsForPrincipal)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentsforprincipalpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAccountAssignmentsForPrincipalRequestListAccountAssignmentsForPrincipalPaginateTypeDef
        ],
    ) -> _PageIterator[ListAccountAssignmentsForPrincipalResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListAccountAssignmentsForPrincipal.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentsforprincipalpaginator)
        """

class ListAccountAssignmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignments.html#SSOAdmin.Paginator.ListAccountAssignments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef]
    ) -> _PageIterator[ListAccountAssignmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignments.html#SSOAdmin.Paginator.ListAccountAssignments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountassignmentspaginator)
        """

class ListAccountsForProvisionedPermissionSetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountsForProvisionedPermissionSet.html#SSOAdmin.Paginator.ListAccountsForProvisionedPermissionSet)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountsforprovisionedpermissionsetpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef
        ],
    ) -> _PageIterator[ListAccountsForProvisionedPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountsForProvisionedPermissionSet.html#SSOAdmin.Paginator.ListAccountsForProvisionedPermissionSet.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listaccountsforprovisionedpermissionsetpaginator)
        """

class ListApplicationAccessScopesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAccessScopes.html#SSOAdmin.Paginator.ListApplicationAccessScopes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationaccessscopespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListApplicationAccessScopesRequestListApplicationAccessScopesPaginateTypeDef
        ],
    ) -> _PageIterator[ListApplicationAccessScopesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAccessScopes.html#SSOAdmin.Paginator.ListApplicationAccessScopes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationaccessscopespaginator)
        """

class ListApplicationAssignmentsForPrincipalPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListApplicationAssignmentsForPrincipal)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationassignmentsforprincipalpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListApplicationAssignmentsForPrincipalRequestListApplicationAssignmentsForPrincipalPaginateTypeDef
        ],
    ) -> _PageIterator[ListApplicationAssignmentsForPrincipalResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListApplicationAssignmentsForPrincipal.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationassignmentsforprincipalpaginator)
        """

class ListApplicationAssignmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignments.html#SSOAdmin.Paginator.ListApplicationAssignments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationassignmentspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListApplicationAssignmentsRequestListApplicationAssignmentsPaginateTypeDef
        ],
    ) -> _PageIterator[ListApplicationAssignmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignments.html#SSOAdmin.Paginator.ListApplicationAssignments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationassignmentspaginator)
        """

class ListApplicationAuthenticationMethodsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAuthenticationMethods.html#SSOAdmin.Paginator.ListApplicationAuthenticationMethods)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationauthenticationmethodspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListApplicationAuthenticationMethodsRequestListApplicationAuthenticationMethodsPaginateTypeDef
        ],
    ) -> _PageIterator[ListApplicationAuthenticationMethodsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAuthenticationMethods.html#SSOAdmin.Paginator.ListApplicationAuthenticationMethods.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationauthenticationmethodspaginator)
        """

class ListApplicationGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationGrants.html#SSOAdmin.Paginator.ListApplicationGrants)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationgrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationGrantsRequestListApplicationGrantsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationGrants.html#SSOAdmin.Paginator.ListApplicationGrants.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationgrantspaginator)
        """

class ListApplicationProvidersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationProviders.html#SSOAdmin.Paginator.ListApplicationProviders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationproviderspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListApplicationProvidersRequestListApplicationProvidersPaginateTypeDef],
    ) -> _PageIterator[ListApplicationProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationProviders.html#SSOAdmin.Paginator.ListApplicationProviders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationproviderspaginator)
        """

class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplications.html#SSOAdmin.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplications.html#SSOAdmin.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listapplicationspaginator)
        """

class ListCustomerManagedPolicyReferencesInPermissionSetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListCustomerManagedPolicyReferencesInPermissionSet.html#SSOAdmin.Paginator.ListCustomerManagedPolicyReferencesInPermissionSet)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listcustomermanagedpolicyreferencesinpermissionsetpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCustomerManagedPolicyReferencesInPermissionSetRequestListCustomerManagedPolicyReferencesInPermissionSetPaginateTypeDef
        ],
    ) -> _PageIterator[ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListCustomerManagedPolicyReferencesInPermissionSet.html#SSOAdmin.Paginator.ListCustomerManagedPolicyReferencesInPermissionSet.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listcustomermanagedpolicyreferencesinpermissionsetpaginator)
        """

class ListInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListInstances.html#SSOAdmin.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstancesRequestListInstancesPaginateTypeDef]
    ) -> _PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListInstances.html#SSOAdmin.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listinstancespaginator)
        """

class ListManagedPoliciesInPermissionSetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListManagedPoliciesInPermissionSet.html#SSOAdmin.Paginator.ListManagedPoliciesInPermissionSet)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listmanagedpoliciesinpermissionsetpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef
        ],
    ) -> _PageIterator[ListManagedPoliciesInPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListManagedPoliciesInPermissionSet.html#SSOAdmin.Paginator.ListManagedPoliciesInPermissionSet.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listmanagedpoliciesinpermissionsetpaginator)
        """

class ListPermissionSetProvisioningStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetProvisioningStatus.html#SSOAdmin.Paginator.ListPermissionSetProvisioningStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listpermissionsetprovisioningstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef
        ],
    ) -> _PageIterator[ListPermissionSetProvisioningStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetProvisioningStatus.html#SSOAdmin.Paginator.ListPermissionSetProvisioningStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listpermissionsetprovisioningstatuspaginator)
        """

class ListPermissionSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSets.html#SSOAdmin.Paginator.ListPermissionSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listpermissionsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPermissionSetsRequestListPermissionSetsPaginateTypeDef]
    ) -> _PageIterator[ListPermissionSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSets.html#SSOAdmin.Paginator.ListPermissionSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listpermissionsetspaginator)
        """

class ListPermissionSetsProvisionedToAccountPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetsProvisionedToAccount.html#SSOAdmin.Paginator.ListPermissionSetsProvisionedToAccount)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listpermissionsetsprovisionedtoaccountpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef
        ],
    ) -> _PageIterator[ListPermissionSetsProvisionedToAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetsProvisionedToAccount.html#SSOAdmin.Paginator.ListPermissionSetsProvisionedToAccount.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listpermissionsetsprovisionedtoaccountpaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTagsForResource.html#SSOAdmin.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTagsForResource.html#SSOAdmin.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listtagsforresourcepaginator)
        """

class ListTrustedTokenIssuersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTrustedTokenIssuers.html#SSOAdmin.Paginator.ListTrustedTokenIssuers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listtrustedtokenissuerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTrustedTokenIssuersRequestListTrustedTokenIssuersPaginateTypeDef]
    ) -> _PageIterator[ListTrustedTokenIssuersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTrustedTokenIssuers.html#SSOAdmin.Paginator.ListTrustedTokenIssuers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/paginators/#listtrustedtokenissuerspaginator)
        """
