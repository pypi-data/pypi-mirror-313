"""
Type annotations for snow-device-management service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_snow_device_management.client import SnowDeviceManagementClient
    from mypy_boto3_snow_device_management.paginator import (
        ListDeviceResourcesPaginator,
        ListDevicesPaginator,
        ListExecutionsPaginator,
        ListTasksPaginator,
    )

    session = Session()
    client: SnowDeviceManagementClient = session.client("snow-device-management")

    list_device_resources_paginator: ListDeviceResourcesPaginator = client.get_paginator("list_device_resources")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDeviceResourcesInputListDeviceResourcesPaginateTypeDef,
    ListDeviceResourcesOutputTypeDef,
    ListDevicesInputListDevicesPaginateTypeDef,
    ListDevicesOutputTypeDef,
    ListExecutionsInputListExecutionsPaginateTypeDef,
    ListExecutionsOutputTypeDef,
    ListTasksInputListTasksPaginateTypeDef,
    ListTasksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDeviceResourcesPaginator",
    "ListDevicesPaginator",
    "ListExecutionsPaginator",
    "ListTasksPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDeviceResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDeviceResources.html#SnowDeviceManagement.Paginator.ListDeviceResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listdeviceresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeviceResourcesInputListDeviceResourcesPaginateTypeDef]
    ) -> _PageIterator[ListDeviceResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDeviceResources.html#SnowDeviceManagement.Paginator.ListDeviceResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listdeviceresourcespaginator)
        """


class ListDevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDevices.html#SnowDeviceManagement.Paginator.ListDevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listdevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDevicesInputListDevicesPaginateTypeDef]
    ) -> _PageIterator[ListDevicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDevices.html#SnowDeviceManagement.Paginator.ListDevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listdevicespaginator)
        """


class ListExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListExecutions.html#SnowDeviceManagement.Paginator.ListExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExecutionsInputListExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListExecutions.html#SnowDeviceManagement.Paginator.ListExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listexecutionspaginator)
        """


class ListTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListTasks.html#SnowDeviceManagement.Paginator.ListTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listtaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTasksInputListTasksPaginateTypeDef]
    ) -> _PageIterator[ListTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListTasks.html#SnowDeviceManagement.Paginator.ListTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/paginators/#listtaskspaginator)
        """
