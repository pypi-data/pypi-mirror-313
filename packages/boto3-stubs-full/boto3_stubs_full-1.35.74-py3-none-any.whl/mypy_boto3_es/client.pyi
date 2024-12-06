"""
Type annotations for es service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_es.client import ElasticsearchServiceClient

    session = Session()
    client: ElasticsearchServiceClient = session.client("es")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeReservedElasticsearchInstanceOfferingsPaginator,
    DescribeReservedElasticsearchInstancesPaginator,
    GetUpgradeHistoryPaginator,
    ListElasticsearchInstanceTypesPaginator,
    ListElasticsearchVersionsPaginator,
)
from .type_defs import (
    AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef,
    AcceptInboundCrossClusterSearchConnectionResponseTypeDef,
    AddTagsRequestRequestTypeDef,
    AssociatePackageRequestRequestTypeDef,
    AssociatePackageResponseTypeDef,
    AuthorizeVpcEndpointAccessRequestRequestTypeDef,
    AuthorizeVpcEndpointAccessResponseTypeDef,
    CancelDomainConfigChangeRequestRequestTypeDef,
    CancelDomainConfigChangeResponseTypeDef,
    CancelElasticsearchServiceSoftwareUpdateRequestRequestTypeDef,
    CancelElasticsearchServiceSoftwareUpdateResponseTypeDef,
    CreateElasticsearchDomainRequestRequestTypeDef,
    CreateElasticsearchDomainResponseTypeDef,
    CreateOutboundCrossClusterSearchConnectionRequestRequestTypeDef,
    CreateOutboundCrossClusterSearchConnectionResponseTypeDef,
    CreatePackageRequestRequestTypeDef,
    CreatePackageResponseTypeDef,
    CreateVpcEndpointRequestRequestTypeDef,
    CreateVpcEndpointResponseTypeDef,
    DeleteElasticsearchDomainRequestRequestTypeDef,
    DeleteElasticsearchDomainResponseTypeDef,
    DeleteInboundCrossClusterSearchConnectionRequestRequestTypeDef,
    DeleteInboundCrossClusterSearchConnectionResponseTypeDef,
    DeleteOutboundCrossClusterSearchConnectionRequestRequestTypeDef,
    DeleteOutboundCrossClusterSearchConnectionResponseTypeDef,
    DeletePackageRequestRequestTypeDef,
    DeletePackageResponseTypeDef,
    DeleteVpcEndpointRequestRequestTypeDef,
    DeleteVpcEndpointResponseTypeDef,
    DescribeDomainAutoTunesRequestRequestTypeDef,
    DescribeDomainAutoTunesResponseTypeDef,
    DescribeDomainChangeProgressRequestRequestTypeDef,
    DescribeDomainChangeProgressResponseTypeDef,
    DescribeElasticsearchDomainConfigRequestRequestTypeDef,
    DescribeElasticsearchDomainConfigResponseTypeDef,
    DescribeElasticsearchDomainRequestRequestTypeDef,
    DescribeElasticsearchDomainResponseTypeDef,
    DescribeElasticsearchDomainsRequestRequestTypeDef,
    DescribeElasticsearchDomainsResponseTypeDef,
    DescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef,
    DescribeElasticsearchInstanceTypeLimitsResponseTypeDef,
    DescribeInboundCrossClusterSearchConnectionsRequestRequestTypeDef,
    DescribeInboundCrossClusterSearchConnectionsResponseTypeDef,
    DescribeOutboundCrossClusterSearchConnectionsRequestRequestTypeDef,
    DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef,
    DescribePackagesRequestRequestTypeDef,
    DescribePackagesResponseTypeDef,
    DescribeReservedElasticsearchInstanceOfferingsRequestRequestTypeDef,
    DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef,
    DescribeReservedElasticsearchInstancesRequestRequestTypeDef,
    DescribeReservedElasticsearchInstancesResponseTypeDef,
    DescribeVpcEndpointsRequestRequestTypeDef,
    DescribeVpcEndpointsResponseTypeDef,
    DissociatePackageRequestRequestTypeDef,
    DissociatePackageResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCompatibleElasticsearchVersionsRequestRequestTypeDef,
    GetCompatibleElasticsearchVersionsResponseTypeDef,
    GetPackageVersionHistoryRequestRequestTypeDef,
    GetPackageVersionHistoryResponseTypeDef,
    GetUpgradeHistoryRequestRequestTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    GetUpgradeStatusRequestRequestTypeDef,
    GetUpgradeStatusResponseTypeDef,
    ListDomainNamesRequestRequestTypeDef,
    ListDomainNamesResponseTypeDef,
    ListDomainsForPackageRequestRequestTypeDef,
    ListDomainsForPackageResponseTypeDef,
    ListElasticsearchInstanceTypesRequestRequestTypeDef,
    ListElasticsearchInstanceTypesResponseTypeDef,
    ListElasticsearchVersionsRequestRequestTypeDef,
    ListElasticsearchVersionsResponseTypeDef,
    ListPackagesForDomainRequestRequestTypeDef,
    ListPackagesForDomainResponseTypeDef,
    ListTagsRequestRequestTypeDef,
    ListTagsResponseTypeDef,
    ListVpcEndpointAccessRequestRequestTypeDef,
    ListVpcEndpointAccessResponseTypeDef,
    ListVpcEndpointsForDomainRequestRequestTypeDef,
    ListVpcEndpointsForDomainResponseTypeDef,
    ListVpcEndpointsRequestRequestTypeDef,
    ListVpcEndpointsResponseTypeDef,
    PurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef,
    PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef,
    RejectInboundCrossClusterSearchConnectionRequestRequestTypeDef,
    RejectInboundCrossClusterSearchConnectionResponseTypeDef,
    RemoveTagsRequestRequestTypeDef,
    RevokeVpcEndpointAccessRequestRequestTypeDef,
    StartElasticsearchServiceSoftwareUpdateRequestRequestTypeDef,
    StartElasticsearchServiceSoftwareUpdateResponseTypeDef,
    UpdateElasticsearchDomainConfigRequestRequestTypeDef,
    UpdateElasticsearchDomainConfigResponseTypeDef,
    UpdatePackageRequestRequestTypeDef,
    UpdatePackageResponseTypeDef,
    UpdateVpcEndpointRequestRequestTypeDef,
    UpdateVpcEndpointResponseTypeDef,
    UpgradeElasticsearchDomainRequestRequestTypeDef,
    UpgradeElasticsearchDomainResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ElasticsearchServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ElasticsearchServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticsearchServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#close)
        """

    def accept_inbound_cross_cluster_search_connection(
        self, **kwargs: Unpack[AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef]
    ) -> AcceptInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to accept an inbound cross-cluster search
        connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/accept_inbound_cross_cluster_search_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#accept_inbound_cross_cluster_search_connection)
        """

    def add_tags(
        self, **kwargs: Unpack[AddTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches tags to an existing Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/add_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#add_tags)
        """

    def associate_package(
        self, **kwargs: Unpack[AssociatePackageRequestRequestTypeDef]
    ) -> AssociatePackageResponseTypeDef:
        """
        Associates a package with an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/associate_package.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#associate_package)
        """

    def authorize_vpc_endpoint_access(
        self, **kwargs: Unpack[AuthorizeVpcEndpointAccessRequestRequestTypeDef]
    ) -> AuthorizeVpcEndpointAccessResponseTypeDef:
        """
        Provides access to an Amazon OpenSearch Service domain through the use of an
        interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/authorize_vpc_endpoint_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#authorize_vpc_endpoint_access)
        """

    def cancel_domain_config_change(
        self, **kwargs: Unpack[CancelDomainConfigChangeRequestRequestTypeDef]
    ) -> CancelDomainConfigChangeResponseTypeDef:
        """
        Cancels a pending configuration change on an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/cancel_domain_config_change.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#cancel_domain_config_change)
        """

    def cancel_elasticsearch_service_software_update(
        self, **kwargs: Unpack[CancelElasticsearchServiceSoftwareUpdateRequestRequestTypeDef]
    ) -> CancelElasticsearchServiceSoftwareUpdateResponseTypeDef:
        """
        Cancels a scheduled service software update for an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/cancel_elasticsearch_service_software_update.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#cancel_elasticsearch_service_software_update)
        """

    def create_elasticsearch_domain(
        self, **kwargs: Unpack[CreateElasticsearchDomainRequestRequestTypeDef]
    ) -> CreateElasticsearchDomainResponseTypeDef:
        """
        Creates a new Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/create_elasticsearch_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_elasticsearch_domain)
        """

    def create_outbound_cross_cluster_search_connection(
        self, **kwargs: Unpack[CreateOutboundCrossClusterSearchConnectionRequestRequestTypeDef]
    ) -> CreateOutboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Creates a new cross-cluster search connection from a source domain to a
        destination domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/create_outbound_cross_cluster_search_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_outbound_cross_cluster_search_connection)
        """

    def create_package(
        self, **kwargs: Unpack[CreatePackageRequestRequestTypeDef]
    ) -> CreatePackageResponseTypeDef:
        """
        Create a package for use with Amazon ES domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/create_package.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_package)
        """

    def create_vpc_endpoint(
        self, **kwargs: Unpack[CreateVpcEndpointRequestRequestTypeDef]
    ) -> CreateVpcEndpointResponseTypeDef:
        """
        Creates an Amazon OpenSearch Service-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/create_vpc_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_vpc_endpoint)
        """

    def delete_elasticsearch_domain(
        self, **kwargs: Unpack[DeleteElasticsearchDomainRequestRequestTypeDef]
    ) -> DeleteElasticsearchDomainResponseTypeDef:
        """
        Permanently deletes the specified Elasticsearch domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/delete_elasticsearch_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_elasticsearch_domain)
        """

    def delete_elasticsearch_service_role(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the service-linked role that Elasticsearch Service uses to manage and
        maintain VPC domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/delete_elasticsearch_service_role.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_elasticsearch_service_role)
        """

    def delete_inbound_cross_cluster_search_connection(
        self, **kwargs: Unpack[DeleteInboundCrossClusterSearchConnectionRequestRequestTypeDef]
    ) -> DeleteInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to delete an existing inbound cross-cluster
        search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/delete_inbound_cross_cluster_search_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_inbound_cross_cluster_search_connection)
        """

    def delete_outbound_cross_cluster_search_connection(
        self, **kwargs: Unpack[DeleteOutboundCrossClusterSearchConnectionRequestRequestTypeDef]
    ) -> DeleteOutboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the source domain owner to delete an existing outbound cross-cluster
        search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/delete_outbound_cross_cluster_search_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_outbound_cross_cluster_search_connection)
        """

    def delete_package(
        self, **kwargs: Unpack[DeletePackageRequestRequestTypeDef]
    ) -> DeletePackageResponseTypeDef:
        """
        Delete the package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/delete_package.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_package)
        """

    def delete_vpc_endpoint(
        self, **kwargs: Unpack[DeleteVpcEndpointRequestRequestTypeDef]
    ) -> DeleteVpcEndpointResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/delete_vpc_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_vpc_endpoint)
        """

    def describe_domain_auto_tunes(
        self, **kwargs: Unpack[DescribeDomainAutoTunesRequestRequestTypeDef]
    ) -> DescribeDomainAutoTunesResponseTypeDef:
        """
        Provides scheduled Auto-Tune action details for the Elasticsearch domain, such
        as Auto-Tune action type, description, severity, and scheduled date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_domain_auto_tunes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_domain_auto_tunes)
        """

    def describe_domain_change_progress(
        self, **kwargs: Unpack[DescribeDomainChangeProgressRequestRequestTypeDef]
    ) -> DescribeDomainChangeProgressResponseTypeDef:
        """
        Returns information about the current blue/green deployment happening on a
        domain, including a change ID, status, and progress stages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_domain_change_progress.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_domain_change_progress)
        """

    def describe_elasticsearch_domain(
        self, **kwargs: Unpack[DescribeElasticsearchDomainRequestRequestTypeDef]
    ) -> DescribeElasticsearchDomainResponseTypeDef:
        """
        Returns domain configuration information about the specified Elasticsearch
        domain, including the domain ID, domain endpoint, and domain ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_elasticsearch_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_domain)
        """

    def describe_elasticsearch_domain_config(
        self, **kwargs: Unpack[DescribeElasticsearchDomainConfigRequestRequestTypeDef]
    ) -> DescribeElasticsearchDomainConfigResponseTypeDef:
        """
        Provides cluster configuration information about the specified Elasticsearch
        domain, such as the state, creation date, update version, and update date for
        cluster options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_elasticsearch_domain_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_domain_config)
        """

    def describe_elasticsearch_domains(
        self, **kwargs: Unpack[DescribeElasticsearchDomainsRequestRequestTypeDef]
    ) -> DescribeElasticsearchDomainsResponseTypeDef:
        """
        Returns domain configuration information about the specified Elasticsearch
        domains, including the domain ID, domain endpoint, and domain ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_elasticsearch_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_domains)
        """

    def describe_elasticsearch_instance_type_limits(
        self, **kwargs: Unpack[DescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef]
    ) -> DescribeElasticsearchInstanceTypeLimitsResponseTypeDef:
        """
        Describe Elasticsearch Limits for a given InstanceType and ElasticsearchVersion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_elasticsearch_instance_type_limits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_instance_type_limits)
        """

    def describe_inbound_cross_cluster_search_connections(
        self, **kwargs: Unpack[DescribeInboundCrossClusterSearchConnectionsRequestRequestTypeDef]
    ) -> DescribeInboundCrossClusterSearchConnectionsResponseTypeDef:
        """
        Lists all the inbound cross-cluster search connections for a destination domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_inbound_cross_cluster_search_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_inbound_cross_cluster_search_connections)
        """

    def describe_outbound_cross_cluster_search_connections(
        self, **kwargs: Unpack[DescribeOutboundCrossClusterSearchConnectionsRequestRequestTypeDef]
    ) -> DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef:
        """
        Lists all the outbound cross-cluster search connections for a source domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_outbound_cross_cluster_search_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_outbound_cross_cluster_search_connections)
        """

    def describe_packages(
        self, **kwargs: Unpack[DescribePackagesRequestRequestTypeDef]
    ) -> DescribePackagesResponseTypeDef:
        """
        Describes all packages available to Amazon ES.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_packages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_packages)
        """

    def describe_reserved_elasticsearch_instance_offerings(
        self, **kwargs: Unpack[DescribeReservedElasticsearchInstanceOfferingsRequestRequestTypeDef]
    ) -> DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef:
        """
        Lists available reserved Elasticsearch instance offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_reserved_elasticsearch_instance_offerings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_reserved_elasticsearch_instance_offerings)
        """

    def describe_reserved_elasticsearch_instances(
        self, **kwargs: Unpack[DescribeReservedElasticsearchInstancesRequestRequestTypeDef]
    ) -> DescribeReservedElasticsearchInstancesResponseTypeDef:
        """
        Returns information about reserved Elasticsearch instances for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_reserved_elasticsearch_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_reserved_elasticsearch_instances)
        """

    def describe_vpc_endpoints(
        self, **kwargs: Unpack[DescribeVpcEndpointsRequestRequestTypeDef]
    ) -> DescribeVpcEndpointsResponseTypeDef:
        """
        Describes one or more Amazon OpenSearch Service-managed VPC endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/describe_vpc_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_vpc_endpoints)
        """

    def dissociate_package(
        self, **kwargs: Unpack[DissociatePackageRequestRequestTypeDef]
    ) -> DissociatePackageResponseTypeDef:
        """
        Dissociates a package from the Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/dissociate_package.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#dissociate_package)
        """

    def get_compatible_elasticsearch_versions(
        self, **kwargs: Unpack[GetCompatibleElasticsearchVersionsRequestRequestTypeDef]
    ) -> GetCompatibleElasticsearchVersionsResponseTypeDef:
        """
        Returns a list of upgrade compatible Elastisearch versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_compatible_elasticsearch_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_compatible_elasticsearch_versions)
        """

    def get_package_version_history(
        self, **kwargs: Unpack[GetPackageVersionHistoryRequestRequestTypeDef]
    ) -> GetPackageVersionHistoryResponseTypeDef:
        """
        Returns a list of versions of the package, along with their creation time and
        commit message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_package_version_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_package_version_history)
        """

    def get_upgrade_history(
        self, **kwargs: Unpack[GetUpgradeHistoryRequestRequestTypeDef]
    ) -> GetUpgradeHistoryResponseTypeDef:
        """
        Retrieves the complete history of the last 10 upgrades that were performed on
        the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_upgrade_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_upgrade_history)
        """

    def get_upgrade_status(
        self, **kwargs: Unpack[GetUpgradeStatusRequestRequestTypeDef]
    ) -> GetUpgradeStatusResponseTypeDef:
        """
        Retrieves the latest status of the last upgrade or upgrade eligibility check
        that was performed on the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_upgrade_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_upgrade_status)
        """

    def list_domain_names(
        self, **kwargs: Unpack[ListDomainNamesRequestRequestTypeDef]
    ) -> ListDomainNamesResponseTypeDef:
        """
        Returns the name of all Elasticsearch domains owned by the current user's
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_domain_names.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_domain_names)
        """

    def list_domains_for_package(
        self, **kwargs: Unpack[ListDomainsForPackageRequestRequestTypeDef]
    ) -> ListDomainsForPackageResponseTypeDef:
        """
        Lists all Amazon ES domains associated with the package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_domains_for_package.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_domains_for_package)
        """

    def list_elasticsearch_instance_types(
        self, **kwargs: Unpack[ListElasticsearchInstanceTypesRequestRequestTypeDef]
    ) -> ListElasticsearchInstanceTypesResponseTypeDef:
        """
        List all Elasticsearch instance types that are supported for given
        ElasticsearchVersion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_elasticsearch_instance_types.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_elasticsearch_instance_types)
        """

    def list_elasticsearch_versions(
        self, **kwargs: Unpack[ListElasticsearchVersionsRequestRequestTypeDef]
    ) -> ListElasticsearchVersionsResponseTypeDef:
        """
        List all supported Elasticsearch versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_elasticsearch_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_elasticsearch_versions)
        """

    def list_packages_for_domain(
        self, **kwargs: Unpack[ListPackagesForDomainRequestRequestTypeDef]
    ) -> ListPackagesForDomainResponseTypeDef:
        """
        Lists all packages associated with the Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_packages_for_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_packages_for_domain)
        """

    def list_tags(self, **kwargs: Unpack[ListTagsRequestRequestTypeDef]) -> ListTagsResponseTypeDef:
        """
        Returns all tags for the given Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_tags)
        """

    def list_vpc_endpoint_access(
        self, **kwargs: Unpack[ListVpcEndpointAccessRequestRequestTypeDef]
    ) -> ListVpcEndpointAccessResponseTypeDef:
        """
        Retrieves information about each principal that is allowed to access a given
        Amazon OpenSearch Service domain through the use of an interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_vpc_endpoint_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_vpc_endpoint_access)
        """

    def list_vpc_endpoints(
        self, **kwargs: Unpack[ListVpcEndpointsRequestRequestTypeDef]
    ) -> ListVpcEndpointsResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints in the current
        account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_vpc_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_vpc_endpoints)
        """

    def list_vpc_endpoints_for_domain(
        self, **kwargs: Unpack[ListVpcEndpointsForDomainRequestRequestTypeDef]
    ) -> ListVpcEndpointsForDomainResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints associated with a
        particular domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/list_vpc_endpoints_for_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_vpc_endpoints_for_domain)
        """

    def purchase_reserved_elasticsearch_instance_offering(
        self, **kwargs: Unpack[PurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef]
    ) -> PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef:
        """
        Allows you to purchase reserved Elasticsearch instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/purchase_reserved_elasticsearch_instance_offering.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#purchase_reserved_elasticsearch_instance_offering)
        """

    def reject_inbound_cross_cluster_search_connection(
        self, **kwargs: Unpack[RejectInboundCrossClusterSearchConnectionRequestRequestTypeDef]
    ) -> RejectInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to reject an inbound cross-cluster search
        connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/reject_inbound_cross_cluster_search_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#reject_inbound_cross_cluster_search_connection)
        """

    def remove_tags(
        self, **kwargs: Unpack[RemoveTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified set of tags from the specified Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/remove_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#remove_tags)
        """

    def revoke_vpc_endpoint_access(
        self, **kwargs: Unpack[RevokeVpcEndpointAccessRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Revokes access to an Amazon OpenSearch Service domain that was provided through
        an interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/revoke_vpc_endpoint_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#revoke_vpc_endpoint_access)
        """

    def start_elasticsearch_service_software_update(
        self, **kwargs: Unpack[StartElasticsearchServiceSoftwareUpdateRequestRequestTypeDef]
    ) -> StartElasticsearchServiceSoftwareUpdateResponseTypeDef:
        """
        Schedules a service software update for an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/start_elasticsearch_service_software_update.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#start_elasticsearch_service_software_update)
        """

    def update_elasticsearch_domain_config(
        self, **kwargs: Unpack[UpdateElasticsearchDomainConfigRequestRequestTypeDef]
    ) -> UpdateElasticsearchDomainConfigResponseTypeDef:
        """
        Modifies the cluster configuration of the specified Elasticsearch domain,
        setting as setting the instance type and the number of instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/update_elasticsearch_domain_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#update_elasticsearch_domain_config)
        """

    def update_package(
        self, **kwargs: Unpack[UpdatePackageRequestRequestTypeDef]
    ) -> UpdatePackageResponseTypeDef:
        """
        Updates a package for use with Amazon ES domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/update_package.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#update_package)
        """

    def update_vpc_endpoint(
        self, **kwargs: Unpack[UpdateVpcEndpointRequestRequestTypeDef]
    ) -> UpdateVpcEndpointResponseTypeDef:
        """
        Modifies an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/update_vpc_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#update_vpc_endpoint)
        """

    def upgrade_elasticsearch_domain(
        self, **kwargs: Unpack[UpgradeElasticsearchDomainRequestRequestTypeDef]
    ) -> UpgradeElasticsearchDomainResponseTypeDef:
        """
        Allows you to either upgrade your domain or perform an Upgrade eligibility
        check to a compatible Elasticsearch version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/upgrade_elasticsearch_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#upgrade_elasticsearch_domain)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_elasticsearch_instance_offerings"]
    ) -> DescribeReservedElasticsearchInstanceOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_elasticsearch_instances"]
    ) -> DescribeReservedElasticsearchInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_upgrade_history"]
    ) -> GetUpgradeHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_elasticsearch_instance_types"]
    ) -> ListElasticsearchInstanceTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_elasticsearch_versions"]
    ) -> ListElasticsearchVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """
