"""
Type annotations for iam service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iam.client import IAMClient
    from mypy_boto3_iam.paginator import (
        GetAccountAuthorizationDetailsPaginator,
        GetGroupPaginator,
        ListAccessKeysPaginator,
        ListAccountAliasesPaginator,
        ListAttachedGroupPoliciesPaginator,
        ListAttachedRolePoliciesPaginator,
        ListAttachedUserPoliciesPaginator,
        ListEntitiesForPolicyPaginator,
        ListGroupPoliciesPaginator,
        ListGroupsForUserPaginator,
        ListGroupsPaginator,
        ListInstanceProfileTagsPaginator,
        ListInstanceProfilesForRolePaginator,
        ListInstanceProfilesPaginator,
        ListMFADeviceTagsPaginator,
        ListMFADevicesPaginator,
        ListOpenIDConnectProviderTagsPaginator,
        ListPoliciesPaginator,
        ListPolicyTagsPaginator,
        ListPolicyVersionsPaginator,
        ListRolePoliciesPaginator,
        ListRoleTagsPaginator,
        ListRolesPaginator,
        ListSAMLProviderTagsPaginator,
        ListSSHPublicKeysPaginator,
        ListServerCertificateTagsPaginator,
        ListServerCertificatesPaginator,
        ListSigningCertificatesPaginator,
        ListUserPoliciesPaginator,
        ListUserTagsPaginator,
        ListUsersPaginator,
        ListVirtualMFADevicesPaginator,
        SimulateCustomPolicyPaginator,
        SimulatePrincipalPolicyPaginator,
    )

    session = Session()
    client: IAMClient = session.client("iam")

    get_account_authorization_details_paginator: GetAccountAuthorizationDetailsPaginator = client.get_paginator("get_account_authorization_details")
    get_group_paginator: GetGroupPaginator = client.get_paginator("get_group")
    list_access_keys_paginator: ListAccessKeysPaginator = client.get_paginator("list_access_keys")
    list_account_aliases_paginator: ListAccountAliasesPaginator = client.get_paginator("list_account_aliases")
    list_attached_group_policies_paginator: ListAttachedGroupPoliciesPaginator = client.get_paginator("list_attached_group_policies")
    list_attached_role_policies_paginator: ListAttachedRolePoliciesPaginator = client.get_paginator("list_attached_role_policies")
    list_attached_user_policies_paginator: ListAttachedUserPoliciesPaginator = client.get_paginator("list_attached_user_policies")
    list_entities_for_policy_paginator: ListEntitiesForPolicyPaginator = client.get_paginator("list_entities_for_policy")
    list_group_policies_paginator: ListGroupPoliciesPaginator = client.get_paginator("list_group_policies")
    list_groups_for_user_paginator: ListGroupsForUserPaginator = client.get_paginator("list_groups_for_user")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_instance_profile_tags_paginator: ListInstanceProfileTagsPaginator = client.get_paginator("list_instance_profile_tags")
    list_instance_profiles_for_role_paginator: ListInstanceProfilesForRolePaginator = client.get_paginator("list_instance_profiles_for_role")
    list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
    list_mfa_device_tags_paginator: ListMFADeviceTagsPaginator = client.get_paginator("list_mfa_device_tags")
    list_mfa_devices_paginator: ListMFADevicesPaginator = client.get_paginator("list_mfa_devices")
    list_open_id_connect_provider_tags_paginator: ListOpenIDConnectProviderTagsPaginator = client.get_paginator("list_open_id_connect_provider_tags")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_tags_paginator: ListPolicyTagsPaginator = client.get_paginator("list_policy_tags")
    list_policy_versions_paginator: ListPolicyVersionsPaginator = client.get_paginator("list_policy_versions")
    list_role_policies_paginator: ListRolePoliciesPaginator = client.get_paginator("list_role_policies")
    list_role_tags_paginator: ListRoleTagsPaginator = client.get_paginator("list_role_tags")
    list_roles_paginator: ListRolesPaginator = client.get_paginator("list_roles")
    list_saml_provider_tags_paginator: ListSAMLProviderTagsPaginator = client.get_paginator("list_saml_provider_tags")
    list_ssh_public_keys_paginator: ListSSHPublicKeysPaginator = client.get_paginator("list_ssh_public_keys")
    list_server_certificate_tags_paginator: ListServerCertificateTagsPaginator = client.get_paginator("list_server_certificate_tags")
    list_server_certificates_paginator: ListServerCertificatesPaginator = client.get_paginator("list_server_certificates")
    list_signing_certificates_paginator: ListSigningCertificatesPaginator = client.get_paginator("list_signing_certificates")
    list_user_policies_paginator: ListUserPoliciesPaginator = client.get_paginator("list_user_policies")
    list_user_tags_paginator: ListUserTagsPaginator = client.get_paginator("list_user_tags")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    list_virtual_mfa_devices_paginator: ListVirtualMFADevicesPaginator = client.get_paginator("list_virtual_mfa_devices")
    simulate_custom_policy_paginator: SimulateCustomPolicyPaginator = client.get_paginator("simulate_custom_policy")
    simulate_principal_policy_paginator: SimulatePrincipalPolicyPaginator = client.get_paginator("simulate_principal_policy")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetAccountAuthorizationDetailsRequestGetAccountAuthorizationDetailsPaginateTypeDef,
    GetAccountAuthorizationDetailsResponseTypeDef,
    GetGroupRequestGetGroupPaginateTypeDef,
    GetGroupResponseTypeDef,
    ListAccessKeysRequestListAccessKeysPaginateTypeDef,
    ListAccessKeysResponseTypeDef,
    ListAccountAliasesRequestListAccountAliasesPaginateTypeDef,
    ListAccountAliasesResponseTypeDef,
    ListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef,
    ListAttachedGroupPoliciesResponseTypeDef,
    ListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef,
    ListAttachedRolePoliciesResponseTypeDef,
    ListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef,
    ListAttachedUserPoliciesResponseTypeDef,
    ListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef,
    ListEntitiesForPolicyResponseTypeDef,
    ListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef,
    ListGroupPoliciesResponseTypeDef,
    ListGroupsForUserRequestListGroupsForUserPaginateTypeDef,
    ListGroupsForUserResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef,
    ListInstanceProfilesForRoleResponseTypeDef,
    ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef,
    ListInstanceProfilesResponseTypeDef,
    ListInstanceProfileTagsRequestListInstanceProfileTagsPaginateTypeDef,
    ListInstanceProfileTagsResponseTypeDef,
    ListMFADevicesRequestListMFADevicesPaginateTypeDef,
    ListMFADevicesResponseTypeDef,
    ListMFADeviceTagsRequestListMFADeviceTagsPaginateTypeDef,
    ListMFADeviceTagsResponseTypeDef,
    ListOpenIDConnectProviderTagsRequestListOpenIDConnectProviderTagsPaginateTypeDef,
    ListOpenIDConnectProviderTagsResponseTypeDef,
    ListPoliciesRequestListPoliciesPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyTagsRequestListPolicyTagsPaginateTypeDef,
    ListPolicyTagsResponseTypeDef,
    ListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListRolePoliciesRequestListRolePoliciesPaginateTypeDef,
    ListRolePoliciesResponseTypeDef,
    ListRolesRequestListRolesPaginateTypeDef,
    ListRolesResponseTypeDef,
    ListRoleTagsRequestListRoleTagsPaginateTypeDef,
    ListRoleTagsResponseTypeDef,
    ListSAMLProviderTagsRequestListSAMLProviderTagsPaginateTypeDef,
    ListSAMLProviderTagsResponseTypeDef,
    ListServerCertificatesRequestListServerCertificatesPaginateTypeDef,
    ListServerCertificatesResponseTypeDef,
    ListServerCertificateTagsRequestListServerCertificateTagsPaginateTypeDef,
    ListServerCertificateTagsResponseTypeDef,
    ListSigningCertificatesRequestListSigningCertificatesPaginateTypeDef,
    ListSigningCertificatesResponseTypeDef,
    ListSSHPublicKeysRequestListSSHPublicKeysPaginateTypeDef,
    ListSSHPublicKeysResponseTypeDef,
    ListUserPoliciesRequestListUserPoliciesPaginateTypeDef,
    ListUserPoliciesResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListUserTagsRequestListUserTagsPaginateTypeDef,
    ListUserTagsResponseTypeDef,
    ListVirtualMFADevicesRequestListVirtualMFADevicesPaginateTypeDef,
    ListVirtualMFADevicesResponseTypeDef,
    SimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef,
    SimulatePolicyResponseTypeDef,
    SimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetAccountAuthorizationDetailsPaginator",
    "GetGroupPaginator",
    "ListAccessKeysPaginator",
    "ListAccountAliasesPaginator",
    "ListAttachedGroupPoliciesPaginator",
    "ListAttachedRolePoliciesPaginator",
    "ListAttachedUserPoliciesPaginator",
    "ListEntitiesForPolicyPaginator",
    "ListGroupPoliciesPaginator",
    "ListGroupsForUserPaginator",
    "ListGroupsPaginator",
    "ListInstanceProfileTagsPaginator",
    "ListInstanceProfilesForRolePaginator",
    "ListInstanceProfilesPaginator",
    "ListMFADeviceTagsPaginator",
    "ListMFADevicesPaginator",
    "ListOpenIDConnectProviderTagsPaginator",
    "ListPoliciesPaginator",
    "ListPolicyTagsPaginator",
    "ListPolicyVersionsPaginator",
    "ListRolePoliciesPaginator",
    "ListRoleTagsPaginator",
    "ListRolesPaginator",
    "ListSAMLProviderTagsPaginator",
    "ListSSHPublicKeysPaginator",
    "ListServerCertificateTagsPaginator",
    "ListServerCertificatesPaginator",
    "ListSigningCertificatesPaginator",
    "ListUserPoliciesPaginator",
    "ListUserTagsPaginator",
    "ListUsersPaginator",
    "ListVirtualMFADevicesPaginator",
    "SimulateCustomPolicyPaginator",
    "SimulatePrincipalPolicyPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetAccountAuthorizationDetailsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetAccountAuthorizationDetails.html#IAM.Paginator.GetAccountAuthorizationDetails)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#getaccountauthorizationdetailspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetAccountAuthorizationDetailsRequestGetAccountAuthorizationDetailsPaginateTypeDef
        ],
    ) -> _PageIterator[GetAccountAuthorizationDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetAccountAuthorizationDetails.html#IAM.Paginator.GetAccountAuthorizationDetails.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#getaccountauthorizationdetailspaginator)
        """

class GetGroupPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetGroup.html#IAM.Paginator.GetGroup)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#getgrouppaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetGroupRequestGetGroupPaginateTypeDef]
    ) -> _PageIterator[GetGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetGroup.html#IAM.Paginator.GetGroup.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#getgrouppaginator)
        """

class ListAccessKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html#IAM.Paginator.ListAccessKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listaccesskeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessKeysRequestListAccessKeysPaginateTypeDef]
    ) -> _PageIterator[ListAccessKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html#IAM.Paginator.ListAccessKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listaccesskeyspaginator)
        """

class ListAccountAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccountAliases.html#IAM.Paginator.ListAccountAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listaccountaliasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountAliasesRequestListAccountAliasesPaginateTypeDef]
    ) -> _PageIterator[ListAccountAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccountAliases.html#IAM.Paginator.ListAccountAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listaccountaliasespaginator)
        """

class ListAttachedGroupPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedGroupPolicies.html#IAM.Paginator.ListAttachedGroupPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listattachedgrouppoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef],
    ) -> _PageIterator[ListAttachedGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedGroupPolicies.html#IAM.Paginator.ListAttachedGroupPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listattachedgrouppoliciespaginator)
        """

class ListAttachedRolePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedRolePolicies.html#IAM.Paginator.ListAttachedRolePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listattachedrolepoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef],
    ) -> _PageIterator[ListAttachedRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedRolePolicies.html#IAM.Paginator.ListAttachedRolePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listattachedrolepoliciespaginator)
        """

class ListAttachedUserPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedUserPolicies.html#IAM.Paginator.ListAttachedUserPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listattacheduserpoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef],
    ) -> _PageIterator[ListAttachedUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedUserPolicies.html#IAM.Paginator.ListAttachedUserPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listattacheduserpoliciespaginator)
        """

class ListEntitiesForPolicyPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListEntitiesForPolicy.html#IAM.Paginator.ListEntitiesForPolicy)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listentitiesforpolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef]
    ) -> _PageIterator[ListEntitiesForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListEntitiesForPolicy.html#IAM.Paginator.ListEntitiesForPolicy.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listentitiesforpolicypaginator)
        """

class ListGroupPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupPolicies.html#IAM.Paginator.ListGroupPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listgrouppoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupPolicies.html#IAM.Paginator.ListGroupPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listgrouppoliciespaginator)
        """

class ListGroupsForUserPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupsForUser.html#IAM.Paginator.ListGroupsForUser)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listgroupsforuserpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsForUserRequestListGroupsForUserPaginateTypeDef]
    ) -> _PageIterator[ListGroupsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupsForUser.html#IAM.Paginator.ListGroupsForUser.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listgroupsforuserpaginator)
        """

class ListGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroups.html#IAM.Paginator.ListGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> _PageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroups.html#IAM.Paginator.ListGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listgroupspaginator)
        """

class ListInstanceProfileTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfileTags.html#IAM.Paginator.ListInstanceProfileTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listinstanceprofiletagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceProfileTagsRequestListInstanceProfileTagsPaginateTypeDef]
    ) -> _PageIterator[ListInstanceProfileTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfileTags.html#IAM.Paginator.ListInstanceProfileTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listinstanceprofiletagspaginator)
        """

class ListInstanceProfilesForRolePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfilesForRole.html#IAM.Paginator.ListInstanceProfilesForRole)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listinstanceprofilesforrolepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef
        ],
    ) -> _PageIterator[ListInstanceProfilesForRoleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfilesForRole.html#IAM.Paginator.ListInstanceProfilesForRole.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listinstanceprofilesforrolepaginator)
        """

class ListInstanceProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfiles.html#IAM.Paginator.ListInstanceProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listinstanceprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef]
    ) -> _PageIterator[ListInstanceProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfiles.html#IAM.Paginator.ListInstanceProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listinstanceprofilespaginator)
        """

class ListMFADeviceTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADeviceTags.html#IAM.Paginator.ListMFADeviceTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listmfadevicetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMFADeviceTagsRequestListMFADeviceTagsPaginateTypeDef]
    ) -> _PageIterator[ListMFADeviceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADeviceTags.html#IAM.Paginator.ListMFADeviceTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listmfadevicetagspaginator)
        """

class ListMFADevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADevices.html#IAM.Paginator.ListMFADevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listmfadevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMFADevicesRequestListMFADevicesPaginateTypeDef]
    ) -> _PageIterator[ListMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADevices.html#IAM.Paginator.ListMFADevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listmfadevicespaginator)
        """

class ListOpenIDConnectProviderTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListOpenIDConnectProviderTags.html#IAM.Paginator.ListOpenIDConnectProviderTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listopenidconnectprovidertagspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListOpenIDConnectProviderTagsRequestListOpenIDConnectProviderTagsPaginateTypeDef
        ],
    ) -> _PageIterator[ListOpenIDConnectProviderTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListOpenIDConnectProviderTags.html#IAM.Paginator.ListOpenIDConnectProviderTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listopenidconnectprovidertagspaginator)
        """

class ListPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicies.html#IAM.Paginator.ListPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPoliciesRequestListPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicies.html#IAM.Paginator.ListPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listpoliciespaginator)
        """

class ListPolicyTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyTags.html#IAM.Paginator.ListPolicyTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listpolicytagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyTagsRequestListPolicyTagsPaginateTypeDef]
    ) -> _PageIterator[ListPolicyTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyTags.html#IAM.Paginator.ListPolicyTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listpolicytagspaginator)
        """

class ListPolicyVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyVersions.html#IAM.Paginator.ListPolicyVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listpolicyversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef]
    ) -> _PageIterator[ListPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyVersions.html#IAM.Paginator.ListPolicyVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listpolicyversionspaginator)
        """

class ListRolePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRolePolicies.html#IAM.Paginator.ListRolePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listrolepoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRolePoliciesRequestListRolePoliciesPaginateTypeDef]
    ) -> _PageIterator[ListRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRolePolicies.html#IAM.Paginator.ListRolePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listrolepoliciespaginator)
        """

class ListRoleTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoleTags.html#IAM.Paginator.ListRoleTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listroletagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRoleTagsRequestListRoleTagsPaginateTypeDef]
    ) -> _PageIterator[ListRoleTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoleTags.html#IAM.Paginator.ListRoleTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listroletagspaginator)
        """

class ListRolesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html#IAM.Paginator.ListRoles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listrolespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRolesRequestListRolesPaginateTypeDef]
    ) -> _PageIterator[ListRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html#IAM.Paginator.ListRoles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listrolespaginator)
        """

class ListSAMLProviderTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSAMLProviderTags.html#IAM.Paginator.ListSAMLProviderTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listsamlprovidertagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSAMLProviderTagsRequestListSAMLProviderTagsPaginateTypeDef]
    ) -> _PageIterator[ListSAMLProviderTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSAMLProviderTags.html#IAM.Paginator.ListSAMLProviderTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listsamlprovidertagspaginator)
        """

class ListSSHPublicKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSSHPublicKeys.html#IAM.Paginator.ListSSHPublicKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listsshpublickeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSSHPublicKeysRequestListSSHPublicKeysPaginateTypeDef]
    ) -> _PageIterator[ListSSHPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSSHPublicKeys.html#IAM.Paginator.ListSSHPublicKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listsshpublickeyspaginator)
        """

class ListServerCertificateTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificateTags.html#IAM.Paginator.ListServerCertificateTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listservercertificatetagspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListServerCertificateTagsRequestListServerCertificateTagsPaginateTypeDef],
    ) -> _PageIterator[ListServerCertificateTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificateTags.html#IAM.Paginator.ListServerCertificateTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listservercertificatetagspaginator)
        """

class ListServerCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificates.html#IAM.Paginator.ListServerCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listservercertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServerCertificatesRequestListServerCertificatesPaginateTypeDef]
    ) -> _PageIterator[ListServerCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificates.html#IAM.Paginator.ListServerCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listservercertificatespaginator)
        """

class ListSigningCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSigningCertificates.html#IAM.Paginator.ListSigningCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listsigningcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningCertificatesRequestListSigningCertificatesPaginateTypeDef]
    ) -> _PageIterator[ListSigningCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSigningCertificates.html#IAM.Paginator.ListSigningCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listsigningcertificatespaginator)
        """

class ListUserPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserPolicies.html#IAM.Paginator.ListUserPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listuserpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUserPoliciesRequestListUserPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserPolicies.html#IAM.Paginator.ListUserPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listuserpoliciespaginator)
        """

class ListUserTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserTags.html#IAM.Paginator.ListUserTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listusertagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUserTagsRequestListUserTagsPaginateTypeDef]
    ) -> _PageIterator[ListUserTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserTags.html#IAM.Paginator.ListUserTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listusertagspaginator)
        """

class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html#IAM.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html#IAM.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listuserspaginator)
        """

class ListVirtualMFADevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListVirtualMFADevices.html#IAM.Paginator.ListVirtualMFADevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listvirtualmfadevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVirtualMFADevicesRequestListVirtualMFADevicesPaginateTypeDef]
    ) -> _PageIterator[ListVirtualMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListVirtualMFADevices.html#IAM.Paginator.ListVirtualMFADevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#listvirtualmfadevicespaginator)
        """

class SimulateCustomPolicyPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulateCustomPolicy.html#IAM.Paginator.SimulateCustomPolicy)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#simulatecustompolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef]
    ) -> _PageIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulateCustomPolicy.html#IAM.Paginator.SimulateCustomPolicy.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#simulatecustompolicypaginator)
        """

class SimulatePrincipalPolicyPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulatePrincipalPolicy.html#IAM.Paginator.SimulatePrincipalPolicy)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#simulateprincipalpolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef]
    ) -> _PageIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulatePrincipalPolicy.html#IAM.Paginator.SimulatePrincipalPolicy.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/paginators/#simulateprincipalpolicypaginator)
        """
