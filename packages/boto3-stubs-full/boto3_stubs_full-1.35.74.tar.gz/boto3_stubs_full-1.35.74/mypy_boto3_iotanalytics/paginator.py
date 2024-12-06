"""
Type annotations for iotanalytics service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iotanalytics.client import IoTAnalyticsClient
    from mypy_boto3_iotanalytics.paginator import (
        ListChannelsPaginator,
        ListDatasetContentsPaginator,
        ListDatasetsPaginator,
        ListDatastoresPaginator,
        ListPipelinesPaginator,
    )

    session = Session()
    client: IoTAnalyticsClient = session.client("iotanalytics")

    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_dataset_contents_paginator: ListDatasetContentsPaginator = client.get_paginator("list_dataset_contents")
    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_datastores_paginator: ListDatastoresPaginator = client.get_paginator("list_datastores")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListDatasetContentsRequestListDatasetContentsPaginateTypeDef,
    ListDatasetContentsResponseTypeDef,
    ListDatasetsRequestListDatasetsPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListDatastoresRequestListDatastoresPaginateTypeDef,
    ListDatastoresResponseTypeDef,
    ListPipelinesRequestListPipelinesPaginateTypeDef,
    ListPipelinesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChannelsPaginator",
    "ListDatasetContentsPaginator",
    "ListDatasetsPaginator",
    "ListDatastoresPaginator",
    "ListPipelinesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListChannels.html#IoTAnalytics.Paginator.ListChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listchannelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListChannels.html#IoTAnalytics.Paginator.ListChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listchannelspaginator)
        """


class ListDatasetContentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasetContents.html#IoTAnalytics.Paginator.ListDatasetContents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listdatasetcontentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatasetContentsRequestListDatasetContentsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasetContents.html#IoTAnalytics.Paginator.ListDatasetContents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listdatasetcontentspaginator)
        """


class ListDatasetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasets.html#IoTAnalytics.Paginator.ListDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatasetsRequestListDatasetsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasets.html#IoTAnalytics.Paginator.ListDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listdatasetspaginator)
        """


class ListDatastoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatastores.html#IoTAnalytics.Paginator.ListDatastores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listdatastorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatastoresRequestListDatastoresPaginateTypeDef]
    ) -> _PageIterator[ListDatastoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatastores.html#IoTAnalytics.Paginator.ListDatastores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listdatastorespaginator)
        """


class ListPipelinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListPipelines.html#IoTAnalytics.Paginator.ListPipelines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listpipelinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPipelinesRequestListPipelinesPaginateTypeDef]
    ) -> _PageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListPipelines.html#IoTAnalytics.Paginator.ListPipelines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/paginators/#listpipelinespaginator)
        """
