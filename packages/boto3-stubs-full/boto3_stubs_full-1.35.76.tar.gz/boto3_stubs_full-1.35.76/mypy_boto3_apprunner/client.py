"""
Type annotations for apprunner service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_apprunner.client import AppRunnerClient

    session = Session()
    client: AppRunnerClient = session.client("apprunner")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AssociateCustomDomainRequestRequestTypeDef,
    AssociateCustomDomainResponseTypeDef,
    CreateAutoScalingConfigurationRequestRequestTypeDef,
    CreateAutoScalingConfigurationResponseTypeDef,
    CreateConnectionRequestRequestTypeDef,
    CreateConnectionResponseTypeDef,
    CreateObservabilityConfigurationRequestRequestTypeDef,
    CreateObservabilityConfigurationResponseTypeDef,
    CreateServiceRequestRequestTypeDef,
    CreateServiceResponseTypeDef,
    CreateVpcConnectorRequestRequestTypeDef,
    CreateVpcConnectorResponseTypeDef,
    CreateVpcIngressConnectionRequestRequestTypeDef,
    CreateVpcIngressConnectionResponseTypeDef,
    DeleteAutoScalingConfigurationRequestRequestTypeDef,
    DeleteAutoScalingConfigurationResponseTypeDef,
    DeleteConnectionRequestRequestTypeDef,
    DeleteConnectionResponseTypeDef,
    DeleteObservabilityConfigurationRequestRequestTypeDef,
    DeleteObservabilityConfigurationResponseTypeDef,
    DeleteServiceRequestRequestTypeDef,
    DeleteServiceResponseTypeDef,
    DeleteVpcConnectorRequestRequestTypeDef,
    DeleteVpcConnectorResponseTypeDef,
    DeleteVpcIngressConnectionRequestRequestTypeDef,
    DeleteVpcIngressConnectionResponseTypeDef,
    DescribeAutoScalingConfigurationRequestRequestTypeDef,
    DescribeAutoScalingConfigurationResponseTypeDef,
    DescribeCustomDomainsRequestRequestTypeDef,
    DescribeCustomDomainsResponseTypeDef,
    DescribeObservabilityConfigurationRequestRequestTypeDef,
    DescribeObservabilityConfigurationResponseTypeDef,
    DescribeServiceRequestRequestTypeDef,
    DescribeServiceResponseTypeDef,
    DescribeVpcConnectorRequestRequestTypeDef,
    DescribeVpcConnectorResponseTypeDef,
    DescribeVpcIngressConnectionRequestRequestTypeDef,
    DescribeVpcIngressConnectionResponseTypeDef,
    DisassociateCustomDomainRequestRequestTypeDef,
    DisassociateCustomDomainResponseTypeDef,
    ListAutoScalingConfigurationsRequestRequestTypeDef,
    ListAutoScalingConfigurationsResponseTypeDef,
    ListConnectionsRequestRequestTypeDef,
    ListConnectionsResponseTypeDef,
    ListObservabilityConfigurationsRequestRequestTypeDef,
    ListObservabilityConfigurationsResponseTypeDef,
    ListOperationsRequestRequestTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesForAutoScalingConfigurationRequestRequestTypeDef,
    ListServicesForAutoScalingConfigurationResponseTypeDef,
    ListServicesRequestRequestTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVpcConnectorsRequestRequestTypeDef,
    ListVpcConnectorsResponseTypeDef,
    ListVpcIngressConnectionsRequestRequestTypeDef,
    ListVpcIngressConnectionsResponseTypeDef,
    PauseServiceRequestRequestTypeDef,
    PauseServiceResponseTypeDef,
    ResumeServiceRequestRequestTypeDef,
    ResumeServiceResponseTypeDef,
    StartDeploymentRequestRequestTypeDef,
    StartDeploymentResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDefaultAutoScalingConfigurationRequestRequestTypeDef,
    UpdateDefaultAutoScalingConfigurationResponseTypeDef,
    UpdateServiceRequestRequestTypeDef,
    UpdateServiceResponseTypeDef,
    UpdateVpcIngressConnectionRequestRequestTypeDef,
    UpdateVpcIngressConnectionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("AppRunnerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]


class AppRunnerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppRunnerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#close)
        """

    def associate_custom_domain(
        self, **kwargs: Unpack[AssociateCustomDomainRequestRequestTypeDef]
    ) -> AssociateCustomDomainResponseTypeDef:
        """
        Associate your own domain name with the App Runner subdomain URL of your App
        Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/associate_custom_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#associate_custom_domain)
        """

    def create_auto_scaling_configuration(
        self, **kwargs: Unpack[CreateAutoScalingConfigurationRequestRequestTypeDef]
    ) -> CreateAutoScalingConfigurationResponseTypeDef:
        """
        Create an App Runner automatic scaling configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_auto_scaling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#create_auto_scaling_configuration)
        """

    def create_connection(
        self, **kwargs: Unpack[CreateConnectionRequestRequestTypeDef]
    ) -> CreateConnectionResponseTypeDef:
        """
        Create an App Runner connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#create_connection)
        """

    def create_observability_configuration(
        self, **kwargs: Unpack[CreateObservabilityConfigurationRequestRequestTypeDef]
    ) -> CreateObservabilityConfigurationResponseTypeDef:
        """
        Create an App Runner observability configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_observability_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#create_observability_configuration)
        """

    def create_service(
        self, **kwargs: Unpack[CreateServiceRequestRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Create an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#create_service)
        """

    def create_vpc_connector(
        self, **kwargs: Unpack[CreateVpcConnectorRequestRequestTypeDef]
    ) -> CreateVpcConnectorResponseTypeDef:
        """
        Create an App Runner VPC connector resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_vpc_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#create_vpc_connector)
        """

    def create_vpc_ingress_connection(
        self, **kwargs: Unpack[CreateVpcIngressConnectionRequestRequestTypeDef]
    ) -> CreateVpcIngressConnectionResponseTypeDef:
        """
        Create an App Runner VPC Ingress Connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_vpc_ingress_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#create_vpc_ingress_connection)
        """

    def delete_auto_scaling_configuration(
        self, **kwargs: Unpack[DeleteAutoScalingConfigurationRequestRequestTypeDef]
    ) -> DeleteAutoScalingConfigurationResponseTypeDef:
        """
        Delete an App Runner automatic scaling configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_auto_scaling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#delete_auto_scaling_configuration)
        """

    def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionRequestRequestTypeDef]
    ) -> DeleteConnectionResponseTypeDef:
        """
        Delete an App Runner connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#delete_connection)
        """

    def delete_observability_configuration(
        self, **kwargs: Unpack[DeleteObservabilityConfigurationRequestRequestTypeDef]
    ) -> DeleteObservabilityConfigurationResponseTypeDef:
        """
        Delete an App Runner observability configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_observability_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#delete_observability_configuration)
        """

    def delete_service(
        self, **kwargs: Unpack[DeleteServiceRequestRequestTypeDef]
    ) -> DeleteServiceResponseTypeDef:
        """
        Delete an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#delete_service)
        """

    def delete_vpc_connector(
        self, **kwargs: Unpack[DeleteVpcConnectorRequestRequestTypeDef]
    ) -> DeleteVpcConnectorResponseTypeDef:
        """
        Delete an App Runner VPC connector resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_vpc_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#delete_vpc_connector)
        """

    def delete_vpc_ingress_connection(
        self, **kwargs: Unpack[DeleteVpcIngressConnectionRequestRequestTypeDef]
    ) -> DeleteVpcIngressConnectionResponseTypeDef:
        """
        Delete an App Runner VPC Ingress Connection resource that's associated with an
        App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_vpc_ingress_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#delete_vpc_ingress_connection)
        """

    def describe_auto_scaling_configuration(
        self, **kwargs: Unpack[DescribeAutoScalingConfigurationRequestRequestTypeDef]
    ) -> DescribeAutoScalingConfigurationResponseTypeDef:
        """
        Return a full description of an App Runner automatic scaling configuration
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_auto_scaling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#describe_auto_scaling_configuration)
        """

    def describe_custom_domains(
        self, **kwargs: Unpack[DescribeCustomDomainsRequestRequestTypeDef]
    ) -> DescribeCustomDomainsResponseTypeDef:
        """
        Return a description of custom domain names that are associated with an App
        Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_custom_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#describe_custom_domains)
        """

    def describe_observability_configuration(
        self, **kwargs: Unpack[DescribeObservabilityConfigurationRequestRequestTypeDef]
    ) -> DescribeObservabilityConfigurationResponseTypeDef:
        """
        Return a full description of an App Runner observability configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_observability_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#describe_observability_configuration)
        """

    def describe_service(
        self, **kwargs: Unpack[DescribeServiceRequestRequestTypeDef]
    ) -> DescribeServiceResponseTypeDef:
        """
        Return a full description of an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#describe_service)
        """

    def describe_vpc_connector(
        self, **kwargs: Unpack[DescribeVpcConnectorRequestRequestTypeDef]
    ) -> DescribeVpcConnectorResponseTypeDef:
        """
        Return a description of an App Runner VPC connector resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_vpc_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#describe_vpc_connector)
        """

    def describe_vpc_ingress_connection(
        self, **kwargs: Unpack[DescribeVpcIngressConnectionRequestRequestTypeDef]
    ) -> DescribeVpcIngressConnectionResponseTypeDef:
        """
        Return a full description of an App Runner VPC Ingress Connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_vpc_ingress_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#describe_vpc_ingress_connection)
        """

    def disassociate_custom_domain(
        self, **kwargs: Unpack[DisassociateCustomDomainRequestRequestTypeDef]
    ) -> DisassociateCustomDomainResponseTypeDef:
        """
        Disassociate a custom domain name from an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/disassociate_custom_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#disassociate_custom_domain)
        """

    def list_auto_scaling_configurations(
        self, **kwargs: Unpack[ListAutoScalingConfigurationsRequestRequestTypeDef]
    ) -> ListAutoScalingConfigurationsResponseTypeDef:
        """
        Returns a list of active App Runner automatic scaling configurations in your
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_auto_scaling_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_auto_scaling_configurations)
        """

    def list_connections(
        self, **kwargs: Unpack[ListConnectionsRequestRequestTypeDef]
    ) -> ListConnectionsResponseTypeDef:
        """
        Returns a list of App Runner connections that are associated with your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_connections)
        """

    def list_observability_configurations(
        self, **kwargs: Unpack[ListObservabilityConfigurationsRequestRequestTypeDef]
    ) -> ListObservabilityConfigurationsResponseTypeDef:
        """
        Returns a list of active App Runner observability configurations in your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_observability_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_observability_configurations)
        """

    def list_operations(
        self, **kwargs: Unpack[ListOperationsRequestRequestTypeDef]
    ) -> ListOperationsResponseTypeDef:
        """
        Return a list of operations that occurred on an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_operations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_operations)
        """

    def list_services(
        self, **kwargs: Unpack[ListServicesRequestRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Returns a list of running App Runner services in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_services.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_services)
        """

    def list_services_for_auto_scaling_configuration(
        self, **kwargs: Unpack[ListServicesForAutoScalingConfigurationRequestRequestTypeDef]
    ) -> ListServicesForAutoScalingConfigurationResponseTypeDef:
        """
        Returns a list of the associated App Runner services using an auto scaling
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_services_for_auto_scaling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_services_for_auto_scaling_configuration)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags that are associated with for an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_tags_for_resource)
        """

    def list_vpc_connectors(
        self, **kwargs: Unpack[ListVpcConnectorsRequestRequestTypeDef]
    ) -> ListVpcConnectorsResponseTypeDef:
        """
        Returns a list of App Runner VPC connectors in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_vpc_connectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_vpc_connectors)
        """

    def list_vpc_ingress_connections(
        self, **kwargs: Unpack[ListVpcIngressConnectionsRequestRequestTypeDef]
    ) -> ListVpcIngressConnectionsResponseTypeDef:
        """
        Return a list of App Runner VPC Ingress Connections in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_vpc_ingress_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#list_vpc_ingress_connections)
        """

    def pause_service(
        self, **kwargs: Unpack[PauseServiceRequestRequestTypeDef]
    ) -> PauseServiceResponseTypeDef:
        """
        Pause an active App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/pause_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#pause_service)
        """

    def resume_service(
        self, **kwargs: Unpack[ResumeServiceRequestRequestTypeDef]
    ) -> ResumeServiceResponseTypeDef:
        """
        Resume an active App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/resume_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#resume_service)
        """

    def start_deployment(
        self, **kwargs: Unpack[StartDeploymentRequestRequestTypeDef]
    ) -> StartDeploymentResponseTypeDef:
        """
        Initiate a manual deployment of the latest commit in a source code repository
        or the latest image in a source image repository to an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/start_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#start_deployment)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Add tags to, or update the tag values of, an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove tags from an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#untag_resource)
        """

    def update_default_auto_scaling_configuration(
        self, **kwargs: Unpack[UpdateDefaultAutoScalingConfigurationRequestRequestTypeDef]
    ) -> UpdateDefaultAutoScalingConfigurationResponseTypeDef:
        """
        Update an auto scaling configuration to be the default.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/update_default_auto_scaling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#update_default_auto_scaling_configuration)
        """

    def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Update an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/update_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#update_service)
        """

    def update_vpc_ingress_connection(
        self, **kwargs: Unpack[UpdateVpcIngressConnectionRequestRequestTypeDef]
    ) -> UpdateVpcIngressConnectionResponseTypeDef:
        """
        Update an existing App Runner VPC Ingress Connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/update_vpc_ingress_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/client/#update_vpc_ingress_connection)
        """
