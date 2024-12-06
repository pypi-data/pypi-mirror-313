"""
Type annotations for omics service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_omics.client import OmicsClient
    from mypy_boto3_omics.waiter import (
        AnnotationImportJobCreatedWaiter,
        AnnotationStoreCreatedWaiter,
        AnnotationStoreDeletedWaiter,
        AnnotationStoreVersionCreatedWaiter,
        AnnotationStoreVersionDeletedWaiter,
        ReadSetActivationJobCompletedWaiter,
        ReadSetExportJobCompletedWaiter,
        ReadSetImportJobCompletedWaiter,
        ReferenceImportJobCompletedWaiter,
        RunCompletedWaiter,
        RunRunningWaiter,
        TaskCompletedWaiter,
        TaskRunningWaiter,
        VariantImportJobCreatedWaiter,
        VariantStoreCreatedWaiter,
        VariantStoreDeletedWaiter,
        WorkflowActiveWaiter,
    )

    session = Session()
    client: OmicsClient = session.client("omics")

    annotation_import_job_created_waiter: AnnotationImportJobCreatedWaiter = client.get_waiter("annotation_import_job_created")
    annotation_store_created_waiter: AnnotationStoreCreatedWaiter = client.get_waiter("annotation_store_created")
    annotation_store_deleted_waiter: AnnotationStoreDeletedWaiter = client.get_waiter("annotation_store_deleted")
    annotation_store_version_created_waiter: AnnotationStoreVersionCreatedWaiter = client.get_waiter("annotation_store_version_created")
    annotation_store_version_deleted_waiter: AnnotationStoreVersionDeletedWaiter = client.get_waiter("annotation_store_version_deleted")
    read_set_activation_job_completed_waiter: ReadSetActivationJobCompletedWaiter = client.get_waiter("read_set_activation_job_completed")
    read_set_export_job_completed_waiter: ReadSetExportJobCompletedWaiter = client.get_waiter("read_set_export_job_completed")
    read_set_import_job_completed_waiter: ReadSetImportJobCompletedWaiter = client.get_waiter("read_set_import_job_completed")
    reference_import_job_completed_waiter: ReferenceImportJobCompletedWaiter = client.get_waiter("reference_import_job_completed")
    run_completed_waiter: RunCompletedWaiter = client.get_waiter("run_completed")
    run_running_waiter: RunRunningWaiter = client.get_waiter("run_running")
    task_completed_waiter: TaskCompletedWaiter = client.get_waiter("task_completed")
    task_running_waiter: TaskRunningWaiter = client.get_waiter("task_running")
    variant_import_job_created_waiter: VariantImportJobCreatedWaiter = client.get_waiter("variant_import_job_created")
    variant_store_created_waiter: VariantStoreCreatedWaiter = client.get_waiter("variant_store_created")
    variant_store_deleted_waiter: VariantStoreDeletedWaiter = client.get_waiter("variant_store_deleted")
    workflow_active_waiter: WorkflowActiveWaiter = client.get_waiter("workflow_active")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef,
    GetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef,
    GetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef,
    GetAnnotationStoreVersionRequestAnnotationStoreVersionCreatedWaitTypeDef,
    GetAnnotationStoreVersionRequestAnnotationStoreVersionDeletedWaitTypeDef,
    GetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef,
    GetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef,
    GetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef,
    GetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef,
    GetRunRequestRunCompletedWaitTypeDef,
    GetRunRequestRunRunningWaitTypeDef,
    GetRunTaskRequestTaskCompletedWaitTypeDef,
    GetRunTaskRequestTaskRunningWaitTypeDef,
    GetVariantImportRequestVariantImportJobCreatedWaitTypeDef,
    GetVariantStoreRequestVariantStoreCreatedWaitTypeDef,
    GetVariantStoreRequestVariantStoreDeletedWaitTypeDef,
    GetWorkflowRequestWorkflowActiveWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "AnnotationImportJobCreatedWaiter",
    "AnnotationStoreCreatedWaiter",
    "AnnotationStoreDeletedWaiter",
    "AnnotationStoreVersionCreatedWaiter",
    "AnnotationStoreVersionDeletedWaiter",
    "ReadSetActivationJobCompletedWaiter",
    "ReadSetExportJobCompletedWaiter",
    "ReadSetImportJobCompletedWaiter",
    "ReferenceImportJobCompletedWaiter",
    "RunCompletedWaiter",
    "RunRunningWaiter",
    "TaskCompletedWaiter",
    "TaskRunningWaiter",
    "VariantImportJobCreatedWaiter",
    "VariantStoreCreatedWaiter",
    "VariantStoreDeletedWaiter",
    "WorkflowActiveWaiter",
)


class AnnotationImportJobCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationImportJobCreated.html#Omics.Waiter.AnnotationImportJobCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationimportjobcreatedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationImportJobCreated.html#Omics.Waiter.AnnotationImportJobCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationimportjobcreatedwaiter)
        """


class AnnotationStoreCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreCreated.html#Omics.Waiter.AnnotationStoreCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstorecreatedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreCreated.html#Omics.Waiter.AnnotationStoreCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstorecreatedwaiter)
        """


class AnnotationStoreDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreDeleted.html#Omics.Waiter.AnnotationStoreDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstoredeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreDeleted.html#Omics.Waiter.AnnotationStoreDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstoredeletedwaiter)
        """


class AnnotationStoreVersionCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreVersionCreated.html#Omics.Waiter.AnnotationStoreVersionCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstoreversioncreatedwaiter)
    """

    def wait(
        self,
        **kwargs: Unpack[GetAnnotationStoreVersionRequestAnnotationStoreVersionCreatedWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreVersionCreated.html#Omics.Waiter.AnnotationStoreVersionCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstoreversioncreatedwaiter)
        """


class AnnotationStoreVersionDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreVersionDeleted.html#Omics.Waiter.AnnotationStoreVersionDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstoreversiondeletedwaiter)
    """

    def wait(
        self,
        **kwargs: Unpack[GetAnnotationStoreVersionRequestAnnotationStoreVersionDeletedWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/AnnotationStoreVersionDeleted.html#Omics.Waiter.AnnotationStoreVersionDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#annotationstoreversiondeletedwaiter)
        """


class ReadSetActivationJobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReadSetActivationJobCompleted.html#Omics.Waiter.ReadSetActivationJobCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#readsetactivationjobcompletedwaiter)
    """

    def wait(
        self,
        **kwargs: Unpack[GetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReadSetActivationJobCompleted.html#Omics.Waiter.ReadSetActivationJobCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#readsetactivationjobcompletedwaiter)
        """


class ReadSetExportJobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReadSetExportJobCompleted.html#Omics.Waiter.ReadSetExportJobCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#readsetexportjobcompletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReadSetExportJobCompleted.html#Omics.Waiter.ReadSetExportJobCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#readsetexportjobcompletedwaiter)
        """


class ReadSetImportJobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReadSetImportJobCompleted.html#Omics.Waiter.ReadSetImportJobCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#readsetimportjobcompletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReadSetImportJobCompleted.html#Omics.Waiter.ReadSetImportJobCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#readsetimportjobcompletedwaiter)
        """


class ReferenceImportJobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReferenceImportJobCompleted.html#Omics.Waiter.ReferenceImportJobCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#referenceimportjobcompletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/ReferenceImportJobCompleted.html#Omics.Waiter.ReferenceImportJobCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#referenceimportjobcompletedwaiter)
        """


class RunCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/RunCompleted.html#Omics.Waiter.RunCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#runcompletedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetRunRequestRunCompletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/RunCompleted.html#Omics.Waiter.RunCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#runcompletedwaiter)
        """


class RunRunningWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/RunRunning.html#Omics.Waiter.RunRunning)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#runrunningwaiter)
    """

    def wait(self, **kwargs: Unpack[GetRunRequestRunRunningWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/RunRunning.html#Omics.Waiter.RunRunning.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#runrunningwaiter)
        """


class TaskCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/TaskCompleted.html#Omics.Waiter.TaskCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#taskcompletedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetRunTaskRequestTaskCompletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/TaskCompleted.html#Omics.Waiter.TaskCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#taskcompletedwaiter)
        """


class TaskRunningWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/TaskRunning.html#Omics.Waiter.TaskRunning)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#taskrunningwaiter)
    """

    def wait(self, **kwargs: Unpack[GetRunTaskRequestTaskRunningWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/TaskRunning.html#Omics.Waiter.TaskRunning.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#taskrunningwaiter)
        """


class VariantImportJobCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/VariantImportJobCreated.html#Omics.Waiter.VariantImportJobCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#variantimportjobcreatedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetVariantImportRequestVariantImportJobCreatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/VariantImportJobCreated.html#Omics.Waiter.VariantImportJobCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#variantimportjobcreatedwaiter)
        """


class VariantStoreCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/VariantStoreCreated.html#Omics.Waiter.VariantStoreCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#variantstorecreatedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetVariantStoreRequestVariantStoreCreatedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/VariantStoreCreated.html#Omics.Waiter.VariantStoreCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#variantstorecreatedwaiter)
        """


class VariantStoreDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/VariantStoreDeleted.html#Omics.Waiter.VariantStoreDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#variantstoredeletedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetVariantStoreRequestVariantStoreDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/VariantStoreDeleted.html#Omics.Waiter.VariantStoreDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#variantstoredeletedwaiter)
        """


class WorkflowActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/WorkflowActive.html#Omics.Waiter.WorkflowActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#workflowactivewaiter)
    """

    def wait(self, **kwargs: Unpack[GetWorkflowRequestWorkflowActiveWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/waiter/WorkflowActive.html#Omics.Waiter.WorkflowActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/waiters/#workflowactivewaiter)
        """
