"""
Type annotations for codecommit service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codecommit.client import CodeCommitClient
    from mypy_boto3_codecommit.paginator import (
        DescribePullRequestEventsPaginator,
        GetCommentsForComparedCommitPaginator,
        GetCommentsForPullRequestPaginator,
        GetDifferencesPaginator,
        ListBranchesPaginator,
        ListPullRequestsPaginator,
        ListRepositoriesPaginator,
    )

    session = Session()
    client: CodeCommitClient = session.client("codecommit")

    describe_pull_request_events_paginator: DescribePullRequestEventsPaginator = client.get_paginator("describe_pull_request_events")
    get_comments_for_compared_commit_paginator: GetCommentsForComparedCommitPaginator = client.get_paginator("get_comments_for_compared_commit")
    get_comments_for_pull_request_paginator: GetCommentsForPullRequestPaginator = client.get_paginator("get_comments_for_pull_request")
    get_differences_paginator: GetDifferencesPaginator = client.get_paginator("get_differences")
    list_branches_paginator: ListBranchesPaginator = client.get_paginator("list_branches")
    list_pull_requests_paginator: ListPullRequestsPaginator = client.get_paginator("list_pull_requests")
    list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef,
    DescribePullRequestEventsOutputTypeDef,
    GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetDifferencesInputGetDifferencesPaginateTypeDef,
    GetDifferencesOutputTypeDef,
    ListBranchesInputListBranchesPaginateTypeDef,
    ListBranchesOutputTypeDef,
    ListPullRequestsInputListPullRequestsPaginateTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesInputListRepositoriesPaginateTypeDef,
    ListRepositoriesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribePullRequestEventsPaginator",
    "GetCommentsForComparedCommitPaginator",
    "GetCommentsForPullRequestPaginator",
    "GetDifferencesPaginator",
    "ListBranchesPaginator",
    "ListPullRequestsPaginator",
    "ListRepositoriesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribePullRequestEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#describepullrequesteventspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef],
    ) -> _PageIterator[DescribePullRequestEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#describepullrequesteventspaginator)
        """

class GetCommentsForComparedCommitPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef
        ],
    ) -> _PageIterator[GetCommentsForComparedCommitOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
        """

class GetCommentsForPullRequestPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforpullrequestpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef],
    ) -> _PageIterator[GetCommentsForPullRequestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforpullrequestpaginator)
        """

class GetDifferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getdifferencespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDifferencesInputGetDifferencesPaginateTypeDef]
    ) -> _PageIterator[GetDifferencesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getdifferencespaginator)
        """

class ListBranchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listbranchespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBranchesInputListBranchesPaginateTypeDef]
    ) -> _PageIterator[ListBranchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listbranchespaginator)
        """

class ListPullRequestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listpullrequestspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPullRequestsInputListPullRequestsPaginateTypeDef]
    ) -> _PageIterator[ListPullRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listpullrequestspaginator)
        """

class ListRepositoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listrepositoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRepositoriesInputListRepositoriesPaginateTypeDef]
    ) -> _PageIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listrepositoriespaginator)
        """
