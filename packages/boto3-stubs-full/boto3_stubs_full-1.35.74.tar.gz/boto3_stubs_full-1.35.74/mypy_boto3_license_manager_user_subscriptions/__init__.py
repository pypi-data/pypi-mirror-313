"""
Main interface for license-manager-user-subscriptions service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_license_manager_user_subscriptions import (
        Client,
        LicenseManagerUserSubscriptionsClient,
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

from .client import LicenseManagerUserSubscriptionsClient
from .paginator import (
    ListIdentityProvidersPaginator,
    ListInstancesPaginator,
    ListLicenseServerEndpointsPaginator,
    ListProductSubscriptionsPaginator,
    ListUserAssociationsPaginator,
)

Client = LicenseManagerUserSubscriptionsClient


__all__ = (
    "Client",
    "LicenseManagerUserSubscriptionsClient",
    "ListIdentityProvidersPaginator",
    "ListInstancesPaginator",
    "ListLicenseServerEndpointsPaginator",
    "ListProductSubscriptionsPaginator",
    "ListUserAssociationsPaginator",
)
