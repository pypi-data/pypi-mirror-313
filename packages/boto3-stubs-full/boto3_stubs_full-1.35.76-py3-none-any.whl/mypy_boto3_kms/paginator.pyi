"""
Type annotations for kms service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_kms.client import KMSClient
    from mypy_boto3_kms.paginator import (
        DescribeCustomKeyStoresPaginator,
        ListAliasesPaginator,
        ListGrantsPaginator,
        ListKeyPoliciesPaginator,
        ListKeyRotationsPaginator,
        ListKeysPaginator,
        ListResourceTagsPaginator,
        ListRetirableGrantsPaginator,
    )

    session = Session()
    client: KMSClient = session.client("kms")

    describe_custom_key_stores_paginator: DescribeCustomKeyStoresPaginator = client.get_paginator("describe_custom_key_stores")
    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_grants_paginator: ListGrantsPaginator = client.get_paginator("list_grants")
    list_key_policies_paginator: ListKeyPoliciesPaginator = client.get_paginator("list_key_policies")
    list_key_rotations_paginator: ListKeyRotationsPaginator = client.get_paginator("list_key_rotations")
    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    list_resource_tags_paginator: ListResourceTagsPaginator = client.get_paginator("list_resource_tags")
    list_retirable_grants_paginator: ListRetirableGrantsPaginator = client.get_paginator("list_retirable_grants")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeCustomKeyStoresRequestDescribeCustomKeyStoresPaginateTypeDef,
    DescribeCustomKeyStoresResponseTypeDef,
    ListAliasesRequestListAliasesPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListGrantsRequestListGrantsPaginateTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeyRotationsRequestListKeyRotationsPaginateTypeDef,
    ListKeyRotationsResponseTypeDef,
    ListKeysRequestListKeysPaginateTypeDef,
    ListKeysResponseTypeDef,
    ListResourceTagsRequestListResourceTagsPaginateTypeDef,
    ListResourceTagsResponseTypeDef,
    ListRetirableGrantsRequestListRetirableGrantsPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCustomKeyStoresPaginator",
    "ListAliasesPaginator",
    "ListGrantsPaginator",
    "ListKeyPoliciesPaginator",
    "ListKeyRotationsPaginator",
    "ListKeysPaginator",
    "ListResourceTagsPaginator",
    "ListRetirableGrantsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCustomKeyStoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/DescribeCustomKeyStores.html#KMS.Paginator.DescribeCustomKeyStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#describecustomkeystorespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCustomKeyStoresRequestDescribeCustomKeyStoresPaginateTypeDef]
    ) -> _PageIterator[DescribeCustomKeyStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/DescribeCustomKeyStores.html#KMS.Paginator.DescribeCustomKeyStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#describecustomkeystorespaginator)
        """

class ListAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListAliases.html#KMS.Paginator.ListAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listaliasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAliasesRequestListAliasesPaginateTypeDef]
    ) -> _PageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListAliases.html#KMS.Paginator.ListAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listaliasespaginator)
        """

class ListGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListGrants.html#KMS.Paginator.ListGrants)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listgrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGrantsRequestListGrantsPaginateTypeDef]
    ) -> _PageIterator[ListGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListGrants.html#KMS.Paginator.ListGrants.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listgrantspaginator)
        """

class ListKeyPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyPolicies.html#KMS.Paginator.ListKeyPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listkeypoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListKeyPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyPolicies.html#KMS.Paginator.ListKeyPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listkeypoliciespaginator)
        """

class ListKeyRotationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyRotations.html#KMS.Paginator.ListKeyRotations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listkeyrotationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListKeyRotationsRequestListKeyRotationsPaginateTypeDef]
    ) -> _PageIterator[ListKeyRotationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyRotations.html#KMS.Paginator.ListKeyRotations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listkeyrotationspaginator)
        """

class ListKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeys.html#KMS.Paginator.ListKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listkeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListKeysRequestListKeysPaginateTypeDef]
    ) -> _PageIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeys.html#KMS.Paginator.ListKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listkeyspaginator)
        """

class ListResourceTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListResourceTags.html#KMS.Paginator.ListResourceTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listresourcetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceTagsRequestListResourceTagsPaginateTypeDef]
    ) -> _PageIterator[ListResourceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListResourceTags.html#KMS.Paginator.ListResourceTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listresourcetagspaginator)
        """

class ListRetirableGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListRetirableGrants.html#KMS.Paginator.ListRetirableGrants)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listretirablegrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRetirableGrantsRequestListRetirableGrantsPaginateTypeDef]
    ) -> _PageIterator[ListGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListRetirableGrants.html#KMS.Paginator.ListRetirableGrants.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/paginators/#listretirablegrantspaginator)
        """
