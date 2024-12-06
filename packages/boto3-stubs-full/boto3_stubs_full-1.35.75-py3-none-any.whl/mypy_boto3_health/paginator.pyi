"""
Type annotations for health service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_health.client import HealthClient
    from mypy_boto3_health.paginator import (
        DescribeAffectedAccountsForOrganizationPaginator,
        DescribeAffectedEntitiesForOrganizationPaginator,
        DescribeAffectedEntitiesPaginator,
        DescribeEventAggregatesPaginator,
        DescribeEventTypesPaginator,
        DescribeEventsForOrganizationPaginator,
        DescribeEventsPaginator,
    )

    session = Session()
    client: HealthClient = session.client("health")

    describe_affected_accounts_for_organization_paginator: DescribeAffectedAccountsForOrganizationPaginator = client.get_paginator("describe_affected_accounts_for_organization")
    describe_affected_entities_for_organization_paginator: DescribeAffectedEntitiesForOrganizationPaginator = client.get_paginator("describe_affected_entities_for_organization")
    describe_affected_entities_paginator: DescribeAffectedEntitiesPaginator = client.get_paginator("describe_affected_entities")
    describe_event_aggregates_paginator: DescribeEventAggregatesPaginator = client.get_paginator("describe_event_aggregates")
    describe_event_types_paginator: DescribeEventTypesPaginator = client.get_paginator("describe_event_types")
    describe_events_for_organization_paginator: DescribeEventsForOrganizationPaginator = client.get_paginator("describe_events_for_organization")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef,
    DescribeAffectedAccountsForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef,
    DescribeAffectedEntitiesForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef,
    DescribeAffectedEntitiesResponseTypeDef,
    DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef,
    DescribeEventAggregatesResponseTypeDef,
    DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef,
    DescribeEventsForOrganizationResponseTypeDef,
    DescribeEventsRequestDescribeEventsPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef,
    DescribeEventTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAffectedAccountsForOrganizationPaginator",
    "DescribeAffectedEntitiesForOrganizationPaginator",
    "DescribeAffectedEntitiesPaginator",
    "DescribeEventAggregatesPaginator",
    "DescribeEventTypesPaginator",
    "DescribeEventsForOrganizationPaginator",
    "DescribeEventsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAffectedAccountsForOrganizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedAccountsForOrganization.html#Health.Paginator.DescribeAffectedAccountsForOrganization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeaffectedaccountsfororganizationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAffectedAccountsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedAccountsForOrganization.html#Health.Paginator.DescribeAffectedAccountsForOrganization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeaffectedaccountsfororganizationpaginator)
        """

class DescribeAffectedEntitiesForOrganizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntitiesForOrganization.html#Health.Paginator.DescribeAffectedEntitiesForOrganization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeaffectedentitiesfororganizationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAffectedEntitiesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntitiesForOrganization.html#Health.Paginator.DescribeAffectedEntitiesForOrganization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeaffectedentitiesfororganizationpaginator)
        """

class DescribeAffectedEntitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntities.html#Health.Paginator.DescribeAffectedEntities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeaffectedentitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef],
    ) -> _PageIterator[DescribeAffectedEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntities.html#Health.Paginator.DescribeAffectedEntities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeaffectedentitiespaginator)
        """

class DescribeEventAggregatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventAggregates.html#Health.Paginator.DescribeEventAggregates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventaggregatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef]
    ) -> _PageIterator[DescribeEventAggregatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventAggregates.html#Health.Paginator.DescribeEventAggregates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventaggregatespaginator)
        """

class DescribeEventTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventTypes.html#Health.Paginator.DescribeEventTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef]
    ) -> _PageIterator[DescribeEventTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventTypes.html#Health.Paginator.DescribeEventTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventtypespaginator)
        """

class DescribeEventsForOrganizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventsForOrganization.html#Health.Paginator.DescribeEventsForOrganization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventsfororganizationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeEventsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventsForOrganization.html#Health.Paginator.DescribeEventsForOrganization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventsfororganizationpaginator)
        """

class DescribeEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEvents.html#Health.Paginator.DescribeEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsRequestDescribeEventsPaginateTypeDef]
    ) -> _PageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEvents.html#Health.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/paginators/#describeeventspaginator)
        """
