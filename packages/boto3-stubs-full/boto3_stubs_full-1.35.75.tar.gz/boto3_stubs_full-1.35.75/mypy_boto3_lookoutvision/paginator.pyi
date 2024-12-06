"""
Type annotations for lookoutvision service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lookoutvision.client import LookoutforVisionClient
    from mypy_boto3_lookoutvision.paginator import (
        ListDatasetEntriesPaginator,
        ListModelPackagingJobsPaginator,
        ListModelsPaginator,
        ListProjectsPaginator,
    )

    session = Session()
    client: LookoutforVisionClient = session.client("lookoutvision")

    list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
    list_model_packaging_jobs_paginator: ListModelPackagingJobsPaginator = client.get_paginator("list_model_packaging_jobs")
    list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef,
    ListModelPackagingJobsResponseTypeDef,
    ListModelsRequestListModelsPaginateTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDatasetEntriesPaginator",
    "ListModelPackagingJobsPaginator",
    "ListModelsPaginator",
    "ListProjectsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDatasetEntriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListDatasetEntries.html#LookoutforVision.Paginator.ListDatasetEntries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listdatasetentriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef]
    ) -> _PageIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListDatasetEntries.html#LookoutforVision.Paginator.ListDatasetEntries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listdatasetentriespaginator)
        """

class ListModelPackagingJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModelPackagingJobs.html#LookoutforVision.Paginator.ListModelPackagingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listmodelpackagingjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef]
    ) -> _PageIterator[ListModelPackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModelPackagingJobs.html#LookoutforVision.Paginator.ListModelPackagingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listmodelpackagingjobspaginator)
        """

class ListModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModels.html#LookoutforVision.Paginator.ListModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listmodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelsRequestListModelsPaginateTypeDef]
    ) -> _PageIterator[ListModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModels.html#LookoutforVision.Paginator.ListModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listmodelspaginator)
        """

class ListProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListProjects.html#LookoutforVision.Paginator.ListProjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListProjects.html#LookoutforVision.Paginator.ListProjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators/#listprojectspaginator)
        """
