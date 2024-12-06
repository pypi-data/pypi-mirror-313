"""
Type annotations for codecatalyst service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codecatalyst.client import CodeCatalystClient
    from mypy_boto3_codecatalyst.paginator import (
        ListAccessTokensPaginator,
        ListDevEnvironmentSessionsPaginator,
        ListDevEnvironmentsPaginator,
        ListEventLogsPaginator,
        ListProjectsPaginator,
        ListSourceRepositoriesPaginator,
        ListSourceRepositoryBranchesPaginator,
        ListSpacesPaginator,
        ListWorkflowRunsPaginator,
        ListWorkflowsPaginator,
    )

    session = Session()
    client: CodeCatalystClient = session.client("codecatalyst")

    list_access_tokens_paginator: ListAccessTokensPaginator = client.get_paginator("list_access_tokens")
    list_dev_environment_sessions_paginator: ListDevEnvironmentSessionsPaginator = client.get_paginator("list_dev_environment_sessions")
    list_dev_environments_paginator: ListDevEnvironmentsPaginator = client.get_paginator("list_dev_environments")
    list_event_logs_paginator: ListEventLogsPaginator = client.get_paginator("list_event_logs")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_source_repositories_paginator: ListSourceRepositoriesPaginator = client.get_paginator("list_source_repositories")
    list_source_repository_branches_paginator: ListSourceRepositoryBranchesPaginator = client.get_paginator("list_source_repository_branches")
    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    list_workflow_runs_paginator: ListWorkflowRunsPaginator = client.get_paginator("list_workflow_runs")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccessTokensRequestListAccessTokensPaginateTypeDef,
    ListAccessTokensResponseTypeDef,
    ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef,
    ListDevEnvironmentSessionsResponseTypeDef,
    ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef,
    ListDevEnvironmentsResponseTypeDef,
    ListEventLogsRequestListEventLogsPaginateTypeDef,
    ListEventLogsResponseTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResponseTypeDef,
    ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef,
    ListSourceRepositoriesResponseTypeDef,
    ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef,
    ListSourceRepositoryBranchesResponseTypeDef,
    ListSpacesRequestListSpacesPaginateTypeDef,
    ListSpacesResponseTypeDef,
    ListWorkflowRunsRequestListWorkflowRunsPaginateTypeDef,
    ListWorkflowRunsResponseTypeDef,
    ListWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccessTokensPaginator",
    "ListDevEnvironmentSessionsPaginator",
    "ListDevEnvironmentsPaginator",
    "ListEventLogsPaginator",
    "ListProjectsPaginator",
    "ListSourceRepositoriesPaginator",
    "ListSourceRepositoryBranchesPaginator",
    "ListSpacesPaginator",
    "ListWorkflowRunsPaginator",
    "ListWorkflowsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccessTokensPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListAccessTokens.html#CodeCatalyst.Paginator.ListAccessTokens)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listaccesstokenspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAccessTokensRequestListAccessTokensPaginateTypeDef]
    ) -> _PageIterator[ListAccessTokensResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListAccessTokens.html#CodeCatalyst.Paginator.ListAccessTokens.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listaccesstokenspaginator)
        """


class ListDevEnvironmentSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironmentSessions.html#CodeCatalyst.Paginator.ListDevEnvironmentSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listdevenvironmentsessionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDevEnvironmentSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironmentSessions.html#CodeCatalyst.Paginator.ListDevEnvironmentSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listdevenvironmentsessionspaginator)
        """


class ListDevEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironments.html#CodeCatalyst.Paginator.ListDevEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listdevenvironmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[ListDevEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironments.html#CodeCatalyst.Paginator.ListDevEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listdevenvironmentspaginator)
        """


class ListEventLogsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListEventLogs.html#CodeCatalyst.Paginator.ListEventLogs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listeventlogspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventLogsRequestListEventLogsPaginateTypeDef]
    ) -> _PageIterator[ListEventLogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListEventLogs.html#CodeCatalyst.Paginator.ListEventLogs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listeventlogspaginator)
        """


class ListProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListProjects.html#CodeCatalyst.Paginator.ListProjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listprojectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListProjects.html#CodeCatalyst.Paginator.ListProjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listprojectspaginator)
        """


class ListSourceRepositoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositories.html#CodeCatalyst.Paginator.ListSourceRepositories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listsourcerepositoriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef]
    ) -> _PageIterator[ListSourceRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositories.html#CodeCatalyst.Paginator.ListSourceRepositories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listsourcerepositoriespaginator)
        """


class ListSourceRepositoryBranchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositoryBranches.html#CodeCatalyst.Paginator.ListSourceRepositoryBranches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listsourcerepositorybranchespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef
        ],
    ) -> _PageIterator[ListSourceRepositoryBranchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositoryBranches.html#CodeCatalyst.Paginator.ListSourceRepositoryBranches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listsourcerepositorybranchespaginator)
        """


class ListSpacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSpaces.html#CodeCatalyst.Paginator.ListSpaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listspacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSpacesRequestListSpacesPaginateTypeDef]
    ) -> _PageIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSpaces.html#CodeCatalyst.Paginator.ListSpaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listspacespaginator)
        """


class ListWorkflowRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflowRuns.html#CodeCatalyst.Paginator.ListWorkflowRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listworkflowrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowRunsRequestListWorkflowRunsPaginateTypeDef]
    ) -> _PageIterator[ListWorkflowRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflowRuns.html#CodeCatalyst.Paginator.ListWorkflowRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listworkflowrunspaginator)
        """


class ListWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflows.html#CodeCatalyst.Paginator.ListWorkflows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listworkflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> _PageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflows.html#CodeCatalyst.Paginator.ListWorkflows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/paginators/#listworkflowspaginator)
        """
