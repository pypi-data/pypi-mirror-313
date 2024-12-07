"""
Type annotations for mgn service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mgn.client import MgnClient
    from mypy_boto3_mgn.paginator import (
        DescribeJobLogItemsPaginator,
        DescribeJobsPaginator,
        DescribeLaunchConfigurationTemplatesPaginator,
        DescribeReplicationConfigurationTemplatesPaginator,
        DescribeSourceServersPaginator,
        DescribeVcenterClientsPaginator,
        ListApplicationsPaginator,
        ListConnectorsPaginator,
        ListExportErrorsPaginator,
        ListExportsPaginator,
        ListImportErrorsPaginator,
        ListImportsPaginator,
        ListManagedAccountsPaginator,
        ListSourceServerActionsPaginator,
        ListTemplateActionsPaginator,
        ListWavesPaginator,
    )

    session = Session()
    client: MgnClient = session.client("mgn")

    describe_job_log_items_paginator: DescribeJobLogItemsPaginator = client.get_paginator("describe_job_log_items")
    describe_jobs_paginator: DescribeJobsPaginator = client.get_paginator("describe_jobs")
    describe_launch_configuration_templates_paginator: DescribeLaunchConfigurationTemplatesPaginator = client.get_paginator("describe_launch_configuration_templates")
    describe_replication_configuration_templates_paginator: DescribeReplicationConfigurationTemplatesPaginator = client.get_paginator("describe_replication_configuration_templates")
    describe_source_servers_paginator: DescribeSourceServersPaginator = client.get_paginator("describe_source_servers")
    describe_vcenter_clients_paginator: DescribeVcenterClientsPaginator = client.get_paginator("describe_vcenter_clients")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_export_errors_paginator: ListExportErrorsPaginator = client.get_paginator("list_export_errors")
    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    list_import_errors_paginator: ListImportErrorsPaginator = client.get_paginator("list_import_errors")
    list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
    list_managed_accounts_paginator: ListManagedAccountsPaginator = client.get_paginator("list_managed_accounts")
    list_source_server_actions_paginator: ListSourceServerActionsPaginator = client.get_paginator("list_source_server_actions")
    list_template_actions_paginator: ListTemplateActionsPaginator = client.get_paginator("list_template_actions")
    list_waves_paginator: ListWavesPaginator = client.get_paginator("list_waves")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestDescribeJobsPaginateTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef,
    DescribeLaunchConfigurationTemplatesResponseTypeDef,
    DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef,
    DescribeSourceServersResponseTypeDef,
    DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef,
    DescribeVcenterClientsResponseTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListConnectorsRequestListConnectorsPaginateTypeDef,
    ListConnectorsResponseTypeDef,
    ListExportErrorsRequestListExportErrorsPaginateTypeDef,
    ListExportErrorsResponseTypeDef,
    ListExportsRequestListExportsPaginateTypeDef,
    ListExportsResponseTypeDef,
    ListImportErrorsRequestListImportErrorsPaginateTypeDef,
    ListImportErrorsResponseTypeDef,
    ListImportsRequestListImportsPaginateTypeDef,
    ListImportsResponseTypeDef,
    ListManagedAccountsRequestListManagedAccountsPaginateTypeDef,
    ListManagedAccountsResponseTypeDef,
    ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef,
    ListSourceServerActionsResponseTypeDef,
    ListTemplateActionsRequestListTemplateActionsPaginateTypeDef,
    ListTemplateActionsResponseTypeDef,
    ListWavesRequestListWavesPaginateTypeDef,
    ListWavesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeJobLogItemsPaginator",
    "DescribeJobsPaginator",
    "DescribeLaunchConfigurationTemplatesPaginator",
    "DescribeReplicationConfigurationTemplatesPaginator",
    "DescribeSourceServersPaginator",
    "DescribeVcenterClientsPaginator",
    "ListApplicationsPaginator",
    "ListConnectorsPaginator",
    "ListExportErrorsPaginator",
    "ListExportsPaginator",
    "ListImportErrorsPaginator",
    "ListImportsPaginator",
    "ListManagedAccountsPaginator",
    "ListSourceServerActionsPaginator",
    "ListTemplateActionsPaginator",
    "ListWavesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeJobLogItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobLogItems.html#Mgn.Paginator.DescribeJobLogItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejoblogitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef]
    ) -> _PageIterator[DescribeJobLogItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobLogItems.html#Mgn.Paginator.DescribeJobLogItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejoblogitemspaginator)
        """


class DescribeJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobs.html#Mgn.Paginator.DescribeJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeJobsRequestDescribeJobsPaginateTypeDef]
    ) -> _PageIterator[DescribeJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobs.html#Mgn.Paginator.DescribeJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejobspaginator)
        """


class DescribeLaunchConfigurationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeLaunchConfigurationTemplates.html#Mgn.Paginator.DescribeLaunchConfigurationTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLaunchConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeLaunchConfigurationTemplates.html#Mgn.Paginator.DescribeLaunchConfigurationTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
        """


class DescribeReplicationConfigurationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeReplicationConfigurationTemplates.html#Mgn.Paginator.DescribeReplicationConfigurationTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReplicationConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeReplicationConfigurationTemplates.html#Mgn.Paginator.DescribeReplicationConfigurationTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
        """


class DescribeSourceServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeSourceServers.html#Mgn.Paginator.DescribeSourceServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describesourceserverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef]
    ) -> _PageIterator[DescribeSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeSourceServers.html#Mgn.Paginator.DescribeSourceServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describesourceserverspaginator)
        """


class DescribeVcenterClientsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeVcenterClients.html#Mgn.Paginator.DescribeVcenterClients)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describevcenterclientspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef]
    ) -> _PageIterator[DescribeVcenterClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeVcenterClients.html#Mgn.Paginator.DescribeVcenterClients.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describevcenterclientspaginator)
        """


class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListApplications.html#Mgn.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListApplications.html#Mgn.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listapplicationspaginator)
        """


class ListConnectorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListConnectors.html#Mgn.Paginator.ListConnectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listconnectorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListConnectorsRequestListConnectorsPaginateTypeDef]
    ) -> _PageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListConnectors.html#Mgn.Paginator.ListConnectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listconnectorspaginator)
        """


class ListExportErrorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExportErrors.html#Mgn.Paginator.ListExportErrors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexporterrorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExportErrorsRequestListExportErrorsPaginateTypeDef]
    ) -> _PageIterator[ListExportErrorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExportErrors.html#Mgn.Paginator.ListExportErrors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexporterrorspaginator)
        """


class ListExportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExports.html#Mgn.Paginator.ListExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExportsRequestListExportsPaginateTypeDef]
    ) -> _PageIterator[ListExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExports.html#Mgn.Paginator.ListExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexportspaginator)
        """


class ListImportErrorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportErrors.html#Mgn.Paginator.ListImportErrors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimporterrorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportErrorsRequestListImportErrorsPaginateTypeDef]
    ) -> _PageIterator[ListImportErrorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportErrors.html#Mgn.Paginator.ListImportErrors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimporterrorspaginator)
        """


class ListImportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImports.html#Mgn.Paginator.ListImports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportsRequestListImportsPaginateTypeDef]
    ) -> _PageIterator[ListImportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImports.html#Mgn.Paginator.ListImports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimportspaginator)
        """


class ListManagedAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListManagedAccounts.html#Mgn.Paginator.ListManagedAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listmanagedaccountspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListManagedAccountsRequestListManagedAccountsPaginateTypeDef]
    ) -> _PageIterator[ListManagedAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListManagedAccounts.html#Mgn.Paginator.ListManagedAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listmanagedaccountspaginator)
        """


class ListSourceServerActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListSourceServerActions.html#Mgn.Paginator.ListSourceServerActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listsourceserveractionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef]
    ) -> _PageIterator[ListSourceServerActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListSourceServerActions.html#Mgn.Paginator.ListSourceServerActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listsourceserveractionspaginator)
        """


class ListTemplateActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListTemplateActions.html#Mgn.Paginator.ListTemplateActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listtemplateactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplateActionsRequestListTemplateActionsPaginateTypeDef]
    ) -> _PageIterator[ListTemplateActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListTemplateActions.html#Mgn.Paginator.ListTemplateActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listtemplateactionspaginator)
        """


class ListWavesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListWaves.html#Mgn.Paginator.ListWaves)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listwavespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWavesRequestListWavesPaginateTypeDef]
    ) -> _PageIterator[ListWavesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListWaves.html#Mgn.Paginator.ListWaves.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listwavespaginator)
        """
