"""
Type annotations for backup service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_backup.client import BackupClient
    from mypy_boto3_backup.paginator import (
        ListBackupJobsPaginator,
        ListBackupPlanTemplatesPaginator,
        ListBackupPlanVersionsPaginator,
        ListBackupPlansPaginator,
        ListBackupSelectionsPaginator,
        ListBackupVaultsPaginator,
        ListCopyJobsPaginator,
        ListLegalHoldsPaginator,
        ListProtectedResourcesByBackupVaultPaginator,
        ListProtectedResourcesPaginator,
        ListRecoveryPointsByBackupVaultPaginator,
        ListRecoveryPointsByLegalHoldPaginator,
        ListRecoveryPointsByResourcePaginator,
        ListRestoreJobsByProtectedResourcePaginator,
        ListRestoreJobsPaginator,
        ListRestoreTestingPlansPaginator,
        ListRestoreTestingSelectionsPaginator,
    )

    session = Session()
    client: BackupClient = session.client("backup")

    list_backup_jobs_paginator: ListBackupJobsPaginator = client.get_paginator("list_backup_jobs")
    list_backup_plan_templates_paginator: ListBackupPlanTemplatesPaginator = client.get_paginator("list_backup_plan_templates")
    list_backup_plan_versions_paginator: ListBackupPlanVersionsPaginator = client.get_paginator("list_backup_plan_versions")
    list_backup_plans_paginator: ListBackupPlansPaginator = client.get_paginator("list_backup_plans")
    list_backup_selections_paginator: ListBackupSelectionsPaginator = client.get_paginator("list_backup_selections")
    list_backup_vaults_paginator: ListBackupVaultsPaginator = client.get_paginator("list_backup_vaults")
    list_copy_jobs_paginator: ListCopyJobsPaginator = client.get_paginator("list_copy_jobs")
    list_legal_holds_paginator: ListLegalHoldsPaginator = client.get_paginator("list_legal_holds")
    list_protected_resources_by_backup_vault_paginator: ListProtectedResourcesByBackupVaultPaginator = client.get_paginator("list_protected_resources_by_backup_vault")
    list_protected_resources_paginator: ListProtectedResourcesPaginator = client.get_paginator("list_protected_resources")
    list_recovery_points_by_backup_vault_paginator: ListRecoveryPointsByBackupVaultPaginator = client.get_paginator("list_recovery_points_by_backup_vault")
    list_recovery_points_by_legal_hold_paginator: ListRecoveryPointsByLegalHoldPaginator = client.get_paginator("list_recovery_points_by_legal_hold")
    list_recovery_points_by_resource_paginator: ListRecoveryPointsByResourcePaginator = client.get_paginator("list_recovery_points_by_resource")
    list_restore_jobs_by_protected_resource_paginator: ListRestoreJobsByProtectedResourcePaginator = client.get_paginator("list_restore_jobs_by_protected_resource")
    list_restore_jobs_paginator: ListRestoreJobsPaginator = client.get_paginator("list_restore_jobs")
    list_restore_testing_plans_paginator: ListRestoreTestingPlansPaginator = client.get_paginator("list_restore_testing_plans")
    list_restore_testing_selections_paginator: ListRestoreTestingSelectionsPaginator = client.get_paginator("list_restore_testing_selections")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBackupJobsInputListBackupJobsPaginateTypeDef,
    ListBackupJobsOutputTypeDef,
    ListBackupPlansInputListBackupPlansPaginateTypeDef,
    ListBackupPlansOutputTypeDef,
    ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef,
    ListBackupPlanTemplatesOutputTypeDef,
    ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef,
    ListBackupPlanVersionsOutputTypeDef,
    ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef,
    ListBackupSelectionsOutputTypeDef,
    ListBackupVaultsInputListBackupVaultsPaginateTypeDef,
    ListBackupVaultsOutputTypeDef,
    ListCopyJobsInputListCopyJobsPaginateTypeDef,
    ListCopyJobsOutputTypeDef,
    ListLegalHoldsInputListLegalHoldsPaginateTypeDef,
    ListLegalHoldsOutputTypeDef,
    ListProtectedResourcesByBackupVaultInputListProtectedResourcesByBackupVaultPaginateTypeDef,
    ListProtectedResourcesByBackupVaultOutputTypeDef,
    ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef,
    ListProtectedResourcesOutputTypeDef,
    ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef,
    ListRecoveryPointsByBackupVaultOutputTypeDef,
    ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef,
    ListRecoveryPointsByLegalHoldOutputTypeDef,
    ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef,
    ListRecoveryPointsByResourceOutputTypeDef,
    ListRestoreJobsByProtectedResourceInputListRestoreJobsByProtectedResourcePaginateTypeDef,
    ListRestoreJobsByProtectedResourceOutputTypeDef,
    ListRestoreJobsInputListRestoreJobsPaginateTypeDef,
    ListRestoreJobsOutputTypeDef,
    ListRestoreTestingPlansInputListRestoreTestingPlansPaginateTypeDef,
    ListRestoreTestingPlansOutputTypeDef,
    ListRestoreTestingSelectionsInputListRestoreTestingSelectionsPaginateTypeDef,
    ListRestoreTestingSelectionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListBackupJobsPaginator",
    "ListBackupPlanTemplatesPaginator",
    "ListBackupPlanVersionsPaginator",
    "ListBackupPlansPaginator",
    "ListBackupSelectionsPaginator",
    "ListBackupVaultsPaginator",
    "ListCopyJobsPaginator",
    "ListLegalHoldsPaginator",
    "ListProtectedResourcesByBackupVaultPaginator",
    "ListProtectedResourcesPaginator",
    "ListRecoveryPointsByBackupVaultPaginator",
    "ListRecoveryPointsByLegalHoldPaginator",
    "ListRecoveryPointsByResourcePaginator",
    "ListRestoreJobsByProtectedResourcePaginator",
    "ListRestoreJobsPaginator",
    "ListRestoreTestingPlansPaginator",
    "ListRestoreTestingSelectionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBackupJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupJobs.html#Backup.Paginator.ListBackupJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBackupJobsInputListBackupJobsPaginateTypeDef]
    ) -> _PageIterator[ListBackupJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupJobs.html#Backup.Paginator.ListBackupJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupjobspaginator)
        """


class ListBackupPlanTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanTemplates.html#Backup.Paginator.ListBackupPlanTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplantemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListBackupPlanTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanTemplates.html#Backup.Paginator.ListBackupPlanTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplantemplatespaginator)
        """


class ListBackupPlanVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanVersions.html#Backup.Paginator.ListBackupPlanVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef]
    ) -> _PageIterator[ListBackupPlanVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanVersions.html#Backup.Paginator.ListBackupPlanVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanversionspaginator)
        """


class ListBackupPlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlans.html#Backup.Paginator.ListBackupPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBackupPlansInputListBackupPlansPaginateTypeDef]
    ) -> _PageIterator[ListBackupPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlans.html#Backup.Paginator.ListBackupPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanspaginator)
        """


class ListBackupSelectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupSelections.html#Backup.Paginator.ListBackupSelections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupselectionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef]
    ) -> _PageIterator[ListBackupSelectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupSelections.html#Backup.Paginator.ListBackupSelections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupselectionspaginator)
        """


class ListBackupVaultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupVaults.html#Backup.Paginator.ListBackupVaults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupvaultspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBackupVaultsInputListBackupVaultsPaginateTypeDef]
    ) -> _PageIterator[ListBackupVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupVaults.html#Backup.Paginator.ListBackupVaults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupvaultspaginator)
        """


class ListCopyJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListCopyJobs.html#Backup.Paginator.ListCopyJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listcopyjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCopyJobsInputListCopyJobsPaginateTypeDef]
    ) -> _PageIterator[ListCopyJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListCopyJobs.html#Backup.Paginator.ListCopyJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listcopyjobspaginator)
        """


class ListLegalHoldsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListLegalHolds.html#Backup.Paginator.ListLegalHolds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listlegalholdspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLegalHoldsInputListLegalHoldsPaginateTypeDef]
    ) -> _PageIterator[ListLegalHoldsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListLegalHolds.html#Backup.Paginator.ListLegalHolds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listlegalholdspaginator)
        """


class ListProtectedResourcesByBackupVaultPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResourcesByBackupVault.html#Backup.Paginator.ListProtectedResourcesByBackupVault)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listprotectedresourcesbybackupvaultpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListProtectedResourcesByBackupVaultInputListProtectedResourcesByBackupVaultPaginateTypeDef
        ],
    ) -> _PageIterator[ListProtectedResourcesByBackupVaultOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResourcesByBackupVault.html#Backup.Paginator.ListProtectedResourcesByBackupVault.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listprotectedresourcesbybackupvaultpaginator)
        """


class ListProtectedResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResources.html#Backup.Paginator.ListProtectedResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listprotectedresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef]
    ) -> _PageIterator[ListProtectedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResources.html#Backup.Paginator.ListProtectedResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listprotectedresourcespaginator)
        """


class ListRecoveryPointsByBackupVaultPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByBackupVault.html#Backup.Paginator.ListRecoveryPointsByBackupVault)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbybackupvaultpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef
        ],
    ) -> _PageIterator[ListRecoveryPointsByBackupVaultOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByBackupVault.html#Backup.Paginator.ListRecoveryPointsByBackupVault.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbybackupvaultpaginator)
        """


class ListRecoveryPointsByLegalHoldPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByLegalHold.html#Backup.Paginator.ListRecoveryPointsByLegalHold)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbylegalholdpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef
        ],
    ) -> _PageIterator[ListRecoveryPointsByLegalHoldOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByLegalHold.html#Backup.Paginator.ListRecoveryPointsByLegalHold.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbylegalholdpaginator)
        """


class ListRecoveryPointsByResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByResource.html#Backup.Paginator.ListRecoveryPointsByResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbyresourcepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef
        ],
    ) -> _PageIterator[ListRecoveryPointsByResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByResource.html#Backup.Paginator.ListRecoveryPointsByResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbyresourcepaginator)
        """


class ListRestoreJobsByProtectedResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobsByProtectedResource.html#Backup.Paginator.ListRestoreJobsByProtectedResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestorejobsbyprotectedresourcepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRestoreJobsByProtectedResourceInputListRestoreJobsByProtectedResourcePaginateTypeDef
        ],
    ) -> _PageIterator[ListRestoreJobsByProtectedResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobsByProtectedResource.html#Backup.Paginator.ListRestoreJobsByProtectedResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestorejobsbyprotectedresourcepaginator)
        """


class ListRestoreJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobs.html#Backup.Paginator.ListRestoreJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestorejobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRestoreJobsInputListRestoreJobsPaginateTypeDef]
    ) -> _PageIterator[ListRestoreJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobs.html#Backup.Paginator.ListRestoreJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestorejobspaginator)
        """


class ListRestoreTestingPlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingPlans.html#Backup.Paginator.ListRestoreTestingPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestoretestingplanspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRestoreTestingPlansInputListRestoreTestingPlansPaginateTypeDef]
    ) -> _PageIterator[ListRestoreTestingPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingPlans.html#Backup.Paginator.ListRestoreTestingPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestoretestingplanspaginator)
        """


class ListRestoreTestingSelectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingSelections.html#Backup.Paginator.ListRestoreTestingSelections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestoretestingselectionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRestoreTestingSelectionsInputListRestoreTestingSelectionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListRestoreTestingSelectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingSelections.html#Backup.Paginator.ListRestoreTestingSelections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestoretestingselectionspaginator)
        """
