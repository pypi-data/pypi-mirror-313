"""
Type annotations for ecs service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ecs.client import ECSClient

    session = Session()
    client: ECSClient = session.client("ecs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAccountSettingsPaginator,
    ListAttributesPaginator,
    ListClustersPaginator,
    ListContainerInstancesPaginator,
    ListServicesByNamespacePaginator,
    ListServicesPaginator,
    ListTaskDefinitionFamiliesPaginator,
    ListTaskDefinitionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    CreateCapacityProviderRequestRequestTypeDef,
    CreateCapacityProviderResponseTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateServiceRequestRequestTypeDef,
    CreateServiceResponseTypeDef,
    CreateTaskSetRequestRequestTypeDef,
    CreateTaskSetResponseTypeDef,
    DeleteAccountSettingRequestRequestTypeDef,
    DeleteAccountSettingResponseTypeDef,
    DeleteAttributesRequestRequestTypeDef,
    DeleteAttributesResponseTypeDef,
    DeleteCapacityProviderRequestRequestTypeDef,
    DeleteCapacityProviderResponseTypeDef,
    DeleteClusterRequestRequestTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteServiceRequestRequestTypeDef,
    DeleteServiceResponseTypeDef,
    DeleteTaskDefinitionsRequestRequestTypeDef,
    DeleteTaskDefinitionsResponseTypeDef,
    DeleteTaskSetRequestRequestTypeDef,
    DeleteTaskSetResponseTypeDef,
    DeregisterContainerInstanceRequestRequestTypeDef,
    DeregisterContainerInstanceResponseTypeDef,
    DeregisterTaskDefinitionRequestRequestTypeDef,
    DeregisterTaskDefinitionResponseTypeDef,
    DescribeCapacityProvidersRequestRequestTypeDef,
    DescribeCapacityProvidersResponseTypeDef,
    DescribeClustersRequestRequestTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeContainerInstancesRequestRequestTypeDef,
    DescribeContainerInstancesResponseTypeDef,
    DescribeServiceDeploymentsRequestRequestTypeDef,
    DescribeServiceDeploymentsResponseTypeDef,
    DescribeServiceRevisionsRequestRequestTypeDef,
    DescribeServiceRevisionsResponseTypeDef,
    DescribeServicesRequestRequestTypeDef,
    DescribeServicesResponseTypeDef,
    DescribeTaskDefinitionRequestRequestTypeDef,
    DescribeTaskDefinitionResponseTypeDef,
    DescribeTaskSetsRequestRequestTypeDef,
    DescribeTaskSetsResponseTypeDef,
    DescribeTasksRequestRequestTypeDef,
    DescribeTasksResponseTypeDef,
    DiscoverPollEndpointRequestRequestTypeDef,
    DiscoverPollEndpointResponseTypeDef,
    ExecuteCommandRequestRequestTypeDef,
    ExecuteCommandResponseTypeDef,
    GetTaskProtectionRequestRequestTypeDef,
    GetTaskProtectionResponseTypeDef,
    ListAccountSettingsRequestRequestTypeDef,
    ListAccountSettingsResponseTypeDef,
    ListAttributesRequestRequestTypeDef,
    ListAttributesResponseTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResponseTypeDef,
    ListContainerInstancesRequestRequestTypeDef,
    ListContainerInstancesResponseTypeDef,
    ListServiceDeploymentsRequestRequestTypeDef,
    ListServiceDeploymentsResponseTypeDef,
    ListServicesByNamespaceRequestRequestTypeDef,
    ListServicesByNamespaceResponseTypeDef,
    ListServicesRequestRequestTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskDefinitionFamiliesRequestRequestTypeDef,
    ListTaskDefinitionFamiliesResponseTypeDef,
    ListTaskDefinitionsRequestRequestTypeDef,
    ListTaskDefinitionsResponseTypeDef,
    ListTasksRequestRequestTypeDef,
    ListTasksResponseTypeDef,
    PutAccountSettingDefaultRequestRequestTypeDef,
    PutAccountSettingDefaultResponseTypeDef,
    PutAccountSettingRequestRequestTypeDef,
    PutAccountSettingResponseTypeDef,
    PutAttributesRequestRequestTypeDef,
    PutAttributesResponseTypeDef,
    PutClusterCapacityProvidersRequestRequestTypeDef,
    PutClusterCapacityProvidersResponseTypeDef,
    RegisterContainerInstanceRequestRequestTypeDef,
    RegisterContainerInstanceResponseTypeDef,
    RegisterTaskDefinitionRequestRequestTypeDef,
    RegisterTaskDefinitionResponseTypeDef,
    RunTaskRequestRequestTypeDef,
    RunTaskResponseTypeDef,
    StartTaskRequestRequestTypeDef,
    StartTaskResponseTypeDef,
    StopTaskRequestRequestTypeDef,
    StopTaskResponseTypeDef,
    SubmitAttachmentStateChangesRequestRequestTypeDef,
    SubmitAttachmentStateChangesResponseTypeDef,
    SubmitContainerStateChangeRequestRequestTypeDef,
    SubmitContainerStateChangeResponseTypeDef,
    SubmitTaskStateChangeRequestRequestTypeDef,
    SubmitTaskStateChangeResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCapacityProviderRequestRequestTypeDef,
    UpdateCapacityProviderResponseTypeDef,
    UpdateClusterRequestRequestTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateClusterSettingsRequestRequestTypeDef,
    UpdateClusterSettingsResponseTypeDef,
    UpdateContainerAgentRequestRequestTypeDef,
    UpdateContainerAgentResponseTypeDef,
    UpdateContainerInstancesStateRequestRequestTypeDef,
    UpdateContainerInstancesStateResponseTypeDef,
    UpdateServicePrimaryTaskSetRequestRequestTypeDef,
    UpdateServicePrimaryTaskSetResponseTypeDef,
    UpdateServiceRequestRequestTypeDef,
    UpdateServiceResponseTypeDef,
    UpdateTaskProtectionRequestRequestTypeDef,
    UpdateTaskProtectionResponseTypeDef,
    UpdateTaskSetRequestRequestTypeDef,
    UpdateTaskSetResponseTypeDef,
)
from .waiter import (
    ServicesInactiveWaiter,
    ServicesStableWaiter,
    TasksRunningWaiter,
    TasksStoppedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ECSClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AttributeLimitExceededException: Type[BotocoreClientError]
    BlockedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ClusterContainsContainerInstancesException: Type[BotocoreClientError]
    ClusterContainsServicesException: Type[BotocoreClientError]
    ClusterContainsTasksException: Type[BotocoreClientError]
    ClusterNotFoundException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingVersionException: Type[BotocoreClientError]
    NamespaceNotFoundException: Type[BotocoreClientError]
    NoUpdateAvailableException: Type[BotocoreClientError]
    PlatformTaskDefinitionIncompatibilityException: Type[BotocoreClientError]
    PlatformUnknownException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]
    ServiceNotActiveException: Type[BotocoreClientError]
    ServiceNotFoundException: Type[BotocoreClientError]
    TargetNotConnectedException: Type[BotocoreClientError]
    TargetNotFoundException: Type[BotocoreClientError]
    TaskSetNotFoundException: Type[BotocoreClientError]
    UnsupportedFeatureException: Type[BotocoreClientError]
    UpdateInProgressException: Type[BotocoreClientError]


class ECSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ECSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#close)
        """

    def create_capacity_provider(
        self, **kwargs: Unpack[CreateCapacityProviderRequestRequestTypeDef]
    ) -> CreateCapacityProviderResponseTypeDef:
        """
        Creates a new capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_capacity_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#create_capacity_provider)
        """

    def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a new Amazon ECS cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#create_cluster)
        """

    def create_service(
        self, **kwargs: Unpack[CreateServiceRequestRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Runs and maintains your desired number of tasks from a specified task
        definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#create_service)
        """

    def create_task_set(
        self, **kwargs: Unpack[CreateTaskSetRequestRequestTypeDef]
    ) -> CreateTaskSetResponseTypeDef:
        """
        Create a task set in the specified cluster and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_task_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#create_task_set)
        """

    def delete_account_setting(
        self, **kwargs: Unpack[DeleteAccountSettingRequestRequestTypeDef]
    ) -> DeleteAccountSettingResponseTypeDef:
        """
        Disables an account setting for a specified user, role, or the root user for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_account_setting.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#delete_account_setting)
        """

    def delete_attributes(
        self, **kwargs: Unpack[DeleteAttributesRequestRequestTypeDef]
    ) -> DeleteAttributesResponseTypeDef:
        """
        Deletes one or more custom attributes from an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#delete_attributes)
        """

    def delete_capacity_provider(
        self, **kwargs: Unpack[DeleteCapacityProviderRequestRequestTypeDef]
    ) -> DeleteCapacityProviderResponseTypeDef:
        """
        Deletes the specified capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_capacity_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#delete_capacity_provider)
        """

    def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestRequestTypeDef]
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#delete_cluster)
        """

    def delete_service(
        self, **kwargs: Unpack[DeleteServiceRequestRequestTypeDef]
    ) -> DeleteServiceResponseTypeDef:
        """
        Deletes a specified service within a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#delete_service)
        """

    def delete_task_definitions(
        self, **kwargs: Unpack[DeleteTaskDefinitionsRequestRequestTypeDef]
    ) -> DeleteTaskDefinitionsResponseTypeDef:
        """
        Deletes one or more task definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_task_definitions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#delete_task_definitions)
        """

    def delete_task_set(
        self, **kwargs: Unpack[DeleteTaskSetRequestRequestTypeDef]
    ) -> DeleteTaskSetResponseTypeDef:
        """
        Deletes a specified task set within a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_task_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#delete_task_set)
        """

    def deregister_container_instance(
        self, **kwargs: Unpack[DeregisterContainerInstanceRequestRequestTypeDef]
    ) -> DeregisterContainerInstanceResponseTypeDef:
        """
        Deregisters an Amazon ECS container instance from the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/deregister_container_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#deregister_container_instance)
        """

    def deregister_task_definition(
        self, **kwargs: Unpack[DeregisterTaskDefinitionRequestRequestTypeDef]
    ) -> DeregisterTaskDefinitionResponseTypeDef:
        """
        Deregisters the specified task definition by family and revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/deregister_task_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#deregister_task_definition)
        """

    def describe_capacity_providers(
        self, **kwargs: Unpack[DescribeCapacityProvidersRequestRequestTypeDef]
    ) -> DescribeCapacityProvidersResponseTypeDef:
        """
        Describes one or more of your capacity providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_capacity_providers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_capacity_providers)
        """

    def describe_clusters(
        self, **kwargs: Unpack[DescribeClustersRequestRequestTypeDef]
    ) -> DescribeClustersResponseTypeDef:
        """
        Describes one or more of your clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_clusters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_clusters)
        """

    def describe_container_instances(
        self, **kwargs: Unpack[DescribeContainerInstancesRequestRequestTypeDef]
    ) -> DescribeContainerInstancesResponseTypeDef:
        """
        Describes one or more container instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_container_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_container_instances)
        """

    def describe_service_deployments(
        self, **kwargs: Unpack[DescribeServiceDeploymentsRequestRequestTypeDef]
    ) -> DescribeServiceDeploymentsResponseTypeDef:
        """
        Describes one or more of your service deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_service_deployments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_service_deployments)
        """

    def describe_service_revisions(
        self, **kwargs: Unpack[DescribeServiceRevisionsRequestRequestTypeDef]
    ) -> DescribeServiceRevisionsResponseTypeDef:
        """
        Describes one or more service revisions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_service_revisions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_service_revisions)
        """

    def describe_services(
        self, **kwargs: Unpack[DescribeServicesRequestRequestTypeDef]
    ) -> DescribeServicesResponseTypeDef:
        """
        Describes the specified services running in your cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_services.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_services)
        """

    def describe_task_definition(
        self, **kwargs: Unpack[DescribeTaskDefinitionRequestRequestTypeDef]
    ) -> DescribeTaskDefinitionResponseTypeDef:
        """
        Describes a task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_task_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_task_definition)
        """

    def describe_task_sets(
        self, **kwargs: Unpack[DescribeTaskSetsRequestRequestTypeDef]
    ) -> DescribeTaskSetsResponseTypeDef:
        """
        Describes the task sets in the specified cluster and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_task_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_task_sets)
        """

    def describe_tasks(
        self, **kwargs: Unpack[DescribeTasksRequestRequestTypeDef]
    ) -> DescribeTasksResponseTypeDef:
        """
        Describes a specified task or tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#describe_tasks)
        """

    def discover_poll_endpoint(
        self, **kwargs: Unpack[DiscoverPollEndpointRequestRequestTypeDef]
    ) -> DiscoverPollEndpointResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/discover_poll_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#discover_poll_endpoint)
        """

    def execute_command(
        self, **kwargs: Unpack[ExecuteCommandRequestRequestTypeDef]
    ) -> ExecuteCommandResponseTypeDef:
        """
        Runs a command remotely on a container within a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/execute_command.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#execute_command)
        """

    def get_task_protection(
        self, **kwargs: Unpack[GetTaskProtectionRequestRequestTypeDef]
    ) -> GetTaskProtectionResponseTypeDef:
        """
        Retrieves the protection status of tasks in an Amazon ECS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_task_protection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_task_protection)
        """

    def list_account_settings(
        self, **kwargs: Unpack[ListAccountSettingsRequestRequestTypeDef]
    ) -> ListAccountSettingsResponseTypeDef:
        """
        Lists the account settings for a specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_account_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_account_settings)
        """

    def list_attributes(
        self, **kwargs: Unpack[ListAttributesRequestRequestTypeDef]
    ) -> ListAttributesResponseTypeDef:
        """
        Lists the attributes for Amazon ECS resources within a specified target type
        and cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_attributes)
        """

    def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of existing clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_clusters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_clusters)
        """

    def list_container_instances(
        self, **kwargs: Unpack[ListContainerInstancesRequestRequestTypeDef]
    ) -> ListContainerInstancesResponseTypeDef:
        """
        Returns a list of container instances in a specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_container_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_container_instances)
        """

    def list_service_deployments(
        self, **kwargs: Unpack[ListServiceDeploymentsRequestRequestTypeDef]
    ) -> ListServiceDeploymentsResponseTypeDef:
        """
        This operation lists all the service deployments that meet the specified filter
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_service_deployments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_service_deployments)
        """

    def list_services(
        self, **kwargs: Unpack[ListServicesRequestRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Returns a list of services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_services.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_services)
        """

    def list_services_by_namespace(
        self, **kwargs: Unpack[ListServicesByNamespaceRequestRequestTypeDef]
    ) -> ListServicesByNamespaceResponseTypeDef:
        """
        This operation lists all of the services that are associated with a Cloud Map
        namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_services_by_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_services_by_namespace)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_tags_for_resource)
        """

    def list_task_definition_families(
        self, **kwargs: Unpack[ListTaskDefinitionFamiliesRequestRequestTypeDef]
    ) -> ListTaskDefinitionFamiliesResponseTypeDef:
        """
        Returns a list of task definition families that are registered to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_task_definition_families.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_task_definition_families)
        """

    def list_task_definitions(
        self, **kwargs: Unpack[ListTaskDefinitionsRequestRequestTypeDef]
    ) -> ListTaskDefinitionsResponseTypeDef:
        """
        Returns a list of task definitions that are registered to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_task_definitions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_task_definitions)
        """

    def list_tasks(
        self, **kwargs: Unpack[ListTasksRequestRequestTypeDef]
    ) -> ListTasksResponseTypeDef:
        """
        Returns a list of tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#list_tasks)
        """

    def put_account_setting(
        self, **kwargs: Unpack[PutAccountSettingRequestRequestTypeDef]
    ) -> PutAccountSettingResponseTypeDef:
        """
        Modifies an account setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_account_setting.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#put_account_setting)
        """

    def put_account_setting_default(
        self, **kwargs: Unpack[PutAccountSettingDefaultRequestRequestTypeDef]
    ) -> PutAccountSettingDefaultResponseTypeDef:
        """
        Modifies an account setting for all users on an account for whom no individual
        account setting has been specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_account_setting_default.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#put_account_setting_default)
        """

    def put_attributes(
        self, **kwargs: Unpack[PutAttributesRequestRequestTypeDef]
    ) -> PutAttributesResponseTypeDef:
        """
        Create or update an attribute on an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#put_attributes)
        """

    def put_cluster_capacity_providers(
        self, **kwargs: Unpack[PutClusterCapacityProvidersRequestRequestTypeDef]
    ) -> PutClusterCapacityProvidersResponseTypeDef:
        """
        Modifies the available capacity providers and the default capacity provider
        strategy for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_cluster_capacity_providers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#put_cluster_capacity_providers)
        """

    def register_container_instance(
        self, **kwargs: Unpack[RegisterContainerInstanceRequestRequestTypeDef]
    ) -> RegisterContainerInstanceResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/register_container_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#register_container_instance)
        """

    def register_task_definition(
        self, **kwargs: Unpack[RegisterTaskDefinitionRequestRequestTypeDef]
    ) -> RegisterTaskDefinitionResponseTypeDef:
        """
        Registers a new task definition from the supplied <code>family</code> and
        <code>containerDefinitions</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/register_task_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#register_task_definition)
        """

    def run_task(self, **kwargs: Unpack[RunTaskRequestRequestTypeDef]) -> RunTaskResponseTypeDef:
        """
        Starts a new task using the specified task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/run_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#run_task)
        """

    def start_task(
        self, **kwargs: Unpack[StartTaskRequestRequestTypeDef]
    ) -> StartTaskResponseTypeDef:
        """
        Starts a new task from the specified task definition on the specified container
        instance or instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/start_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#start_task)
        """

    def stop_task(self, **kwargs: Unpack[StopTaskRequestRequestTypeDef]) -> StopTaskResponseTypeDef:
        """
        Stops a running task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/stop_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#stop_task)
        """

    def submit_attachment_state_changes(
        self, **kwargs: Unpack[SubmitAttachmentStateChangesRequestRequestTypeDef]
    ) -> SubmitAttachmentStateChangesResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/submit_attachment_state_changes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#submit_attachment_state_changes)
        """

    def submit_container_state_change(
        self, **kwargs: Unpack[SubmitContainerStateChangeRequestRequestTypeDef]
    ) -> SubmitContainerStateChangeResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/submit_container_state_change.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#submit_container_state_change)
        """

    def submit_task_state_change(
        self, **kwargs: Unpack[SubmitTaskStateChangeRequestRequestTypeDef]
    ) -> SubmitTaskStateChangeResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/submit_task_state_change.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#submit_task_state_change)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#untag_resource)
        """

    def update_capacity_provider(
        self, **kwargs: Unpack[UpdateCapacityProviderRequestRequestTypeDef]
    ) -> UpdateCapacityProviderResponseTypeDef:
        """
        Modifies the parameters for a capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_capacity_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_capacity_provider)
        """

    def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestRequestTypeDef]
    ) -> UpdateClusterResponseTypeDef:
        """
        Updates the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_cluster)
        """

    def update_cluster_settings(
        self, **kwargs: Unpack[UpdateClusterSettingsRequestRequestTypeDef]
    ) -> UpdateClusterSettingsResponseTypeDef:
        """
        Modifies the settings to use for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_cluster_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_cluster_settings)
        """

    def update_container_agent(
        self, **kwargs: Unpack[UpdateContainerAgentRequestRequestTypeDef]
    ) -> UpdateContainerAgentResponseTypeDef:
        """
        Updates the Amazon ECS container agent on a specified container instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_container_agent.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_container_agent)
        """

    def update_container_instances_state(
        self, **kwargs: Unpack[UpdateContainerInstancesStateRequestRequestTypeDef]
    ) -> UpdateContainerInstancesStateResponseTypeDef:
        """
        Modifies the status of an Amazon ECS container instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_container_instances_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_container_instances_state)
        """

    def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Modifies the parameters of a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_service)
        """

    def update_service_primary_task_set(
        self, **kwargs: Unpack[UpdateServicePrimaryTaskSetRequestRequestTypeDef]
    ) -> UpdateServicePrimaryTaskSetResponseTypeDef:
        """
        Modifies which task set in a service is the primary task set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_service_primary_task_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_service_primary_task_set)
        """

    def update_task_protection(
        self, **kwargs: Unpack[UpdateTaskProtectionRequestRequestTypeDef]
    ) -> UpdateTaskProtectionResponseTypeDef:
        """
        Updates the protection status of a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_task_protection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_task_protection)
        """

    def update_task_set(
        self, **kwargs: Unpack[UpdateTaskSetRequestRequestTypeDef]
    ) -> UpdateTaskSetResponseTypeDef:
        """
        Modifies a task set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_task_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#update_task_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_settings"]
    ) -> ListAccountSettingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_attributes"]) -> ListAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_container_instances"]
    ) -> ListContainerInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_services_by_namespace"]
    ) -> ListServicesByNamespacePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_task_definition_families"]
    ) -> ListTaskDefinitionFamiliesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_task_definitions"]
    ) -> ListTaskDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["services_inactive"]) -> ServicesInactiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["services_stable"]) -> ServicesStableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["tasks_running"]) -> TasksRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["tasks_stopped"]) -> TasksStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/client/#get_waiter)
        """
