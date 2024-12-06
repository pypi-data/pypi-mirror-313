"""
Type annotations for license-manager-user-subscriptions service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_license_manager_user_subscriptions.client import LicenseManagerUserSubscriptionsClient
    from mypy_boto3_license_manager_user_subscriptions.paginator import (
        ListIdentityProvidersPaginator,
        ListInstancesPaginator,
        ListLicenseServerEndpointsPaginator,
        ListProductSubscriptionsPaginator,
        ListUserAssociationsPaginator,
    )

    session = Session()
    client: LicenseManagerUserSubscriptionsClient = session.client("license-manager-user-subscriptions")

    list_identity_providers_paginator: ListIdentityProvidersPaginator = client.get_paginator("list_identity_providers")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_license_server_endpoints_paginator: ListLicenseServerEndpointsPaginator = client.get_paginator("list_license_server_endpoints")
    list_product_subscriptions_paginator: ListProductSubscriptionsPaginator = client.get_paginator("list_product_subscriptions")
    list_user_associations_paginator: ListUserAssociationsPaginator = client.get_paginator("list_user_associations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListInstancesRequestListInstancesPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListLicenseServerEndpointsRequestListLicenseServerEndpointsPaginateTypeDef,
    ListLicenseServerEndpointsResponseTypeDef,
    ListProductSubscriptionsRequestListProductSubscriptionsPaginateTypeDef,
    ListProductSubscriptionsResponseTypeDef,
    ListUserAssociationsRequestListUserAssociationsPaginateTypeDef,
    ListUserAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListIdentityProvidersPaginator",
    "ListInstancesPaginator",
    "ListLicenseServerEndpointsPaginator",
    "ListProductSubscriptionsPaginator",
    "ListUserAssociationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListIdentityProvidersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListIdentityProviders.html#LicenseManagerUserSubscriptions.Paginator.ListIdentityProviders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listidentityproviderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef]
    ) -> _PageIterator[ListIdentityProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListIdentityProviders.html#LicenseManagerUserSubscriptions.Paginator.ListIdentityProviders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listidentityproviderspaginator)
        """


class ListInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListInstances.html#LicenseManagerUserSubscriptions.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstancesRequestListInstancesPaginateTypeDef]
    ) -> _PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListInstances.html#LicenseManagerUserSubscriptions.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listinstancespaginator)
        """


class ListLicenseServerEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListLicenseServerEndpoints.html#LicenseManagerUserSubscriptions.Paginator.ListLicenseServerEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listlicenseserverendpointspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListLicenseServerEndpointsRequestListLicenseServerEndpointsPaginateTypeDef
        ],
    ) -> _PageIterator[ListLicenseServerEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListLicenseServerEndpoints.html#LicenseManagerUserSubscriptions.Paginator.ListLicenseServerEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listlicenseserverendpointspaginator)
        """


class ListProductSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListProductSubscriptions.html#LicenseManagerUserSubscriptions.Paginator.ListProductSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listproductsubscriptionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListProductSubscriptionsRequestListProductSubscriptionsPaginateTypeDef],
    ) -> _PageIterator[ListProductSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListProductSubscriptions.html#LicenseManagerUserSubscriptions.Paginator.ListProductSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listproductsubscriptionspaginator)
        """


class ListUserAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListUserAssociations.html#LicenseManagerUserSubscriptions.Paginator.ListUserAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listuserassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUserAssociationsRequestListUserAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListUserAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListUserAssociations.html#LicenseManagerUserSubscriptions.Paginator.ListUserAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager_user_subscriptions/paginators/#listuserassociationspaginator)
        """
