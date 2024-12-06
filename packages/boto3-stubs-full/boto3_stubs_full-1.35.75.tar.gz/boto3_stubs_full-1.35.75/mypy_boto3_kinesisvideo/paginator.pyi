"""
Type annotations for kinesisvideo service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_kinesisvideo.client import KinesisVideoClient
    from mypy_boto3_kinesisvideo.paginator import (
        DescribeMappedResourceConfigurationPaginator,
        ListEdgeAgentConfigurationsPaginator,
        ListSignalingChannelsPaginator,
        ListStreamsPaginator,
    )

    session = Session()
    client: KinesisVideoClient = session.client("kinesisvideo")

    describe_mapped_resource_configuration_paginator: DescribeMappedResourceConfigurationPaginator = client.get_paginator("describe_mapped_resource_configuration")
    list_edge_agent_configurations_paginator: ListEdgeAgentConfigurationsPaginator = client.get_paginator("list_edge_agent_configurations")
    list_signaling_channels_paginator: ListSignalingChannelsPaginator = client.get_paginator("list_signaling_channels")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeMappedResourceConfigurationInputDescribeMappedResourceConfigurationPaginateTypeDef,
    DescribeMappedResourceConfigurationOutputTypeDef,
    ListEdgeAgentConfigurationsInputListEdgeAgentConfigurationsPaginateTypeDef,
    ListEdgeAgentConfigurationsOutputTypeDef,
    ListSignalingChannelsInputListSignalingChannelsPaginateTypeDef,
    ListSignalingChannelsOutputTypeDef,
    ListStreamsInputListStreamsPaginateTypeDef,
    ListStreamsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeMappedResourceConfigurationPaginator",
    "ListEdgeAgentConfigurationsPaginator",
    "ListSignalingChannelsPaginator",
    "ListStreamsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeMappedResourceConfigurationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/DescribeMappedResourceConfiguration.html#KinesisVideo.Paginator.DescribeMappedResourceConfiguration)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#describemappedresourceconfigurationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMappedResourceConfigurationInputDescribeMappedResourceConfigurationPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMappedResourceConfigurationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/DescribeMappedResourceConfiguration.html#KinesisVideo.Paginator.DescribeMappedResourceConfiguration.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#describemappedresourceconfigurationpaginator)
        """

class ListEdgeAgentConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListEdgeAgentConfigurations.html#KinesisVideo.Paginator.ListEdgeAgentConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#listedgeagentconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEdgeAgentConfigurationsInputListEdgeAgentConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListEdgeAgentConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListEdgeAgentConfigurations.html#KinesisVideo.Paginator.ListEdgeAgentConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#listedgeagentconfigurationspaginator)
        """

class ListSignalingChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListSignalingChannels.html#KinesisVideo.Paginator.ListSignalingChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#listsignalingchannelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSignalingChannelsInputListSignalingChannelsPaginateTypeDef]
    ) -> _PageIterator[ListSignalingChannelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListSignalingChannels.html#KinesisVideo.Paginator.ListSignalingChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#listsignalingchannelspaginator)
        """

class ListStreamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListStreams.html#KinesisVideo.Paginator.ListStreams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#liststreamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamsInputListStreamsPaginateTypeDef]
    ) -> _PageIterator[ListStreamsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListStreams.html#KinesisVideo.Paginator.ListStreams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators/#liststreamspaginator)
        """
