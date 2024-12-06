"""
Type annotations for elastictranscoder service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elastictranscoder.client import ElasticTranscoderClient
    from mypy_boto3_elastictranscoder.paginator import (
        ListJobsByPipelinePaginator,
        ListJobsByStatusPaginator,
        ListPipelinesPaginator,
        ListPresetsPaginator,
    )

    session = Session()
    client: ElasticTranscoderClient = session.client("elastictranscoder")

    list_jobs_by_pipeline_paginator: ListJobsByPipelinePaginator = client.get_paginator("list_jobs_by_pipeline")
    list_jobs_by_status_paginator: ListJobsByStatusPaginator = client.get_paginator("list_jobs_by_status")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef,
    ListJobsByPipelineResponseTypeDef,
    ListJobsByStatusRequestListJobsByStatusPaginateTypeDef,
    ListJobsByStatusResponseTypeDef,
    ListPipelinesRequestListPipelinesPaginateTypeDef,
    ListPipelinesResponseTypeDef,
    ListPresetsRequestListPresetsPaginateTypeDef,
    ListPresetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListJobsByPipelinePaginator",
    "ListJobsByStatusPaginator",
    "ListPipelinesPaginator",
    "ListPresetsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobsByPipelinePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByPipeline.html#ElasticTranscoder.Paginator.ListJobsByPipeline)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listjobsbypipelinepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef]
    ) -> _PageIterator[ListJobsByPipelineResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByPipeline.html#ElasticTranscoder.Paginator.ListJobsByPipeline.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listjobsbypipelinepaginator)
        """

class ListJobsByStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByStatus.html#ElasticTranscoder.Paginator.ListJobsByStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listjobsbystatuspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsByStatusRequestListJobsByStatusPaginateTypeDef]
    ) -> _PageIterator[ListJobsByStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByStatus.html#ElasticTranscoder.Paginator.ListJobsByStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listjobsbystatuspaginator)
        """

class ListPipelinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPipelines.html#ElasticTranscoder.Paginator.ListPipelines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listpipelinespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPipelinesRequestListPipelinesPaginateTypeDef]
    ) -> _PageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPipelines.html#ElasticTranscoder.Paginator.ListPipelines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listpipelinespaginator)
        """

class ListPresetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPresets.html#ElasticTranscoder.Paginator.ListPresets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listpresetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPresetsRequestListPresetsPaginateTypeDef]
    ) -> _PageIterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPresets.html#ElasticTranscoder.Paginator.ListPresets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/paginators/#listpresetspaginator)
        """
