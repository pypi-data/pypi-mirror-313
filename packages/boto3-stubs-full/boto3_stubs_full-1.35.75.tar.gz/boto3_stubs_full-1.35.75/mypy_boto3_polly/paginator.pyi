"""
Type annotations for polly service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_polly.client import PollyClient
    from mypy_boto3_polly.paginator import (
        DescribeVoicesPaginator,
        ListLexiconsPaginator,
        ListSpeechSynthesisTasksPaginator,
    )

    session = Session()
    client: PollyClient = session.client("polly")

    describe_voices_paginator: DescribeVoicesPaginator = client.get_paginator("describe_voices")
    list_lexicons_paginator: ListLexiconsPaginator = client.get_paginator("list_lexicons")
    list_speech_synthesis_tasks_paginator: ListSpeechSynthesisTasksPaginator = client.get_paginator("list_speech_synthesis_tasks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeVoicesInputDescribeVoicesPaginateTypeDef,
    DescribeVoicesOutputTypeDef,
    ListLexiconsInputListLexiconsPaginateTypeDef,
    ListLexiconsOutputTypeDef,
    ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef,
    ListSpeechSynthesisTasksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeVoicesPaginator", "ListLexiconsPaginator", "ListSpeechSynthesisTasksPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeVoicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/DescribeVoices.html#Polly.Paginator.DescribeVoices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#describevoicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeVoicesInputDescribeVoicesPaginateTypeDef]
    ) -> _PageIterator[DescribeVoicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/DescribeVoices.html#Polly.Paginator.DescribeVoices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#describevoicespaginator)
        """

class ListLexiconsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListLexicons.html#Polly.Paginator.ListLexicons)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listlexiconspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLexiconsInputListLexiconsPaginateTypeDef]
    ) -> _PageIterator[ListLexiconsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListLexicons.html#Polly.Paginator.ListLexicons.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listlexiconspaginator)
        """

class ListSpeechSynthesisTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListSpeechSynthesisTasks.html#Polly.Paginator.ListSpeechSynthesisTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listspeechsynthesistaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef]
    ) -> _PageIterator[ListSpeechSynthesisTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListSpeechSynthesisTasks.html#Polly.Paginator.ListSpeechSynthesisTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listspeechsynthesistaskspaginator)
        """
