"""
Type annotations for batch service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_batch.client import BatchClient
    from mypy_boto3_batch.paginator import (
        DescribeComputeEnvironmentsPaginator,
        DescribeJobDefinitionsPaginator,
        DescribeJobQueuesPaginator,
        ListJobsPaginator,
        ListSchedulingPoliciesPaginator,
    )

    session = Session()
    client: BatchClient = session.client("batch")

    describe_compute_environments_paginator: DescribeComputeEnvironmentsPaginator = client.get_paginator("describe_compute_environments")
    describe_job_definitions_paginator: DescribeJobDefinitionsPaginator = client.get_paginator("describe_job_definitions")
    describe_job_queues_paginator: DescribeJobQueuesPaginator = client.get_paginator("describe_job_queues")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_scheduling_policies_paginator: ListSchedulingPoliciesPaginator = client.get_paginator("list_scheduling_policies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeComputeEnvironmentsRequestDescribeComputeEnvironmentsPaginateTypeDef,
    DescribeComputeEnvironmentsResponseTypeDef,
    DescribeJobDefinitionsRequestDescribeJobDefinitionsPaginateTypeDef,
    DescribeJobDefinitionsResponseTypeDef,
    DescribeJobQueuesRequestDescribeJobQueuesPaginateTypeDef,
    DescribeJobQueuesResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListSchedulingPoliciesRequestListSchedulingPoliciesPaginateTypeDef,
    ListSchedulingPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeComputeEnvironmentsPaginator",
    "DescribeJobDefinitionsPaginator",
    "DescribeJobQueuesPaginator",
    "ListJobsPaginator",
    "ListSchedulingPoliciesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeComputeEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeComputeEnvironments.html#Batch.Paginator.DescribeComputeEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#describecomputeenvironmentspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeComputeEnvironmentsRequestDescribeComputeEnvironmentsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeComputeEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeComputeEnvironments.html#Batch.Paginator.DescribeComputeEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#describecomputeenvironmentspaginator)
        """

class DescribeJobDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobDefinitions.html#Batch.Paginator.DescribeJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#describejobdefinitionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeJobDefinitionsRequestDescribeJobDefinitionsPaginateTypeDef]
    ) -> _PageIterator[DescribeJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobDefinitions.html#Batch.Paginator.DescribeJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#describejobdefinitionspaginator)
        """

class DescribeJobQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobQueues.html#Batch.Paginator.DescribeJobQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#describejobqueuespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeJobQueuesRequestDescribeJobQueuesPaginateTypeDef]
    ) -> _PageIterator[DescribeJobQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobQueues.html#Batch.Paginator.DescribeJobQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#describejobqueuespaginator)
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListJobs.html#Batch.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListJobs.html#Batch.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#listjobspaginator)
        """

class ListSchedulingPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListSchedulingPolicies.html#Batch.Paginator.ListSchedulingPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#listschedulingpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchedulingPoliciesRequestListSchedulingPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListSchedulingPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListSchedulingPolicies.html#Batch.Paginator.ListSchedulingPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators/#listschedulingpoliciespaginator)
        """
