"""
Type annotations for cloudfront service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudfront.client import CloudFrontClient
    from mypy_boto3_cloudfront.paginator import (
        ListCloudFrontOriginAccessIdentitiesPaginator,
        ListDistributionsPaginator,
        ListInvalidationsPaginator,
        ListKeyValueStoresPaginator,
        ListPublicKeysPaginator,
        ListStreamingDistributionsPaginator,
    )

    session = Session()
    client: CloudFrontClient = session.client("cloudfront")

    list_cloud_front_origin_access_identities_paginator: ListCloudFrontOriginAccessIdentitiesPaginator = client.get_paginator("list_cloud_front_origin_access_identities")
    list_distributions_paginator: ListDistributionsPaginator = client.get_paginator("list_distributions")
    list_invalidations_paginator: ListInvalidationsPaginator = client.get_paginator("list_invalidations")
    list_key_value_stores_paginator: ListKeyValueStoresPaginator = client.get_paginator("list_key_value_stores")
    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    list_streaming_distributions_paginator: ListStreamingDistributionsPaginator = client.get_paginator("list_streaming_distributions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef,
    ListCloudFrontOriginAccessIdentitiesResultTypeDef,
    ListDistributionsRequestListDistributionsPaginateTypeDef,
    ListDistributionsResultTypeDef,
    ListInvalidationsRequestListInvalidationsPaginateTypeDef,
    ListInvalidationsResultTypeDef,
    ListKeyValueStoresRequestListKeyValueStoresPaginateTypeDef,
    ListKeyValueStoresResultTypeDef,
    ListPublicKeysRequestListPublicKeysPaginateTypeDef,
    ListPublicKeysResultTypeDef,
    ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef,
    ListStreamingDistributionsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCloudFrontOriginAccessIdentitiesPaginator",
    "ListDistributionsPaginator",
    "ListInvalidationsPaginator",
    "ListKeyValueStoresPaginator",
    "ListPublicKeysPaginator",
    "ListStreamingDistributionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCloudFrontOriginAccessIdentitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListCloudFrontOriginAccessIdentities.html#CloudFront.Paginator.ListCloudFrontOriginAccessIdentities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listcloudfrontoriginaccessidentitiespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef
        ],
    ) -> _PageIterator[ListCloudFrontOriginAccessIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListCloudFrontOriginAccessIdentities.html#CloudFront.Paginator.ListCloudFrontOriginAccessIdentities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listcloudfrontoriginaccessidentitiespaginator)
        """


class ListDistributionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListDistributions.html#CloudFront.Paginator.ListDistributions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listdistributionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDistributionsRequestListDistributionsPaginateTypeDef]
    ) -> _PageIterator[ListDistributionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListDistributions.html#CloudFront.Paginator.ListDistributions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listdistributionspaginator)
        """


class ListInvalidationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListInvalidations.html#CloudFront.Paginator.ListInvalidations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listinvalidationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInvalidationsRequestListInvalidationsPaginateTypeDef]
    ) -> _PageIterator[ListInvalidationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListInvalidations.html#CloudFront.Paginator.ListInvalidations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listinvalidationspaginator)
        """


class ListKeyValueStoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListKeyValueStores.html#CloudFront.Paginator.ListKeyValueStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listkeyvaluestorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKeyValueStoresRequestListKeyValueStoresPaginateTypeDef]
    ) -> _PageIterator[ListKeyValueStoresResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListKeyValueStores.html#CloudFront.Paginator.ListKeyValueStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listkeyvaluestorespaginator)
        """


class ListPublicKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListPublicKeys.html#CloudFront.Paginator.ListPublicKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listpublickeyspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPublicKeysRequestListPublicKeysPaginateTypeDef]
    ) -> _PageIterator[ListPublicKeysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListPublicKeys.html#CloudFront.Paginator.ListPublicKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listpublickeyspaginator)
        """


class ListStreamingDistributionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListStreamingDistributions.html#CloudFront.Paginator.ListStreamingDistributions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#liststreamingdistributionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListStreamingDistributionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListStreamingDistributions.html#CloudFront.Paginator.ListStreamingDistributions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#liststreamingdistributionspaginator)
        """
