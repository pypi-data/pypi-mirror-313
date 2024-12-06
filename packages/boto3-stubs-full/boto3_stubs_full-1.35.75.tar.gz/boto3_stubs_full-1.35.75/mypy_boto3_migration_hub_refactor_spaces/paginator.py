"""
Type annotations for migration-hub-refactor-spaces service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_migration_hub_refactor_spaces.client import MigrationHubRefactorSpacesClient
    from mypy_boto3_migration_hub_refactor_spaces.paginator import (
        ListApplicationsPaginator,
        ListEnvironmentVpcsPaginator,
        ListEnvironmentsPaginator,
        ListRoutesPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: MigrationHubRefactorSpacesClient = session.client("migration-hub-refactor-spaces")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_environment_vpcs_paginator: ListEnvironmentVpcsPaginator = client.get_paginator("list_environment_vpcs")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_routes_paginator: ListRoutesPaginator = client.get_paginator("list_routes")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListEnvironmentsRequestListEnvironmentsPaginateTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef,
    ListEnvironmentVpcsResponseTypeDef,
    ListRoutesRequestListRoutesPaginateTypeDef,
    ListRoutesResponseTypeDef,
    ListServicesRequestListServicesPaginateTypeDef,
    ListServicesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationsPaginator",
    "ListEnvironmentVpcsPaginator",
    "ListEnvironmentsPaginator",
    "ListRoutesPaginator",
    "ListServicesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListApplications.html#MigrationHubRefactorSpaces.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListApplications.html#MigrationHubRefactorSpaces.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listapplicationspaginator)
        """


class ListEnvironmentVpcsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironmentVpcs.html#MigrationHubRefactorSpaces.Paginator.ListEnvironmentVpcs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listenvironmentvpcspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef]
    ) -> _PageIterator[ListEnvironmentVpcsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironmentVpcs.html#MigrationHubRefactorSpaces.Paginator.ListEnvironmentVpcs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listenvironmentvpcspaginator)
        """


class ListEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironments.html#MigrationHubRefactorSpaces.Paginator.ListEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listenvironmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsRequestListEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironments.html#MigrationHubRefactorSpaces.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listenvironmentspaginator)
        """


class ListRoutesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListRoutes.html#MigrationHubRefactorSpaces.Paginator.ListRoutes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listroutespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRoutesRequestListRoutesPaginateTypeDef]
    ) -> _PageIterator[ListRoutesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListRoutes.html#MigrationHubRefactorSpaces.Paginator.ListRoutes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listroutespaginator)
        """


class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListServices.html#MigrationHubRefactorSpaces.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listservicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServicesRequestListServicesPaginateTypeDef]
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListServices.html#MigrationHubRefactorSpaces.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/paginators/#listservicespaginator)
        """
