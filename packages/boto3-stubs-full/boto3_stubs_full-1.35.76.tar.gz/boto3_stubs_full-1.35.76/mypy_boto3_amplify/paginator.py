"""
Type annotations for amplify service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_amplify.client import AmplifyClient
    from mypy_boto3_amplify.paginator import (
        ListAppsPaginator,
        ListBranchesPaginator,
        ListDomainAssociationsPaginator,
        ListJobsPaginator,
    )

    session = Session()
    client: AmplifyClient = session.client("amplify")

    list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
    list_branches_paginator: ListBranchesPaginator = client.get_paginator("list_branches")
    list_domain_associations_paginator: ListDomainAssociationsPaginator = client.get_paginator("list_domain_associations")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAppsRequestListAppsPaginateTypeDef,
    ListAppsResultTypeDef,
    ListBranchesRequestListBranchesPaginateTypeDef,
    ListBranchesResultTypeDef,
    ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef,
    ListDomainAssociationsResultTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAppsPaginator",
    "ListBranchesPaginator",
    "ListDomainAssociationsPaginator",
    "ListJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListApps.html#Amplify.Paginator.ListApps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listappspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppsRequestListAppsPaginateTypeDef]
    ) -> _PageIterator[ListAppsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListApps.html#Amplify.Paginator.ListApps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listappspaginator)
        """


class ListBranchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListBranches.html#Amplify.Paginator.ListBranches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listbranchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBranchesRequestListBranchesPaginateTypeDef]
    ) -> _PageIterator[ListBranchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListBranches.html#Amplify.Paginator.ListBranches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listbranchespaginator)
        """


class ListDomainAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListDomainAssociations.html#Amplify.Paginator.ListDomainAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listdomainassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListDomainAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListDomainAssociations.html#Amplify.Paginator.ListDomainAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listdomainassociationspaginator)
        """


class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListJobs.html#Amplify.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListJobs.html#Amplify.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/paginators/#listjobspaginator)
        """
