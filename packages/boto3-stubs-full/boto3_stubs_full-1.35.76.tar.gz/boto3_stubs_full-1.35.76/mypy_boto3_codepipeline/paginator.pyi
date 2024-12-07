"""
Type annotations for codepipeline service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codepipeline.client import CodePipelineClient
    from mypy_boto3_codepipeline.paginator import (
        ListActionExecutionsPaginator,
        ListActionTypesPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelinesPaginator,
        ListRuleExecutionsPaginator,
        ListTagsForResourcePaginator,
        ListWebhooksPaginator,
    )

    session = Session()
    client: CodePipelineClient = session.client("codepipeline")

    list_action_executions_paginator: ListActionExecutionsPaginator = client.get_paginator("list_action_executions")
    list_action_types_paginator: ListActionTypesPaginator = client.get_paginator("list_action_types")
    list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    list_rule_executions_paginator: ListRuleExecutionsPaginator = client.get_paginator("list_rule_executions")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_webhooks_paginator: ListWebhooksPaginator = client.get_paginator("list_webhooks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListActionExecutionsInputListActionExecutionsPaginateTypeDef,
    ListActionExecutionsOutputTypeDef,
    ListActionTypesInputListActionTypesPaginateTypeDef,
    ListActionTypesOutputTypeDef,
    ListPipelineExecutionsInputListPipelineExecutionsPaginateTypeDef,
    ListPipelineExecutionsOutputTypeDef,
    ListPipelinesInputListPipelinesPaginateTypeDef,
    ListPipelinesOutputTypeDef,
    ListRuleExecutionsInputListRuleExecutionsPaginateTypeDef,
    ListRuleExecutionsOutputTypeDef,
    ListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWebhooksInputListWebhooksPaginateTypeDef,
    ListWebhooksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListActionExecutionsPaginator",
    "ListActionTypesPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelinesPaginator",
    "ListRuleExecutionsPaginator",
    "ListTagsForResourcePaginator",
    "ListWebhooksPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListActionExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionExecutions.html#CodePipeline.Paginator.ListActionExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactionexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListActionExecutionsInputListActionExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListActionExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionExecutions.html#CodePipeline.Paginator.ListActionExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactionexecutionspaginator)
        """

class ListActionTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionTypes.html#CodePipeline.Paginator.ListActionTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactiontypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListActionTypesInputListActionTypesPaginateTypeDef]
    ) -> _PageIterator[ListActionTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionTypes.html#CodePipeline.Paginator.ListActionTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactiontypespaginator)
        """

class ListPipelineExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelineExecutions.html#CodePipeline.Paginator.ListPipelineExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelineexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPipelineExecutionsInputListPipelineExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListPipelineExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelineExecutions.html#CodePipeline.Paginator.ListPipelineExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelineexecutionspaginator)
        """

class ListPipelinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelines.html#CodePipeline.Paginator.ListPipelines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelinespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPipelinesInputListPipelinesPaginateTypeDef]
    ) -> _PageIterator[ListPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelines.html#CodePipeline.Paginator.ListPipelines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelinespaginator)
        """

class ListRuleExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListRuleExecutions.html#CodePipeline.Paginator.ListRuleExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listruleexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRuleExecutionsInputListRuleExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListRuleExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListRuleExecutions.html#CodePipeline.Paginator.ListRuleExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listruleexecutionspaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListTagsForResource.html#CodePipeline.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceInputListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListTagsForResource.html#CodePipeline.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listtagsforresourcepaginator)
        """

class ListWebhooksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListWebhooks.html#CodePipeline.Paginator.ListWebhooks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listwebhookspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWebhooksInputListWebhooksPaginateTypeDef]
    ) -> _PageIterator[ListWebhooksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListWebhooks.html#CodePipeline.Paginator.ListWebhooks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listwebhookspaginator)
        """
