"""
Type annotations for ds service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ds.client import DirectoryServiceClient
    from mypy_boto3_ds.paginator import (
        DescribeClientAuthenticationSettingsPaginator,
        DescribeDirectoriesPaginator,
        DescribeDomainControllersPaginator,
        DescribeLDAPSSettingsPaginator,
        DescribeRegionsPaginator,
        DescribeSharedDirectoriesPaginator,
        DescribeSnapshotsPaginator,
        DescribeTrustsPaginator,
        DescribeUpdateDirectoryPaginator,
        ListCertificatesPaginator,
        ListIpRoutesPaginator,
        ListLogSubscriptionsPaginator,
        ListSchemaExtensionsPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: DirectoryServiceClient = session.client("ds")

    describe_client_authentication_settings_paginator: DescribeClientAuthenticationSettingsPaginator = client.get_paginator("describe_client_authentication_settings")
    describe_directories_paginator: DescribeDirectoriesPaginator = client.get_paginator("describe_directories")
    describe_domain_controllers_paginator: DescribeDomainControllersPaginator = client.get_paginator("describe_domain_controllers")
    describe_ldaps_settings_paginator: DescribeLDAPSSettingsPaginator = client.get_paginator("describe_ldaps_settings")
    describe_regions_paginator: DescribeRegionsPaginator = client.get_paginator("describe_regions")
    describe_shared_directories_paginator: DescribeSharedDirectoriesPaginator = client.get_paginator("describe_shared_directories")
    describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
    describe_trusts_paginator: DescribeTrustsPaginator = client.get_paginator("describe_trusts")
    describe_update_directory_paginator: DescribeUpdateDirectoryPaginator = client.get_paginator("describe_update_directory")
    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    list_ip_routes_paginator: ListIpRoutesPaginator = client.get_paginator("list_ip_routes")
    list_log_subscriptions_paginator: ListLogSubscriptionsPaginator = client.get_paginator("list_log_subscriptions")
    list_schema_extensions_paginator: ListSchemaExtensionsPaginator = client.get_paginator("list_schema_extensions")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeClientAuthenticationSettingsRequestDescribeClientAuthenticationSettingsPaginateTypeDef,
    DescribeClientAuthenticationSettingsResultTypeDef,
    DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef,
    DescribeDirectoriesResultTypeDef,
    DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef,
    DescribeDomainControllersResultTypeDef,
    DescribeLDAPSSettingsRequestDescribeLDAPSSettingsPaginateTypeDef,
    DescribeLDAPSSettingsResultTypeDef,
    DescribeRegionsRequestDescribeRegionsPaginateTypeDef,
    DescribeRegionsResultTypeDef,
    DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef,
    DescribeSharedDirectoriesResultTypeDef,
    DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef,
    DescribeSnapshotsResultTypeDef,
    DescribeTrustsRequestDescribeTrustsPaginateTypeDef,
    DescribeTrustsResultTypeDef,
    DescribeUpdateDirectoryRequestDescribeUpdateDirectoryPaginateTypeDef,
    DescribeUpdateDirectoryResultTypeDef,
    ListCertificatesRequestListCertificatesPaginateTypeDef,
    ListCertificatesResultTypeDef,
    ListIpRoutesRequestListIpRoutesPaginateTypeDef,
    ListIpRoutesResultTypeDef,
    ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef,
    ListLogSubscriptionsResultTypeDef,
    ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef,
    ListSchemaExtensionsResultTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeClientAuthenticationSettingsPaginator",
    "DescribeDirectoriesPaginator",
    "DescribeDomainControllersPaginator",
    "DescribeLDAPSSettingsPaginator",
    "DescribeRegionsPaginator",
    "DescribeSharedDirectoriesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeTrustsPaginator",
    "DescribeUpdateDirectoryPaginator",
    "ListCertificatesPaginator",
    "ListIpRoutesPaginator",
    "ListLogSubscriptionsPaginator",
    "ListSchemaExtensionsPaginator",
    "ListTagsForResourcePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeClientAuthenticationSettingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeClientAuthenticationSettings.html#DirectoryService.Paginator.DescribeClientAuthenticationSettings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeclientauthenticationsettingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClientAuthenticationSettingsRequestDescribeClientAuthenticationSettingsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeClientAuthenticationSettingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeClientAuthenticationSettings.html#DirectoryService.Paginator.DescribeClientAuthenticationSettings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeclientauthenticationsettingspaginator)
        """


class DescribeDirectoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDirectories.html#DirectoryService.Paginator.DescribeDirectories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describedirectoriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef]
    ) -> _PageIterator[DescribeDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDirectories.html#DirectoryService.Paginator.DescribeDirectories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describedirectoriespaginator)
        """


class DescribeDomainControllersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDomainControllers.html#DirectoryService.Paginator.DescribeDomainControllers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describedomaincontrollerspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef],
    ) -> _PageIterator[DescribeDomainControllersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDomainControllers.html#DirectoryService.Paginator.DescribeDomainControllers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describedomaincontrollerspaginator)
        """


class DescribeLDAPSSettingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeLDAPSSettings.html#DirectoryService.Paginator.DescribeLDAPSSettings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeldapssettingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeLDAPSSettingsRequestDescribeLDAPSSettingsPaginateTypeDef]
    ) -> _PageIterator[DescribeLDAPSSettingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeLDAPSSettings.html#DirectoryService.Paginator.DescribeLDAPSSettings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeldapssettingspaginator)
        """


class DescribeRegionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeRegions.html#DirectoryService.Paginator.DescribeRegions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeregionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeRegionsRequestDescribeRegionsPaginateTypeDef]
    ) -> _PageIterator[DescribeRegionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeRegions.html#DirectoryService.Paginator.DescribeRegions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeregionspaginator)
        """


class DescribeSharedDirectoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSharedDirectories.html#DirectoryService.Paginator.DescribeSharedDirectories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeshareddirectoriespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef],
    ) -> _PageIterator[DescribeSharedDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSharedDirectories.html#DirectoryService.Paginator.DescribeSharedDirectories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeshareddirectoriespaginator)
        """


class DescribeSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSnapshots.html#DirectoryService.Paginator.DescribeSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describesnapshotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef]
    ) -> _PageIterator[DescribeSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSnapshots.html#DirectoryService.Paginator.DescribeSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describesnapshotspaginator)
        """


class DescribeTrustsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeTrusts.html#DirectoryService.Paginator.DescribeTrusts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describetrustspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeTrustsRequestDescribeTrustsPaginateTypeDef]
    ) -> _PageIterator[DescribeTrustsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeTrusts.html#DirectoryService.Paginator.DescribeTrusts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describetrustspaginator)
        """


class DescribeUpdateDirectoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeUpdateDirectory.html#DirectoryService.Paginator.DescribeUpdateDirectory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeupdatedirectorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeUpdateDirectoryRequestDescribeUpdateDirectoryPaginateTypeDef]
    ) -> _PageIterator[DescribeUpdateDirectoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeUpdateDirectory.html#DirectoryService.Paginator.DescribeUpdateDirectory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#describeupdatedirectorypaginator)
        """


class ListCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListCertificates.html#DirectoryService.Paginator.ListCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listcertificatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCertificatesRequestListCertificatesPaginateTypeDef]
    ) -> _PageIterator[ListCertificatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListCertificates.html#DirectoryService.Paginator.ListCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listcertificatespaginator)
        """


class ListIpRoutesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListIpRoutes.html#DirectoryService.Paginator.ListIpRoutes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listiproutespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIpRoutesRequestListIpRoutesPaginateTypeDef]
    ) -> _PageIterator[ListIpRoutesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListIpRoutes.html#DirectoryService.Paginator.ListIpRoutes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listiproutespaginator)
        """


class ListLogSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListLogSubscriptions.html#DirectoryService.Paginator.ListLogSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listlogsubscriptionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef]
    ) -> _PageIterator[ListLogSubscriptionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListLogSubscriptions.html#DirectoryService.Paginator.ListLogSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listlogsubscriptionspaginator)
        """


class ListSchemaExtensionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListSchemaExtensions.html#DirectoryService.Paginator.ListSchemaExtensions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listschemaextensionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef]
    ) -> _PageIterator[ListSchemaExtensionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListSchemaExtensions.html#DirectoryService.Paginator.ListSchemaExtensions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listschemaextensionspaginator)
        """


class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListTagsForResource.html#DirectoryService.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListTagsForResource.html#DirectoryService.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/paginators/#listtagsforresourcepaginator)
        """
