"""
Type annotations for cognito-idp service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cognito_idp.client import CognitoIdentityProviderClient
    from mypy_boto3_cognito_idp.paginator import (
        AdminListGroupsForUserPaginator,
        AdminListUserAuthEventsPaginator,
        ListGroupsPaginator,
        ListIdentityProvidersPaginator,
        ListResourceServersPaginator,
        ListUserPoolClientsPaginator,
        ListUserPoolsPaginator,
        ListUsersInGroupPaginator,
        ListUsersPaginator,
    )

    session = Session()
    client: CognitoIdentityProviderClient = session.client("cognito-idp")

    admin_list_groups_for_user_paginator: AdminListGroupsForUserPaginator = client.get_paginator("admin_list_groups_for_user")
    admin_list_user_auth_events_paginator: AdminListUserAuthEventsPaginator = client.get_paginator("admin_list_user_auth_events")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_identity_providers_paginator: ListIdentityProvidersPaginator = client.get_paginator("list_identity_providers")
    list_resource_servers_paginator: ListResourceServersPaginator = client.get_paginator("list_resource_servers")
    list_user_pool_clients_paginator: ListUserPoolClientsPaginator = client.get_paginator("list_user_pool_clients")
    list_user_pools_paginator: ListUserPoolsPaginator = client.get_paginator("list_user_pools")
    list_users_in_group_paginator: ListUsersInGroupPaginator = client.get_paginator("list_users_in_group")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    AdminListGroupsForUserRequestAdminListGroupsForUserPaginateTypeDef,
    AdminListGroupsForUserResponseTypeDef,
    AdminListUserAuthEventsRequestAdminListUserAuthEventsPaginateTypeDef,
    AdminListUserAuthEventsResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListResourceServersRequestListResourceServersPaginateTypeDef,
    ListResourceServersResponseTypeDef,
    ListUserPoolClientsRequestListUserPoolClientsPaginateTypeDef,
    ListUserPoolClientsResponseTypeDef,
    ListUserPoolsRequestListUserPoolsPaginateTypeDef,
    ListUserPoolsResponseTypeDef,
    ListUsersInGroupRequestListUsersInGroupPaginateTypeDef,
    ListUsersInGroupResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "AdminListGroupsForUserPaginator",
    "AdminListUserAuthEventsPaginator",
    "ListGroupsPaginator",
    "ListIdentityProvidersPaginator",
    "ListResourceServersPaginator",
    "ListUserPoolClientsPaginator",
    "ListUserPoolsPaginator",
    "ListUsersInGroupPaginator",
    "ListUsersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class AdminListGroupsForUserPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListGroupsForUser.html#CognitoIdentityProvider.Paginator.AdminListGroupsForUser)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#adminlistgroupsforuserpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[AdminListGroupsForUserRequestAdminListGroupsForUserPaginateTypeDef]
    ) -> _PageIterator[AdminListGroupsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListGroupsForUser.html#CognitoIdentityProvider.Paginator.AdminListGroupsForUser.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#adminlistgroupsforuserpaginator)
        """


class AdminListUserAuthEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListUserAuthEvents.html#CognitoIdentityProvider.Paginator.AdminListUserAuthEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#adminlistuserautheventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[AdminListUserAuthEventsRequestAdminListUserAuthEventsPaginateTypeDef]
    ) -> _PageIterator[AdminListUserAuthEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListUserAuthEvents.html#CognitoIdentityProvider.Paginator.AdminListUserAuthEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#adminlistuserautheventspaginator)
        """


class ListGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListGroups.html#CognitoIdentityProvider.Paginator.ListGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> _PageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListGroups.html#CognitoIdentityProvider.Paginator.ListGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listgroupspaginator)
        """


class ListIdentityProvidersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListIdentityProviders.html#CognitoIdentityProvider.Paginator.ListIdentityProviders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listidentityproviderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef]
    ) -> _PageIterator[ListIdentityProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListIdentityProviders.html#CognitoIdentityProvider.Paginator.ListIdentityProviders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listidentityproviderspaginator)
        """


class ListResourceServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListResourceServers.html#CognitoIdentityProvider.Paginator.ListResourceServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listresourceserverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceServersRequestListResourceServersPaginateTypeDef]
    ) -> _PageIterator[ListResourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListResourceServers.html#CognitoIdentityProvider.Paginator.ListResourceServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listresourceserverspaginator)
        """


class ListUserPoolClientsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPoolClients.html#CognitoIdentityProvider.Paginator.ListUserPoolClients)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listuserpoolclientspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUserPoolClientsRequestListUserPoolClientsPaginateTypeDef]
    ) -> _PageIterator[ListUserPoolClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPoolClients.html#CognitoIdentityProvider.Paginator.ListUserPoolClients.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listuserpoolclientspaginator)
        """


class ListUserPoolsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPools.html#CognitoIdentityProvider.Paginator.ListUserPools)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listuserpoolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUserPoolsRequestListUserPoolsPaginateTypeDef]
    ) -> _PageIterator[ListUserPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPools.html#CognitoIdentityProvider.Paginator.ListUserPools.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listuserpoolspaginator)
        """


class ListUsersInGroupPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsersInGroup.html#CognitoIdentityProvider.Paginator.ListUsersInGroup)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listusersingrouppaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUsersInGroupRequestListUsersInGroupPaginateTypeDef]
    ) -> _PageIterator[ListUsersInGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsersInGroup.html#CognitoIdentityProvider.Paginator.ListUsersInGroup.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listusersingrouppaginator)
        """


class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsers.html#CognitoIdentityProvider.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsers.html#CognitoIdentityProvider.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/paginators/#listuserspaginator)
        """
