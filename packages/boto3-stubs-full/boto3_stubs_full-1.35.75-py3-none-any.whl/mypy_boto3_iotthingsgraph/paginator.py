"""
Type annotations for iotthingsgraph service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iotthingsgraph.client import IoTThingsGraphClient
    from mypy_boto3_iotthingsgraph.paginator import (
        GetFlowTemplateRevisionsPaginator,
        GetSystemTemplateRevisionsPaginator,
        ListFlowExecutionMessagesPaginator,
        ListTagsForResourcePaginator,
        SearchEntitiesPaginator,
        SearchFlowExecutionsPaginator,
        SearchFlowTemplatesPaginator,
        SearchSystemInstancesPaginator,
        SearchSystemTemplatesPaginator,
        SearchThingsPaginator,
    )

    session = Session()
    client: IoTThingsGraphClient = session.client("iotthingsgraph")

    get_flow_template_revisions_paginator: GetFlowTemplateRevisionsPaginator = client.get_paginator("get_flow_template_revisions")
    get_system_template_revisions_paginator: GetSystemTemplateRevisionsPaginator = client.get_paginator("get_system_template_revisions")
    list_flow_execution_messages_paginator: ListFlowExecutionMessagesPaginator = client.get_paginator("list_flow_execution_messages")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    search_entities_paginator: SearchEntitiesPaginator = client.get_paginator("search_entities")
    search_flow_executions_paginator: SearchFlowExecutionsPaginator = client.get_paginator("search_flow_executions")
    search_flow_templates_paginator: SearchFlowTemplatesPaginator = client.get_paginator("search_flow_templates")
    search_system_instances_paginator: SearchSystemInstancesPaginator = client.get_paginator("search_system_instances")
    search_system_templates_paginator: SearchSystemTemplatesPaginator = client.get_paginator("search_system_templates")
    search_things_paginator: SearchThingsPaginator = client.get_paginator("search_things")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef,
    GetFlowTemplateRevisionsResponseTypeDef,
    GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef,
    GetSystemTemplateRevisionsResponseTypeDef,
    ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef,
    ListFlowExecutionMessagesResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchEntitiesRequestSearchEntitiesPaginateTypeDef,
    SearchEntitiesResponseTypeDef,
    SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef,
    SearchFlowExecutionsResponseTypeDef,
    SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef,
    SearchFlowTemplatesResponseTypeDef,
    SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef,
    SearchSystemInstancesResponseTypeDef,
    SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef,
    SearchSystemTemplatesResponseTypeDef,
    SearchThingsRequestSearchThingsPaginateTypeDef,
    SearchThingsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetFlowTemplateRevisionsPaginator",
    "GetSystemTemplateRevisionsPaginator",
    "ListFlowExecutionMessagesPaginator",
    "ListTagsForResourcePaginator",
    "SearchEntitiesPaginator",
    "SearchFlowExecutionsPaginator",
    "SearchFlowTemplatesPaginator",
    "SearchSystemInstancesPaginator",
    "SearchSystemTemplatesPaginator",
    "SearchThingsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetFlowTemplateRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetFlowTemplateRevisions.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#getflowtemplaterevisionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef],
    ) -> _PageIterator[GetFlowTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetFlowTemplateRevisions.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#getflowtemplaterevisionspaginator)
        """


class GetSystemTemplateRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetSystemTemplateRevisions.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#getsystemtemplaterevisionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef
        ],
    ) -> _PageIterator[GetSystemTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetSystemTemplateRevisions.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#getsystemtemplaterevisionspaginator)
        """


class ListFlowExecutionMessagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListFlowExecutionMessages.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#listflowexecutionmessagespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef],
    ) -> _PageIterator[ListFlowExecutionMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListFlowExecutionMessages.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#listflowexecutionmessagespaginator)
        """


class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListTagsForResource.html#IoTThingsGraph.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListTagsForResource.html#IoTThingsGraph.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#listtagsforresourcepaginator)
        """


class SearchEntitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchEntities.html#IoTThingsGraph.Paginator.SearchEntities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchentitiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchEntitiesRequestSearchEntitiesPaginateTypeDef]
    ) -> _PageIterator[SearchEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchEntities.html#IoTThingsGraph.Paginator.SearchEntities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchentitiespaginator)
        """


class SearchFlowExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowExecutions.html#IoTThingsGraph.Paginator.SearchFlowExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchflowexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef]
    ) -> _PageIterator[SearchFlowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowExecutions.html#IoTThingsGraph.Paginator.SearchFlowExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchflowexecutionspaginator)
        """


class SearchFlowTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowTemplates.html#IoTThingsGraph.Paginator.SearchFlowTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchflowtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef]
    ) -> _PageIterator[SearchFlowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowTemplates.html#IoTThingsGraph.Paginator.SearchFlowTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchflowtemplatespaginator)
        """


class SearchSystemInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemInstances.html#IoTThingsGraph.Paginator.SearchSystemInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchsysteminstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef]
    ) -> _PageIterator[SearchSystemInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemInstances.html#IoTThingsGraph.Paginator.SearchSystemInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchsysteminstancespaginator)
        """


class SearchSystemTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemTemplates.html#IoTThingsGraph.Paginator.SearchSystemTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchsystemtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef]
    ) -> _PageIterator[SearchSystemTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemTemplates.html#IoTThingsGraph.Paginator.SearchSystemTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchsystemtemplatespaginator)
        """


class SearchThingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchThings.html#IoTThingsGraph.Paginator.SearchThings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchthingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchThingsRequestSearchThingsPaginateTypeDef]
    ) -> _PageIterator[SearchThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchThings.html#IoTThingsGraph.Paginator.SearchThings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/paginators/#searchthingspaginator)
        """
