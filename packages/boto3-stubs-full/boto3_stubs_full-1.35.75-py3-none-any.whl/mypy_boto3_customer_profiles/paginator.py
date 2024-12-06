"""
Type annotations for customer-profiles service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_customer_profiles.client import CustomerProfilesClient
    from mypy_boto3_customer_profiles.paginator import (
        GetSimilarProfilesPaginator,
        ListEventStreamsPaginator,
        ListEventTriggersPaginator,
        ListObjectTypeAttributesPaginator,
        ListRuleBasedMatchesPaginator,
        ListSegmentDefinitionsPaginator,
    )

    session = Session()
    client: CustomerProfilesClient = session.client("customer-profiles")

    get_similar_profiles_paginator: GetSimilarProfilesPaginator = client.get_paginator("get_similar_profiles")
    list_event_streams_paginator: ListEventStreamsPaginator = client.get_paginator("list_event_streams")
    list_event_triggers_paginator: ListEventTriggersPaginator = client.get_paginator("list_event_triggers")
    list_object_type_attributes_paginator: ListObjectTypeAttributesPaginator = client.get_paginator("list_object_type_attributes")
    list_rule_based_matches_paginator: ListRuleBasedMatchesPaginator = client.get_paginator("list_rule_based_matches")
    list_segment_definitions_paginator: ListSegmentDefinitionsPaginator = client.get_paginator("list_segment_definitions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetSimilarProfilesRequestGetSimilarProfilesPaginateTypeDef,
    GetSimilarProfilesResponseTypeDef,
    ListEventStreamsRequestListEventStreamsPaginateTypeDef,
    ListEventStreamsResponseTypeDef,
    ListEventTriggersRequestListEventTriggersPaginateTypeDef,
    ListEventTriggersResponseTypeDef,
    ListObjectTypeAttributesRequestListObjectTypeAttributesPaginateTypeDef,
    ListObjectTypeAttributesResponseTypeDef,
    ListRuleBasedMatchesRequestListRuleBasedMatchesPaginateTypeDef,
    ListRuleBasedMatchesResponseTypeDef,
    ListSegmentDefinitionsRequestListSegmentDefinitionsPaginateTypeDef,
    ListSegmentDefinitionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetSimilarProfilesPaginator",
    "ListEventStreamsPaginator",
    "ListEventTriggersPaginator",
    "ListObjectTypeAttributesPaginator",
    "ListRuleBasedMatchesPaginator",
    "ListSegmentDefinitionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetSimilarProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/GetSimilarProfiles.html#CustomerProfiles.Paginator.GetSimilarProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#getsimilarprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetSimilarProfilesRequestGetSimilarProfilesPaginateTypeDef]
    ) -> _PageIterator[GetSimilarProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/GetSimilarProfiles.html#CustomerProfiles.Paginator.GetSimilarProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#getsimilarprofilespaginator)
        """


class ListEventStreamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventStreams.html#CustomerProfiles.Paginator.ListEventStreams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listeventstreamspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventStreamsRequestListEventStreamsPaginateTypeDef]
    ) -> _PageIterator[ListEventStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventStreams.html#CustomerProfiles.Paginator.ListEventStreams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listeventstreamspaginator)
        """


class ListEventTriggersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventTriggers.html#CustomerProfiles.Paginator.ListEventTriggers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listeventtriggerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventTriggersRequestListEventTriggersPaginateTypeDef]
    ) -> _PageIterator[ListEventTriggersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventTriggers.html#CustomerProfiles.Paginator.ListEventTriggers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listeventtriggerspaginator)
        """


class ListObjectTypeAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListObjectTypeAttributes.html#CustomerProfiles.Paginator.ListObjectTypeAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listobjecttypeattributespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListObjectTypeAttributesRequestListObjectTypeAttributesPaginateTypeDef],
    ) -> _PageIterator[ListObjectTypeAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListObjectTypeAttributes.html#CustomerProfiles.Paginator.ListObjectTypeAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listobjecttypeattributespaginator)
        """


class ListRuleBasedMatchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListRuleBasedMatches.html#CustomerProfiles.Paginator.ListRuleBasedMatches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listrulebasedmatchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRuleBasedMatchesRequestListRuleBasedMatchesPaginateTypeDef]
    ) -> _PageIterator[ListRuleBasedMatchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListRuleBasedMatches.html#CustomerProfiles.Paginator.ListRuleBasedMatches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listrulebasedmatchespaginator)
        """


class ListSegmentDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListSegmentDefinitions.html#CustomerProfiles.Paginator.ListSegmentDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listsegmentdefinitionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSegmentDefinitionsRequestListSegmentDefinitionsPaginateTypeDef]
    ) -> _PageIterator[ListSegmentDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListSegmentDefinitions.html#CustomerProfiles.Paginator.ListSegmentDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listsegmentdefinitionspaginator)
        """
