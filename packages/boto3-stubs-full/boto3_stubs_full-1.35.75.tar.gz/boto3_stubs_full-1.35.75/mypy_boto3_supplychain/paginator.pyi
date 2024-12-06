"""
Type annotations for supplychain service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_supplychain.client import SupplyChainClient
    from mypy_boto3_supplychain.paginator import (
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListInstancesPaginator,
    )

    session = Session()
    client: SupplyChainClient = session.client("supplychain")

    list_data_integration_flows_paginator: ListDataIntegrationFlowsPaginator = client.get_paginator("list_data_integration_flows")
    list_data_lake_datasets_paginator: ListDataLakeDatasetsPaginator = client.get_paginator("list_data_lake_datasets")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDataIntegrationFlowsRequestListDataIntegrationFlowsPaginateTypeDef,
    ListDataIntegrationFlowsResponseTypeDef,
    ListDataLakeDatasetsRequestListDataLakeDatasetsPaginateTypeDef,
    ListDataLakeDatasetsResponseTypeDef,
    ListInstancesRequestListInstancesPaginateTypeDef,
    ListInstancesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDataIntegrationFlowsPaginator",
    "ListDataLakeDatasetsPaginator",
    "ListInstancesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDataIntegrationFlowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListDataIntegrationFlowsRequestListDataIntegrationFlowsPaginateTypeDef],
    ) -> _PageIterator[ListDataIntegrationFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowspaginator)
        """

class ListDataLakeDatasetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakedatasetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestListDataLakeDatasetsPaginateTypeDef]
    ) -> _PageIterator[ListDataLakeDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakedatasetspaginator)
        """

class ListInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstancesRequestListInstancesPaginateTypeDef]
    ) -> _PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listinstancespaginator)
        """
