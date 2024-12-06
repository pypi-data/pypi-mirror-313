"""
Type annotations for dms service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dms.client import DatabaseMigrationServiceClient

    session = Session()
    client: DatabaseMigrationServiceClient = session.client("dms")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeCertificatesPaginator,
    DescribeConnectionsPaginator,
    DescribeDataMigrationsPaginator,
    DescribeEndpointsPaginator,
    DescribeEndpointTypesPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeOrderableReplicationInstancesPaginator,
    DescribeReplicationInstancesPaginator,
    DescribeReplicationSubnetGroupsPaginator,
    DescribeReplicationTaskAssessmentResultsPaginator,
    DescribeReplicationTasksPaginator,
    DescribeSchemasPaginator,
    DescribeTableStatisticsPaginator,
)
from .type_defs import (
    AddTagsToResourceMessageRequestTypeDef,
    ApplyPendingMaintenanceActionMessageRequestTypeDef,
    ApplyPendingMaintenanceActionResponseTypeDef,
    BatchStartRecommendationsRequestRequestTypeDef,
    BatchStartRecommendationsResponseTypeDef,
    CancelReplicationTaskAssessmentRunMessageRequestTypeDef,
    CancelReplicationTaskAssessmentRunResponseTypeDef,
    CreateDataMigrationMessageRequestTypeDef,
    CreateDataMigrationResponseTypeDef,
    CreateDataProviderMessageRequestTypeDef,
    CreateDataProviderResponseTypeDef,
    CreateEndpointMessageRequestTypeDef,
    CreateEndpointResponseTypeDef,
    CreateEventSubscriptionMessageRequestTypeDef,
    CreateEventSubscriptionResponseTypeDef,
    CreateFleetAdvisorCollectorRequestRequestTypeDef,
    CreateFleetAdvisorCollectorResponseTypeDef,
    CreateInstanceProfileMessageRequestTypeDef,
    CreateInstanceProfileResponseTypeDef,
    CreateMigrationProjectMessageRequestTypeDef,
    CreateMigrationProjectResponseTypeDef,
    CreateReplicationConfigMessageRequestTypeDef,
    CreateReplicationConfigResponseTypeDef,
    CreateReplicationInstanceMessageRequestTypeDef,
    CreateReplicationInstanceResponseTypeDef,
    CreateReplicationSubnetGroupMessageRequestTypeDef,
    CreateReplicationSubnetGroupResponseTypeDef,
    CreateReplicationTaskMessageRequestTypeDef,
    CreateReplicationTaskResponseTypeDef,
    DeleteCertificateMessageRequestTypeDef,
    DeleteCertificateResponseTypeDef,
    DeleteCollectorRequestRequestTypeDef,
    DeleteConnectionMessageRequestTypeDef,
    DeleteConnectionResponseTypeDef,
    DeleteDataMigrationMessageRequestTypeDef,
    DeleteDataMigrationResponseTypeDef,
    DeleteDataProviderMessageRequestTypeDef,
    DeleteDataProviderResponseTypeDef,
    DeleteEndpointMessageRequestTypeDef,
    DeleteEndpointResponseTypeDef,
    DeleteEventSubscriptionMessageRequestTypeDef,
    DeleteEventSubscriptionResponseTypeDef,
    DeleteFleetAdvisorDatabasesRequestRequestTypeDef,
    DeleteFleetAdvisorDatabasesResponseTypeDef,
    DeleteInstanceProfileMessageRequestTypeDef,
    DeleteInstanceProfileResponseTypeDef,
    DeleteMigrationProjectMessageRequestTypeDef,
    DeleteMigrationProjectResponseTypeDef,
    DeleteReplicationConfigMessageRequestTypeDef,
    DeleteReplicationConfigResponseTypeDef,
    DeleteReplicationInstanceMessageRequestTypeDef,
    DeleteReplicationInstanceResponseTypeDef,
    DeleteReplicationSubnetGroupMessageRequestTypeDef,
    DeleteReplicationTaskAssessmentRunMessageRequestTypeDef,
    DeleteReplicationTaskAssessmentRunResponseTypeDef,
    DeleteReplicationTaskMessageRequestTypeDef,
    DeleteReplicationTaskResponseTypeDef,
    DescribeAccountAttributesResponseTypeDef,
    DescribeApplicableIndividualAssessmentsMessageRequestTypeDef,
    DescribeApplicableIndividualAssessmentsResponseTypeDef,
    DescribeCertificatesMessageRequestTypeDef,
    DescribeCertificatesResponseTypeDef,
    DescribeConnectionsMessageRequestTypeDef,
    DescribeConnectionsResponseTypeDef,
    DescribeConversionConfigurationMessageRequestTypeDef,
    DescribeConversionConfigurationResponseTypeDef,
    DescribeDataMigrationsMessageRequestTypeDef,
    DescribeDataMigrationsResponseTypeDef,
    DescribeDataProvidersMessageRequestTypeDef,
    DescribeDataProvidersResponseTypeDef,
    DescribeEndpointSettingsMessageRequestTypeDef,
    DescribeEndpointSettingsResponseTypeDef,
    DescribeEndpointsMessageRequestTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeEndpointTypesMessageRequestTypeDef,
    DescribeEndpointTypesResponseTypeDef,
    DescribeEngineVersionsMessageRequestTypeDef,
    DescribeEngineVersionsResponseTypeDef,
    DescribeEventCategoriesMessageRequestTypeDef,
    DescribeEventCategoriesResponseTypeDef,
    DescribeEventsMessageRequestTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventSubscriptionsMessageRequestTypeDef,
    DescribeEventSubscriptionsResponseTypeDef,
    DescribeExtensionPackAssociationsMessageRequestTypeDef,
    DescribeExtensionPackAssociationsResponseTypeDef,
    DescribeFleetAdvisorCollectorsRequestRequestTypeDef,
    DescribeFleetAdvisorCollectorsResponseTypeDef,
    DescribeFleetAdvisorDatabasesRequestRequestTypeDef,
    DescribeFleetAdvisorDatabasesResponseTypeDef,
    DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef,
    DescribeFleetAdvisorLsaAnalysisResponseTypeDef,
    DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef,
    DescribeFleetAdvisorSchemaObjectSummaryResponseTypeDef,
    DescribeFleetAdvisorSchemasRequestRequestTypeDef,
    DescribeFleetAdvisorSchemasResponseTypeDef,
    DescribeInstanceProfilesMessageRequestTypeDef,
    DescribeInstanceProfilesResponseTypeDef,
    DescribeMetadataModelAssessmentsMessageRequestTypeDef,
    DescribeMetadataModelAssessmentsResponseTypeDef,
    DescribeMetadataModelConversionsMessageRequestTypeDef,
    DescribeMetadataModelConversionsResponseTypeDef,
    DescribeMetadataModelExportsAsScriptMessageRequestTypeDef,
    DescribeMetadataModelExportsAsScriptResponseTypeDef,
    DescribeMetadataModelExportsToTargetMessageRequestTypeDef,
    DescribeMetadataModelExportsToTargetResponseTypeDef,
    DescribeMetadataModelImportsMessageRequestTypeDef,
    DescribeMetadataModelImportsResponseTypeDef,
    DescribeMigrationProjectsMessageRequestTypeDef,
    DescribeMigrationProjectsResponseTypeDef,
    DescribeOrderableReplicationInstancesMessageRequestTypeDef,
    DescribeOrderableReplicationInstancesResponseTypeDef,
    DescribePendingMaintenanceActionsMessageRequestTypeDef,
    DescribePendingMaintenanceActionsResponseTypeDef,
    DescribeRecommendationLimitationsRequestRequestTypeDef,
    DescribeRecommendationLimitationsResponseTypeDef,
    DescribeRecommendationsRequestRequestTypeDef,
    DescribeRecommendationsResponseTypeDef,
    DescribeRefreshSchemasStatusMessageRequestTypeDef,
    DescribeRefreshSchemasStatusResponseTypeDef,
    DescribeReplicationConfigsMessageRequestTypeDef,
    DescribeReplicationConfigsResponseTypeDef,
    DescribeReplicationInstancesMessageRequestTypeDef,
    DescribeReplicationInstancesResponseTypeDef,
    DescribeReplicationInstanceTaskLogsMessageRequestTypeDef,
    DescribeReplicationInstanceTaskLogsResponseTypeDef,
    DescribeReplicationsMessageRequestTypeDef,
    DescribeReplicationsResponseTypeDef,
    DescribeReplicationSubnetGroupsMessageRequestTypeDef,
    DescribeReplicationSubnetGroupsResponseTypeDef,
    DescribeReplicationTableStatisticsMessageRequestTypeDef,
    DescribeReplicationTableStatisticsResponseTypeDef,
    DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef,
    DescribeReplicationTaskAssessmentResultsResponseTypeDef,
    DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef,
    DescribeReplicationTaskAssessmentRunsResponseTypeDef,
    DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef,
    DescribeReplicationTaskIndividualAssessmentsResponseTypeDef,
    DescribeReplicationTasksMessageRequestTypeDef,
    DescribeReplicationTasksResponseTypeDef,
    DescribeSchemasMessageRequestTypeDef,
    DescribeSchemasResponseTypeDef,
    DescribeTableStatisticsMessageRequestTypeDef,
    DescribeTableStatisticsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportMetadataModelAssessmentMessageRequestTypeDef,
    ExportMetadataModelAssessmentResponseTypeDef,
    ImportCertificateMessageRequestTypeDef,
    ImportCertificateResponseTypeDef,
    ListTagsForResourceMessageRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ModifyConversionConfigurationMessageRequestTypeDef,
    ModifyConversionConfigurationResponseTypeDef,
    ModifyDataMigrationMessageRequestTypeDef,
    ModifyDataMigrationResponseTypeDef,
    ModifyDataProviderMessageRequestTypeDef,
    ModifyDataProviderResponseTypeDef,
    ModifyEndpointMessageRequestTypeDef,
    ModifyEndpointResponseTypeDef,
    ModifyEventSubscriptionMessageRequestTypeDef,
    ModifyEventSubscriptionResponseTypeDef,
    ModifyInstanceProfileMessageRequestTypeDef,
    ModifyInstanceProfileResponseTypeDef,
    ModifyMigrationProjectMessageRequestTypeDef,
    ModifyMigrationProjectResponseTypeDef,
    ModifyReplicationConfigMessageRequestTypeDef,
    ModifyReplicationConfigResponseTypeDef,
    ModifyReplicationInstanceMessageRequestTypeDef,
    ModifyReplicationInstanceResponseTypeDef,
    ModifyReplicationSubnetGroupMessageRequestTypeDef,
    ModifyReplicationSubnetGroupResponseTypeDef,
    ModifyReplicationTaskMessageRequestTypeDef,
    ModifyReplicationTaskResponseTypeDef,
    MoveReplicationTaskMessageRequestTypeDef,
    MoveReplicationTaskResponseTypeDef,
    RebootReplicationInstanceMessageRequestTypeDef,
    RebootReplicationInstanceResponseTypeDef,
    RefreshSchemasMessageRequestTypeDef,
    RefreshSchemasResponseTypeDef,
    ReloadReplicationTablesMessageRequestTypeDef,
    ReloadReplicationTablesResponseTypeDef,
    ReloadTablesMessageRequestTypeDef,
    ReloadTablesResponseTypeDef,
    RemoveTagsFromResourceMessageRequestTypeDef,
    RunFleetAdvisorLsaAnalysisResponseTypeDef,
    StartDataMigrationMessageRequestTypeDef,
    StartDataMigrationResponseTypeDef,
    StartExtensionPackAssociationMessageRequestTypeDef,
    StartExtensionPackAssociationResponseTypeDef,
    StartMetadataModelAssessmentMessageRequestTypeDef,
    StartMetadataModelAssessmentResponseTypeDef,
    StartMetadataModelConversionMessageRequestTypeDef,
    StartMetadataModelConversionResponseTypeDef,
    StartMetadataModelExportAsScriptMessageRequestTypeDef,
    StartMetadataModelExportAsScriptResponseTypeDef,
    StartMetadataModelExportToTargetMessageRequestTypeDef,
    StartMetadataModelExportToTargetResponseTypeDef,
    StartMetadataModelImportMessageRequestTypeDef,
    StartMetadataModelImportResponseTypeDef,
    StartRecommendationsRequestRequestTypeDef,
    StartReplicationMessageRequestTypeDef,
    StartReplicationResponseTypeDef,
    StartReplicationTaskAssessmentMessageRequestTypeDef,
    StartReplicationTaskAssessmentResponseTypeDef,
    StartReplicationTaskAssessmentRunMessageRequestTypeDef,
    StartReplicationTaskAssessmentRunResponseTypeDef,
    StartReplicationTaskMessageRequestTypeDef,
    StartReplicationTaskResponseTypeDef,
    StopDataMigrationMessageRequestTypeDef,
    StopDataMigrationResponseTypeDef,
    StopReplicationMessageRequestTypeDef,
    StopReplicationResponseTypeDef,
    StopReplicationTaskMessageRequestTypeDef,
    StopReplicationTaskResponseTypeDef,
    TestConnectionMessageRequestTypeDef,
    TestConnectionResponseTypeDef,
    UpdateSubscriptionsToEventBridgeMessageRequestTypeDef,
    UpdateSubscriptionsToEventBridgeResponseTypeDef,
)
from .waiter import (
    EndpointDeletedWaiter,
    ReplicationInstanceAvailableWaiter,
    ReplicationInstanceDeletedWaiter,
    ReplicationTaskDeletedWaiter,
    ReplicationTaskReadyWaiter,
    ReplicationTaskRunningWaiter,
    ReplicationTaskStoppedWaiter,
    TestConnectionSucceedsWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("DatabaseMigrationServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CollectorNotFoundFault: Type[BotocoreClientError]
    FailedDependencyFault: Type[BotocoreClientError]
    InsufficientResourceCapacityFault: Type[BotocoreClientError]
    InvalidCertificateFault: Type[BotocoreClientError]
    InvalidOperationFault: Type[BotocoreClientError]
    InvalidResourceStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    KMSAccessDeniedFault: Type[BotocoreClientError]
    KMSDisabledFault: Type[BotocoreClientError]
    KMSFault: Type[BotocoreClientError]
    KMSInvalidStateFault: Type[BotocoreClientError]
    KMSKeyNotAccessibleFault: Type[BotocoreClientError]
    KMSNotFoundFault: Type[BotocoreClientError]
    KMSThrottlingFault: Type[BotocoreClientError]
    ReplicationSubnetGroupDoesNotCoverEnoughAZs: Type[BotocoreClientError]
    ResourceAlreadyExistsFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    ResourceQuotaExceededFault: Type[BotocoreClientError]
    S3AccessDeniedFault: Type[BotocoreClientError]
    S3ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    StorageQuotaExceededFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    UpgradeDependencyFailureFault: Type[BotocoreClientError]

class DatabaseMigrationServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DatabaseMigrationServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#close)
        """

    def add_tags_to_resource(
        self, **kwargs: Unpack[AddTagsToResourceMessageRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds metadata tags to an DMS resource, including replication instance,
        endpoint, subnet group, and migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/add_tags_to_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#add_tags_to_resource)
        """

    def apply_pending_maintenance_action(
        self, **kwargs: Unpack[ApplyPendingMaintenanceActionMessageRequestTypeDef]
    ) -> ApplyPendingMaintenanceActionResponseTypeDef:
        """
        Applies a pending maintenance action to a resource (for example, to a
        replication instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/apply_pending_maintenance_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#apply_pending_maintenance_action)
        """

    def batch_start_recommendations(
        self, **kwargs: Unpack[BatchStartRecommendationsRequestRequestTypeDef]
    ) -> BatchStartRecommendationsResponseTypeDef:
        """
        Starts the analysis of up to 20 source databases to recommend target engines
        for each source database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/batch_start_recommendations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#batch_start_recommendations)
        """

    def cancel_replication_task_assessment_run(
        self, **kwargs: Unpack[CancelReplicationTaskAssessmentRunMessageRequestTypeDef]
    ) -> CancelReplicationTaskAssessmentRunResponseTypeDef:
        """
        Cancels a single premigration assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/cancel_replication_task_assessment_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#cancel_replication_task_assessment_run)
        """

    def create_data_migration(
        self, **kwargs: Unpack[CreateDataMigrationMessageRequestTypeDef]
    ) -> CreateDataMigrationResponseTypeDef:
        """
        Creates a data migration using the provided settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_data_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_data_migration)
        """

    def create_data_provider(
        self, **kwargs: Unpack[CreateDataProviderMessageRequestTypeDef]
    ) -> CreateDataProviderResponseTypeDef:
        """
        Creates a data provider using the provided settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_data_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_data_provider)
        """

    def create_endpoint(
        self, **kwargs: Unpack[CreateEndpointMessageRequestTypeDef]
    ) -> CreateEndpointResponseTypeDef:
        """
        Creates an endpoint using the provided settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_endpoint)
        """

    def create_event_subscription(
        self, **kwargs: Unpack[CreateEventSubscriptionMessageRequestTypeDef]
    ) -> CreateEventSubscriptionResponseTypeDef:
        """
        Creates an DMS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_event_subscription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_event_subscription)
        """

    def create_fleet_advisor_collector(
        self, **kwargs: Unpack[CreateFleetAdvisorCollectorRequestRequestTypeDef]
    ) -> CreateFleetAdvisorCollectorResponseTypeDef:
        """
        Creates a Fleet Advisor collector using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_fleet_advisor_collector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_fleet_advisor_collector)
        """

    def create_instance_profile(
        self, **kwargs: Unpack[CreateInstanceProfileMessageRequestTypeDef]
    ) -> CreateInstanceProfileResponseTypeDef:
        """
        Creates the instance profile using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_instance_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_instance_profile)
        """

    def create_migration_project(
        self, **kwargs: Unpack[CreateMigrationProjectMessageRequestTypeDef]
    ) -> CreateMigrationProjectResponseTypeDef:
        """
        Creates the migration project using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_migration_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_migration_project)
        """

    def create_replication_config(
        self, **kwargs: Unpack[CreateReplicationConfigMessageRequestTypeDef]
    ) -> CreateReplicationConfigResponseTypeDef:
        """
        Creates a configuration that you can later provide to configure and start an
        DMS Serverless replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_replication_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_config)
        """

    def create_replication_instance(
        self, **kwargs: Unpack[CreateReplicationInstanceMessageRequestTypeDef]
    ) -> CreateReplicationInstanceResponseTypeDef:
        """
        Creates the replication instance using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_replication_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_instance)
        """

    def create_replication_subnet_group(
        self, **kwargs: Unpack[CreateReplicationSubnetGroupMessageRequestTypeDef]
    ) -> CreateReplicationSubnetGroupResponseTypeDef:
        """
        Creates a replication subnet group given a list of the subnet IDs in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_replication_subnet_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_subnet_group)
        """

    def create_replication_task(
        self, **kwargs: Unpack[CreateReplicationTaskMessageRequestTypeDef]
    ) -> CreateReplicationTaskResponseTypeDef:
        """
        Creates a replication task using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/create_replication_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#create_replication_task)
        """

    def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateMessageRequestTypeDef]
    ) -> DeleteCertificateResponseTypeDef:
        """
        Deletes the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_certificate)
        """

    def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionMessageRequestTypeDef]
    ) -> DeleteConnectionResponseTypeDef:
        """
        Deletes the connection between a replication instance and an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_connection)
        """

    def delete_data_migration(
        self, **kwargs: Unpack[DeleteDataMigrationMessageRequestTypeDef]
    ) -> DeleteDataMigrationResponseTypeDef:
        """
        Deletes the specified data migration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_data_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_data_migration)
        """

    def delete_data_provider(
        self, **kwargs: Unpack[DeleteDataProviderMessageRequestTypeDef]
    ) -> DeleteDataProviderResponseTypeDef:
        """
        Deletes the specified data provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_data_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_data_provider)
        """

    def delete_endpoint(
        self, **kwargs: Unpack[DeleteEndpointMessageRequestTypeDef]
    ) -> DeleteEndpointResponseTypeDef:
        """
        Deletes the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_endpoint)
        """

    def delete_event_subscription(
        self, **kwargs: Unpack[DeleteEventSubscriptionMessageRequestTypeDef]
    ) -> DeleteEventSubscriptionResponseTypeDef:
        """
        Deletes an DMS event subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_event_subscription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_event_subscription)
        """

    def delete_fleet_advisor_collector(
        self, **kwargs: Unpack[DeleteCollectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Fleet Advisor collector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_fleet_advisor_collector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_fleet_advisor_collector)
        """

    def delete_fleet_advisor_databases(
        self, **kwargs: Unpack[DeleteFleetAdvisorDatabasesRequestRequestTypeDef]
    ) -> DeleteFleetAdvisorDatabasesResponseTypeDef:
        """
        Deletes the specified Fleet Advisor collector databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_fleet_advisor_databases.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_fleet_advisor_databases)
        """

    def delete_instance_profile(
        self, **kwargs: Unpack[DeleteInstanceProfileMessageRequestTypeDef]
    ) -> DeleteInstanceProfileResponseTypeDef:
        """
        Deletes the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_instance_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_instance_profile)
        """

    def delete_migration_project(
        self, **kwargs: Unpack[DeleteMigrationProjectMessageRequestTypeDef]
    ) -> DeleteMigrationProjectResponseTypeDef:
        """
        Deletes the specified migration project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_migration_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_migration_project)
        """

    def delete_replication_config(
        self, **kwargs: Unpack[DeleteReplicationConfigMessageRequestTypeDef]
    ) -> DeleteReplicationConfigResponseTypeDef:
        """
        Deletes an DMS Serverless replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_replication_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_config)
        """

    def delete_replication_instance(
        self, **kwargs: Unpack[DeleteReplicationInstanceMessageRequestTypeDef]
    ) -> DeleteReplicationInstanceResponseTypeDef:
        """
        Deletes the specified replication instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_replication_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_instance)
        """

    def delete_replication_subnet_group(
        self, **kwargs: Unpack[DeleteReplicationSubnetGroupMessageRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_replication_subnet_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_subnet_group)
        """

    def delete_replication_task(
        self, **kwargs: Unpack[DeleteReplicationTaskMessageRequestTypeDef]
    ) -> DeleteReplicationTaskResponseTypeDef:
        """
        Deletes the specified replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_replication_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_task)
        """

    def delete_replication_task_assessment_run(
        self, **kwargs: Unpack[DeleteReplicationTaskAssessmentRunMessageRequestTypeDef]
    ) -> DeleteReplicationTaskAssessmentRunResponseTypeDef:
        """
        Deletes the record of a single premigration assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/delete_replication_task_assessment_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#delete_replication_task_assessment_run)
        """

    def describe_account_attributes(self) -> DescribeAccountAttributesResponseTypeDef:
        """
        Lists all of the DMS attributes for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_account_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_account_attributes)
        """

    def describe_applicable_individual_assessments(
        self, **kwargs: Unpack[DescribeApplicableIndividualAssessmentsMessageRequestTypeDef]
    ) -> DescribeApplicableIndividualAssessmentsResponseTypeDef:
        """
        Provides a list of individual assessments that you can specify for a new
        premigration assessment run, given one or more parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_applicable_individual_assessments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_applicable_individual_assessments)
        """

    def describe_certificates(
        self, **kwargs: Unpack[DescribeCertificatesMessageRequestTypeDef]
    ) -> DescribeCertificatesResponseTypeDef:
        """
        Provides a description of the certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_certificates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_certificates)
        """

    def describe_connections(
        self, **kwargs: Unpack[DescribeConnectionsMessageRequestTypeDef]
    ) -> DescribeConnectionsResponseTypeDef:
        """
        Describes the status of the connections that have been made between the
        replication instance and an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_connections)
        """

    def describe_conversion_configuration(
        self, **kwargs: Unpack[DescribeConversionConfigurationMessageRequestTypeDef]
    ) -> DescribeConversionConfigurationResponseTypeDef:
        """
        Returns configuration parameters for a schema conversion project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_conversion_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_conversion_configuration)
        """

    def describe_data_migrations(
        self, **kwargs: Unpack[DescribeDataMigrationsMessageRequestTypeDef]
    ) -> DescribeDataMigrationsResponseTypeDef:
        """
        Returns information about data migrations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_data_migrations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_data_migrations)
        """

    def describe_data_providers(
        self, **kwargs: Unpack[DescribeDataProvidersMessageRequestTypeDef]
    ) -> DescribeDataProvidersResponseTypeDef:
        """
        Returns a paginated list of data providers for your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_data_providers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_data_providers)
        """

    def describe_endpoint_settings(
        self, **kwargs: Unpack[DescribeEndpointSettingsMessageRequestTypeDef]
    ) -> DescribeEndpointSettingsResponseTypeDef:
        """
        Returns information about the possible endpoint settings available when you
        create an endpoint for a specific database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_endpoint_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_endpoint_settings)
        """

    def describe_endpoint_types(
        self, **kwargs: Unpack[DescribeEndpointTypesMessageRequestTypeDef]
    ) -> DescribeEndpointTypesResponseTypeDef:
        """
        Returns information about the type of endpoints available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_endpoint_types.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_endpoint_types)
        """

    def describe_endpoints(
        self, **kwargs: Unpack[DescribeEndpointsMessageRequestTypeDef]
    ) -> DescribeEndpointsResponseTypeDef:
        """
        Returns information about the endpoints for your account in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_endpoints)
        """

    def describe_engine_versions(
        self, **kwargs: Unpack[DescribeEngineVersionsMessageRequestTypeDef]
    ) -> DescribeEngineVersionsResponseTypeDef:
        """
        Returns information about the replication instance versions used in the project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_engine_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_engine_versions)
        """

    def describe_event_categories(
        self, **kwargs: Unpack[DescribeEventCategoriesMessageRequestTypeDef]
    ) -> DescribeEventCategoriesResponseTypeDef:
        """
        Lists categories for all event source types, or, if specified, for a specified
        source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_event_categories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_event_categories)
        """

    def describe_event_subscriptions(
        self, **kwargs: Unpack[DescribeEventSubscriptionsMessageRequestTypeDef]
    ) -> DescribeEventSubscriptionsResponseTypeDef:
        """
        Lists all the event subscriptions for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_event_subscriptions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_event_subscriptions)
        """

    def describe_events(
        self, **kwargs: Unpack[DescribeEventsMessageRequestTypeDef]
    ) -> DescribeEventsResponseTypeDef:
        """
        Lists events for a given source identifier and source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_events)
        """

    def describe_extension_pack_associations(
        self, **kwargs: Unpack[DescribeExtensionPackAssociationsMessageRequestTypeDef]
    ) -> DescribeExtensionPackAssociationsResponseTypeDef:
        """
        Returns a paginated list of extension pack associations for the specified
        migration project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_extension_pack_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_extension_pack_associations)
        """

    def describe_fleet_advisor_collectors(
        self, **kwargs: Unpack[DescribeFleetAdvisorCollectorsRequestRequestTypeDef]
    ) -> DescribeFleetAdvisorCollectorsResponseTypeDef:
        """
        Returns a list of the Fleet Advisor collectors in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_fleet_advisor_collectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_collectors)
        """

    def describe_fleet_advisor_databases(
        self, **kwargs: Unpack[DescribeFleetAdvisorDatabasesRequestRequestTypeDef]
    ) -> DescribeFleetAdvisorDatabasesResponseTypeDef:
        """
        Returns a list of Fleet Advisor databases in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_fleet_advisor_databases.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_databases)
        """

    def describe_fleet_advisor_lsa_analysis(
        self, **kwargs: Unpack[DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef]
    ) -> DescribeFleetAdvisorLsaAnalysisResponseTypeDef:
        """
        Provides descriptions of large-scale assessment (LSA) analyses produced by your
        Fleet Advisor collectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_fleet_advisor_lsa_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_lsa_analysis)
        """

    def describe_fleet_advisor_schema_object_summary(
        self, **kwargs: Unpack[DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef]
    ) -> DescribeFleetAdvisorSchemaObjectSummaryResponseTypeDef:
        """
        Provides descriptions of the schemas discovered by your Fleet Advisor
        collectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_fleet_advisor_schema_object_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_schema_object_summary)
        """

    def describe_fleet_advisor_schemas(
        self, **kwargs: Unpack[DescribeFleetAdvisorSchemasRequestRequestTypeDef]
    ) -> DescribeFleetAdvisorSchemasResponseTypeDef:
        """
        Returns a list of schemas detected by Fleet Advisor Collectors in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_fleet_advisor_schemas.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_fleet_advisor_schemas)
        """

    def describe_instance_profiles(
        self, **kwargs: Unpack[DescribeInstanceProfilesMessageRequestTypeDef]
    ) -> DescribeInstanceProfilesResponseTypeDef:
        """
        Returns a paginated list of instance profiles for your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_instance_profiles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_instance_profiles)
        """

    def describe_metadata_model_assessments(
        self, **kwargs: Unpack[DescribeMetadataModelAssessmentsMessageRequestTypeDef]
    ) -> DescribeMetadataModelAssessmentsResponseTypeDef:
        """
        Returns a paginated list of metadata model assessments for your account in the
        current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_metadata_model_assessments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_metadata_model_assessments)
        """

    def describe_metadata_model_conversions(
        self, **kwargs: Unpack[DescribeMetadataModelConversionsMessageRequestTypeDef]
    ) -> DescribeMetadataModelConversionsResponseTypeDef:
        """
        Returns a paginated list of metadata model conversions for a migration project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_metadata_model_conversions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_metadata_model_conversions)
        """

    def describe_metadata_model_exports_as_script(
        self, **kwargs: Unpack[DescribeMetadataModelExportsAsScriptMessageRequestTypeDef]
    ) -> DescribeMetadataModelExportsAsScriptResponseTypeDef:
        """
        Returns a paginated list of metadata model exports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_metadata_model_exports_as_script.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_metadata_model_exports_as_script)
        """

    def describe_metadata_model_exports_to_target(
        self, **kwargs: Unpack[DescribeMetadataModelExportsToTargetMessageRequestTypeDef]
    ) -> DescribeMetadataModelExportsToTargetResponseTypeDef:
        """
        Returns a paginated list of metadata model exports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_metadata_model_exports_to_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_metadata_model_exports_to_target)
        """

    def describe_metadata_model_imports(
        self, **kwargs: Unpack[DescribeMetadataModelImportsMessageRequestTypeDef]
    ) -> DescribeMetadataModelImportsResponseTypeDef:
        """
        Returns a paginated list of metadata model imports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_metadata_model_imports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_metadata_model_imports)
        """

    def describe_migration_projects(
        self, **kwargs: Unpack[DescribeMigrationProjectsMessageRequestTypeDef]
    ) -> DescribeMigrationProjectsResponseTypeDef:
        """
        Returns a paginated list of migration projects for your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_migration_projects.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_migration_projects)
        """

    def describe_orderable_replication_instances(
        self, **kwargs: Unpack[DescribeOrderableReplicationInstancesMessageRequestTypeDef]
    ) -> DescribeOrderableReplicationInstancesResponseTypeDef:
        """
        Returns information about the replication instance types that can be created in
        the specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_orderable_replication_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_orderable_replication_instances)
        """

    def describe_pending_maintenance_actions(
        self, **kwargs: Unpack[DescribePendingMaintenanceActionsMessageRequestTypeDef]
    ) -> DescribePendingMaintenanceActionsResponseTypeDef:
        """
        For internal use only.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_pending_maintenance_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_pending_maintenance_actions)
        """

    def describe_recommendation_limitations(
        self, **kwargs: Unpack[DescribeRecommendationLimitationsRequestRequestTypeDef]
    ) -> DescribeRecommendationLimitationsResponseTypeDef:
        """
        Returns a paginated list of limitations for recommendations of target Amazon
        Web Services engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_recommendation_limitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_recommendation_limitations)
        """

    def describe_recommendations(
        self, **kwargs: Unpack[DescribeRecommendationsRequestRequestTypeDef]
    ) -> DescribeRecommendationsResponseTypeDef:
        """
        Returns a paginated list of target engine recommendations for your source
        databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_recommendations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_recommendations)
        """

    def describe_refresh_schemas_status(
        self, **kwargs: Unpack[DescribeRefreshSchemasStatusMessageRequestTypeDef]
    ) -> DescribeRefreshSchemasStatusResponseTypeDef:
        """
        Returns the status of the RefreshSchemas operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_refresh_schemas_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_refresh_schemas_status)
        """

    def describe_replication_configs(
        self, **kwargs: Unpack[DescribeReplicationConfigsMessageRequestTypeDef]
    ) -> DescribeReplicationConfigsResponseTypeDef:
        """
        Returns one or more existing DMS Serverless replication configurations as a
        list of structures.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_configs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_configs)
        """

    def describe_replication_instance_task_logs(
        self, **kwargs: Unpack[DescribeReplicationInstanceTaskLogsMessageRequestTypeDef]
    ) -> DescribeReplicationInstanceTaskLogsResponseTypeDef:
        """
        Returns information about the task logs for the specified task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_instance_task_logs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_instance_task_logs)
        """

    def describe_replication_instances(
        self, **kwargs: Unpack[DescribeReplicationInstancesMessageRequestTypeDef]
    ) -> DescribeReplicationInstancesResponseTypeDef:
        """
        Returns information about replication instances for your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_instances)
        """

    def describe_replication_subnet_groups(
        self, **kwargs: Unpack[DescribeReplicationSubnetGroupsMessageRequestTypeDef]
    ) -> DescribeReplicationSubnetGroupsResponseTypeDef:
        """
        Returns information about the replication subnet groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_subnet_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_subnet_groups)
        """

    def describe_replication_table_statistics(
        self, **kwargs: Unpack[DescribeReplicationTableStatisticsMessageRequestTypeDef]
    ) -> DescribeReplicationTableStatisticsResponseTypeDef:
        """
        Returns table and schema statistics for one or more provisioned replications
        that use a given DMS Serverless replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_table_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_table_statistics)
        """

    def describe_replication_task_assessment_results(
        self, **kwargs: Unpack[DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef]
    ) -> DescribeReplicationTaskAssessmentResultsResponseTypeDef:
        """
        Returns the task assessment results from the Amazon S3 bucket that DMS creates
        in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_task_assessment_results.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_task_assessment_results)
        """

    def describe_replication_task_assessment_runs(
        self, **kwargs: Unpack[DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef]
    ) -> DescribeReplicationTaskAssessmentRunsResponseTypeDef:
        """
        Returns a paginated list of premigration assessment runs based on filter
        settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_task_assessment_runs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_task_assessment_runs)
        """

    def describe_replication_task_individual_assessments(
        self, **kwargs: Unpack[DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef]
    ) -> DescribeReplicationTaskIndividualAssessmentsResponseTypeDef:
        """
        Returns a paginated list of individual assessments based on filter settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_task_individual_assessments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_task_individual_assessments)
        """

    def describe_replication_tasks(
        self, **kwargs: Unpack[DescribeReplicationTasksMessageRequestTypeDef]
    ) -> DescribeReplicationTasksResponseTypeDef:
        """
        Returns information about replication tasks for your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replication_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replication_tasks)
        """

    def describe_replications(
        self, **kwargs: Unpack[DescribeReplicationsMessageRequestTypeDef]
    ) -> DescribeReplicationsResponseTypeDef:
        """
        Provides details on replication progress by returning status information for
        one or more provisioned DMS Serverless replications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_replications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_replications)
        """

    def describe_schemas(
        self, **kwargs: Unpack[DescribeSchemasMessageRequestTypeDef]
    ) -> DescribeSchemasResponseTypeDef:
        """
        Returns information about the schema for the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_schemas.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_schemas)
        """

    def describe_table_statistics(
        self, **kwargs: Unpack[DescribeTableStatisticsMessageRequestTypeDef]
    ) -> DescribeTableStatisticsResponseTypeDef:
        """
        Returns table statistics on the database migration task, including table name,
        rows inserted, rows updated, and rows deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/describe_table_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#describe_table_statistics)
        """

    def export_metadata_model_assessment(
        self, **kwargs: Unpack[ExportMetadataModelAssessmentMessageRequestTypeDef]
    ) -> ExportMetadataModelAssessmentResponseTypeDef:
        """
        Saves a copy of a database migration assessment report to your Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/export_metadata_model_assessment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#export_metadata_model_assessment)
        """

    def import_certificate(
        self, **kwargs: Unpack[ImportCertificateMessageRequestTypeDef]
    ) -> ImportCertificateResponseTypeDef:
        """
        Uploads the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/import_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#import_certificate)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceMessageRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all metadata tags attached to an DMS resource, including replication
        instance, endpoint, subnet group, and migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#list_tags_for_resource)
        """

    def modify_conversion_configuration(
        self, **kwargs: Unpack[ModifyConversionConfigurationMessageRequestTypeDef]
    ) -> ModifyConversionConfigurationResponseTypeDef:
        """
        Modifies the specified schema conversion configuration using the provided
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_conversion_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_conversion_configuration)
        """

    def modify_data_migration(
        self, **kwargs: Unpack[ModifyDataMigrationMessageRequestTypeDef]
    ) -> ModifyDataMigrationResponseTypeDef:
        """
        Modifies an existing DMS data migration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_data_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_data_migration)
        """

    def modify_data_provider(
        self, **kwargs: Unpack[ModifyDataProviderMessageRequestTypeDef]
    ) -> ModifyDataProviderResponseTypeDef:
        """
        Modifies the specified data provider using the provided settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_data_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_data_provider)
        """

    def modify_endpoint(
        self, **kwargs: Unpack[ModifyEndpointMessageRequestTypeDef]
    ) -> ModifyEndpointResponseTypeDef:
        """
        Modifies the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_endpoint)
        """

    def modify_event_subscription(
        self, **kwargs: Unpack[ModifyEventSubscriptionMessageRequestTypeDef]
    ) -> ModifyEventSubscriptionResponseTypeDef:
        """
        Modifies an existing DMS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_event_subscription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_event_subscription)
        """

    def modify_instance_profile(
        self, **kwargs: Unpack[ModifyInstanceProfileMessageRequestTypeDef]
    ) -> ModifyInstanceProfileResponseTypeDef:
        """
        Modifies the specified instance profile using the provided parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_instance_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_instance_profile)
        """

    def modify_migration_project(
        self, **kwargs: Unpack[ModifyMigrationProjectMessageRequestTypeDef]
    ) -> ModifyMigrationProjectResponseTypeDef:
        """
        Modifies the specified migration project using the provided parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_migration_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_migration_project)
        """

    def modify_replication_config(
        self, **kwargs: Unpack[ModifyReplicationConfigMessageRequestTypeDef]
    ) -> ModifyReplicationConfigResponseTypeDef:
        """
        Modifies an existing DMS Serverless replication configuration that you can use
        to start a replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_replication_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_config)
        """

    def modify_replication_instance(
        self, **kwargs: Unpack[ModifyReplicationInstanceMessageRequestTypeDef]
    ) -> ModifyReplicationInstanceResponseTypeDef:
        """
        Modifies the replication instance to apply new settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_replication_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_instance)
        """

    def modify_replication_subnet_group(
        self, **kwargs: Unpack[ModifyReplicationSubnetGroupMessageRequestTypeDef]
    ) -> ModifyReplicationSubnetGroupResponseTypeDef:
        """
        Modifies the settings for the specified replication subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_replication_subnet_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_subnet_group)
        """

    def modify_replication_task(
        self, **kwargs: Unpack[ModifyReplicationTaskMessageRequestTypeDef]
    ) -> ModifyReplicationTaskResponseTypeDef:
        """
        Modifies the specified replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/modify_replication_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#modify_replication_task)
        """

    def move_replication_task(
        self, **kwargs: Unpack[MoveReplicationTaskMessageRequestTypeDef]
    ) -> MoveReplicationTaskResponseTypeDef:
        """
        Moves a replication task from its current replication instance to a different
        target replication instance using the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/move_replication_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#move_replication_task)
        """

    def reboot_replication_instance(
        self, **kwargs: Unpack[RebootReplicationInstanceMessageRequestTypeDef]
    ) -> RebootReplicationInstanceResponseTypeDef:
        """
        Reboots a replication instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/reboot_replication_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#reboot_replication_instance)
        """

    def refresh_schemas(
        self, **kwargs: Unpack[RefreshSchemasMessageRequestTypeDef]
    ) -> RefreshSchemasResponseTypeDef:
        """
        Populates the schema for the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/refresh_schemas.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#refresh_schemas)
        """

    def reload_replication_tables(
        self, **kwargs: Unpack[ReloadReplicationTablesMessageRequestTypeDef]
    ) -> ReloadReplicationTablesResponseTypeDef:
        """
        Reloads the target database table with the source data for a given DMS
        Serverless replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/reload_replication_tables.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#reload_replication_tables)
        """

    def reload_tables(
        self, **kwargs: Unpack[ReloadTablesMessageRequestTypeDef]
    ) -> ReloadTablesResponseTypeDef:
        """
        Reloads the target database table with the source data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/reload_tables.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#reload_tables)
        """

    def remove_tags_from_resource(
        self, **kwargs: Unpack[RemoveTagsFromResourceMessageRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes metadata tags from an DMS resource, including replication instance,
        endpoint, subnet group, and migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/remove_tags_from_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#remove_tags_from_resource)
        """

    def run_fleet_advisor_lsa_analysis(self) -> RunFleetAdvisorLsaAnalysisResponseTypeDef:
        """
        Runs large-scale assessment (LSA) analysis on every Fleet Advisor collector in
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/run_fleet_advisor_lsa_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#run_fleet_advisor_lsa_analysis)
        """

    def start_data_migration(
        self, **kwargs: Unpack[StartDataMigrationMessageRequestTypeDef]
    ) -> StartDataMigrationResponseTypeDef:
        """
        Starts the specified data migration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_data_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_data_migration)
        """

    def start_extension_pack_association(
        self, **kwargs: Unpack[StartExtensionPackAssociationMessageRequestTypeDef]
    ) -> StartExtensionPackAssociationResponseTypeDef:
        """
        Applies the extension pack to your target database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_extension_pack_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_extension_pack_association)
        """

    def start_metadata_model_assessment(
        self, **kwargs: Unpack[StartMetadataModelAssessmentMessageRequestTypeDef]
    ) -> StartMetadataModelAssessmentResponseTypeDef:
        """
        Creates a database migration assessment report by assessing the migration
        complexity for your source database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_metadata_model_assessment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_metadata_model_assessment)
        """

    def start_metadata_model_conversion(
        self, **kwargs: Unpack[StartMetadataModelConversionMessageRequestTypeDef]
    ) -> StartMetadataModelConversionResponseTypeDef:
        """
        Converts your source database objects to a format compatible with the target
        database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_metadata_model_conversion.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_metadata_model_conversion)
        """

    def start_metadata_model_export_as_script(
        self, **kwargs: Unpack[StartMetadataModelExportAsScriptMessageRequestTypeDef]
    ) -> StartMetadataModelExportAsScriptResponseTypeDef:
        """
        Saves your converted code to a file as a SQL script, and stores this file on
        your Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_metadata_model_export_as_script.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_metadata_model_export_as_script)
        """

    def start_metadata_model_export_to_target(
        self, **kwargs: Unpack[StartMetadataModelExportToTargetMessageRequestTypeDef]
    ) -> StartMetadataModelExportToTargetResponseTypeDef:
        """
        Applies converted database objects to your target database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_metadata_model_export_to_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_metadata_model_export_to_target)
        """

    def start_metadata_model_import(
        self, **kwargs: Unpack[StartMetadataModelImportMessageRequestTypeDef]
    ) -> StartMetadataModelImportResponseTypeDef:
        """
        Loads the metadata for all the dependent database objects of the parent object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_metadata_model_import.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_metadata_model_import)
        """

    def start_recommendations(
        self, **kwargs: Unpack[StartRecommendationsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts the analysis of your source database to provide recommendations of
        target engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_recommendations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_recommendations)
        """

    def start_replication(
        self, **kwargs: Unpack[StartReplicationMessageRequestTypeDef]
    ) -> StartReplicationResponseTypeDef:
        """
        For a given DMS Serverless replication configuration, DMS connects to the
        source endpoint and collects the metadata to analyze the replication workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication)
        """

    def start_replication_task(
        self, **kwargs: Unpack[StartReplicationTaskMessageRequestTypeDef]
    ) -> StartReplicationTaskResponseTypeDef:
        """
        Starts the replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_replication_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication_task)
        """

    def start_replication_task_assessment(
        self, **kwargs: Unpack[StartReplicationTaskAssessmentMessageRequestTypeDef]
    ) -> StartReplicationTaskAssessmentResponseTypeDef:
        """
        Starts the replication task assessment for unsupported data types in the source
        database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_replication_task_assessment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication_task_assessment)
        """

    def start_replication_task_assessment_run(
        self, **kwargs: Unpack[StartReplicationTaskAssessmentRunMessageRequestTypeDef]
    ) -> StartReplicationTaskAssessmentRunResponseTypeDef:
        """
        Starts a new premigration assessment run for one or more individual assessments
        of a migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/start_replication_task_assessment_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#start_replication_task_assessment_run)
        """

    def stop_data_migration(
        self, **kwargs: Unpack[StopDataMigrationMessageRequestTypeDef]
    ) -> StopDataMigrationResponseTypeDef:
        """
        Stops the specified data migration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/stop_data_migration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#stop_data_migration)
        """

    def stop_replication(
        self, **kwargs: Unpack[StopReplicationMessageRequestTypeDef]
    ) -> StopReplicationResponseTypeDef:
        """
        For a given DMS Serverless replication configuration, DMS stops any and all
        ongoing DMS Serverless replications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/stop_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#stop_replication)
        """

    def stop_replication_task(
        self, **kwargs: Unpack[StopReplicationTaskMessageRequestTypeDef]
    ) -> StopReplicationTaskResponseTypeDef:
        """
        Stops the replication task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/stop_replication_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#stop_replication_task)
        """

    def test_connection(
        self, **kwargs: Unpack[TestConnectionMessageRequestTypeDef]
    ) -> TestConnectionResponseTypeDef:
        """
        Tests the connection between the replication instance and the endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/test_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#test_connection)
        """

    def update_subscriptions_to_event_bridge(
        self, **kwargs: Unpack[UpdateSubscriptionsToEventBridgeMessageRequestTypeDef]
    ) -> UpdateSubscriptionsToEventBridgeResponseTypeDef:
        """
        Migrates 10 active and enabled Amazon SNS subscriptions at a time and converts
        them to corresponding Amazon EventBridge rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/update_subscriptions_to_event_bridge.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#update_subscriptions_to_event_bridge)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_certificates"]
    ) -> DescribeCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_connections"]
    ) -> DescribeConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_data_migrations"]
    ) -> DescribeDataMigrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoint_types"]
    ) -> DescribeEndpointTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoints"]
    ) -> DescribeEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_replication_instances"]
    ) -> DescribeOrderableReplicationInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_instances"]
    ) -> DescribeReplicationInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_subnet_groups"]
    ) -> DescribeReplicationSubnetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_task_assessment_results"]
    ) -> DescribeReplicationTaskAssessmentResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_tasks"]
    ) -> DescribeReplicationTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_schemas"]
    ) -> DescribeSchemasPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_table_statistics"]
    ) -> DescribeTableStatisticsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["endpoint_deleted"]) -> EndpointDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_instance_available"]
    ) -> ReplicationInstanceAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_instance_deleted"]
    ) -> ReplicationInstanceDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_deleted"]
    ) -> ReplicationTaskDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_ready"]
    ) -> ReplicationTaskReadyWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_running"]
    ) -> ReplicationTaskRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_task_stopped"]
    ) -> ReplicationTaskStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["test_connection_succeeds"]
    ) -> TestConnectionSucceedsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/client/#get_waiter)
        """
