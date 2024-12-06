"""
Type annotations for chime-sdk-voice service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_chime_sdk_voice.client import ChimeSDKVoiceClient
    from mypy_boto3_chime_sdk_voice.paginator import (
        ListSipMediaApplicationsPaginator,
        ListSipRulesPaginator,
    )

    session = Session()
    client: ChimeSDKVoiceClient = session.client("chime-sdk-voice")

    list_sip_media_applications_paginator: ListSipMediaApplicationsPaginator = client.get_paginator("list_sip_media_applications")
    list_sip_rules_paginator: ListSipRulesPaginator = client.get_paginator("list_sip_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListSipMediaApplicationsRequestListSipMediaApplicationsPaginateTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesRequestListSipRulesPaginateTypeDef,
    ListSipRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListSipMediaApplicationsPaginator", "ListSipRulesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSipMediaApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipMediaApplications.html#ChimeSDKVoice.Paginator.ListSipMediaApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSipMediaApplicationsRequestListSipMediaApplicationsPaginateTypeDef],
    ) -> _PageIterator[ListSipMediaApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipMediaApplications.html#ChimeSDKVoice.Paginator.ListSipMediaApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
        """

class ListSipRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipRules.html#ChimeSDKVoice.Paginator.ListSipRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsiprulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSipRulesRequestListSipRulesPaginateTypeDef]
    ) -> _PageIterator[ListSipRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipRules.html#ChimeSDKVoice.Paginator.ListSipRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsiprulespaginator)
        """
