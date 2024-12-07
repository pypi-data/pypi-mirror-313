"""
Type annotations for iot1click-devices service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot1click_devices.client import IoT1ClickDevicesServiceClient
    from mypy_boto3_iot1click_devices.paginator import (
        ListDeviceEventsPaginator,
        ListDevicesPaginator,
    )

    session = Session()
    client: IoT1ClickDevicesServiceClient = session.client("iot1click-devices")

    list_device_events_paginator: ListDeviceEventsPaginator = client.get_paginator("list_device_events")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDeviceEventsRequestListDeviceEventsPaginateTypeDef,
    ListDeviceEventsResponseTypeDef,
    ListDevicesRequestListDevicesPaginateTypeDef,
    ListDevicesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListDeviceEventsPaginator", "ListDevicesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDeviceEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDeviceEvents.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators/#listdeviceeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeviceEventsRequestListDeviceEventsPaginateTypeDef]
    ) -> _PageIterator[ListDeviceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDeviceEvents.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators/#listdeviceeventspaginator)
        """


class ListDevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDevices.html#IoT1ClickDevicesService.Paginator.ListDevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators/#listdevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDevicesRequestListDevicesPaginateTypeDef]
    ) -> _PageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDevices.html#IoT1ClickDevicesService.Paginator.ListDevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators/#listdevicespaginator)
        """
