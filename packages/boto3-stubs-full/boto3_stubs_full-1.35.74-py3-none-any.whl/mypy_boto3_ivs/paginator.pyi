"""
Type annotations for ivs service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ivs.client import IVSClient
    from mypy_boto3_ivs.paginator import (
        ListChannelsPaginator,
        ListPlaybackKeyPairsPaginator,
        ListRecordingConfigurationsPaginator,
        ListStreamKeysPaginator,
        ListStreamsPaginator,
    )

    session = Session()
    client: IVSClient = session.client("ivs")

    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_playback_key_pairs_paginator: ListPlaybackKeyPairsPaginator = client.get_paginator("list_playback_key_pairs")
    list_recording_configurations_paginator: ListRecordingConfigurationsPaginator = client.get_paginator("list_recording_configurations")
    list_stream_keys_paginator: ListStreamKeysPaginator = client.get_paginator("list_stream_keys")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef,
    ListPlaybackKeyPairsResponseTypeDef,
    ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef,
    ListRecordingConfigurationsResponseTypeDef,
    ListStreamKeysRequestListStreamKeysPaginateTypeDef,
    ListStreamKeysResponseTypeDef,
    ListStreamsRequestListStreamsPaginateTypeDef,
    ListStreamsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListChannelsPaginator",
    "ListPlaybackKeyPairsPaginator",
    "ListRecordingConfigurationsPaginator",
    "ListStreamKeysPaginator",
    "ListStreamsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListChannels.html#IVS.Paginator.ListChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#listchannelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListChannels.html#IVS.Paginator.ListChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#listchannelspaginator)
        """

class ListPlaybackKeyPairsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListPlaybackKeyPairs.html#IVS.Paginator.ListPlaybackKeyPairs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#listplaybackkeypairspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef]
    ) -> _PageIterator[ListPlaybackKeyPairsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListPlaybackKeyPairs.html#IVS.Paginator.ListPlaybackKeyPairs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#listplaybackkeypairspaginator)
        """

class ListRecordingConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListRecordingConfigurations.html#IVS.Paginator.ListRecordingConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#listrecordingconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListRecordingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListRecordingConfigurations.html#IVS.Paginator.ListRecordingConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#listrecordingconfigurationspaginator)
        """

class ListStreamKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreamKeys.html#IVS.Paginator.ListStreamKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#liststreamkeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamKeysRequestListStreamKeysPaginateTypeDef]
    ) -> _PageIterator[ListStreamKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreamKeys.html#IVS.Paginator.ListStreamKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#liststreamkeyspaginator)
        """

class ListStreamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreams.html#IVS.Paginator.ListStreams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#liststreamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamsRequestListStreamsPaginateTypeDef]
    ) -> _PageIterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreams.html#IVS.Paginator.ListStreams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/paginators/#liststreamspaginator)
        """
