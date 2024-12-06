"""
Type annotations for omics service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_omics.client import OmicsClient
    from mypy_boto3_omics.paginator import (
        ListAnnotationImportJobsPaginator,
        ListAnnotationStoreVersionsPaginator,
        ListAnnotationStoresPaginator,
        ListMultipartReadSetUploadsPaginator,
        ListReadSetActivationJobsPaginator,
        ListReadSetExportJobsPaginator,
        ListReadSetImportJobsPaginator,
        ListReadSetUploadPartsPaginator,
        ListReadSetsPaginator,
        ListReferenceImportJobsPaginator,
        ListReferenceStoresPaginator,
        ListReferencesPaginator,
        ListRunCachesPaginator,
        ListRunGroupsPaginator,
        ListRunTasksPaginator,
        ListRunsPaginator,
        ListSequenceStoresPaginator,
        ListSharesPaginator,
        ListVariantImportJobsPaginator,
        ListVariantStoresPaginator,
        ListWorkflowsPaginator,
    )

    session = Session()
    client: OmicsClient = session.client("omics")

    list_annotation_import_jobs_paginator: ListAnnotationImportJobsPaginator = client.get_paginator("list_annotation_import_jobs")
    list_annotation_store_versions_paginator: ListAnnotationStoreVersionsPaginator = client.get_paginator("list_annotation_store_versions")
    list_annotation_stores_paginator: ListAnnotationStoresPaginator = client.get_paginator("list_annotation_stores")
    list_multipart_read_set_uploads_paginator: ListMultipartReadSetUploadsPaginator = client.get_paginator("list_multipart_read_set_uploads")
    list_read_set_activation_jobs_paginator: ListReadSetActivationJobsPaginator = client.get_paginator("list_read_set_activation_jobs")
    list_read_set_export_jobs_paginator: ListReadSetExportJobsPaginator = client.get_paginator("list_read_set_export_jobs")
    list_read_set_import_jobs_paginator: ListReadSetImportJobsPaginator = client.get_paginator("list_read_set_import_jobs")
    list_read_set_upload_parts_paginator: ListReadSetUploadPartsPaginator = client.get_paginator("list_read_set_upload_parts")
    list_read_sets_paginator: ListReadSetsPaginator = client.get_paginator("list_read_sets")
    list_reference_import_jobs_paginator: ListReferenceImportJobsPaginator = client.get_paginator("list_reference_import_jobs")
    list_reference_stores_paginator: ListReferenceStoresPaginator = client.get_paginator("list_reference_stores")
    list_references_paginator: ListReferencesPaginator = client.get_paginator("list_references")
    list_run_caches_paginator: ListRunCachesPaginator = client.get_paginator("list_run_caches")
    list_run_groups_paginator: ListRunGroupsPaginator = client.get_paginator("list_run_groups")
    list_run_tasks_paginator: ListRunTasksPaginator = client.get_paginator("list_run_tasks")
    list_runs_paginator: ListRunsPaginator = client.get_paginator("list_runs")
    list_sequence_stores_paginator: ListSequenceStoresPaginator = client.get_paginator("list_sequence_stores")
    list_shares_paginator: ListSharesPaginator = client.get_paginator("list_shares")
    list_variant_import_jobs_paginator: ListVariantImportJobsPaginator = client.get_paginator("list_variant_import_jobs")
    list_variant_stores_paginator: ListVariantStoresPaginator = client.get_paginator("list_variant_stores")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAnnotationImportJobsRequestListAnnotationImportJobsPaginateTypeDef,
    ListAnnotationImportJobsResponseTypeDef,
    ListAnnotationStoresRequestListAnnotationStoresPaginateTypeDef,
    ListAnnotationStoresResponseTypeDef,
    ListAnnotationStoreVersionsRequestListAnnotationStoreVersionsPaginateTypeDef,
    ListAnnotationStoreVersionsResponseTypeDef,
    ListMultipartReadSetUploadsRequestListMultipartReadSetUploadsPaginateTypeDef,
    ListMultipartReadSetUploadsResponseTypeDef,
    ListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef,
    ListReadSetActivationJobsResponseTypeDef,
    ListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef,
    ListReadSetExportJobsResponseTypeDef,
    ListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef,
    ListReadSetImportJobsResponseTypeDef,
    ListReadSetsRequestListReadSetsPaginateTypeDef,
    ListReadSetsResponseTypeDef,
    ListReadSetUploadPartsRequestListReadSetUploadPartsPaginateTypeDef,
    ListReadSetUploadPartsResponseTypeDef,
    ListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef,
    ListReferenceImportJobsResponseTypeDef,
    ListReferencesRequestListReferencesPaginateTypeDef,
    ListReferencesResponseTypeDef,
    ListReferenceStoresRequestListReferenceStoresPaginateTypeDef,
    ListReferenceStoresResponseTypeDef,
    ListRunCachesRequestListRunCachesPaginateTypeDef,
    ListRunCachesResponseTypeDef,
    ListRunGroupsRequestListRunGroupsPaginateTypeDef,
    ListRunGroupsResponseTypeDef,
    ListRunsRequestListRunsPaginateTypeDef,
    ListRunsResponseTypeDef,
    ListRunTasksRequestListRunTasksPaginateTypeDef,
    ListRunTasksResponseTypeDef,
    ListSequenceStoresRequestListSequenceStoresPaginateTypeDef,
    ListSequenceStoresResponseTypeDef,
    ListSharesRequestListSharesPaginateTypeDef,
    ListSharesResponseTypeDef,
    ListVariantImportJobsRequestListVariantImportJobsPaginateTypeDef,
    ListVariantImportJobsResponseTypeDef,
    ListVariantStoresRequestListVariantStoresPaginateTypeDef,
    ListVariantStoresResponseTypeDef,
    ListWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAnnotationImportJobsPaginator",
    "ListAnnotationStoreVersionsPaginator",
    "ListAnnotationStoresPaginator",
    "ListMultipartReadSetUploadsPaginator",
    "ListReadSetActivationJobsPaginator",
    "ListReadSetExportJobsPaginator",
    "ListReadSetImportJobsPaginator",
    "ListReadSetUploadPartsPaginator",
    "ListReadSetsPaginator",
    "ListReferenceImportJobsPaginator",
    "ListReferenceStoresPaginator",
    "ListReferencesPaginator",
    "ListRunCachesPaginator",
    "ListRunGroupsPaginator",
    "ListRunTasksPaginator",
    "ListRunsPaginator",
    "ListSequenceStoresPaginator",
    "ListSharesPaginator",
    "ListVariantImportJobsPaginator",
    "ListVariantStoresPaginator",
    "ListWorkflowsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAnnotationImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationImportJobs.html#Omics.Paginator.ListAnnotationImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listannotationimportjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAnnotationImportJobsRequestListAnnotationImportJobsPaginateTypeDef],
    ) -> _PageIterator[ListAnnotationImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationImportJobs.html#Omics.Paginator.ListAnnotationImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listannotationimportjobspaginator)
        """


class ListAnnotationStoreVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStoreVersions.html#Omics.Paginator.ListAnnotationStoreVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listannotationstoreversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAnnotationStoreVersionsRequestListAnnotationStoreVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListAnnotationStoreVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStoreVersions.html#Omics.Paginator.ListAnnotationStoreVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listannotationstoreversionspaginator)
        """


class ListAnnotationStoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStores.html#Omics.Paginator.ListAnnotationStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listannotationstorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAnnotationStoresRequestListAnnotationStoresPaginateTypeDef]
    ) -> _PageIterator[ListAnnotationStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListAnnotationStores.html#Omics.Paginator.ListAnnotationStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listannotationstorespaginator)
        """


class ListMultipartReadSetUploadsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListMultipartReadSetUploads.html#Omics.Paginator.ListMultipartReadSetUploads)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listmultipartreadsetuploadspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListMultipartReadSetUploadsRequestListMultipartReadSetUploadsPaginateTypeDef
        ],
    ) -> _PageIterator[ListMultipartReadSetUploadsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListMultipartReadSetUploads.html#Omics.Paginator.ListMultipartReadSetUploads.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listmultipartreadsetuploadspaginator)
        """


class ListReadSetActivationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetActivationJobs.html#Omics.Paginator.ListReadSetActivationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetactivationjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef],
    ) -> _PageIterator[ListReadSetActivationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetActivationJobs.html#Omics.Paginator.ListReadSetActivationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetactivationjobspaginator)
        """


class ListReadSetExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetExportJobs.html#Omics.Paginator.ListReadSetExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetexportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef]
    ) -> _PageIterator[ListReadSetExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetExportJobs.html#Omics.Paginator.ListReadSetExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetexportjobspaginator)
        """


class ListReadSetImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetImportJobs.html#Omics.Paginator.ListReadSetImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListReadSetImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetImportJobs.html#Omics.Paginator.ListReadSetImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetimportjobspaginator)
        """


class ListReadSetUploadPartsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetUploadParts.html#Omics.Paginator.ListReadSetUploadParts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetuploadpartspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetUploadPartsRequestListReadSetUploadPartsPaginateTypeDef]
    ) -> _PageIterator[ListReadSetUploadPartsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSetUploadParts.html#Omics.Paginator.ListReadSetUploadParts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetuploadpartspaginator)
        """


class ListReadSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSets.html#Omics.Paginator.ListReadSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadSetsRequestListReadSetsPaginateTypeDef]
    ) -> _PageIterator[ListReadSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReadSets.html#Omics.Paginator.ListReadSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreadsetspaginator)
        """


class ListReferenceImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceImportJobs.html#Omics.Paginator.ListReferenceImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreferenceimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListReferenceImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceImportJobs.html#Omics.Paginator.ListReferenceImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreferenceimportjobspaginator)
        """


class ListReferenceStoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceStores.html#Omics.Paginator.ListReferenceStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreferencestorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReferenceStoresRequestListReferenceStoresPaginateTypeDef]
    ) -> _PageIterator[ListReferenceStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferenceStores.html#Omics.Paginator.ListReferenceStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreferencestorespaginator)
        """


class ListReferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferences.html#Omics.Paginator.ListReferences)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreferencespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReferencesRequestListReferencesPaginateTypeDef]
    ) -> _PageIterator[ListReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListReferences.html#Omics.Paginator.ListReferences.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listreferencespaginator)
        """


class ListRunCachesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunCaches.html#Omics.Paginator.ListRunCaches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listruncachespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRunCachesRequestListRunCachesPaginateTypeDef]
    ) -> _PageIterator[ListRunCachesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunCaches.html#Omics.Paginator.ListRunCaches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listruncachespaginator)
        """


class ListRunGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunGroups.html#Omics.Paginator.ListRunGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listrungroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRunGroupsRequestListRunGroupsPaginateTypeDef]
    ) -> _PageIterator[ListRunGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunGroups.html#Omics.Paginator.ListRunGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listrungroupspaginator)
        """


class ListRunTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunTasks.html#Omics.Paginator.ListRunTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listruntaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRunTasksRequestListRunTasksPaginateTypeDef]
    ) -> _PageIterator[ListRunTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRunTasks.html#Omics.Paginator.ListRunTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listruntaskspaginator)
        """


class ListRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRuns.html#Omics.Paginator.ListRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRunsRequestListRunsPaginateTypeDef]
    ) -> _PageIterator[ListRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListRuns.html#Omics.Paginator.ListRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listrunspaginator)
        """


class ListSequenceStoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListSequenceStores.html#Omics.Paginator.ListSequenceStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listsequencestorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSequenceStoresRequestListSequenceStoresPaginateTypeDef]
    ) -> _PageIterator[ListSequenceStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListSequenceStores.html#Omics.Paginator.ListSequenceStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listsequencestorespaginator)
        """


class ListSharesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListShares.html#Omics.Paginator.ListShares)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listsharespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSharesRequestListSharesPaginateTypeDef]
    ) -> _PageIterator[ListSharesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListShares.html#Omics.Paginator.ListShares.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listsharespaginator)
        """


class ListVariantImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantImportJobs.html#Omics.Paginator.ListVariantImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listvariantimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVariantImportJobsRequestListVariantImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListVariantImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantImportJobs.html#Omics.Paginator.ListVariantImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listvariantimportjobspaginator)
        """


class ListVariantStoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantStores.html#Omics.Paginator.ListVariantStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listvariantstorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVariantStoresRequestListVariantStoresPaginateTypeDef]
    ) -> _PageIterator[ListVariantStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListVariantStores.html#Omics.Paginator.ListVariantStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listvariantstorespaginator)
        """


class ListWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListWorkflows.html#Omics.Paginator.ListWorkflows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listworkflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> _PageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/paginator/ListWorkflows.html#Omics.Paginator.ListWorkflows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/paginators/#listworkflowspaginator)
        """
