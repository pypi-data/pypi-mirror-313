"""
Type annotations for controltower service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_controltower.client import ControlTowerClient
    from mypy_boto3_controltower.paginator import (
        ListBaselinesPaginator,
        ListControlOperationsPaginator,
        ListEnabledBaselinesPaginator,
        ListEnabledControlsPaginator,
        ListLandingZoneOperationsPaginator,
        ListLandingZonesPaginator,
    )

    session = Session()
    client: ControlTowerClient = session.client("controltower")

    list_baselines_paginator: ListBaselinesPaginator = client.get_paginator("list_baselines")
    list_control_operations_paginator: ListControlOperationsPaginator = client.get_paginator("list_control_operations")
    list_enabled_baselines_paginator: ListEnabledBaselinesPaginator = client.get_paginator("list_enabled_baselines")
    list_enabled_controls_paginator: ListEnabledControlsPaginator = client.get_paginator("list_enabled_controls")
    list_landing_zone_operations_paginator: ListLandingZoneOperationsPaginator = client.get_paginator("list_landing_zone_operations")
    list_landing_zones_paginator: ListLandingZonesPaginator = client.get_paginator("list_landing_zones")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBaselinesInputListBaselinesPaginateTypeDef,
    ListBaselinesOutputTypeDef,
    ListControlOperationsInputListControlOperationsPaginateTypeDef,
    ListControlOperationsOutputTypeDef,
    ListEnabledBaselinesInputListEnabledBaselinesPaginateTypeDef,
    ListEnabledBaselinesOutputTypeDef,
    ListEnabledControlsInputListEnabledControlsPaginateTypeDef,
    ListEnabledControlsOutputTypeDef,
    ListLandingZoneOperationsInputListLandingZoneOperationsPaginateTypeDef,
    ListLandingZoneOperationsOutputTypeDef,
    ListLandingZonesInputListLandingZonesPaginateTypeDef,
    ListLandingZonesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListBaselinesPaginator",
    "ListControlOperationsPaginator",
    "ListEnabledBaselinesPaginator",
    "ListEnabledControlsPaginator",
    "ListLandingZoneOperationsPaginator",
    "ListLandingZonesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBaselinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListBaselines.html#ControlTower.Paginator.ListBaselines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listbaselinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBaselinesInputListBaselinesPaginateTypeDef]
    ) -> _PageIterator[ListBaselinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListBaselines.html#ControlTower.Paginator.ListBaselines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listbaselinespaginator)
        """


class ListControlOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListControlOperations.html#ControlTower.Paginator.ListControlOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listcontroloperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListControlOperationsInputListControlOperationsPaginateTypeDef]
    ) -> _PageIterator[ListControlOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListControlOperations.html#ControlTower.Paginator.ListControlOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listcontroloperationspaginator)
        """


class ListEnabledBaselinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListEnabledBaselines.html#ControlTower.Paginator.ListEnabledBaselines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listenabledbaselinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnabledBaselinesInputListEnabledBaselinesPaginateTypeDef]
    ) -> _PageIterator[ListEnabledBaselinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListEnabledBaselines.html#ControlTower.Paginator.ListEnabledBaselines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listenabledbaselinespaginator)
        """


class ListEnabledControlsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListEnabledControls.html#ControlTower.Paginator.ListEnabledControls)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listenabledcontrolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnabledControlsInputListEnabledControlsPaginateTypeDef]
    ) -> _PageIterator[ListEnabledControlsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListEnabledControls.html#ControlTower.Paginator.ListEnabledControls.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listenabledcontrolspaginator)
        """


class ListLandingZoneOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListLandingZoneOperations.html#ControlTower.Paginator.ListLandingZoneOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listlandingzoneoperationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListLandingZoneOperationsInputListLandingZoneOperationsPaginateTypeDef],
    ) -> _PageIterator[ListLandingZoneOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListLandingZoneOperations.html#ControlTower.Paginator.ListLandingZoneOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listlandingzoneoperationspaginator)
        """


class ListLandingZonesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListLandingZones.html#ControlTower.Paginator.ListLandingZones)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listlandingzonespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLandingZonesInputListLandingZonesPaginateTypeDef]
    ) -> _PageIterator[ListLandingZonesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower/paginator/ListLandingZones.html#ControlTower.Paginator.ListLandingZones.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listlandingzonespaginator)
        """
