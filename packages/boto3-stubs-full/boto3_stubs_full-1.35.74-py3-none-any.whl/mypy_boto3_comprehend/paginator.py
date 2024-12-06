"""
Type annotations for comprehend service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_comprehend.client import ComprehendClient
    from mypy_boto3_comprehend.paginator import (
        ListDocumentClassificationJobsPaginator,
        ListDocumentClassifiersPaginator,
        ListDominantLanguageDetectionJobsPaginator,
        ListEndpointsPaginator,
        ListEntitiesDetectionJobsPaginator,
        ListEntityRecognizersPaginator,
        ListKeyPhrasesDetectionJobsPaginator,
        ListPiiEntitiesDetectionJobsPaginator,
        ListSentimentDetectionJobsPaginator,
        ListTopicsDetectionJobsPaginator,
    )

    session = Session()
    client: ComprehendClient = session.client("comprehend")

    list_document_classification_jobs_paginator: ListDocumentClassificationJobsPaginator = client.get_paginator("list_document_classification_jobs")
    list_document_classifiers_paginator: ListDocumentClassifiersPaginator = client.get_paginator("list_document_classifiers")
    list_dominant_language_detection_jobs_paginator: ListDominantLanguageDetectionJobsPaginator = client.get_paginator("list_dominant_language_detection_jobs")
    list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    list_entities_detection_jobs_paginator: ListEntitiesDetectionJobsPaginator = client.get_paginator("list_entities_detection_jobs")
    list_entity_recognizers_paginator: ListEntityRecognizersPaginator = client.get_paginator("list_entity_recognizers")
    list_key_phrases_detection_jobs_paginator: ListKeyPhrasesDetectionJobsPaginator = client.get_paginator("list_key_phrases_detection_jobs")
    list_pii_entities_detection_jobs_paginator: ListPiiEntitiesDetectionJobsPaginator = client.get_paginator("list_pii_entities_detection_jobs")
    list_sentiment_detection_jobs_paginator: ListSentimentDetectionJobsPaginator = client.get_paginator("list_sentiment_detection_jobs")
    list_topics_detection_jobs_paginator: ListTopicsDetectionJobsPaginator = client.get_paginator("list_topics_detection_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDocumentClassificationJobsRequestListDocumentClassificationJobsPaginateTypeDef,
    ListDocumentClassificationJobsResponseTypeDef,
    ListDocumentClassifiersRequestListDocumentClassifiersPaginateTypeDef,
    ListDocumentClassifiersResponseTypeDef,
    ListDominantLanguageDetectionJobsRequestListDominantLanguageDetectionJobsPaginateTypeDef,
    ListDominantLanguageDetectionJobsResponseTypeDef,
    ListEndpointsRequestListEndpointsPaginateTypeDef,
    ListEndpointsResponseTypeDef,
    ListEntitiesDetectionJobsRequestListEntitiesDetectionJobsPaginateTypeDef,
    ListEntitiesDetectionJobsResponseTypeDef,
    ListEntityRecognizersRequestListEntityRecognizersPaginateTypeDef,
    ListEntityRecognizersResponseTypeDef,
    ListKeyPhrasesDetectionJobsRequestListKeyPhrasesDetectionJobsPaginateTypeDef,
    ListKeyPhrasesDetectionJobsResponseTypeDef,
    ListPiiEntitiesDetectionJobsRequestListPiiEntitiesDetectionJobsPaginateTypeDef,
    ListPiiEntitiesDetectionJobsResponseTypeDef,
    ListSentimentDetectionJobsRequestListSentimentDetectionJobsPaginateTypeDef,
    ListSentimentDetectionJobsResponseTypeDef,
    ListTopicsDetectionJobsRequestListTopicsDetectionJobsPaginateTypeDef,
    ListTopicsDetectionJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDocumentClassificationJobsPaginator",
    "ListDocumentClassifiersPaginator",
    "ListDominantLanguageDetectionJobsPaginator",
    "ListEndpointsPaginator",
    "ListEntitiesDetectionJobsPaginator",
    "ListEntityRecognizersPaginator",
    "ListKeyPhrasesDetectionJobsPaginator",
    "ListPiiEntitiesDetectionJobsPaginator",
    "ListSentimentDetectionJobsPaginator",
    "ListTopicsDetectionJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDocumentClassificationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassificationJobs.html#Comprehend.Paginator.ListDocumentClassificationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listdocumentclassificationjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDocumentClassificationJobsRequestListDocumentClassificationJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDocumentClassificationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassificationJobs.html#Comprehend.Paginator.ListDocumentClassificationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listdocumentclassificationjobspaginator)
        """


class ListDocumentClassifiersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassifiers.html#Comprehend.Paginator.ListDocumentClassifiers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listdocumentclassifierspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDocumentClassifiersRequestListDocumentClassifiersPaginateTypeDef]
    ) -> _PageIterator[ListDocumentClassifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassifiers.html#Comprehend.Paginator.ListDocumentClassifiers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listdocumentclassifierspaginator)
        """


class ListDominantLanguageDetectionJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDominantLanguageDetectionJobs.html#Comprehend.Paginator.ListDominantLanguageDetectionJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listdominantlanguagedetectionjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDominantLanguageDetectionJobsRequestListDominantLanguageDetectionJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDominantLanguageDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDominantLanguageDetectionJobs.html#Comprehend.Paginator.ListDominantLanguageDetectionJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listdominantlanguagedetectionjobspaginator)
        """


class ListEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEndpoints.html#Comprehend.Paginator.ListEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEndpointsRequestListEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEndpoints.html#Comprehend.Paginator.ListEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listendpointspaginator)
        """


class ListEntitiesDetectionJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntitiesDetectionJobs.html#Comprehend.Paginator.ListEntitiesDetectionJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listentitiesdetectionjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListEntitiesDetectionJobsRequestListEntitiesDetectionJobsPaginateTypeDef],
    ) -> _PageIterator[ListEntitiesDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntitiesDetectionJobs.html#Comprehend.Paginator.ListEntitiesDetectionJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listentitiesdetectionjobspaginator)
        """


class ListEntityRecognizersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntityRecognizers.html#Comprehend.Paginator.ListEntityRecognizers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listentityrecognizerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEntityRecognizersRequestListEntityRecognizersPaginateTypeDef]
    ) -> _PageIterator[ListEntityRecognizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntityRecognizers.html#Comprehend.Paginator.ListEntityRecognizers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listentityrecognizerspaginator)
        """


class ListKeyPhrasesDetectionJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListKeyPhrasesDetectionJobs.html#Comprehend.Paginator.ListKeyPhrasesDetectionJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listkeyphrasesdetectionjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListKeyPhrasesDetectionJobsRequestListKeyPhrasesDetectionJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListKeyPhrasesDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListKeyPhrasesDetectionJobs.html#Comprehend.Paginator.ListKeyPhrasesDetectionJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listkeyphrasesdetectionjobspaginator)
        """


class ListPiiEntitiesDetectionJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListPiiEntitiesDetectionJobs.html#Comprehend.Paginator.ListPiiEntitiesDetectionJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listpiientitiesdetectionjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPiiEntitiesDetectionJobsRequestListPiiEntitiesDetectionJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListPiiEntitiesDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListPiiEntitiesDetectionJobs.html#Comprehend.Paginator.ListPiiEntitiesDetectionJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listpiientitiesdetectionjobspaginator)
        """


class ListSentimentDetectionJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListSentimentDetectionJobs.html#Comprehend.Paginator.ListSentimentDetectionJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listsentimentdetectionjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSentimentDetectionJobsRequestListSentimentDetectionJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSentimentDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListSentimentDetectionJobs.html#Comprehend.Paginator.ListSentimentDetectionJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listsentimentdetectionjobspaginator)
        """


class ListTopicsDetectionJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListTopicsDetectionJobs.html#Comprehend.Paginator.ListTopicsDetectionJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listtopicsdetectionjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTopicsDetectionJobsRequestListTopicsDetectionJobsPaginateTypeDef]
    ) -> _PageIterator[ListTopicsDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListTopicsDetectionJobs.html#Comprehend.Paginator.ListTopicsDetectionJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/paginators/#listtopicsdetectionjobspaginator)
        """
