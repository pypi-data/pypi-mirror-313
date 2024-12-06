"""
Type annotations for sms service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sms.client import SMSClient
    from mypy_boto3_sms.paginator import (
        GetConnectorsPaginator,
        GetReplicationJobsPaginator,
        GetReplicationRunsPaginator,
        GetServersPaginator,
        ListAppsPaginator,
    )

    session = Session()
    client: SMSClient = session.client("sms")

    get_connectors_paginator: GetConnectorsPaginator = client.get_paginator("get_connectors")
    get_replication_jobs_paginator: GetReplicationJobsPaginator = client.get_paginator("get_replication_jobs")
    get_replication_runs_paginator: GetReplicationRunsPaginator = client.get_paginator("get_replication_runs")
    get_servers_paginator: GetServersPaginator = client.get_paginator("get_servers")
    list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetConnectorsRequestGetConnectorsPaginateTypeDef,
    GetConnectorsResponseTypeDef,
    GetReplicationJobsRequestGetReplicationJobsPaginateTypeDef,
    GetReplicationJobsResponseTypeDef,
    GetReplicationRunsRequestGetReplicationRunsPaginateTypeDef,
    GetReplicationRunsResponseTypeDef,
    GetServersRequestGetServersPaginateTypeDef,
    GetServersResponseTypeDef,
    ListAppsRequestListAppsPaginateTypeDef,
    ListAppsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetConnectorsPaginator",
    "GetReplicationJobsPaginator",
    "GetReplicationRunsPaginator",
    "GetServersPaginator",
    "ListAppsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetConnectorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetConnectors.html#SMS.Paginator.GetConnectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getconnectorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetConnectorsRequestGetConnectorsPaginateTypeDef]
    ) -> _PageIterator[GetConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetConnectors.html#SMS.Paginator.GetConnectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getconnectorspaginator)
        """


class GetReplicationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationJobs.html#SMS.Paginator.GetReplicationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getreplicationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetReplicationJobsRequestGetReplicationJobsPaginateTypeDef]
    ) -> _PageIterator[GetReplicationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationJobs.html#SMS.Paginator.GetReplicationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getreplicationjobspaginator)
        """


class GetReplicationRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationRuns.html#SMS.Paginator.GetReplicationRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getreplicationrunspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetReplicationRunsRequestGetReplicationRunsPaginateTypeDef]
    ) -> _PageIterator[GetReplicationRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationRuns.html#SMS.Paginator.GetReplicationRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getreplicationrunspaginator)
        """


class GetServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetServers.html#SMS.Paginator.GetServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getserverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetServersRequestGetServersPaginateTypeDef]
    ) -> _PageIterator[GetServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetServers.html#SMS.Paginator.GetServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#getserverspaginator)
        """


class ListAppsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/ListApps.html#SMS.Paginator.ListApps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#listappspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppsRequestListAppsPaginateTypeDef]
    ) -> _PageIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/ListApps.html#SMS.Paginator.ListApps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms/paginators/#listappspaginator)
        """
