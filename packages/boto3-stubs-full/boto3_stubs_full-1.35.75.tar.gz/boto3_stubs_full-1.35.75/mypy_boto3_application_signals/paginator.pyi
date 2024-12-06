"""
Type annotations for application-signals service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_application_signals.client import CloudWatchApplicationSignalsClient
    from mypy_boto3_application_signals.paginator import (
        ListServiceDependenciesPaginator,
        ListServiceDependentsPaginator,
        ListServiceLevelObjectivesPaginator,
        ListServiceOperationsPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: CloudWatchApplicationSignalsClient = session.client("application-signals")

    list_service_dependencies_paginator: ListServiceDependenciesPaginator = client.get_paginator("list_service_dependencies")
    list_service_dependents_paginator: ListServiceDependentsPaginator = client.get_paginator("list_service_dependents")
    list_service_level_objectives_paginator: ListServiceLevelObjectivesPaginator = client.get_paginator("list_service_level_objectives")
    list_service_operations_paginator: ListServiceOperationsPaginator = client.get_paginator("list_service_operations")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListServiceDependenciesInputListServiceDependenciesPaginateTypeDef,
    ListServiceDependenciesOutputTypeDef,
    ListServiceDependentsInputListServiceDependentsPaginateTypeDef,
    ListServiceDependentsOutputTypeDef,
    ListServiceLevelObjectivesInputListServiceLevelObjectivesPaginateTypeDef,
    ListServiceLevelObjectivesOutputTypeDef,
    ListServiceOperationsInputListServiceOperationsPaginateTypeDef,
    ListServiceOperationsOutputTypeDef,
    ListServicesInputListServicesPaginateTypeDef,
    ListServicesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListServiceDependenciesPaginator",
    "ListServiceDependentsPaginator",
    "ListServiceLevelObjectivesPaginator",
    "ListServiceOperationsPaginator",
    "ListServicesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListServiceDependenciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependencies.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependenciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServiceDependenciesInputListServiceDependenciesPaginateTypeDef]
    ) -> _PageIterator[ListServiceDependenciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependencies.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependenciespaginator)
        """

class ListServiceDependentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependents.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServiceDependentsInputListServiceDependentsPaginateTypeDef]
    ) -> _PageIterator[ListServiceDependentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependents.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependentspaginator)
        """

class ListServiceLevelObjectivesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectives.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectivespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListServiceLevelObjectivesInputListServiceLevelObjectivesPaginateTypeDef],
    ) -> _PageIterator[ListServiceLevelObjectivesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectives.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectivespaginator)
        """

class ListServiceOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceOperations.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listserviceoperationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServiceOperationsInputListServiceOperationsPaginateTypeDef]
    ) -> _PageIterator[ListServiceOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceOperations.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listserviceoperationspaginator)
        """

class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServices.html#CloudWatchApplicationSignals.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServicesInputListServicesPaginateTypeDef]
    ) -> _PageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServices.html#CloudWatchApplicationSignals.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicespaginator)
        """
