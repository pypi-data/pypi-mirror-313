"""
Type annotations for swf service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_swf.client import SWFClient
    from mypy_boto3_swf.paginator import (
        GetWorkflowExecutionHistoryPaginator,
        ListActivityTypesPaginator,
        ListClosedWorkflowExecutionsPaginator,
        ListDomainsPaginator,
        ListOpenWorkflowExecutionsPaginator,
        ListWorkflowTypesPaginator,
        PollForDecisionTaskPaginator,
    )

    session = Session()
    client: SWFClient = session.client("swf")

    get_workflow_execution_history_paginator: GetWorkflowExecutionHistoryPaginator = client.get_paginator("get_workflow_execution_history")
    list_activity_types_paginator: ListActivityTypesPaginator = client.get_paginator("list_activity_types")
    list_closed_workflow_executions_paginator: ListClosedWorkflowExecutionsPaginator = client.get_paginator("list_closed_workflow_executions")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_open_workflow_executions_paginator: ListOpenWorkflowExecutionsPaginator = client.get_paginator("list_open_workflow_executions")
    list_workflow_types_paginator: ListWorkflowTypesPaginator = client.get_paginator("list_workflow_types")
    poll_for_decision_task_paginator: PollForDecisionTaskPaginator = client.get_paginator("poll_for_decision_task")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ActivityTypeInfosTypeDef,
    DecisionTaskTypeDef,
    DomainInfosTypeDef,
    GetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef,
    HistoryTypeDef,
    ListActivityTypesInputListActivityTypesPaginateTypeDef,
    ListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef,
    ListDomainsInputListDomainsPaginateTypeDef,
    ListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef,
    ListWorkflowTypesInputListWorkflowTypesPaginateTypeDef,
    PollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowTypeInfosTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetWorkflowExecutionHistoryPaginator",
    "ListActivityTypesPaginator",
    "ListClosedWorkflowExecutionsPaginator",
    "ListDomainsPaginator",
    "ListOpenWorkflowExecutionsPaginator",
    "ListWorkflowTypesPaginator",
    "PollForDecisionTaskPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetWorkflowExecutionHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/GetWorkflowExecutionHistory.html#SWF.Paginator.GetWorkflowExecutionHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#getworkflowexecutionhistorypaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef
        ],
    ) -> _PageIterator[HistoryTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/GetWorkflowExecutionHistory.html#SWF.Paginator.GetWorkflowExecutionHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#getworkflowexecutionhistorypaginator)
        """

class ListActivityTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListActivityTypes.html#SWF.Paginator.ListActivityTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listactivitytypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListActivityTypesInputListActivityTypesPaginateTypeDef]
    ) -> _PageIterator[ActivityTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListActivityTypes.html#SWF.Paginator.ListActivityTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listactivitytypespaginator)
        """

class ListClosedWorkflowExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListClosedWorkflowExecutions.html#SWF.Paginator.ListClosedWorkflowExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listclosedworkflowexecutionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef
        ],
    ) -> _PageIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListClosedWorkflowExecutions.html#SWF.Paginator.ListClosedWorkflowExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listclosedworkflowexecutionspaginator)
        """

class ListDomainsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListDomains.html#SWF.Paginator.ListDomains)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listdomainspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainsInputListDomainsPaginateTypeDef]
    ) -> _PageIterator[DomainInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListDomains.html#SWF.Paginator.ListDomains.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listdomainspaginator)
        """

class ListOpenWorkflowExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListOpenWorkflowExecutions.html#SWF.Paginator.ListOpenWorkflowExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listopenworkflowexecutionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef],
    ) -> _PageIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListOpenWorkflowExecutions.html#SWF.Paginator.ListOpenWorkflowExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listopenworkflowexecutionspaginator)
        """

class ListWorkflowTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListWorkflowTypes.html#SWF.Paginator.ListWorkflowTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listworkflowtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkflowTypesInputListWorkflowTypesPaginateTypeDef]
    ) -> _PageIterator[WorkflowTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListWorkflowTypes.html#SWF.Paginator.ListWorkflowTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#listworkflowtypespaginator)
        """

class PollForDecisionTaskPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/PollForDecisionTask.html#SWF.Paginator.PollForDecisionTask)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#pollfordecisiontaskpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[PollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef]
    ) -> _PageIterator[DecisionTaskTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/PollForDecisionTask.html#SWF.Paginator.PollForDecisionTask.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/paginators/#pollfordecisiontaskpaginator)
        """
