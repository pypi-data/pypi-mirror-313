"""
Type annotations for license-manager service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_license_manager.client import LicenseManagerClient
    from mypy_boto3_license_manager.paginator import (
        ListAssociationsForLicenseConfigurationPaginator,
        ListLicenseConfigurationsPaginator,
        ListLicenseSpecificationsForResourcePaginator,
        ListResourceInventoryPaginator,
        ListUsageForLicenseConfigurationPaginator,
    )

    session = Session()
    client: LicenseManagerClient = session.client("license-manager")

    list_associations_for_license_configuration_paginator: ListAssociationsForLicenseConfigurationPaginator = client.get_paginator("list_associations_for_license_configuration")
    list_license_configurations_paginator: ListLicenseConfigurationsPaginator = client.get_paginator("list_license_configurations")
    list_license_specifications_for_resource_paginator: ListLicenseSpecificationsForResourcePaginator = client.get_paginator("list_license_specifications_for_resource")
    list_resource_inventory_paginator: ListResourceInventoryPaginator = client.get_paginator("list_resource_inventory")
    list_usage_for_license_configuration_paginator: ListUsageForLicenseConfigurationPaginator = client.get_paginator("list_usage_for_license_configuration")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef,
    ListAssociationsForLicenseConfigurationResponseTypeDef,
    ListLicenseConfigurationsRequestListLicenseConfigurationsPaginateTypeDef,
    ListLicenseConfigurationsResponseTypeDef,
    ListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef,
    ListLicenseSpecificationsForResourceResponseTypeDef,
    ListResourceInventoryRequestListResourceInventoryPaginateTypeDef,
    ListResourceInventoryResponseTypeDef,
    ListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef,
    ListUsageForLicenseConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssociationsForLicenseConfigurationPaginator",
    "ListLicenseConfigurationsPaginator",
    "ListLicenseSpecificationsForResourcePaginator",
    "ListResourceInventoryPaginator",
    "ListUsageForLicenseConfigurationPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssociationsForLicenseConfigurationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListAssociationsForLicenseConfiguration.html#LicenseManager.Paginator.ListAssociationsForLicenseConfiguration)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listassociationsforlicenseconfigurationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef
        ],
    ) -> _PageIterator[ListAssociationsForLicenseConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListAssociationsForLicenseConfiguration.html#LicenseManager.Paginator.ListAssociationsForLicenseConfiguration.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listassociationsforlicenseconfigurationpaginator)
        """


class ListLicenseConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseConfigurations.html#LicenseManager.Paginator.ListLicenseConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listlicenseconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListLicenseConfigurationsRequestListLicenseConfigurationsPaginateTypeDef],
    ) -> _PageIterator[ListLicenseConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseConfigurations.html#LicenseManager.Paginator.ListLicenseConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listlicenseconfigurationspaginator)
        """


class ListLicenseSpecificationsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseSpecificationsForResource.html#LicenseManager.Paginator.ListLicenseSpecificationsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listlicensespecificationsforresourcepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef
        ],
    ) -> _PageIterator[ListLicenseSpecificationsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseSpecificationsForResource.html#LicenseManager.Paginator.ListLicenseSpecificationsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listlicensespecificationsforresourcepaginator)
        """


class ListResourceInventoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListResourceInventory.html#LicenseManager.Paginator.ListResourceInventory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listresourceinventorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceInventoryRequestListResourceInventoryPaginateTypeDef]
    ) -> _PageIterator[ListResourceInventoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListResourceInventory.html#LicenseManager.Paginator.ListResourceInventory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listresourceinventorypaginator)
        """


class ListUsageForLicenseConfigurationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListUsageForLicenseConfiguration.html#LicenseManager.Paginator.ListUsageForLicenseConfiguration)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listusageforlicenseconfigurationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef
        ],
    ) -> _PageIterator[ListUsageForLicenseConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListUsageForLicenseConfiguration.html#LicenseManager.Paginator.ListUsageForLicenseConfiguration.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/paginators/#listusageforlicenseconfigurationpaginator)
        """
