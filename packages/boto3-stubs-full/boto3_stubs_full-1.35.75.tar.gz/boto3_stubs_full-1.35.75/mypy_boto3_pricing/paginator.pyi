"""
Type annotations for pricing service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pricing.client import PricingClient
    from mypy_boto3_pricing.paginator import (
        DescribeServicesPaginator,
        GetAttributeValuesPaginator,
        GetProductsPaginator,
        ListPriceListsPaginator,
    )

    session = Session()
    client: PricingClient = session.client("pricing")

    describe_services_paginator: DescribeServicesPaginator = client.get_paginator("describe_services")
    get_attribute_values_paginator: GetAttributeValuesPaginator = client.get_paginator("get_attribute_values")
    get_products_paginator: GetProductsPaginator = client.get_paginator("get_products")
    list_price_lists_paginator: ListPriceListsPaginator = client.get_paginator("list_price_lists")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeServicesRequestDescribeServicesPaginateTypeDef,
    DescribeServicesResponseTypeDef,
    GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef,
    GetAttributeValuesResponseTypeDef,
    GetProductsRequestGetProductsPaginateTypeDef,
    GetProductsResponseTypeDef,
    ListPriceListsRequestListPriceListsPaginateTypeDef,
    ListPriceListsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeServicesPaginator",
    "GetAttributeValuesPaginator",
    "GetProductsPaginator",
    "ListPriceListsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/DescribeServices.html#Pricing.Paginator.DescribeServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#describeservicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeServicesRequestDescribeServicesPaginateTypeDef]
    ) -> _PageIterator[DescribeServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/DescribeServices.html#Pricing.Paginator.DescribeServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#describeservicespaginator)
        """

class GetAttributeValuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetAttributeValues.html#Pricing.Paginator.GetAttributeValues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getattributevaluespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef]
    ) -> _PageIterator[GetAttributeValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetAttributeValues.html#Pricing.Paginator.GetAttributeValues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getattributevaluespaginator)
        """

class GetProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetProducts.html#Pricing.Paginator.GetProducts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getproductspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetProductsRequestGetProductsPaginateTypeDef]
    ) -> _PageIterator[GetProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetProducts.html#Pricing.Paginator.GetProducts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getproductspaginator)
        """

class ListPriceListsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/ListPriceLists.html#Pricing.Paginator.ListPriceLists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#listpricelistspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPriceListsRequestListPriceListsPaginateTypeDef]
    ) -> _PageIterator[ListPriceListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/ListPriceLists.html#Pricing.Paginator.ListPriceLists.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#listpricelistspaginator)
        """
