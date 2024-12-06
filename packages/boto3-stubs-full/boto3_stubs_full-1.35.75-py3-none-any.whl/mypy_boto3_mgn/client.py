"""
Type annotations for mgn service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mgn.client import MgnClient

    session = Session()
    client: MgnClient = session.client("mgn")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
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
from .type_defs import (
    ApplicationResponseTypeDef,
    ArchiveApplicationRequestRequestTypeDef,
    ArchiveWaveRequestRequestTypeDef,
    AssociateApplicationsRequestRequestTypeDef,
    AssociateSourceServersRequestRequestTypeDef,
    ChangeServerLifeCycleStateRequestRequestTypeDef,
    ConnectorResponseTypeDef,
    CreateApplicationRequestRequestTypeDef,
    CreateConnectorRequestRequestTypeDef,
    CreateLaunchConfigurationTemplateRequestRequestTypeDef,
    CreateReplicationConfigurationTemplateRequestRequestTypeDef,
    CreateWaveRequestRequestTypeDef,
    DeleteApplicationRequestRequestTypeDef,
    DeleteConnectorRequestRequestTypeDef,
    DeleteJobRequestRequestTypeDef,
    DeleteLaunchConfigurationTemplateRequestRequestTypeDef,
    DeleteReplicationConfigurationTemplateRequestRequestTypeDef,
    DeleteSourceServerRequestRequestTypeDef,
    DeleteVcenterClientRequestRequestTypeDef,
    DeleteWaveRequestRequestTypeDef,
    DescribeJobLogItemsRequestRequestTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestRequestTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeLaunchConfigurationTemplatesRequestRequestTypeDef,
    DescribeLaunchConfigurationTemplatesResponseTypeDef,
    DescribeReplicationConfigurationTemplatesRequestRequestTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestRequestTypeDef,
    DescribeSourceServersResponseTypeDef,
    DescribeVcenterClientsRequestRequestTypeDef,
    DescribeVcenterClientsResponseTypeDef,
    DisassociateApplicationsRequestRequestTypeDef,
    DisassociateSourceServersRequestRequestTypeDef,
    DisconnectFromServiceRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    FinalizeCutoverRequestRequestTypeDef,
    GetLaunchConfigurationRequestRequestTypeDef,
    GetReplicationConfigurationRequestRequestTypeDef,
    LaunchConfigurationTemplateResponseTypeDef,
    LaunchConfigurationTypeDef,
    ListApplicationsRequestRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListConnectorsRequestRequestTypeDef,
    ListConnectorsResponseTypeDef,
    ListExportErrorsRequestRequestTypeDef,
    ListExportErrorsResponseTypeDef,
    ListExportsRequestRequestTypeDef,
    ListExportsResponseTypeDef,
    ListImportErrorsRequestRequestTypeDef,
    ListImportErrorsResponseTypeDef,
    ListImportsRequestRequestTypeDef,
    ListImportsResponseTypeDef,
    ListManagedAccountsRequestRequestTypeDef,
    ListManagedAccountsResponseTypeDef,
    ListSourceServerActionsRequestRequestTypeDef,
    ListSourceServerActionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplateActionsRequestRequestTypeDef,
    ListTemplateActionsResponseTypeDef,
    ListWavesRequestRequestTypeDef,
    ListWavesResponseTypeDef,
    MarkAsArchivedRequestRequestTypeDef,
    PauseReplicationRequestRequestTypeDef,
    PutSourceServerActionRequestRequestTypeDef,
    PutTemplateActionRequestRequestTypeDef,
    RemoveSourceServerActionRequestRequestTypeDef,
    RemoveTemplateActionRequestRequestTypeDef,
    ReplicationConfigurationTemplateResponseTypeDef,
    ReplicationConfigurationTypeDef,
    ResumeReplicationRequestRequestTypeDef,
    RetryDataReplicationRequestRequestTypeDef,
    SourceServerActionDocumentResponseTypeDef,
    SourceServerResponseTypeDef,
    StartCutoverRequestRequestTypeDef,
    StartCutoverResponseTypeDef,
    StartExportRequestRequestTypeDef,
    StartExportResponseTypeDef,
    StartImportRequestRequestTypeDef,
    StartImportResponseTypeDef,
    StartReplicationRequestRequestTypeDef,
    StartTestRequestRequestTypeDef,
    StartTestResponseTypeDef,
    StopReplicationRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    TemplateActionDocumentResponseTypeDef,
    TerminateTargetInstancesRequestRequestTypeDef,
    TerminateTargetInstancesResponseTypeDef,
    UnarchiveApplicationRequestRequestTypeDef,
    UnarchiveWaveRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApplicationRequestRequestTypeDef,
    UpdateConnectorRequestRequestTypeDef,
    UpdateLaunchConfigurationRequestRequestTypeDef,
    UpdateLaunchConfigurationTemplateRequestRequestTypeDef,
    UpdateReplicationConfigurationRequestRequestTypeDef,
    UpdateReplicationConfigurationTemplateRequestRequestTypeDef,
    UpdateSourceServerReplicationTypeRequestRequestTypeDef,
    UpdateSourceServerRequestRequestTypeDef,
    UpdateWaveRequestRequestTypeDef,
    WaveResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MgnClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UninitializedAccountException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MgnClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MgnClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#close)
        """

    def archive_application(
        self, **kwargs: Unpack[ArchiveApplicationRequestRequestTypeDef]
    ) -> ApplicationResponseTypeDef:
        """
        Archive application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/archive_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#archive_application)
        """

    def archive_wave(
        self, **kwargs: Unpack[ArchiveWaveRequestRequestTypeDef]
    ) -> WaveResponseTypeDef:
        """
        Archive wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/archive_wave.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#archive_wave)
        """

    def associate_applications(
        self, **kwargs: Unpack[AssociateApplicationsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate applications to wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/associate_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#associate_applications)
        """

    def associate_source_servers(
        self, **kwargs: Unpack[AssociateSourceServersRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate source servers to application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/associate_source_servers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#associate_source_servers)
        """

    def change_server_life_cycle_state(
        self, **kwargs: Unpack[ChangeServerLifeCycleStateRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Allows the user to set the SourceServer.LifeCycle.state property for specific
        Source Server IDs to one of the following: READY_FOR_TEST or READY_FOR_CUTOVER.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/change_server_life_cycle_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#change_server_life_cycle_state)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestRequestTypeDef]
    ) -> ApplicationResponseTypeDef:
        """
        Create application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/create_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#create_application)
        """

    def create_connector(
        self, **kwargs: Unpack[CreateConnectorRequestRequestTypeDef]
    ) -> ConnectorResponseTypeDef:
        """
        Create Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/create_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#create_connector)
        """

    def create_launch_configuration_template(
        self, **kwargs: Unpack[CreateLaunchConfigurationTemplateRequestRequestTypeDef]
    ) -> LaunchConfigurationTemplateResponseTypeDef:
        """
        Creates a new Launch Configuration Template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/create_launch_configuration_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#create_launch_configuration_template)
        """

    def create_replication_configuration_template(
        self, **kwargs: Unpack[CreateReplicationConfigurationTemplateRequestRequestTypeDef]
    ) -> ReplicationConfigurationTemplateResponseTypeDef:
        """
        Creates a new ReplicationConfigurationTemplate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/create_replication_configuration_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#create_replication_configuration_template)
        """

    def create_wave(self, **kwargs: Unpack[CreateWaveRequestRequestTypeDef]) -> WaveResponseTypeDef:
        """
        Create wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/create_wave.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#create_wave)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_application)
        """

    def delete_connector(
        self, **kwargs: Unpack[DeleteConnectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_connector)
        """

    def delete_job(self, **kwargs: Unpack[DeleteJobRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a single Job by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_job)
        """

    def delete_launch_configuration_template(
        self, **kwargs: Unpack[DeleteLaunchConfigurationTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a single Launch Configuration Template by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_launch_configuration_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_launch_configuration_template)
        """

    def delete_replication_configuration_template(
        self, **kwargs: Unpack[DeleteReplicationConfigurationTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a single Replication Configuration Template by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_replication_configuration_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_replication_configuration_template)
        """

    def delete_source_server(
        self, **kwargs: Unpack[DeleteSourceServerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a single source server by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_source_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_source_server)
        """

    def delete_vcenter_client(
        self, **kwargs: Unpack[DeleteVcenterClientRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a given vCenter client by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_vcenter_client.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_vcenter_client)
        """

    def delete_wave(self, **kwargs: Unpack[DeleteWaveRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Delete wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/delete_wave.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#delete_wave)
        """

    def describe_job_log_items(
        self, **kwargs: Unpack[DescribeJobLogItemsRequestRequestTypeDef]
    ) -> DescribeJobLogItemsResponseTypeDef:
        """
        Retrieves detailed job log items with paging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/describe_job_log_items.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#describe_job_log_items)
        """

    def describe_jobs(
        self, **kwargs: Unpack[DescribeJobsRequestRequestTypeDef]
    ) -> DescribeJobsResponseTypeDef:
        """
        Returns a list of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/describe_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#describe_jobs)
        """

    def describe_launch_configuration_templates(
        self, **kwargs: Unpack[DescribeLaunchConfigurationTemplatesRequestRequestTypeDef]
    ) -> DescribeLaunchConfigurationTemplatesResponseTypeDef:
        """
        Lists all Launch Configuration Templates, filtered by Launch Configuration
        Template IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/describe_launch_configuration_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#describe_launch_configuration_templates)
        """

    def describe_replication_configuration_templates(
        self, **kwargs: Unpack[DescribeReplicationConfigurationTemplatesRequestRequestTypeDef]
    ) -> DescribeReplicationConfigurationTemplatesResponseTypeDef:
        """
        Lists all ReplicationConfigurationTemplates, filtered by Source Server IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/describe_replication_configuration_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#describe_replication_configuration_templates)
        """

    def describe_source_servers(
        self, **kwargs: Unpack[DescribeSourceServersRequestRequestTypeDef]
    ) -> DescribeSourceServersResponseTypeDef:
        """
        Retrieves all SourceServers or multiple SourceServers by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/describe_source_servers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#describe_source_servers)
        """

    def describe_vcenter_clients(
        self, **kwargs: Unpack[DescribeVcenterClientsRequestRequestTypeDef]
    ) -> DescribeVcenterClientsResponseTypeDef:
        """
        Returns a list of the installed vCenter clients.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/describe_vcenter_clients.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#describe_vcenter_clients)
        """

    def disassociate_applications(
        self, **kwargs: Unpack[DisassociateApplicationsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociate applications from wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/disassociate_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#disassociate_applications)
        """

    def disassociate_source_servers(
        self, **kwargs: Unpack[DisassociateSourceServersRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociate source servers from application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/disassociate_source_servers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#disassociate_source_servers)
        """

    def disconnect_from_service(
        self, **kwargs: Unpack[DisconnectFromServiceRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Disconnects specific Source Servers from Application Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/disconnect_from_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#disconnect_from_service)
        """

    def finalize_cutover(
        self, **kwargs: Unpack[FinalizeCutoverRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Finalizes the cutover immediately for specific Source Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/finalize_cutover.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#finalize_cutover)
        """

    def get_launch_configuration(
        self, **kwargs: Unpack[GetLaunchConfigurationRequestRequestTypeDef]
    ) -> LaunchConfigurationTypeDef:
        """
        Lists all LaunchConfigurations available, filtered by Source Server IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_launch_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_launch_configuration)
        """

    def get_replication_configuration(
        self, **kwargs: Unpack[GetReplicationConfigurationRequestRequestTypeDef]
    ) -> ReplicationConfigurationTypeDef:
        """
        Lists all ReplicationConfigurations, filtered by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_replication_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_replication_configuration)
        """

    def initialize_service(self) -> Dict[str, Any]:
        """
        Initialize Application Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/initialize_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#initialize_service)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Retrieves all applications or multiple applications by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_applications)
        """

    def list_connectors(
        self, **kwargs: Unpack[ListConnectorsRequestRequestTypeDef]
    ) -> ListConnectorsResponseTypeDef:
        """
        List Connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_connectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_connectors)
        """

    def list_export_errors(
        self, **kwargs: Unpack[ListExportErrorsRequestRequestTypeDef]
    ) -> ListExportErrorsResponseTypeDef:
        """
        List export errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_export_errors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_export_errors)
        """

    def list_exports(
        self, **kwargs: Unpack[ListExportsRequestRequestTypeDef]
    ) -> ListExportsResponseTypeDef:
        """
        List exports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_exports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_exports)
        """

    def list_import_errors(
        self, **kwargs: Unpack[ListImportErrorsRequestRequestTypeDef]
    ) -> ListImportErrorsResponseTypeDef:
        """
        List import errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_import_errors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_import_errors)
        """

    def list_imports(
        self, **kwargs: Unpack[ListImportsRequestRequestTypeDef]
    ) -> ListImportsResponseTypeDef:
        """
        List imports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_imports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_imports)
        """

    def list_managed_accounts(
        self, **kwargs: Unpack[ListManagedAccountsRequestRequestTypeDef]
    ) -> ListManagedAccountsResponseTypeDef:
        """
        List Managed Accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_managed_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_managed_accounts)
        """

    def list_source_server_actions(
        self, **kwargs: Unpack[ListSourceServerActionsRequestRequestTypeDef]
    ) -> ListSourceServerActionsResponseTypeDef:
        """
        List source server post migration custom actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_source_server_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_source_server_actions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags for your Application Migration Service resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_tags_for_resource)
        """

    def list_template_actions(
        self, **kwargs: Unpack[ListTemplateActionsRequestRequestTypeDef]
    ) -> ListTemplateActionsResponseTypeDef:
        """
        List template post migration custom actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_template_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_template_actions)
        """

    def list_waves(
        self, **kwargs: Unpack[ListWavesRequestRequestTypeDef]
    ) -> ListWavesResponseTypeDef:
        """
        Retrieves all waves or multiple waves by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/list_waves.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#list_waves)
        """

    def mark_as_archived(
        self, **kwargs: Unpack[MarkAsArchivedRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Archives specific Source Servers by setting the SourceServer.isArchived
        property to true for specified SourceServers by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/mark_as_archived.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#mark_as_archived)
        """

    def pause_replication(
        self, **kwargs: Unpack[PauseReplicationRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Pause Replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/pause_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#pause_replication)
        """

    def put_source_server_action(
        self, **kwargs: Unpack[PutSourceServerActionRequestRequestTypeDef]
    ) -> SourceServerActionDocumentResponseTypeDef:
        """
        Put source server post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/put_source_server_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#put_source_server_action)
        """

    def put_template_action(
        self, **kwargs: Unpack[PutTemplateActionRequestRequestTypeDef]
    ) -> TemplateActionDocumentResponseTypeDef:
        """
        Put template post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/put_template_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#put_template_action)
        """

    def remove_source_server_action(
        self, **kwargs: Unpack[RemoveSourceServerActionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove source server post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/remove_source_server_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#remove_source_server_action)
        """

    def remove_template_action(
        self, **kwargs: Unpack[RemoveTemplateActionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove template post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/remove_template_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#remove_template_action)
        """

    def resume_replication(
        self, **kwargs: Unpack[ResumeReplicationRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Resume Replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/resume_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#resume_replication)
        """

    def retry_data_replication(
        self, **kwargs: Unpack[RetryDataReplicationRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Causes the data replication initiation sequence to begin immediately upon next
        Handshake for specified SourceServer IDs, regardless of when the previous
        initiation started.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/retry_data_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#retry_data_replication)
        """

    def start_cutover(
        self, **kwargs: Unpack[StartCutoverRequestRequestTypeDef]
    ) -> StartCutoverResponseTypeDef:
        """
        Launches a Cutover Instance for specific Source Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/start_cutover.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#start_cutover)
        """

    def start_export(
        self, **kwargs: Unpack[StartExportRequestRequestTypeDef]
    ) -> StartExportResponseTypeDef:
        """
        Start export.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/start_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#start_export)
        """

    def start_import(
        self, **kwargs: Unpack[StartImportRequestRequestTypeDef]
    ) -> StartImportResponseTypeDef:
        """
        Start import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/start_import.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#start_import)
        """

    def start_replication(
        self, **kwargs: Unpack[StartReplicationRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Starts replication for SNAPSHOT_SHIPPING agents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/start_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#start_replication)
        """

    def start_test(
        self, **kwargs: Unpack[StartTestRequestRequestTypeDef]
    ) -> StartTestResponseTypeDef:
        """
        Launches a Test Instance for specific Source Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/start_test.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#start_test)
        """

    def stop_replication(
        self, **kwargs: Unpack[StopReplicationRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Stop Replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/stop_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#stop_replication)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or overwrites only the specified tags for the specified Application
        Migration Service resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#tag_resource)
        """

    def terminate_target_instances(
        self, **kwargs: Unpack[TerminateTargetInstancesRequestRequestTypeDef]
    ) -> TerminateTargetInstancesResponseTypeDef:
        """
        Starts a job that terminates specific launched EC2 Test and Cutover instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/terminate_target_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#terminate_target_instances)
        """

    def unarchive_application(
        self, **kwargs: Unpack[UnarchiveApplicationRequestRequestTypeDef]
    ) -> ApplicationResponseTypeDef:
        """
        Unarchive application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/unarchive_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#unarchive_application)
        """

    def unarchive_wave(
        self, **kwargs: Unpack[UnarchiveWaveRequestRequestTypeDef]
    ) -> WaveResponseTypeDef:
        """
        Unarchive wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/unarchive_wave.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#unarchive_wave)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified set of tags from the specified set of Application
        Migration Service resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#untag_resource)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestRequestTypeDef]
    ) -> ApplicationResponseTypeDef:
        """
        Update application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_application)
        """

    def update_connector(
        self, **kwargs: Unpack[UpdateConnectorRequestRequestTypeDef]
    ) -> ConnectorResponseTypeDef:
        """
        Update Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_connector)
        """

    def update_launch_configuration(
        self, **kwargs: Unpack[UpdateLaunchConfigurationRequestRequestTypeDef]
    ) -> LaunchConfigurationTypeDef:
        """
        Updates multiple LaunchConfigurations by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_launch_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_launch_configuration)
        """

    def update_launch_configuration_template(
        self, **kwargs: Unpack[UpdateLaunchConfigurationTemplateRequestRequestTypeDef]
    ) -> LaunchConfigurationTemplateResponseTypeDef:
        """
        Updates an existing Launch Configuration Template by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_launch_configuration_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_launch_configuration_template)
        """

    def update_replication_configuration(
        self, **kwargs: Unpack[UpdateReplicationConfigurationRequestRequestTypeDef]
    ) -> ReplicationConfigurationTypeDef:
        """
        Allows you to update multiple ReplicationConfigurations by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_replication_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_replication_configuration)
        """

    def update_replication_configuration_template(
        self, **kwargs: Unpack[UpdateReplicationConfigurationTemplateRequestRequestTypeDef]
    ) -> ReplicationConfigurationTemplateResponseTypeDef:
        """
        Updates multiple ReplicationConfigurationTemplates by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_replication_configuration_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_replication_configuration_template)
        """

    def update_source_server(
        self, **kwargs: Unpack[UpdateSourceServerRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Update Source Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_source_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_source_server)
        """

    def update_source_server_replication_type(
        self, **kwargs: Unpack[UpdateSourceServerReplicationTypeRequestRequestTypeDef]
    ) -> SourceServerResponseTypeDef:
        """
        Allows you to change between the AGENT_BASED replication type and the
        SNAPSHOT_SHIPPING replication type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_source_server_replication_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_source_server_replication_type)
        """

    def update_wave(self, **kwargs: Unpack[UpdateWaveRequestRequestTypeDef]) -> WaveResponseTypeDef:
        """
        Update wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/update_wave.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#update_wave)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_log_items"]
    ) -> DescribeJobLogItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_jobs"]) -> DescribeJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_configuration_templates"]
    ) -> DescribeLaunchConfigurationTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_configuration_templates"]
    ) -> DescribeReplicationConfigurationTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_source_servers"]
    ) -> DescribeSourceServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vcenter_clients"]
    ) -> DescribeVcenterClientsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_connectors"]) -> ListConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_export_errors"]
    ) -> ListExportErrorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_exports"]) -> ListExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_import_errors"]
    ) -> ListImportErrorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_imports"]) -> ListImportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_accounts"]
    ) -> ListManagedAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_server_actions"]
    ) -> ListSourceServerActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_template_actions"]
    ) -> ListTemplateActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_waves"]) -> ListWavesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/client/#get_paginator)
        """
