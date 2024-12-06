"""
Type annotations for wisdom service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_wisdom.client import ConnectWisdomServiceClient
    from mypy_boto3_wisdom.paginator import (
        ListAssistantAssociationsPaginator,
        ListAssistantsPaginator,
        ListContentsPaginator,
        ListImportJobsPaginator,
        ListKnowledgeBasesPaginator,
        ListQuickResponsesPaginator,
        QueryAssistantPaginator,
        SearchContentPaginator,
        SearchQuickResponsesPaginator,
        SearchSessionsPaginator,
    )

    session = Session()
    client: ConnectWisdomServiceClient = session.client("wisdom")

    list_assistant_associations_paginator: ListAssistantAssociationsPaginator = client.get_paginator("list_assistant_associations")
    list_assistants_paginator: ListAssistantsPaginator = client.get_paginator("list_assistants")
    list_contents_paginator: ListContentsPaginator = client.get_paginator("list_contents")
    list_import_jobs_paginator: ListImportJobsPaginator = client.get_paginator("list_import_jobs")
    list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
    list_quick_responses_paginator: ListQuickResponsesPaginator = client.get_paginator("list_quick_responses")
    query_assistant_paginator: QueryAssistantPaginator = client.get_paginator("query_assistant")
    search_content_paginator: SearchContentPaginator = client.get_paginator("search_content")
    search_quick_responses_paginator: SearchQuickResponsesPaginator = client.get_paginator("search_quick_responses")
    search_sessions_paginator: SearchSessionsPaginator = client.get_paginator("search_sessions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef,
    ListAssistantAssociationsResponseTypeDef,
    ListAssistantsRequestListAssistantsPaginateTypeDef,
    ListAssistantsResponseTypeDef,
    ListContentsRequestListContentsPaginateTypeDef,
    ListContentsResponseTypeDef,
    ListImportJobsRequestListImportJobsPaginateTypeDef,
    ListImportJobsResponseTypeDef,
    ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListQuickResponsesRequestListQuickResponsesPaginateTypeDef,
    ListQuickResponsesResponseTypeDef,
    QueryAssistantRequestQueryAssistantPaginateTypeDef,
    QueryAssistantResponseTypeDef,
    SearchContentRequestSearchContentPaginateTypeDef,
    SearchContentResponseTypeDef,
    SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef,
    SearchQuickResponsesResponseTypeDef,
    SearchSessionsRequestSearchSessionsPaginateTypeDef,
    SearchSessionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssistantAssociationsPaginator",
    "ListAssistantsPaginator",
    "ListContentsPaginator",
    "ListImportJobsPaginator",
    "ListKnowledgeBasesPaginator",
    "ListQuickResponsesPaginator",
    "QueryAssistantPaginator",
    "SearchContentPaginator",
    "SearchQuickResponsesPaginator",
    "SearchSessionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssistantAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistantAssociations.html#ConnectWisdomService.Paginator.ListAssistantAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listassistantassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef],
    ) -> _PageIterator[ListAssistantAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistantAssociations.html#ConnectWisdomService.Paginator.ListAssistantAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listassistantassociationspaginator)
        """


class ListAssistantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistants.html#ConnectWisdomService.Paginator.ListAssistants)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listassistantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssistantsRequestListAssistantsPaginateTypeDef]
    ) -> _PageIterator[ListAssistantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistants.html#ConnectWisdomService.Paginator.ListAssistants.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listassistantspaginator)
        """


class ListContentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListContents.html#ConnectWisdomService.Paginator.ListContents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listcontentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContentsRequestListContentsPaginateTypeDef]
    ) -> _PageIterator[ListContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListContents.html#ConnectWisdomService.Paginator.ListContents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listcontentspaginator)
        """


class ListImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListImportJobs.html#ConnectWisdomService.Paginator.ListImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportJobsRequestListImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListImportJobs.html#ConnectWisdomService.Paginator.ListImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listimportjobspaginator)
        """


class ListKnowledgeBasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListKnowledgeBases.html#ConnectWisdomService.Paginator.ListKnowledgeBases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listknowledgebasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef]
    ) -> _PageIterator[ListKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListKnowledgeBases.html#ConnectWisdomService.Paginator.ListKnowledgeBases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listknowledgebasespaginator)
        """


class ListQuickResponsesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListQuickResponses.html#ConnectWisdomService.Paginator.ListQuickResponses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listquickresponsespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQuickResponsesRequestListQuickResponsesPaginateTypeDef]
    ) -> _PageIterator[ListQuickResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListQuickResponses.html#ConnectWisdomService.Paginator.ListQuickResponses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#listquickresponsespaginator)
        """


class QueryAssistantPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/QueryAssistant.html#ConnectWisdomService.Paginator.QueryAssistant)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#queryassistantpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[QueryAssistantRequestQueryAssistantPaginateTypeDef]
    ) -> _PageIterator[QueryAssistantResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/QueryAssistant.html#ConnectWisdomService.Paginator.QueryAssistant.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#queryassistantpaginator)
        """


class SearchContentPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchContent.html#ConnectWisdomService.Paginator.SearchContent)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#searchcontentpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchContentRequestSearchContentPaginateTypeDef]
    ) -> _PageIterator[SearchContentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchContent.html#ConnectWisdomService.Paginator.SearchContent.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#searchcontentpaginator)
        """


class SearchQuickResponsesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchQuickResponses.html#ConnectWisdomService.Paginator.SearchQuickResponses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#searchquickresponsespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef]
    ) -> _PageIterator[SearchQuickResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchQuickResponses.html#ConnectWisdomService.Paginator.SearchQuickResponses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#searchquickresponsespaginator)
        """


class SearchSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchSessions.html#ConnectWisdomService.Paginator.SearchSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#searchsessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchSessionsRequestSearchSessionsPaginateTypeDef]
    ) -> _PageIterator[SearchSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchSessions.html#ConnectWisdomService.Paginator.SearchSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators/#searchsessionspaginator)
        """
