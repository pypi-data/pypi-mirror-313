"""
Type annotations for ram service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ram.client import RAMClient
    from mypy_boto3_ram.paginator import (
        GetResourcePoliciesPaginator,
        GetResourceShareAssociationsPaginator,
        GetResourceShareInvitationsPaginator,
        GetResourceSharesPaginator,
        ListPrincipalsPaginator,
        ListResourcesPaginator,
    )

    session = Session()
    client: RAMClient = session.client("ram")

    get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
    get_resource_share_associations_paginator: GetResourceShareAssociationsPaginator = client.get_paginator("get_resource_share_associations")
    get_resource_share_invitations_paginator: GetResourceShareInvitationsPaginator = client.get_paginator("get_resource_share_invitations")
    get_resource_shares_paginator: GetResourceSharesPaginator = client.get_paginator("get_resource_shares")
    list_principals_paginator: ListPrincipalsPaginator = client.get_paginator("list_principals")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef,
    GetResourceShareAssociationsResponseTypeDef,
    GetResourceShareInvitationsRequestGetResourceShareInvitationsPaginateTypeDef,
    GetResourceShareInvitationsResponseTypeDef,
    GetResourceSharesRequestGetResourceSharesPaginateTypeDef,
    GetResourceSharesResponseTypeDef,
    ListPrincipalsRequestListPrincipalsPaginateTypeDef,
    ListPrincipalsResponseTypeDef,
    ListResourcesRequestListResourcesPaginateTypeDef,
    ListResourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetResourcePoliciesPaginator",
    "GetResourceShareAssociationsPaginator",
    "GetResourceShareInvitationsPaginator",
    "GetResourceSharesPaginator",
    "ListPrincipalsPaginator",
    "ListResourcesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetResourcePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourcePolicies.html#RAM.Paginator.GetResourcePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourcepoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef]
    ) -> _PageIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourcePolicies.html#RAM.Paginator.GetResourcePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourcepoliciespaginator)
        """


class GetResourceShareAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareAssociations.html#RAM.Paginator.GetResourceShareAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourceshareassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetResourceShareAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareAssociations.html#RAM.Paginator.GetResourceShareAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourceshareassociationspaginator)
        """


class GetResourceShareInvitationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareInvitations.html#RAM.Paginator.GetResourceShareInvitations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourceshareinvitationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetResourceShareInvitationsRequestGetResourceShareInvitationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetResourceShareInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareInvitations.html#RAM.Paginator.GetResourceShareInvitations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourceshareinvitationspaginator)
        """


class GetResourceSharesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShares.html#RAM.Paginator.GetResourceShares)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourcesharespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetResourceSharesRequestGetResourceSharesPaginateTypeDef]
    ) -> _PageIterator[GetResourceSharesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShares.html#RAM.Paginator.GetResourceShares.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#getresourcesharespaginator)
        """


class ListPrincipalsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListPrincipals.html#RAM.Paginator.ListPrincipals)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#listprincipalspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPrincipalsRequestListPrincipalsPaginateTypeDef]
    ) -> _PageIterator[ListPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListPrincipals.html#RAM.Paginator.ListPrincipals.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#listprincipalspaginator)
        """


class ListResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListResources.html#RAM.Paginator.ListResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#listresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourcesRequestListResourcesPaginateTypeDef]
    ) -> _PageIterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListResources.html#RAM.Paginator.ListResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators/#listresourcespaginator)
        """
