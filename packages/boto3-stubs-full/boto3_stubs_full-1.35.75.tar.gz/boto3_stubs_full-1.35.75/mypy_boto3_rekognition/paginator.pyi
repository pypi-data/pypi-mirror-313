"""
Type annotations for rekognition service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rekognition.client import RekognitionClient
    from mypy_boto3_rekognition.paginator import (
        DescribeProjectVersionsPaginator,
        DescribeProjectsPaginator,
        ListCollectionsPaginator,
        ListDatasetEntriesPaginator,
        ListDatasetLabelsPaginator,
        ListFacesPaginator,
        ListProjectPoliciesPaginator,
        ListStreamProcessorsPaginator,
        ListUsersPaginator,
    )

    session = Session()
    client: RekognitionClient = session.client("rekognition")

    describe_project_versions_paginator: DescribeProjectVersionsPaginator = client.get_paginator("describe_project_versions")
    describe_projects_paginator: DescribeProjectsPaginator = client.get_paginator("describe_projects")
    list_collections_paginator: ListCollectionsPaginator = client.get_paginator("list_collections")
    list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
    list_dataset_labels_paginator: ListDatasetLabelsPaginator = client.get_paginator("list_dataset_labels")
    list_faces_paginator: ListFacesPaginator = client.get_paginator("list_faces")
    list_project_policies_paginator: ListProjectPoliciesPaginator = client.get_paginator("list_project_policies")
    list_stream_processors_paginator: ListStreamProcessorsPaginator = client.get_paginator("list_stream_processors")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeProjectsRequestDescribeProjectsPaginateTypeDef,
    DescribeProjectsResponseTypeDef,
    DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef,
    DescribeProjectVersionsResponseTypeDef,
    ListCollectionsRequestListCollectionsPaginateTypeDef,
    ListCollectionsResponseTypeDef,
    ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef,
    ListDatasetLabelsResponseTypeDef,
    ListFacesRequestListFacesPaginateTypeDef,
    ListFacesResponseTypeDef,
    ListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef,
    ListProjectPoliciesResponseTypeDef,
    ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef,
    ListStreamProcessorsResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeProjectVersionsPaginator",
    "DescribeProjectsPaginator",
    "ListCollectionsPaginator",
    "ListDatasetEntriesPaginator",
    "ListDatasetLabelsPaginator",
    "ListFacesPaginator",
    "ListProjectPoliciesPaginator",
    "ListStreamProcessorsPaginator",
    "ListUsersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeProjectVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjectVersions.html#Rekognition.Paginator.DescribeProjectVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#describeprojectversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef]
    ) -> _PageIterator[DescribeProjectVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjectVersions.html#Rekognition.Paginator.DescribeProjectVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#describeprojectversionspaginator)
        """

class DescribeProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjects.html#Rekognition.Paginator.DescribeProjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#describeprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeProjectsRequestDescribeProjectsPaginateTypeDef]
    ) -> _PageIterator[DescribeProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjects.html#Rekognition.Paginator.DescribeProjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#describeprojectspaginator)
        """

class ListCollectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListCollections.html#Rekognition.Paginator.ListCollections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listcollectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCollectionsRequestListCollectionsPaginateTypeDef]
    ) -> _PageIterator[ListCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListCollections.html#Rekognition.Paginator.ListCollections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listcollectionspaginator)
        """

class ListDatasetEntriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetEntries.html#Rekognition.Paginator.ListDatasetEntries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listdatasetentriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef]
    ) -> _PageIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetEntries.html#Rekognition.Paginator.ListDatasetEntries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listdatasetentriespaginator)
        """

class ListDatasetLabelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetLabels.html#Rekognition.Paginator.ListDatasetLabels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listdatasetlabelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef]
    ) -> _PageIterator[ListDatasetLabelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetLabels.html#Rekognition.Paginator.ListDatasetLabels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listdatasetlabelspaginator)
        """

class ListFacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListFaces.html#Rekognition.Paginator.ListFaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listfacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFacesRequestListFacesPaginateTypeDef]
    ) -> _PageIterator[ListFacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListFaces.html#Rekognition.Paginator.ListFaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listfacespaginator)
        """

class ListProjectPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListProjectPolicies.html#Rekognition.Paginator.ListProjectPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listprojectpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListProjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListProjectPolicies.html#Rekognition.Paginator.ListProjectPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listprojectpoliciespaginator)
        """

class ListStreamProcessorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListStreamProcessors.html#Rekognition.Paginator.ListStreamProcessors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#liststreamprocessorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef]
    ) -> _PageIterator[ListStreamProcessorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListStreamProcessors.html#Rekognition.Paginator.ListStreamProcessors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#liststreamprocessorspaginator)
        """

class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListUsers.html#Rekognition.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListUsers.html#Rekognition.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/paginators/#listuserspaginator)
        """
