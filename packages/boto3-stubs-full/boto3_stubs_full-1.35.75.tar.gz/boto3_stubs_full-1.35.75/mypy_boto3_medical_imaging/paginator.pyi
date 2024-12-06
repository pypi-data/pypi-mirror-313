"""
Type annotations for medical-imaging service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_medical_imaging.client import HealthImagingClient
    from mypy_boto3_medical_imaging.paginator import (
        ListDICOMImportJobsPaginator,
        ListDatastoresPaginator,
        ListImageSetVersionsPaginator,
        SearchImageSetsPaginator,
    )

    session = Session()
    client: HealthImagingClient = session.client("medical-imaging")

    list_dicom_import_jobs_paginator: ListDICOMImportJobsPaginator = client.get_paginator("list_dicom_import_jobs")
    list_datastores_paginator: ListDatastoresPaginator = client.get_paginator("list_datastores")
    list_image_set_versions_paginator: ListImageSetVersionsPaginator = client.get_paginator("list_image_set_versions")
    search_image_sets_paginator: SearchImageSetsPaginator = client.get_paginator("search_image_sets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDatastoresRequestListDatastoresPaginateTypeDef,
    ListDatastoresResponseTypeDef,
    ListDICOMImportJobsRequestListDICOMImportJobsPaginateTypeDef,
    ListDICOMImportJobsResponseTypeDef,
    ListImageSetVersionsRequestListImageSetVersionsPaginateTypeDef,
    ListImageSetVersionsResponseTypeDef,
    SearchImageSetsRequestSearchImageSetsPaginateTypeDef,
    SearchImageSetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDICOMImportJobsPaginator",
    "ListDatastoresPaginator",
    "ListImageSetVersionsPaginator",
    "SearchImageSetsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDICOMImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/ListDICOMImportJobs.html#HealthImaging.Paginator.ListDICOMImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#listdicomimportjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDICOMImportJobsRequestListDICOMImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListDICOMImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/ListDICOMImportJobs.html#HealthImaging.Paginator.ListDICOMImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#listdicomimportjobspaginator)
        """

class ListDatastoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/ListDatastores.html#HealthImaging.Paginator.ListDatastores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#listdatastorespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatastoresRequestListDatastoresPaginateTypeDef]
    ) -> _PageIterator[ListDatastoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/ListDatastores.html#HealthImaging.Paginator.ListDatastores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#listdatastorespaginator)
        """

class ListImageSetVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/ListImageSetVersions.html#HealthImaging.Paginator.ListImageSetVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#listimagesetversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImageSetVersionsRequestListImageSetVersionsPaginateTypeDef]
    ) -> _PageIterator[ListImageSetVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/ListImageSetVersions.html#HealthImaging.Paginator.ListImageSetVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#listimagesetversionspaginator)
        """

class SearchImageSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/SearchImageSets.html#HealthImaging.Paginator.SearchImageSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#searchimagesetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchImageSetsRequestSearchImageSetsPaginateTypeDef]
    ) -> _PageIterator[SearchImageSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medical-imaging/paginator/SearchImageSets.html#HealthImaging.Paginator.SearchImageSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/paginators/#searchimagesetspaginator)
        """
