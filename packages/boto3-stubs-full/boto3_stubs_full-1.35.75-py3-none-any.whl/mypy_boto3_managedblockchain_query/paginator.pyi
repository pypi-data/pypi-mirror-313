"""
Type annotations for managedblockchain-query service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_managedblockchain_query.client import ManagedBlockchainQueryClient
    from mypy_boto3_managedblockchain_query.paginator import (
        ListAssetContractsPaginator,
        ListFilteredTransactionEventsPaginator,
        ListTokenBalancesPaginator,
        ListTransactionEventsPaginator,
        ListTransactionsPaginator,
    )

    session = Session()
    client: ManagedBlockchainQueryClient = session.client("managedblockchain-query")

    list_asset_contracts_paginator: ListAssetContractsPaginator = client.get_paginator("list_asset_contracts")
    list_filtered_transaction_events_paginator: ListFilteredTransactionEventsPaginator = client.get_paginator("list_filtered_transaction_events")
    list_token_balances_paginator: ListTokenBalancesPaginator = client.get_paginator("list_token_balances")
    list_transaction_events_paginator: ListTransactionEventsPaginator = client.get_paginator("list_transaction_events")
    list_transactions_paginator: ListTransactionsPaginator = client.get_paginator("list_transactions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssetContractsInputListAssetContractsPaginateTypeDef,
    ListAssetContractsOutputTypeDef,
    ListFilteredTransactionEventsInputListFilteredTransactionEventsPaginateTypeDef,
    ListFilteredTransactionEventsOutputTypeDef,
    ListTokenBalancesInputListTokenBalancesPaginateTypeDef,
    ListTokenBalancesOutputTypeDef,
    ListTransactionEventsInputListTransactionEventsPaginateTypeDef,
    ListTransactionEventsOutputTypeDef,
    ListTransactionsInputListTransactionsPaginateTypeDef,
    ListTransactionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssetContractsPaginator",
    "ListFilteredTransactionEventsPaginator",
    "ListTokenBalancesPaginator",
    "ListTransactionEventsPaginator",
    "ListTransactionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAssetContractsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListAssetContracts.html#ManagedBlockchainQuery.Paginator.ListAssetContracts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listassetcontractspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssetContractsInputListAssetContractsPaginateTypeDef]
    ) -> _PageIterator[ListAssetContractsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListAssetContracts.html#ManagedBlockchainQuery.Paginator.ListAssetContracts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listassetcontractspaginator)
        """

class ListFilteredTransactionEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListFilteredTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListFilteredTransactionEventsInputListFilteredTransactionEventsPaginateTypeDef
        ],
    ) -> _PageIterator[ListFilteredTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListFilteredTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
        """

class ListTokenBalancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTokenBalances.html#ManagedBlockchainQuery.Paginator.ListTokenBalances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtokenbalancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTokenBalancesInputListTokenBalancesPaginateTypeDef]
    ) -> _PageIterator[ListTokenBalancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTokenBalances.html#ManagedBlockchainQuery.Paginator.ListTokenBalances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtokenbalancespaginator)
        """

class ListTransactionEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactioneventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTransactionEventsInputListTransactionEventsPaginateTypeDef]
    ) -> _PageIterator[ListTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactioneventspaginator)
        """

class ListTransactionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactions.html#ManagedBlockchainQuery.Paginator.ListTransactions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTransactionsInputListTransactionsPaginateTypeDef]
    ) -> _PageIterator[ListTransactionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactions.html#ManagedBlockchainQuery.Paginator.ListTransactions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactionspaginator)
        """
