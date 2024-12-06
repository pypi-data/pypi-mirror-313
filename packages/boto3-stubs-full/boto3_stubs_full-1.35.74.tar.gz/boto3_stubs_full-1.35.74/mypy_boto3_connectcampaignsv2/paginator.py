"""
Type annotations for connectcampaignsv2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_connectcampaignsv2.client import ConnectCampaignServiceV2Client
    from mypy_boto3_connectcampaignsv2.paginator import (
        ListCampaignsPaginator,
        ListConnectInstanceIntegrationsPaginator,
    )

    session = Session()
    client: ConnectCampaignServiceV2Client = session.client("connectcampaignsv2")

    list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    list_connect_instance_integrations_paginator: ListConnectInstanceIntegrationsPaginator = client.get_paginator("list_connect_instance_integrations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCampaignsRequestListCampaignsPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListConnectInstanceIntegrationsRequestListConnectInstanceIntegrationsPaginateTypeDef,
    ListConnectInstanceIntegrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListCampaignsPaginator", "ListConnectInstanceIntegrationsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCampaignsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListCampaigns.html#ConnectCampaignServiceV2.Paginator.ListCampaigns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/paginators/#listcampaignspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCampaignsRequestListCampaignsPaginateTypeDef]
    ) -> _PageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListCampaigns.html#ConnectCampaignServiceV2.Paginator.ListCampaigns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/paginators/#listcampaignspaginator)
        """


class ListConnectInstanceIntegrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListConnectInstanceIntegrations.html#ConnectCampaignServiceV2.Paginator.ListConnectInstanceIntegrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/paginators/#listconnectinstanceintegrationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListConnectInstanceIntegrationsRequestListConnectInstanceIntegrationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConnectInstanceIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListConnectInstanceIntegrations.html#ConnectCampaignServiceV2.Paginator.ListConnectInstanceIntegrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/paginators/#listconnectinstanceintegrationspaginator)
        """
