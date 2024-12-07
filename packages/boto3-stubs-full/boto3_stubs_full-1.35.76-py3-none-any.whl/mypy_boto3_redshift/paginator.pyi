"""
Type annotations for redshift service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_redshift.client import RedshiftClient
    from mypy_boto3_redshift.paginator import (
        DescribeClusterDbRevisionsPaginator,
        DescribeClusterParameterGroupsPaginator,
        DescribeClusterParametersPaginator,
        DescribeClusterSecurityGroupsPaginator,
        DescribeClusterSnapshotsPaginator,
        DescribeClusterSubnetGroupsPaginator,
        DescribeClusterTracksPaginator,
        DescribeClusterVersionsPaginator,
        DescribeClustersPaginator,
        DescribeCustomDomainAssociationsPaginator,
        DescribeDataSharesForConsumerPaginator,
        DescribeDataSharesForProducerPaginator,
        DescribeDataSharesPaginator,
        DescribeDefaultClusterParametersPaginator,
        DescribeEndpointAccessPaginator,
        DescribeEndpointAuthorizationPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeHsmClientCertificatesPaginator,
        DescribeHsmConfigurationsPaginator,
        DescribeInboundIntegrationsPaginator,
        DescribeIntegrationsPaginator,
        DescribeNodeConfigurationOptionsPaginator,
        DescribeOrderableClusterOptionsPaginator,
        DescribeRedshiftIdcApplicationsPaginator,
        DescribeReservedNodeExchangeStatusPaginator,
        DescribeReservedNodeOfferingsPaginator,
        DescribeReservedNodesPaginator,
        DescribeScheduledActionsPaginator,
        DescribeSnapshotCopyGrantsPaginator,
        DescribeSnapshotSchedulesPaginator,
        DescribeTableRestoreStatusPaginator,
        DescribeTagsPaginator,
        DescribeUsageLimitsPaginator,
        GetReservedNodeExchangeConfigurationOptionsPaginator,
        GetReservedNodeExchangeOfferingsPaginator,
        ListRecommendationsPaginator,
    )

    session = Session()
    client: RedshiftClient = session.client("redshift")

    describe_cluster_db_revisions_paginator: DescribeClusterDbRevisionsPaginator = client.get_paginator("describe_cluster_db_revisions")
    describe_cluster_parameter_groups_paginator: DescribeClusterParameterGroupsPaginator = client.get_paginator("describe_cluster_parameter_groups")
    describe_cluster_parameters_paginator: DescribeClusterParametersPaginator = client.get_paginator("describe_cluster_parameters")
    describe_cluster_security_groups_paginator: DescribeClusterSecurityGroupsPaginator = client.get_paginator("describe_cluster_security_groups")
    describe_cluster_snapshots_paginator: DescribeClusterSnapshotsPaginator = client.get_paginator("describe_cluster_snapshots")
    describe_cluster_subnet_groups_paginator: DescribeClusterSubnetGroupsPaginator = client.get_paginator("describe_cluster_subnet_groups")
    describe_cluster_tracks_paginator: DescribeClusterTracksPaginator = client.get_paginator("describe_cluster_tracks")
    describe_cluster_versions_paginator: DescribeClusterVersionsPaginator = client.get_paginator("describe_cluster_versions")
    describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
    describe_custom_domain_associations_paginator: DescribeCustomDomainAssociationsPaginator = client.get_paginator("describe_custom_domain_associations")
    describe_data_shares_for_consumer_paginator: DescribeDataSharesForConsumerPaginator = client.get_paginator("describe_data_shares_for_consumer")
    describe_data_shares_for_producer_paginator: DescribeDataSharesForProducerPaginator = client.get_paginator("describe_data_shares_for_producer")
    describe_data_shares_paginator: DescribeDataSharesPaginator = client.get_paginator("describe_data_shares")
    describe_default_cluster_parameters_paginator: DescribeDefaultClusterParametersPaginator = client.get_paginator("describe_default_cluster_parameters")
    describe_endpoint_access_paginator: DescribeEndpointAccessPaginator = client.get_paginator("describe_endpoint_access")
    describe_endpoint_authorization_paginator: DescribeEndpointAuthorizationPaginator = client.get_paginator("describe_endpoint_authorization")
    describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_hsm_client_certificates_paginator: DescribeHsmClientCertificatesPaginator = client.get_paginator("describe_hsm_client_certificates")
    describe_hsm_configurations_paginator: DescribeHsmConfigurationsPaginator = client.get_paginator("describe_hsm_configurations")
    describe_inbound_integrations_paginator: DescribeInboundIntegrationsPaginator = client.get_paginator("describe_inbound_integrations")
    describe_integrations_paginator: DescribeIntegrationsPaginator = client.get_paginator("describe_integrations")
    describe_node_configuration_options_paginator: DescribeNodeConfigurationOptionsPaginator = client.get_paginator("describe_node_configuration_options")
    describe_orderable_cluster_options_paginator: DescribeOrderableClusterOptionsPaginator = client.get_paginator("describe_orderable_cluster_options")
    describe_redshift_idc_applications_paginator: DescribeRedshiftIdcApplicationsPaginator = client.get_paginator("describe_redshift_idc_applications")
    describe_reserved_node_exchange_status_paginator: DescribeReservedNodeExchangeStatusPaginator = client.get_paginator("describe_reserved_node_exchange_status")
    describe_reserved_node_offerings_paginator: DescribeReservedNodeOfferingsPaginator = client.get_paginator("describe_reserved_node_offerings")
    describe_reserved_nodes_paginator: DescribeReservedNodesPaginator = client.get_paginator("describe_reserved_nodes")
    describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
    describe_snapshot_copy_grants_paginator: DescribeSnapshotCopyGrantsPaginator = client.get_paginator("describe_snapshot_copy_grants")
    describe_snapshot_schedules_paginator: DescribeSnapshotSchedulesPaginator = client.get_paginator("describe_snapshot_schedules")
    describe_table_restore_status_paginator: DescribeTableRestoreStatusPaginator = client.get_paginator("describe_table_restore_status")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    describe_usage_limits_paginator: DescribeUsageLimitsPaginator = client.get_paginator("describe_usage_limits")
    get_reserved_node_exchange_configuration_options_paginator: GetReservedNodeExchangeConfigurationOptionsPaginator = client.get_paginator("get_reserved_node_exchange_configuration_options")
    get_reserved_node_exchange_offerings_paginator: GetReservedNodeExchangeOfferingsPaginator = client.get_paginator("get_reserved_node_exchange_offerings")
    list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ClusterDbRevisionsMessageTypeDef,
    ClusterParameterGroupDetailsTypeDef,
    ClusterParameterGroupsMessageTypeDef,
    ClusterSecurityGroupMessageTypeDef,
    ClustersMessageTypeDef,
    ClusterSubnetGroupMessageTypeDef,
    ClusterVersionsMessageTypeDef,
    CustomDomainAssociationsMessageTypeDef,
    DescribeClusterDbRevisionsMessageDescribeClusterDbRevisionsPaginateTypeDef,
    DescribeClusterParameterGroupsMessageDescribeClusterParameterGroupsPaginateTypeDef,
    DescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef,
    DescribeClusterSecurityGroupsMessageDescribeClusterSecurityGroupsPaginateTypeDef,
    DescribeClustersMessageDescribeClustersPaginateTypeDef,
    DescribeClusterSnapshotsMessageDescribeClusterSnapshotsPaginateTypeDef,
    DescribeClusterSubnetGroupsMessageDescribeClusterSubnetGroupsPaginateTypeDef,
    DescribeClusterTracksMessageDescribeClusterTracksPaginateTypeDef,
    DescribeClusterVersionsMessageDescribeClusterVersionsPaginateTypeDef,
    DescribeCustomDomainAssociationsMessageDescribeCustomDomainAssociationsPaginateTypeDef,
    DescribeDataSharesForConsumerMessageDescribeDataSharesForConsumerPaginateTypeDef,
    DescribeDataSharesForConsumerResultTypeDef,
    DescribeDataSharesForProducerMessageDescribeDataSharesForProducerPaginateTypeDef,
    DescribeDataSharesForProducerResultTypeDef,
    DescribeDataSharesMessageDescribeDataSharesPaginateTypeDef,
    DescribeDataSharesResultTypeDef,
    DescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef,
    DescribeDefaultClusterParametersResultTypeDef,
    DescribeEndpointAccessMessageDescribeEndpointAccessPaginateTypeDef,
    DescribeEndpointAuthorizationMessageDescribeEndpointAuthorizationPaginateTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef,
    DescribeHsmClientCertificatesMessageDescribeHsmClientCertificatesPaginateTypeDef,
    DescribeHsmConfigurationsMessageDescribeHsmConfigurationsPaginateTypeDef,
    DescribeInboundIntegrationsMessageDescribeInboundIntegrationsPaginateTypeDef,
    DescribeIntegrationsMessageDescribeIntegrationsPaginateTypeDef,
    DescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef,
    DescribeOrderableClusterOptionsMessageDescribeOrderableClusterOptionsPaginateTypeDef,
    DescribeRedshiftIdcApplicationsMessageDescribeRedshiftIdcApplicationsPaginateTypeDef,
    DescribeRedshiftIdcApplicationsResultTypeDef,
    DescribeReservedNodeExchangeStatusInputMessageDescribeReservedNodeExchangeStatusPaginateTypeDef,
    DescribeReservedNodeExchangeStatusOutputMessageTypeDef,
    DescribeReservedNodeOfferingsMessageDescribeReservedNodeOfferingsPaginateTypeDef,
    DescribeReservedNodesMessageDescribeReservedNodesPaginateTypeDef,
    DescribeScheduledActionsMessageDescribeScheduledActionsPaginateTypeDef,
    DescribeSnapshotCopyGrantsMessageDescribeSnapshotCopyGrantsPaginateTypeDef,
    DescribeSnapshotSchedulesMessageDescribeSnapshotSchedulesPaginateTypeDef,
    DescribeSnapshotSchedulesOutputMessageTypeDef,
    DescribeTableRestoreStatusMessageDescribeTableRestoreStatusPaginateTypeDef,
    DescribeTagsMessageDescribeTagsPaginateTypeDef,
    DescribeUsageLimitsMessageDescribeUsageLimitsPaginateTypeDef,
    EndpointAccessListTypeDef,
    EndpointAuthorizationListTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    GetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef,
    GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef,
    GetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef,
    GetReservedNodeExchangeOfferingsOutputMessageTypeDef,
    HsmClientCertificateMessageTypeDef,
    HsmConfigurationMessageTypeDef,
    InboundIntegrationsMessageTypeDef,
    IntegrationsMessageTypeDef,
    ListRecommendationsMessageListRecommendationsPaginateTypeDef,
    ListRecommendationsResultTypeDef,
    NodeConfigurationOptionsMessageTypeDef,
    OrderableClusterOptionsMessageTypeDef,
    ReservedNodeOfferingsMessageTypeDef,
    ReservedNodesMessageTypeDef,
    ScheduledActionsMessageTypeDef,
    SnapshotCopyGrantMessageTypeDef,
    SnapshotMessageTypeDef,
    TableRestoreStatusMessageTypeDef,
    TaggedResourceListMessageTypeDef,
    TrackListMessageTypeDef,
    UsageLimitListTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeClusterDbRevisionsPaginator",
    "DescribeClusterParameterGroupsPaginator",
    "DescribeClusterParametersPaginator",
    "DescribeClusterSecurityGroupsPaginator",
    "DescribeClusterSnapshotsPaginator",
    "DescribeClusterSubnetGroupsPaginator",
    "DescribeClusterTracksPaginator",
    "DescribeClusterVersionsPaginator",
    "DescribeClustersPaginator",
    "DescribeCustomDomainAssociationsPaginator",
    "DescribeDataSharesForConsumerPaginator",
    "DescribeDataSharesForProducerPaginator",
    "DescribeDataSharesPaginator",
    "DescribeDefaultClusterParametersPaginator",
    "DescribeEndpointAccessPaginator",
    "DescribeEndpointAuthorizationPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeHsmClientCertificatesPaginator",
    "DescribeHsmConfigurationsPaginator",
    "DescribeInboundIntegrationsPaginator",
    "DescribeIntegrationsPaginator",
    "DescribeNodeConfigurationOptionsPaginator",
    "DescribeOrderableClusterOptionsPaginator",
    "DescribeRedshiftIdcApplicationsPaginator",
    "DescribeReservedNodeExchangeStatusPaginator",
    "DescribeReservedNodeOfferingsPaginator",
    "DescribeReservedNodesPaginator",
    "DescribeScheduledActionsPaginator",
    "DescribeSnapshotCopyGrantsPaginator",
    "DescribeSnapshotSchedulesPaginator",
    "DescribeTableRestoreStatusPaginator",
    "DescribeTagsPaginator",
    "DescribeUsageLimitsPaginator",
    "GetReservedNodeExchangeConfigurationOptionsPaginator",
    "GetReservedNodeExchangeOfferingsPaginator",
    "ListRecommendationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeClusterDbRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterDbRevisions.html#Redshift.Paginator.DescribeClusterDbRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterdbrevisionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterDbRevisionsMessageDescribeClusterDbRevisionsPaginateTypeDef
        ],
    ) -> _PageIterator[ClusterDbRevisionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterDbRevisions.html#Redshift.Paginator.DescribeClusterDbRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterdbrevisionspaginator)
        """

class DescribeClusterParameterGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameterGroups.html#Redshift.Paginator.DescribeClusterParameterGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterparametergroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterParameterGroupsMessageDescribeClusterParameterGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameterGroups.html#Redshift.Paginator.DescribeClusterParameterGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterparametergroupspaginator)
        """

class DescribeClusterParametersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameters.html#Redshift.Paginator.DescribeClusterParameters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef],
    ) -> _PageIterator[ClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameters.html#Redshift.Paginator.DescribeClusterParameters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterparameterspaginator)
        """

class DescribeClusterSecurityGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSecurityGroups.html#Redshift.Paginator.DescribeClusterSecurityGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustersecuritygroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterSecurityGroupsMessageDescribeClusterSecurityGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ClusterSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSecurityGroups.html#Redshift.Paginator.DescribeClusterSecurityGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustersecuritygroupspaginator)
        """

class DescribeClusterSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSnapshots.html#Redshift.Paginator.DescribeClusterSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustersnapshotspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeClusterSnapshotsMessageDescribeClusterSnapshotsPaginateTypeDef],
    ) -> _PageIterator[SnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSnapshots.html#Redshift.Paginator.DescribeClusterSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustersnapshotspaginator)
        """

class DescribeClusterSubnetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSubnetGroups.html#Redshift.Paginator.DescribeClusterSubnetGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustersubnetgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterSubnetGroupsMessageDescribeClusterSubnetGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ClusterSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSubnetGroups.html#Redshift.Paginator.DescribeClusterSubnetGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustersubnetgroupspaginator)
        """

class DescribeClusterTracksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterTracks.html#Redshift.Paginator.DescribeClusterTracks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustertrackspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClusterTracksMessageDescribeClusterTracksPaginateTypeDef]
    ) -> _PageIterator[TrackListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterTracks.html#Redshift.Paginator.DescribeClusterTracks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclustertrackspaginator)
        """

class DescribeClusterVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterVersions.html#Redshift.Paginator.DescribeClusterVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClusterVersionsMessageDescribeClusterVersionsPaginateTypeDef]
    ) -> _PageIterator[ClusterVersionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterVersions.html#Redshift.Paginator.DescribeClusterVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterversionspaginator)
        """

class DescribeClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusters.html#Redshift.Paginator.DescribeClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClustersMessageDescribeClustersPaginateTypeDef]
    ) -> _PageIterator[ClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusters.html#Redshift.Paginator.DescribeClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeclusterspaginator)
        """

class DescribeCustomDomainAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeCustomDomainAssociations.html#Redshift.Paginator.DescribeCustomDomainAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describecustomdomainassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCustomDomainAssociationsMessageDescribeCustomDomainAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[CustomDomainAssociationsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeCustomDomainAssociations.html#Redshift.Paginator.DescribeCustomDomainAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describecustomdomainassociationspaginator)
        """

class DescribeDataSharesForConsumerPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForConsumer.html#Redshift.Paginator.DescribeDataSharesForConsumer)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedatasharesforconsumerpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDataSharesForConsumerMessageDescribeDataSharesForConsumerPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeDataSharesForConsumerResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForConsumer.html#Redshift.Paginator.DescribeDataSharesForConsumer.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedatasharesforconsumerpaginator)
        """

class DescribeDataSharesForProducerPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForProducer.html#Redshift.Paginator.DescribeDataSharesForProducer)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedatasharesforproducerpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDataSharesForProducerMessageDescribeDataSharesForProducerPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeDataSharesForProducerResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForProducer.html#Redshift.Paginator.DescribeDataSharesForProducer.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedatasharesforproducerpaginator)
        """

class DescribeDataSharesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataShares.html#Redshift.Paginator.DescribeDataShares)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedatasharespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDataSharesMessageDescribeDataSharesPaginateTypeDef]
    ) -> _PageIterator[DescribeDataSharesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataShares.html#Redshift.Paginator.DescribeDataShares.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedatasharespaginator)
        """

class DescribeDefaultClusterParametersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDefaultClusterParameters.html#Redshift.Paginator.DescribeDefaultClusterParameters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedefaultclusterparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeDefaultClusterParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDefaultClusterParameters.html#Redshift.Paginator.DescribeDefaultClusterParameters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describedefaultclusterparameterspaginator)
        """

class DescribeEndpointAccessPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAccess.html#Redshift.Paginator.DescribeEndpointAccess)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeendpointaccesspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEndpointAccessMessageDescribeEndpointAccessPaginateTypeDef]
    ) -> _PageIterator[EndpointAccessListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAccess.html#Redshift.Paginator.DescribeEndpointAccess.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeendpointaccesspaginator)
        """

class DescribeEndpointAuthorizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAuthorization.html#Redshift.Paginator.DescribeEndpointAuthorization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeendpointauthorizationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEndpointAuthorizationMessageDescribeEndpointAuthorizationPaginateTypeDef
        ],
    ) -> _PageIterator[EndpointAuthorizationListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAuthorization.html#Redshift.Paginator.DescribeEndpointAuthorization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeendpointauthorizationpaginator)
        """

class DescribeEventSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEventSubscriptions.html#Redshift.Paginator.DescribeEventSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeeventsubscriptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef
        ],
    ) -> _PageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEventSubscriptions.html#Redshift.Paginator.DescribeEventSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeeventsubscriptionspaginator)
        """

class DescribeEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEvents.html#Redshift.Paginator.DescribeEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> _PageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEvents.html#Redshift.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeeventspaginator)
        """

class DescribeHsmClientCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmClientCertificates.html#Redshift.Paginator.DescribeHsmClientCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describehsmclientcertificatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeHsmClientCertificatesMessageDescribeHsmClientCertificatesPaginateTypeDef
        ],
    ) -> _PageIterator[HsmClientCertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmClientCertificates.html#Redshift.Paginator.DescribeHsmClientCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describehsmclientcertificatespaginator)
        """

class DescribeHsmConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmConfigurations.html#Redshift.Paginator.DescribeHsmConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describehsmconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeHsmConfigurationsMessageDescribeHsmConfigurationsPaginateTypeDef],
    ) -> _PageIterator[HsmConfigurationMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmConfigurations.html#Redshift.Paginator.DescribeHsmConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describehsmconfigurationspaginator)
        """

class DescribeInboundIntegrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeInboundIntegrations.html#Redshift.Paginator.DescribeInboundIntegrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeinboundintegrationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInboundIntegrationsMessageDescribeInboundIntegrationsPaginateTypeDef
        ],
    ) -> _PageIterator[InboundIntegrationsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeInboundIntegrations.html#Redshift.Paginator.DescribeInboundIntegrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeinboundintegrationspaginator)
        """

class DescribeIntegrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeIntegrations.html#Redshift.Paginator.DescribeIntegrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeintegrationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeIntegrationsMessageDescribeIntegrationsPaginateTypeDef]
    ) -> _PageIterator[IntegrationsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeIntegrations.html#Redshift.Paginator.DescribeIntegrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeintegrationspaginator)
        """

class DescribeNodeConfigurationOptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeNodeConfigurationOptions.html#Redshift.Paginator.DescribeNodeConfigurationOptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describenodeconfigurationoptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef
        ],
    ) -> _PageIterator[NodeConfigurationOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeNodeConfigurationOptions.html#Redshift.Paginator.DescribeNodeConfigurationOptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describenodeconfigurationoptionspaginator)
        """

class DescribeOrderableClusterOptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeOrderableClusterOptions.html#Redshift.Paginator.DescribeOrderableClusterOptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeorderableclusteroptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrderableClusterOptionsMessageDescribeOrderableClusterOptionsPaginateTypeDef
        ],
    ) -> _PageIterator[OrderableClusterOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeOrderableClusterOptions.html#Redshift.Paginator.DescribeOrderableClusterOptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeorderableclusteroptionspaginator)
        """

class DescribeRedshiftIdcApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeRedshiftIdcApplications.html#Redshift.Paginator.DescribeRedshiftIdcApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeredshiftidcapplicationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRedshiftIdcApplicationsMessageDescribeRedshiftIdcApplicationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRedshiftIdcApplicationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeRedshiftIdcApplications.html#Redshift.Paginator.DescribeRedshiftIdcApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeredshiftidcapplicationspaginator)
        """

class DescribeReservedNodeExchangeStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeExchangeStatus.html#Redshift.Paginator.DescribeReservedNodeExchangeStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describereservednodeexchangestatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedNodeExchangeStatusInputMessageDescribeReservedNodeExchangeStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReservedNodeExchangeStatusOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeExchangeStatus.html#Redshift.Paginator.DescribeReservedNodeExchangeStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describereservednodeexchangestatuspaginator)
        """

class DescribeReservedNodeOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeOfferings.html#Redshift.Paginator.DescribeReservedNodeOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describereservednodeofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedNodeOfferingsMessageDescribeReservedNodeOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[ReservedNodeOfferingsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeOfferings.html#Redshift.Paginator.DescribeReservedNodeOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describereservednodeofferingspaginator)
        """

class DescribeReservedNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodes.html#Redshift.Paginator.DescribeReservedNodes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describereservednodespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeReservedNodesMessageDescribeReservedNodesPaginateTypeDef]
    ) -> _PageIterator[ReservedNodesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodes.html#Redshift.Paginator.DescribeReservedNodes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describereservednodespaginator)
        """

class DescribeScheduledActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeScheduledActions.html#Redshift.Paginator.DescribeScheduledActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describescheduledactionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeScheduledActionsMessageDescribeScheduledActionsPaginateTypeDef],
    ) -> _PageIterator[ScheduledActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeScheduledActions.html#Redshift.Paginator.DescribeScheduledActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describescheduledactionspaginator)
        """

class DescribeSnapshotCopyGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotCopyGrants.html#Redshift.Paginator.DescribeSnapshotCopyGrants)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describesnapshotcopygrantspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSnapshotCopyGrantsMessageDescribeSnapshotCopyGrantsPaginateTypeDef
        ],
    ) -> _PageIterator[SnapshotCopyGrantMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotCopyGrants.html#Redshift.Paginator.DescribeSnapshotCopyGrants.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describesnapshotcopygrantspaginator)
        """

class DescribeSnapshotSchedulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotSchedules.html#Redshift.Paginator.DescribeSnapshotSchedules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describesnapshotschedulespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeSnapshotSchedulesMessageDescribeSnapshotSchedulesPaginateTypeDef],
    ) -> _PageIterator[DescribeSnapshotSchedulesOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotSchedules.html#Redshift.Paginator.DescribeSnapshotSchedules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describesnapshotschedulespaginator)
        """

class DescribeTableRestoreStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTableRestoreStatus.html#Redshift.Paginator.DescribeTableRestoreStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describetablerestorestatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTableRestoreStatusMessageDescribeTableRestoreStatusPaginateTypeDef
        ],
    ) -> _PageIterator[TableRestoreStatusMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTableRestoreStatus.html#Redshift.Paginator.DescribeTableRestoreStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describetablerestorestatuspaginator)
        """

class DescribeTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTags.html#Redshift.Paginator.DescribeTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTagsMessageDescribeTagsPaginateTypeDef]
    ) -> _PageIterator[TaggedResourceListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTags.html#Redshift.Paginator.DescribeTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describetagspaginator)
        """

class DescribeUsageLimitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeUsageLimits.html#Redshift.Paginator.DescribeUsageLimits)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeusagelimitspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUsageLimitsMessageDescribeUsageLimitsPaginateTypeDef]
    ) -> _PageIterator[UsageLimitListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeUsageLimits.html#Redshift.Paginator.DescribeUsageLimits.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#describeusagelimitspaginator)
        """

class GetReservedNodeExchangeConfigurationOptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeConfigurationOptions.html#Redshift.Paginator.GetReservedNodeExchangeConfigurationOptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#getreservednodeexchangeconfigurationoptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef
        ],
    ) -> _PageIterator[GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeConfigurationOptions.html#Redshift.Paginator.GetReservedNodeExchangeConfigurationOptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#getreservednodeexchangeconfigurationoptionspaginator)
        """

class GetReservedNodeExchangeOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeOfferings.html#Redshift.Paginator.GetReservedNodeExchangeOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#getreservednodeexchangeofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[GetReservedNodeExchangeOfferingsOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeOfferings.html#Redshift.Paginator.GetReservedNodeExchangeOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#getreservednodeexchangeofferingspaginator)
        """

class ListRecommendationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/ListRecommendations.html#Redshift.Paginator.ListRecommendations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#listrecommendationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecommendationsMessageListRecommendationsPaginateTypeDef]
    ) -> _PageIterator[ListRecommendationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/ListRecommendations.html#Redshift.Paginator.ListRecommendations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/paginators/#listrecommendationspaginator)
        """
