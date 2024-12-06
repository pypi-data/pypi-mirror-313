"""
Type annotations for b2bi service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_b2bi.client import B2BIClient
    from mypy_boto3_b2bi.paginator import (
        ListCapabilitiesPaginator,
        ListPartnershipsPaginator,
        ListProfilesPaginator,
        ListTransformersPaginator,
    )

    session = Session()
    client: B2BIClient = session.client("b2bi")

    list_capabilities_paginator: ListCapabilitiesPaginator = client.get_paginator("list_capabilities")
    list_partnerships_paginator: ListPartnershipsPaginator = client.get_paginator("list_partnerships")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    list_transformers_paginator: ListTransformersPaginator = client.get_paginator("list_transformers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCapabilitiesRequestListCapabilitiesPaginateTypeDef,
    ListCapabilitiesResponseTypeDef,
    ListPartnershipsRequestListPartnershipsPaginateTypeDef,
    ListPartnershipsResponseTypeDef,
    ListProfilesRequestListProfilesPaginateTypeDef,
    ListProfilesResponseTypeDef,
    ListTransformersRequestListTransformersPaginateTypeDef,
    ListTransformersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCapabilitiesPaginator",
    "ListPartnershipsPaginator",
    "ListProfilesPaginator",
    "ListTransformersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCapabilitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListCapabilities.html#B2BI.Paginator.ListCapabilities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listcapabilitiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCapabilitiesRequestListCapabilitiesPaginateTypeDef]
    ) -> _PageIterator[ListCapabilitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListCapabilities.html#B2BI.Paginator.ListCapabilities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listcapabilitiespaginator)
        """


class ListPartnershipsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListPartnerships.html#B2BI.Paginator.ListPartnerships)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listpartnershipspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPartnershipsRequestListPartnershipsPaginateTypeDef]
    ) -> _PageIterator[ListPartnershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListPartnerships.html#B2BI.Paginator.ListPartnerships.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listpartnershipspaginator)
        """


class ListProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListProfiles.html#B2BI.Paginator.ListProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProfilesRequestListProfilesPaginateTypeDef]
    ) -> _PageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListProfiles.html#B2BI.Paginator.ListProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listprofilespaginator)
        """


class ListTransformersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListTransformers.html#B2BI.Paginator.ListTransformers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listtransformerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTransformersRequestListTransformersPaginateTypeDef]
    ) -> _PageIterator[ListTransformersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListTransformers.html#B2BI.Paginator.ListTransformers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_b2bi/paginators/#listtransformerspaginator)
        """
