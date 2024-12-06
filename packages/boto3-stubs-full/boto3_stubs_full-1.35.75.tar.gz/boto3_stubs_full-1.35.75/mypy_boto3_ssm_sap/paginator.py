"""
Type annotations for ssm-sap service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ssm_sap.client import SsmSapClient
    from mypy_boto3_ssm_sap.paginator import (
        ListApplicationsPaginator,
        ListComponentsPaginator,
        ListDatabasesPaginator,
        ListOperationEventsPaginator,
        ListOperationsPaginator,
    )

    session = Session()
    client: SsmSapClient = session.client("ssm-sap")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_operation_events_paginator: ListOperationEventsPaginator = client.get_paginator("list_operation_events")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApplicationsInputListApplicationsPaginateTypeDef,
    ListApplicationsOutputTypeDef,
    ListComponentsInputListComponentsPaginateTypeDef,
    ListComponentsOutputTypeDef,
    ListDatabasesInputListDatabasesPaginateTypeDef,
    ListDatabasesOutputTypeDef,
    ListOperationEventsInputListOperationEventsPaginateTypeDef,
    ListOperationEventsOutputTypeDef,
    ListOperationsInputListOperationsPaginateTypeDef,
    ListOperationsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationsPaginator",
    "ListComponentsPaginator",
    "ListDatabasesPaginator",
    "ListOperationEventsPaginator",
    "ListOperationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListApplications.html#SsmSap.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsInputListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListApplications.html#SsmSap.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listapplicationspaginator)
        """


class ListComponentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListComponents.html#SsmSap.Paginator.ListComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listcomponentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComponentsInputListComponentsPaginateTypeDef]
    ) -> _PageIterator[ListComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListComponents.html#SsmSap.Paginator.ListComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listcomponentspaginator)
        """


class ListDatabasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListDatabases.html#SsmSap.Paginator.ListDatabases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listdatabasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDatabasesInputListDatabasesPaginateTypeDef]
    ) -> _PageIterator[ListDatabasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListDatabases.html#SsmSap.Paginator.ListDatabases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listdatabasespaginator)
        """


class ListOperationEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperationEvents.html#SsmSap.Paginator.ListOperationEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listoperationeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOperationEventsInputListOperationEventsPaginateTypeDef]
    ) -> _PageIterator[ListOperationEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperationEvents.html#SsmSap.Paginator.ListOperationEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listoperationeventspaginator)
        """


class ListOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperations.html#SsmSap.Paginator.ListOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOperationsInputListOperationsPaginateTypeDef]
    ) -> _PageIterator[ListOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperations.html#SsmSap.Paginator.ListOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/paginators/#listoperationspaginator)
        """
