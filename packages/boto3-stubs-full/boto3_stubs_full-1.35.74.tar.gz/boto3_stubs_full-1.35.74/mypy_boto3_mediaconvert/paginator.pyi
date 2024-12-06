"""
Type annotations for mediaconvert service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediaconvert.client import MediaConvertClient
    from mypy_boto3_mediaconvert.paginator import (
        DescribeEndpointsPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListPresetsPaginator,
        ListQueuesPaginator,
        ListVersionsPaginator,
        SearchJobsPaginator,
    )

    session = Session()
    client: MediaConvertClient = session.client("mediaconvert")

    describe_endpoints_paginator: DescribeEndpointsPaginator = client.get_paginator("describe_endpoints")
    list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    list_versions_paginator: ListVersionsPaginator = client.get_paginator("list_versions")
    search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef,
    DescribeEndpointsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestListJobTemplatesPaginateTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListPresetsRequestListPresetsPaginateTypeDef,
    ListPresetsResponseTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListVersionsRequestListVersionsPaginateTypeDef,
    ListVersionsResponseTypeDef,
    SearchJobsRequestSearchJobsPaginateTypeDef,
    SearchJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeEndpointsPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListPresetsPaginator",
    "ListQueuesPaginator",
    "ListVersionsPaginator",
    "SearchJobsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/DescribeEndpoints.html#MediaConvert.Paginator.DescribeEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#describeendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef]
    ) -> _PageIterator[DescribeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/DescribeEndpoints.html#MediaConvert.Paginator.DescribeEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#describeendpointspaginator)
        """

class ListJobTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobTemplates.html#MediaConvert.Paginator.ListJobTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listjobtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobTemplatesRequestListJobTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobTemplates.html#MediaConvert.Paginator.ListJobTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listjobtemplatespaginator)
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobs.html#MediaConvert.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobs.html#MediaConvert.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listjobspaginator)
        """

class ListPresetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListPresets.html#MediaConvert.Paginator.ListPresets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listpresetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPresetsRequestListPresetsPaginateTypeDef]
    ) -> _PageIterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListPresets.html#MediaConvert.Paginator.ListPresets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listpresetspaginator)
        """

class ListQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListQueues.html#MediaConvert.Paginator.ListQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listqueuespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> _PageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListQueues.html#MediaConvert.Paginator.ListQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listqueuespaginator)
        """

class ListVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListVersions.html#MediaConvert.Paginator.ListVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVersionsRequestListVersionsPaginateTypeDef]
    ) -> _PageIterator[ListVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListVersions.html#MediaConvert.Paginator.ListVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#listversionspaginator)
        """

class SearchJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/SearchJobs.html#MediaConvert.Paginator.SearchJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#searchjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchJobsRequestSearchJobsPaginateTypeDef]
    ) -> _PageIterator[SearchJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/SearchJobs.html#MediaConvert.Paginator.SearchJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/paginators/#searchjobspaginator)
        """
