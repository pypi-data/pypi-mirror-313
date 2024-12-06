"""
Type annotations for datapipeline service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_datapipeline.client import DataPipelineClient
    from mypy_boto3_datapipeline.paginator import (
        DescribeObjectsPaginator,
        ListPipelinesPaginator,
        QueryObjectsPaginator,
    )

    session = Session()
    client: DataPipelineClient = session.client("datapipeline")

    describe_objects_paginator: DescribeObjectsPaginator = client.get_paginator("describe_objects")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    query_objects_paginator: QueryObjectsPaginator = client.get_paginator("query_objects")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeObjectsInputDescribeObjectsPaginateTypeDef,
    DescribeObjectsOutputTypeDef,
    ListPipelinesInputListPipelinesPaginateTypeDef,
    ListPipelinesOutputTypeDef,
    QueryObjectsInputQueryObjectsPaginateTypeDef,
    QueryObjectsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeObjectsPaginator", "ListPipelinesPaginator", "QueryObjectsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeObjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/DescribeObjects.html#DataPipeline.Paginator.DescribeObjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/paginators/#describeobjectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeObjectsInputDescribeObjectsPaginateTypeDef]
    ) -> _PageIterator[DescribeObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/DescribeObjects.html#DataPipeline.Paginator.DescribeObjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/paginators/#describeobjectspaginator)
        """


class ListPipelinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/ListPipelines.html#DataPipeline.Paginator.ListPipelines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/paginators/#listpipelinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPipelinesInputListPipelinesPaginateTypeDef]
    ) -> _PageIterator[ListPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/ListPipelines.html#DataPipeline.Paginator.ListPipelines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/paginators/#listpipelinespaginator)
        """


class QueryObjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/QueryObjects.html#DataPipeline.Paginator.QueryObjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/paginators/#queryobjectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[QueryObjectsInputQueryObjectsPaginateTypeDef]
    ) -> _PageIterator[QueryObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/QueryObjects.html#DataPipeline.Paginator.QueryObjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/paginators/#queryobjectspaginator)
        """
