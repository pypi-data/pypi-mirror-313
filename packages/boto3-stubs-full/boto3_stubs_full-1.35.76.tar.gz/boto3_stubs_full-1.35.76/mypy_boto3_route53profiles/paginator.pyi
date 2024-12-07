"""
Type annotations for route53profiles service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53profiles/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53profiles.client import Route53ProfilesClient
    from mypy_boto3_route53profiles.paginator import (
        ListProfileAssociationsPaginator,
        ListProfileResourceAssociationsPaginator,
        ListProfilesPaginator,
    )

    session = Session()
    client: Route53ProfilesClient = session.client("route53profiles")

    list_profile_associations_paginator: ListProfileAssociationsPaginator = client.get_paginator("list_profile_associations")
    list_profile_resource_associations_paginator: ListProfileResourceAssociationsPaginator = client.get_paginator("list_profile_resource_associations")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListProfileAssociationsRequestListProfileAssociationsPaginateTypeDef,
    ListProfileAssociationsResponseTypeDef,
    ListProfileResourceAssociationsRequestListProfileResourceAssociationsPaginateTypeDef,
    ListProfileResourceAssociationsResponseTypeDef,
    ListProfilesRequestListProfilesPaginateTypeDef,
    ListProfilesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListProfileAssociationsPaginator",
    "ListProfileResourceAssociationsPaginator",
    "ListProfilesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListProfileAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileAssociations.html#Route53Profiles.Paginator.ListProfileAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53profiles/paginators/#listprofileassociationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProfileAssociationsRequestListProfileAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListProfileAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileAssociations.html#Route53Profiles.Paginator.ListProfileAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53profiles/paginators/#listprofileassociationspaginator)
        """

class ListProfileResourceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileResourceAssociations.html#Route53Profiles.Paginator.ListProfileResourceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53profiles/paginators/#listprofileresourceassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProfileResourceAssociationsRequestListProfileResourceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListProfileResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileResourceAssociations.html#Route53Profiles.Paginator.ListProfileResourceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53profiles/paginators/#listprofileresourceassociationspaginator)
        """

class ListProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfiles.html#Route53Profiles.Paginator.ListProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53profiles/paginators/#listprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProfilesRequestListProfilesPaginateTypeDef]
    ) -> _PageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfiles.html#Route53Profiles.Paginator.ListProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53profiles/paginators/#listprofilespaginator)
        """
