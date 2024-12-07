"""
Type annotations for kafka service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_kafka.client import KafkaClient
    from mypy_boto3_kafka.paginator import (
        ListClientVpcConnectionsPaginator,
        ListClusterOperationsPaginator,
        ListClusterOperationsV2Paginator,
        ListClustersPaginator,
        ListClustersV2Paginator,
        ListConfigurationRevisionsPaginator,
        ListConfigurationsPaginator,
        ListKafkaVersionsPaginator,
        ListNodesPaginator,
        ListReplicatorsPaginator,
        ListScramSecretsPaginator,
        ListVpcConnectionsPaginator,
    )

    session = Session()
    client: KafkaClient = session.client("kafka")

    list_client_vpc_connections_paginator: ListClientVpcConnectionsPaginator = client.get_paginator("list_client_vpc_connections")
    list_cluster_operations_paginator: ListClusterOperationsPaginator = client.get_paginator("list_cluster_operations")
    list_cluster_operations_v2_paginator: ListClusterOperationsV2Paginator = client.get_paginator("list_cluster_operations_v2")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_clusters_v2_paginator: ListClustersV2Paginator = client.get_paginator("list_clusters_v2")
    list_configuration_revisions_paginator: ListConfigurationRevisionsPaginator = client.get_paginator("list_configuration_revisions")
    list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    list_kafka_versions_paginator: ListKafkaVersionsPaginator = client.get_paginator("list_kafka_versions")
    list_nodes_paginator: ListNodesPaginator = client.get_paginator("list_nodes")
    list_replicators_paginator: ListReplicatorsPaginator = client.get_paginator("list_replicators")
    list_scram_secrets_paginator: ListScramSecretsPaginator = client.get_paginator("list_scram_secrets")
    list_vpc_connections_paginator: ListVpcConnectionsPaginator = client.get_paginator("list_vpc_connections")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef,
    ListClientVpcConnectionsResponseTypeDef,
    ListClusterOperationsRequestListClusterOperationsPaginateTypeDef,
    ListClusterOperationsResponseTypeDef,
    ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef,
    ListClusterOperationsV2ResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListClustersV2RequestListClustersV2PaginateTypeDef,
    ListClustersV2ResponseTypeDef,
    ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsRequestListConfigurationsPaginateTypeDef,
    ListConfigurationsResponseTypeDef,
    ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef,
    ListKafkaVersionsResponseTypeDef,
    ListNodesRequestListNodesPaginateTypeDef,
    ListNodesResponseTypeDef,
    ListReplicatorsRequestListReplicatorsPaginateTypeDef,
    ListReplicatorsResponseTypeDef,
    ListScramSecretsRequestListScramSecretsPaginateTypeDef,
    ListScramSecretsResponseTypeDef,
    ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef,
    ListVpcConnectionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListClientVpcConnectionsPaginator",
    "ListClusterOperationsPaginator",
    "ListClusterOperationsV2Paginator",
    "ListClustersPaginator",
    "ListClustersV2Paginator",
    "ListConfigurationRevisionsPaginator",
    "ListConfigurationsPaginator",
    "ListKafkaVersionsPaginator",
    "ListNodesPaginator",
    "ListReplicatorsPaginator",
    "ListScramSecretsPaginator",
    "ListVpcConnectionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListClientVpcConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClientVpcConnections.html#Kafka.Paginator.ListClientVpcConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclientvpcconnectionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef],
    ) -> _PageIterator[ListClientVpcConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClientVpcConnections.html#Kafka.Paginator.ListClientVpcConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclientvpcconnectionspaginator)
        """


class ListClusterOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperations.html#Kafka.Paginator.ListClusterOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclusteroperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClusterOperationsRequestListClusterOperationsPaginateTypeDef]
    ) -> _PageIterator[ListClusterOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperations.html#Kafka.Paginator.ListClusterOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclusteroperationspaginator)
        """


class ListClusterOperationsV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperationsV2.html#Kafka.Paginator.ListClusterOperationsV2)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclusteroperationsv2paginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef]
    ) -> _PageIterator[ListClusterOperationsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperationsV2.html#Kafka.Paginator.ListClusterOperationsV2.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclusteroperationsv2paginator)
        """


class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusters.html#Kafka.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusters.html#Kafka.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclusterspaginator)
        """


class ListClustersV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClustersV2.html#Kafka.Paginator.ListClustersV2)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclustersv2paginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClustersV2RequestListClustersV2PaginateTypeDef]
    ) -> _PageIterator[ListClustersV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClustersV2.html#Kafka.Paginator.ListClustersV2.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listclustersv2paginator)
        """


class ListConfigurationRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurationRevisions.html#Kafka.Paginator.ListConfigurationRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listconfigurationrevisionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfigurationRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurationRevisions.html#Kafka.Paginator.ListConfigurationRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listconfigurationrevisionspaginator)
        """


class ListConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurations.html#Kafka.Paginator.ListConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listconfigurationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListConfigurationsRequestListConfigurationsPaginateTypeDef]
    ) -> _PageIterator[ListConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurations.html#Kafka.Paginator.ListConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listconfigurationspaginator)
        """


class ListKafkaVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListKafkaVersions.html#Kafka.Paginator.ListKafkaVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listkafkaversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef]
    ) -> _PageIterator[ListKafkaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListKafkaVersions.html#Kafka.Paginator.ListKafkaVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listkafkaversionspaginator)
        """


class ListNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListNodes.html#Kafka.Paginator.ListNodes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listnodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNodesRequestListNodesPaginateTypeDef]
    ) -> _PageIterator[ListNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListNodes.html#Kafka.Paginator.ListNodes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listnodespaginator)
        """


class ListReplicatorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListReplicators.html#Kafka.Paginator.ListReplicators)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listreplicatorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReplicatorsRequestListReplicatorsPaginateTypeDef]
    ) -> _PageIterator[ListReplicatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListReplicators.html#Kafka.Paginator.ListReplicators.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listreplicatorspaginator)
        """


class ListScramSecretsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListScramSecrets.html#Kafka.Paginator.ListScramSecrets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listscramsecretspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListScramSecretsRequestListScramSecretsPaginateTypeDef]
    ) -> _PageIterator[ListScramSecretsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListScramSecrets.html#Kafka.Paginator.ListScramSecrets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listscramsecretspaginator)
        """


class ListVpcConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListVpcConnections.html#Kafka.Paginator.ListVpcConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listvpcconnectionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef]
    ) -> _PageIterator[ListVpcConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListVpcConnections.html#Kafka.Paginator.ListVpcConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/paginators/#listvpcconnectionspaginator)
        """
