"""
Type annotations for route53 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53.client import Route53Client
    from mypy_boto3_route53.paginator import (
        ListCidrBlocksPaginator,
        ListCidrCollectionsPaginator,
        ListCidrLocationsPaginator,
        ListHealthChecksPaginator,
        ListHostedZonesPaginator,
        ListQueryLoggingConfigsPaginator,
        ListResourceRecordSetsPaginator,
        ListVPCAssociationAuthorizationsPaginator,
    )

    session = Session()
    client: Route53Client = session.client("route53")

    list_cidr_blocks_paginator: ListCidrBlocksPaginator = client.get_paginator("list_cidr_blocks")
    list_cidr_collections_paginator: ListCidrCollectionsPaginator = client.get_paginator("list_cidr_collections")
    list_cidr_locations_paginator: ListCidrLocationsPaginator = client.get_paginator("list_cidr_locations")
    list_health_checks_paginator: ListHealthChecksPaginator = client.get_paginator("list_health_checks")
    list_hosted_zones_paginator: ListHostedZonesPaginator = client.get_paginator("list_hosted_zones")
    list_query_logging_configs_paginator: ListQueryLoggingConfigsPaginator = client.get_paginator("list_query_logging_configs")
    list_resource_record_sets_paginator: ListResourceRecordSetsPaginator = client.get_paginator("list_resource_record_sets")
    list_vpc_association_authorizations_paginator: ListVPCAssociationAuthorizationsPaginator = client.get_paginator("list_vpc_association_authorizations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCidrBlocksRequestListCidrBlocksPaginateTypeDef,
    ListCidrBlocksResponseTypeDef,
    ListCidrCollectionsRequestListCidrCollectionsPaginateTypeDef,
    ListCidrCollectionsResponseTypeDef,
    ListCidrLocationsRequestListCidrLocationsPaginateTypeDef,
    ListCidrLocationsResponseTypeDef,
    ListHealthChecksRequestListHealthChecksPaginateTypeDef,
    ListHealthChecksResponseTypeDef,
    ListHostedZonesRequestListHostedZonesPaginateTypeDef,
    ListHostedZonesResponseTypeDef,
    ListQueryLoggingConfigsRequestListQueryLoggingConfigsPaginateTypeDef,
    ListQueryLoggingConfigsResponseTypeDef,
    ListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef,
    ListResourceRecordSetsResponseTypeDef,
    ListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef,
    ListVPCAssociationAuthorizationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCidrBlocksPaginator",
    "ListCidrCollectionsPaginator",
    "ListCidrLocationsPaginator",
    "ListHealthChecksPaginator",
    "ListHostedZonesPaginator",
    "ListQueryLoggingConfigsPaginator",
    "ListResourceRecordSetsPaginator",
    "ListVPCAssociationAuthorizationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCidrBlocksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrBlocks.html#Route53.Paginator.ListCidrBlocks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listcidrblockspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCidrBlocksRequestListCidrBlocksPaginateTypeDef]
    ) -> _PageIterator[ListCidrBlocksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrBlocks.html#Route53.Paginator.ListCidrBlocks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listcidrblockspaginator)
        """

class ListCidrCollectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrCollections.html#Route53.Paginator.ListCidrCollections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listcidrcollectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCidrCollectionsRequestListCidrCollectionsPaginateTypeDef]
    ) -> _PageIterator[ListCidrCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrCollections.html#Route53.Paginator.ListCidrCollections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listcidrcollectionspaginator)
        """

class ListCidrLocationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrLocations.html#Route53.Paginator.ListCidrLocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listcidrlocationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCidrLocationsRequestListCidrLocationsPaginateTypeDef]
    ) -> _PageIterator[ListCidrLocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrLocations.html#Route53.Paginator.ListCidrLocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listcidrlocationspaginator)
        """

class ListHealthChecksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHealthChecks.html#Route53.Paginator.ListHealthChecks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listhealthcheckspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHealthChecksRequestListHealthChecksPaginateTypeDef]
    ) -> _PageIterator[ListHealthChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHealthChecks.html#Route53.Paginator.ListHealthChecks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listhealthcheckspaginator)
        """

class ListHostedZonesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHostedZones.html#Route53.Paginator.ListHostedZones)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listhostedzonespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHostedZonesRequestListHostedZonesPaginateTypeDef]
    ) -> _PageIterator[ListHostedZonesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHostedZones.html#Route53.Paginator.ListHostedZones.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listhostedzonespaginator)
        """

class ListQueryLoggingConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListQueryLoggingConfigs.html#Route53.Paginator.ListQueryLoggingConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listqueryloggingconfigspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueryLoggingConfigsRequestListQueryLoggingConfigsPaginateTypeDef]
    ) -> _PageIterator[ListQueryLoggingConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListQueryLoggingConfigs.html#Route53.Paginator.ListQueryLoggingConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listqueryloggingconfigspaginator)
        """

class ListResourceRecordSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListResourceRecordSets.html#Route53.Paginator.ListResourceRecordSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listresourcerecordsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef]
    ) -> _PageIterator[ListResourceRecordSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListResourceRecordSets.html#Route53.Paginator.ListResourceRecordSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listresourcerecordsetspaginator)
        """

class ListVPCAssociationAuthorizationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListVPCAssociationAuthorizations.html#Route53.Paginator.ListVPCAssociationAuthorizations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listvpcassociationauthorizationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListVPCAssociationAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListVPCAssociationAuthorizations.html#Route53.Paginator.ListVPCAssociationAuthorizations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/paginators/#listvpcassociationauthorizationspaginator)
        """
